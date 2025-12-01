"""
Setup script for the IEP RAG System

This script initializes the system by:
1. Collecting/creating sample data
2. Processing documents
3. Creating vector database
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data_collection import DataCollector
from src.vector_store import setup_vector_store

def main():
    print("="*80)
    print("IEP RAG SYSTEM SETUP")
    print("="*80)

    print("\nStep 1: Collecting data...")
    print("-" * 80)
    collector = DataCollector()
    collector.collect_all_data()

    print("\n\nStep 2: Processing documents and creating vector database...")
    print("-" * 80)
    manager = setup_vector_store(force_recreate=True)

    print("\n\n" + "="*80)
    print("SETUP COMPLETE!")
    print("="*80)
    print("\nYou can now run the application:")
    print("  streamlit run app.py")
    print("\nOr test the RAG pipeline:")
    print("  python src/rag_pipeline.py")
    print("="*80)

if __name__ == "__main__":
    main()
