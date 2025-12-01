"""
Test script for the IEP RAG System

Tests the system with sample student data
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.rag_pipeline import IEPRAGPipeline

def test_clarence():
    """Test with Clarence from the project description"""
    print("="*80)
    print("TESTING IEP RAG SYSTEM WITH CLARENCE")
    print("="*80)

    student_info = {
        "name": "Clarence",
        "age": "15",
        "grade": "10th grade (Sophomore)",
        "disability": "Behavior disorder",
        "interests": "Enterprising activities, hands-on learning, prefers hands-on over academic instruction",
        "career_interest": "Retail sales, driver/sales worker, working at Walmart",
        "assessment_results": "O*Net Interest Profiler shows strength in Enterprising category. Vision for the Future interview indicates interest in working at Walmart as a sales associate."
    }

    print("\nStudent Information:")
    print("-" * 80)
    for key, value in student_info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    print("\n\nInitializing RAG Pipeline...")
    print("-" * 80)

    try:
        # Initialize pipeline (will use OpenAI if API key is set, otherwise will fail gracefully)
        pipeline = IEPRAGPipeline(use_openai=True)

        print("\nGenerating IEP Goals...")
        print("-" * 80)

        result = pipeline.generate_complete_iep(student_info)

        print("\n" + "="*80)
        print("GENERATED IEP")
        print("="*80)
        print(result["complete_iep"])

        print("\n" + "="*80)
        print("CONTEXT DOCUMENTS USED")
        print("="*80)
        for i, doc in enumerate(result.get("context_documents", []), 1):
            print(f"\nDocument {i}:")
            print(f"  Source: {doc['metadata'].get('source', 'Unknown')}")
            print(f"  Type: {doc['metadata'].get('type', 'Unknown')}")
            print(f"  Preview: {doc['content'][:150]}...")

        print("\n" + "="*80)
        print("TEST COMPLETE")
        print("="*80)

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nNote: Make sure you have:")
        print("1. Run setup.py to initialize the data and vector store")
        print("2. Set your OPENAI_API_KEY in the .env file")
        print("3. Installed all required dependencies")

def test_retrieval():
    """Test the retrieval component"""
    print("\n\n" + "="*80)
    print("TESTING RETRIEVAL COMPONENT")
    print("="*80)

    try:
        pipeline = IEPRAGPipeline(use_openai=True)

        test_queries = [
            "What skills are needed for retail sales work?",
            "What are employability skills for workplace success?",
            "Examples of postsecondary employment goals"
        ]

        for query in test_queries:
            print(f"\nQuery: {query}")
            print("-" * 80)

            results = pipeline.retrieve_relevant_context(query, k=3)

            for i, doc in enumerate(results, 1):
                print(f"\nResult {i}:")
                print(f"  Source: {doc['metadata'].get('source', 'Unknown')}")
                print(f"  Type: {doc['metadata'].get('type', 'Unknown')}")
                print(f"  Content: {doc['content'][:200]}...")

    except Exception as e:
        print(f"\nError: {str(e)}")

def main():
    """Run all tests"""
    # Test retrieval first
    test_retrieval()

    # Test complete IEP generation
    test_clarence()

if __name__ == "__main__":
    main()
