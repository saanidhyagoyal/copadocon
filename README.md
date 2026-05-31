# 🚀 Copado Native MCP Server — Track C

> **CopadoCon Headless Hackathon** · Full native integration of the **Copado CI/CD Actions REST API** and **Agentia Testing (CRT) Open API** via the Model Context Protocol.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/protocol-MCP-purple.svg)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [🏆 Track C Requirements Addressed](#-track-c-requirements-addressed)
- [Architecture](#architecture)
- [Tools Reference](#tools-reference)
- [Setup & Installation](#setup--installation)
- [MCP Client Configuration](#mcp-client-configuration)
- [Mock Mode](#mock-mode)
- [Safety Guardrails](#safety-guardrails)
- [Rule Compliance](#rule-compliance)

---

## Overview

This MCP server exposes **13 granular tools + 1 macro orchestration tool** that allow any MCP-compatible AI client (Claude Desktop, Cursor, custom agents) to perform the full Copado DevOps lifecycle — from committing metadata to deploying to production and running automated CRT test suites — entirely through natural language, with **zero browser interaction**.

### Key Capabilities

| Category | Tools |
|---|---|
| **CI/CD Actions** | `copado_commit`, `copado_promote`, `copado_validate`, `copado_deploy` |
| **User Story Mgmt** | `copado_list_user_stories`, `copado_get_user_story_details` |
| **Environment Mgmt** | `copado_list_environments` |
| **Job Tracking** | `copado_poll_job_execution` |
| **CRT Testing** | `crt_trigger_test_job`, `crt_poll_execution_status`, `crt_retrieve_test_results`, `crt_list_test_jobs` |
| **Autonomous Loop** | `copado_autonomous_delivery_loop` |

---

## 🏆 Track C Requirements Addressed

### Copado API Surfaces Utilized

1. **Copado CI/CD Actions REST API (Agentia Pro)**
   - Base URL: `https://copadogpt-api.robotic.copado.com`
   - Endpoints: `/actions/commit`, `/actions/promote`, `/actions/validate`, `/actions/deploy`, `/user-stories`, `/user-stories/{id}`, `/environments`, `/job-executions/{id}`
   - Auth: `X-Authorization` header

2. **Agentia Testing Instance (CRT) Open API**
   - Path prefix: `/pace/v4`
   - Endpoints: `/projects/{id}/jobs/{id}/builds` (POST/GET), `/builds/{id}/results`, `/projects/{id}/jobs`
   - Auth: `X-Authorization` header

### Copado Browser UI Interactions Eliminated

This MCP server **completely eliminates** the following manual browser-based workflows from a developer's daily flow:

- ✅ **Manually clicking 'Commit'** in the Copado UI to snapshot metadata — replaced by `copado_commit`
- ✅ **Navigating to a User Story and clicking 'Promote'** — replaced by `copado_promote`
- ✅ **Clicking 'Validate' and waiting for the browser to refresh** — replaced by `copado_validate`
- ✅ **Opening the deployment wizard and clicking 'Deploy'** — replaced by `copado_deploy`
- ✅ **Scrolling through web tables to find User Story IDs** and details — replaced by `copado_list_user_stories` and `copado_get_user_story_details`
- ✅ **Navigating to Pipeline Manager to view environments** — replaced by `copado_list_environments`
- ✅ **Context-switching to the Job Execution detail page** to check logs — replaced by `copado_poll_job_execution`
- ✅ **Opening the CRT dashboard in a separate browser tab** to trigger test runs — replaced by `crt_trigger_test_job`
- ✅ **Refreshing the CRT build page to check test progress** — replaced by `crt_poll_execution_status`
- ✅ **Navigating CRT result tables to read pass/fail details** — replaced by `crt_retrieve_test_results`
- ✅ **Browsing the CRT project to find available test jobs** — replaced by `crt_list_test_jobs`
- ✅ **Manually executing the full commit→validate→promote→deploy→test sequence** across multiple UI pages — replaced by the single `copado_autonomous_delivery_loop` macro tool

---

## Architecture

```
┌─────────────────────────┐
│  MCP Client             │
│  (Claude / Cursor /     │
│   Custom Agent)         │
└──────────┬──────────────┘
           │ MCP Protocol (stdio)
           ▼
┌─────────────────────────┐
│  server.py (FastMCP)    │
│  ┌───────────────────┐  │
│  │ 8× CI/CD Tools    │  │
│  │ 4× CRT Tools      │  │
│  │ 1× Macro Loop     │  │
│  │ Production Guard   │  │
│  └───────────────────┘  │
└──────────┬──────────────┘
           │ httpx (async)
           ▼
┌─────────────────────────┐
│  Downstream API Endpoint│
│  (Real Copado API or    │
│   simulator.py FastAPI) │
└─────────────────────────┘
```

---

## Tools Reference

### Surface 1: CI/CD Actions

| Tool | Method | Endpoint | Description |
|---|---|---|---|
| `copado_commit` | POST | `/actions/commit` | Commit metadata from a user story |
| `copado_promote` | POST | `/actions/promote` | Promote user story to next environment |
| `copado_validate` | POST | `/actions/validate` | Run validation-only deployment |
| `copado_deploy` | POST | `/actions/deploy` | Execute deployment (with PROD guardrail) |
| `copado_list_user_stories` | GET | `/user-stories` | List/filter user stories |
| `copado_get_user_story_details` | GET | `/user-stories/{id}` | Get user story details + metadata |
| `copado_list_environments` | GET | `/environments` | List pipeline environments |
| `copado_poll_job_execution` | GET | `/job-executions/{id}` | Poll job execution status/logs |

### Surface 2: CRT Testing

| Tool | Method | Endpoint | Description |
|---|---|---|---|
| `crt_trigger_test_job` | POST | `/pace/v4/.../builds` | Trigger a test job |
| `crt_poll_execution_status` | GET | `/pace/v4/.../builds/{id}` | Poll build status |
| `crt_retrieve_test_results` | GET | `/pace/v4/.../builds/{id}/results` | Get test results |
| `crt_list_test_jobs` | GET | `/pace/v4/.../jobs` | List available test jobs |

### Macro Tool

| Tool | Description |
|---|---|
| `copado_autonomous_delivery_loop` | Full pipeline: commit → validate → promote → deploy → CRT tests |

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- A Copado API token (for live mode)

### Install

```bash
cd copadacon
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run

You can run the MCP server in two modes:

#### 1. Simulator Mode (Local Testing)
Run the standalone mock API simulator server first in one terminal:
```bash
source .venv/bin/activate
python3 simulator.py
```
This starts the mock API on `http://127.0.0.1:8000`.

Then, run the MCP server (it will automatically connect to `http://127.0.0.1:8000` by default):
```bash
source .venv/bin/activate
python3 server.py
```

To run verification tests:
```bash
source .venv/bin/activate
python3 test_simulator.py
```

#### 2. Live API Mode
To connect to the live Copado API, override `COPADO_BASE_URL` and supply your authorization token:
```bash
export COPADO_API_TOKEN="your-real-token"
export COPADO_BASE_URL="https://copadogpt-api.robotic.copado.com"
python3 server.py
```

---

## MCP Client Configuration

### Cursor IDE

Add to your Cursor MCP settings (`.cursor/mcp.json` or the global settings):

```json
{
  "mcpServers": {
    "copado-native": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/absolute/path/to/copadacon",
      "env": {
        "COPADO_API_TOKEN": "<YOUR_TOKEN>",
        "COPADO_BASE_URL": "https://copadogpt-api.robotic.copado.com"
      }
    }
  }
}
```

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "copado-native": {
      "command": "python",
      "args": ["/absolute/path/to/copadacon/server.py"],
      "env": {
        "COPADO_API_TOKEN": "<YOUR_TOKEN>"
      }
    }
  }
}
```

### VS Code (Copilot MCP)

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "copado-native": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

---

## Mock Simulator Server

The mock engine has been completely separated into `simulator.py` to keep `server.py` production-ready and free of simulator logic. 

- **Independent service**: Runs as a separate FastAPI web application.
- **Request logging**: Prints every single incoming HTTP request (headers, method, path, query, and payload) to `sys.stderr` so you can verify that the MCP server is communicating with it correctly.
- **Contract-faithful**: Returns realistic Copado response shapes and statuses.

---

## Safety Guardrails

### Production Deployment Protection

Any tool that targets `PROD` requires an explicit `confirm_production: true` parameter:

```
User: "Deploy US-1001 to PROD"

Server Response:
🚫 Deployment to PROD blocked. You must set 'confirm_production'
to True to acknowledge this production deployment.
```

This applies to both `copado_deploy` and `copado_autonomous_delivery_loop`.

---

## Rule Compliance

| Rule | Compliance |
|---|---|
| **Rule 6 (Demo)** | All tool outputs return pure JSON/text. No browser tabs or Copado UI URLs are opened. |
| **Rule 7 (Agent Scope)** | No references to Copado "Orchestrate Agent" or "Agentia Studio". Agent routing restricted to: `plan`, `build`, `test`, `release`, `operate`. |
| **Rule 8 (README)** | This README includes the required "Track C Requirements Addressed" section with API surfaces and eliminated UI interactions. |
| **Naming** | Macro tool named `copado_autonomous_delivery_loop` (not "orchestrate_delivery"). |

---

## License

MIT — Built for the CopadoCon Headless Hackathon, Track C.
