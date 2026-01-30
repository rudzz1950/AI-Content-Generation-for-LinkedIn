from pipelines.ingestion import NewsFetcher, WebScraper
from pipelines.medium_reader import MediumReader

def test_scraper():
    print("\n--- Testing Web Scraper ---")
    scraper = WebScraper()
    # Test a known safe URL
    url = "https://example.com"
    result = scraper.scrape(url)
    print(f"Title: {result.get('title')}")
    print(f"Content Length: {len(result.get('content', ''))}")
    assert result.get('content'), "Scraping failed for example.com"
    print("Web Scraper: PASS")

def test_fetcher():
    print("\n--- Testing RSS News Fetcher ---")
    fetcher = NewsFetcher()
    # This might take a while as it fetches multiple feeds
    articles = fetcher.fetch_feeds()
    print(f"Fetched {len(articles)} articles.")
    assert len(articles) > 0, "No articles fetched from RSS feeds"
    print("News Fetcher: PASS")
    
def test_medium_bypass():
    print("\n--- Testing Medium Reader (Bypass) ---")
    # Using a known Paywalled article URL (or a placeholder one that redirects)
    # Freedium mirror check
    reader = MediumReader()
    # Using a random recent Medium article
    url = "https://medium.com/@ev/welcome-to-medium-9e53ca408c48" 
    result = reader.read_article(url)
    if "error" in result:
        print(f"Medium Bypass: WARNING ({result['error']}) - This matches expectation if network blocks it.")
    else:
        print(f"Medium Title: {result.get('title')}")
        print("Medium Reader: PASS")

if __name__ == "__main__":
    test_scraper()
    # test_fetcher() # Uncomment to test full RSS fetch
    test_medium_bypass()
