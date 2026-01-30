from collections import Counter
from typing import List, Dict
from config import TREND_THRESHOLD

class TrendDetector:
    def __init__(self):
        pass
    
    def detect_trends(self, articles: List[Dict]) -> List[str]:
        """Identify trending topics based on frequency."""
        if not articles:
            return []
            
        topics = [a.get("topic") for a in articles if a.get("topic")]
        counts = Counter(topics)
        
        # Determine trends: Topics appearing more than threshold
        trends = [topic for topic, count in counts.items() if count >= TREND_THRESHOLD]
        
        print(f"Detected trends: {trends}")
        return trends
