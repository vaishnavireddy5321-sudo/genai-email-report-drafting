# Document Generation and History API

## Overview

Phase 05 implementation providing JWT-protected endpoints for AI-powered document generation and history retrieval.

## Endpoints

### Generate Email

**POST** `/api/documents/email:generate`

Generate an email draft using AI.

**Authentication:** Required (JWT Bearer token)

**Request Headers:**

- `Authorization: Bearer <token>` (required)
- `X-Request-Id: <correlation-id>` (optional, auto-generated if not provided)

**Request Body:**

```json
{
  "context": "Main content or purpose of the email (required, max 5000 chars)",
  "recipient": "Optional recipient information (max 500 chars)",
  "subject": "Optional subject line (max 500 chars)",
  "tone": "professional|casual|formal|friendly (default: professional)"
}
```

**Response (201 Created):**

```json
{
  "message": "Email generated successfully",
  "document": {
    "id": 1,
    "user_id": 1,
    "doc_type": "email",
    "title": "Subject line if provided",
    "content": "Generated email content...",
    "tone": "professional",
    "created_at": "2024-01-08T12:00:00"
  },
  "request_id": "correlation-id"
}
```

### Generate Report

**POST** `/api/documents/report:generate`

Generate a report draft using AI.

**Authentication:** Required (JWT Bearer token)

**Request Headers:**

- `Authorization: Bearer <token>` (required)
- `X-Request-Id: <correlation-id>` (optional, auto-generated if not provided)

**Request Body:**

```json
{
  "topic": "Main topic or title of the report (required, max 5000 chars)",
  "key_points": "Optional key points or data to include (max 5000 chars)",
  "tone": "professional|casual|formal|friendly (default: professional)",
  "structure": "executive_summary|detailed|bullet_points (default: detailed)"
}
```

**Response (201 Created):**

```json
{
  "message": "Report generated successfully",
  "document": {
    "id": 2,
    "user_id": 1,
    "doc_type": "report",
    "title": "Report topic",
    "content": "Generated report content...",
    "tone": "professional",
    "structure": "detailed",
    "created_at": "2024-01-08T12:00:00"
  },
  "request_id": "correlation-id"
}
```

### Get Document History

**GET** `/api/history`

Retrieve document history for the authenticated user.

**Authentication:** Required (JWT Bearer token)

**Query Parameters:**

- `limit` (optional): Number of results (1-100, default: 50)
- `offset` (optional): Pagination offset (default: 0)
- `doc_type` (optional): Filter by type (`email` or `report`)

**Response (200 OK):**

```json
{
  "documents": [
    {
      "id": 2,
      "doc_type": "report",
      "title": "Report topic",
      "tone": "professional",
      "structure": "detailed",
      "created_at": "2024-01-08T12:00:00",
      "content_preview": "First 200 characters..."
    }
  ],
  "total": 10,
  "limit": 50,
  "offset": 0,
  "has_more": false
}
```

### Get Document Detail

**GET** `/api/history/<document_id>`

Retrieve full details of a specific document.

**Authentication:** Required (JWT Bearer token)

**Response (200 OK):**

```json
{
  "document": {
    "id": 2,
    "user_id": 1,
    "doc_type": "report",
    "title": "Report topic",
    "content": "Full document content...",
    "tone": "professional",
    "structure": "detailed",
    "created_at": "2024-01-08T12:00:00"
  }
}
```

## Request Correlation and Idempotency

### X-Request-Id Header

All endpoints support the `X-Request-Id` header for request correlation and tracing:

- If provided, the value is used as the correlation ID
- If not provided, a UUID is automatically generated
- The correlation ID is:
  - Returned in the response
  - Included in logs via the Gemini service
  - Stored in audit logs as `request_context_id`

**Usage:**

```bash
curl -X POST http://localhost:5000/api/documents/email:generate \
  -H "Authorization: Bearer <token>" \
  -H "X-Request-Id: my-custom-request-id" \
  -H "Content-Type: application/json" \
  -d '{"context": "Test email", "tone": "professional"}'
```

### Idempotency-Key Header (Future Enhancement)

For true idempotency (preventing duplicate document creation on retry), an `Idempotency-Key` header pattern can be implemented:

**Proposed Pattern:**

1. Client generates a unique idempotency key (UUID)
2. Server stores key + response in cache (Redis/database)
3. On duplicate key, return cached response
4. Keys expire after 24 hours

**Implementation Notes:**

- Not included in Phase 05 (minimal implementation as per requirements)
- Can be added later if needed for production resilience
- Would require additional storage for key-response mapping

## Security Features

### User Scoping

- All endpoints enforce user-scoping via JWT authentication
- Users can only access their own documents
- Cross-user data leakage is prevented at query level

### Audit Logging

Every document generation creates an audit log entry with:

- User ID
- Action (`generate_email` or `generate_report`)
- Entity type and ID
- Request correlation ID
- Timestamp

Failed generation attempts are also logged with action `generate_email_failed` or `generate_report_failed`.

## Error Responses

### 400 Bad Request

```json
{
  "error": "context is required"
}
```

### 401 Unauthorized

```json
{
  "error": "Authorization token missing",
  "message": "Please provide a valid token"
}
```

### 404 Not Found

```json
{
  "error": "Document not found"
}
```

### 500 Internal Server Error

```json
{
  "error": "Failed to generate email. Please try again."
}
```

### 503 Service Unavailable

```json
{
  "error": "AI service unavailable"
}
```

## Testing

Run the test suite:

```bash
cd src/backend
source venv/bin/activate
python -m pytest tests/test_documents.py tests/test_history.py -v
```

All tests include:

- Authentication requirements
- Input validation
- Gemini service mocking
- Database persistence verification
- Audit log creation
- User scoping (no cross-user leakage)
- Pagination and filtering
