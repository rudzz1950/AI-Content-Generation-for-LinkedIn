import os
from typing import List, Dict

class RecommendationEngine:
    def __init__(self):
        self.preferred_topics = os.getenv("PREFERRED_TOPICS", "").split(",")
        self.excluded_topics = os.getenv("EXCLUDED_TOPICS", "").split(",")
    
    def rank_articles(self, articles: List[Dict]) -> List[Dict]:
        """Rank articles based on user preferences."""
        ranked_articles = []
        
        for article in articles:
            score = 0
            text = (article.get("title", "") + " " + article.get("content", "")).lower()
            topic = article.get("topic", "Uncategorized")
            
            # Exclude check
            if any(t.lower() in text or t.lower() == topic.lower() for t in self.excluded_topics if t):
                continue
                
            # Preference boost
            if any(t.lower() in text or t.lower() == topic.lower() for t in self.preferred_topics if t):
                score += 5
            
            # Recentness boost (placeholder logic)
            score += 1
            
            ranked_articles.append({**article, "score": score})
            
        # Sort by score desc
        return sorted(ranked_articles, key=lambda x: x["score"], reverse=True)
