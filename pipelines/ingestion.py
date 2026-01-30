import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import List, Dict
from config import RSS_FEEDS, MAX_ARTICLES_PER_FEED

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self, url: str) -> Dict:
        """Scrape content from a given URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()

            # Strategy 1: Look for main article content
            article_body = soup.find('article')
            if article_body:
                text = article_body.get_text()
            else:
                # Strategy 2: Fallback to all paragraphs
                text = "\n".join([p.get_text() for p in soup.find_all('p')])
            
            title = soup.find('h1').get_text() if soup.find('h1') else "Untitled"
            
            return {
                "title": title.strip(),
                "content": text.strip(),
                "source": "Web Scraper",
                "url": url,
                "date": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {"title": "Error", "content": "", "source": "Error", "url": url}

class NewsFetcher:
    def __init__(self):
        self.scraper = WebScraper()
        
    def fetch_feeds(self) -> List[Dict]:
        """Fetch and parse all configured RSS feeds."""
        articles = []
        
        for feed_url in RSS_FEEDS:
            try:
                print(f"Fetching {feed_url}...")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:
                    # Basic metadata from RSS
                    article_data = {
                        "title": entry.title,
                        "url": entry.link,
                        "date": datetime.now().isoformat(), # Default if missing
                        "source": feed.feed.get('title', 'Unknown Source')
                    }
                    
                    # enrich with full content from scraping
                    scraped_data = self.scraper.scrape(entry.link)
                    if len(scraped_data["content"]) > 100: # Only if valid content found
                        article_data["content"] = scraped_data["content"]
                        articles.append(article_data)
                        
            except Exception as e:
                print(f"Failed to fetch feed {feed_url}: {e}")
                continue
                
        print(f"Total articles fetched: {len(articles)}")
        return articles
