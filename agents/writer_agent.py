import os
import google.generativeai as genai
from agents.prompts import WRITER_PROMPT_TEMPLATE
from config import LLM_CONFIGS

class WriterAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        
        config = LLM_CONFIGS["writer"]
        self.model = genai.GenerativeModel(config["model"])
        self.max_tokens = config["max_tokens"]
        self.temperature = config["temperature"]
        
    def generate(self, context: dict) -> str:
        """Generate a LinkedIn post draft."""
        topic = context.get("topic", "Tech News")
        research_summary = context.get("research_summary", "")
        
        # User preferences fallback
        style = os.getenv("POST_STYLE", "professional")
        max_length = os.getenv("MAX_POST_LENGTH", "200")
        
        prompt = WRITER_PROMPT_TEMPLATE.format(
            topic=topic,
            research_summary=research_summary,
            style=style,
            max_length=max_length
        )
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens
                )
            )
            return response.text.strip()
        except Exception as e:
            print(f"Writer Agent Error: {e}")
            return f"Draft generation failed: {str(e)}"
