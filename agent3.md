# 🤖 Surface 3 — Copado AI Platform Dialogue API

> **MCP Server:** `server.py` (Surface 3 section)
> **Base URL:** `https://copadogpt-api.robotic.copado.com`
> **Auth:** `X-Authorization: <Personal-Access-Key>`
> **Organization ID:** `49240`
> **Default Workspace:** `16cbafef-b504-4536-b8ae-ab66cd41a5bd`

---

## 📋 Table of Contents

1. [Configuration (.env)](#configuration-env)
2. [Authentication](#authentication)
3. [Agent → Assistant Mapping](#agent--assistant-mapping)
4. [MCP Tool Reference](#mcp-tool-reference)
   - [copado_start_dialogue](#1--copado_start_dialogue)
   - [copado_send_message](#2--copado_send_message)
   - [copado_get_dialogue_history](#3--copado_get_dialogue_history)
   - [copado_list_workspaces](#4--copado_list_workspaces)
   - [copado_list_dialogues](#5--copado_list_dialogues)
   - [copado_delete_dialogue](#6--copado_delete_dialogue)
5. [Internal Helpers](#internal-helpers)
6. [Error Handling](#error-handling)

---

## Configuration (.env)

| Variable | Value | Description |
|----------|-------|-------------|
| `COPADO_DIALOGUE_BASE_URL` | `https://copadogpt-api.robotic.copado.com` | API base URL (US region) |
| `COPADO_API_TOKEN` | `wLkWFdLY...v9WM` | Personal Access Key (PAK) |
| `COPADO_ORG_ID` | `49240` | Organization ID |
| `COPADO_DEFAULT_WORKSPACE_ID` | `16cbafef-b504-4536-b8ae-ab66cd41a5bd` | Default workspace UUID |
| `COPADO_USER_ID` | `3313712` | User ID |
| `COPADO_MEMBER_ID` | `39aaf46d-032c-4a0c-ae36-4d95a1b7f68d` | Workspace member UUID |
| `COPADO_PLATFORM_BASE_URL` | `https://platform.robotic.copado.com` | Platform URL (for user endpoints) |

### Regional Base URLs

| Region | API Base URL |
|--------|-------------|
| 🇺🇸 US | `https://copadogpt-api.robotic.copado.com` |
| 🇪🇺 EU | `https://copadogpt-api.eu-robotic.copado.com` |
| 🇦🇺 AU | `https://copadogpt-api.au-robotic.copado.com` |
| 🇸🇬 SG | `https://copadogpt-api.sg-robotic.copado.com` |

---

## Authentication

Every request includes the `X-Authorization` header with the Personal Access Key:

```
X-Authorization: wLkWFdLYDrNrSXhVgPVNJZuN0X92qpNGbH2tgHBqSjt2yRZkv9WM
Content-Type: application/json
Accept: application/json
```

Unauthorized requests return **HTTP 401**.

---

## Agent → Assistant Mapping

The MCP tools accept a user-friendly `agent_id` which maps to the Copado `assistantId`:

| Agent Name | `assistantId` | When to Use |
|------------|---------------|-------------|
| `plan` | `plan` | Sprint planning, user stories, backlog management, conflict/duplicate checking |
| `build` | `build` | Code writing, review, test coverage, troubleshooting, Apex development |
| `test` | `test` | Test script generation, QA automation, test execution monitoring |
| `release` | `release` | Deployment coordination, version control, quality gates, release documentation |
| `operate` | `operate` | Post-release troubleshooting, change management, process optimization |
| `knowledge` | `knowledge` | **Default** — General Copado/Salesforce technical support, data analysis |

---

## MCP Tool Reference

---

### 1. 🔵 `copado_start_dialogue`

**Create a new dialogue (chat) with a Copado AI agent.**

#### HTTP Endpoint

```
POST /organizations/{organization_id}/dialogues
```

**Full URL:** `https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues`

#### MCP Tool Input (Pydantic Model: `StartDialogueInput`)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `agent_id` | `string` | No | `"knowledge"` | Agent to chat with: `plan`, `build`, `test`, `release`, `operate`, or `knowledge` |
| `name` | `string \| null` | No | Auto-generated | Dialogue name (max 100 chars). Auto-generates as `{agent_id}-{short_uuid}` if omitted |
| `workspace_id` | `string \| null` | No | From `.env` | Workspace UUID. Falls back to `COPADO_DEFAULT_WORKSPACE_ID` |

#### Request Body (sent to Copado API)

Schema: **`DialogueCreate`**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ Yes | Dialogue name (1–100 chars) |
| `workspaceId` | `string (uuid)` | No | Workspace to associate the dialogue with |
| `assistantId` | `string` | No | AI assistant ID (default: `"knowledge"`) |

#### Example Request JSON

```json
{
  "name": "build-a1b2c3d4",
  "workspaceId": "16cbafef-b504-4536-b8ae-ab66cd41a5bd",
  "assistantId": "build"
}
```

#### Example curl

```bash
curl -X POST 'https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues' \
  -H 'X-Authorization: wLkWFdLYDrNrSXhVgPVNJZuN0X92qpNGbH2tgHBqSjt2yRZkv9WM' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "build-session-01",
    "workspaceId": "16cbafef-b504-4536-b8ae-ab66cd41a5bd",
    "assistantId": "build"
  }'
```

#### Response (200 OK)

Schema: **`DialogueResponse`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string (uuid)` | The created dialogue's UUID |
| `name` | `string` | Dialogue name |
| `workspace_id` | `string (uuid) \| null` | Associated workspace |
| `message_count` | `integer` | Number of messages (0 for new dialogue) |
| `document_count` | `integer \| null` | Number of attached documents |
| `assistant_id` | `string \| null` | The assigned assistant ID |
| `created_at` | `string (datetime)` | ISO 8601 creation timestamp |

```json
{
  "id": "9a3da4b3-42f4-4079-94be-04216ccad737",
  "name": "build-session-01",
  "workspace_id": "16cbafef-b504-4536-b8ae-ab66cd41a5bd",
  "message_count": 0,
  "document_count": null,
  "assistant_id": "build",
  "created_at": "2026-06-02T05:30:00.000000Z"
}
```

#### Errors

| Status | Reason |
|--------|--------|
| `401` | Invalid or missing API key |
| `422` | Validation error (e.g., name too long, invalid workspace UUID) |
| `CONFIG_MISSING` | `COPADO_ORG_ID` not set in `.env` (MCP-level error) |
| `INVALID_AGENT_ID` | Agent name not in the allowed list (MCP-level error) |

---

### 2. 🔵 `copado_send_message`

**Send a message/prompt to an active dialogue and receive a streamed AI response.**

#### HTTP Endpoint

```
POST /organizations/{organization_id}/dialogues/{dialogue_id}/messages
```

**Full URL:** `https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues/{dialogue_id}/messages`

> ⚡ **Streaming:** This endpoint returns a Server-Sent Events (SSE) stream. The MCP tool automatically collects all streamed chunks and assembles the full response text.

#### MCP Tool Input (Pydantic Model: `SendMessageInput`)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `dialogue_id` | `string` | ✅ Yes | — | Dialogue UUID from `copado_start_dialogue` |
| `message` | `string` | ✅ Yes | — | The message/prompt to send to the AI agent |
| `assistant_id` | `string \| null` | No | — | Override the agent for this specific message |

#### Request Body (sent to Copado API)

Schema: **`MessageCreate`**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `request_id` | `string (uuid)` | ✅ Yes | Unique request UUID — **auto-generated** by the tool |
| `prompt` | `string` | No | The user's message/prompt text |
| `assistantId` | `string \| null` | No | Override assistant for this message |
| `dev_context` | `ChatDevContext \| null` | No | Developer context (libraries, functions, buffers) |
| `system_prompt` | `string \| null` | No | Custom system prompt override |
| `integrations` | `object \| null` | No | Third-party integrations config |
| `tools` | `array[object] \| null` | No | Tool definitions for function calling |
| `tool_choice` | `string \| null` | No | Tool selection mode |
| `messages` | `array[object] \| null` | No | Additional context messages |

#### Example Request JSON

```json
{
  "request_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "prompt": "Write an Apex trigger for Account that prevents deletion of accounts with active opportunities",
  "assistantId": "build"
}
```

#### Example curl

```bash
curl -X POST 'https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues/9a3da4b3-42f4-4079-94be-04216ccad737/messages' \
  -H 'X-Authorization: wLkWFdLYDrNrSXhVgPVNJZuN0X92qpNGbH2tgHBqSjt2yRZkv9WM' \
  -H 'Content-Type: application/json' \
  -d '{
    "request_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "prompt": "Write an Apex trigger for Account that prevents deletion"
  }'
```

#### Response (assembled from SSE stream)

The MCP tool returns an assembled dict:

| Field | Type | Description |
|-------|------|-------------|
| `response` | `string` | The full AI-generated response text |
| `chunk_count` | `integer` | Number of SSE chunks received |
| `raw_chunks` | `array[object]` | First 5 raw SSE payloads for debugging |

```json
{
  "response": "Here's an Apex trigger that prevents deletion of Account records with active Opportunities:\n\n```apex\ntrigger PreventAccountDeletion on Account (before delete) {\n    Set<Id> accountIds = Trigger.oldMap.keySet();\n    List<Opportunity> activeOpps = [\n        SELECT AccountId FROM Opportunity \n        WHERE AccountId IN :accountIds AND IsClosed = false\n    ];\n    ...\n}\n```",
  "chunk_count": 42,
  "raw_chunks": [
    {"content": "Here's"},
    {"content": " an Apex"},
    {"content": " trigger"}
  ]
}
```

#### Errors

| Status | Reason |
|--------|--------|
| `401` | Invalid or missing API key |
| `404` | Dialogue not found |
| `422` | Validation error (missing `request_id`, invalid UUID) |

---

### 3. 🟢 `copado_get_dialogue_history`

**Retrieve the full message history for a dialogue.**

#### HTTP Endpoint

```
GET /organizations/{organization_id}/dialogues/{dialogue_id}
```

**Full URL:** `https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues/{dialogue_id}`

#### MCP Tool Input (Pydantic Model: `GetDialogueHistoryInput`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dialogue_id` | `string` | ✅ Yes | Dialogue UUID to retrieve history for |

#### Example curl

```bash
curl -s 'https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues/9a3da4b3-42f4-4079-94be-04216ccad737' \
  -H 'X-Authorization: wLkWFdLYDrNrSXhVgPVNJZuN0X92qpNGbH2tgHBqSjt2yRZkv9WM'
```

#### Response (200 OK)

Schema: **`DialogueWithMessagesResponse`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string (uuid)` | Dialogue UUID |
| `name` | `string` | Dialogue name |
| `workspace_id` | `string (uuid) \| null` | Associated workspace |
| `message_count` | `integer` | Total number of messages |
| `document_count` | `integer \| null` | Number of attached documents |
| `assistant_id` | `string \| null` | Assigned assistant ID |
| `created_at` | `string (datetime)` | ISO 8601 creation timestamp |
| `messages` | `array[ExtendedChatMessage]` | Full message history array |

**`ExtendedChatMessage` fields:**

| Field | Type | Description |
|-------|------|-------------|
| `role` | `string` | Message role: `"user"` or `"assistant"` |
| `content` | `string \| array \| null` | Message text (plain string or multi-modal content array) |
| `timestamp` | `string` | Message timestamp |
| `dialogueId` | `string (uuid)` | Parent dialogue UUID |

```json
{
  "id": "9a3da4b3-42f4-4079-94be-04216ccad737",
  "name": "build-session-01",
  "workspace_id": "16cbafef-b504-4536-b8ae-ab66cd41a5bd",
  "message_count": 2,
  "document_count": null,
  "assistant_id": "build",
  "created_at": "2026-06-02T05:30:00.000000Z",
  "messages": [
    {
      "role": "user",
      "content": "Write an Apex trigger for Account",
      "timestamp": "2026-06-02T05:31:00.000Z",
      "dialogueId": "9a3da4b3-42f4-4079-94be-04216ccad737"
    },
    {
      "role": "assistant",
      "content": "Here's an Apex trigger that...",
      "timestamp": "2026-06-02T05:31:05.000Z",
      "dialogueId": "9a3da4b3-42f4-4079-94be-04216ccad737"
    }
  ]
}
```

---

### 4. 🟢 `copado_list_workspaces`

**List all workspaces accessible by the current user.**

#### HTTP Endpoint

```
GET /organizations/{organization_id}/workspaces
```

**Full URL:** `https://copadogpt-api.robotic.copado.com/organizations/49240/workspaces`

#### MCP Tool Input (Pydantic Model: `ListWorkspacesInput`)

No input parameters required — `organization_id` is taken from `.env`.

#### Example curl

```bash
curl -s 'https://copadogpt-api.robotic.copado.com/organizations/49240/workspaces' \
  -H 'X-Authorization: wLkWFdLYDrNrSXhVgPVNJZuN0X92qpNGbH2tgHBqSjt2yRZkv9WM'
```

#### Response (200 OK — wrapped by MCP tool)

The raw API returns an `array[WorkspaceSummary]`. The MCP tool wraps it:

| Field | Type | Description |
|-------|------|-------------|
| `workspaces` | `array[WorkspaceSummary]` | List of workspace objects |
| `count` | `integer` | Number of workspaces |

**`WorkspaceSummary` fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string (uuid)` | Workspace UUID |
| `created_at` | `string (datetime)` | Creation timestamp |
| `modified_at` | `string (datetime)` | Last modified timestamp |
| `created_by` | `integer` | Creator's user ID |
| `modified_by` | `integer` | Last modifier's user ID |
| `name` | `string` | Workspace name |
| `description` | `string` | Workspace description |
| `organization_id` | `integer` | Parent org ID |
| `icon_url` | `string \| null` | Workspace icon (base64 data URL) |

```json
{
  "workspaces": [
    {
      "id": "16cbafef-b504-4536-b8ae-ab66cd41a5bd",
      "created_at": "2026-06-01T16:02:39.498207Z",
      "modified_at": "2026-06-01T16:02:39.528911Z",
      "created_by": 3313712,
      "modified_by": 3313712,
      "name": "My Workspace",
      "description": "For personal use to summarise meetings, draft emails, troubleshoot and more.",
      "organization_id": 49240,
      "icon_url": null
    }
  ],
  "count": 1
}
```

---

### 5. 🟢 `copado_list_dialogues`

**List all dialogues belonging to the current user.**

#### HTTP Endpoint

```
GET /organizations/{organization_id}/dialogues
```

**Full URL:** `https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues`

#### MCP Tool Input (Pydantic Model: `ListDialoguesInput`)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `workspace_id` | `string \| null` | No | — | Filter dialogues by workspace UUID |

#### Query Parameters (sent to API)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | No | Filter by workspace |

#### Example curl

```bash
# List all dialogues
curl -s 'https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues' \
  -H 'X-Authorization: wLkWFdLYDrNrSXhVgPVNJZuN0X92qpNGbH2tgHBqSjt2yRZkv9WM'

# Filter by workspace
curl -s 'https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues?workspace_id=16cbafef-b504-4536-b8ae-ab66cd41a5bd' \
  -H 'X-Authorization: wLkWFdLYDrNrSXhVgPVNJZuN0X92qpNGbH2tgHBqSjt2yRZkv9WM'
```

#### Response (200 OK — wrapped by MCP tool)

| Field | Type | Description |
|-------|------|-------------|
| `dialogues` | `array[DialogueResponse]` | List of dialogue objects |
| `count` | `integer` | Number of dialogues |

```json
{
  "dialogues": [
    {
      "id": "2566ac9c-5b60-4363-9751-5aa0b873bb3f",
      "name": "build-a1b2c3d4",
      "workspace_id": "16cbafef-b504-4536-b8ae-ab66cd41a5bd",
      "message_count": 4,
      "document_count": null,
      "assistant_id": "build",
      "created_at": "2026-06-01T18:00:00.000000Z"
    },
    {
      "id": "9a3da4b3-42f4-4079-94be-04216ccad737",
      "name": "test-session",
      "workspace_id": "16cbafef-b504-4536-b8ae-ab66cd41a5bd",
      "message_count": 2,
      "document_count": null,
      "assistant_id": "test",
      "created_at": "2026-06-02T05:30:00.000000Z"
    }
  ],
  "count": 2
}
```

---

### 6. 🔴 `copado_delete_dialogue`

**Delete a dialogue and all its documents.**

#### HTTP Endpoint

```
DELETE /organizations/{organization_id}/dialogues/{dialogue_id}
```

**Full URL:** `https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues/{dialogue_id}`

> ⚠️ **Only the dialogue creator can delete it.** All documents attached to the dialogue will also be deleted.

#### MCP Tool Input (Pydantic Model: `DeleteDialogueInput`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dialogue_id` | `string` | ✅ Yes | Dialogue UUID to delete |

#### Example curl

```bash
curl -X DELETE 'https://copadogpt-api.robotic.copado.com/organizations/49240/dialogues/9a3da4b3-42f4-4079-94be-04216ccad737' \
  -H 'X-Authorization: wLkWFdLYDrNrSXhVgPVNJZuN0X92qpNGbH2tgHBqSjt2yRZkv9WM'
```

#### Response (204 No Content — wrapped by MCP tool)

The API returns `204 No Content`. The MCP tool wraps it:

```json
{
  "status": "deleted",
  "detail": "Dialogue successfully deleted"
}
```

#### Errors

| Status | Reason |
|--------|--------|
| `401` | Invalid or missing API key |
| `403` | Not the dialogue creator |
| `404` | Dialogue not found |

---

## Internal Helpers

These are internal functions in `server.py` used by the Surface 3 tools:

| Helper | Purpose |
|--------|---------|
| `_dialogue_headers()` | Builds auth headers: `X-Authorization`, `Content-Type`, `Accept` |
| `_org_path(suffix)` | Constructs `/organizations/49240/{suffix}` paths |
| `_dialogue_request(method, path, body, params)` | Standard HTTP dispatcher for JSON responses |
| `_dialogue_stream_request(method, path, body)` | SSE streaming dispatcher — collects chunked response into a single string |
| `_dialogue_delete_request(path)` | DELETE dispatcher that handles `204 No Content` responses |

### SSE Stream Processing

The `_dialogue_stream_request()` helper:

1. Opens an `httpx` streaming connection
2. Reads lines from the SSE event stream
3. Parses `data: {...}` lines as JSON
4. Extracts text from fields: `content`, `text`, or `delta.content`
5. Stops on `data: [DONE]`
6. Returns: `{ response, chunk_count, raw_chunks[:5] }`

---

## Error Handling

All 6 tools check for configuration before making API calls:

```python
if not COPADO_ORG_ID:
    return {"error": "CONFIG_MISSING", "message": "COPADO_ORG_ID not set in .env"}
```

### Error Response Shapes

**MCP-level errors (returned by the tool):**
```json
{
  "error": "INVALID_AGENT_ID",
  "message": "Agent 'foo' is not valid. Must be one of: build, knowledge, operate, plan, release, test"
}
```

**API-level errors (HTTP 422 — Copado validation):**
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "String should have at most 100 characters",
      "type": "string_too_long"
    }
  ]
}
```

---

## End-to-End Flow Example

```
Step 1: List workspaces
  → copado_list_workspaces()
  ← { workspaces: [...], count: 1 }

Step 2: Start a dialogue with the Build agent
  → copado_start_dialogue(agent_id="build", name="apex-review")
  ← { id: "abc-123", name: "apex-review", assistant_id: "build", ... }

Step 3: Send a prompt
  → copado_send_message(dialogue_id="abc-123", message="Review my Apex class")
  ← { response: "Here are my findings...", chunk_count: 35 }

Step 4: Get full history
  → copado_get_dialogue_history(dialogue_id="abc-123")
  ← { messages: [{role: "user", ...}, {role: "assistant", ...}] }

Step 5: List all dialogues
  → copado_list_dialogues()
  ← { dialogues: [...], count: 3 }

Step 6: Clean up
  → copado_delete_dialogue(dialogue_id="abc-123")
  ← { status: "deleted" }
```
