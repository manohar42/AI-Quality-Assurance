from graph.pipeline import app
from dotenv import load_dotenv
import os

load_dotenv()

print("🚀 Starting QA Sentinel pipeline...\n")

result = app.invoke({
    "azure_devops_org": os.getenv("AZURE_DEVOPS_ORG"),
    "azure_devops_project": os.getenv("AZURE_DEVOPS_PROJECT"),
    "azure_devops_pat": os.getenv("AZURE_DEVOPS_PAT"),
    "revision_count": 0,
    "quality_approved": False,
    "raw_work_items": None,
    "parsed_requirements": None,
    "foundry_iq_context": None,
    "test_cases": None,
    "playwright_script": None,
    "error": None
})

print("\n" + "="*60)
print("✅ PIPELINE COMPLETE")
print("="*60)
print(f"Revisions needed: {result['revision_count']}")
print(f"\n--- TEST CASES PREVIEW ---")
print(result["test_cases"][:800] if result["test_cases"] else "None")
print(f"\n--- OUTPUT ---")
print("Script saved to: output/generated_tests/test_generated.py")