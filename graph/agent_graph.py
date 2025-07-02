from langgraph.graph import StateGraph
from agents.orchestrator_agent import get_orchestrator
from agents.hubspot_agent import create_contact, update_contact, create_deal, update_deal
from agents.email_agent import send_email
from pydantic import BaseModel
import re
from utils.helpers import extract_email

# --- Step 1: Shared state for graph ---
class AgentState(BaseModel):
    query: str
    result: str | None = None
    email_to: str | None = None
    email_subject: str | None = None
    email_body: str | None = None

# --- Step 2: Orchestrator node ---
def orchestrator_node(state: AgentState) -> AgentState:
    try:
        tools = [create_contact, update_contact, create_deal, update_deal]
        orchestrator = get_orchestrator(tools)
        if not orchestrator:
            raise RuntimeError("Failed to initialize orchestrator.")

        result = orchestrator.run(state.query)

        # Fallback/defaults
        subject = "✅ Action Performed"
        body = result
        email_to = extract_email(result) or "admin@example.com"
        print("resss",result)

        # Optional: smarter subject selection
        result_lower = result.lower()
        if "created contact" in result_lower:
            subject = "✅ Contact Created"
        elif "created deal" in result_lower:
            subject = "✅ Deal Created"
        elif "updated" in result_lower and "contact" in result_lower:
            subject = "✅ Contact Updated"
        elif "updated" in result_lower and "deal" in result_lower:
            subject = "🛠️ Deal Updated"

        # Update state
        state.result = result
        state.email_subject = subject
        state.email_body = body
        state.email_to = email_to

    except Exception as e:
        error_msg = f"❌ Error in orchestrator_node: {e}\n{traceback.format_exc()}"
        print(error_msg)
        state.result = error_msg
        state.email_subject = "❌ Orchestration Failed"
        state.email_body = error_msg
        state.email_to = "admin@example.com"

    return state

# --- Step 3: Wrap send_email to use state ---
def send_email_node(state: AgentState) -> AgentState:
    try:
        email_result = send_email(
            to_email=state.email_to,
            subject=state.email_subject,
            body=state.email_body,
        )
        state.result += f"\n\nEmail result: {email_result}"
    except Exception as e:
        error_msg = f"Error sending email: {e}\n{traceback.format_exc()}"
        print(error_msg)
        state.result += f"\n\n{error_msg}"
    return state

# --- Step 4: Build and run graph ---
def run_agent_graph(user_query: str):
    try:
        graph = StateGraph(AgentState)

        graph.add_node("orchestrator", orchestrator_node)
        graph.add_node("send_email", send_email_node)

        graph.set_entry_point("orchestrator")
        graph.add_edge("orchestrator", "send_email")
        graph.set_finish_point("send_email")

        app = graph.compile()
        return app.invoke({"query": user_query})

    except Exception as e:
        error_msg = f"Critical error running the agent graph: {e}\n{traceback.format_exc()}"
        print(error_msg)
        return AgentState(query=user_query, result=error_msg)
