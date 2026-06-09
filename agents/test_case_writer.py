from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import QASentinelState
from plugins.foundry_iq import query_foundry_iq
from agents.ticket_reader import llm

def test_case_writer_node(state: QASentinelState) -> QASentinelState:
    print("✍️ Agent 2: Querying knowledge base + writing test cases...")
    kb_context = query_foundry_iq.invoke({
        "query": f"test patterns for: {state['parsed_requirements'][:300]}"
    })
    revision_note = ""
    if state.get("revision_count", 0) > 0:
        revision_note = "\nPrevious attempt rejected. Add more negative and edge case coverage."

    messages = [
        SystemMessage(content=f"""You are a senior QA engineer.
        Use this org-specific knowledge base context:
        === KNOWLEDGE BASE CONTEXT ===
        {kb_context}
        ==============================
        Generate comprehensive test cases including positive, negative, and edge cases.
        Format each as:
        TC-{{ID}}: {{Title}}
        Given: {{precondition}}
        When: {{action}}
        Then: {{expected result}}
        Minimum 30% must be negative or edge cases.{revision_note}"""),
        HumanMessage(content=state["parsed_requirements"])
    ]
    response = llm.invoke(messages)
    print("✅ Agent 2 complete")
    return {
        **state,
        "foundry_iq_context": kb_context,
        "test_cases": response.content,
        "revision_count": state.get("revision_count", 0)
    }