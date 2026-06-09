from langchain_core.tools import tool
import os

KNOWLEDGE_BASE_DIR = "knowledge_base"

@tool
def query_foundry_iq(query: str) -> str:
    """
    PHASE 1 MOCK: Reads from local knowledge_base/ folder.
    Replace with real Foundry IQ API call in Phase 2.
    """
    results = []
    try:
        for filename in os.listdir(KNOWLEDGE_BASE_DIR):
            if filename.endswith(".md"):
                with open(os.path.join(KNOWLEDGE_BASE_DIR, filename), "r") as f:
                    content = f.read()
                    results.append(f"[Source: {filename}]\n{content}")
        return "\n\n---\n\n".join(results) if results else "No knowledge base files found."
    except Exception as e:
        return f"Knowledge base unavailable: {str(e)}"