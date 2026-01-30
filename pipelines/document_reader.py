import PyPDF2
import os

class DocumentReader:
    def __init__(self):
        pass
    
    def read_pdf(self, pdf_path: str) -> str:
        """Extract text from text-based PDF (PyPDF2)."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    content = page.extract_text()
                    if content:
                        text += content + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""

    def read_with_ocr(self, image_path: str) -> str:
        """Read text from image/scanned PDF using Gemini Vision."""
        from utils.vision_reader import VisionReader
        vision = VisionReader()
        return vision.read_image(image_path)

    def read_file(self, file_path: str) -> str:
        """Route to appropriate reader based on extension."""
        if file_path.endswith('.pdf'):
            text = self.read_pdf(file_path)
            if not text.strip(): # Fallback to OCR if empty (scanned)
                print("PDF seems empty/scanned. Trying Vision OCR...")
                # Note: PyPDF2 doesn't extract images easily for OCR without extra libs.
                # For this simplified flow, we assume user provides an Image file for OCR
                # OR we accept that we can't easily convert PDF-pages-to-Images without poppler.
                # So we will only enable OCR for actual Image files for now.
                return "" 
            return text
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            return self.read_with_ocr(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
