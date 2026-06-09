from langchain_openai import ChatOpenAI          # Phase 1: direct OpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import QASentinelState
from plugins.azure_devops import fetch_azure_devops_tickets
import os
from dotenv import load_dotenv

load_dotenv()

# Phase 1: Use OpenAI directly
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)

# Phase 2 replacement (swap this in later):
# from langchain_openai import AzureChatOpenAI
# llm = AzureChatOpenAI(
#     azure_deployment="DeepSeek-V4-flash",
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     api_version="2024-08-01-preview",
#     temperature=0.1
# )

def ticket_reader_node(state: QASentinelState) -> QASentinelState:
    print("🔍 Agent 1: Fetching Azure DevOps tickets...")
    raw = fetch_azure_devops_tickets.invoke({
        "org": state["azure_devops_org"],
        "project": state["azure_devops_project"],
        "pat": state["azure_devops_pat"]
    })
    messages = [
        SystemMessage(content="""You are a QA analyst. Given Azure DevOps work item JSON:
        1. Extract Work Item ID and Title
        2. Write a clean feature summary
        3. List all acceptance criteria as bullet points
        4. Identify edge cases and boundary conditions
        Format clearly in markdown per work item."""),
        HumanMessage(content=f"Work Items:\n{raw}")
    ]
    response = llm.invoke(messages)
    print(response)
    print("✅ Agent 1 complete")
    return {**state, "raw_work_items": raw, "parsed_requirements": response.content}