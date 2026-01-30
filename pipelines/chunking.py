from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP
from typing import List, Dict

class ArticleChunker:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def chunk_article(self, article: dict) -> List[Dict]:
        """Split article content into semantic chunks with metadata."""
        content = article.get("content", "")
        if not content:
            return []
            
        chunks = self.splitter.split_text(content)
        
        chunked_docs = []
        for i, text in enumerate(chunks):
            chunked_docs.append({
                "text": text,
                "metadata": {
                    "source": article.get("source", "Unknown"),
                    "title": article.get("title", "Untitled"),
                    "url": article.get("url", ""),
                    "date": article.get("date", ""),
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            })
            
        return chunked_docs
