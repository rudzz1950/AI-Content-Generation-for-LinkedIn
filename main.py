print("HELLO WORLD")
import argparse
import time
from datetime import datetime
from dotenv import load_dotenv

# Components
from pipelines.ingestion import NewsFetcher
from pipelines.chunking import ArticleChunker
from pipelines.recommendation import RecommendationEngine
from intelligence.classifier import TopicClassifier
from intelligence.trends import TrendDetector
from intelligence.embeddings import EmbeddingService
from intelligence.memory_manager import MemoryManager
from storage.chroma_store import ChromaStore
# from storage.simple_store import SimpleVectorStore

# Agents
from agents.orchestrator import OrchestratorAgent
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.critic_agent import CriticAgent

# Pipelines & Utils
from pipelines.on_demand import OnDemandPipeline
from utils.notion_client import NotionPostSaver
from utils.retry import with_retry

load_dotenv()

class DailyContentPipeline:
    def __init__(self):
        # Initialize Core Services
        # self.chroma_store = SimpleVectorStore() 
        print("--- DEBUG: Switching to Persistent ChromaStore ---")
        self.chroma_store = ChromaStore() # Now uses PersistentClient
        self.embedder = EmbeddingService()
        self.chunker = ArticleChunker()
        self.classifier = TopicClassifier()
        self.trend_detector = TrendDetector()
        self.recommender = RecommendationEngine()
        self.memory_manager = MemoryManager(self.chroma_store)
        self.notion = NotionPostSaver()
        self.fetcher = NewsFetcher()
        
        # Initialize Agents
        self.researcher = ResearchAgent()
        self.writer = WriterAgent()
        self.critic = CriticAgent()
        
        # Initialize Orchestrator
        self.orchestrator = OrchestratorAgent(
            researcher=self.researcher,
            writer=self.writer,
            critic=self.critic
        )
    
    @with_retry(max_attempts=3, backoff=2.0)
    def run_daily_pipeline(self):
        """Execute the complete daily content generation pipeline."""
        print(f"[{datetime.now()}] Starting daily pipeline...")
        
        # Phase 1: Ingestion
        articles = self.fetcher.fetch_feeds()
        if not articles:
            print("No articles found.")
            return

        # Phase 2: Store & Classify
        processed_docs = []
        for article in articles:
            # Classify
            topic = self.classifier.classify(article.get("title") + " " + article.get("content", "")[:500])
            article["topic"] = topic
            
            # Chunk & Embed
            chunks = self.chunker.chunk_article(article)
            if not chunks: continue
            
            texts = [c["text"] for c in chunks]
            embeddings = self.embedder.embed_texts(texts)
            self.chroma_store.add_documents(chunks, embeddings)
            processed_docs.append(article)

        # Phase 3: Trends & Recommendations
        trends = self.trend_detector.detect_trends(processed_docs)
        ranked_articles = self.recommender.rank_articles(processed_docs)
        
        top_article = ranked_articles[0] if ranked_articles else None
        
        if top_article:
            print(f"--- Generating Post for Top Article: {top_article['title']} ---")
            
            final_post = self.orchestrator.run(
                topic=top_article["title"],
                context={"articles": [top_article], "topic": top_article["topic"]}
            )
            
            self.notion.save_post(
                title=top_article["title"],
                content=final_post,
                topic=top_article["topic"],
                url=top_article["url"]
            )
        else:
            print("No suitable articles found to generate post.")

def main():
    print("--- DEBUG: Starting Main ---")
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--url", help="Process single article URL")
        parser.add_argument("--daily", action="store_true", help="Run daily pipeline")
        args = parser.parse_args()
        
        print("--- DEBUG: Initializing Pipeline ---")
        pipeline = DailyContentPipeline()
        print("--- DEBUG: Pipeline Initialized ---")
        
        if args.url:
            print(f"--- DEBUG: Processing URL: {args.url} ---")
            # On-Demand Mode
            on_demand = OnDemandPipeline(
                pipeline.orchestrator, 
                pipeline.chroma_store,
                pipeline.embedder
            )
            result = on_demand.process_url(args.url)
            if result.get("notion_url"):
                print(f"Success! Post saved to Notion: {result['notion_url']}")
            else:
                # Safe print for Windows consoles
                post_content = result.get('post', '')
                try:
                    print(f"Failed or Not Saved. Output:\n{post_content}")
                except UnicodeEncodeError:
                    print(f"Failed or Not Saved. Output (ASCII):\n{post_content.encode('ascii', 'replace').decode('ascii')}")
                
        elif args.daily:
            # Daily Mode - Schedule Loop
            import schedule
            from config import DAILY_RUN_TIME
            
            print(f"[{datetime.now()}] Scheduler Started. Will run daily at {DAILY_RUN_TIME}")
            
            # Safe wrapper to catch pipeline errors without killing scheduler
            def safe_daily_runner():
                try:
                   pipeline.run_daily_pipeline()
                except Exception as e:
                   print(f"[{datetime.now()}] JOB FAILED: {e}")
            
            schedule.every().day.at(DAILY_RUN_TIME).do(safe_daily_runner)
            
            # Force run immediately if missed window? No, just loop.
            while True:
                try:
                    schedule.run_pending()
                except Exception as e:
                    print(f"SCHEDULER LOOP ERROR: {e}")
                time.sleep(60)
        elif not args.url:
             # Default behavior if no args: Run once immediately
             print("No args provided. Running Daily Pipeline ONCE immediately...")
             pipeline.run_daily_pipeline()
            
    except Exception as e:
        import traceback
        print(f"CRITICAL ERROR in MAIN: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
