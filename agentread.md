# 🚀 CopadoGPT Gateway API — Complete Endpoint Reference

> **API Version:** 1.105.0
> **Base URL:** `https://copadogpt-api.robotic.copado.com`
> **Spec:** OpenAPI 3.1.0 (FastAPI)
> **Total Endpoints:** 155
> **Total Schemas:** 182

---

## 📋 Table of Contents

1. [Healthz (1 endpoints)](#healthz)
2. [Check System Status (1 endpoints)](#check-system-status)
3. [Admin (7 endpoints)](#admin)
4. [General (2 endpoints)](#general)
5. [Workspaces (21 endpoints)](#workspaces)
6. [Workflows (25 endpoints)](#workflows)
7. [Webhooks (1 endpoints)](#webhooks)
8. [Dialogues (12 endpoints)](#dialogues)
9. [Messages (1 endpoints)](#messages)
10. [Activity (2 endpoints)](#activity)
11. [V2 (1 endpoints)](#v2)
12. [Quota (1 endpoints)](#quota)
13. [Agents (1 endpoints)](#agents)
14. [Image (1 endpoints)](#image)
15. [Users (11 endpoints)](#users)
16. [Checkouts (3 endpoints)](#checkouts)
17. [Subscriptions (2 endpoints)](#subscriptions)
18. [Skills (7 endpoints)](#skills)
19. [Prompts (9 endpoints)](#prompts)
20. [Salesforce Connector (2 endpoints)](#salesforce-connector)
21. [Integrations (20 endpoints)](#integrations)
22. [Datasets (12 endpoints)](#datasets)
23. [Groups (8 endpoints)](#groups)
24. [Agent Internal (3 endpoints)](#agent-internal)
25. [Mcp (1 endpoints)](#mcp)
26. [Schema / Model Reference](#schema--model-reference)

---

## 🔐 Authentication

Most endpoints require authentication via one or more of the following methods:

| Method | Type | Details |
|--------|------|---------|
| `apikey` | API Key | Primary API key authentication |
| `apikey2` | API Key | Secondary/alternate API key |
| `cookie_auth` | Cookie | Session-based cookie authentication |
| `header_xsrf` | Header | XSRF token in header |
| `cookie_xsrf` | Cookie | XSRF token in cookie |

---

## 📨 Common Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `x-client` | `string` | No | Client identifier for tracking |
| `Content-Type` | `string` | Yes (for POST/PATCH) | `application/json` or `multipart/form-data` |

---

## Healthz

### 🟢 `GET` `/healthz`

**Healthz**

> Check that the server is running

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `HealthResponse` |

---

## Check System Status

### 🟢 `GET` `/organizations/{organization_id}/check-system-status`

**Check System Status**

> Internal endpoint to check the status of all systems

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `maximum_time` | `integer` | No | `-1` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Admin

### 🟢 `GET` `/organizations/{organization_id}/admin/scheduler/health`

**Admin Scheduler Health**

> Scheduler queue depth, lease backlog, and pause state. Requires Copado admin.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SchedulerHealth` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/admin/scheduler/pause`

**Admin Pause Scheduler**

> Pause the scheduler globally. Requires Copado admin.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`SchedulerPauseRequest`](#schedulerpauserequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `duration_minutes` | `integer \| null` | No | Pause duration in minutes. Omit or null for indefinite pause. |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "duration_minutes": 0
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SchedulerHealth` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/admin/scheduler/resume`

**Admin Resume Scheduler**

> Resume the scheduler globally. Requires Copado admin.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SchedulerHealth` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/admin/scheduler/orgs/{org_id}/pause`

**Admin Pause Org Scheduler**

> Pause scheduling for a specific organization. Requires Copado admin.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `org_id` | `integer` | Yes | Org Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`SchedulerPauseRequest`](#schedulerpauserequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `duration_minutes` | `integer \| null` | No | Pause duration in minutes. Omit or null for indefinite pause. |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "duration_minutes": 0
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SchedulerHealth` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/admin/scheduler/orgs/{org_id}/resume`

**Admin Resume Org Scheduler**

> Resume scheduling for a specific organization. Requires Copado admin.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `org_id` | `integer` | Yes | Org Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SchedulerHealth` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/admin/skills/builtin`

**Admin Publish Builtin Skill**

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `SkillPackageResponse` |

---

### 🔴 `DELETE` `/admin/skills/builtin/{skill_id}`

**Admin Delete Builtin Skill**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skill_id` | `string (uuid)` | Yes | Skill Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

## General

### 🟢 `GET` `/organizations/{organization_id}/`

**Read Organization**

> read the details of an Organization.
> icon_url if set is in the format "data:image/png;base64,(data)"
> feature_list is a comma separated list of features enabled for the organization

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `Organization` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/`

**Upsert Organization**

> Create/Update the Organization. only a Workspace manager can call this.
> icon_url must be in the format "data:(mediatype);base64,(data)" and the max length
> is 5mb.
> To remove an icon, send an empty string as its value ( icon_url="" )
> feature_list is a list of strings representing the features enabled for the organization.
> To clear the features, send an empty list as its value ( feature_list=[] )

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`OrganizationUpdate`](#organizationupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `icon_url` | `string \| null` | No |  |
| `feature_list` | `array[string] \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "icon_url": "string",
  "feature_list": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `Organization` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Workspaces

### 🟢 `GET` `/organizations/{organization_id}/workspaces`

**List Workspaces**

> list all Workspace accessible for the current User.
> icon_url if set is in the format "data:image/png;base64,(data)"

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkspaceSummary`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workspaces`

**Create Workspace**

> create a Workspace. any User can call this.
> Limited to 1000 workspaces created per user.
> icon_url must be in the format "data:(mediatype);base64,(data)" and the max length
> is 5mb.
> To remove an icon, send an empty string as its value ( icon_url="" )
> 
> NOTE: capabilities includes an "OtherKnowledge" value that is a catch-all
> for any future unknown capability. Do not show it.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkspaceCreate`](#workspacecreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ Yes |  |
| `description` | `string` | No |  |
| `icon_url` | `string \| null` | No |  |
| `capabilities` | `array[WorkspaceCapability] \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "description": "string",
  "icon_url": "string",
  "capabilities": []
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `Workspace` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workspaces/{workspace_id}`

**Read Workspace**

> read details of a Workspace. only a Workspace Member call this.
> 
> NOTE: capabilities includes an "OtherKnowledge" value that is a catch-all
> for any future unknown capability. Do not show it.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `Workspace` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/workspaces/{workspace_id}`

**Update Workspace**

> update a Workspace. only a Workspace managers call this.
> icon_url must be in the format "data:(mediatype);base64,(data)" and the max length
> is 5mb.
> To remove an icon, send an empty string as its value ( icon_url="" )
> 
> NOTE: capabilities includes an "OtherKnowledge" value that is a catch-all
> for any future unknown capability. Do not show it.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkspaceUpdate`](#workspaceupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string \| null` | No |  |
| `description` | `string \| null` | No |  |
| `default_dataset_id` | `string \| null` | No |  |
| `icon_url` | `string \| null` | No |  |
| `capabilities` | `array[WorkspaceCapability] \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "description": "string",
  "default_dataset_id": "string",
  "icon_url": "string",
  "capabilities": []
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `Workspace` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/workspaces/{workspace_id}`

**Delete Workspace**

> remove a Workspace. only a Workspace managers call this.
> All the documents in the Dataset associated with this workspace will be deleted

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workspaces/{workspace_id}/approvals`

**Read Workspace Approvals**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkspaceApprovalsResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/workspaces/{workspace_id}/approvals`

**Patch Workspace Approvals**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkspaceApprovalsPatch`](#workspaceapprovalspatch)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mode` | `WorkspaceApprovalMode \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "mode": null
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkspaceApprovalsResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/workspaces/{workspace_id}/approvals/exceptions/{exception_id}`

**Delete Workspace Approval Exception**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `exception_id` | `string (uuid)` | Yes | Exception Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkspaceApprovalsResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/workspaces/{workspace_id}/approvals/exceptions`

**Delete All Workspace Approval Exceptions**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkspaceApprovalsResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workspaces/{workspace_id}/approvals/exceptions`

**Create Workspace Approval Exception**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkspaceApprovalExceptionCreate`](#workspaceapprovalexceptioncreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `toolNames` | `array[string]` | ✅ Yes |  |
| `scopeType` | `string` | No |  (default: `tool`) |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "toolNames": "string",
  "scopeType": "tool"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `WorkspaceApprovalsResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workspaces/{workspace_id}/members`

**Create Member**

> Create a Member. Any Workspace Member can invite other  users, but only from the same
> organization

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkspaceMemberCreate`](#workspacemembercreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `integer` | ✅ Yes |  |
| `permission` | `WorkspaceMemberPermission` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "user_id": 0,
  "permission": "..."
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `WorkspaceMember` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/workspaces/{workspace_id}/members/{member_id}`

**Update Member**

> update a Member on a Workspace. only a Workspace managers can update other Member

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `member_id` | `string (uuid)` | Yes | Member Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkspaceMemberUpdate`](#workspacememberupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `permission` | `WorkspaceMemberPermission` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "permission": "..."
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkspaceMember` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/workspaces/{workspace_id}/members/{member_id}`

**Delete Member**

> remove a Member from a Workspace. only a Workspace Managers can remove other Member,
> or the current user can remove himself.
> 
> All the dialogues of the user in this workspace and the documents in them will be deleted.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `member_id` | `string (uuid)` | Yes | Member Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workspaces/{workspace_id}/expert/{expert}/v1/chat/completions`

**Openai Chat Completions**

> OpenAI compatible endpoint (Experimental feature)
>  API Documentation: https://platform.openai.com/docs/api-reference/chat/create
> 
>  Some notes:
> - only messages, tools, response_format, tool_choice, parallel_tool_calls, and stream fields
> are used, the rest are ignored
> - usage data will always be zero
> - the heuristic detection and automatic creation of Chats with the prefix "Automated Chat..."
> is not perfect

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `expert` | `string` | Yes | Expert |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`copadogpt_gateway__app__models__ChatCompletionRequest`](#copadogpt_gateway__app__models__chatcompletionrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | `string` | ✅ Yes |  |
| `messages` | `array[ChatCompletionMessage-Input]` | ✅ Yes |  |
| `max_tokens` | `integer \| null` | No |  |
| `max_completion_tokens` | `integer \| null` | No |  |
| `temperature` | `number \| null` | No |  |
| `top_p` | `number \| null` | No |  |
| `n` | `integer \| null` | No |  |
| `stream` | `boolean \| null` | No |  |
| `stream_options` | `object \| null` | No |  |
| `stop` | `string \| array[string] \| null` | No |  |
| `presence_penalty` | `number \| null` | No |  |
| `frequency_penalty` | `number \| null` | No |  |
| `logit_bias` | `object \| null` | No |  |
| `user` | `string \| null` | No |  |
| `logprobs` | `boolean \| null` | No |  |
| `top_logprobs` | `integer \| null` | No |  |
| `response_format` | `ResponseFormat \| ResponseFormatJsonSchema \| null` | No |  |
| `seed` | `integer \| null` | No |  |
| `service_tier` | `string \| null` | No |  |
| `tools` | `array[Tool] \| null` | No |  |
| `tool_choice` | `string \| object \| null` | No |  |
| `parallel_tool_calls` | `boolean \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "model": "string",
  "messages": [],
  "max_tokens": 0,
  "max_completion_tokens": 0,
  "temperature": 0.0,
  "top_p": 0.0,
  "n": 0,
  "stream": false,
  "stream_options": null,
  "stop": "string",
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "logit_bias": null,
  "user": "string",
  "logprobs": false,
  "top_logprobs": 0,
  "response_format": null,
  "seed": 0,
  "service_tier": "string",
  "tools": [],
  "tool_choice": "string",
  "parallel_tool_calls": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workspaces/{workspace_id}/v1/chat/completions`

**Openai Chat Completions**

> OpenAI compatible endpoint (Experimental feature)
>  API Documentation: https://platform.openai.com/docs/api-reference/chat/create
> 
>  Some notes:
> - only messages, tools, response_format, tool_choice, parallel_tool_calls, and stream fields
> are used, the rest are ignored
> - usage data will always be zero
> - the heuristic detection and automatic creation of Chats with the prefix "Automated Chat..."
> is not perfect

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `expert` | `string` | No | `build` |  |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`copadogpt_gateway__app__models__ChatCompletionRequest`](#copadogpt_gateway__app__models__chatcompletionrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | `string` | ✅ Yes |  |
| `messages` | `array[ChatCompletionMessage-Input]` | ✅ Yes |  |
| `max_tokens` | `integer \| null` | No |  |
| `max_completion_tokens` | `integer \| null` | No |  |
| `temperature` | `number \| null` | No |  |
| `top_p` | `number \| null` | No |  |
| `n` | `integer \| null` | No |  |
| `stream` | `boolean \| null` | No |  |
| `stream_options` | `object \| null` | No |  |
| `stop` | `string \| array[string] \| null` | No |  |
| `presence_penalty` | `number \| null` | No |  |
| `frequency_penalty` | `number \| null` | No |  |
| `logit_bias` | `object \| null` | No |  |
| `user` | `string \| null` | No |  |
| `logprobs` | `boolean \| null` | No |  |
| `top_logprobs` | `integer \| null` | No |  |
| `response_format` | `ResponseFormat \| ResponseFormatJsonSchema \| null` | No |  |
| `seed` | `integer \| null` | No |  |
| `service_tier` | `string \| null` | No |  |
| `tools` | `array[Tool] \| null` | No |  |
| `tool_choice` | `string \| object \| null` | No |  |
| `parallel_tool_calls` | `boolean \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "model": "string",
  "messages": [],
  "max_tokens": 0,
  "max_completion_tokens": 0,
  "temperature": 0.0,
  "top_p": 0.0,
  "n": 0,
  "stream": false,
  "stream_options": null,
  "stop": "string",
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "logit_bias": null,
  "user": "string",
  "logprobs": false,
  "top_logprobs": 0,
  "response_format": null,
  "seed": 0,
  "service_tier": "string",
  "tools": [],
  "tool_choice": "string",
  "parallel_tool_calls": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workspaces/{workspace_id}/expert/{expert}/v1/models`

**Openai Models**

> OpenAI compatible endpoint (Experimental feature)
>  API Documentation: https://platform.openai.com/docs/api-reference/chat/create
> 
>  Some notes:
> - only messages, tools, response_format, tool_choice, parallel_tool_calls, and stream fields
> are used, the rest are ignored
> - usage data will always be zero

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `expert` | `string` | Yes | Expert |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workspaces/{workspace_id}/v1/models`

**Openai Models**

> OpenAI compatible endpoint (Experimental feature)
>  API Documentation: https://platform.openai.com/docs/api-reference/chat/create
> 
>  Some notes:
> - only messages, tools, response_format, tool_choice, parallel_tool_calls, and stream fields
> are used, the rest are ignored
> - usage data will always be zero

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `expert` | `string` | No | `build` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workspaces/{workspace_id}/cline/expert/{expert}/v1/chat/completions`

**Cline Chat Completions**

> Cline compatible endpoint (Experimental feature)
>  Some notes:
> - only messages, tools, response_format, tool_choice, parallel_tool_calls, and stream fields
> are used, the rest are ignored
> - usage data will always be zero
> - this endpoint adds pre-defined instructions, disables features, and responses specifically tailored to Cline, and allows for additional version if Cline decideds to change.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `expert` | `string` | Yes | Expert |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`copadogpt_gateway__app__models__ChatCompletionRequest`](#copadogpt_gateway__app__models__chatcompletionrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | `string` | ✅ Yes |  |
| `messages` | `array[ChatCompletionMessage-Input]` | ✅ Yes |  |
| `max_tokens` | `integer \| null` | No |  |
| `max_completion_tokens` | `integer \| null` | No |  |
| `temperature` | `number \| null` | No |  |
| `top_p` | `number \| null` | No |  |
| `n` | `integer \| null` | No |  |
| `stream` | `boolean \| null` | No |  |
| `stream_options` | `object \| null` | No |  |
| `stop` | `string \| array[string] \| null` | No |  |
| `presence_penalty` | `number \| null` | No |  |
| `frequency_penalty` | `number \| null` | No |  |
| `logit_bias` | `object \| null` | No |  |
| `user` | `string \| null` | No |  |
| `logprobs` | `boolean \| null` | No |  |
| `top_logprobs` | `integer \| null` | No |  |
| `response_format` | `ResponseFormat \| ResponseFormatJsonSchema \| null` | No |  |
| `seed` | `integer \| null` | No |  |
| `service_tier` | `string \| null` | No |  |
| `tools` | `array[Tool] \| null` | No |  |
| `tool_choice` | `string \| object \| null` | No |  |
| `parallel_tool_calls` | `boolean \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "model": "string",
  "messages": [],
  "max_tokens": 0,
  "max_completion_tokens": 0,
  "temperature": 0.0,
  "top_p": 0.0,
  "n": 0,
  "stream": false,
  "stream_options": null,
  "stop": "string",
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "logit_bias": null,
  "user": "string",
  "logprobs": false,
  "top_logprobs": 0,
  "response_format": null,
  "seed": 0,
  "service_tier": "string",
  "tools": [],
  "tool_choice": "string",
  "parallel_tool_calls": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workspaces/{workspace_id}/cline/v1/chat/completions`

**Cline Chat Completions**

> Cline compatible endpoint (Experimental feature)
>  Some notes:
> - only messages, tools, response_format, tool_choice, parallel_tool_calls, and stream fields
> are used, the rest are ignored
> - usage data will always be zero
> - this endpoint adds pre-defined instructions, disables features, and responses specifically tailored to Cline, and allows for additional version if Cline decideds to change.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `expert` | `string` | No | `generalist` |  |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`copadogpt_gateway__app__models__ChatCompletionRequest`](#copadogpt_gateway__app__models__chatcompletionrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | `string` | ✅ Yes |  |
| `messages` | `array[ChatCompletionMessage-Input]` | ✅ Yes |  |
| `max_tokens` | `integer \| null` | No |  |
| `max_completion_tokens` | `integer \| null` | No |  |
| `temperature` | `number \| null` | No |  |
| `top_p` | `number \| null` | No |  |
| `n` | `integer \| null` | No |  |
| `stream` | `boolean \| null` | No |  |
| `stream_options` | `object \| null` | No |  |
| `stop` | `string \| array[string] \| null` | No |  |
| `presence_penalty` | `number \| null` | No |  |
| `frequency_penalty` | `number \| null` | No |  |
| `logit_bias` | `object \| null` | No |  |
| `user` | `string \| null` | No |  |
| `logprobs` | `boolean \| null` | No |  |
| `top_logprobs` | `integer \| null` | No |  |
| `response_format` | `ResponseFormat \| ResponseFormatJsonSchema \| null` | No |  |
| `seed` | `integer \| null` | No |  |
| `service_tier` | `string \| null` | No |  |
| `tools` | `array[Tool] \| null` | No |  |
| `tool_choice` | `string \| object \| null` | No |  |
| `parallel_tool_calls` | `boolean \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "model": "string",
  "messages": [],
  "max_tokens": 0,
  "max_completion_tokens": 0,
  "temperature": 0.0,
  "top_p": 0.0,
  "n": 0,
  "stream": false,
  "stream_options": null,
  "stop": "string",
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "logit_bias": null,
  "user": "string",
  "logprobs": false,
  "top_logprobs": 0,
  "response_format": null,
  "seed": 0,
  "service_tier": "string",
  "tools": [],
  "tool_choice": "string",
  "parallel_tool_calls": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workspaces/{workspace_id}/datasets`

**List Workspace Datasets**

> Lists datasets owned by the workspace.
> Does not list dataset memberships of a workspace.
> - If a dataset is not enabled it will be omitted from non-manager users
>   of the workspace
> Does not list organization datasets

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`DatasetSummary`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workspaces/{workspace_id}/dataset_memberships`

**List Workspace Dataset Memberships**

> Lists dataset memberships of the workspace,
> includes disabled memberships.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`DatasetMemberWorkspace`] |
| `422` | Validation Error | `HTTPValidationError` |

---

## Workflows

### 🟢 `GET` `/organizations/{organization_id}/workflows`

**List Workflows**

> List Workflows

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkflowSummary`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workflows`

**Batch Create Workflow**

> Create a new workflow with nodes and edges.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowBatchData`](#workflowbatchdata)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ Yes |  |
| `title` | `string` | ✅ Yes |  |
| `description` | `string` | ✅ Yes |  |
| `dialogue_id` | `string \| null` | No |  |
| `parameters` | `array[WorkflowParameter]` | No |  (default: `[]`) |
| `initial_state` | `object` | No |  (default: `{}`) |
| `nodes` | `array[WorkflowNodeCreate]` | No |  (default: `[]`) |
| `edges` | `array[WorkflowEdgeCreate]` | No |  (default: `[]`) |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "dialogue_id": "string",
  "parameters": [],
  "initial_state": {},
  "nodes": [],
  "edges": []
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `WorkflowBatchResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/runs`

**List All Workflow Runs**

> List all workflow runs for the organization with optional filtering.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | `array[WorkflowRunStatus] \| null` | No | `—` | Repeat to filter by multiple statuses, e.g. `?status=starting&status=running`. |
| `triggerType` | `WorkflowTriggerType \| null` | No | `—` |  |
| `dialogueId` | `string \| null` | No | `—` |  |
| `startDate` | `string \| null` | No | `—` |  |
| `endDate` | `string \| null` | No | `—` |  |
| `limit` | `integer` | No | `100` |  |
| `offset` | `integer` | No | `0` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkflowRun`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workflows/runs`

**Create Workflow Run**

> Create a new workflow run manually.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowRunCreate`](#workflowruncreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | ✅ Yes |  |
| `workspace_id` | `string (uuid)` | ✅ Yes |  |
| `dialogue_id` | `string \| null` | No |  |
| `trigger_type` | `WorkflowTriggerType` | No |  (default: `manual`) |
| `trigger_data` | `object \| null` | No |  |
| `schedule_id` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "workflow_id": "00000000-0000-0000-0000-000000000000",
  "workspace_id": "00000000-0000-0000-0000-000000000000",
  "dialogue_id": "string",
  "trigger_type": "manual",
  "trigger_data": null,
  "schedule_id": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `WorkflowRun` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/{workflow_id}/runs`

**List Workflow Runs**

> List all runs for a specific workflow.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Workflow Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | `array[WorkflowRunStatus] \| null` | No | `—` | Repeat to filter by multiple statuses, e.g. `?status=starting&status=running`. |
| `triggerType` | `WorkflowTriggerType \| null` | No | `—` |  |
| `dialogueId` | `string \| null` | No | `—` |  |
| `startDate` | `string \| null` | No | `—` |  |
| `endDate` | `string \| null` | No | `—` |  |
| `limit` | `integer` | No | `100` |  |
| `offset` | `integer` | No | `0` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkflowRun`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/workflows/runs/{run_id}`

**Update Workflow Run**

> Update a workflow run's status or timestamps.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `run_id` | `string (uuid)` | Yes | Run Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowRunUpdate`](#workflowrunupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `WorkflowRunStatus \| null` | No |  |
| `started_at` | `string \| null` | No |  |
| `finished_at` | `string \| null` | No |  |
| `error_message` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "status": null,
  "started_at": "string",
  "finished_at": "string",
  "error_message": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkflowRun` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/automations`

**List Workflow Automations**

> List every workflow with at least one schedule or webhook, with triggers and recent runs attached.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `recentRunsLimit` | `integer` | No | `5` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkflowAutomation`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/runs/by-workflow`

**List Runs By Workflow**

> Top-N recent runs + total run count for each requested workflow, returned in one query.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `workflowIds` | `array[string]` | Yes | `—` | Repeat to query multiple workflows, e.g. `?workflowIds=a&workflowIds=b`. |
| `recentRunsLimit` | `integer` | No | `5` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkflowRunsSummary`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/schedules/{schedule_id}`

**Get Workflow Schedule**

> Retrieve a specific workflow schedule.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `schedule_id` | `string (uuid)` | Yes | Schedule Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkflowSchedule` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/workflows/schedules/{schedule_id}`

**Update Workflow Schedule**

> Update a specific workflow schedule.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `schedule_id` | `string (uuid)` | Yes | Schedule Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowScheduleUpdate`](#workflowscheduleupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cron_expr` | `string \| null` | No |  |
| `timezone` | `string \| null` | No |  |
| `parameters` | `object \| null` | No |  |
| `ui_mode` | `string \| null` | No |  |
| `is_active` | `boolean \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "cron_expr": "string",
  "timezone": "string",
  "parameters": null,
  "ui_mode": "string",
  "is_active": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkflowSchedule` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/workflows/schedules/{schedule_id}`

**Delete Workflow Schedule**

> Delete a specific workflow schedule.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `schedule_id` | `string (uuid)` | Yes | Schedule Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/schedules`

**List All Workflow Schedules**

> List every schedule in the org created by the calling user.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkflowSchedule`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/{workflow_id}/schedules`

**List Workflow Schedules**

> List the caller's schedules for a workflow.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Workflow Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkflowSchedule`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workflows/{workflow_id}/schedules`

**Create Workflow Schedule**

> Create a new schedule for a workflow.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Workflow Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowScheduleCreate`](#workflowschedulecreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | ✅ Yes |  |
| `cron_expr` | `string` | ✅ Yes |  |
| `timezone` | `string` | No |  (default: `UTC`) |
| `parameters` | `object` | No |  (default: `{}`) |
| `ui_mode` | `string \| null` | No |  |
| `is_active` | `boolean` | No |  (default: `True`) |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "workspace_id": "00000000-0000-0000-0000-000000000000",
  "cron_expr": "string",
  "timezone": "UTC",
  "parameters": {},
  "ui_mode": "string",
  "is_active": true
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `WorkflowSchedule` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/webhooks/{webhook_id}`

**Get Workflow Webhook**

> Retrieve a specific workflow webhook.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `webhook_id` | `string (uuid)` | Yes | Webhook Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkflowWebhook` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/workflows/webhooks/{webhook_id}`

**Update Workflow Webhook**

> Update a specific workflow webhook.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `webhook_id` | `string (uuid)` | Yes | Webhook Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowWebhookUpdate`](#workflowwebhookupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string \| null` | No |  |
| `webhook_path` | `string \| null` | No |  |
| `http_method` | `string \| null` | No |  |
| `parameter_mapping` | `object \| null` | No |  |
| `is_active` | `boolean \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "workspace_id": "string",
  "webhook_path": "string",
  "http_method": "string",
  "parameter_mapping": null,
  "is_active": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkflowWebhook` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/workflows/webhooks/{webhook_id}`

**Delete Workflow Webhook**

> Delete a specific workflow webhook.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `webhook_id` | `string (uuid)` | Yes | Webhook Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/webhooks`

**List All Workflow Webhooks**

> List every webhook in the org created by the calling user.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkflowWebhook`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/{workflow_id}/webhooks`

**List Workflow Webhooks**

> List the caller's webhooks for a workflow.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Workflow Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`WorkflowWebhook`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workflows/{workflow_id}/webhooks`

**Create Workflow Webhook**

> Create a new webhook for a workflow.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Workflow Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowWebhookCreate`](#workflowwebhookcreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | ✅ Yes |  |
| `webhook_path` | `string` | ✅ Yes |  |
| `http_method` | `string` | No |  (default: `POST`) |
| `parameter_mapping` | `object` | No |  (default: `{}`) |
| `is_active` | `boolean` | No |  (default: `True`) |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "workspace_id": "00000000-0000-0000-0000-000000000000",
  "webhook_path": "string",
  "http_method": "POST",
  "parameter_mapping": {},
  "is_active": true
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `WorkflowWebhook` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/workflows/{workflow_id}`

**Get Workflow By Id**

> Get Workflow by ID

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Unique workflow identifier |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkflowDefinition` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟠 `PUT` `/organizations/{organization_id}/workflows/{workflow_id}`

**Batch Update Workflow**

> Update an existing workflow with new nodes and edges.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Workflow Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowBatchData`](#workflowbatchdata)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ Yes |  |
| `title` | `string` | ✅ Yes |  |
| `description` | `string` | ✅ Yes |  |
| `dialogue_id` | `string \| null` | No |  |
| `parameters` | `array[WorkflowParameter]` | No |  (default: `[]`) |
| `initial_state` | `object` | No |  (default: `{}`) |
| `nodes` | `array[WorkflowNodeCreate]` | No |  (default: `[]`) |
| `edges` | `array[WorkflowEdgeCreate]` | No |  (default: `[]`) |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "dialogue_id": "string",
  "parameters": [],
  "initial_state": {},
  "nodes": [],
  "edges": []
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkflowBatchResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/workflows/{workflow_id}`

**Delete Workflow**

> Delete a workflow.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Workflow Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/workflows/{workflow_id}/clone`

**Clone Workflow**

> Clone a workflow.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Workflow Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `WorkflowSummary` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/workflows/{workflow_id}/nodes/{node_id}`

**Update Workflow Node**

> Update prompt/code or label of a single workflow node.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | Yes | Workflow Id |
| `node_id` | `string (uuid)` | Yes | Node Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowNodeUpdate`](#workflownodeupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | `object \| null` | No |  |
| `label` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "config": null,
  "label": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkflowNode` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Webhooks

### 🔵 `POST` `/organizations/{organization_id}/webhooks/workflows/{webhook_path}`

**Trigger Workflow Webhook**

> Trigger a workflow run via webhook.
> 
> Looks up the webhook by path, resolves parameters from the payload,
> and schedules a proactive workflow run as a background task.
> Returns 202 immediately.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `webhook_path` | `string` | Yes | Webhook Path |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body:**

Content-Type: `application/json`

Type: `object`
*(accepts any JSON object)*

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `202` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Dialogues

### 🔵 `POST` `/organizations/{organization_id}/dialogues`

**Create Dialogue**

> Create an empty dialogue. Only a Workspace Member can do this

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`DialogueCreate`](#dialoguecreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ Yes |  |
| `workspaceId` | `string \| null` | No |  |
| `assistantId` | `string \| null` | No |  (default: `knowledge`) |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "workspaceId": "string",
  "assistantId": "knowledge"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `DialogueResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/dialogues`

**List Dialogues**

> List the dialogues of the user

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `workspace_id` | `string \| null` | No | `—` | Filter dialogues by workspace ID |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`DialogueResponse`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/dialogues/{dialogue_id}`

**Update Dialogue**

> Modify an existing dialogue. Only the dialogue creator can do this

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`DialogueUpdate`](#dialogueupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `DialogueResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/dialogues/{dialogue_id}`

**Delete Dialogue**

> Delete a dialogue and all the documents in AI services.
> Only the dialogue creator can do this

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/dialogues/{dialogue_id}`

**Read Dialogue With Messages**

> Read the details of a dialogue, with all its messages.
> Only the dialogue creator and current workspace member can call this

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `DialogueWithMessagesResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/dialogues/{dialogue_id}/rollback`

**Rollback Dialogue**

> Roll back a dialogue to a given message order. Only the dialogue creator can do this.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`DialogueRollback`](#dialoguerollback)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `beforeTimestamp` | `string (date-time)` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "beforeTimestamp": "2025-01-01T00:00:00Z"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/dialogues/{dialogue_id}/messages`

**Create Message**

> Send a message to AI and stream its response. Only the dialogue creator and current
> workspace member can call this.
> The optional parameter "assistantId" allows to select a different Assistant at any point in
> the conversation. This will override the pre-existing dialogue assistant, or any other change d
> one before this.
> Limited to 1000 messages created per user per month

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`MessageCreate`](#messagecreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `request_id` | `string (uuid)` | ✅ Yes |  |
| `prompt` | `unknown` | No |  |
| `dev_context` | `ChatDevContext \| null` | No |  |
| `system_prompt` | `string \| null` | No |  |
| `assistantId` | `string \| null` | No |  |
| `integrations` | `object \| null` | No |  |
| `tools` | `array[object] \| null` | No |  |
| `tool_choice` | `string \| null` | No |  |
| `messages` | `array[object] \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "request_id": "00000000-0000-0000-0000-000000000000",
  "prompt": "...",
  "dev_context": null,
  "system_prompt": "string",
  "assistantId": "string",
  "integrations": null,
  "tools": [],
  "tool_choice": "string",
  "messages": []
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | array[`string`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/dialogues/{dialogue_id}/messages/{request_id}/feedback`

**Create Feedback**

> Send user feedback on a message. Only the dialogue creator and current
> workspace member can call this

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`FeedbackCreate`](#feedbackcreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | `string` | ✅ Yes |  |
| `response` | `string` | ✅ Yes |  |
| `feedback` | `string \| null` | No |  |
| `sentiment` | `boolean` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "prompt": "string",
  "response": "string",
  "feedback": "string",
  "sentiment": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `SuccessResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/dialogues/{dialogue_id}/agent-session`

**Get Agent Session For Dialogue**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `AgentWorkerResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/dialogues/{dialogue_id}/documents`

**Create Document In Dialogue**

> Create a document in a dialogue. Anybody in the organization can call this if they know the
> dialogue_id, but this behavior will change in the future.
> If the document filename already exists in the dialog, it will be updated, overwritten.
> Limited to 1000mb of documents created per user

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `multipart/form-data`

Schema: [`Body_create_document_in_dialogue_organizations__organization_id__dialogues__dialogue_id__documents_post`](#body_create_document_in_dialogue_organizations__organization_id__dialogues__dialogue_id__documents_post)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | `string` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "file": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `Document` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/dialogues/{dialogue_id}/documents`

**List Documents In Dialogue**

> List all documents in a dialogue. Only owner of dialogue can call this if they know the
> dialogue_id, but this behavior will change in the future.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`Document`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/dialogues/{dialogue_id}/documents/{filename}`

**Delete Document In Dialogue**

> Delete a document in a dialogue. Only the original creator can delete it.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string (uuid)` | Yes | Dialogue Id |
| `filename` | `string` | Yes | Filename |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

## Messages

### 🔵 `POST` `/organizations/{organization_id}/messages/search`

**Search Messages**

> Search messages using semantic, BM25, or hybrid search.
> 
> Scope options (mutually exclusive):
> - dialogue_id: search within a single dialogue
> - workspace_id: search across all user's dialogues in a workspace
> - neither: search across all user's dialogues in the organization

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `dialogue_id` | `string \| null` | No | `—` | Scope search to a single dialogue |
| `workspace_id` | `string \| null` | No | `—` | Scope search to all dialogues in a workspace |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`MessageSearchRequest`](#messagesearchrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | `string` | ✅ Yes |  |
| `k` | `integer` | No |  (default: `4`) |
| `search_strategy` | `string` | No |  (default: `hybrid`) |
| `semantic_weight` | `number` | No |  (default: `0.3`) |
| `bm25_weight` | `number` | No |  (default: `0.7`) |
| `case_sensitive` | `boolean` | No |  (default: `False`) |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "text": "string",
  "k": 4,
  "search_strategy": "hybrid",
  "semantic_weight": 0.3,
  "bm25_weight": 0.7,
  "case_sensitive": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`MessageSearchResult`] |
| `422` | Validation Error | `HTTPValidationError` |

---

## Activity

### 🟢 `GET` `/organizations/{organization_id}/activity`

**List Activity**

> List the activity of all the users of the organization
> - If the user is Organization Admin it will get a list of activity of all the user's org.
> - If the user is not an Or Admin it will get a list of his own activity only.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | `integer` | No | `1` |  |
| `limit` | `integer` | No | `1000` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`TrackedActivity`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/activity/summary`

**Summary Organization**

> List the activity of all the users of the organization or workspace.
> 
> - If the user is Organization Admin it will get a list of stats of all the user's org.
> - If the user is a workspace manager, it will get a list of stats of all the workspace members.
> - If it is a regular user, it will return its own statistics (in a workspace or in general)

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `workspace_id` | `string \| null` | No | `—` | Filter activity by workspace ID |
| `date_since` | `string \| null` | No | `—` | Filter activity starting date |
| `date_until` | `string \| null` | No | `—` | Filter activity ending date |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`UserActivity`] |
| `422` | Validation Error | `HTTPValidationError` |

---

## V2

### 🟢 `GET` `/organizations/{organization_id}/v2/activity`

**List Activity V2**

> List organization activity in nested v2 format
> 
> Same information as /activity but nested into `common` and `details` objects.
> Details are now typed based on the action type for better type safety.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `n` | `integer \| null` | No | `—` | Limit number of activity items returned |
| `start` | `string \| null` | No | `—` | Filter activity starting date |
| `end` | `string \| null` | No | `—` | Filter activity ending date |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`TrackedActivityV2`] |
| `422` | Validation Error | `HTTPValidationError` |

---

## Quota

### 🟢 `GET` `/organizations/{organization_id}/quota`

**Get Organization Quota**

> Retrieve the current prompt quota usage and limit for the organization.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `OrganizationQuota` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Agents

### 🔵 `POST` `/organizations/{organization_id}/agents`

**Create Agent Worker**

> Start an agent worker session

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`AgentWorkerCreate`](#agentworkercreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent` | `string` | ✅ Yes |  |
| `integrations` | `object \| null` | No |  |
| `dev_context` | `ChatDevContext \| null` | No |  |
| `workspace_id` | `string \| null` | No |  |
| `dialogue_id` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "agent": "string",
  "integrations": null,
  "dev_context": null,
  "workspace_id": "string",
  "dialogue_id": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `AgentWorkerResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Image

### 🔵 `POST` `/organizations/{organization_id}/image`

**Resize Image Request**

> Resize an image to fit model requirements

**Request Body (required):**

Content-Type: `application/json`

Schema: [`ImageResizeRequest`](#imageresizerequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image_url` | `string` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "image_url": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `ImageResizeResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Users

### 🟢 `GET` `/organizations/{organization_id}/users/memories`

**Get User Memories**

> Retrieve stored memories for the authenticated user in this organization.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | `integer \| null` | No | `—` | Maximum number of memories to return (None for all) |
| `keys` | `string \| null` | No | `—` | Comma-separated list of specific keys to retrieve |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `MemoryListResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟠 `PUT` `/organizations/{organization_id}/users/memories/{memory_key}`

**Update User Memory**

> Update the value of an existing memory by key.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `memory_key` | `string` | Yes | Memory Key |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`MemoryUpdateRequest`](#memoryupdaterequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | `string` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "value": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/users/memories/{memory_key}`

**Delete User Memory**

> Delete a specific memory by key. The memory_key can contain dots.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `memory_key` | `string` | Yes | Memory Key |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/users/memories/delete`

**Bulk Delete User Memories**

> Delete multiple memories. Pass null keys to delete all.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`MemoryBulkDeleteRequest`](#memorybulkdeleterequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `keys` | `array[string] \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "keys": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/users/{user_id}/onboarding-profile`

**Get User Onboarding Profile**

> Get the onboarding profile for a specific user.
> Can be called by the user themselves or an organization admin.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | `integer` | Yes | User Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `UserOnboardingProfile` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/users/{user_id}/onboarding-profile`

**Create User Onboarding Profile**

> Create an onboarding profile for a specific user.
> Can be called by the user themselves or an organization admin.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | `integer` | Yes | User Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`UserOnboardingProfileCreate`](#useronboardingprofilecreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `string` | ✅ Yes |  |
| `other_role` | `string \| null` | No |  |
| `experience_level` | `string` | ✅ Yes |  |
| `areas_of_interest` | `array[string]` | ✅ Yes |  |
| `team_size` | `string` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "role": "string",
  "other_role": "string",
  "experience_level": "string",
  "areas_of_interest": "string",
  "team_size": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `UserOnboardingProfile` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/users/{user_id}/onboarding-profile`

**Update User Onboarding Profile**

> Update the onboarding profile for a specific user.
> Can be called by the user themselves or an organization admin.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | `integer` | Yes | User Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`UserOnboardingProfileUpdate`](#useronboardingprofileupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `string \| null` | No |  |
| `other_role` | `string \| null` | No |  |
| `experience_level` | `string \| null` | No |  |
| `areas_of_interest` | `array[string] \| null` | No |  |
| `team_size` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "role": "string",
  "other_role": "string",
  "experience_level": "string",
  "areas_of_interest": "string",
  "team_size": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `UserOnboardingProfile` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/users/{user_id}/onboarding-profile`

**Delete User Onboarding Profile**

> Delete the onboarding profile for a specific user.
> Can be called by the user themselves or an organization admin.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | `integer` | Yes | User Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/users/preferences`

**Get User Preferences**

> Get the preferences for the current user.

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `UserPreference` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟠 `PUT` `/users/preferences`

**Upsert User Preferences**

> Create or update preferences for the current user.

**Request Body (required):**

Content-Type: `application/json`

Schema: [`UserPreferenceUpsert`](#userpreferenceupsert)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `default_agent` | `string \| null` | No |  |
| `memory_enabled` | `boolean \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "default_agent": "string",
  "memory_enabled": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `UserPreference` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/users/preferences`

**Delete User Preferences**

> Delete the preferences for the current user.

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

## Checkouts

### 🔵 `POST` `/organizations/{organization_id}/checkouts`

**Create Checkout**

> Initiates a checkout session and returns the Chargebee payment page URL.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`CheckoutInitiateRequest`](#checkoutinitiaterequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `checkoutItemId` | `string` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "checkoutItemId": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `CheckoutInitiateResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/checkouts`

**Get Checkout**

> Retrieve the checkout record for the organization.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `CheckoutWithSubscriptionResponse` |
| `204` | No checkout found for the organization | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/checkouts`

**Delete Checkout**

> Delete the checkout record for the organization.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

## Subscriptions

### 🟢 `GET` `/organizations/{organization_id}/subscriptions`

**Get Subscription**

> Retrieve the subscription for the organization.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SubscriptionResponse` |
| `204` | No subscription found for the organization | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/subscriptions`

**Cancel Subscription**

> Cancel an existing subscription at the end of the term.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SubscriptionResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Skills

### 🔵 `POST` `/organizations/{organization_id}/skills/publish`

**Publish Skill**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`PublishSkillRequest`](#publishskillrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ Yes |  |
| `files` | `object` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "files": {}
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `SkillPackageResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/skills/my`

**List My Skills**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | `integer` | No | `1` |  |
| `limit` | `integer` | No | `1000` |  |
| `query` | `string \| null` | No | `—` |  |
| `scope` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`SkillPackageResponse`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/skills/{skill_id}/promote`

**Promote Skill**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skill_id` | `string (uuid)` | Yes | Skill Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `SkillPackageResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/skills/{skill_id}/demote`

**Demote Skill**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skill_id` | `string (uuid)` | Yes | Skill Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SkillPackageResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/skills/{skill_id}/status`

**Update Skill Status**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skill_id` | `string (uuid)` | Yes | Skill Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`SkillStatusUpdateRequest`](#skillstatusupdaterequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `string` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "status": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SkillPackageResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/skills/{skill_id}`

**Update Skill**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skill_id` | `string (uuid)` | Yes | Skill Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`SkillMetadataUpdateRequest`](#skillmetadataupdaterequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ Yes |  |
| `description` | `string` | No |  |
| `icon` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "description": "string",
  "icon": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `SkillPackageResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/skills/{skill_id}`

**Delete Skill**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skill_id` | `string (uuid)` | Yes | Skill Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

## Prompts

### 🟢 `GET` `/prompts`

**Get User Prompts**

> Retrieve all prompts for the user, merging predefined and custom prompts.
> Pinned prompts are returned first.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `locale` | `string` | No | `en` | Locale for predefined prompts |
| `noAgent` | `array[string]` | No | `—` | Leaves out prompts for the given agent(s), can be repeated |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`PromptResponse`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/prompts`

**Create User Prompt**

> Create a new custom prompt for the specified user.

**Request Body (required):**

Content-Type: `application/json`

Schema: [`CreatePromptRequest`](#createpromptrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | ✅ Yes |  |
| `agent` | `AgentType` | ✅ Yes |  |
| `description` | `string \| null` | No |  |
| `prompt` | `string` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "title": "string",
  "agent": "...",
  "description": "string",
  "prompt": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `CreatedPromptResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/prompts`

**Delete User Prompts**

> Delete multiple custom prompts for the specified user.

**Request Body (required):**

Content-Type: `application/json`

Schema: [`DeletePromptsRequest`](#deletepromptsrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `promptIds` | `array[string]` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "promptIds": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `DeletePromptsCompleteResponse` |
| `207` | Some prompts failed to delete. | `DeletePromptsPartialResponse` |
| `204` | All prompts deleted successfully. | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/prompts/recommend`

**Get Recommended Prompts**

> Retrieve n random prompts from a mix of predefined and custom prompts.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `locale` | `string` | No | `en` | Locale for predefined prompts |
| `noAgent` | `array[string]` | No | `—` | Leaves out prompts for the given agent(s), can be repeated |
| `n` | `integer` | No | `6` | Number of prompts to recommend |
| `pinned` | `boolean \| null` | No | `—` | Prioritize or drop (default) pinned prompts |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`PromptResponse`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/prompts/{prompt_id}`

**Update User Prompt**

> Update an existing custom prompt.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | `string (uuid)` | Yes | Prompt Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`UpdatePromptRequest`](#updatepromptrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string \| null` | No |  |
| `agent` | `AgentType \| null` | No |  |
| `description` | `string \| null` | No |  |
| `prompt` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "title": "string",
  "agent": null,
  "description": "string",
  "prompt": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `UpdatedPromptResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/prompts/{prompt_id}/usage`

**Increment Prompt Usage**

> Increment the usage count by 1 and update the last used timestamp for a specific prompt.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | `string (uuid)` | Yes | Prompt Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `UpdatedPromptUsageResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/prompts/{prompt_id}/share`

**Share Prompt**

> Share a prompt with other users.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | `string (uuid)` | Yes | Prompt Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`SharePromptRequest`](#sharepromptrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `userIds` | `array[integer]` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "userIds": 0
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/prompts/{prompt_id}/pin`

**Pin Prompt**

> Pin a prompt for the current user.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | `string (uuid)` | Yes | Prompt Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/prompts/{prompt_id}/pin`

**Unpin Prompt**

> Unpin a prompt for the current user.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | `string (uuid)` | Yes | Prompt Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

## Salesforce Connector

### 🔵 `POST` `/organizations/{organization_id}/salesforce-connector/workspaces/{workspace_id}/expert/{expert}/chat/completions`

**Chat Completions**

> Salesforce LLM Open Connector API (v1)
> 
> https://github.com/salesforce/einstein-platform
> 
> Some remarks:
> - model is ignored
> - usage data will be always 0
> - heuristic detection and automatic creation of Chats with the prefix "SF Chat..."

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `expert` | `string` | Yes | Expert |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`copadogpt_gateway__app__salesforce_open_connector__ChatCompletionRequest`](#copadogpt_gateway__app__salesforce_open_connector__chatcompletionrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | `string` | ✅ Yes |  |
| `messages` | `array[Message]` | ✅ Yes |  |
| `temperature` | `number \| null` | No |  (default: `1.0`) |
| `n` | `integer \| null` | No |  (default: `1`) |
| `max_tokens` | `integer \| null` | No |  |
| `parameters` | `? \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "model": "string",
  "messages": [],
  "temperature": 1.0,
  "n": 1,
  "max_tokens": 0,
  "parameters": null
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `copadogpt_gateway__app__salesforce_open_connector__ChatCompletionResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/salesforce-connector/workspaces/{workspace_id}/chat/completions`

**Chat Completions**

> Salesforce LLM Open Connector API (v1)
> 
> https://github.com/salesforce/einstein-platform
> 
> Some remarks:
> - model is ignored
> - usage data will be always 0
> - heuristic detection and automatic creation of Chats with the prefix "SF Chat..."

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `expert` | `string` | No | `knowledge` |  |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`copadogpt_gateway__app__salesforce_open_connector__ChatCompletionRequest`](#copadogpt_gateway__app__salesforce_open_connector__chatcompletionrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | `string` | ✅ Yes |  |
| `messages` | `array[Message]` | ✅ Yes |  |
| `temperature` | `number \| null` | No |  (default: `1.0`) |
| `n` | `integer \| null` | No |  (default: `1`) |
| `max_tokens` | `integer \| null` | No |  |
| `parameters` | `? \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "model": "string",
  "messages": [],
  "temperature": 1.0,
  "n": 1,
  "max_tokens": 0,
  "parameters": null
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `copadogpt_gateway__app__salesforce_open_connector__ChatCompletionResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Integrations

### 🟢 `GET` `/organizations/{organization_id}/integrations`

**List Integrations**

> List all organization integrations

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | `integer` | No | `1` |  |
| `limit` | `integer` | No | `100` |  |
| `level` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/integrations`

**Create Integration**

> Add an activated integration to the organization

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`IntegrationCreate`](#integrationcreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | No |  |
| `workspaceId` | `string \| null` | No |  |
| `credential` | `object` | No |  (default: `{}`) |
| `config` | `object \| null` | No |  |
| `type` | `IntegrationTypes` | ✅ Yes |  |
| `category` | `IntegrationCategory` | No |  (default: `GENERAL`) |
| `level` | `string` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "workspaceId": "string",
  "credential": {},
  "config": null,
  "type": "...",
  "category": "GENERAL",
  "level": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `IntegrationResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/integrations/git/ssh-key`

**Generate Git Ssh Key**

> Generate a secure SSH key pair for Git authentication (ECDSA NIST P-256).
> Returns the public key and a pending credential id.
> Private key stored in KeyValueStore (15 min TTL); no rate limit—entries auto-expire.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `SshKeyGenerateResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/integrations/git/ssh-key/pending/{pending_credential_id}`

**Delete Pending Git Ssh Credential**

> Discard a pending SSH credential when user cancels or leaves without saving. Only the owning user can delete.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pending_credential_id` | `string (uuid)` | Yes | Pending Credential Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/integrations/git/validate`

**Validate Git Connection**

> Validate a Git URL and credentials without generating or storing any secret.
> 
> Success: 204 No Content. Failure: 400 with body {"errorCode": "...", "message": "..."}.
> 
> SSH: POST with connectionType "ssh", url (git@...), credential {"privateKey": "<PEM>"}.
> HTTP/HTTPS: POST with connectionType "http_https", url (http(s)://...), credential {"username": "...", "password": "..."}.
> Performs a read-only ls-remote; no data is persisted.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`GitConnectionValidateRequest`](#gitconnectionvalidaterequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | `string` | ✅ Yes | Git repo URL: git@... for SSH, http:// or https:// for HTTP(s). |
| `connectionType` | `string` | No | "ssh" for git@ URLs; "http_https" for http:// or https:// URLs. (default: `ssh`) |
| `credential` | `object` | No | SSH: {"privateKey": "..."}. HTTP(s): {"username": "...", "password": "..."}. |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "url": "string",
  "connectionType": "ssh",
  "credential": {}
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/integrations/configure`

**Configure Integration**

> Get configuration details for integration, like `copado_cicd`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`IntegrationConfigure`](#integrationconfigure)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | `object \| null` | No |  |
| `type` | `IntegrationTypes` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "config": null,
  "type": "..."
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/integrations/agentia-pipeline/users`

**List Agentia Pipeline Users**

> Returns the list of users available in Agentia Pipeline for the current AI platform user.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`CopaIdentityServiceInfo`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/integrations/salesforce_auth`

**Salesforce Auth Integration**

> Callback for the SF auth integration. It needs to be a fixed URL because this is declared
> in Salesforce's connected app, so there are no path parameters.
> 
> redirect_uri is the last page after a successful authentication. E.g. workspace settings page

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` | Yes | `—` |  |
| `level` | `string` | Yes | `—` |  |
| `redirect_uri` | `string` | Yes | `—` |  |
| `org_type` | `string` | Yes | `—` |  |
| `workspace_id` | `string \| null` | No | `—` |  |
| `config` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/integrations/github`

**Github Oauth Initate**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` | Yes | `—` |  |
| `level` | `string` | Yes | `—` |  |
| `redirect_uri` | `string` | Yes | `—` |  |
| `workspace_id` | `string \| null` | No | `—` |  |
| `transport` | `string` | No | `sse` |  |
| `config` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/integrations/google`

**Google Oauth Initiate**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `redirect_uri` | `string` | Yes | `—` |  |
| `workspace_id` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/integrations/oauth`

**Mcp Oauth Initate**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` | Yes | `—` |  |
| `type` | `string` | Yes | `—` |  |
| `level` | `string` | Yes | `—` |  |
| `redirect_uri` | `string` | Yes | `—` |  |
| `server_url` | `string` | Yes | `—` |  |
| `workspace_id` | `string \| null` | No | `—` |  |
| `transport` | `string` | No | `sse` |  |
| `config` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/integrations/{integration_id}`

**Get Integration**

> Get a single integration by id.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `integration_id` | `string (uuid)` | Yes | Integration Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `IntegrationResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/integrations/{integration_id}`

**Update Integration**

> Update an activated integration. Name, config, and credential can be sent in the body.
> Note: Credential updates are only supported for Git repository integrations; sending
> credential for other integration types returns 400.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `integration_id` | `string (uuid)` | Yes | Integration Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`IntegrationUpdate`](#integrationupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | No |  |
| `config` | `object \| null` | No |  |
| `credential` | `object \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "config": null,
  "credential": null
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `IntegrationResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/integrations/{integration_id}`

**Delete Integration**

> Remove an activated integration to the organization

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `integration_id` | `string (uuid)` | Yes | Integration Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/integrations/{integration_id}/configure`

**Get Configure Integration**

> Get configuration details for integration, like `copado_cicd`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `integration_id` | `string (uuid)` | Yes | Integration Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/integrations/{integration_id}/check-status`

**Check Integration Status**

> Live-validate whether a saved integration can authenticate right now.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `integration_id` | `string (uuid)` | Yes | Integration Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `IntegrationCheckResponse` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/integrations/salesforce_auth_callback`

**Salesforce Auth Callback**

> Callback called from Salesforce after authentication.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `code` | `string \| null` | No | `—` |  |
| `state` | `string \| null` | No | `—` |  |
| `error` | `string \| null` | No | `—` |  |
| `error_description` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/integrations/github/callback`

**Github Oauth Callback**

> Callback called from GitHub OAuth 2.1 flow after authentication.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `code` | `string` | Yes | `—` |  |
| `state` | `string` | Yes | `—` |  |
| `error` | `string \| null` | No | `—` |  |
| `error_description` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/integrations/google/callback`

**Google Oauth Callback**

> Callback called from Google OAuth 2.0 flow after authentication.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `code` | `string` | Yes | `—` |  |
| `state` | `string` | Yes | `—` |  |
| `error` | `string \| null` | No | `—` |  |
| `error_description` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/integrations/mcp`

**Mcp Oauth Callback**

> Callback called from MCP OAuth 2.1 flow after authentication.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `code` | `string` | Yes | `—` |  |
| `state` | `string` | Yes | `—` |  |
| `error` | `string \| null` | No | `—` |  |
| `error_description` | `string \| null` | No | `—` |  |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Datasets

### 🔵 `POST` `/organizations/{organization_id}/datasets`

**Create Dataset**

> Create a new dataset.
> - If owner_workspace_id is NOT provided then the user must be an organization admin
>   and the dataset will be owned by the organization.
> - If owner_workspace_id is provided then the user must be a workspace manager
>   and the dataset will be owned by the workspace.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`DatasetCreate`](#datasetcreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ Yes |  |
| `description` | `string` | No |  |
| `owner_workspace_id` | `string \| null` | No |  |
| `enabled` | `boolean` | No |  (default: `True`) |
| `add_to_workspaces` | `DatasetAddRule` | No |  (default: `None`) |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "description": "string",
  "owner_workspace_id": "string",
  "enabled": true,
  "add_to_workspaces": "None"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `Dataset` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/datasets`

**List Datasets**

> Lists datasets owned by the organization.
> Does not list workspace datasets.
> - If dataset is not enabled it will be omitted for non-admin users

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`DatasetSummary`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/datasets/{dataset_id}`

**Update Dataset**

> Update a dataset.
> - If dataset is owned by organization
> - - user must be an organization admin.
> - - if `enabled` is set to false, all enabled dataset workspace memberships will be deleted,
>     disabled memberships will not be deleted.
> - - if `add_to_workspaces` is set to 'New',
>     dataset membership will be added for new workspaces of the organization
>     (workspaces created after the change)
> - - if `add_to_workspaces` is set to 'All',
>     dataset membership will be added for all workspaces of the organization
>     which do not have existing disabled membership.
> - - if `add_to_workspaces` is set to 'ForceAll',
>     dataset membership will be added for all workspaces of the organization
>     and pre-existing disabled memberships will be enabled.
>     Workspaces can still delete or disable the membership afterwards.
> - If dataset is owned by workspace
> - - user must be a workspace manager.
> - - trying to set `add_to_workspaces` to anything else than 'None'
>   will return 406

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`DatasetUpdate`](#datasetupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string \| null` | No |  |
| `description` | `string \| null` | No |  |
| `add_to_workspaces` | `DatasetAddRule \| null` | No |  |
| `enabled` | `boolean \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "description": "string",
  "add_to_workspaces": null,
  "enabled": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `Dataset` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/datasets/{dataset_id}`

**Read Dataset**

> Read details of a Dataset.
> - If dataset is owned by workspace then the user must be a member of the workspace.
> - Returns 404 for non-manager users if dataset is not enabled and is owned by workspace
> - Returns 404 for non-admin users if dataset is not enabled and is owned by organization

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `Dataset` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/datasets/{dataset_id}`

**Delete Dataset**

> Delete a dataset and the documents in the dataset.
> - If dataset is owned by organization then the user must be organization admin.
> - If dataset is owned by workspace then the user must be workspace manager.
> - If dataset is owned by workspace it can not be the default dataset of the workspace.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/datasets/{dataset_id}/documents`

**Create Document In Dataset**

> Create a document in a dataset.
> - If dataset is owned by organization then the user must be organization admin.
> - If dataset is owned by workspace then the user must be workspace member.
> If the document filename already exists in the dataset, it will be updated, overwritten.
> Limited to 1000mb of documents created per user.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `multipart/form-data`

Schema: [`Body_create_document_in_dataset_organizations__organization_id__datasets__dataset_id__documents_post`](#body_create_document_in_dataset_organizations__organization_id__datasets__dataset_id__documents_post)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | `string` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "file": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `Document` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/datasets/{dataset_id}/documents`

**List Documents In Dataset**

> List all documents in a dataset.
> - If dataset is owned by workspace then the user must be workspace member.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`Document`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/datasets/{dataset_id}/documents/{filename}`

**Delete Document In Dataset**

> Delete a document in a dataset.
> - If dataset is owned by organization then the user must be organization admin.
> - If dataset is owned by workspace then the user must be workspace manager.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `filename` | `string` | Yes | Filename |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/datasets/{dataset_id}/member_workspaces`

**List Dataset Member Workspaces**

> List workspaces which have membership record for organization level dataset,
>   includes disabled membership records.
> - If the user is Organization Admin it will get a list of all member workspaces.
> - If the user is not an Organization Admin it will
>   get a list workspace memberships of workspaces where the user is a member.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`DatasetMemberWorkspace`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/datasets/{dataset_id}/member_workspaces`

**Create Dataset Member Workspace**

> Adds organization dataset membership for a workspace.
> User must be a manager of the workspace

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`DatasetMemberWorkspaceCreate`](#datasetmemberworkspacecreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "workspace_id": "00000000-0000-0000-0000-000000000000"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `DatasetMemberWorkspace` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/datasets/{dataset_id}/member_workspaces`

**Update Dataset Member Workspace**

> Updates organization dataset membership of a workspace.
> User must be a manager of the workspace and the org dataset must be enabled.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`DatasetMemberWorkspaceUpdate`](#datasetmemberworkspaceupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | ✅ Yes |  |
| `disabled` | `boolean` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "workspace_id": "00000000-0000-0000-0000-000000000000",
  "disabled": false
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `DatasetMemberWorkspace` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/datasets/{dataset_id}/member_workspaces/{workspace_id}`

**Delete Dataset Member Workspace**

> Deletes an organization dataset membership of a workspace.
> User must be a manager of the workspace

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | Yes | Dataset Id |
| `workspace_id` | `string (uuid)` | Yes | Workspace Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

## Groups

### 🔵 `POST` `/organizations/{organization_id}/groups/`

**Create Group**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`GroupCreate`](#groupcreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ Yes |  |
| `description` | `string` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "description": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `201` | Successful Response | `Group` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/groups/`

**List Groups**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`Group`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/groups/{group_id}`

**Get Group**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `group_id` | `string (uuid)` | Yes | Group Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `Group` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟡 `PATCH` `/organizations/{organization_id}/groups/{group_id}`

**Update Group**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `group_id` | `string (uuid)` | Yes | Group Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`GroupUpdate`](#groupupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string \| null` | No |  |
| `description` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "name": "string",
  "description": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `Group` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/groups/{group_id}`

**Delete Group**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `group_id` | `string (uuid)` | Yes | Group Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/groups/{group_id}/members`

**Add Group Member**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `group_id` | `string (uuid)` | Yes | Group Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`GroupMemberCreate`](#groupmembercreate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `integer` | ✅ Yes |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "user_id": 0
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `GroupMember` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🟢 `GET` `/organizations/{organization_id}/groups/{group_id}/members`

**List Group Members**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `group_id` | `string (uuid)` | Yes | Group Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | array[`GroupMember`] |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔴 `DELETE` `/organizations/{organization_id}/groups/{group_id}/members/{user_id}`

**Remove Group Member**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `group_id` | `string (uuid)` | Yes | Group Id |
| `user_id` | `integer` | Yes | User Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

## Agent Internal

### 🟡 `PATCH` `/organizations/{organization_id}/agent-internal/workflow-runs/{run_id}`

**Set Workflow Run Status From Worker**

> Transition a workflow run between lifecycle states.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `run_id` | `string (uuid)` | Yes | Run Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkflowRunUpdate`](#workflowrunupdate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `WorkflowRunStatus \| null` | No |  |
| `started_at` | `string \| null` | No |  |
| `finished_at` | `string \| null` | No |  |
| `error_message` | `string \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "status": null,
  "started_at": "string",
  "finished_at": "string",
  "error_message": "string"
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `WorkflowRun` |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/agent-internal/workflow-runs/{run_id}/heartbeat`

**Heartbeat Workflow Run From Worker**

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `run_id` | `string (uuid)` | Yes | Run Id |
| `organization_id` | `integer` | Yes | Organization Id |

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `204` | Successful Response | — |
| `422` | Validation Error | `HTTPValidationError` |

---

### 🔵 `POST` `/organizations/{organization_id}/agent-internal/sessions/finish`

**Finish Agent Worker Session**

> Mark the agent worker session as finished. Idempotent.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `integer` | Yes | Organization Id |

**Request Body (required):**

Content-Type: `application/json`

Schema: [`WorkerFinishRequest`](#workerfinishrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error_details` | `object \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "error_details": null
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | Successful Response | `object` |
| `422` | Validation Error | `HTTPValidationError` |

---

## Mcp

### 🔵 `POST` `/mcp/rpc`

**JSON-RPC 2.0 endpoint for MCP protocol**

> JSON-RPC 2.0 endpoint for MCP protocol.
>         
>         Accepts JSON-RPC requests and routes them to appropriate MCP method handlers.
>         
>         **Supported Methods:**
>         - `initialize` - MCP handshake (requires full authentication)
>         - `tools/list` - List available tools (requires full authentication)
>         - `tools/call` - Execute a tool (requires full authentication)
>         - `resources/list` - List available resources (requires full authentication)
>         - `resources/read` - Read a resource (requires full authentication)
>         
>         **Authentication:**
>         All methods require full authentication with `X-Authorization`, `X-Workspace-Id`, and `X-Organization-Id` headers.
>         
>         **Feature Flag:**
>         This endpoint requires the ENABLE_MCP feature flag to be enabled.
>         When disabled, returns 503 Service Unavailable.

**Request Body (required):**

Content-Type: `application/json`

Schema: [`JSONRPCRequest`](#jsonrpcrequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `jsonrpc` | `string` | No |  (default: `2.0`) |
| `method` | `string` | ✅ Yes |  |
| `params` | `object \| null` | No |  (default: `{}`) |
| `id` | `integer \| null` | No |  |

<details>
<summary>📝 Example Request JSON</summary>

```json
{
  "jsonrpc": "2.0",
  "method": "string",
  "params": {},
  "id": 0
}
```

</details>

**Responses:**

| Status | Description | Response Schema |
|--------|-------------|-----------------|
| `200` | JSON-RPC 2.0 response | `object` |
| `401` | Missing or invalid authentication headers | — |
| `400` | Invalid request parameters | — |
| `500` | Internal server error | — |
| `503` | MCP Server is not enabled for this organization | — |
| `422` | Validation Error | `HTTPValidationError` |

---

## Schema / Model Reference

Below are **all 182 data models** (schemas) used across the API.

### `AddedRole`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `target_user_id` | `integer` | ✅ |  |

### `AgentType`

> Agent types for prompts

**Type:** Enum (`string`)

**Values:**
- `build`
- `plan`
- `knowledge`
- `release`
- `operate`
- `test`

### `AgentWorkerCreate`

> Agent worker start request body to CopadoGPT-Gateway

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent` | `string` | ✅ |  |
| `integrations` | `object \| null` | — |  |
| `dev_context` | `ChatDevContext \| null` | — |  |
| `workspace_id` | `string \| null` | — |  |
| `dialogue_id` | `string \| null` | — |  |

### `AgentWorkerResponse`

> Response from CopadoGPT-Gateway to agent worker start request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_worker_url` | `string` | ✅ |  |
| `session_id` | `string (uuid)` | ✅ |  |
| `session_auth_key` | `string` | ✅ |  |

### `ArtifactInfo`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ |  |
| `kind` | `string` | — |  (default: `standard`) |
| `type` | `string` | ✅ |  |
| `title` | `string` | ✅ |  |
| `filename` | `string \| null` | — |  |
| `language` | `string \| null` | — |  |
| `version` | `string \| null` | — |  |
| `timestamp` | `string \| null` | — |  |
| `versioned` | `boolean \| null` | — |  |

### `Assistant`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `name` | `string` | ✅ |  |
| `visible_name` | `string` | ✅ |  |
| `is_builtin` | `boolean` | — |  (default: `False`) |
| `agent` | `string \| null` | — |  |
| `description` | `string` | — |  |
| `instructions` | `string` | — |  |
| `suggestedPrompts` | `array[string]` | ✅ |  |
| `copadoKnowledge` | `boolean` | ✅ |  |

### `BaseOrganizationActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `organization_id` | `integer \| null` | — |  |
| `message` | `string \| null` | — |  |

### `BaseTrackedActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |

### `Body_create_document_in_dataset_organizations__organization_id__datasets__dataset_id__documents_post`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | `string` | ✅ |  |

### `Body_create_document_in_dialogue_organizations__organization_id__dialogues__dialogue_id__documents_post`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | `string` | ✅ |  |

### `ChatCompletionChoice`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `index` | `integer` | ✅ |  |
| `message` | `ChatCompletionMessage-Output` | ✅ |  |
| `finish_reason` | `string \| null` | — |  |
| `logprobs` | `ChatCompletionChoiceLogprobs \| null` | — |  |

### `ChatCompletionChoiceLogprobs`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content` | `array[ChatCompletionTokenLogprob] \| null` | — |  |
| `refusal` | `array[ChatCompletionTokenLogprob] \| null` | — |  |

### `ChatCompletionMessage-Input`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `ChatMessageRole` | ✅ |  |
| `content` | `string \| array[?] \| null` | — |  |
| `name` | `string \| null` | — |  |
| `refusal` | `string \| null` | — |  |
| `tool_calls` | `array[ToolCall] \| null` | — |  |
| `tool_call_id` | `string \| null` | — |  |

### `ChatCompletionMessage-Output`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `ChatMessageRole` | ✅ |  |
| `content` | `string \| array[?] \| null` | — |  |
| `name` | `string \| null` | — |  |
| `refusal` | `string \| null` | — |  |
| `tool_calls` | `array[ToolCall] \| null` | — |  |
| `tool_call_id` | `string \| null` | — |  |

### `ChatCompletionTokenLogprob`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `token` | `string` | ✅ |  |
| `logprob` | `number` | ✅ |  |
| `bytes` | `array[integer] \| null` | — |  |
| `top_logprobs` | `array[object]` | ✅ |  |

### `ChatDevContext`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `libraries` | `array[string]` | ✅ |  |
| `functions` | `array[ChatFunction]` | ✅ |  |
| `buffers` | `array[DevBuffer] \| null` | — |  |

### `ChatFunction`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `parameters` | `JSONSchemaObject` | ✅ |  |
| `description` | `string \| null` | — |  |

### `ChatInteractionResponse`

> A single search result interaction from AI Service

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `ExtendedChatMessage` | ✅ |  |
| `answer` | `ExtendedChatMessage` | ✅ |  |
| `groupId` | `string (uuid)` | ✅ |  |
| `groupName` | `string \| null` | — |  |
| `messageOffset` | `integer` | ✅ |  |

### `ChatMessageImagePart`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | — |  (default: `image`) |
| `image_url` | `ChatMessageImagePartSource` | ✅ |  |
| `artifact` | `ArtifactInfo \| null` | — |  |

### `ChatMessageImagePartSource`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | `string` | ✅ |  |

### `ChatMessageRole`

**Type:** Enum (`string`)

**Values:**
- `system`
- `user`
- `assistant`
- `tool`

### `ChatMessageTextPart`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | — |  (default: `text`) |
| `text` | `string` | ✅ |  |
| `artifact` | `ArtifactInfo \| null` | — |  |

### `ChatMessageThinkingPart`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | — |  (default: `thinking`) |
| `text` | `string` | ✅ |  |
| `artifact` | `ArtifactInfo \| null` | — |  |

### `ChatMessageToolUsePart`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | — |  (default: `tool_use`) |
| `text` | `string` | ✅ |  |
| `artifact` | `ArtifactInfo \| null` | — |  |

### `CheckoutInitiateRequest`

> Request to initiate a checkout session.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `checkoutItemId` | `string` | ✅ |  |

### `CheckoutInitiateResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `checkoutUrl` | `string` | ✅ |  |

### `CheckoutWithSubscriptionResponse`

> Checkout response that may include a newly created subscription.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `organizationId` | `integer` | ✅ |  |
| `chargebeeCheckoutId` | `string` | ✅ |  |
| `status` | `string` | ✅ |  |
| `createdAt` | `string (date-time)` | ✅ |  |
| `subscription` | `SubscriptionResponse \| null` | — |  |

### `Choice`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `index` | `integer` | ✅ |  |
| `message` | `Message` | ✅ |  |
| `finish_reason` | `string` | ✅ |  |

### `ContentPartImageUrl`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | ✅ |  |
| `image_url` | `object` | ✅ |  |

### `ContentPartInputAudio`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | ✅ |  |
| `input_audio` | `object` | ✅ |  |

### `ContentPartRefusal`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | ✅ |  |
| `refusal` | `string` | ✅ |  |

### `ContentPartText`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | ✅ |  |
| `text` | `string` | ✅ |  |

### `ContextPolicy`

> Policy for how context is passed between nodes.

**Type:** Enum (`string`)

**Values:**
- `forward`
- `accumulate`

### `CopaIdentityServiceInfo`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `local_id` | `string` | ✅ |  |
| `label` | `string` | ✅ |  |

### `CreatePromptRequest`

> Request model for creating a prompt

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | ✅ |  |
| `agent` | `AgentType` | ✅ |  |
| `description` | `string \| null` | — |  |
| `prompt` | `string` | ✅ |  |

### `CreatedPromptResponse`

> Response model for created prompt

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `title` | `string` | ✅ |  |
| `agent` | `AgentType` | ✅ |  |
| `description` | `string \| null` | — |  |
| `prompt` | `string` | ✅ |  |
| `createdAt` | `string (date-time)` | ✅ |  |

### `Dataset`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `name` | `string` | ✅ |  |
| `description` | `string` | — |  |
| `organization_id` | `integer` | ✅ |  |
| `owner_workspace_id` | `string \| null` | ✅ |  |
| `add_to_workspaces` | `DatasetAddRule` | — |  (default: `None`) |
| `enabled` | `boolean` | ✅ |  |

### `DatasetActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `organization_id` | `integer \| null` | — |  |
| `message` | `string \| null` | — |  |
| `dataset_id` | `string (uuid)` | ✅ |  |

### `DatasetAddRule`

> - `None`: never add organization dataset memberships automatically - `New`: automatically add organization dataset membership for workspaces created afterwards - `All`: automatically add organization dataset membership for workspaces which have not opted      out previously.      This is determined by checking if there is      existing organization dataset membership for a workspace with `bool disabled==True`. - `ForceAll`: automatically add organization dataset memberships for all workspaces  For workspace owned datasets this must always be `None`

**Type:** Enum (`string`)

**Values:**
- `None`
- `New`
- `All`
- `ForceAll`

### `DatasetCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `description` | `string` | — |  |
| `owner_workspace_id` | `string \| null` | — |  |
| `enabled` | `boolean` | — |  (default: `True`) |
| `add_to_workspaces` | `DatasetAddRule` | — |  (default: `None`) |

### `DatasetMemberWorkspace`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dataset_id` | `string (uuid)` | ✅ |  |
| `workspace_id` | `string (uuid)` | ✅ |  |
| `disabled` | `boolean` | — |  (default: `False`) |

### `DatasetMemberWorkspaceCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | ✅ |  |

### `DatasetMemberWorkspaceUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | ✅ |  |
| `disabled` | `boolean` | ✅ |  |

### `DatasetSummary`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `name` | `string` | ✅ |  |
| `description` | `string` | ✅ |  |
| `owned_by_workspace` | `boolean` | ✅ |  |
| `enabled` | `boolean` | ✅ |  |
| `add_to_workspaces` | `DatasetAddRule` | ✅ |  |

### `DatasetUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string \| null` | — |  |
| `description` | `string \| null` | — |  |
| `add_to_workspaces` | `DatasetAddRule \| null` | — |  |
| `enabled` | `boolean \| null` | — |  |

### `DeletePromptsCompleteResponse`

> Response model for complete bulk deletion success

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `deleted` | `array[string]` | ✅ |  |
| `failed` | `array[object]` | — |  |

### `DeletePromptsPartialResponse`

> Response model for partial bulk deletion success

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `deleted` | `array[string]` | ✅ |  |
| `failed` | `array[object]` | ✅ |  |

### `DeletePromptsRequest`

> Request model for bulk prompt deletion

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `promptIds` | `array[string]` | ✅ |  |

### `DeletedRole`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `target_user_id` | `integer` | ✅ |  |
| `role_id` | `integer` | ✅ |  |

### `DevBuffer`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `content` | `string` | ✅ |  |
| `description` | `string \| null` | — |  |

### `DialogueActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `organization_id` | `integer \| null` | — |  |
| `message` | `string \| null` | — |  |
| `workspace_id` | `string (uuid)` | ✅ |  |
| `dialogue_id` | `string (uuid)` | ✅ |  |

### `DialogueCreate`

> Dialogue creation request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `workspaceId` | `string \| null` | — |  |
| `assistantId` | `string \| null` | — |  (default: `knowledge`) |

### `DialogueResponse`

> Dialogue creation or update response body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `name` | `string` | ✅ |  |
| `workspace_id` | `string \| null` | ✅ |  |
| `message_count` | `integer` | ✅ |  |
| `document_count` | `integer \| null` | — |  |
| `assistant_id` | `string \| null` | — |  |
| `created_at` | `string (date-time)` | ✅ |  |

### `DialogueRollback`

> Dialogue rollback request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `beforeTimestamp` | `string (date-time)` | ✅ |  |

### `DialogueUpdate`

> Dialogue update request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string \| null` | — |  |

### `DialogueWithMessagesResponse`

> Dialogue read response body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `name` | `string` | ✅ |  |
| `workspace_id` | `string \| null` | ✅ |  |
| `message_count` | `integer` | ✅ |  |
| `document_count` | `integer \| null` | — |  |
| `assistant_id` | `string \| null` | — |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `messages` | `array[ExtendedChatMessage]` | ✅ |  |

### `Document`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `filename` | `string` | ✅ |  |
| `size` | `integer` | ✅ |  |

### `DocumentActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `workspace_id` | `string \| null` | — |  |
| `organization_id` | `integer \| null` | — |  |
| `dataset_id` | `string \| null` | — |  |
| `dialogue_id` | `string \| null` | — |  |
| `message` | `string \| null` | — |  |

### `ExtendedChatMessage`

> The 'messages' property of a dialogue contents response from AI Service

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `string` | ✅ |  |
| `content` | `string \| array[?] \| null` | — | Message content, can be plain text or multi-modal content |
| `timestamp` | `string` | ✅ |  |
| `dialogueId` | `string (uuid)` | ✅ |  |
| `messageOffset` | `integer \| null` | — |  |
| `requestId` | `string \| null` | — |  |
| `probability` | `number \| null` | — |  |
| `learnMoreLinks` | `array[LearnMoreLink]` | — |  (default: `[]`) |
| `followUpQuestions` | `array[FollowUpQuestion]` | — |  (default: `[]`) |
| `plots` | `array[Plot]` | — |  (default: `[]`) |
| `assistant` | `string \| null` | — |  |
| `metadata` | `object` | — |  (default: `{}`) |

### `FeedbackCreate`

> User feedback request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | `string` | ✅ |  |
| `response` | `string` | ✅ |  |
| `feedback` | `string \| null` | — |  |
| `sentiment` | `boolean` | ✅ |  |

### `FollowUpQuestion`

> A follow-up question in a response from AI Service

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | `string` | ✅ |  |

### `FunctionCall`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `arguments` | `string` | ✅ |  |

### `FunctionObject`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | `string \| null` | — |  |
| `name` | `string` | ✅ |  |
| `parameters` | `? \| null` | — |  |
| `strict` | `boolean` | — |  (default: `False`) |

### `GitConnectionValidateRequest`

> Request body for validating a Git connection without persisting. No secrets are stored.  SSH: set connectionType to "ssh", url to a git@ URL (e.g. git@github.com:org/repo.git), and credential to {"privateKey": "<PEM string>"} (optional "publicKey" allowed). HTTP/HTTPS: set connectionType to "http_https", url to an http(s):// URL, and credential to {"username": "...", "password": "..."}.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | `string` | ✅ | Git repo URL: git@... for SSH, http:// or https:// for HTTP(s). |
| `connectionType` | `string` | — | "ssh" for git@ URLs; "http_https" for http:// or https:// URLs. (default: `ssh`) |
| `credential` | `object` | — | SSH: {"privateKey": "..."}. HTTP(s): {"username": "...", "password": "..."}. |

### `Group`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `name` | `string` | ✅ |  |
| `organization_id` | `integer` | ✅ |  |
| `description` | `string` | — |  |

### `GroupCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `description` | `string` | — |  |

### `GroupMember`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `group_id` | `string (uuid)` | ✅ |  |
| `user_id` | `integer` | ✅ |  |

### `GroupMemberCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `integer` | ✅ |  |

### `GroupUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string \| null` | — |  |
| `description` | `string \| null` | — |  |

### `HTTPValidationError`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `detail` | `array[ValidationError]` | — |  |

### `HealthResponse`

> Health endpoint response body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `releaseId` | `string` | ✅ |  |
| `status` | `string` | ✅ |  |

### `IdMapping`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflow` | `object` | ✅ |  |
| `nodes` | `object` | ✅ |  |
| `edges` | `object` | ✅ |  |

### `ImageResizeRequest`

> Image resize request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image_url` | `string` | ✅ |  |

### `ImageResizeResponse`

> Image resize response body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image_url` | `string` | ✅ |  |

### `IntegrationCategory`

**Type:** Enum (`string`)

**Values:**
- `GENERAL`
- `MCP`

### `IntegrationCheckResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `type` | `string` | ✅ |  |
| `status` | `string` | ✅ |  |

### `IntegrationConfigure`

> Integration configure request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | `object \| null` | — |  |
| `type` | `IntegrationTypes` | ✅ |  |

### `IntegrationCreate`

> Integration creation request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | — |  |
| `workspaceId` | `string \| null` | — |  |
| `credential` | `object` | — |  (default: `{}`) |
| `config` | `object \| null` | — |  |
| `type` | `IntegrationTypes` | ✅ |  |
| `category` | `IntegrationCategory` | — |  (default: `GENERAL`) |
| `level` | `string` | ✅ |  |

### `IntegrationResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `name` | `string` | — |  |
| `workspaceId` | `string \| null` | — |  |
| `config` | `object \| null` | — |  |
| `level` | `string` | — |  |
| `type` | `string` | — |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |

### `IntegrationTypes`

**Type:** Enum (`string`)

**Values:**
- `copado_cicd`
- `salesforce`
- `atlassian`
- `github`
- `git_repository`
- `agentia_pipeline`
- `google`

### `IntegrationUpdate`

> Integration update request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | — |  |
| `config` | `object \| null` | — |  |
| `credential` | `object \| null` | — |  |

### `JSONRPCRequest`

> JSON-RPC 2.0 request model

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `jsonrpc` | `string` | — |  (default: `2.0`) |
| `method` | `string` | ✅ |  |
| `params` | `object \| null` | — |  (default: `{}`) |
| `id` | `integer \| null` | — |  |

### `JSONSchemaArray`

> An array according to JSON Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | ✅ |  |
| `items` | `JSONSchemaArray \| JSONSchemaObject \| JSONSchemaPrimitive` | ✅ |  |

### `JSONSchemaObject`

> An object according to JSON Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | ✅ |  |
| `properties` | `object` | ✅ |  |
| `required` | `array[string] \| null` | — |  |

### `JSONSchemaPrimitive`

> A single function parameter definition

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string \| array[string]` | ✅ |  |
| `description` | `string \| null` | — |  |
| `enum` | `array[string] \| null` | — |  |

### `JsonValue`

Type: `object`

### `LearnMoreLink`

> A "learn more" link in a response from AI Service

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string \| null` | — |  |
| `title` | `string` | ✅ |  |
| `summary` | `string` | ✅ |  |
| `url` | `string \| null` | — |  |
| `score` | `number \| null` | — |  |

### `MemberActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `organization_id` | `integer \| null` | — |  |
| `message` | `string \| null` | — |  |
| `workspace_id` | `string (uuid)` | ✅ |  |
| `member_user_id` | `integer` | ✅ |  |

### `Memory`

> Single memory item returned to frontend

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | `string` | ✅ |  |
| `value` | `unknown` | ✅ |  |
| `category` | `string \| null` | — |  |
| `metadata` | `object \| null` | — |  |
| `timestamp` | `string \| null` | — |  |

### `MemoryBulkDeleteRequest`

> Request for bulk memory deletion

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `keys` | `array[string] \| null` | — |  |

### `MemoryListResponse`

> Response for listing memories

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `memories` | `array[Memory]` | ✅ |  |
| `totalCount` | `integer` | ✅ |  |

### `MemoryUpdateRequest`

> Request for updating an existing memory's value (manual edit)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | `string` | ✅ |  |

### `Message`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `string` | ✅ |  |
| `content` | `string` | ✅ |  |
| `user` | `string \| null` | — |  |

### `MessageCreate`

> Message creation request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `request_id` | `string (uuid)` | ✅ |  |
| `prompt` | `unknown` | — |  |
| `dev_context` | `ChatDevContext \| null` | — |  |
| `system_prompt` | `string \| null` | — |  |
| `assistantId` | `string \| null` | — |  |
| `integrations` | `object \| null` | — |  |
| `tools` | `array[object] \| null` | — |  |
| `tool_choice` | `string \| null` | — |  |
| `messages` | `array[object] \| null` | — |  |

### `MessageSearchRequest`

> Message search request body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | `string` | ✅ |  |
| `k` | `integer` | — |  (default: `4`) |
| `search_strategy` | `string` | — |  (default: `hybrid`) |
| `semantic_weight` | `number` | — |  (default: `0.3`) |
| `bm25_weight` | `number` | — |  (default: `0.7`) |
| `case_sensitive` | `boolean` | — |  (default: `False`) |

### `MessageSearchResult`

> A search result with its relevance score

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `interaction` | `ChatInteractionResponse` | ✅ |  |
| `score` | `number` | ✅ |  |

### `Organization`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `icon_url` | `string \| null` | — |  |
| `feature_list` | `array[string] \| null` | — |  |

### `OrganizationActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `organization_id` | `integer` | ✅ |  |
| `message` | `string` | ✅ |  |

### `OrganizationQuota`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `usage` | `integer` | ✅ |  |
| `limit` | `integer` | ✅ |  |

### `OrganizationUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `icon_url` | `string \| null` | — |  |
| `feature_list` | `array[string] \| null` | — |  |

### `Plot`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `data` | `array[object]` | — |  (default: `[]`) |
| `layout` | `object` | ✅ |  |

### `PromptResponse`

> Response model for prompt data

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `title` | `string` | ✅ |  |
| `agent` | `AgentType` | ✅ |  |
| `description` | `string \| null` | — |  |
| `prompt` | `string` | ✅ |  |
| `type` | `PromptType` | ✅ |  |
| `createdAt` | `string \| null` | — |  |
| `modifiedAt` | `string \| null` | — |  |
| `usageCount` | `integer` | ✅ |  |
| `lastUsed` | `string \| null` | — |  |
| `sharedBy` | `integer \| null` | — |  |
| `sharedTo` | `array[integer] \| null` | — |  |
| `isPinned` | `boolean` | — |  (default: `False`) |

### `PromptType`

**Type:** Enum (`string`)

**Values:**
- `custom`
- `predefined`

### `PublishSkillRequest`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `files` | `object` | ✅ |  |

### `ResponseFormat`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | ✅ |  |

### `ResponseFormatJsonSchema`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | ✅ |  |
| `json_schema` | `object` | ✅ |  |

### `SchedulerHealth`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `region_paused` | `boolean` | — |  (default: `False`) |
| `region_paused_until` | `string \| null` | — |  |
| `paused_orgs` | `array[integer]` | — |  |
| `pending_runs` | `integer` | ✅ |  |
| `starting_runs` | `integer` | ✅ |  |
| `expired_leases` | `integer` | ✅ |  |
| `active_schedules` | `integer` | ✅ |  |

### `SchedulerPauseRequest`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `duration_minutes` | `integer \| null` | — | Pause duration in minutes. Omit or null for indefinite pause. |

### `SharePromptRequest`

> Request model for sharing a prompt

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `userIds` | `array[integer]` | ✅ |  |

### `SkillMetadataUpdateRequest`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `description` | `string` | — |  |
| `icon` | `string \| null` | — |  |

### `SkillPackageResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `owner_user_id` | `integer` | ✅ |  |
| `name` | `string` | ✅ |  |
| `description` | `string` | — |  |
| `scope` | `string` | — |  (default: `user`) |
| `status` | `string` | — |  (default: `active`) |
| `promoted_to_org` | `boolean` | — |  (default: `False`) |
| `author` | `string \| null` | — |  |
| `icon` | `string \| null` | — |  |
| `icon_url` | `string \| null` | — |  |
| `enabled` | `boolean` | — |  (default: `False`) |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |

### `SkillStatusUpdateRequest`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `string` | ✅ |  |

### `SshKeyGenerateResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `publicKey` | `string` | ✅ |  |
| `pendingCredentialId` | `string` | ✅ |  |

### `SubscriptionResponse`

> Subscription response body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `organizationId` | `integer` | ✅ |  |
| `chargebeeSubscriptionId` | `string` | ✅ |  |
| `chargebeeCustomerId` | `string` | ✅ |  |
| `status` | `string` | ✅ |  |
| `termEnd` | `string \| null` | ✅ |  |
| `nextBillingAt` | `string \| null` | ✅ |  |
| `checkoutItemId` | `string` | ✅ |  |
| `createdBy` | `integer` | ✅ |  |
| `modifiedBy` | `integer` | ✅ |  |

### `SuccessResponse`

> Generic response body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `detail` | `string` | ✅ |  |

### `Tool`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | — |  (default: `function`) |
| `function` | `FunctionObject` | ✅ |  |

### `ToolCall`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ |  |
| `type` | `string` | — |  (default: `function`) |
| `function` | `FunctionCall` | ✅ |  |

### `TrackedAction`

**Type:** Enum (`string`)

**Values:**
- `delete_dataset`
- `delete_dataset_member_workspace`
- `delete_dialogue`
- `delete_document`
- `delete_integration`
- `delete_member`
- `delete_workspace`
- `delete_workflow`
- `feedback_message`
- `new_dataset`
- `new_dataset_member_workspace`
- `new_dialogue`
- `new_document`
- `new_member`
- `new_message`
- `new_openai_message`
- `new_salesforce_message`
- `new_workspace`
- `set_integration`
- `set_skill`
- `promote_skill`
- `update_skill_status`
- `delete_skill`
- `update_member`
- `update_organization`
- `update_workspace`
- `update_dataset`
- `update_dataset_member_workspace`
- `update_integration`
- `login`
- `user_invited`
- `unknown`
- `role_updated`
- `role_deleted`
- `force_enable_dataset_member_workspace`
- `mcp_tool_call`
- `mcp_tool_call_failed`
- `mcp_tools_list`
- `mcp_initialize`
- `mcp_resources_list`
- `mcp_resource_read`
- `mcp_resource_read_failed`
- `update_workspace_approval_mode`

### `TrackedActivity`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `user_id` | `integer \| null` | ✅ |  |
| `organization_id` | `integer \| null` | ✅ |  |
| `action` | `TrackedAction \| null` | — |  |
| `workspace_id` | `string \| null` | — |  |
| `dataset_id` | `string \| null` | — |  |
| `dialogue_id` | `string \| null` | — |  |
| `member_user_id` | `integer \| null` | — |  |
| `message` | `string \| null` | — |  |

### `TrackedActivityCommon`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string \| null` | — |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `user_id` | `integer \| null` | — |  |

### `TrackedActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `workspace_id` | `string \| null` | — |  |
| `dataset_id` | `string \| null` | — |  |
| `dialogue_id` | `string \| null` | — |  |
| `member_user_id` | `integer \| null` | — |  |
| `message` | `string \| null` | — |  |

### `TrackedActivityV2`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `common` | `TrackedActivityCommon` | ✅ |  |
| `details` | `WorkspaceActivityDetails \| DatasetActivityDetails \| DialogueActivityDetails \| DocumentActivityDetails \| MemberActivityDetails \| DeletedRole \| AddedRole \| OrganizationActivityDetails \| BaseTrackedActivityDetails \| TrackedActivityDetails \| WorkspaceDatasetActivityDetails \| BaseOrganizationActivityDetails` | ✅ |  |

### `UpdatePromptRequest`

> Request model for updating a prompt (partial)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string \| null` | — |  |
| `agent` | `AgentType \| null` | — |  |
| `description` | `string \| null` | — |  |
| `prompt` | `string \| null` | — |  |

### `UpdatedPromptResponse`

> Response model for updated prompt

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `title` | `string` | ✅ |  |
| `agent` | `AgentType` | ✅ |  |
| `description` | `string \| null` | — |  |
| `prompt` | `string` | ✅ |  |
| `modifiedAt` | `string (date-time)` | ✅ |  |

### `UpdatedPromptUsageResponse`

> Response model for updated prompt usage

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `usageCount` | `integer` | ✅ |  |
| `lastUsed` | `string (date-time)` | ✅ |  |

### `UserActivity`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `integer` | ✅ |  |
| `count_messages` | `integer` | ✅ |  |
| `count_documents` | `integer` | ✅ |  |
| `count_workspaces` | `integer` | ✅ |  |
| `max_messages` | `integer` | — |  (default: `0`) |
| `max_documents_total` | `integer` | — |  (default: `0`) |

### `UserOnboardingProfile`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `user_id` | `integer` | ✅ |  |
| `role` | `string` | ✅ |  |
| `other_role` | `string \| null` | — |  |
| `experience_level` | `string` | ✅ |  |
| `areas_of_interest` | `array[string]` | ✅ |  |
| `team_size` | `string` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `updated_at` | `string (date-time)` | ✅ |  |

### `UserOnboardingProfileCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `string` | ✅ |  |
| `other_role` | `string \| null` | — |  |
| `experience_level` | `string` | ✅ |  |
| `areas_of_interest` | `array[string]` | ✅ |  |
| `team_size` | `string` | ✅ |  |

### `UserOnboardingProfileUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `string \| null` | — |  |
| `other_role` | `string \| null` | — |  |
| `experience_level` | `string \| null` | — |  |
| `areas_of_interest` | `array[string] \| null` | — |  |
| `team_size` | `string \| null` | — |  |

### `UserPreference`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `user_id` | `integer` | ✅ |  |
| `default_agent` | `string \| null` | — |  |
| `memory_enabled` | `boolean` | ✅ |  |

### `UserPreferenceUpsert`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `default_agent` | `string \| null` | — |  |
| `memory_enabled` | `boolean \| null` | — |  |

### `ValidationError`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `loc` | `array[?]` | ✅ |  |
| `msg` | `string` | ✅ |  |
| `type` | `string` | ✅ |  |
| `input` | `unknown` | — |  |
| `ctx` | `object` | — |  |

### `WorkerFinishRequest`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error_details` | `object \| null` | — |  |

### `WorkflowAutomation`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflow` | `WorkflowSummary` | ✅ |  |
| `schedules` | `array[WorkflowSchedule]` | — |  (default: `[]`) |
| `webhooks` | `array[WorkflowWebhook]` | — |  (default: `[]`) |
| `recentRuns` | `array[WorkflowRun]` | — |  |
| `runCount` | `integer` | — |  (default: `0`) |

### `WorkflowBatchData`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ |  |
| `title` | `string` | ✅ |  |
| `description` | `string` | ✅ |  |
| `dialogue_id` | `string \| null` | — |  |
| `parameters` | `array[WorkflowParameter]` | — |  (default: `[]`) |
| `initial_state` | `object` | — |  (default: `{}`) |
| `nodes` | `array[WorkflowNodeCreate]` | — |  (default: `[]`) |
| `edges` | `array[WorkflowEdgeCreate]` | — |  (default: `[]`) |

### `WorkflowBatchResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflow` | `WorkflowResponse` | ✅ |  |
| `id_mapping` | `IdMapping` | ✅ |  |

### `WorkflowDefinition`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `organization_id` | `integer` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `title` | `string` | ✅ |  |
| `description` | `string \| null` | — |  |
| `dialogue_id` | `string \| null` | — |  |
| `is_built_in` | `boolean` | — |  (default: `False`) |
| `context_policy` | `ContextPolicy` | — |  (default: `forward`) |
| `initial_state` | `object` | — |  (default: `{}`) |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `parameters` | `array[WorkflowParameter]` | — |  (default: `[]`) |
| `nodes` | `array[WorkflowNode]` | — |  (default: `[]`) |
| `edges` | `array[WorkflowEdge]` | — |  (default: `[]`) |

### `WorkflowEdge`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `source_node_id` | `string (uuid)` | ✅ |  |
| `target_node_id` | `string (uuid)` | ✅ |  |
| `condition` | `string \| null` | — |  |

### `WorkflowEdgeCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ |  |
| `source_node_id` | `string \| string` | ✅ |  |
| `target_node_id` | `string \| string` | ✅ |  |
| `condition` | `string \| null` | — |  |

### `WorkflowEdgeResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `source_node_id` | `string (uuid)` | ✅ |  |
| `target_node_id` | `string (uuid)` | ✅ |  |
| `condition` | `string \| null` | — |  |

### `WorkflowNode`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `type` | `string` | ✅ |  |
| `label` | `string` | ✅ |  |
| `config` | `object` | — |  (default: `{}`) |
| `inputs` | `object` | — |  (default: `{}`) |
| `outputs` | `object` | — |  (default: `{}`) |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |

### `WorkflowNodeCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ |  |
| `type` | `string` | ✅ |  |
| `label` | `string` | ✅ |  |
| `config` | `object` | — |  (default: `{}`) |
| `inputs` | `object` | — |  (default: `{}`) |
| `outputs` | `object` | — |  (default: `{}`) |

### `WorkflowNodeResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `type` | `string` | ✅ |  |
| `label` | `string` | ✅ |  |
| `config` | `object \| null` | — |  |
| `inputs` | `object` | — |  (default: `{}`) |
| `outputs` | `object` | — |  (default: `{}`) |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |

### `WorkflowNodeUpdate`

> Patch payload for a single workflow node (prompt/code/label edits).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | `object \| null` | — |  |
| `label` | `string \| null` | — |  |

### `WorkflowParameter`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `type` | `string` | ✅ |  |
| `description` | `string \| null` | — |  |
| `required` | `boolean` | — |  (default: `True`) |
| `default` | `? \| null` | — |  |

### `WorkflowResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `organization_id` | `integer` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `title` | `string` | ✅ |  |
| `description` | `string` | ✅ |  |
| `dialogue_id` | `string \| null` | — |  |
| `is_built_in` | `boolean` | — |  (default: `False`) |
| `initial_state` | `object` | — |  (default: `{}`) |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `parameters` | `array[WorkflowParameter]` | — |  (default: `[]`) |
| `nodes` | `array[WorkflowNodeResponse]` | — |  (default: `[]`) |
| `edges` | `array[WorkflowEdgeResponse]` | — |  (default: `[]`) |

### `WorkflowRun`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `workflowId` | `string (uuid)` | ✅ |  |
| `organizationId` | `integer` | ✅ |  |
| `workspaceId` | `string (uuid)` | ✅ |  |
| `workspaceDeleted` | `boolean` | — |  (default: `False`) |
| `dialogueId` | `string \| null` | ✅ |  |
| `createdBy` | `integer` | ✅ |  |
| `triggerType` | `WorkflowTriggerType` | ✅ |  |
| `triggerData` | `object \| null` | ✅ |  |
| `scheduleId` | `string \| null` | ✅ |  |
| `status` | `WorkflowRunStatus` | ✅ |  |
| `createdAt` | `string (date-time)` | ✅ |  |
| `startedAt` | `string \| null` | ✅ |  |
| `finishedAt` | `string \| null` | ✅ |  |
| `errorMessage` | `string \| null` | ✅ |  |

### `WorkflowRunCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflow_id` | `string (uuid)` | ✅ |  |
| `workspace_id` | `string (uuid)` | ✅ |  |
| `dialogue_id` | `string \| null` | — |  |
| `trigger_type` | `WorkflowTriggerType` | — |  (default: `manual`) |
| `trigger_data` | `object \| null` | — |  |
| `schedule_id` | `string \| null` | — |  |

### `WorkflowRunStatus`

**Type:** Enum (`string`)

**Values:**
- `pending`
- `starting`
- `running`
- `success`
- `error`
- `cancelled`

### `WorkflowRunUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `WorkflowRunStatus \| null` | — |  |
| `started_at` | `string \| null` | — |  |
| `finished_at` | `string \| null` | — |  |
| `error_message` | `string \| null` | — |  |

### `WorkflowRunsSummary`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflowId` | `string (uuid)` | ✅ |  |
| `recentRuns` | `array[WorkflowRun]` | — |  |
| `runCount` | `integer` | — |  (default: `0`) |

### `WorkflowSchedule`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `workflowId` | `string (uuid)` | ✅ |  |
| `organizationId` | `integer` | ✅ |  |
| `workspaceId` | `string (uuid)` | ✅ |  |
| `cronExpr` | `string` | ✅ |  |
| `timezone` | `string` | ✅ |  |
| `parameters` | `object` | ✅ |  |
| `uiMode` | `string \| null` | — |  |
| `isActive` | `boolean` | ✅ |  |
| `lastFiredAt` | `string \| null` | ✅ |  |
| `createdBy` | `integer \| null` | ✅ |  |
| `createdAt` | `string (date-time)` | ✅ |  |
| `updatedAt` | `string (date-time)` | ✅ |  |

### `WorkflowScheduleCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | ✅ |  |
| `cron_expr` | `string` | ✅ |  |
| `timezone` | `string` | — |  (default: `UTC`) |
| `parameters` | `object` | — |  (default: `{}`) |
| `ui_mode` | `string \| null` | — |  |
| `is_active` | `boolean` | — |  (default: `True`) |

### `WorkflowScheduleUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cron_expr` | `string \| null` | — |  |
| `timezone` | `string \| null` | — |  |
| `parameters` | `object \| null` | — |  |
| `ui_mode` | `string \| null` | — |  |
| `is_active` | `boolean \| null` | — |  |

### `WorkflowSummary`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `title` | `string` | ✅ |  |
| `description` | `string \| null` | — |  |
| `dialogue_id` | `string \| null` | — |  |
| `is_built_in` | `boolean` | — |  (default: `False`) |
| `parameters` | `array[WorkflowParameter]` | — |  (default: `[]`) |
| `created_at` | `string \| null` | — |  |
| `modified_at` | `string \| null` | — |  |

### `WorkflowTriggerType`

**Type:** Enum (`string`)

**Values:**
- `schedule`
- `webhook`
- `review_mode`
- `manual`

### `WorkflowWebhook`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `workflowId` | `string (uuid)` | ✅ |  |
| `organizationId` | `integer` | ✅ |  |
| `workspaceId` | `string (uuid)` | ✅ |  |
| `webhookPath` | `string` | ✅ |  |
| `httpMethod` | `string` | ✅ |  |
| `parameterMapping` | `object` | ✅ |  |
| `isActive` | `boolean` | ✅ |  |
| `createdBy` | `integer \| null` | ✅ |  |
| `createdAt` | `string (date-time)` | ✅ |  |
| `updatedAt` | `string (date-time)` | ✅ |  |

### `WorkflowWebhookCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string (uuid)` | ✅ |  |
| `webhook_path` | `string` | ✅ |  |
| `http_method` | `string` | — |  (default: `POST`) |
| `parameter_mapping` | `object` | — |  (default: `{}`) |
| `is_active` | `boolean` | — |  (default: `True`) |

### `WorkflowWebhookUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workspace_id` | `string \| null` | — |  |
| `webhook_path` | `string \| null` | — |  |
| `http_method` | `string \| null` | — |  |
| `parameter_mapping` | `object \| null` | — |  |
| `is_active` | `boolean \| null` | — |  |

### `Workspace`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `name` | `string` | ✅ |  |
| `description` | `string` | — |  |
| `organization_id` | `integer` | ✅ |  |
| `icon_url` | `string \| null` | ✅ |  |
| `default_dataset_id` | `string \| null` | — |  |
| `members` | `array[WorkspaceMember]` | ✅ |  |
| `assistants` | `array[Assistant]` | ✅ |  |
| `datasets` | `array[DatasetSummary]` | ✅ |  |
| `dataset_memberships` | `array[DatasetMemberWorkspace]` | ✅ |  |
| `currentUserMember` | `WorkspaceMember` | ✅ |  |
| `capabilities` | `array[WorkspaceCapability]` | ✅ |  |
| `integrations` | `array[WorkspaceIntegration]` | ✅ |  |

### `WorkspaceActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `organization_id` | `integer \| null` | — |  |
| `message` | `string \| null` | — |  |
| `workspace_id` | `string (uuid)` | ✅ |  |

### `WorkspaceApprovalExceptionCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `toolNames` | `array[string]` | ✅ |  |
| `scopeType` | `string` | — |  (default: `tool`) |

### `WorkspaceApprovalExceptionResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `scopeValue` | `string` | ✅ |  |
| `scopeType` | `string` | — |  (default: `tool`) |

### `WorkspaceApprovalMode`

**Type:** Enum (`string`)

**Values:**
- `accept_all`
- `accept_read_only`
- `ask_all`

### `WorkspaceApprovalsPatch`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mode` | `WorkspaceApprovalMode \| null` | — |  |

### `WorkspaceApprovalsResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mode` | `WorkspaceApprovalMode` | ✅ |  |
| `canEdit` | `boolean` | ✅ |  |
| `exceptions` | `array[WorkspaceApprovalExceptionResponse]` | — |  |

### `WorkspaceCapability`

> Core Capabilities: - FollowUpQuestions: Enables generation of follow-up questions - Reasoning: Required for knowledge processing capabilities - WebSearch: Enables web search capabilities - STEM: Enables tailored method for answering coding and math questions - DeepResearch: Enables advanced research capabilities - LongTermMemory: Enables long-term memory capabilities (storing information about the user preferences) - TabularData: Enables tabular data processing capabilities - Mermaid: Enables rendering of diagrams using Mermaid syntax - Mindmap: Enables generation of mind maps - Artifacts: Supports Artifact tags for sideview  Knowledge Capabilities: - CustomKnowledge: Enables processing of user-uploaded documents - EssentialsKnowledge: Enables Copado Essentials product knowledge - CRTKnowledge: Enables Copado Robotic Testing knowledge - MetadataFormatKnowledge: Enables Metadata Format knowledge - SourceFormatKnowledge: Enables Source Format knowledge

**Type:** Enum (`string`)

**Values:**
- `FollowUpQuestions`
- `Reasoning`
- `WebSearch`
- `STEM`
- `DeepResearch`
- `LongTermMemory`
- `Mindmap`
- `Mermaid`
- `Artifacts`
- `TabularData`
- `CustomKnowledge`
- `EssentialsKnowledge`
- `CRTKnowledge`
- `MetadataFormatKnowledge`
- `SourceFormatKnowledge`
- `OtherKnowledge`
- `AgentFramework`

### `WorkspaceCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ |  |
| `description` | `string` | — |  |
| `icon_url` | `string \| null` | — |  |
| `capabilities` | `array[WorkspaceCapability] \| null` | — |  |

### `WorkspaceDatasetActivityDetails`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `TrackedAction` | ✅ |  |
| `organization_id` | `integer \| null` | — |  |
| `message` | `string \| null` | — |  |
| `workspace_id` | `string (uuid)` | ✅ |  |
| `dataset_id` | `string (uuid)` | ✅ |  |

### `WorkspaceIntegration`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `name` | `string` | ✅ |  |
| `workspace_id` | `string \| null` | ✅ |  |
| `type` | `string` | ✅ |  |
| `level` | `string` | ✅ |  |
| `user_id` | `integer \| null` | ✅ |  |
| `config` | `object` | ✅ |  |

### `WorkspaceMember`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `user_id` | `integer` | ✅ |  |
| `permission` | `WorkspaceMemberPermission` | ✅ |  |

### `WorkspaceMemberCreate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `integer` | ✅ |  |
| `permission` | `WorkspaceMemberPermission` | ✅ |  |

### `WorkspaceMemberPermission`

**Type:** Enum (`string`)

**Values:**
- `Manage`
- `Access`

### `WorkspaceMemberUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `permission` | `WorkspaceMemberPermission` | ✅ |  |

### `WorkspaceSummary`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string (uuid)` | ✅ |  |
| `created_at` | `string (date-time)` | ✅ |  |
| `modified_at` | `string (date-time)` | ✅ |  |
| `created_by` | `integer` | ✅ |  |
| `modified_by` | `integer` | ✅ |  |
| `name` | `string` | ✅ |  |
| `description` | `string` | — |  |
| `organization_id` | `integer` | ✅ |  |
| `icon_url` | `string \| null` | ✅ |  |

### `WorkspaceUpdate`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string \| null` | — |  |
| `description` | `string \| null` | — |  |
| `default_dataset_id` | `string \| null` | — |  |
| `icon_url` | `string \| null` | — |  |
| `capabilities` | `array[WorkspaceCapability] \| null` | — |  |

### `copadogpt_gateway__app__models__ChatCompletionRequest`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | `string` | ✅ |  |
| `messages` | `array[ChatCompletionMessage-Input]` | ✅ |  |
| `max_tokens` | `integer \| null` | — |  |
| `max_completion_tokens` | `integer \| null` | — |  |
| `temperature` | `number \| null` | — |  |
| `top_p` | `number \| null` | — |  |
| `n` | `integer \| null` | — |  |
| `stream` | `boolean \| null` | — |  |
| `stream_options` | `object \| null` | — |  |
| `stop` | `string \| array[string] \| null` | — |  |
| `presence_penalty` | `number \| null` | — |  |
| `frequency_penalty` | `number \| null` | — |  |
| `logit_bias` | `object \| null` | — |  |
| `user` | `string \| null` | — |  |
| `logprobs` | `boolean \| null` | — |  |
| `top_logprobs` | `integer \| null` | — |  |
| `response_format` | `ResponseFormat \| ResponseFormatJsonSchema \| null` | — |  |
| `seed` | `integer \| null` | — |  |
| `service_tier` | `string \| null` | — |  |
| `tools` | `array[Tool] \| null` | — |  |
| `tool_choice` | `string \| object \| null` | — |  |
| `parallel_tool_calls` | `boolean \| null` | — |  |

### `copadogpt_gateway__app__models__ChatCompletionResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ |  |
| `object` | `string` | ✅ |  |
| `created` | `integer` | ✅ |  |
| `model` | `string` | ✅ |  |
| `choices` | `array[ChatCompletionChoice]` | ✅ |  |
| `usage` | `copadogpt_gateway__app__models__Usage \| null` | — |  |
| `system_fingerprint` | `string \| null` | — |  |

### `copadogpt_gateway__app__models__Usage`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt_tokens` | `integer` | ✅ |  |
| `completion_tokens` | `integer` | ✅ |  |
| `total_tokens` | `integer` | ✅ |  |
| `completion_tokens_details` | `object \| null` | — |  |

### `copadogpt_gateway__app__salesforce_open_connector__ChatCompletionRequest`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | `string` | ✅ |  |
| `messages` | `array[Message]` | ✅ |  |
| `temperature` | `number \| null` | — |  (default: `1.0`) |
| `n` | `integer \| null` | — |  (default: `1`) |
| `max_tokens` | `integer \| null` | — |  |
| `parameters` | `? \| null` | — |  |

### `copadogpt_gateway__app__salesforce_open_connector__ChatCompletionResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | — |  |
| `object` | `string` | — |  (default: `chat.completion`) |
| `created` | `integer` | — |  |
| `model` | `string` | ✅ |  |
| `choices` | `array[Choice]` | ✅ |  |
| `usage` | `copadogpt_gateway__app__salesforce_open_connector__Usage` | ✅ |  |

### `copadogpt_gateway__app__salesforce_open_connector__Usage`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt_tokens` | `integer` | ✅ |  |
| `completion_tokens` | `integer` | ✅ |  |
| `total_tokens` | `integer` | ✅ |  |
