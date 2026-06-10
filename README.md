# 🛡️ QA Sentinel

> **Intelligent agents that read your tickets, write your tests, and guard your code.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)](https://langchain.com)
[![Azure DevOps](https://img.shields.io/badge/Azure%20DevOps-REST%20API-blue.svg)](https://dev.azure.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Overview

**QA Sentinel** is a multi-agent AI system that eliminates the manual effort of writing QA test cases and Playwright automation scripts. It reads your active Azure DevOps User Stories and Bug tickets, reasons over them using a knowledge base of QA standards, generates structured Given/When/Then test cases, and outputs ready-to-run Playwright Python scripts — all automatically.

Built for the **Agents League Hackathon 2026** — Reasoning Agents Track.

> **Phase 1** — Fully functional local build using a mock knowledge base (local `.md` files) and OpenAI directly. No Azure Foundry dependency required to run. Phase 2 swaps in DeepSeek-V4-Flash via Azure AI Foundry and Foundry IQ in two file changes.

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         INPUT LAYER                                 │
│                                                                     │
│   [Azure DevOps REST API]          [Local Knowledge Base (.md)]     │
│   User Stories + Bugs              Coding Standards + Test Patterns │
└────────────────┬────────────────────────────┬───────────────────────┘
                 │                            │
                 ▼                            │
┌─────────────────────────────────────────────────────────────────────┐
│                  LANGGRAPH MULTI-AGENT PIPELINE                     │
│                                                                     │
│  ┌──────────────────┐    ┌───────────────────┐   ┌───────────────┐  │
│  │  Agent 1         │    │  Agent 2          │   │  Agent 3      │  │
│  │  Ticket Reader   │───▶│  Test Case Writer │──▶│  Script Gen  │  │
│  │                  │    │  (uses KB context)│   │               │  │
│  └──────────────────┘    └────────┬──────────┘   └──────┬────────┘  │
│                                   │  ▲                  │           │
│                           ┌───────▼──┴──────┐           │           │
│                           │ Quality Checker  │          │           │
│                           │ (loop ≤ 2 times) │          │           │
│                           └─────────────────┘           │           │
└─────────────────────────────────────────────────────────┼───────────┘
                                                           │ 
┌──────────────────────────────────────────────────────────▼──────────┐
│                          OUTPUT LAYER                               │
│                                                                     │
│          [Playwright .py Test Scripts]    [Local output/ folder]    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      LLM + TRIGGER LAYER                            │
│                                                                     │
│    OpenAI gpt-4o-mini (Phase 1)      FastAPI /run endpoint          │
└─────────────────────────────────────────────────────────────────────┘
```

### Agent Descriptions

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Agent 1 — Ticket Reader** | Fetches work items from Azure DevOps via REST API and uses LLM to extract clean requirements and acceptance criteria | Azure DevOps WIQL response | `parsed_requirements` |
| **Agent 2 — Test Case Writer** | Queries local knowledge base for org standards, then generates structured Given/When/Then test cases with 30%+ negative cases | `parsed_requirements` + KB context | `test_cases` |
| **Quality Checker** | Evaluates test case completeness and coverage — loops back to Agent 2 up to 2 times if insufficient | `test_cases` | `quality_approved` boolean |
| **Agent 3 — Script Generator** | Converts approved test cases into a complete pytest + Playwright Python test file using async/await and Page Object Model | `test_cases` | `playwright_script` saved to disk |

---

## 📁 Project Structure

```text
qa-sentinel/
├── agents/
│   ├── ticket_reader.py        ← Agent 1: Reads & parses DevOps tickets
│   ├── test_case_writer.py     ← Agent 2: Generates test cases with KB grounding
│   ├── quality_checker.py      ← Quality gate + conditional loop router
│   └── script_generator.py    ← Agent 3: Generates Playwright Python scripts
├── graph/
│   ├── state.py                ← QASentinelState TypedDict (shared pipeline state)
│   └── pipeline.py             ← LangGraph StateGraph wiring + compilation
├── plugins/
│   ├── azure_devops.py         ← @tool: fetch active work items from Azure DevOps
│   └── foundry_iq.py           ← @tool: query knowledge base (Phase 1: local mock)
├── api/
│   └── main.py                 ← FastAPI app with /run and /health endpoints
├── output/
│   └── generated_tests/        ← Generated Playwright .py scripts saved here
├── knowledge_base/
│   ├── coding_standards.md     ← QA standards and test case rules
│   ├── test_patterns.md        ← Playwright patterns and conventions
│   └── past_bugs.md            ← Common bug patterns to always test
├── run.py                      ← Direct pipeline runner (no FastAPI needed)
├── test_connections.py         ← Verify Azure DevOps + OpenAI connections
├── .env.example                ← Template with all required variables
├── requirements.txt
└── README.md
```

---

## ⚙️ Prerequisites

- **Python 3.11+** — [Download](https://python.org/downloads)
- **Azure DevOps account** — [Free at dev.azure.com](https://dev.azure.com)
  - A project using the **Agile** process template
  - Active **User Stories** and/or **Bugs** with Acceptance Criteria filled in
  - A **Personal Access Token (PAT)** with `Work Items (Read)` scope
- **OpenAI API Key** — [Get one at platform.openai.com](https://platform.openai.com)
  - The project uses `gpt-4o-mini` by default (very low cost)
- **Git** — for cloning and version control

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/qa-sentinel.git
cd qa-sentinel
```

### 2. Create a Virtual Environment

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env
```

Open `.env` and fill in your values:

```bash
# .env
OPENAI_API_KEY=sk-your-openai-key-here

AZURE_DEVOPS_ORG=your-organization-name
AZURE_DEVOPS_PROJECT=your-project-name
AZURE_DEVOPS_PAT=your-personal-access-token
```

### 5. Verify Connections

```bash
python test_connections.py
```

Expected output:
```text
Testing connections...

✅ OpenAI: Connected — gpt-4o-mini ready
✅ Azure DevOps: 200 OK — 5 active work items found
✅ Knowledge Base: 3 local files loaded

🎉 All connections verified! Ready to run pipeline.
```

---

## ▶️ How to Run

### Option A — Direct Runner (Quickest)

```bash
python run.py
```

Sample output:
```text
🚀 Starting QA Sentinel pipeline...

🔍 Agent 1: Fetching Azure DevOps tickets...
✅ Agent 1 complete — 5 work items parsed

✍️  Agent 2: Querying knowledge base + writing test cases...
✅ Agent 2 complete — 18 test cases generated

🔎 Quality Checker: Evaluating test case coverage...
✅ Approved — coverage sufficient

🤖 Agent 3: Generating Playwright scripts...
✅ Agent 3 complete — script saved

============================================================
✅ PIPELINE COMPLETE
============================================================
Revisions needed: 0
Script saved to: output/generated_tests/test_generated.py
```

### Option B — FastAPI Server

```bash
uvicorn api.main:api --reload --port 8000
```

Trigger the pipeline:
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{}'
```

With custom credentials:
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"org":"my-org","project":"my-project","pat":"my-pat"}'
```

Health check:
```bash
curl http://localhost:8000/health
# {"status": "QA Sentinel is running", "version": "1.0.0"}
```

Interactive API docs:
```text
http://localhost:8000/docs
```

### View the Generated Test Script

```bash
cat output/generated_tests/test_generated.py
```

### Run the Generated Tests

```bash
# Install Playwright browsers (first time only)
playwright install chromium

# Run tests
pytest output/generated_tests/test_generated.py -v
```

---

## 📄 Example Output

### Test Cases Generated (Agent 2)

```text
TC-001: Valid Login with Correct Credentials
Given: A registered user with email "user@example.com" and password "Pass@123"
When: User enters valid credentials and clicks Login
Then: User is redirected to the dashboard and sees their name in the navbar

TC-002: Login Fails with Wrong Password
Given: A registered user with email "user@example.com"
When: User enters an incorrect password and clicks Login
Then: Error message "Invalid email or password" is displayed

TC-003: Account Locks After 5 Failed Attempts
Given: A registered user attempting to login
When: User fails login 5 consecutive times
Then: Account is locked and message "Account locked. Contact support." is shown

TC-004: Login Blocked with Empty Email
Given: User is on the login page
When: User leaves the email field empty and clicks Login
Then: Inline error "Email is required" is displayed below the email field
```

### Playwright Script Generated (Agent 3)

```python
import pytest
from playwright.async_api import async_playwright, expect

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.email_input = page.get_by_test_id("email")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-btn")
        self.error_message = page.get_by_test_id("error-msg")

    async def login(self, email: str, password: str):
        await self.email_input.fill(email)
        await self.password_input.fill(password)
        await self.login_button.click()

@pytest.mark.asyncio
class TestTC001ValidLogin:
    async def test_valid_login_redirects_to_dashboard(self, page):
        login = LoginPage(page)
        await page.goto("http://localhost:3000/login")
        await login.login("user@example.com", "Pass@123")
        await expect(page).to_have_url("http://localhost:3000/dashboard")
```

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Agent Orchestration** | LangGraph 0.2+ | Multi-agent StateGraph pipeline |
| **LLM Framework** | LangChain 0.3+ | LLM abstraction, tool calling |
| **LLM (Phase 1)** | OpenAI gpt-4o-mini | Reasoning and code generation |
| **Work Item Source** | Azure DevOps REST API | Fetches User Stories and Bugs |
| **Knowledge Base (Phase 1)** | Local Markdown files | QA standards and test patterns |
| **API Trigger** | FastAPI + Uvicorn | HTTP endpoint to run pipeline |
| **Test Output** | Playwright + pytest | Generated automation scripts |
| **Env Management** | python-dotenv | Credential management |

---

## 🔄 Phase 2 Upgrade Path

Phase 1 is fully functional. When Azure AI Foundry is ready, only **2 files change**:

| File | Phase 1 | Phase 2 |
|------|---------|---------|
| `plugins/foundry_iq.py` | Reads local `.md` files | Calls Foundry IQ via `AIProjectClient` |
| `agents/ticket_reader.py` | `ChatOpenAI` (gpt-4o-mini) | `AzureChatOpenAI` (DeepSeek-V4-Flash) |

Zero changes to agents, pipeline, state, or API.

---

## 🌐 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Phase 1 ✅ | OpenAI API key for gpt-4o-mini |
| `AZURE_DEVOPS_ORG` | ✅ Always | Your Azure DevOps organization name |
| `AZURE_DEVOPS_PROJECT` | ✅ Always | Your Azure DevOps project name |
| `AZURE_DEVOPS_PAT` | ✅ Always | Personal Access Token (Work Items: Read) |
| `AZURE_OPENAI_ENDPOINT` | Phase 2 | Azure OpenAI resource endpoint |
| `AZURE_OPENAI_API_KEY` | Phase 2 | Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT` | Phase 2 | Deployment name (DeepSeek-V4-flash) |
| `PROJECT_ENDPOINT` | Phase 2 | Azure AI Foundry project endpoint |
| `AZURE_SEARCH_ENDPOINT` | Phase 2 | Azure AI Search endpoint |
| `AZURE_SEARCH_API_KEY` | Phase 2 | Azure AI Search admin key |
| `FOUNDRY_IQ_KB_NAME` | Phase 2 | Knowledge base name in Foundry IQ |

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `No active work items found` | Work items have wrong State | Open DevOps → set State to **Active** |
| `401 Unauthorized` on DevOps | PAT expired or wrong scope | Regenerate PAT with `Work Items: Read` |
| `openai.AuthenticationError` | Invalid API key | Check `OPENAI_API_KEY` in `.env` |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `No such file: knowledge_base` | Missing KB folder | Create `knowledge_base/` with `.md` files |
| Pipeline produces empty test cases | Empty Acceptance Criteria in DevOps | Add Acceptance Criteria to each work item |

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) — multi-agent orchestration framework
- [LangChain](https://langchain.com) — LLM integration toolkit
- [Azure DevOps](https://azure.microsoft.com/en-us/products/devops) — work item management
- [Playwright](https://playwright.dev) — browser automation framework
- [FastAPI](https://fastapi.tiangolo.com) — modern Python web framework
- **Agents League Hackathon 2026** — for the inspiration to build this

---

*Built with ❤️ for the Agents League Hackathon 2026 — Reasoning Agents Track*
