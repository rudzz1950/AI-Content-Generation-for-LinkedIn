import os
import json
from openai import OpenAI
from agents.prompts import CRITIC_PROMPT_TEMPLATE
from config import LLM_CONFIGS

class CriticAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Fallback checks (e.g. if user forgot to remove Groq key but added OpenAI)
            raise ValueError("OPENAI_API_KEY not found")
            
        self.client = OpenAI(api_key=api_key)
        self.config = LLM_CONFIGS["critic"]
        
    def review_post(self, draft: str, context: dict) -> dict:
        """Critique the draft and return structured feedback."""
        prompt = CRITIC_PROMPT_TEMPLATE.format(
            draft=draft,
            context=json.dumps(context, default=str)
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                response_format={"type": "json_object"} # OpenAI JSON mode
            )
            
            content = response.choices[0].message.content
            return self._parse_json(content)
            
        except Exception as e:
            print(f"Critic Agent Error: {e}")
            return {
                "score": 5, 
                "feedback": f"Error during critique: {e}",
                "revised_post": draft
            }
            
    def _parse_json(self, content: str) -> dict:
        """robust json parsing from LLM output."""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Failed to parse Critic JSON. Returning raw content.")
            return {
                "score": 5, 
                "feedback": content,
                "revised_post": "" 
            }
