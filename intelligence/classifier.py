import os
import google.generativeai as genai

class TopicClassifier:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        self.candidate_labels = [
            "Artificial Intelligence", "Startups & Venture Capital", 
            "Software Engineering", "Product Management", 
            "Tech Policy & Regulation", "Cryptocurrency & Blockchain"
        ]
        
    def classify(self, text: str) -> str:
        """Classify text into one of the predefined topics using LLM."""
        if not text:
            return "Uncategorized"
            
        prompt = f"""
        Classify the following text into ONE of these categories: {', '.join(self.candidate_labels)}.
        Return ONLY the category name.
        
        Text: {text[:1000]}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            # Simple validation
            for label in self.candidate_labels:
                if label.lower() in result.lower():
                    return label
            return "Uncategorized"
        except Exception as e:
            print(f"Classification Error: {e}")
            return "Uncategorized"
