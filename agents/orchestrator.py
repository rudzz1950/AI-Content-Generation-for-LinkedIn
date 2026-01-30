from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.critic_agent import CriticAgent

# Define the State
class AgentState(TypedDict):
    topic: str
    context: Dict[str, Any]
    draft: str
    review: Dict[str, Any]
    revision_count: int
    final_post: str

class OrchestratorAgent:
    def __init__(self, researcher: ResearchAgent, writer: WriterAgent, critic: CriticAgent):
        self.researcher = researcher
        self.writer = writer
        self.critic = critic
        self.workflow = self._build_graph()
        
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        # Add Nodes
        workflow.add_node("research", self.research_node)
        workflow.add_node("draft", self.draft_node)
        workflow.add_node("critique", self.critique_node)
        workflow.add_node("revise", self.revise_node)
        
        # Define Edges
        workflow.set_entry_point("research")
        workflow.add_edge("research", "draft")
        workflow.add_edge("draft", "critique")
        
        # Conditional Logic for Loop
        workflow.add_conditional_edges(
            "critique",
            self.check_review,
            {
                "approved": END,
                "revise": "revise"
            }
        )
        
        workflow.add_edge("revise", "critique") # Loop back to critic
        
        return workflow.compile()

    # --- Node Implementations ---
    
    def research_node(self, state: AgentState):
        print(f"--- Researching: {state['topic']} ---")
        topic = state["topic"]
        # Assuming context has initial articles, we let researcher dive deeper
        # For simplicity, we just pass the existing context or enhance it
        if "research_summary" not in state["context"]:
             # If no summary, do deep research
             summary = self.researcher.research_topic(topic, state["context"].get("articles", []))
             state["context"]["research_summary"] = summary
             
        return {"context": state["context"]}

    def draft_node(self, state: AgentState):
        print("--- Drafting Post ---")
        draft = self.writer.generate(state["context"])
        return {"draft": draft, "revision_count": 0}

    def critique_node(self, state: AgentState):
        print("--- Critiquing Draft ---")
        review = self.critic.review_post(state["draft"], state["context"])
        return {"review": review}

    def revise_node(self, state: AgentState):
        print(f"--- Revising Draft (Attempt {state['revision_count'] + 1}) ---")
        # Logic: We could ask Writer to revise, or use the Critic's "revised_post"
        # For this v1, we trust the Critic's revised version if available,
        # or we could prompt the writer again with feedback.
        
        # Taking Critic's suggested revision directly for efficiency:
        new_draft = state["review"].get("revised_post", state["draft"])
        
        return {
            "draft": new_draft, 
            "revision_count": state["revision_count"] + 1
        }

    # --- Conditional Logic ---
    
    def check_review(self, state: AgentState):
        score = state["review"].get("score", 0)
        count = state["revision_count"]
        
        # Approve if score is high OR max revisions reached
        if score >= 8 or count >= 3:
            state["final_post"] = state["draft"]
            print(f"--- Post Approved (Score: {score}) ---")
            return "approved"
        else:
            print(f"--- Requesting Revision (Score: {score}) ---")
            return "revise"
            
    def run(self, topic: str, context: Dict):
        """Entry point to run the graph."""
        inputs = {
            "topic": topic,
            "context": context,
            "draft": "",
            "review": {},
            "revision_count": 0,
            "final_post": ""
        }
        
        # Invoke the graph
        final_state = self.workflow.invoke(inputs)
        return final_state["draft"] # Return final draft
