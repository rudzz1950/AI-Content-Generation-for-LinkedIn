from agents.critic_agent import CriticAgent
from agents.orchestrator import OrchestratorAgent
from intelligence.embeddings import EmbeddingService
from intelligence.classifier import TopicClassifier
import os

def test_critic():
    print("\n--- Testing Critic Agent (OpenAI) ---")
    if not os.getenv("OPENAI_API_KEY"):
        print("SKIPPING: OPENAI_API_KEY not found")
        return
    
    critic = CriticAgent()
    draft = "AI is cool."
    context = {"topic": "AI"}
    
    review = critic.review_post(draft, context)
    print(f"Score: {review.get('score')}")
    print("Critic Agent: PASS")

def test_gemini_tools():
    print("\n--- Testing Gemini Embeddings & Classifier ---")
    if not os.getenv("GEMINI_API_KEY"):
        print("SKIPPING: GEMINI_API_KEY not found")
        return

    # Embeddings
    embedder = EmbeddingService()
    vec = embedder.embed_query("Hello world")
    print(f"Embedding Dim: {len(vec)}")
    assert len(vec) > 0
    
    # Classifier
    classifier = TopicClassifier()
    topic = classifier.classify("New funding for AI startup in San Francisco")
    print(f"Classified Topic: {topic}")
    assert topic in classifier.candidate_labels or topic == "Uncategorized"
    print("Gemini Tools: PASS")

def test_orchestrator_build():
    print("\n--- Testing Orchestrator Graph Build ---")
    try:
        o = OrchestratorAgent(None, None, None)
        print("Orchestrator: PASS")
    except Exception as e:
        print(f"Orchestrator Build FAIL: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    test_critic()
    test_gemini_tools()
    test_orchestrator_build()
