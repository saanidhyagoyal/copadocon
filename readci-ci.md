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
| 4 | CreatePackage | ✅ | ✅ | [→](#4-createpackage) |
| 5 | CreatePackageVersion | ✅ | ✅ | [→](#5-createpackageversion) |
| 6 | PublishPackageVersion | ✅ | ✅ | [→](#6-publishpackageversion) |
| 7 | ImportPackage | ✅ | ✅ | [→](#7-importpackage) |
| 8 | CheckStatusAction | ✅ | ✅ | [→](#8-checkstatusaction) |
| 9 | RunJobTemplate | ✅ | ✅ | [→](#9-runjobtemplate) |
| 10 | RunTestsAction | ✅ | ✅ | [→](#10-runtestsaction) |
| 11 | TakeSnapshot | ✅ | — | [→](#11-takesnapshot) |

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

---

## 4. CreatePackage

Creates a package.

**URL:** `/json/v1/webhook/mcwebhook/createPackage`

### POST — CreatePackage Action

```
POST /json/v1/webhook/mcwebhook/createPackage
```

**Request Body:**
```json
{
  "payload": {
    "packageId": "a050900000HjW0VAAV",
    "jsonInformation": ""
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `packageId` | string | Salesforce ID of the Package record |
| `jsonInformation` | string | Additional JSON configuration |

**Response:** `200 OK`
```json
{
  "job": {
    "attributes": { "type": "JobExecution__c", "url": "..." },
    "ParentRecord_Id__c": "a050900000HjW0VAAV",
    "Status__c": "In Progress",
    "Callback__c": "PackageCreateAction",
    "Id": "a1q09000000SW2gAAG",
    "ErrorMessage__c": null
  }
}
```

### GET — CreatePackage (Query Param)

```
GET /json/v1/webhook/mcwebhook/createPackage?payload={encodedPayload}
```

**Response:** Same as POST `200 OK`.

---

## 5. CreatePackageVersion

Creates a new package version.

**URL:** `/json/v1/webhook/mcwebhook/createPackageVersion`

### POST — CreatePackageVersion Action

```
POST /json/v1/webhook/mcwebhook/createPackageVersion
```

**Request Body:**
```json
{
  "payload": {
    "packageId": "a050900000HjW0VAAV",
    "versionName": "Summer 2022",
    "versionNumber": "19.20",
    "description": "Latest",
    "jsonInformation": ""
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `packageId` | string | Salesforce ID of the Package |
| `versionName` | string | Human-readable version label |
| `versionNumber` | string | Semantic version number |
| `description` | string | Version description |
| `jsonInformation` | string | Additional JSON configuration |

**Response:** `200 OK`
```json
{
  "job": {
    "attributes": { "type": "JobExecution__c", "url": "..." },
    "Status__c": "In Progress",
    "Callback__c": "PackageVersionCreateAction",
    "Id": "a1q09000000SW2lAAG",
    "ErrorMessage__c": null
  }
}
```

### GET — CreatePackageVersion (Query Param)

```
GET /json/v1/webhook/mcwebhook/createPackageVersion?payload={encodedPayload}
```

**Response:** `200 OK` or `400 Bad Request` (generic error).

---

## 6. PublishPackageVersion

Publishes a package version.

**URL:** `/json/v1/webhook/mcwebhook/publishPackageVersion`

### POST — PublishPackageVersion Action

```
POST /json/v1/webhook/mcwebhook/publishPackageVersion
```

**Request Body:**
```json
{
  "payload": {
    "packageVersionId": "a040900000fNZNtAAO"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `packageVersionId` | string | Salesforce ID of the Package Version |

**Response:** `200 OK`
```json
{
  "job": {
    "attributes": { "type": "JobExecution__c", "url": "..." },
    "Status__c": "In Progress",
    "Callback__c": "PackageVersionPublishAction",
    "Id": "a1q09000000SW2bAAG",
    "ErrorMessage__c": null
  }
}
```

### GET — PublishPackageVersion (Query Param)

```
GET /json/v1/webhook/mcwebhook/publishPackageVersion?payload={encodedPayload}
```

**Response:** `200 OK` or `400 Bad Request`.

---

## 7. ImportPackage

Imports a package into the specified pipeline.

**URL:** `/json/v1/webhook/mcwebhook/importPackage`

### POST — ImportPackage Action

```
POST /json/v1/webhook/mcwebhook/importPackage
```

**Request Body:**
```json
{
  "payload": {
    "packageNameOrId": "Spring 2022",
    "pipelineId": "a0Q0900002Osw0ZEAR",
    "jsonInformation": ""
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `packageNameOrId` | string | Package name or Salesforce ID |
| `pipelineId` | string | Salesforce ID of the target Pipeline |
| `jsonInformation` | string | Additional JSON configuration |

**Response:** `200 OK`
```json
{
  "job": {
    "attributes": { "type": "JobExecution__c", "url": "..." },
    "Status__c": "In Progress",
    "Callback__c": "PackageImportAction",
    "Id": "a1q09000000SW2qAAG",
    "ErrorMessage__c": null
  }
}
```

### GET — ImportPackage (Query Param)

```
GET /json/v1/webhook/mcwebhook/importPackage?payload={encodedPayload}
```

**Response:** `200 OK` or `400 Bad Request`.

---

## 8. CheckStatusAction

Checks the progress status of a job execution result.

**URL:** `/json/v1/webhook/mcwebhook/checkStatusAction`

### POST — CheckStatusAction

```
POST /json/v1/webhook/mcwebhook/checkStatusAction
```

**Request Body:**
```json
{
  "payload": {
    "resultId": "a1009000002sxZ1AAI"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `resultId` | string | Salesforce ID of the Job Execution Result |

**Response:** `200 OK`
```json
{
  "status": "In Progress",
  "resultId": "a1009000002sxZ1AAI",
  "progressStatus": "Creating data",
  "errorMessage": null
}
```

### GET — CheckStatusAction (Query Param)

```
GET /json/v1/webhook/mcwebhook/checkStatusAction?payload={encodedPayload}
```

**Response:** `200 OK` or `400 Bad Request`.

---

## 9. RunJobTemplate

Runs a job template in the context of a specific record.

**URL:** `/json/v1/webhook/mcwebhook/RunJobTemplate`

### POST — RunJobTemplate Action

```
POST /json/v1/webhook/mcwebhook/RunJobTemplate
```

**Request Body:**
```json
{
  "payload": {
    "templateAPIName": "dmo_Run_Test",
    "contextId": "a050900000HjW0VAAV"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `templateAPIName` | string | API name of the Job Template |
| `contextId` | string | Salesforce ID of the context record |

**Response:** `200 OK`
```json
{
  "job": {
    "attributes": { "type": "copado__JobExecution__c", "url": "..." },
    "copado__Status__c": "In Progress",
    "copado__Template__c": "a1s09000000STHOAA4",
    "copado__Callback__c": "",
    "copado__Id": "a1q09000002HMC6AAO",
    "copado__ErrorMessage__c": null
  }
}
```

### GET — RunJobTemplate (Query Param)

```
GET /json/v1/webhook/mcwebhook/RunJobTemplate?payload={encodedPayload}
```

**Response:** `200 OK` or `400 Bad Request`.

---

## 10. RunTestsAction

Triggers execution of specified tests.

**URL:** `/json/v1/webhook/mcwebhook/RunTests`

### POST — RunTestsAction

```
POST /json/v1/webhook/mcwebhook/RunTests
```

**Request Body:**
```json
{
  "payload": {
    "tool": "MC Mock Tool",
    "contextIds": ["a1d090000001ylMAAQ"],
    "extensionConfigurationId": "a1t09000000G2KcAAK",
    "actionCallback": "",
    "resultId": "",
    "acceptanceCriteria": "{}",
    "environmentId": "a0V09000000tkcOEAQ",
    "transactionId": ""
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `tool` | string | Name of the test tool |
| `contextIds` | array[string] | Salesforce IDs of test context records |
| `extensionConfigurationId` | string | Extension Configuration Salesforce ID |
| `actionCallback` | string | Callback identifier |
| `resultId` | string | Existing Result ID (optional) |
| `acceptanceCriteria` | string | JSON string with acceptance criteria |
| `environmentId` | string | Salesforce ID of the environment |
| `transactionId` | string | Transaction identifier |

**Response:** `200 OK`
```json
{
  "jobExecution": {
    "attributes": { "type": "JobExecution__c", "url": "..." },
    "ParentRecord_Id__c": "a1s09000000EFbeAAG",
    "Status__c": "Not Started",
    "Callback__c": "RunTestServiceImpl",
    "Id": "a1o090000066FcoAAE"
  }
}
```

### GET — RunTestsAction (Query Param)

```
GET /json/v1/webhook/mcwebhook/RunTests?payload={encodedPayload}
```

**Response:** `200 OK`, `400`, `401`, or `500`.

---

## 11. TakeSnapshot

Takes a Git snapshot (creates a backup operation record). **POST only — no GET equivalent.**

**URL:** `/json/v1/webhook/mcwebhook/TakeSnapshot`

### POST — TakeSnapshot Action

```
POST /json/v1/webhook/mcwebhook/TakeSnapshot
```

**Request Body:**
```json
{
  "payload": {
    "snapshotId": "snap1",
    "message": "a1d090000001ylMAAQ",
    "otherInformation": "{\"mycustomparamter\":\"customValue\"}",
    "actionCallback": ""
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `snapshotId` | string | Identifier for the snapshot |
| `message` | string | Commit message or context ID |
| `otherInformation` | string | Additional JSON parameters |
| `actionCallback` | string | Callback action identifier |

**Response:** `200 OK`
```json
{
  "job": {
    "attributes": { "type": "copado__Git_Backup__c", "url": "..." },
    "copado__Commit_Message__c": "My Commit",
    "copado__Git_Backup__c": "a1s09000000EFbeAAG",
    "copado__Git_Operation__c": "Commit Files",
    "copado__Status__c": "Pending",
    "copado__Id": "a1o090000066FcoAAE"
  }
}
```

---

## Quick Reference — All Endpoints at a Glance

| # | Method | Endpoint Path | Callback Action |
|---|--------|---------------|-----------------|
| 1 | POST | `/json/v1/webhook/mcwebhook/commit` | `CommitAction` |
| 2 | GET | `/json/v1/webhook/mcwebhook/commit` | `CommitAction` |
| 3 | POST | `/json/v1/webhook/mcwebhook/promotion` | `PromoteAction` |
| 4 | GET | `/json/v1/webhook/mcwebhook/promotion` | `PromoteAction` |
| 5 | POST | `/json/v1/webhook/mcwebhook/promotiondeployment` | `PromotionDeployAction` |
| 6 | GET | `/json/v1/webhook/mcwebhook/promotiondeployment` | `PromotionDeployAction` |
| 7 | POST | `/json/v1/webhook/mcwebhook/createPackage` | `PackageCreateAction` |
| 8 | GET | `/json/v1/webhook/mcwebhook/createPackage` | `PackageCreateAction` |
| 9 | POST | `/json/v1/webhook/mcwebhook/createPackageVersion` | `PackageVersionCreateAction` |
| 10 | GET | `/json/v1/webhook/mcwebhook/createPackageVersion` | `PackageVersionCreateAction` |
| 11 | POST | `/json/v1/webhook/mcwebhook/publishPackageVersion` | `PackageVersionPublishAction` |
| 12 | GET | `/json/v1/webhook/mcwebhook/publishPackageVersion` | `PackageVersionPublishAction` |
| 13 | POST | `/json/v1/webhook/mcwebhook/importPackage` | `PackageImportAction` |
| 14 | GET | `/json/v1/webhook/mcwebhook/importPackage` | `PackageImportAction` |
| 15 | POST | `/json/v1/webhook/mcwebhook/checkStatusAction` | — (status check) |
| 16 | GET | `/json/v1/webhook/mcwebhook/checkStatusAction` | — (status check) |
| 17 | POST | `/json/v1/webhook/mcwebhook/RunJobTemplate` | (dynamic) |
| 18 | GET | `/json/v1/webhook/mcwebhook/RunJobTemplate` | (dynamic) |
| 19 | POST | `/json/v1/webhook/mcwebhook/RunTests` | `RunTestServiceImpl` |
| 20 | GET | `/json/v1/webhook/mcwebhook/RunTests` | `RunTestServiceImpl` |
| 21 | POST | `/json/v1/webhook/mcwebhook/TakeSnapshot` | (Git backup) |

---

## Key Architecture Notes

1. **Dual Access Pattern:** Every resource (except TakeSnapshot) supports both POST (JSON body) and GET (URL-encoded `?payload=` query param). The GET variant is useful for webhook integrations that only support GET.
2. **Async Job Model:** All actions return a `JobExecution__c` (or equivalent) record with `Status__c: "In Progress"`. Use `CheckStatusAction` to poll for completion.
3. **Salesforce Object IDs:** All IDs follow the Salesforce 18-character format (e.g. `a1q09000000SDVlAAO`).
4. **Namespaced vs Unnamespaced Fields:** Some responses use the `copado__` namespace prefix (e.g. `copado__Status__c`) while others use unnamespaced fields (`Status__c`). This depends on whether the org has the Copado managed package installed.
