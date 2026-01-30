print("--- Testing Imports ---")
try:
    from intelligence.image_gen_google import GoogleImageGenerator
    print("[PASS] Imported GoogleImageGenerator")
except Exception as e:
    print(f"[FAIL] GoogleImageGenerator: {e}")

try:
    from utils.email_sender import EmailSender
    print("[PASS] Imported EmailSender")
except Exception as e:
    print(f"[FAIL] EmailSender: {e}")

try:
    from storage.chroma_store import ChromaStore
    print("[PASS] Imported ChromaStore")
except Exception as e:
    print(f"[FAIL] ChromaStore: {e}")

print("--- Testing Advanced Features ---")

# 1. Image Gen
print("\n[1] Google Image Generator")
try:
    gen = GoogleImageGenerator()
    if gen.model:
        print("PASS: Gemini Imagen Model Configured")
    else:
        print("FAIL: Gemini Imagen Model NOT Configured")
except Exception as e:
    print(f"Error init ImageGen: {e}")

# 2. Email
print("\n[2] Email Sender")
email = EmailSender()
if email.sender_email:
    print(f"PASS: Email Configured for {email.sender_email}")
else:
    print("WARN: Email credentials missing (Expected if not in .env)")

# 3. ChromaDB
print("\n[3] Persistent ChromaDB")
try:
    store = ChromaStore()
    store.collection.count()
    print(f"PASS: ChromaDB Connected at {store.client}")
except Exception as e:
    print(f"FAIL: ChromaDB Error: {e}")
