"""
Copado Native MCP Server — Track C (CopadoCon Hackathon)
========================================================
Surfaces: Copado CI/CD Actions REST API  +  Agentia CRT Open API
Runtime:  FastMCP  ·  httpx (async)  ·  Pydantic v2
"""

from __future__ import annotations

import json
import sys
import uuid
import os
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

import httpx
from pydantic import BaseModel, Field
# pyrefly: ignore [missing-import]
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load configuration from environment file (.env)
load_dotenv()

# ──────────────────────────────────────────────
# Global config — 3 separate API surfaces
# ──────────────────────────────────────────────

# Surface 1: Copado Multicloud Webhooks (CI/CD Pipeline)
COPADO_WEBHOOK_BASE_URL = os.getenv("COPADO_WEBHOOK_BASE_URL", "").rstrip("/")
COPADO_WEBHOOK_KEY = os.getenv("COPADO_WEBHOOK_KEY", "")
COPADO_PROJECT_ID = os.getenv("COPADO_PROJECT_ID", "")
COPADO_SOURCE_ENV_ID = os.getenv("COPADO_SOURCE_ENVIRONMENT_ID", "")

# Surface 2: CRT Testing API
COPADO_CRT_BASE_URL = os.getenv("COPADO_CRT_BASE_URL", "").rstrip("/")
COPADO_CRT_TOKEN = os.getenv("COPADO_CRT_TOKEN", "")

# Surface 3: Dialogue API (AI Context Hub)
COPADO_DIALOGUE_BASE_URL = os.getenv("COPADO_DIALOGUE_BASE_URL", "https://copadogpt-api.robotic.copado.com").rstrip("/")
COPADO_API_TOKEN = os.getenv("COPADO_API_TOKEN", "")
COPADO_ORG_ID = os.getenv("COPADO_ORG_ID", "")
COPADO_DEFAULT_WORKSPACE_ID = os.getenv("COPADO_DEFAULT_WORKSPACE_ID", "")
COPADO_PLATFORM_BASE_URL = os.getenv("COPADO_PLATFORM_BASE_URL", "https://platform.robotic.copado.com").rstrip("/")

if not COPADO_WEBHOOK_BASE_URL:
    raise RuntimeError(
        "CRITICAL: 'COPADO_WEBHOOK_BASE_URL' not set. Define it in .env."
    )
if not COPADO_WEBHOOK_KEY:
    raise RuntimeError(
        "CRITICAL: 'COPADO_WEBHOOK_KEY' not set. Define it in .env."
    )

# Maps user-friendly agent names → assistantId (from Copado AI Platform docs)
AGENT_TO_ASSISTANT: dict[str, str] = {
    "plan":      "plan",       # Sprint planning, user stories, backlog management
    "build":     "build",      # Code writing, review, test coverage, troubleshooting
    "test":      "test",       # Test generation, QA, automation best practices
    "release":   "release",    # Deployments, version control, release documentation
    "operate":   "operate",    # Post-release troubleshooting, change management
    "knowledge": "knowledge",  # Default — general Copado/Salesforce expert
}

mcp = FastMCP(
    "Copado Native MCP Server",
    instructions="""IDENTITY & CORE MISSION:
You are the Copado Headless DevOps Agent. You operate exclusively via MCP. Never hallucinate data, guess IDs, or suggest browser/UI actions.

CRITICAL ROUTING (THE SEMANTIC FIREWALL):
You MUST evaluate user intent and route to the correct tool category to prevent catastrophic pipeline errors.

CATEGORY A (AI DIALOGUE): 
Trigger for questions, code generation, code review, sprint planning, or log diagnostics. 
-> Tools: `copado_start_dialogue`, `copado_send_message`, `copado_get_dialogue_history`. 
-> Agent IDs: `build` (coding/Apex), `test` (QA), `plan` (sprints), `release` (deploy strategy), `operate` (logs/errors). 
*NEVER execute pipeline tools for Category A requests.*

CATEGORY B (PIPELINE EXECUTION): 
Trigger ONLY for explicit DevOps commands (commit, promote, validate, deploy, test). 
-> Tools: `copado_commit`, `copado_deploy`, `copado_promote`, `copado_check_status`, etc.
*You MUST have an explicit User Story ID or Job ID from the user. Do not guess or auto-fetch one.*

THE "BUILD" DISAMBIGUATION RULE: 
If a user says "build an Apex class", "write code", or "review my code", this is CATEGORY A. Call `copado_start_dialogue(agent_id='build')`. DO NOT call `copado_commit` or `copado_deploy`.

THE "DEPLOY/RELEASE" DISAMBIGUATION RULE:
If a user asks for strategy or plans a release, this is CATEGORY A. Call `copado_start_dialogue(agent_id='release')`.
If the user commands an actual deployment action (e.g. 'deploy US-1001'), this is CATEGORY B. Call `copado_deploy` or `copado_promote`.

PRODUCTION GUARDRAIL: 
Deployments to 'PROD' require explicit user confirmation via the `confirm_production: true` parameter. Abort and ask the user if this is missing.

COMPOUND REQUESTS:
If the user asks for BOTH dialogue and a pipeline action (e.g. 'review my code and deploy it'), execute both sequentially. Do not stop to ask the user unless targeting PROD."""
)

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _log(label: str, data: Any) -> None:
    """Emit structured debug info to stderr for real-time verification."""
    print(f"[COPADO-MCP] [{label}] {json.dumps(data, default=str)}", file=sys.stderr)


def _uid() -> str:
    return str(uuid.uuid4())[:8]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Surface 1: Webhook request dispatcher ──

def _webhook_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "copado-webhook-key": COPADO_WEBHOOK_KEY,
    }


async def _webhook_request(
    method: str, path: str, *, body: dict | None = None, params: dict | None = None
) -> dict:
    """HTTP dispatcher for Copado Multicloud Webhooks API (Surface 1)."""
    url = f"{COPADO_WEBHOOK_BASE_URL}{path}"
    _log("WEBHOOK_REQUEST", {"method": method, "url": url, "body": body})
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.request(method, url, headers=_webhook_headers(), json=body, params=params)
        resp.raise_for_status()
        return resp.json()


# ── Surface 2: CRT request dispatcher ──

def _crt_headers() -> dict[str, str]:
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if COPADO_CRT_TOKEN:
        h["X-Authorization"] = COPADO_CRT_TOKEN
    return h


async def _crt_request(
    method: str, path: str, *, body: dict | None = None, params: dict | None = None
) -> dict:
    """HTTP dispatcher for CRT Testing API (Surface 2)."""
    base = COPADO_CRT_BASE_URL or COPADO_WEBHOOK_BASE_URL
    url = f"{base}{path}"
    _log("CRT_REQUEST", {"method": method, "url": url, "body": body})
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.request(method, url, headers=_crt_headers(), json=body, params=params)
        resp.raise_for_status()
        return resp.json()


# ── Surface 3: Dialogue request dispatcher ──

def _dialogue_headers() -> dict[str, str]:
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if COPADO_API_TOKEN:
        h["X-Authorization"] = COPADO_API_TOKEN
    return h


def _org_path(suffix: str) -> str:
    """Build an org-scoped API path: /organizations/{org_id}/{suffix}."""
    return f"/organizations/{COPADO_ORG_ID}/{suffix.lstrip('/')}"


async def _dialogue_request(
    method: str, path: str, *, body: dict | None = None, params: dict | None = None
) -> dict:
    """HTTP dispatcher for Dialogue/AI Context Hub API (Surface 3)."""
    url = f"{COPADO_DIALOGUE_BASE_URL}{path}"
    _log("DIALOGUE_REQUEST", {"method": method, "url": url, "body": body})
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.request(method, url, headers=_dialogue_headers(), json=body, params=params)
        resp.raise_for_status()
        return resp.json()


async def _dialogue_stream_request(
    method: str, path: str, *, body: dict | None = None
) -> dict:
    """HTTP dispatcher that handles streaming responses from the Dialogue messages API.

    The Copado API returns newline-delimited JSON (NDJSON), where each line is a
    JSON object with a 'type' field. Token content is in type='token' objects.
    """
    url = f"{COPADO_DIALOGUE_BASE_URL}{path}"
    _log("DIALOGUE_STREAM", {"method": method, "url": url, "body": body})
    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream(
            method, url, headers=_dialogue_headers(), json=body
        ) as resp:
            resp.raise_for_status()
            full_text = ""
            followups: list[str] = []
            model_usage: dict = {}
            chunk_count = 0
            async for line in resp.aiter_lines():
                if not line:
                    continue
                try:
                    parsed = json.loads(line)
                    chunk_count += 1
                    msg_type = parsed.get("type", "")
                    content = parsed.get("content", "")

                    if msg_type == "token" and content:
                        full_text += content
                    elif msg_type == "followup" and content:
                        followups.append(content)
                    elif msg_type == "model_usage":
                        model_usage = parsed.get("usage_summary", {})
                    elif msg_type == "status":
                        _log("STREAM_STATUS", content)
                except json.JSONDecodeError:
                    # Fallback: append raw text
                    full_text += line
            return {
                "response": full_text,
                "chunk_count": chunk_count,
                "followup_suggestions": followups,
                "model_usage": model_usage,
            }


async def _dialogue_delete_request(path: str) -> dict:
    """HTTP DELETE dispatcher for Dialogue API (returns 204 No Content)."""
    url = f"{COPADO_DIALOGUE_BASE_URL}{path}"
    _log("DIALOGUE_DELETE", {"url": url})
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.request("DELETE", url, headers=_dialogue_headers())
        resp.raise_for_status()
        if resp.status_code == 204:
            return {"status": "deleted", "detail": "Dialogue successfully deleted"}
        return resp.json()



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PYDANTIC INPUT MODELS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CommitInput(BaseModel):
    user_story_id: str = Field(..., description="Salesforce 18-char User Story Id")
    message: str = Field("MCP commit", description="Commit message")
    base_branch: str = Field("main", description="Target branch for the commit")
    execute_commit: bool = Field(True, description="Execute the commit immediately")
    recreate_feature_branch: bool = Field(False, description="Recreate the feature branch")

class PromoteInput(BaseModel):
    user_story_ids: list[str] = Field(..., description="List of Salesforce User Story IDs to promote")
    execute_deployment: bool = Field(True, description="Execute the deployment after promotion")
    deployment_dry_run: bool = Field(False, description="If true, validation only (no real deploy)")
    is_back_promotion: bool = Field(False, description="Whether this is a back-promotion")
    confirm_production: bool = Field(False, description="Must be True for PROD")

class ValidateInput(BaseModel):
    user_story_ids: list[str] = Field(..., description="List of Salesforce User Story IDs to validate")
    confirm_production: bool = Field(False, description="Must be True for PROD")

class DeployInput(BaseModel):
    promotion_id: str = Field(..., description="Salesforce Promotion Id from a prior promote response")
    execute_deployment: bool = Field(True, description="Execute the deployment")
    deployment_dry_run: bool = Field(False, description="If true, validation only")
    confirm_production: bool = Field(False, description="Must be True for PROD")

class CheckStatusInput(BaseModel):
    result_id: str = Field(..., description="Salesforce Result Id to check status for")

class CrtTriggerInput(BaseModel):
    project_id: str = Field(..., description="CRT Project Id")
    job_id: str = Field(..., description="CRT Test Job Id to trigger")
    input_parameters: Optional[dict] = Field(None, description="Optional input parameters")

class CrtPollInput(BaseModel):
    project_id: str = Field(..., description="CRT Project Id")
    job_id: str = Field(..., description="CRT Test Job Id")
    build_id: str = Field(..., description="Build Id returned when the job was triggered")

class CrtResultsInput(BaseModel):
    project_id: str = Field(..., description="CRT Project Id")
    job_id: str = Field(..., description="CRT Test Job Id")
    build_id: str = Field(..., description="Build Id to retrieve results for")

class CrtListJobsInput(BaseModel):
    project_id: str = Field(..., description="CRT Project Id")

class StartDialogueInput(BaseModel):
    """Input for creating a new Copado AI dialogue."""
    agent_id: str = Field(
        "knowledge",
        description="Agent to chat with: 'plan', 'build', 'test', 'release', 'operate', or 'knowledge' (default)"
    )
    name: Optional[str] = Field(
        None,
        description="Dialogue name (max 100 chars). Auto-generated if omitted."
    )
    workspace_id: Optional[str] = Field(
        None,
        description="Workspace UUID. Uses default from config if omitted."
    )

class SendMessageInput(BaseModel):
    """Input for sending a message/prompt to a Copado AI dialogue."""
    dialogue_id: str = Field(..., description="Dialogue UUID from copado_start_dialogue")
    message: str = Field(..., description="The message/prompt to send to the AI agent")
    assistant_id: Optional[str] = Field(
        None,
        description="Override the agent for this message (e.g. 'build', 'test')"
    )

class GetDialogueHistoryInput(BaseModel):
    """Input for retrieving dialogue history with all messages."""
    dialogue_id: str = Field(..., description="Dialogue UUID to retrieve history for")

class ListDialoguesInput(BaseModel):
    """Input for listing user's dialogues."""
    workspace_id: Optional[str] = Field(
        None,
        description="Filter by workspace UUID. Lists all if omitted."
    )

class DeleteDialogueInput(BaseModel):
    """Input for deleting a dialogue."""
    dialogue_id: str = Field(..., description="Dialogue UUID to delete")

class ListWorkspacesInput(BaseModel):
    """Input for listing workspaces. No parameters needed — uses org from config."""
    pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SURFACE 1 — Copado Multicloud Webhooks (CI/CD)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WEBHOOK_PATH = "/json/v1/webhook/mcwebhook"


@mcp.tool()
async def copado_commit(input: CommitInput) -> dict:
    """Commit metadata from a Copado User Story.

    POST /json/v1/webhook/mcwebhook/commit
    """
    _log("copado_commit", input.model_dump())
    return await _webhook_request("POST", f"{WEBHOOK_PATH}/commit", body={
        "payload": {
            "userStoryId": input.user_story_id,
            "message": input.message,
            "baseBranch": input.base_branch,
            "executeCommit": input.execute_commit,
            "recreateFeatureBranch": input.recreate_feature_branch,
            "changes": [],
        }
    })


@mcp.tool()
async def copado_promote(input: PromoteInput) -> dict:
    """Promote User Stories to the next pipeline environment.

    POST /json/v1/webhook/mcwebhook/promotion
    Set deployment_dry_run=True for validation-only.
    """
    _log("copado_promote", input.model_dump())
    return await _webhook_request("POST", f"{WEBHOOK_PATH}/promotion", body={
        "payload": {
            "userStoryIds": input.user_story_ids,
            "projectId": COPADO_PROJECT_ID,
            "sourceEnvironmentId": COPADO_SOURCE_ENV_ID,
            "executePromotion": True,
            "executeDeployment": input.execute_deployment,
            "deploymentDryRun": input.deployment_dry_run,
            "isBackPromotion": input.is_back_promotion,
            "otherInformation": "",
            "actionCallback": "",
            "promotionId": "",
        }
    })


@mcp.tool()
async def copado_validate(input: ValidateInput) -> dict:
    """Run a validation-only deployment (no merge, no side-effects).

    POST /json/v1/webhook/mcwebhook/promotion with deploymentDryRun=True.
    """
    _log("copado_validate", input.model_dump())
    return await _webhook_request("POST", f"{WEBHOOK_PATH}/promotion", body={
        "payload": {
            "userStoryIds": input.user_story_ids,
            "projectId": COPADO_PROJECT_ID,
            "sourceEnvironmentId": COPADO_SOURCE_ENV_ID,
            "executePromotion": True,
            "executeDeployment": True,
            "deploymentDryRun": True,
            "isBackPromotion": False,
            "otherInformation": "",
            "actionCallback": "",
            "promotionId": "",
        }
    })


@mcp.tool()
async def copado_deploy(input: DeployInput) -> dict:
    """Deploy a promotion to the destination environment.

    POST /json/v1/webhook/mcwebhook/promotiondeployment
    Requires a promotionId from a prior copado_promote response.
    """
    _log("copado_deploy", input.model_dump())
    return await _webhook_request("POST", f"{WEBHOOK_PATH}/promotiondeployment", body={
        "payload": {
            "promotionId": input.promotion_id,
            "executeDeployment": input.execute_deployment,
            "deploymentDryRun": input.deployment_dry_run,
            "otherInformation": "",
            "actionCallback": "",
        }
    })


@mcp.tool()
async def copado_check_status(input: CheckStatusInput) -> dict:
    """Check the status of a running Copado job execution.

    POST /json/v1/webhook/mcwebhook/checkStatusAction
    """
    _log("copado_check_status", input.model_dump())
    return await _webhook_request("POST", f"{WEBHOOK_PATH}/checkStatusAction", body={
        "payload": {
            "resultId": input.result_id,
        }
    })


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SURFACE 2 — Agentia Testing (CRT) Open API
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@mcp.tool()
async def crt_trigger_test_job(input: CrtTriggerInput) -> dict:
    """Trigger a CRT test job execution.

    POST /pace/v4/projects/{projectId}/jobs/{jobId}/builds
    """
    _log("crt_trigger_test_job", input.model_dump())
    body: dict[str, Any] = {}
    if input.input_parameters:
        body["inputParameters"] = input.input_parameters
    return await _crt_request(
        "POST",
        f"/pace/v4/projects/{input.project_id}/jobs/{input.job_id}/builds",
        body=body,
    )


@mcp.tool()
async def crt_poll_execution_status(input: CrtPollInput) -> dict:
    """Poll a running CRT build's execution status.

    GET /pace/v4/projects/{projectId}/jobs/{jobId}/builds/{buildId}
    """
    _log("crt_poll_execution_status", input.model_dump())
    return await _crt_request(
        "GET",
        f"/pace/v4/projects/{input.project_id}/jobs/{input.job_id}/builds/{input.build_id}",
    )

@mcp.tool()
async def crt_retrieve_test_results(input: CrtResultsInput) -> dict:
    """Retrieve detailed test results for a completed CRT build.

    GET /pace/v4/projects/{projectId}/jobs/{jobId}/builds/{buildId}/results
    """
    _log("crt_retrieve_test_results", input.model_dump())
    return await _crt_request(
        "GET",
        f"/pace/v4/projects/{input.project_id}/jobs/{input.job_id}/builds/{input.build_id}/results",
    )


@mcp.tool()
async def crt_list_test_jobs(input: CrtListJobsInput) -> dict:
    """List all available CRT test jobs in a project.

    GET /pace/v4/projects/{projectId}/jobs
    """
    _log("crt_list_test_jobs", input.model_dump())
    return await _crt_request(
        "GET",
        f"/pace/v4/projects/{input.project_id}/jobs",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SURFACE 3 — Agentia AI Context Hub (Dialogue API)
# Real endpoints from Copado AI Platform OpenAPI spec
# Base: https://copadogpt-api.robotic.copado.com
# Auth: X-Authorization header with Personal Access Key
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@mcp.tool()
async def copado_start_dialogue(input: StartDialogueInput) -> dict:
    """Start a new dialogue with a Copado specialist agent.

    POST /organizations/{org_id}/dialogues

    Agents: plan (sprint planning), build (code), test (QA),
    release (deployments), operate (post-release), knowledge (default expert).
    """
    _log("copado_start_dialogue", input.model_dump())

    if not COPADO_ORG_ID:
        return {"error": "CONFIG_MISSING", "message": "COPADO_ORG_ID not set in .env"}

    # Resolve agent_id → assistantId
    assistant_id = AGENT_TO_ASSISTANT.get(input.agent_id)
    if not assistant_id:
        return {
            "error": "INVALID_AGENT_ID",
            "message": (
                f"Agent '{input.agent_id}' is not valid. "
                f"Must be one of: {', '.join(sorted(AGENT_TO_ASSISTANT.keys()))}"
            ),
        }

    # Resolve workspace — use input, fall back to .env default
    workspace_id = input.workspace_id or COPADO_DEFAULT_WORKSPACE_ID

    # Build request body matching DialogueCreate schema
    dialogue_name = input.name or f"{input.agent_id}-{_uid()}"
    body: dict[str, Any] = {
        "name": dialogue_name,
        "assistantId": assistant_id,
    }
    if workspace_id:
        body["workspaceId"] = workspace_id

    return await _dialogue_request(
        "POST", _org_path("dialogues"), body=body
    )


@mcp.tool()
async def copado_send_message(input: SendMessageInput) -> dict:
    """Send a message to an active Copado AI dialogue and receive a response.

    POST /organizations/{org_id}/dialogues/{dialogue_id}/messages

    The response is streamed (SSE) and automatically assembled into a single result.
    Optionally override the agent with assistant_id (e.g. 'build', 'test').
    """
    _log("copado_send_message", input.model_dump())

    if not COPADO_ORG_ID:
        return {"error": "CONFIG_MISSING", "message": "COPADO_ORG_ID not set in .env"}

    # Build request body matching MessageCreate schema
    body: dict[str, Any] = {
        "request_id": str(uuid.uuid4()),  # required UUID, auto-generated
        "prompt": input.message,
    }
    if input.assistant_id:
        resolved = AGENT_TO_ASSISTANT.get(input.assistant_id, input.assistant_id)
        body["assistantId"] = resolved

    return await _dialogue_stream_request(
        "POST",
        _org_path(f"dialogues/{input.dialogue_id}/messages"),
        body=body,
    )


@mcp.tool()
async def copado_get_dialogue_history(input: GetDialogueHistoryInput) -> dict:
    """Retrieve the full message history for a Copado AI dialogue.

    GET /organizations/{org_id}/dialogues/{dialogue_id}

    Returns dialogue metadata plus the complete messages array.
    """
    _log("copado_get_dialogue_history", input.model_dump())

    if not COPADO_ORG_ID:
        return {"error": "CONFIG_MISSING", "message": "COPADO_ORG_ID not set in .env"}

    return await _dialogue_request(
        "GET", _org_path(f"dialogues/{input.dialogue_id}")
    )


@mcp.tool()
async def copado_list_workspaces(input: ListWorkspacesInput) -> dict:
    """List available workspaces for the Copado organization.

    GET /organizations/{org_id}/workspaces

    Uses the organization ID from .env configuration.
    """
    _log("copado_list_workspaces", {})

    if not COPADO_ORG_ID:
        return {"error": "CONFIG_MISSING", "message": "COPADO_ORG_ID not set in .env"}

    resp = await _dialogue_request("GET", _org_path("workspaces"))
    # Wrap list response in a dict for MCP compatibility
    if isinstance(resp, list):
        return {"workspaces": resp, "count": len(resp)}
    return resp


@mcp.tool()
async def copado_list_dialogues(input: ListDialoguesInput) -> dict:
    """List the current user's dialogues in the Copado organization.

    GET /organizations/{org_id}/dialogues

    Optionally filter by workspace_id.
    """
    _log("copado_list_dialogues", input.model_dump())

    if not COPADO_ORG_ID:
        return {"error": "CONFIG_MISSING", "message": "COPADO_ORG_ID not set in .env"}

    params: dict[str, str] | None = None
    if input.workspace_id:
        params = {"workspace_id": input.workspace_id}

    resp = await _dialogue_request(
        "GET", _org_path("dialogues"), params=params
    )
    # Wrap list response in a dict for MCP compatibility
    if isinstance(resp, list):
        return {"dialogues": resp, "count": len(resp)}
    return resp


@mcp.tool()
async def copado_delete_dialogue(input: DeleteDialogueInput) -> dict:
    """Delete a Copado AI dialogue and all its documents.

    DELETE /organizations/{org_id}/dialogues/{dialogue_id}

    Only the dialogue creator can delete it.
    """
    _log("copado_delete_dialogue", input.model_dump())

    if not COPADO_ORG_ID:
        return {"error": "CONFIG_MISSING", "message": "COPADO_ORG_ID not set in .env"}

    return await _dialogue_delete_request(
        _org_path(f"dialogues/{input.dialogue_id}")
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Entrypoint
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    _log("STARTUP", {
        "webhook_base_url": COPADO_WEBHOOK_BASE_URL,
        "webhook_key_set": bool(COPADO_WEBHOOK_KEY),
        "project_id": COPADO_PROJECT_ID,
        "source_env_id": COPADO_SOURCE_ENV_ID,
        "dialogue_base_url": COPADO_DIALOGUE_BASE_URL,
        "org_id": COPADO_ORG_ID,
        "default_workspace_id": COPADO_DEFAULT_WORKSPACE_ID,
        "api_token_set": bool(COPADO_API_TOKEN),
        "crt_base_url": COPADO_CRT_BASE_URL or "(not set)",
    })
    mcp.run()

