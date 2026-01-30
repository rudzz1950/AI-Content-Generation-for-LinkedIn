import chromadb
from chromadb.config import Settings
from config import CHROMA_DB_DIR
from typing import List, Dict, Optional
import os

class ChromaStore:
    def __init__(self, collection_name: str = "articles"):
        print(f"--- DEBUG: Using Persistent ChromaDB at {CHROMA_DB_DIR} ---")
        try:
            self.client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
            # Note: We rely on external embeddings passed to add/query methods
            # to avoid loading sentence-transformers/torch locally.
            self.collection = self.client.get_or_create_collection(
                name=collection_name, 
                metadata={"hnsw:space": "cosine"}
            )
            print("--- DEBUG: ChromaDB Collection Loaded ---")
        except Exception as e:
            print(f"CRITICAL CHROMA ERROR: {e}")
            print("Falling back to EphemeralClient...")
            self.client = chromadb.EphemeralClient()
            self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def add_documents(self, documents: List[Dict], embeddings: List[List[float]]):
        """Add chunks + embeddings to ChromaDB."""
        if not documents:
            return
            
        ids = [f"{doc['metadata']['url']}_{doc['metadata']['chunk_index']}" for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        texts = [doc['text'] for doc in documents]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts
        )
        print(f"Added {len(documents)} documents to {self.collection.name}")
        
    def query(self, query_embedding: List[float], n_results: int = 5, where: Optional[Dict] = None):
        """Search for most relevant chunks."""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        return results

    def delete_old_documents(self, days_old: int = 30):
        # Implementation left simple for now - can use where clause with date logic if metadata has timestamp
        pass
