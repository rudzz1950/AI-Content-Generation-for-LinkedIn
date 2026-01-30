import os
import google.generativeai as genai
from typing import List

class EmbeddingService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model_name = "models/text-embedding-004"
        
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Gemini API."""
        if not texts:
            return []
        
        # Batch embedding (Gemini supports batch)
        # We might need to chunk if list is huge, but for now direct call
        try:
            # title is optional, but helps. We just pass text.
            embeddings = []
            for text in texts:
                # Truncate to avoid limit
                result = genai.embed_content(
                    model=self.model_name,
                    content=text[:9000], 
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            return embeddings
        except Exception as e:
            print(f"Embedding Error: {e}")
            return []
        
    def embed_query(self, text: str) -> List[float]:
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=text[:9000],
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding Query Error: {e}")
            return []
