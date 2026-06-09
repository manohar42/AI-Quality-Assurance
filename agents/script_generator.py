from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import QASentinelState
from agents.ticket_reader import llm
import os

def script_generator_node(state: QASentinelState) -> QASentinelState:
    print("🤖 Agent 3: Generating Playwright scripts...")
    messages = [
        SystemMessage(content="""You are a Playwright Python automation engineer.
        Convert the test cases into a complete pytest + Playwright test file:
        - Use async/await pattern
        - pytest fixtures for browser setup/teardown
        - Page Object Model
        - Test names matching TC-IDs
        - pytest assert statements with clear messages
        - Add comments for complex steps
        Output valid, complete Python code only."""),
        HumanMessage(content=state["test_cases"])
    ]
    response = llm.invoke(messages)
    os.makedirs("output/generated_tests", exist_ok=True)
    with open("output/generated_tests/test_generated.py", "w") as f:
        f.write(response.content)
    print("✅ Agent 3 complete — script saved")
    return {**state, "playwright_script": response.content}