# Rebate-Management-System

A rebate management system that handles rebate program data, calculates rebates, and provides endpoints for basic
reporting

# API Documentation

## Overview

This documentation provides details about the API endpoints related to rebate claims, rebate programs, and transactions.

---

## Base URL

The base URL for all API requests will depend on the deployment environment. Examples:

- **Development:** `http://localhost:8420/`
- **Production:** `https://rebate.com/`

---

## Endpoints

### 1. **Rebate Programs**

#### 1.1 Create a New Rebate Program

- **Endpoint**: `POST /api/v1/rebate-programs`
- **Summary**: Create a new rebate program.

##### Example Request

```
{
    "program_name": "Program11",
    "rebate_percentage": 80,
    "start_date": "2025-01-15",
    "end_date": "2025-04-15",
    "eligibility_criteria": "Must have spent more than 20 Lakhs"
}
```

##### Example Response

- Failure

```
{
    "errors": [
        {
            "message": "program_name with value Program11 already exists"
        }
    ]
}
```

- Success

```
{
    "start_date": "2025-01-15 00:00:00",
    "id": "61624e99-abfa-48e9-b348-f90a605d728f",
    "eligibility_criteria": "Must have spent more than 20 Lakhs",
    "last_update_time": "2025-01-19 18:49:54",
    "program_name": "Program12",
    "rebate_percentage": 80.0,
    "end_date": "2025-04-15 00:00:00"
}
```

---

#### 1.2 Get all Rebate Programs

- **Endpoint**: `GET /api/v1/rebate-programs`
- **Summary**: Retrieve all available rebate programs.

##### Example Response

```
{
    "Program11": {
        "start_date": "2025-01-15 00:00:00",
        "id": "82f6e880-867d-415f-932b-0d0f6e35cfe0",
        "eligibility_criteria": "Must have spent more than 20 Lakhs",
        "last_update_time": "2025-01-19 16:55:00",
        "program_name": "Program11",
        "rebate_percentage": 80.0,
        "end_date": "2025-04-15 00:00:00"
    },
    "Program12": {
        "start_date": "2025-01-15 00:00:00",
        "id": "61624e99-abfa-48e9-b348-f90a605d728f",
        "eligibility_criteria": "Must have spent more than 20 Lakhs",
        "last_update_time": "2025-01-19 18:49:54",
        "program_name": "Program12",
        "rebate_percentage": 80.0,
        "end_date": "2025-04-15 00:00:00"
    }
}
```

---

### 2. **Transactions**

#### 2.1 Create a New Transaction

- **Endpoint**: `POST /api/v1/transactions`
- **Summary**: Create a new transaction.

##### Example Request

```
{
    "amount": 90.1,
    "transaction_date": "2025-02-16",
    "rebate_program_id": "2aea8485-641e-4860-b9c1-81c87ece3609"
}
```

##### Example Response

- Failure

```
{
    "errors": [
        {
            "message": "Rebate program with ID 2aea8485-641e-4860-b9c1-81c87ece3608 not found."
        }
    ]
}
```

- Success

```
{
    "id": "f71a4538-afcb-43dd-86b8-1499c1a01bf1",
    "rebate_program_id": "2aea8485-641e-4860-b9c1-81c87ece3609",
    "last_update_time": "2025-01-19 18:52:15",
    "amount": 90.1,
    "transaction_date": "2025-02-16 00:00:00"
}
```

---

#### 2.2 Get All Transactions

- **Endpoint**: `GET /api/v1/transactions`
- **Summary**: Retrieve all transactions.

##### Example Response

```
{
    "0a314ea5-e789-478f-8711-b0cca3bb9fb4": {
        "id": "0a314ea5-e789-478f-8711-b0cca3bb9fb4",
        "transaction_date": "2025-02-16 00:00:00",
        "last_update_time": "2025-01-19 13:57:27",
        "rebate_program_id": "2bf09f96-c56f-4451-8be0-4892f0f522b8",
        "amount": 100.1
    },
    "b1c0eceb-3dbc-41cd-88b7-af0a4fdf14b4": {
        "id": "b1c0eceb-3dbc-41cd-88b7-af0a4fdf14b4",
        "transaction_date": "2025-02-16 00:00:00",
        "last_update_time": "2025-01-19 16:55:36",
        "rebate_program_id": "2aea8485-641e-4860-b9c1-81c87ece3609",
        "amount": 90.1
    }
}
```

---

#### 2.3 Get Details of a Transaction

- **Endpoint**: `GET /api/v1/transactions/{transaction_id}`
- **Summary**: Retrieve details of a specific transaction by its ID.

##### Path Parameters

- **`transaction_id`** *(required)*: The unique identifier of the transaction.

##### Query Parameters

- **`include_rebate`** *(optional)*: Include rebate amount if true. Default value is false (format: `true` or `false`).

##### Example Response

- include_rebate=true

```
{
    "id": "b1c0eceb-3dbc-41cd-88b7-af0a4fdf14b4",
    "amount": 90.1,
    "transaction_date": "2025-02-16 00:00:00",
    "rebate_program_id": "2aea8485-641e-4860-b9c1-81c87ece3609",
    "last_update_time": "2025-01-19 16:55:36",
    "rebate_amount": 72.08
}
```

- include_rebate=false

```
{
    "id": "b1c0eceb-3dbc-41cd-88b7-af0a4fdf14b4",
    "rebate_program_id": "2aea8485-641e-4860-b9c1-81c87ece3609",
    "last_update_time": "2025-01-19 16:55:36",
    "amount": 90.1,
    "transaction_date": "2025-02-16 00:00:00"
}
```

---

### 3. **Rebate Claims**

#### 3.1 Create a New Rebate Claim

- **Endpoint**: `POST /api/v1/rebate-claims`
- **Summary**: Create a new rebate claim.

##### Example Request

```
{
    "transaction_id": "b1c0eceb-3dbc-41cd-88b7-af0a4fdf14b4",
    "claim_amount": "70"
}
```

##### Example Response

- Failure

```
{
    "errors": [
        {
            "message": "A claim with ID aeeda919-4aa5-4513-be53-b957368eceec already exists for transaction ID b1c0eceb-3dbc-41cd-88b7-af0a4fdf14b4."
        }
    ]
}
```

```
{
    "errors": [
        {
            "message": "Claim amount exceeds the allowed limit of 72.08 (80.0% of transaction amount)."
        }
    ]
}
```

- Success

```
{
    "transaction_id": "b1c0eceb-3dbc-41cd-88b7-af0a4fdf14b4",
    "claim_amount": 70.0,
    "claim_date": "2025-01-19 18:08:47",
    "id": "aeeda919-4aa5-4513-be53-b957368eceec",
    "claim_status": "pending",
    "last_update_time": "2025-01-19 18:08:47"
}
```

---

#### 3.2 Get all Rebate Claims

- **Endpoint**: `GET /api/v1/rebate-claims`
- **Summary**: Retrieve all rebate claims.

##### Example Response

```
{
    "aeeda919-4aa5-4513-be53-b957368eceec": {
        "transaction_id": "b1c0eceb-3dbc-41cd-88b7-af0a4fdf14b4",
        "claim_amount": 70.0,
        "claim_date": "2025-01-19 18:08:47",
        "id": "aeeda919-4aa5-4513-be53-b957368eceec",
        "claim_status": "pending",
        "last_update_time": "2025-01-19 18:08:47"
    }
}
```

---

#### 3.3 Get Rebate Claims Summary

- **Endpoint**: `GET /api/v1/rebate-claims/summary`
- **Summary**: Retrieve a summary of rebate claims.

##### Query Parameters

- **`start_date`** *(optional)*: Start date for filtering the claims summary (format: `YYYY-MM-DDTHH:MM:SS`, e.g.: `2025-01-19 16:30:10`).
- **`end_date`** *(optional)*: End date for filtering the claims summary (format: `YYYY-MM-DDTHH:MM:SS`, e.g.: `2025-01-19 20:50:10`).

##### Example Response

```
{
    "total_claims": 2,
    "approved_claims": 0,
    "rejected_claims": 0,
    "pending_claims": 2,
    "approved_claim_amount": 0.0,
    "pending_claim_amount": 110.0
}
```

---
