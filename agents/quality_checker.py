from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import QASentinelState
from agents.ticket_reader import llm

def quality_checker_node(state: QASentinelState) -> QASentinelState:
    print("🔎 Quality Checker: Evaluating test case coverage...")
    messages = [
        SystemMessage(content="""Evaluate these test cases. Respond with EXACTLY one of:
        APPROVED - all AC covered, 30%+ negative/edge cases, clear Given/When/Then format
        REVISION_NEEDED - incomplete, then list specifically what is missing"""),
        HumanMessage(content=state["test_cases"])
    ]
    response = llm.invoke(messages)
    approved = response.content.strip().startswith("APPROVED")
    print(f"{'✅ Approved' if approved else '🔄 Needs revision'}")
    return {**state, "quality_approved": approved}

def should_revise(state: QASentinelState) -> str:
    if state["quality_approved"] or state.get("revision_count", 0) >= 2:
        return "approved"
    state["revision_count"] = state.get("revision_count", 0) + 1
    return "needs_revision"