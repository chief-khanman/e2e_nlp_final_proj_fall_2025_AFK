from typing import List, Optional
from pathlib import Path
import json

from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from config import config

class VectorStoreManager:
    """Manages vector database for document embeddings and retrieval"""

    def __init__(self, use_openai_embeddings: bool = False):
        """
        Initialize vector store manager

        Args:
            use_openai_embeddings: If True, use OpenAI embeddings. Otherwise use HuggingFace.
        """
        self.use_openai_embeddings = use_openai_embeddings

        # Initialize embeddings
        if use_openai_embeddings and config.OPENAI_API_KEY:
            print("Using OpenAI embeddings...")
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=config.OPENAI_API_KEY
            )
        else:
            print(f"Using HuggingFace embeddings: {config.EMBEDDING_MODEL}")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=config.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )

        self.vector_store = None
        self.persist_directory = str(config.VECTOR_DB_PATH)

    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """
        Create a new vector store from documents

        Args:
            documents: List of Document objects to embed

        Returns:
            Chroma vector store
        """
        print(f"Creating vector store with {len(documents)} documents...")

        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=config.COLLECTION_NAME,
            persist_directory=self.persist_directory
        )

        print(f"Vector store created and persisted to {self.persist_directory}")
        return self.vector_store

    def load_vector_store(self) -> Chroma:
        """
        Load existing vector store from disk

        Returns:
            Chroma vector store
        """
        print(f"Loading vector store from {self.persist_directory}")

        self.vector_store = Chroma(
            collection_name=config.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

        print("Vector store loaded successfully")
        return self.vector_store

    def vector_store_exists(self) -> bool:
        """Check if vector store exists on disk"""
        chroma_path = Path(self.persist_directory)
        return chroma_path.exists() and any(chroma_path.iterdir())

    def get_or_create_vector_store(self, documents: Optional[List[Document]] = None) -> Chroma:
        """
        Get existing vector store or create new one

        Args:
            documents: Documents to use if creating new store

        Returns:
            Chroma vector store
        """
        if self.vector_store_exists():
            return self.load_vector_store()
        elif documents:
            return self.create_vector_store(documents)
        else:
            raise ValueError("Vector store does not exist and no documents provided to create it")

    def similarity_search(
        self,
        query: str,
        k: int = None,
        filter_metadata: Optional[dict] = None
    ) -> List[Document]:
        """
        Search for similar documents

        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Metadata filters

        Returns:
            List of relevant documents
        """
        if self.vector_store is None:
            self.load_vector_store()

        k = k or config.TOP_K_RESULTS

        if filter_metadata:
            results = self.vector_store.similarity_search(
                query,
                k=k,
                filter=filter_metadata
            )
        else:
            results = self.vector_store.similarity_search(query, k=k)

        return results

    def similarity_search_with_score(
        self,
        query: str,
        k: int = None,
        filter_metadata: Optional[dict] = None
    ) -> List[tuple]:
        """
        Search for similar documents with relevance scores

        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Metadata filters

        Returns:
            List of (document, score) tuples
        """
        if self.vector_store is None:
            self.load_vector_store()

        k = k or config.TOP_K_RESULTS

        if filter_metadata:
            results = self.vector_store.similarity_search_with_score(
                query,
                k=k,
                filter=filter_metadata
            )
        else:
            results = self.vector_store.similarity_search_with_score(query, k=k)

        return results

    def add_documents(self, documents: List[Document]):
        """Add new documents to existing vector store"""
        if self.vector_store is None:
            self.load_vector_store()

        self.vector_store.add_documents(documents)
        print(f"Added {len(documents)} documents to vector store")

    def delete_collection(self):
        """Delete the vector store collection"""
        if self.vector_store is not None:
            self.vector_store.delete_collection()
            print("Vector store collection deleted")

    def get_retriever(self, search_kwargs: Optional[dict] = None):
        """
        Get a retriever interface for the vector store

        Args:
            search_kwargs: Additional search arguments

        Returns:
            VectorStoreRetriever
        """
        if self.vector_store is None:
            self.load_vector_store()

        if search_kwargs is None:
            search_kwargs = {"k": config.TOP_K_RESULTS}

        return self.vector_store.as_retriever(search_kwargs=search_kwargs)


def setup_vector_store(force_recreate: bool = False):
    """
    Setup vector store with documents

    Args:
        force_recreate: If True, delete existing store and create new one
    """
    from preprocessing import DocumentPreprocessor

    manager = VectorStoreManager(use_openai_embeddings=False)

    if force_recreate and manager.vector_store_exists():
        print("Deleting existing vector store...")
        try:
            manager.load_vector_store()
            manager.delete_collection()
        except Exception as e:
            print(f"Error deleting collection: {e}")

    if not manager.vector_store_exists() or force_recreate:
        print("Creating new vector store...")

        # Process documents
        preprocessor = DocumentPreprocessor()
        documents = preprocessor.process_all_documents()

        # Create vector store
        manager.create_vector_store(documents)

        print(f"\nVector store setup complete with {len(documents)} document chunks")
    else:
        print("Vector store already exists. Loading...")
        manager.load_vector_store()
        print("Vector store loaded successfully")

    return manager


if __name__ == "__main__":
    import sys

    force_recreate = "--recreate" in sys.argv

    manager = setup_vector_store(force_recreate=force_recreate)

    # Test retrieval
    print("\n--- Testing Retrieval ---")
    test_query = "What skills are needed for retail sales work?"
    results = manager.similarity_search(test_query, k=3)

    print(f"\nQuery: {test_query}")
    print(f"Found {len(results)} results:\n")

    for i, doc in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Type: {doc.metadata.get('type', 'Unknown')}")
        print(f"Content preview: {doc.page_content[:200]}...")
        print("-" * 80)
