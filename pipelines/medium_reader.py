import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MediumReader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def read_article(self, url: str) -> dict:
        """
        Bypass Medium Paywall using freedium-mirror.cfd
        Logic: Replace original domain with freedium-mirror.cfd and scrape.
        """
        try:
            # Construct Bypass URL
            # e.g. https://medium.com/xyz -> https://freedium-mirror.cfd/https://medium.com/xyz
            # OR sometimes mirrors work by just changing the domain.
            # Based on user script provided: "https://freedium-mirror.cfd/" + original_url
            
            bypass_url = f"https://freedium-mirror.cfd/{url}"
            print(f"Attempting Medium Bypass: {bypass_url}")
            
            response = requests.get(bypass_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content from the mirrored page
            # Usually the mirror renders the content in a readable format similar to the original
            article_body = soup.find('article') or soup.find('div', class_='main-content')
            
            if article_body:
                text = article_body.get_text(separator='\n\n')
            else:
                # Fallback
                text = "\n".join([p.get_text() for p in soup.find_all('p')])
            
            title = soup.find('h1').get_text().strip() if soup.find('h1') else "Medium Article"
            
            if len(text) < 200:
                raise ValueError("Content too short. Bypass might have failed.")
                
            return {
                "title": title,
                "content": text.strip(),
                "source": "Medium (Bypassed)",
                "url": url,
                "date": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Medium Reader Error: {e}")
            return {"error": str(e)}
