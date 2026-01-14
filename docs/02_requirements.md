# Requirements Specification: N-Tier Enterprise Architecture

**Project:** GenAI Email & Report Drafting System  
**Status:** Planning Phase  
**Current State:** Planning and Design  
**Target State:** N-Tier enterprise architecture with React.js (TypeScript), Flask, and PostgreSQL

---

## Table of Contents

1. [Overview](#overview)
2. [Target Architecture](#target-architecture)
3. [Technology Stack](#technology-stack)
4. [Repository Structure](#repository-structure)
5. [Core API Design](#core-api-design)
6. [User Interface Requirements](#user-interface-requirements)
7. [Database Schema](#database-schema)
8. [Security Requirements](#security-requirements)
9. [Implementation Phases](#implementation-phases)
10. [Code Examples](#code-examples)

---

## Overview

This document specifies the requirements for implementing the GenAI Email & Report Drafting System as an N-Tier enterprise architecture. The target system will implement a React.js with TypeScript frontend, Flask REST API backend, and PostgreSQL database for persistent storage.

### Objectives

- Implement an N-Tier architecture with clear separation of concerns
- Provide a web-based user interface for email and report generation
- Enable multi-user access with JWT authentication and role-based authorization
- Integrate Google Gemini API for AI-powered content generation
- Implement prompt engineering for tone and structure control
- Ensure full auditability and traceability of generated documents
- Support enterprise-grade deployment and scalability

### Key Benefits

- **Separation of Concerns:** Clear UI / API / Data layer boundaries
- **Enterprise-Grade Design:** Industry-standard architecture patterns
- **Scalability:** Support for multiple concurrent users
- **Maintainability:** Modular structure for easy updates
- **Auditability:** Complete audit trails for compliance
- **AI-Powered:** Automated content generation using Google Gemini

---

## Target Architecture

### Three-Tier System

The system will implement a classic three-tier architecture:

```mermaid
---
config:
  layout: elk
---
flowchart TB
classDef presentation fill:#E8F0FE,stroke:#5F8DFF,stroke-width:1px,color:#1F3A5F;
classDef business fill:#E9F7EF,stroke:#3FA796,stroke-width:1px,color:#1E3D34;
classDef data fill:#FFF3E0,stroke:#F4A261,stroke-width:1px,color:#5A3E1B;
classDef ai fill:#F3E5F5,stroke:#9C27B0,stroke-width:1px,color:#4A148C;
subgraph Presentation["Presentation Layer (React.js with TypeScript UI)"]
    Login["Login/Register"]
    EmailForm["Email Generation Form"]
    ReportForm["Report Generation Form"]
    History["Document History"]
    Admin["Admin Dashboard"]
end
class Login,EmailForm,ReportForm,History,Admin presentation
subgraph Business["Business Layer (Flask API)"]
    Auth["Authentication"]
    Prompt["Prompt Engine"]
    Gemini["Gemini API Client"]
    Validation["Validation"]
    Logging["Audit Logging"]
end
class Auth,Prompt,Gemini,Validation,Logging business
subgraph Data["Data Layer (PostgreSQL)"]
    Users[("Users")]
    Documents[("Generated Documents")]
    Logs[("Audit Logs")]
end
class Users,Documents,Logs data
subgraph AI["AI Service Layer (Google Gemini)"]
    LLM["Gemini LLM"]
end
class LLM ai
Presentation -- REST API --> Business
Business -- ORM / SQL --> Data
Business -- API Calls --> AI
AI -- Generated Content --> Business
```

*Note: If the Mermaid diagram above doesn't render, see the ASCII fallback below:*

```text
┌───────────────────┐
│   React.js (TypeScript) UI     │  (Presentation Layer)
│───────────────────│
│ Login/Register    │
│ Email Generation  │
│ Report Generation │
│ Document History  │
│ Admin Dashboard   │
└────────▲──────────┘
         │ REST API
┌────────┴──────────┐
│   Flask API       │  (Business Layer)
│───────────────────│
│ Authentication    │
│ Prompt Engine     │
│ Gemini API Client │
│ Validation        │
│ Audit logging     │
└────────▲──────────┘
         │ ORM / SQL
┌────────┴──────────┐
│   PostgreSQL      │  (Data Layer)
│───────────────────│
│ Users             │
│ Generated Docs    │
│ Audit logs        │
└───────────────────┘
         │
┌────────┴──────────┐
│  Google Gemini    │  (AI Service Layer)
│───────────────────│
│ LLM Generation    │
└───────────────────┘
```

### Architecture Principles

- **Separation of Concerns:** Each layer has distinct responsibilities
- **AI Integration:** Seamless integration with Google Gemini API
- **Prompt Engineering:** Structured prompts for consistent output quality
- **Security First:** JWT authentication and role-based access control
- **Auditability by Design:** Every generated document is traceable
- **Scalability:** Support for multiple concurrent users

---

## Technology Stack

### Frontend (Presentation Layer)

#### React.js with TypeScript

**Purpose:** Modern, type-safe, component-based user interface

**Key Features:**

- User registration and login interface
- Email generation form with tone and context inputs
- Report generation form with structure options
- Document history view with search and filtering
- Admin dashboard for system management
- Responsive design for various screen sizes

**Optional Enhancements:**

- Material UI or Ant Design for professional styling
- Real-time generation status updates
- Export functionality (PDF, Email)
- Template library for common document types

### Backend (Business Layer)

#### Python Flask

**Purpose:** Lightweight web framework for REST API

**Rationale:**

- Explicit and maintainable code structure
- Clean REST endpoint design
- Easy integration with Google Gemini API
- Easy to extend and customize

**Key Libraries:**

| Library | Purpose |
|---------|---------|
| `flask` | Web framework |
| `flask-cors` | Cross-origin resource sharing |
| `flask-sqlalchemy` | ORM for database operations |
| `flask-jwt-extended` | JWT-based authentication |
| `google-generativeai` | Google Gemini API client |
| `bcrypt` or `werkzeug` | Password hashing |

### Data Store (Persistence Layer)

#### PostgreSQL

**Purpose:** Production-grade relational database for enterprise deployments

**Advantages:**

- Better concurrency support
- Advanced features and performance
- Industry-standard for production systems
- Full ACID compliance
- Robust support for text storage (generated documents)
- Excellent for audit logging and history tracking

---

## Repository Structure

For complete repository structure details, see [Repository Structure Documentation](07_repository_structure.md).

**Overview:**

- `frontend/` - React.js with TypeScript application
- `backend/` - Flask REST API with routes, services, and models
- `database/` - PostgreSQL schema and migrations
- `docs/` - Project documentation including this requirements document

---

## Core API Design

### Authentication

#### Register User

```http
POST /api/auth/register
Content-Type: application/json

Request:
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "USER"
}

Response:
{
  "message": "User registered successfully",
  "user_id": 1
}
```

#### Login

```http
POST /api/auth/login
Content-Type: application/json

Request:
{
  "email": "john@example.com",
  "password": "securepassword"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "USER"
  }
}
```

### Document Generation

#### Generate Email

```http
POST /api/documents/generate-email
Authorization: Bearer {jwt_token}
Content-Type: application/json

Request:
{
  "purpose": "Follow-up on meeting",
  "tone": "professional",
  "context": "Meeting with client about project timeline",
  "recipient": "client@example.com"
}

Response:
{
  "document_id": 1,
  "doc_type": "email",
  "generated_text": "Dear [Recipient],\n\nI hope this email finds you well...",
  "created_at": "2026-01-08T10:00:00Z"
}
```

#### Generate Report

```http
POST /api/documents/generate-report
Authorization: Bearer {jwt_token}
Content-Type: application/json

Request:
{
  "purpose": "Quarterly project status",
  "tone": "formal",
  "context": "Q1 2026 project progress, milestones achieved, challenges faced",
  "structure": "executive_summary"
}

Response:
{
  "document_id": 2,
  "doc_type": "report",
  "generated_text": "# Quarterly Project Status Report\n\n## Executive Summary\n...",
  "created_at": "2026-01-08T10:15:00Z"
}
```

### History Retrieval

#### Get User Documents

```http
GET /api/documents/history
Authorization: Bearer {jwt_token}

Query Parameters:
- doc_type: "email" | "report" (optional)
- limit: number (optional, default: 50)
- offset: number (optional, default: 0)

Response:
{
  "documents": [
    {
      "id": 1,
      "doc_type": "email",
      "tone": "professional",
      "input_context": "Meeting follow-up",
      "created_at": "2026-01-08T10:00:00Z"
    },
    ...
  ],
  "total": 25,
  "limit": 50,
  "offset": 0
}
```

#### Get Document by ID

```http
GET /api/documents/{document_id}
Authorization: Bearer {jwt_token}

Response:
{
  "id": 1,
  "user_id": 1,
  "doc_type": "email",
  "tone": "professional",
  "input_context": "Meeting follow-up",
  "output_text": "Dear [Recipient],\n\n...",
  "created_at": "2026-01-08T10:00:00Z"
}
```

### Admin Operations

#### Get All Documents (Admin Only)

```http
GET /api/admin/documents
Authorization: Bearer {jwt_token}
Headers: { "role": "ADMIN" }

Query Parameters:
- user_id: number (optional, filter by user)
- doc_type: "email" | "report" (optional)
- limit: number (optional)
- offset: number (optional)

Response:
{
  "documents": [...],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

#### Get System Usage Stats (Admin Only)

```http
GET /api/admin/stats
Authorization: Bearer {jwt_token}
Headers: { "role": "ADMIN" }

Response:
{
  "total_users": 25,
  "total_documents": 150,
  "emails_generated": 100,
  "reports_generated": 50,
  "most_used_tone": "professional"
}
```

---

## User Interface Requirements

### Screen 1: Login / Register

**Purpose:** User authentication and registration

**Components:**

- Email input field
- Password input field
- Login button
- Register link/button
- Error message display
- Role selection (for registration, default: USER)

**User Flow:**

1. User enters email and password
2. User clicks "Login" or "Register"
3. System validates credentials
4. JWT token stored in localStorage
5. User redirected to dashboard

**Features:**

- JWT token storage
- Role-based UI customization
- Session management
- Password strength indicator (for registration)

### Screen 2: Email Generation

**Purpose:** Generate professional emails using AI

**Components:**

- Purpose input field (text area)
- Tone selector (dropdown: professional, casual, formal, friendly)
- Context input field (text area)
- Recipient email field (optional)
- Generate button
- Generated email display area
- Copy to clipboard button
- Save button
- Loading indicator

**User Flow:**

1. User enters purpose, tone, and context
2. User clicks "Generate"
3. System shows loading indicator
4. Generated email displayed
5. User can copy, save, or regenerate

**Features:**

- Real-time generation status
- Regenerate option
- Copy to clipboard
- Save to history

### Screen 3: Report Generation

**Purpose:** Generate professional reports using AI

**Components:**

- Purpose input field (text area)
- Tone selector (dropdown)
- Context input field (text area)
- Structure selector (dropdown: executive_summary, detailed, bullet_points)
- Generate button
- Generated report display area (with markdown rendering)
- Copy to clipboard button
- Export as PDF button (optional)
- Save button

**User Flow:**

1. User enters purpose, tone, context, and structure
2. User clicks "Generate"
3. System shows loading indicator
4. Generated report displayed (formatted)
5. User can copy, export, save, or regenerate

**Features:**

- Markdown rendering for reports
- Export functionality
- Regenerate option
- Save to history

### Screen 4: Document History

**Purpose:** View previously generated documents

**Components:**

- Document list table with columns:
  - Type (Email/Report)
  - Purpose/Context (truncated)
  - Tone
  - Created Date
  - Actions (View, Delete)
- Filter by document type
- Search functionality
- Pagination
- View document modal/detail page

**Features:**

- Sortable columns
- Filter by type and date range
- Search by purpose/context
- View full document
- Delete documents (own documents only)

### Screen 5: Admin Dashboard (Admin Only)

**Purpose:** System administration and monitoring

**Components:**

- System statistics cards:
  - Total users
  - Total documents generated
  - Emails vs Reports breakdown
  - Most used tones
- All documents table (with user information)
- User management section (optional)
- Usage analytics charts (optional)

**Features:**

- View all documents across all users
- System usage statistics
- Read-only access to system data

---

## Database Schema

### Users Table

Stores user authentication and authorization information.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Role Values:**

- `USER`: Can generate emails and reports, view own history
- `ADMIN`: All User permissions plus view all documents and system stats

### Generated Documents Table

Stores AI-generated emails and reports with metadata.

```sql
CREATE TABLE generated_documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    doc_type VARCHAR(50) NOT NULL,  -- 'email' or 'report'
    tone VARCHAR(50) NOT NULL,       -- 'professional', 'casual', 'formal', 'friendly'
    input_context TEXT NOT NULL,      -- User-provided context
    output_text TEXT NOT NULL,       -- AI-generated content
    structure VARCHAR(50),           -- For reports: 'executive_summary', 'detailed', 'bullet_points'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Document Types:**

- `email`: Generated email content
- `report`: Generated report content

**Tone Values:**

- `professional`: Business-appropriate tone
- `casual`: Informal, friendly tone
- `formal`: Very formal, official tone
- `friendly`: Warm, approachable tone

### Audit Logs Table (Optional)

Stores detailed audit information for compliance and debugging.

```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL,     -- 'created', 'viewed', 'deleted'
    user_id INTEGER NOT NULL,
    metadata JSONB,                  -- Additional context
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(document_id) REFERENCES generated_documents(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Action Values:**

- `created`: Document was generated
- `viewed`: Document was accessed
- `deleted`: Document was removed

---

## Security Requirements

### Security Authentication

For complete authentication and authorization documentation, see [Authentication & Authorization Guide](08_authentication_authorization.md).

**Quick Overview:**

- **JWT-Based Authentication:** Secure token-based authentication
- **Password Hashing:** Passwords stored as hashed values (werkzeug.security)
- **Token Expiration:** Access tokens expire after configured duration
- **Role-Based Access Control:** Admin and User roles with differentiated permissions
- **Endpoint Protection:** All business-critical APIs protected by JWT

### Data Security

- **Input Validation:** All user inputs validated before processing
- **API Key Security:** Google Gemini API key stored securely (environment variables)
- **SQL Injection Prevention:** ORM-based queries prevent SQL injection
- **Error Handling:** No sensitive information exposed in error messages
- **Rate Limiting:** Prevent API abuse and excessive Gemini API calls

---

## Implementation Phases

### Phase 1: Backend API (Flask)

**Duration:** 2-3 weeks

**Tasks:**

1. Set up Flask application structure
2. Create database models and schema (PostgreSQL)
3. Implement REST API endpoints
4. Add authentication (JWT)
5. Implement role-based access control
6. Integrate Google Gemini API
7. Implement prompt engineering logic
8. Add document persistence and history

**Deliverables:**

- Functional Flask REST API
- Database schema and models
- Authentication system
- Gemini API integration
- Document generation endpoints

### Phase 2: Frontend (React with TypeScript)

**Duration:** 2-3 weeks

**Tasks:**

1. Set up React application with TypeScript
2. Configure TypeScript compiler and type definitions
3. Create login/register components with TypeScript types
4. Build email generation form with type safety
5. Build report generation form with type safety
6. Implement document history view
7. Add authentication UI with typed API client
8. Implement role-based UI restrictions
9. Add admin dashboard (if admin role)

**Deliverables:**

- Functional React frontend with TypeScript
- Type-safe user interface
- Typed API integration
- Authentication UI with type checking
- Document generation interfaces with full type safety

### Phase 3: Integration & Polish

**Duration:** 1-2 weeks

**Tasks:**

1. Connect frontend to backend APIs
2. Add error handling and validation
3. Implement loading states and progress indicators
4. Performance optimization
5. UI/UX improvements
6. Comprehensive testing

**Deliverables:**

- Fully integrated system
- Error handling
- Performance optimizations
- Test coverage

### Phase 4: Deployment (Optional)

**Duration:** 1 week

**Tasks:**

1. Docker containerization
2. Docker Compose setup
3. Production configuration
4. Documentation updates
5. Deployment guides

**Deliverables:**

- Dockerized application
- Deployment documentation
- Production-ready configuration

---

## Code Examples

### Backend: Flask Application Structure

#### `backend/app.py`

```python
from flask import Flask
from flask_cors import CORS
from db import db
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.documents import documents_bp
from routes.history import history_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(documents_bp, url_prefix="/api/documents")
    app.register_blueprint(history_bp, url_prefix="/api/documents")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

#### `backend/config.py`

```python
import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/genai_email_report")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "replace-with-environment-variable")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
```

#### `backend/models/document.py`

```python
from db import db
from datetime import datetime

class GeneratedDocument(db.Model):
    __tablename__ = "generated_documents"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)  # 'email' or 'report'
    tone = db.Column(db.String(50), nullable=False)
    input_context = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text, nullable=False)
    structure = db.Column(db.String(50), nullable=True)  # For reports
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "doc_type": self.doc_type,
            "tone": self.tone,
            "input_context": self.input_context,
            "output_text": self.output_text,
            "structure": self.structure,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
```

### Frontend: React Component Examples

#### `frontend/src/api/apiClient.ts`

```typescript
const BASE_URL = "http://localhost:5000/api";

function authHeaders() {
  const token = localStorage.getItem("token");
  return {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  };
}

export async function generateEmail(purpose: string, tone: string, context: string) {
  const res = await fetch(`${BASE_URL}/documents/generate-email`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ purpose, tone, context })
  });
  return res.json();
}

export async function generateReport(purpose: string, tone: string, context: string, structure: string) {
  const res = await fetch(`${BASE_URL}/documents/generate-report`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ purpose, tone, context, structure })
  });
  return res.json();
}

export async function getDocumentHistory(docType?: string) {
  const params = docType ? `?doc_type=${docType}` : "";
  const res = await fetch(`${BASE_URL}/documents/history${params}`, {
    headers: authHeaders()
  });
  return res.json();
}

export async function login(email: string, password: string) {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  return res.json();
}
```

#### `frontend/src/pages/EmailGenerator.tsx`

```tsx
import { useState } from "react";
import { generateEmail } from "../api/apiClient";

interface EmailFormData {
  purpose: string;
  tone: string;
  context: string;
}

export default function EmailGenerator() {
  const [formData, setFormData] = useState<EmailFormData>({
    purpose: "",
    tone: "professional",
    context: ""
  });
  const [loading, setLoading] = useState(false);
  const [generatedEmail, setGeneratedEmail] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await generateEmail(
        formData.purpose,
        formData.tone,
        formData.context
      );
      setGeneratedEmail(result.generated_text);
    } catch (error) {
      console.error("Error generating email:", error);
      alert("Failed to generate email. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Purpose:</label>
          <textarea
            value={formData.purpose}
            onChange={(e) => setFormData({ ...formData, purpose: e.target.value })}
            required
          />
        </div>
        <div>
          <label>Tone:</label>
          <select
            value={formData.tone}
            onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
          >
            <option value="professional">Professional</option>
            <option value="casual">Casual</option>
            <option value="formal">Formal</option>
            <option value="friendly">Friendly</option>
          </select>
        </div>
        <div>
          <label>Context:</label>
          <textarea
            value={formData.context}
            onChange={(e) => setFormData({ ...formData, context: e.target.value })}
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Email"}
        </button>
      </form>
      {generatedEmail && (
        <div>
          <h3>Generated Email:</h3>
          <pre>{generatedEmail}</pre>
        </div>
      )}
    </div>
  );
}
```

---

## Success Criteria

The N-Tier system will be considered complete when:

- ✅ User registration and authentication working
- ✅ Email generation functional
- ✅ Report generation functional
- ✅ JWT authentication working
- ✅ Role-based access control implemented
- ✅ Document history functional
- ✅ Admin dashboard operational
- ✅ Database persistence operational
- ✅ API documentation complete
- ✅ Deployment ready (Docker optional)
- ✅ Comprehensive test coverage
- ✅ Production-ready error handling

---

## Implementation Strategy

The system will be built from scratch following best practices:

1. **Backend First:** Build Flask API with authentication and Gemini integration
2. **Database Setup:** Create PostgreSQL schema and models
3. **Frontend Development:** Build React with TypeScript UI components
4. **Integration:** Connect frontend to backend APIs
5. **Testing & Polish:** Comprehensive testing and refinement

---

## References

- [Architecture Planning Document](05_architecture_plan.md) - Detailed architecture specifications
- [Technical Documentation](04_technical.md) - Technical implementation details
- [Usage Guide](03_usage.md) - System usage guide

---

**Document Version:** 1.0  
**Last Updated:** January 7, 2026  
**Status:** Planning Phase
