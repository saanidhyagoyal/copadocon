# Copado DevOps Actions API — Complete Endpoint Reference

> **Source:** [https://copadomulticoudwebhooks.docs.apiary.io/#reference](https://copadomulticoudwebhooks.docs.apiary.io/#reference)
> **Base URL:** `https://app-api.copado.com`
> **Auth Header (all endpoints):** `copado-webhook-key: <your-api-key>`

---

## Table of Contents

| # | Resource | POST | GET | Section |
|---|----------|------|-----|---------|
| 1 | Commit | ✅ | ✅ | [→](#1-commit) |
| 2 | Promote | ✅ | ✅ | [→](#2-promote) |
| 3 | PromotionDeployment | ✅ | ✅ | [→](#3-promotiondeployment) |


**Total: 11 resources, 21 endpoints (10 POST+GET pairs + 1 POST-only)**

---

## Global Authentication

All endpoints require the following header:

```
copado-webhook-key: <your-webhook-api-key>
```

## Global Error Response (400 / 401 / 500)

```json
{
  "timestamp": "time in millis",
  "status": "status message",
  "error": "error message",
  "message": "additional error information"
}
```

---

## 1. Commit

Triggers the commit action on a user story context.

**URL:** `/json/v1/webhook/mcwebhook/commit`

### POST — Commit Action

```
POST /json/v1/webhook/mcwebhook/commit
```

**Headers:**
| Header | Value |
|--------|-------|
| `copado-webhook-key` | `<api-key>` |
| `Content-Type` | `application/json` |

**Request Body:**
```json
{
  "payload": {
    "baseBranch": "hotfix",
    "changes": [
      {
        "t": "LightningComponentBundle",
        "n": "ObjectiveKeyMetrics",
        "m": "force-app/main/default",
        "a": "add",
        "c": "sfdx"
      }
    ],
    "executeCommit": true,
    "message": "Preparing hotfix",
    "recreateFeatureBranch": true,
    "userStoryId": "a0u1n00001St660AAB"
  }
}
```

**Request Body Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `baseBranch` | string | Target branch for the commit |
| `changes` | array | List of metadata components to commit |
| `changes[].t` | string | Metadata type (e.g. `LightningComponentBundle`) |
| `changes[].n` | string | Component name |
| `changes[].m` | string | Module/directory path |
| `changes[].a` | string | Action (`add`, `modify`, `delete`) |
| `changes[].c` | string | Category (e.g. `sfdx`) |
| `executeCommit` | boolean | Whether to execute the commit immediately |
| `message` | string | Commit message |
| `recreateFeatureBranch` | boolean | Whether to recreate the feature branch |
| `userStoryId` | string | Salesforce ID of the User Story |

**Response:** `200 OK`
```json
{
  "userStorycommit": {
    "attributes": {
      "type": "User_Story_Commit__c",
      "url": "/services/data/v54.0/sobjects/User_Story_Commit__c/a1a090000018yebAAA"
    },
    "Id": "a1a090000018yebAAA"
  },
  "jobExecution": {
    "attributes": {
      "type": "JobExecution__c",
      "url": "/services/data/v54.0/sobjects/JobExecution__c/a1q09000000SDVlAAO"
    },
    "UserStoryCommit__c": "a1a090000018yebAAA",
    "Status__c": "In Progress",
    "Template__c": "a1s09000000SHyVAAW",
    "Callback__c": "CommitAction",
    "DataJson__c": "{...}",
    "Pipeline__c": "a0Q0900002Osw0ZEAR",
    "Source__c": "a0W09000005p1vmEAA",
    "Destination__c": null,
    "Id": "a1q09000000SDVlAAO",
    "VolumeOptions__c": "[...]",
    "ErrorMessage__c": null
  }
}
```

### GET — Commit Action (Query Param)

```
GET /json/v1/webhook/mcwebhook/commit?payload={encodedPayload}
```

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `payload` | string | ✅ | URL-encoded JSON string (same structure as POST body) |

**Response:** Same as POST `200 OK`.

---

## 2. Promote

Promotes user stories to the destination environment.

**URL:** `/json/v1/webhook/mcwebhook/promotion`

### POST — Promote Action

```
POST /json/v1/webhook/mcwebhook/promotion
```

**Request Body:**
```json
{
  "payload": {
    "actionCallback": "",
    "deploymentDryRun": false,
    "executeDeployment": true,
    "executePromotion": true,
    "isBackPromotion": false,
    "otherInformation": "",
    "projectId": "a0o5p00000pFwLVAA0",
    "sourceEnvironmentId": "a0S5p00001Pq6c7EAB",
    "userStoryIds": ["a1Y5p00000NVYbEEAX"],
    "promotionId": ""
  }
}
```

**Request Body Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `actionCallback` | string | Callback action identifier |
| `deploymentDryRun` | boolean | If `true`, simulates deployment without executing |
| `executeDeployment` | boolean | Whether to execute the deployment |
| `executePromotion` | boolean | Whether to execute the promotion |
| `isBackPromotion` | boolean | Whether this is a back-promotion |
| `otherInformation` | string | Additional JSON info |
| `projectId` | string | Salesforce ID of the Project |
| `sourceEnvironmentId` | string | Salesforce ID of the source environment |
| `userStoryIds` | array[string] | List of User Story Salesforce IDs |
| `promotionId` | string | Existing Promotion ID (optional) |

**Response:** `200 OK`
```json
{
  "promotion": null,
  "jobExecution": {
    "attributes": { "type": "JobExecution__c", "url": "..." },
    "Callback__c": "PromoteAction",
    "DataJson__c": "{...}",
    "Id": "a1q09000000SDRlAAO",
    "Name": "JE-154",
    "OwnerId": "00509000003f9R7AAI",
    "ParentId__c": "a0u09000003xPdE",
    "Promotion__c": "a0u09000003xPdEAAU",
    "Status__c": "In Progress",
    "VolumeOptions__c": "[...]",
    "JobSteps__r": {
      "totalSize": 2,
      "done": true,
      "records": [{ "Id": "...", "ApiName__c": "JE-154_Step 1", "CustomType__c": "Function" }]
    }
  }
}
```

### GET — Promote Action (Query Param)

```
GET /json/v1/webhook/mcwebhook/promotion?payload={encodedPayload}
```

**Response:** Same as POST `200 OK`.

---

## 3. PromotionDeployment

Deploys a promotion to the destination environment.

**URL:** `/json/v1/webhook/mcwebhook/promotiondeployment`

### POST — PromotionDeployment Action

```
POST /json/v1/webhook/mcwebhook/promotiondeployment
```

**Request Body:**
```json
{
  "payload": {
    "actionCallback": "",
    "deploymentDryRun": false,
    "executeDeployment": true,
    "executePromotion": true,
    "otherInformation": "",
    "promotionId": "a0q5p001GTeo9AAD"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `actionCallback` | string | Callback action identifier |
| `deploymentDryRun` | boolean | Whether to simulate the deployment |
| `executeDeployment` | boolean | Whether to execute the deployment |
| `executePromotion` | boolean | Whether to execute the promotion |
| `otherInformation` | string | Additional JSON info |
| `promotionId` | string | Salesforce ID of the Promotion to deploy |

**Response:** `200 OK`
```json
{
  "jobExecution": {
    "attributes": { "type": "JobExecution__c", "url": "..." },
    "Callback__c": "PromotionDeployAction",
    "Deployment__c": "a0U09000003uV2rEAE",
    "Id": "a1q09000000SDVqAAO",
    "Name": "JE-157",
    "Status__c": "In Progress",
    "JobSteps__r": { "totalSize": 2, "done": true, "records": [...] }
  }
}
```

### GET — PromotionDeployment (Query Param)

```
GET /json/v1/webhook/mcwebhook/promotiondeployment?payload={encodedPayload}
```

**Response:** Same as POST `200 OK`.

------

## Quick Reference — All Endpoints at a Glance

| # | Method | Endpoint Path | Callback Action |
|---|--------|---------------|-----------------|
| 1 | POST | `/json/v1/webhook/mcwebhook/commit` | `CommitAction` |
| 2 | GET | `/json/v1/webhook/mcwebhook/commit` | `CommitAction` |
| 3 | POST | `/json/v1/webhook/mcwebhook/promotion` | `PromoteAction` |
| 4 | GET | `/json/v1/webhook/mcwebhook/promotion` | `PromoteAction` |
| 5 | POST | `/json/v1/webhook/mcwebhook/promotiondeployment` | `PromotionDeployAction` |
| 6 | GET | `/json/v1/webhook/mcwebhook/promotiondeployment` | `PromotionDeployAction` |



## Key Architecture Notes

1. **Dual Access Pattern:** Every resource (except TakeSnapshot) supports both POST (JSON body) and GET (URL-encoded `?payload=` query param). The GET variant is useful for webhook integrations that only support GET.
2. **Async Job Model:** All actions return a `JobExecution__c` (or equivalent) record with `Status__c: "In Progress"`. Use `CheckStatusAction` to poll for completion.
3. **Salesforce Object IDs:** All IDs follow the Salesforce 18-character format (e.g. `a1q09000000SDVlAAO`).
4. **Namespaced vs Unnamespaced Fields:** Some responses use the `copado__` namespace prefix (e.g. `copado__Status__c`) while others use unnamespaced fields (`Status__c`). This depends on whether the org has the Copado managed package installed.
