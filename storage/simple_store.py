import numpy as np
from typing import List, Dict, Optional

class SimpleVectorStore:
    def __init__(self):
        self.documents = [] # List[Dict] (metadata + text)
        self.embeddings = [] # List[List[float]]
        
    def add_documents(self, documents: List[Dict], embeddings: List[List[float]]):
        """Add documents and embeddings to the store."""
        if not documents:
            return
            
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)
        print(f"--- DEBUG: Stored {len(documents)} docs in SimpleVectorStore. Total: {len(self.documents)} ---")
        
    def query(self, query_embedding: List[float], n_results: int = 5, where: Optional[Dict] = None) -> Dict:
        """Simple cosine similarity search."""
        if not self.embeddings:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
            
        query_vec = np.array(query_embedding)
        doc_vecs = np.array(self.embeddings)
        
        # Normalize
        norm_q = np.linalg.norm(query_vec)
        norm_docs = np.linalg.norm(doc_vecs, axis=1)
        
        # Avoid div by zero
        if norm_q == 0: return {"documents": [[]]}
        norm_docs[norm_docs == 0] = 1e-9
        
        # Cosine Similarity
        # (A . B) / (|A| * |B|)
        dot_product = np.dot(doc_vecs, query_vec)
        similarities = dot_product / (norm_docs * norm_q)
        
        # Top K
        sorted_indices = np.argsort(similarities)[::-1][:n_results]
        
        results = {
            "documents": [[self.documents[i]["text"] for i in sorted_indices]],
            "metadatas": [[self.documents[i]["metadata"] for i in sorted_indices]],
            "distances": [[1 - similarities[i] for i in sorted_indices]] # Convert sim to dist
        }
        return results
