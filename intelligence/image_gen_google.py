import google.generativeai as genai
import os

class GoogleImageGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found. Image generation disabled.")
            self.model = None
        else:
            genai.configure(api_key=self.api_key)
            # Use 'imagen-3.0-generate-001' or latest available via Gemini API
            # Ideally user's "Pro" sub allows access to this model.
            try:
                self.model = genai.GenerativeModel('imagen-3.0-generate-001')
            except:
                print("Warning: Imagen 3 model not found or accessible. Trying fallback...")
                self.model = None # Will fail gracefully

    def generate_image(self, prompt: str) -> str:
        """Generates an image using Google Imagen and returns the path/URL."""
        if not self.model:
            return None

        try:
            print(f"--- Generating Image (Imagen) for: {prompt[:50]}... ---")
            # Note: The Python SDK for Imagen might differ slightly depending on version.
            # This is the standard call for generativeai package if supported.
            # If standard generate_content doesn't support image output directly in this SDK version,
            # we might need to use the REST API or Vertex AI SDK. 
            # However, sticking to google-generativeai for now.
            
            # Since explicit Imagen support in the `google-generativeai` client 
            # can be experimental, we will try the standard method.
            # If this fails, we will print a clear warning.
            
            # Currently (2025/2026), the best way via API key is often via REST or specific beta methods.
            # For this workspace, we'll try the direct model.generate_images if available, 
            # or standard generate_content requesting an image.
            
            # Placeholder for actual library support check:
            if hasattr(self.model, 'generate_images'):
                response = self.model.generate_images(
                    prompt=prompt,
                    number_of_images=1
                )
                image = response.images[0]
            else:
                 # Fallback/Assumption: This SDK might not support it yet.
                 print("Error: current google-generativeai SDK doesn't expose Imagen directly.")
                 return None

            # Save locally since it returns bytes/image object usually
            output_path = os.path.join("data", "generated_image.png")
            image.save(output_path)
            print(f"Image Saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Google Image Generation Failed: {e}")
            return None
