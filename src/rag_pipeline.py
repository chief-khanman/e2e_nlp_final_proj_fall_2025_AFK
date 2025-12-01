from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_core.callbacks import StreamingStdOutCallbackHandler

from vector_store import VectorStoreManager
from prompts import (
    SYSTEM_PROMPT,
    POSTSECONDARY_GOALS_PROMPT,
    ANNUAL_GOAL_PROMPT,
    SHORT_TERM_OBJECTIVES_PROMPT,
    EXPLANATION_PROMPT,
    COMPLETE_IEP_PROMPT
)
from config import config

class IEPRAGPipeline:
    """RAG Pipeline for generating IEP goals"""

    def __init__(self, use_openai: bool = True, model_name: Optional[str] = None):
        """
        Initialize the RAG pipeline

        Args:
            use_openai: If True, use OpenAI. Otherwise use Ollama.
            model_name: Specific model name to use
        """
        self.use_openai = use_openai

        # Initialize vector store with HuggingFace embeddings
        # (must match the embeddings used during setup.py)
        self.vector_store_manager = VectorStoreManager(
            use_openai_embeddings=False  # Always use HuggingFace for consistency
        )
        self.vector_store_manager.get_or_create_vector_store()
        self.retriever = self.vector_store_manager.get_retriever()

        # Initialize LLM
        if use_openai:
            if not config.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env file")

            model_name = model_name or config.LLM_MODEL
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=config.LLM_TEMPERATURE,
                max_tokens=config.LLM_MAX_TOKENS,
                openai_api_key=config.OPENAI_API_KEY
            )
        else:
            # Use Ollama for local LLM
            model_name = model_name or "llama2"
            self.llm = Ollama(
                model=model_name,
                temperature=config.LLM_TEMPERATURE,
                callbacks=[StreamingStdOutCallbackHandler()]
            )

        print(f"Initialized RAG pipeline with {'OpenAI' if use_openai else 'Ollama'} LLM")

    def retrieve_relevant_context(
        self,
        query: str,
        k: int = None,
        filter_by_type: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Retrieve relevant context for a query

        Args:
            query: Search query
            k: Number of results to return
            filter_by_type: Filter results by document type

        Returns:
            List of relevant documents with metadata
        """
        k = k or config.TOP_K_RESULTS

        if filter_by_type:
            results = []
            for doc_type in filter_by_type:
                type_results = self.vector_store_manager.similarity_search(
                    query,
                    k=k,
                    filter_metadata={"type": doc_type}
                )
                results.extend(type_results)
        else:
            results = self.vector_store_manager.similarity_search(query, k=k)

        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in results
        ]

    def format_context(self, documents: List[Dict]) -> str:
        """Format retrieved documents into context string"""
        context_parts = []

        for i, doc in enumerate(documents, 1):
            source = doc['metadata'].get('source', 'Unknown')
            doc_type = doc['metadata'].get('type', 'Unknown')
            content = doc['content']

            context_parts.append(f"--- Document {i} (Source: {source}, Type: {doc_type}) ---\n{content}\n")

        return "\n".join(context_parts)

    def generate_postsecondary_goals(self, student_info: Dict) -> str:
        """
        Generate postsecondary goals for a student

        Args:
            student_info: Dictionary containing student information

        Returns:
            Generated postsecondary goals
        """
        # Create query for retrieval
        query = f"Career information for {student_info.get('interests', '')}. "
        query += f"Requirements for {student_info.get('career_interest', '')}."

        # Retrieve relevant context
        occupation_docs = self.retrieve_relevant_context(
            query,
            k=3,
            filter_by_type=["occupation_data"]
        )

        goal_template_docs = self.retrieve_relevant_context(
            "postsecondary employment and education goals",
            k=2,
            filter_by_type=["postsecondary_goal_template"]
        )

        all_docs = occupation_docs + goal_template_docs
        context = self.format_context(all_docs)

        # Format student info
        student_info_str = self._format_student_info(student_info)

        # Generate goals
        prompt = POSTSECONDARY_GOALS_PROMPT.format(
            student_info=student_info_str,
            context=context
        )

        response = self.llm.invoke(prompt)

        # Extract text from response
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)

    def generate_annual_goal(self, student_info: Dict, postsecondary_goals: str) -> str:
        """
        Generate annual goal aligned with postsecondary goals

        Args:
            student_info: Dictionary containing student information
            postsecondary_goals: Previously generated postsecondary goals

        Returns:
            Generated annual goal with standards alignment
        """
        # Retrieve relevant standards and skills
        query = f"Skills and standards for {student_info.get('career_interest', '')} and workplace communication"

        standards_docs = self.retrieve_relevant_context(
            query,
            k=3,
            filter_by_type=["educational_standard", "employability_skill"]
        )

        annual_goal_docs = self.retrieve_relevant_context(
            "annual IEP goals for employment skills",
            k=2,
            filter_by_type=["annual_goal_template"]
        )

        occupation_docs = self.retrieve_relevant_context(
            f"{student_info.get('career_interest', '')} requirements",
            k=2,
            filter_by_type=["occupation_data"]
        )

        all_docs = standards_docs + annual_goal_docs + occupation_docs
        context = self.format_context(all_docs)

        # Format student info
        student_info_str = self._format_student_info(student_info)

        # Generate annual goal
        prompt = ANNUAL_GOAL_PROMPT.format(
            student_info=student_info_str,
            postsecondary_goals=postsecondary_goals,
            context=context
        )

        response = self.llm.invoke(prompt)

        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)

    def generate_short_term_objectives(
        self,
        student_info: Dict,
        annual_goal: str
    ) -> str:
        """
        Generate short-term objectives that support the annual goal

        Args:
            student_info: Dictionary containing student information
            annual_goal: Previously generated annual goal

        Returns:
            Generated short-term objectives
        """
        # Retrieve objective templates and progression examples
        objective_docs = self.retrieve_relevant_context(
            "short-term objectives benchmarks progression",
            k=3,
            filter_by_type=["short_term_objective_template", "annual_goal_template"]
        )

        context = self.format_context(objective_docs)

        # Format student info
        student_info_str = self._format_student_info(student_info)

        # Generate objectives
        prompt = SHORT_TERM_OBJECTIVES_PROMPT.format(
            student_info=student_info_str,
            annual_goal=annual_goal,
            context=context
        )

        response = self.llm.invoke(prompt)

        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)

    def generate_complete_iep(self, student_info: Dict) -> Dict[str, str]:
        """
        Generate complete IEP with all components

        Args:
            student_info: Dictionary containing student information

        Returns:
            Dictionary containing all IEP components
        """
        print("Generating complete IEP...")

        # Retrieve comprehensive context
        career_query = f"{student_info.get('interests', '')} {student_info.get('career_interest', '')} career requirements"
        career_docs = self.retrieve_relevant_context(career_query, k=3, filter_by_type=["occupation_data"])

        standards_docs = self.retrieve_relevant_context(
            "employability skills workplace standards communication",
            k=3,
            filter_by_type=["educational_standard", "employability_skill"]
        )

        template_docs = self.retrieve_relevant_context(
            "IEP goals objectives transition planning",
            k=4,
            filter_by_type=["postsecondary_goal_template", "annual_goal_template", "short_term_objective_template"]
        )

        all_docs = career_docs + standards_docs + template_docs
        context = self.format_context(all_docs)

        # Generate complete IEP
        prompt = COMPLETE_IEP_PROMPT.format(
            student_name=student_info.get('name', 'Student'),
            age=student_info.get('age', ''),
            grade=student_info.get('grade', ''),
            disability=student_info.get('disability', ''),
            interests=student_info.get('interests', ''),
            assessment_results=student_info.get('assessment_results', ''),
            context=context
        )

        response = self.llm.invoke(prompt)

        if hasattr(response, 'content'):
            result = response.content
        else:
            result = str(response)

        print("IEP generation complete")

        return {
            "complete_iep": result,
            "student_info": student_info,
            "context_documents": all_docs
        }

    def _format_student_info(self, student_info: Dict) -> str:
        """Format student information dictionary into readable string"""
        info_parts = []

        if student_info.get('name'):
            info_parts.append(f"Name: {student_info['name']}")
        if student_info.get('age'):
            info_parts.append(f"Age: {student_info['age']}")
        if student_info.get('grade'):
            info_parts.append(f"Grade: {student_info['grade']}")
        if student_info.get('disability'):
            info_parts.append(f"Disability: {student_info['disability']}")
        if student_info.get('interests'):
            info_parts.append(f"Interests: {student_info['interests']}")
        if student_info.get('career_interest'):
            info_parts.append(f"Career Interest: {student_info['career_interest']}")
        if student_info.get('assessment_results'):
            info_parts.append(f"Assessment Results: {student_info['assessment_results']}")
        if student_info.get('additional_info'):
            info_parts.append(f"Additional Information: {student_info['additional_info']}")

        return "\n".join(info_parts)


if __name__ == "__main__":
    # Test with sample student (Clarence from the project description)
    sample_student = {
        "name": "Clarence",
        "age": "15",
        "grade": "10th grade (Sophomore)",
        "disability": "Behavior disorder",
        "interests": "Enterprising activities, hands-on learning",
        "career_interest": "Retail sales, driver/sales worker, working at Walmart",
        "assessment_results": "O*Net Interest Profiler shows strength in Enterprising category. Vision for the Future interview indicates interest in working at Walmart as a sales associate."
    }

    print("Initializing RAG Pipeline...")
    pipeline = IEPRAGPipeline(use_openai=True)

    print("\nGenerating IEP for Clarence...")
    result = pipeline.generate_complete_iep(sample_student)

    print("\n" + "="*80)
    print("GENERATED IEP")
    print("="*80)
    print(result["complete_iep"])
