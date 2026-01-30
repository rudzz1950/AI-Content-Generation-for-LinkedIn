import google.generativeai as genai
import os
from PIL import Image

class VisionReader:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash') # Good for multimodal

    def read_image(self, image_path: str) -> str:
        """Extract text from image using Gemini Vision."""
        if not os.path.exists(image_path):
            return ""
        
        try:
            print(f"--- Reading Image Text (OCR) from {os.path.basename(image_path)} ---")
            img = Image.open(image_path)
            response = self.model.generate_content(
                ["Transcribe the text in this image exactly.", img]
            )
            return response.text
        except Exception as e:
            print(f"Vision OCR Failed: {e}")
            return ""
