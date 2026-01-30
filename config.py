import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==============================================================================
# PROJECT PATHS
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DB_DIR = DATA_DIR / "chroma_db"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ==============================================================================
# SYSTEM SETTINGS
# ==============================================================================
ENABLE_MEDIUM_BYPASS = os.getenv("ENABLE_MEDIUM_BYPASS", "false").lower() == "true"
DAILY_RUN_TIME = os.getenv("DAILY_RUN_TIME", "06:00")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# ==============================================================================
# DATA INGESTION SETTINGS
# ==============================================================================
RSS_FEEDS = [
    # General Tech / AI
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    
    # AI Specific
    "https://openai.com/blog/rss.xml",
    "https://www.anthropic.com/feed",
    "https://simonwillison.net/atom/entries/",  # Good for LLM dev news
    
    # Startup / VC
    "http://feeds.feedburner.com/PaulGraham",
    "https://a16z.com/feed/",
]

MAX_ARTICLES_PER_FEED = 5
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ==============================================================================
# INTELLIGENCE SETTINGS
# ==============================================================================
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TREND_THRESHOLD = 3  # Mentioned in >3 sources = Trend
SIMILARITY_THRESHOLD = 0.5

# ==============================================================================
# LLM CONFIGS
# ==============================================================================
LLM_CONFIGS = {
    # Writer Agent (Gemini 2.0 Flash)
    "writer": {
        "model": "gemini-2.0-flash-exp",
        "temperature": 0.7,
        "max_tokens": 2000,
    },
    # Critic Agent (OpenAI GPT-4o-mini)
    "critic": {
        "model": "gpt-4o-mini",
        "temperature": 0.3,
        "max_tokens": 1500,
    },
    # Research Agent (Perplexity)
    "researcher": {
        "model": "sonar-pro",
        "temperature": 0.1,
    }
}
