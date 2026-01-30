from datetime import datetime
from storage.chroma_store import ChromaStore

class MemoryManager:
    def __init__(self, vector_store: ChromaStore):
        self.vector_store = vector_store
        
    def prune_old_memories(self, days=30):
        """Remove articles older than X days."""
        print(f"Pruning memories older than {days} days...")
        # Note: ChromaDB delete by metadata query is supported
        # We need to implement current_date - article_date > days logic
        # For now, just a placeholder for the cron job hook
        pass
        
    def retrieve_context(self, query: str) -> str:
        """Get relevant context for writing."""
        # This will wrap the vector store query
        pass
