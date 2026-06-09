from typing import TypedDict, Optional
class QASentinelState(TypedDict):
    azure_devops_org: str
    azure_devops_project: str
    azure_devops_pat: str
    # Agent 1 outputs
    raw_work_items: Optional[str]
    parsed_requirements: Optional[str]
    # Agent 2 outputs
    foundry_iq_context: Optional[str]
    test_cases: Optional[str]
    revision_count: int
    # Quality checker
    quality_approved: bool
    # Agent 3 outputs
    playwright_script: Optional[str]
    # Error tracking
    error: Optional[str]
