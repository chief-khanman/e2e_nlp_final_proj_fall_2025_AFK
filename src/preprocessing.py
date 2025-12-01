import json
from pathlib import Path
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import config

class DocumentPreprocessor:
    """Preprocesses and chunks documents for the RAG system"""

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def load_json_file(self, filepath: Path) -> Dict:
        """Load JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def process_ooh_occupations(self, filepath: Path = None) -> List[Document]:
        """Process Occupational Outlook Handbook data into documents"""
        if filepath is None:
            filepath = config.RAW_DATA_DIR / "ooh_occupations.json"

        print(f"Processing OOH occupations from {filepath}")

        occupations = self.load_json_file(filepath)
        documents = []

        for occupation in occupations:
            # Create comprehensive text for each occupation
            text_parts = []

            title = occupation.get('title', '')
            text_parts.append(f"Occupation: {title}")

            if occupation.get('summary'):
                text_parts.append(f"\nSummary: {occupation['summary']}")

            if occupation.get('what_they_do'):
                text_parts.append(f"\nWhat They Do: {occupation['what_they_do']}")

            if occupation.get('work_environment'):
                text_parts.append(f"\nWork Environment: {occupation['work_environment']}")

            if occupation.get('how_to_become'):
                text_parts.append(f"\nHow to Become One: {occupation['how_to_become']}")

            if occupation.get('pay'):
                text_parts.append(f"\nPay and Outlook: {occupation['pay']}")

            full_text = "\n".join(text_parts)

            # Create metadata
            metadata = {
                'source': 'Occupational Outlook Handbook',
                'occupation': title,
                'url': occupation.get('url', ''),
                'type': 'occupation_data'
            }

            # Create document
            doc = Document(page_content=full_text, metadata=metadata)
            documents.append(doc)

        print(f"Created {len(documents)} occupation documents")
        return documents

    def process_educational_standards(self, filepath: Path = None) -> List[Document]:
        """Process educational standards into documents"""
        if filepath is None:
            filepath = config.RAW_DATA_DIR / "educational_standards.json"

        print(f"Processing educational standards from {filepath}")

        standards_data = self.load_json_file(filepath)
        documents = []

        # Process 21st century skills
        if '21st_century_skills' in standards_data:
            for category_data in standards_data['21st_century_skills']:
                category = category_data['category']
                standards = category_data['standards']

                text = f"21st Century Skill Category: {category}\n\n"
                text += "Standards:\n"
                text += "\n".join([f"- {standard}" for standard in standards])

                metadata = {
                    'source': '21st Century Skills',
                    'category': category,
                    'type': 'educational_standard'
                }

                doc = Document(page_content=text, metadata=metadata)
                documents.append(doc)

        # Process employability skills
        if 'employability_skills' in standards_data:
            for skill_data in standards_data['employability_skills']:
                skill = skill_data['skill']
                description = skill_data['description']
                indicators = skill_data['indicators']

                text = f"Employability Skill: {skill}\n\n"
                text += f"Description: {description}\n\n"
                text += "Indicators:\n"
                text += "\n".join([f"- {indicator}" for indicator in indicators])

                metadata = {
                    'source': 'Employability Skills',
                    'skill': skill,
                    'type': 'employability_skill'
                }

                doc = Document(page_content=text, metadata=metadata)
                documents.append(doc)

        print(f"Created {len(documents)} educational standard documents")
        return documents

    def process_iep_samples(self, filepath: Path = None) -> List[Document]:
        """Process IEP samples into documents"""
        if filepath is None:
            filepath = config.RAW_DATA_DIR / "iep_samples.json"

        print(f"Processing IEP samples from {filepath}")

        iep_data = self.load_json_file(filepath)
        documents = []

        # Process postsecondary goals
        if 'postsecondary_goals' in iep_data:
            for goal_type, examples in iep_data['postsecondary_goals'].items():
                text = f"Postsecondary Goal Type: {goal_type.replace('_', ' ').title()}\n\n"
                text += "Examples:\n"
                text += "\n".join([f"- {example}" for example in examples])

                metadata = {
                    'source': 'IEP Samples',
                    'goal_type': goal_type,
                    'type': 'postsecondary_goal_template'
                }

                doc = Document(page_content=text, metadata=metadata)
                documents.append(doc)

        # Process annual goals
        if 'annual_goals' in iep_data:
            for goal_category, examples in iep_data['annual_goals'].items():
                text = f"Annual Goal Category: {goal_category.replace('_', ' ').title()}\n\n"
                text += "Examples:\n"
                text += "\n".join([f"- {example}" for example in examples])

                metadata = {
                    'source': 'IEP Samples',
                    'category': goal_category,
                    'type': 'annual_goal_template'
                }

                doc = Document(page_content=text, metadata=metadata)
                documents.append(doc)

        # Process short-term objectives
        if 'short_term_objectives' in iep_data:
            objectives_data = iep_data['short_term_objectives']
            text = "Short-term Objectives\n\n"
            text += f"Template: {objectives_data.get('template', '')}\n\n"
            text += "Examples:\n"
            text += "\n".join([f"- {example}" for example in objectives_data.get('examples', [])])

            metadata = {
                'source': 'IEP Samples',
                'type': 'short_term_objective_template'
            }

            doc = Document(page_content=text, metadata=metadata)
            documents.append(doc)

        # Process transition services
        if 'transition_services' in iep_data:
            text = "Transition Services\n\n"
            text += "\n".join([f"- {service}" for service in iep_data['transition_services']])

            metadata = {
                'source': 'IEP Samples',
                'type': 'transition_services'
            }

            doc = Document(page_content=text, metadata=metadata)
            documents.append(doc)

        # Process IDEA requirements
        if 'idea_requirements' in iep_data:
            text = "IDEA 2004 Transition Requirements\n\n"
            for key, value in iep_data['idea_requirements'].items():
                text += f"{key.replace('_', ' ').title()}: {value}\n\n"

            metadata = {
                'source': 'IDEA Requirements',
                'type': 'legal_requirements'
            }

            doc = Document(page_content=text, metadata=metadata)
            documents.append(doc)

        print(f"Created {len(documents)} IEP sample documents")
        return documents

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks"""
        print(f"Chunking {len(documents)} documents...")

        chunked_docs = self.text_splitter.split_documents(documents)

        print(f"Created {len(chunked_docs)} chunks from {len(documents)} documents")
        return chunked_docs

    def process_all_documents(self) -> List[Document]:
        """Process all documents and return chunked results"""
        print("Processing all documents...")

        all_documents = []

        # Process each data source
        ooh_docs = self.process_ooh_occupations()
        all_documents.extend(ooh_docs)

        standards_docs = self.process_educational_standards()
        all_documents.extend(standards_docs)

        iep_docs = self.process_iep_samples()
        all_documents.extend(iep_docs)

        # Chunk all documents
        chunked_documents = self.chunk_documents(all_documents)

        # Save processed documents
        output_file = config.PROCESSED_DATA_DIR / "processed_documents.json"
        processed_data = [
            {
                'content': doc.page_content,
                'metadata': doc.metadata
            }
            for doc in chunked_documents
        ]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(chunked_documents)} processed chunks to {output_file}")

        return chunked_documents


if __name__ == "__main__":
    preprocessor = DocumentPreprocessor()
    documents = preprocessor.process_all_documents()
    print(f"\nProcessing complete! Total chunks: {len(documents)}")
