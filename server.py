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
# Global config
# ──────────────────────────────────────────────
COPADO_BASE_URL = os.getenv("COPADO_BASE_URL")
COPADO_TOKEN = os.getenv("COPADO_API_TOKEN")

if not COPADO_BASE_URL:
    raise RuntimeError(
        "CRITICAL ERROR: 'COPADO_BASE_URL' environment variable is not set. "
        "Please define it in your environment or local .env file."
    )

if not COPADO_TOKEN:
    raise RuntimeError(
        "CRITICAL ERROR: 'COPADO_API_TOKEN' environment variable is not set. "
        "Please define it in your environment or local .env file."
    )

COPADO_BASE_URL = COPADO_BASE_URL.rstrip("/")

VALID_AGENT_IDS = {"plan", "build", "test", "release", "operate"}

mcp = FastMCP(
    "Copado Native MCP Server",
    instructions=(
        "Native MCP integration for Copado CI/CD Actions REST API "
        "and Agentia Testing (CRT) Open API. Track C — CopadoCon Hackathon."
    ),
)

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _log(label: str, data: Any) -> None:
    """Emit structured debug info to stderr for real-time verification."""
    print(f"[COPADO-MCP] [{label}] {json.dumps(data, default=str)}", file=sys.stderr)


def _headers() -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if COPADO_TOKEN:
        headers["X-Authorization"] = COPADO_TOKEN
    return headers


def _uid() -> str:
    return str(uuid.uuid4())[:8]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def _request(
    method: str,
    path: str,
    *,
    body: dict | None = None,
    params: dict | None = None,
) -> dict:
    """Central HTTP dispatcher making downstream network calls."""
    url = f"{COPADO_BASE_URL}{path}"
    _log("HTTP_REQUEST", {"method": method, "url": url, "body": body, "params": params})

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.request(
            method, url, headers=_headers(), json=body, params=params
        )
        resp.raise_for_status()
        return resp.json()



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PYDANTIC INPUT MODELS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CommitInput(BaseModel):
    user_story_id: str = Field(..., description="Copado User Story Id (e.g. 'US-1001')")
    message: str = Field(..., description="Commit message describing the change")
    branch: str = Field("main", description="Target branch name")

class PromoteInput(BaseModel):
    user_story_id: str = Field(..., description="User Story Id to promote")
    target_environment: str = Field(..., description="Target environment name (e.g. 'INT', 'UAT', 'PROD')")

class ValidateInput(BaseModel):
    user_story_id: str = Field(..., description="User Story Id to validate")
    target_environment: str = Field(..., description="Environment to validate against")

class DeployInput(BaseModel):
    user_story_id: str = Field(..., description="User Story Id to deploy")
    target_environment: str = Field(..., description="Destination environment (e.g. 'INT', 'UAT', 'PROD')")
    confirm_production: bool = Field(
        False,
        description=(
            "REQUIRED safety flag — must be explicitly set to True when "
            "target_environment is 'PROD'. Deployment to production will be "
            "REJECTED if this flag is not True."
        ),
    )

class ListUserStoriesInput(BaseModel):
    status_filter: Optional[str] = Field(None, description="Filter by status: 'In Progress', 'Ready to Promote', 'Completed'")
    environment: Optional[str] = Field(None, description="Filter by environment name")

class GetUserStoryInput(BaseModel):
    user_story_id: str = Field(..., description="User Story Id to retrieve")

class PollJobInput(BaseModel):
    job_execution_id: str = Field(..., description="Job Execution Id returned by a prior action")

class CrtTriggerInput(BaseModel):
    project_id: str = Field(..., description="CRT Project Id")
    job_id: str = Field(..., description="CRT Test Job Id to trigger")
    input_parameters: Optional[dict] = Field(None, description="Optional key-value input parameters for the test run")

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

class AutonomousDeliveryInput(BaseModel):
    user_story_id: str = Field(..., description="User Story Id to run the full delivery loop on")
    target_environment: str = Field("INT", description="Final target environment")
    run_tests: bool = Field(True, description="Whether to trigger CRT tests after promotion")
    crt_project_id: Optional[str] = Field(None, description="CRT project Id (required if run_tests is True)")
    crt_job_id: Optional[str] = Field(None, description="CRT job Id (required if run_tests is True)")
    confirm_production: bool = Field(
        False,
        description="Must be True to allow deployment to PROD"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SURFACE 1 — Copado CI/CD Actions REST API
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@mcp.tool()
async def copado_commit(input: CommitInput) -> dict:
    """Commit metadata from a Copado User Story.

    Triggers POST /actions/commit to snapshot the metadata
    components attached to the given user story.
    """
    _log("copado_commit", input.model_dump())
    return await _request("POST", "/actions/commit", body={
        "userStoryId": input.user_story_id,
        "message": input.message,
        "branch": input.branch,
    })


@mcp.tool()
async def copado_promote(input: PromoteInput) -> dict:
    """Promote a User Story to the next pipeline environment.

    Triggers POST /actions/promote.
    """
    _log("copado_promote", input.model_dump())
    return await _request("POST", "/actions/promote", body={
        "userStoryId": input.user_story_id,
        "targetEnvironment": input.target_environment,
    })


@mcp.tool()
async def copado_validate(input: ValidateInput) -> dict:
    """Run a validation-only deployment (no merge, no side-effects).

    Triggers POST /actions/validate.
    """
    _log("copado_validate", input.model_dump())
    return await _request("POST", "/actions/validate", body={
        "userStoryId": input.user_story_id,
        "targetEnvironment": input.target_environment,
    })


@mcp.tool()
async def copado_deploy(input: DeployInput) -> dict:
    """Execute a deployment to a target environment.

    ⚠️  GUARDRAIL: Deploying to 'PROD' requires confirm_production=True.
    The server will REJECT the request otherwise.
    """
    _log("copado_deploy", input.model_dump())

    if input.target_environment.upper() == "PROD" and not input.confirm_production:
        return {
            "error": "PRODUCTION_GUARDRAIL",
            "message": (
                "🚫 Deployment to PROD blocked. You must set "
                "'confirm_production' to True to acknowledge this "
                "production deployment. This is a safety guardrail."
            ),
        }

    return await _request("POST", "/actions/deploy", body={
        "userStoryId": input.user_story_id,
        "targetEnvironment": input.target_environment,
    })


@mcp.tool()
async def copado_list_user_stories(input: ListUserStoriesInput) -> dict:
    """List and filter Copado User Stories.

    Calls GET /user-stories with optional status and environment filters.
    """
    _log("copado_list_user_stories", input.model_dump())
    params: dict[str, str] = {}
    if input.status_filter:
        params["status"] = input.status_filter
    if input.environment:
        params["environment"] = input.environment
    return await _request("GET", "/user-stories", params=params or None)


@mcp.tool()
async def copado_get_user_story_details(input: GetUserStoryInput) -> dict:
    """Get full details and metadata scope for a single User Story.

    Calls GET /user-stories/{id}.
    """
    _log("copado_get_user_story_details", input.model_dump())
    return await _request("GET", f"/user-stories/{input.user_story_id}")


@mcp.tool()
async def copado_list_environments() -> dict:
    """List all pipeline environments.

    Calls GET /environments. No parameters required.
    """
    _log("copado_list_environments", {})
    return await _request("GET", "/environments")


@mcp.tool()
async def copado_poll_job_execution(input: PollJobInput) -> dict:
    """Poll a Job Execution's status, steps, and logs.

    Calls GET /job-executions/{id}. Use this to track any async
    action (commit, promote, deploy, validate).
    """
    _log("copado_poll_job_execution", input.model_dump())
    return await _request("GET", f"/job-executions/{input.job_execution_id}")


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
    return await _request(
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
    return await _request(
        "GET",
        f"/pace/v4/projects/{input.project_id}/jobs/{input.job_id}/builds/{input.build_id}",
    )


@mcp.tool()
async def crt_retrieve_test_results(input: CrtResultsInput) -> dict:
    """Retrieve detailed test results for a completed CRT build.

    GET /pace/v4/projects/{projectId}/jobs/{jobId}/builds/{buildId}/results
    """
    _log("crt_retrieve_test_results", input.model_dump())
    return await _request(
        "GET",
        f"/pace/v4/projects/{input.project_id}/jobs/{input.job_id}/builds/{input.build_id}/results",
    )


@mcp.tool()
async def crt_list_test_jobs(input: CrtListJobsInput) -> dict:
    """List all available CRT test jobs in a project.

    GET /pace/v4/projects/{projectId}/jobs
    """
    _log("crt_list_test_jobs", input.model_dump())
    return await _request(
        "GET",
        f"/pace/v4/projects/{input.project_id}/jobs",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MACRO TOOL — Autonomous Delivery Loop
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@mcp.tool()
async def copado_autonomous_delivery_loop(input: AutonomousDeliveryInput) -> dict:
    """Run a full autonomous delivery pipeline for a User Story.

    Orchestrates: commit → validate → promote → deploy → (optional) CRT tests.

    ⚠️  GUARDRAIL: Production deployments require confirm_production=True.
    ⚠️  NAMING NOTE: This tool is intentionally NOT named 'orchestrate_delivery'
         to comply with Track C rules (no reference to Copado Orchestrate Agent).
    """
    _log("copado_autonomous_delivery_loop", input.model_dump())
    results: dict[str, Any] = {"userStoryId": input.user_story_id, "steps": []}

    # ── Production guardrail ──
    if input.target_environment.upper() == "PROD" and not input.confirm_production:
        return {
            "error": "PRODUCTION_GUARDRAIL",
            "message": (
                "🚫 Autonomous delivery to PROD blocked. "
                "Set confirm_production=True to proceed."
            ),
        }

    # Step 1 — Commit
    _log("LOOP_STEP", "1/5 Commit")
    commit = await _request("POST", "/actions/commit", body={
        "userStoryId": input.user_story_id,
        "message": f"Auto-commit for delivery loop [{_uid()}]",
        "branch": "main",
    })
    results["steps"].append({"step": "commit", "result": commit})

    # Step 2 — Validate
    _log("LOOP_STEP", "2/5 Validate")
    validate = await _request("POST", "/actions/validate", body={
        "userStoryId": input.user_story_id,
        "targetEnvironment": input.target_environment,
    })
    results["steps"].append({"step": "validate", "result": validate})
    if validate.get("status") == "Failed":
        results["outcome"] = "ABORTED — validation failed"
        return results

    # Step 3 — Promote
    _log("LOOP_STEP", "3/5 Promote")
    promote = await _request("POST", "/actions/promote", body={
        "userStoryId": input.user_story_id,
        "targetEnvironment": input.target_environment,
    })
    results["steps"].append({"step": "promote", "result": promote})

    # Step 4 — Deploy
    _log("LOOP_STEP", "4/5 Deploy")
    deploy = await _request("POST", "/actions/deploy", body={
        "userStoryId": input.user_story_id,
        "targetEnvironment": input.target_environment,
    })
    results["steps"].append({"step": "deploy", "result": deploy})

    # Step 5 — CRT Tests (optional)
    if input.run_tests and input.crt_project_id and input.crt_job_id:
        _log("LOOP_STEP", "5/5 CRT Test")
        test_trigger = await _request(
            "POST",
            f"/pace/v4/projects/{input.crt_project_id}/jobs/{input.crt_job_id}/builds",
            body={},
        )
        results["steps"].append({"step": "crt_test_trigger", "result": test_trigger})

        build_id = test_trigger.get("buildId", "unknown")
        test_status = await _request(
            "GET",
            f"/pace/v4/projects/{input.crt_project_id}/jobs/{input.crt_job_id}/builds/{build_id}",
        )
        results["steps"].append({"step": "crt_test_status", "result": test_status})

        test_results = await _request(
            "GET",
            f"/pace/v4/projects/{input.crt_project_id}/jobs/{input.crt_job_id}/builds/{build_id}/results",
        )
        results["steps"].append({"step": "crt_test_results", "result": test_results})
    else:
        results["steps"].append({"step": "crt_tests", "result": "Skipped (not configured)"})

    results["outcome"] = "Delivery loop completed successfully"
    results["timestamp"] = _now()
    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Entrypoint
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    _log("STARTUP", {
        "base_url": COPADO_BASE_URL,
        "token_set": bool(COPADO_TOKEN),
    })
    mcp.run()
