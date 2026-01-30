from agents.orchestrator import OrchestratorAgent
from pipelines.ingestion import WebScraper
from pipelines.medium_reader import MediumReader
from pipelines.chunking import ArticleChunker
from storage.chroma_store import ChromaStore
from intelligence.embeddings import EmbeddingService
from utils.notion_client import NotionPostSaver
from config import ENABLE_MEDIUM_BYPASS

class OnDemandPipeline:
    def __init__(self, orchestrator: "OrchestratorAgent", vector_store: ChromaStore, embedder: EmbeddingService):
        self.orchestrator = orchestrator
        self.vector_store = vector_store
        self.embedder = embedder
        self.chunker = ArticleChunker()
        self.scraper = WebScraper()
        self.medium_reader = MediumReader()
        self.notion = NotionPostSaver()
        
    def process_url(self, url: str):
        """Run the pipeline for a single URL."""
        print(f"--- On-Demand: Processing {url} ---")
        
        # 0. Initialize Extras
        from intelligence.image_gen_google import GoogleImageGenerator
        from utils.email_sender import EmailSender
        image_gen = GoogleImageGenerator()
        email_sender = EmailSender()

        # 1. Fetch
        if "medium.com" in url and ENABLE_MEDIUM_BYPASS:
            print(f"Attempting Medium Bypass: {url}")
            article = self.medium_reader.read_article(url)
        else:
            article = self.scraper.scrape(url)
            
        if not article.get("content"):
            return {"error": "Failed to fetch content"}
            
        print(f"fetched: {article['title']}")
            
        # 2. Chunk & Embed
        print("--- DEBUG: Chunking Article... ---")
        chunks = self.chunker.chunk_article(article)
        print(f"--- DEBUG: Got {len(chunks)} chunks. ---")
        
        print("--- DEBUG: Embedding Texts... ---")
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedder.embed_texts(texts)
        print(f"--- DEBUG: Got {len(embeddings)} embeddings. ---")
        
        print("--- DEBUG: Adding to Vector Store... ---")
        self.vector_store.add_documents(chunks, embeddings)
        print("--- DEBUG: Stored in Vector Store. ---")
        
        # 3. Agent Flow
        print("--- DEBUG: Starting Orchestrator Run... ---")
        final_post = self.orchestrator.run(
            topic=article["title"],
            context={"articles": [article], "topic": article["title"]}
        )
        
        # 4. Image Generation
        image_url = None
        if image_gen.model:
            print("--- DEBUG: Generating Cover Image... ---")
            image_prompt = f"Editorial illustration for a tech article about: {article['title']}. Minimalist, vector art style."
            image_url = image_gen.generate_image(image_prompt)

        # 5. Save to Notion
        notion_url = self.notion.save_post(
            title=article["title"],
            content=final_post,
            topic="On-Demand",
            url=url
        )
        
        # 6. Email Delivery
        if email_sender.sender_email:
            print("--- DEBUG: Sending Email... ---")
            email_body = f"Here is your AI generated article.\n\nRead on Notion: {notion_url}\n\n{final_post}"
            email_sender.send_email(
                subject=f"AI Article: {article['title']}",
                body=email_body,
                image_path=image_url
            )
        
        return {
            "post": final_post,
            "notion_url": notion_url,
            "image_url": image_url
        }
