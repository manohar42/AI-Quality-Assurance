import requests
from base64 import b64encode
from langchain_core.tools import tool
import os

@tool
def fetch_azure_devops_tickets(org: str, project: str, pat: str) -> str:
    """Fetches active User Stories and Bugs from Azure DevOps."""
    try:
        token = b64encode(f":{pat}".encode()).decode()
        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }
        wiql_url = f"https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.1"
        wiql_body = {
            "query": """SELECT [System.Id],[System.Title],[System.Description],
                        [Microsoft.VSTS.Common.AcceptanceCriteria]
                        FROM WorkItems
                        WHERE [System.WorkItemType] IN ('User Story','Bug')
                        AND [System.State] = 'Active'
                        ORDER BY [System.CreatedDate] DESC"""
        }
        wiql_resp = requests.post(wiql_url, json=wiql_body, headers=headers)
        ids = [i["id"] for i in wiql_resp.json().get("workItems", [])[:5]]
        if not ids:
            return "No active work items found."

        fields = "System.Title,System.Description,Microsoft.VSTS.Common.AcceptanceCriteria"
        detail_url = (
            f"https://dev.azure.com/{org}/{project}/_apis/wit/workitems"
            f"?ids={','.join(map(str,ids))}&fields={fields}&api-version=7.1"
        )
        return requests.get(detail_url, headers=headers).text
    except Exception as e:
        return f"Azure DevOps error: {str(e)}"