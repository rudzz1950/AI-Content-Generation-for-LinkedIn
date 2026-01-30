import os
import requests
from agents.prompts import RESEARCH_PROMPT_TEMPLATE

class ResearchAgent:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.model = "sonar-pro"
        
    def research_topic(self, topic: str, context_articles: list) -> str:
        """Perform deep dive research using Perplexity."""
        titles = ", ".join([a['title'] for a in context_articles])
        prompt = RESEARCH_PROMPT_TEMPLATE.format(topic=topic, titles=titles)
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful research assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Research Agent Error: {e}")
            return f"Research failed: {str(e)}"
