import sys
import uuid
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv

# Load configuration from environment file (.env)
load_dotenv()

EXPECTED_TOKEN = os.getenv("COPADO_API_TOKEN")
if not EXPECTED_TOKEN:
    raise RuntimeError(
        "CRITICAL ERROR: 'COPADO_API_TOKEN' environment variable is not set. "
        "Please define it in your environment or local .env file so the simulator can validate requests."
    )

app = FastAPI(
    title="Copado & Agentia Testing (CRT) API Simulator",
    description="Mock API server simulating Copado DevOps Actions & Robotic Testing endpoints for Track C testing.",
)

def _uid() -> str:
    return str(uuid.uuid4())[:8]

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _log(method: str, path: str, body: Any = None, query: Any = None, headers: Dict[str, str] = None):
    print(f"\n[SIMULATOR] === INCOMING REQUEST ===", file=sys.stderr)
    print(f"[SIMULATOR] {method} {path}", file=sys.stderr)
    if headers:
        auth = headers.get("x-authorization") or headers.get("authorization")
        print(f"[SIMULATOR] Auth: {auth}", file=sys.stderr)
    if query:
        print(f"[SIMULATOR] Query Params: {query}", file=sys.stderr)
    if body:
        print(f"[SIMULATOR] Body: {body}", file=sys.stderr)
    print(f"[SIMULATOR] ==========================\n", file=sys.stderr)

# ──────────────────────────────────────────────
# Pydantic Schemas for validation
# ──────────────────────────────────────────────
class CommitPayload(BaseModel):
    userStoryId: str
    message: str
    branch: Optional[str] = "main"

class PromotePayload(BaseModel):
    userStoryId: str
    targetEnvironment: str

class ValidatePayload(BaseModel):
    userStoryId: str
    targetEnvironment: str

class DeployPayload(BaseModel):
    userStoryId: str
    targetEnvironment: str

class BuildPayload(BaseModel):
    inputParameters: Optional[Dict[str, Any]] = None

# ──────────────────────────────────────────────
# Middleware to verify auth header
# ──────────────────────────────────────────────
@app.middleware("http")
async def log_and_authorize_requests(request: Request, call_next):
    # Retrieve query params and body safely
    query_params = dict(request.query_params)
    body = None
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            body = await request.json()
        except Exception:
            pass
    
    headers = {k.lower(): v for k, v in request.headers.items()}
    _log(request.method, request.url.path, body, query_params, headers)
    
    # Exclude openapi/docs paths from token check
    if request.url.path in ("/docs", "/redoc", "/openapi.json"):
        return await call_next(request)

    # Check X-Authorization
    x_auth = headers.get("x-authorization")
    if not x_auth:
        from fastapi.responses import JSONResponse
        print("[SIMULATOR] [ERROR] Blocked request: X-Authorization header missing!", file=sys.stderr)
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized: X-Authorization header is missing."}
        )
        
    if x_auth != EXPECTED_TOKEN:
        from fastapi.responses import JSONResponse
        print(f"[SIMULATOR] [ERROR] Blocked request: Invalid token '{x_auth}' vs expected '{EXPECTED_TOKEN}'", file=sys.stderr)
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized: Invalid X-Authorization token."}
        )
        
    response = await call_next(request)
    return response

# ──────────────────────────────────────────────
# Surface 1: Copado Actions REST API
# ──────────────────────────────────────────────

@app.post("/actions/commit")
async def commit(payload: CommitPayload):
    return {
        "jobExecutionId": f"JE-{_uid()}",
        "status": "Completed Successfully",
        "userStoryId": payload.userStoryId,
        "commitMessage": payload.message,
        "timestamp": _now(),
    }

@app.post("/actions/promote")
async def promote(payload: PromotePayload):
    return {
        "jobExecutionId": f"JE-{_uid()}",
        "status": "Completed Successfully",
        "userStoryId": payload.userStoryId,
        "targetEnvironment": payload.targetEnvironment,
        "timestamp": _now(),
    }

@app.post("/actions/validate")
async def validate(payload: ValidatePayload):
    return {
        "jobExecutionId": f"JE-{_uid()}",
        "status": "Completed Successfully",
        "validationResult": "No Errors",
        "componentsValidated": 12,
        "timestamp": _now(),
    }

@app.post("/actions/deploy")
async def deploy(payload: DeployPayload):
    return {
        "jobExecutionId": f"JE-{_uid()}",
        "status": "Completed Successfully",
        "targetEnvironment": payload.targetEnvironment,
        "componentsDeployed": 8,
        "testsPassed": 24,
        "testsFailed": 0,
        "timestamp": _now(),
    }

@app.get("/user-stories")
async def list_user_stories(status: Optional[str] = None, environment: Optional[str] = None):
    return {
        "totalSize": 3,
        "records": [
            {"id": "US-1001", "title": "Add Lightning Web Component", "status": "In Progress", "environment": "DEV1", "owner": "sgupta"},
            {"id": "US-1002", "title": "Fix Apex trigger bulk handler", "status": "Ready to Promote", "environment": "DEV1", "owner": "jdoe"},
            {"id": "US-1003", "title": "Update validation rules", "status": "Completed", "environment": "INT", "owner": "asmith"},
        ],
    }

@app.get("/user-stories/{user_story_id}")
async def get_user_story(user_story_id: str):
    return {
        "id": user_story_id,
        "title": "Add Lightning Web Component",
        "status": "In Progress",
        "environment": "DEV1",
        "owner": "sgupta",
        "metadata": [
            {"componentName": "myComponent", "type": "LightningComponentBundle", "action": "Add"},
            {"componentName": "MyController", "type": "ApexClass", "action": "Modify"},
        ],
        "pipeline": "Main_Pipeline",
        "createdDate": "2026-05-20T10:00:00Z",
        "lastModifiedDate": _now(),
    }

@app.get("/job-executions/{job_execution_id}")
async def get_job_execution(job_execution_id: str):
    return {
        "id": job_execution_id,
        "status": "Completed Successfully",
        "startTime": "2026-05-30T03:50:00Z",
        "endTime": _now(),
        "steps": [
            {"name": "Checkout", "status": "Completed Successfully", "duration": "2s"},
            {"name": "Compile", "status": "Completed Successfully", "duration": "8s"},
            {"name": "Run Tests", "status": "Completed Successfully", "duration": "14s"},
            {"name": "Deploy", "status": "Completed Successfully", "duration": "6s"},
        ],
        "logs": "All steps executed without errors.",
    }

@app.get("/environments")
async def list_environments():
    return {
        "environments": [
            {"id": "ENV-01", "name": "DEV1", "type": "Development", "org": "dev1@copado.com"},
            {"id": "ENV-02", "name": "INT", "type": "Integration", "org": "int@copado.com"},
            {"id": "ENV-03", "name": "UAT", "type": "UAT", "org": "uat@copado.com"},
            {"id": "ENV-04", "name": "PROD", "type": "Production", "org": "prod@copado.com"},
        ]
    }

# ──────────────────────────────────────────────
# Surface 2: Agentia Testing Instance (CRT)
# ──────────────────────────────────────────────

@app.post("/pace/v4/projects/{project_id}/jobs/{job_id}/builds")
async def trigger_build(project_id: str, job_id: str, payload: Optional[BuildPayload] = None):
    return {
        "buildId": f"BLD-{_uid()}",
        "jobId": job_id,
        "status": "In Progress",
        "triggeredAt": _now(),
    }

@app.get("/pace/v4/projects/{project_id}/jobs/{job_id}/builds/{build_id}")
async def get_build_status(project_id: str, job_id: str, build_id: str):
    return {
        "buildId": build_id,
        "status": "Completed Successfully",
        "startTime": "2026-05-30T03:55:00Z",
        "endTime": _now(),
        "progress": 100,
    }

@app.get("/pace/v4/projects/{project_id}/jobs/{job_id}/builds/{build_id}/results")
async def get_build_results(project_id: str, job_id: str, build_id: str):
    return {
        "totalTests": 42,
        "passed": 40,
        "failed": 1,
        "skipped": 1,
        "duration": "3m 12s",
        "results": [
            {"testName": "Login Flow", "status": "Passed", "duration": "12s"},
            {"testName": "Create Lead", "status": "Passed", "duration": "8s"},
            {"testName": "Bulk Import", "status": "Failed", "errorMessage": "Timeout after 30s", "duration": "30s"},
            {"testName": "Report Export", "status": "Skipped", "duration": "0s"},
        ],
    }

@app.get("/pace/v4/projects/{project_id}/jobs")
async def list_jobs(project_id: str):
    return {
        "jobs": [
            {"jobId": "JOB-101", "name": "Smoke Suite", "type": "Regression", "lastRun": "2026-05-29T18:00:00Z", "status": "Passed"},
            {"jobId": "JOB-102", "name": "Full Regression", "type": "Regression", "lastRun": "2026-05-28T22:00:00Z", "status": "Passed"},
            {"jobId": "JOB-103", "name": "Performance Bench", "type": "Performance", "lastRun": "2026-05-27T12:00:00Z", "status": "Failed"},
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting simulator server on http://127.0.0.1:8000", file=sys.stderr)
    uvicorn.run(app, host="127.0.0.1", port=8000)
