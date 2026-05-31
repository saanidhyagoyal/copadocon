# 📘 Copado Native MCP Server — Technical Deep Dive

> Complete technical reference covering what the code does, how the delivery loop maps to **Plan → Build → Test → Release → Operate**, and the exact migration path from the local simulator to the real Copado APIs.

---

## Table of Contents

- [1. Solution Overview](#1-solution-overview)
- [2. Architecture — How It All Connects](#2-architecture--how-it-all-connects)
- [3. MCP Tool Calls — What Decides What](#3-mcp-tool-calls--what-decides-what)
- [4. The Autonomous Delivery Loop — Plan, Build, Test, Release, Operate](#4-the-autonomous-delivery-loop--plan-build-test-release-operate)
- [5. Current State — Simulator Mode](#5-current-state--simulator-mode)
- [6. Migration Guide — Simulator → Real Copado APIs](#6-migration-guide--simulator--real-copado-apis)
- [7. File-by-File Code Walkthrough](#7-file-by-file-code-walkthrough)

---

## 1. Solution Overview

We built a **Native MCP (Model Context Protocol) Server** that exposes Copado's DevOps capabilities as tool calls to any AI client (Cursor Copilot, Claude Desktop, VS Code Copilot, or custom agents). The AI client reads the tool schemas, understands what each tool does from its description, and **automatically decides which tool to call** based on the user's natural language request.

### What problem does this solve?

Without this server, a developer must:
- Open the Copado browser UI
- Navigate to a User Story → click "Commit"
- Navigate to Pipeline Manager → click "Promote"
- Wait for pages to refresh → click "Deploy"
- Switch to a separate CRT tab → trigger tests → wait → read results

**With this MCP server**, the developer says to their AI assistant:

> _"Commit US-1001, validate it against INT, promote, deploy, and run the smoke test suite"_

…and the AI automatically chains `copado_commit` → `copado_validate` → `copado_promote` → `copado_deploy` → `crt_trigger_test_job` → `crt_poll_execution_status` → `crt_retrieve_test_results` — all without opening a browser.

### Two API Surfaces Integrated

| Surface | Auth Mechanism | Base URL |
|---------|---------------|----------|
| **Copado CI/CD Actions REST API** (Agentia Pro) | `X-Authorization: <API_KEY>` — API key generated from Copado Actions API setup | `https://copadogpt-api.robotic.copado.com` |
| **Copado Robotic Testing (CRT) Open API** | `X-Authorization: <PAK>` — Personal Access Key generated per team from the CRT profile page | `https://copadogpt-api.robotic.copado.com` (same gateway) |

> **Note:** In production, both surfaces go through the same base URL gateway. The CRT endpoints are distinguished by their `/pace/v4/` path prefix.

---

## 2. Architecture — How It All Connects

```
┌────────────────────────────────────┐
│          Developer / User          │
│  "Deploy US-1001 to INT and test"  │
└──────────────┬─────────────────────┘
               │  natural language
               ▼
┌────────────────────────────────────┐
│      AI Client (MCP Host)         │
│  Cursor / Claude Desktop / VSCode │
│                                   │
│  Reads tool schemas from mcp.json │
│  Decides: copado_deploy + crt_*   │
└──────────────┬─────────────────────┘
               │  MCP protocol (stdio)
               ▼
┌────────────────────────────────────┐
│        server.py (FastMCP)        │
│                                   │
│  14 MCP Tools registered:         │
│  • 8× Copado CI/CD Actions        │
│  • 4× CRT Testing                 │
│  • 1× Autonomous Delivery Loop    │
│  • Production guardrails          │
│                                   │
│  Reads config from .env:          │
│    COPADO_BASE_URL                │
│    COPADO_API_TOKEN               │
└──────────────┬─────────────────────┘
               │  httpx async HTTP calls
               │  with X-Authorization header
               ▼
┌────────────────────────────────────┐
│     Downstream API Endpoint       │
│                                   │
│  TODAY:    simulator.py (FastAPI)  │
│            http://127.0.0.1:8000  │
│                                   │
│  LATER:    Real Copado APIs       │
│            https://copadogpt-api  │
│            .robotic.copado.com    │
└────────────────────────────────────┘
```

### How the AI decides which tool to call

The AI client (Cursor/Claude) receives the **tool schemas** from the MCP server. Each tool has:
- A **name** (e.g., `copado_deploy`)
- A **docstring** describing what it does
- **Pydantic input fields** with descriptions explaining each parameter

The AI client uses these descriptions to match the user's intent to the correct tool. For example:
- _"Show me all user stories"_ → AI picks `copado_list_user_stories`
- _"Deploy US-1001 to UAT"_ → AI picks `copado_deploy` with `user_story_id="US-1001"`, `target_environment="UAT"`
- _"Run the full pipeline for US-1002"_ → AI picks `copado_autonomous_delivery_loop`

**The server code does NOT decide which tool to call.** The AI client does, based on the tool schemas and the user's message.

---

## 3. MCP Tool Calls — What Decides What

### Surface 1: Copado CI/CD Actions REST API (8 tools)

| Tool Name | HTTP Call | When AI Calls It |
|-----------|----------|-----------------|
| `copado_commit` | `POST /actions/commit` | User says "commit changes from US-1001" |
| `copado_promote` | `POST /actions/promote` | User says "promote US-1001 to INT" |
| `copado_validate` | `POST /actions/validate` | User says "validate US-1001 against UAT" |
| `copado_deploy` | `POST /actions/deploy` | User says "deploy US-1001 to UAT" |
| `copado_list_user_stories` | `GET /user-stories` | User says "show me all user stories" or "which stories are ready to promote?" |
| `copado_get_user_story_details` | `GET /user-stories/{id}` | User says "show me details of US-1001" |
| `copado_list_environments` | `GET /environments` | User says "what environments do we have?" |
| `copado_poll_job_execution` | `GET /job-executions/{id}` | User says "check status of job JE-abc123" |

### Surface 2: CRT Testing Open API (4 tools)

| Tool Name | HTTP Call | When AI Calls It |
|-----------|----------|-----------------|
| `crt_trigger_test_job` | `POST /pace/v4/projects/{pid}/jobs/{jid}/builds` | User says "run the smoke test suite" |
| `crt_poll_execution_status` | `GET /pace/v4/projects/{pid}/jobs/{jid}/builds/{bid}` | User says "is the test still running?" |
| `crt_retrieve_test_results` | `GET /pace/v4/projects/{pid}/jobs/{jid}/builds/{bid}/results` | User says "show me the test results" |
| `crt_list_test_jobs` | `GET /pace/v4/projects/{pid}/jobs` | User says "what test jobs are available?" |

### Macro Tool (1 tool)

| Tool Name | What It Does | When AI Calls It |
|-----------|-------------|-----------------|
| `copado_autonomous_delivery_loop` | Chains: commit → validate → promote → deploy → CRT tests | User says "run the full delivery pipeline for US-1001" |

---

## 4. The Autonomous Delivery Loop — Plan, Build, Test, Release, Operate

The `copado_autonomous_delivery_loop` tool maps directly to the **5 DevOps phases**:

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  PLAN   │───▶│  BUILD  │───▶│  TEST   │───▶│ RELEASE │───▶│ OPERATE │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### Phase Mapping

| Phase | What Happens in Code | Tools Involved | API Endpoints Hit |
|-------|---------------------|----------------|-------------------|
| **Plan** | AI reads the user story details and metadata scope. Understands what components are being changed and where they need to go. | `copado_list_user_stories`, `copado_get_user_story_details`, `copado_list_environments` | `GET /user-stories`, `GET /user-stories/{id}`, `GET /environments` |
| **Build** | Commit the metadata snapshot from the user story. This captures the current state of all components into version control. | `copado_commit` | `POST /actions/commit` |
| **Test** | (a) Run a validation-only deployment to check for errors without side-effects. (b) Trigger CRT automated test suites and retrieve results. | `copado_validate`, `crt_trigger_test_job`, `crt_poll_execution_status`, `crt_retrieve_test_results` | `POST /actions/validate`, `POST /pace/v4/.../builds`, `GET /pace/v4/.../builds/{id}`, `GET /pace/v4/.../results` |
| **Release** | Promote the user story to the target environment, then execute the deployment. Production deployments require explicit human confirmation. | `copado_promote`, `copado_deploy` | `POST /actions/promote`, `POST /actions/deploy` |
| **Operate** | Poll the job execution to monitor deployment status, check logs, verify completion. If CRT tests were triggered, poll and retrieve their results. | `copado_poll_job_execution`, `crt_poll_execution_status`, `crt_retrieve_test_results` | `GET /job-executions/{id}`, `GET /pace/v4/.../builds/{id}`, `GET /pace/v4/.../results` |

### Inside `copado_autonomous_delivery_loop` — Step by Step

When a user triggers the full delivery loop, here's exactly what happens in `server.py`:

```
Step 1 (Build)   → POST /actions/commit         → Snapshot metadata
Step 2 (Test)    → POST /actions/validate        → Dry-run deployment check
                   ↳ If validation fails → ABORT the entire loop
Step 3 (Release) → POST /actions/promote         → Move story to target env
Step 4 (Release) → POST /actions/deploy          → Execute the deployment
Step 5 (Test)    → POST /pace/v4/.../builds      → Trigger CRT test suite
                   GET  /pace/v4/.../builds/{id}  → Poll test execution
                   GET  /pace/v4/.../results      → Retrieve test results
```

**Production Guardrail:** If `target_environment` is `PROD`, the server requires `confirm_production=True`. Without it, the entire loop is rejected before any API call is made.

---

## 5. Current State — Simulator Mode

### What's running today

| Component | File | Role |
|-----------|------|------|
| MCP Server | `server.py` | Receives tool calls from AI, sends HTTP requests to `COPADO_BASE_URL` |
| Mock Simulator | `simulator.py` | Standalone FastAPI server that mimics Copado's API responses |
| Test Script | `test_simulator.py` | Automated verification that tools → simulator communication works |
| Config | `.env` | Defines `COPADO_BASE_URL=http://127.0.0.1:8000` and `COPADO_API_TOKEN=mock-dev-token-12345` |

### How the simulator validates requests

The simulator (`simulator.py`) reads `COPADO_API_TOKEN` from `.env` and enforces it:
- **Missing `X-Authorization` header** → Returns `401 Unauthorized`
- **Wrong token value** → Returns `401 Unauthorized`
- **Correct token** → Returns realistic Copado-shaped JSON responses

This means the auth flow is already fully tested end-to-end, even in simulator mode.

---

## 6. Migration Guide — Simulator → Real Copado APIs

When Copado APIs are ready, here is the **exact checklist** of what to change:

### Step 1: Update `.env` — The ONLY Required Change

```diff
  # Copado API Configuration
- COPADO_BASE_URL=http://127.0.0.1:8000
- COPADO_API_TOKEN=mock-dev-token-12345
+ COPADO_BASE_URL=https://copadogpt-api.robotic.copado.com
+ COPADO_API_TOKEN=<your-real-copado-api-key-here>
```

**That's it.** No code changes needed in `server.py`. The server reads these values from `.env` via `load_dotenv()` and passes them through to every HTTP request.

### Step 2: Authentication Details

#### For Copado CI/CD Actions REST API:
1. In your Copado org, go to **App Launcher → Copado Actions API**
2. Create a new API Key, selecting the actions you need (Commit, Promote, Deploy, Validate, etc.)
3. Copy the generated key → paste it as `COPADO_API_TOKEN` in `.env`
4. The key is sent as `X-Authorization: <key>` in every request (this is already implemented in `server.py` line 72)

#### For CRT (Copado Robotic Testing) Open API:
1. In your CRT profile page, generate a **Personal Access Key (PAK)**
2. If both APIs use the same gateway (`copadogpt-api.robotic.copado.com`), the same token works for both
3. If CRT uses a separate base URL (e.g., `https://api.robotic.copado.com`), you may need to split into two tokens — see "Potential Changes" below

### Step 3: Stop the Simulator

Simply stop `simulator.py`. You don't need it anymore:
```bash
# Kill the simulator process
# (or just don't start it)
```

### Step 4: Verify with Real APIs

```bash
# Run the test script (it imports server.py which reads .env)
source .venv/bin/activate
python3 test_simulator.py
```

If the real API returns different status codes or error formats, you'll see failures here.

---

### What Changes in server.py — Nothing (If All Goes Well)

The server is designed so that **zero code changes** are needed when switching from simulator to real APIs. Here's why:

| Concern | How It's Already Handled |
|---------|------------------------|
| **Base URL** | Read from `.env` → `COPADO_BASE_URL` |
| **API Token** | Read from `.env` → `COPADO_API_TOKEN` |
| **Auth Header** | `X-Authorization` header sent on every request (line 72 of `server.py`) |
| **Request Format** | JSON body matches Copado's expected format (e.g., `{"userStoryId": "...", "targetEnvironment": "..."}`) |
| **Response Parsing** | `resp.json()` — works with any valid JSON response |

### Potential Changes (If Real API Differs)

These are things that **might** need adjustment based on how the real Copado API actually behaves:

#### 1. Dual Authentication (if CRT uses a separate token)

If the CRT API requires a different Personal Access Key than the CI/CD API, you'll need to split the tokens:

```diff
  # .env
  COPADO_BASE_URL=https://copadogpt-api.robotic.copado.com
  COPADO_API_TOKEN=<ci-cd-api-key>
+ CRT_API_TOKEN=<crt-personal-access-key>
```

And in `server.py`, update the `_headers()` function or create a `_crt_headers()`:

```python
# server.py — add CRT-specific token
CRT_TOKEN = os.getenv("CRT_API_TOKEN", COPADO_TOKEN)

# Then in CRT tool calls, pass CRT_TOKEN instead of COPADO_TOKEN
```

#### 2. Different Base URL for CRT

If CRT is hosted on a different domain:

```diff
  # .env
  COPADO_BASE_URL=https://copadogpt-api.robotic.copado.com
+ CRT_BASE_URL=https://api.robotic.copado.com
```

And in `server.py`, add a separate CRT base URL and use it in the CRT tool calls.

#### 3. Response Shape Differences

The simulator returns simplified, flat JSON. The real API might wrap responses differently:

```json
// Simulator returns:
{"jobExecutionId": "JE-abc", "status": "Completed Successfully"}

// Real API might return:
{"data": {"jobExecutionId": "JE-abc", "status": "Completed Successfully"}, "meta": {"requestId": "..."}}
```

If this happens, add a response normalizer in `_request()`:

```python
async def _request(...) -> dict:
    ...
    data = resp.json()
    # Unwrap if the real API wraps responses
    if "data" in data and isinstance(data["data"], dict):
        return data["data"]
    return data
```

#### 4. Async Job Polling

The simulator returns `"status": "Completed Successfully"` instantly. The real API will likely return `"status": "In Progress"` first, requiring you to poll `GET /job-executions/{id}` until it completes. This is already supported via the `copado_poll_job_execution` tool — the AI client can call it repeatedly.

For the `copado_autonomous_delivery_loop`, you may want to add polling logic:

```python
# In the delivery loop, after deploy:
import asyncio

for _ in range(30):  # Max 30 attempts
    status = await _request("GET", f"/job-executions/{job_id}")
    if status.get("status") in ("Completed Successfully", "Failed"):
        break
    await asyncio.sleep(10)  # Wait 10 seconds between polls
```

#### 5. Error Handling

The real API will return proper HTTP error codes (400, 403, 404, 500). The current `_request()` function already calls `resp.raise_for_status()` which will raise `httpx.HTTPStatusError`. You may want to catch these and return user-friendly messages:

```python
async def _request(...) -> dict:
    ...
    try:
        resp = await client.request(...)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        return {
            "error": f"API_ERROR_{e.response.status_code}",
            "message": e.response.text,
            "url": str(e.request.url),
        }
```

---

## 7. File-by-File Code Walkthrough

### `server.py` — The MCP Server (452 lines)

| Section | Lines | What It Does |
|---------|-------|-------------|
| Imports & dotenv | 1–25 | Loads `.env`, imports FastMCP, httpx, Pydantic |
| Global Config | 27–47 | Reads `COPADO_BASE_URL` and `COPADO_API_TOKEN` from environment. **Crashes on startup if either is missing.** |
| `_headers()` | 66–73 | Builds HTTP headers including `X-Authorization` |
| `_request()` | 84–100 | **Central HTTP dispatcher** — every tool call goes through this single function. Makes async `httpx` calls to `COPADO_BASE_URL + path` |
| Pydantic Models | 104–170 | Input schemas with `Field(description=...)` so the AI knows what parameters each tool needs |
| CI/CD Tools | 173–286 | 8 tool functions for commit, promote, validate, deploy, list stories, get story, list envs, poll jobs |
| CRT Tools | 289–346 | 4 tool functions for trigger test, poll status, get results, list jobs |
| Delivery Loop | 349–439 | `copado_autonomous_delivery_loop` — chains all 5 phases |
| Entrypoint | 442–452 | `mcp.run()` starts the MCP server on stdio |

### `simulator.py` — The Mock API (250 lines)

| Section | What It Does |
|---------|-------------|
| dotenv + Token Load | Reads `COPADO_API_TOKEN` from `.env`. Crashes if missing. |
| Auth Middleware | Every request is checked for `X-Authorization` header. Returns `401` if missing or wrong. |
| CI/CD Endpoints | 8 FastAPI routes returning realistic Copado JSON shapes |
| CRT Endpoints | 4 FastAPI routes returning realistic CRT JSON shapes |
| Request Logging | Prints method, path, headers, and body to stderr for every request |

### `test_simulator.py` — Verification Script (73 lines)

| What It Tests |
|--------------|
| Simulator connectivity (with auth header) |
| `copado_list_environments` returns 4 environments |
| `copado_deploy` to PROD is blocked without `confirm_production` |
| `copado_deploy` to PROD succeeds with `confirm_production=True` |
| `copado_autonomous_delivery_loop` completes all 7 steps (commit → validate → promote → deploy → trigger test → poll test → get results) |

### `.env` — Configuration

```env
# To point to live Copado APIs, change this to: https://copadogpt-api.robotic.copado.com
COPADO_BASE_URL=http://127.0.0.1:8000
COPADO_API_TOKEN=mock-dev-token-12345
```

### `mcp.json` — Client Configuration

```json
{
  "mcpServers": {
    "copado-native": {
      "command": "python3",
      "args": ["server.py"],
      "cwd": "."
    }
  }
}
```

This tells Cursor/Claude/VSCode how to start the MCP server process.

---

## Quick Reference — Migration Checklist

- [ ] **Get real API credentials** from Copado Actions API setup and CRT profile page
- [ ] **Update `.env`** — change `COPADO_BASE_URL` and `COPADO_API_TOKEN`
- [ ] **Stop `simulator.py`** — no longer needed
- [ ] **Run `test_simulator.py`** against the real API to verify
- [ ] **Check response shapes** — if real API wraps responses differently, update `_request()` in `server.py`
- [ ] **Add polling logic** — if real API returns async jobs, add retry loops in `copado_autonomous_delivery_loop`
- [ ] **(Optional) Split CRT token** — if CRT uses a separate PAK, add `CRT_API_TOKEN` to `.env`
- [ ] **(Optional) Add error handling** — wrap `_request()` with `try/except` for graceful error messages
