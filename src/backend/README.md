# Backend - GenAI Email & Report Drafting System

This is the Flask backend for the GenAI Email & Report Drafting System. The system is fully implemented with N-Tier architecture, JWT authentication, Google Gemini AI integration, and comprehensive testing.

## 📁 Structure

```text
src/backend/
├── app.py              # Flask application factory
├── config.py           # Configuration management
├── db.py               # Database initialization
├── models/             # SQLAlchemy models
│   ├── __init__.py
│   ├── user.py         # User model
│   ├── document.py     # Document model
│   └── audit_log.py    # Audit log model
├── tests/              # Test suite
│   ├── conftest.py     # Pytest configuration
│   ├── test_models.py  # Model unit tests
│   └── smoke_test.py   # Smoke test script
├── migrations/         # Alembic migration files (generated)
└── requirements.txt    # Python dependencies
```

## 🔧 Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher
- **Recommended:** [uv](https://github.com/astral-sh/uv) (fast Python package installer)

> **📖 Full Setup Guide**: For complete installation, database setup, and configuration instructions, see [docs/03_setup.md](../../docs/03_setup.md).

## 🚀 Quick Start (Backend)

**1. Install Dependencies & Run:**

```bash
# Navigate to project root if you are in src/backend
cd ../..

# Create virtual environment (at root)
uv venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -r src/backend/requirements.txt --link-mode=copy

# Navigate back to backend directory
cd src/backend

# Run the application
python app.py
```

**2. Verify Environment:**

Ensure your `.env` file is configured (see [docs/03_setup.md](../../docs/03_setup.md#configuration)).

## 🧪 Running Tests

### Run Smoke Test

The smoke test validates basic database operations:

```powershell
python tests/smoke_test.py
```

Expected output:

```text
============================================================
GenAI Email & Report Drafting - Database Smoke Tests
============================================================

[1/6] Creating database tables...
✓ Tables created successfully

[2/6] Creating test user...
✓ User created: <User testuser (USER)>

[3/6] Creating test document...
✓ Document created: <Document 1 (email) by User 1>

[4/6] Creating test audit log...
✓ Audit log created: <AuditLog 1: generate_email by User 1>

[5/6] Querying documents by user...
✓ Found 1 document(s) for user testuser
  - email: Test Email

[6/6] Querying audit logs...
✓ Found 1 audit log(s) for user testuser
  - generate_email on document 1

[Bonus] Testing relationships...
✓ User has 1 document(s)
✓ User has 1 audit log(s)

============================================================
All smoke tests passed! ✓
============================================================
```

### Run Unit Tests with pytest

```powershell
pytest tests/test_models.py -v
```

### Run All Tests with Coverage

```powershell
pytest --cov=. --cov-report=term-missing
```

## 📊 Database Schema

### Users Table

| Column        | Type          | Constraints                  |
|---------------|---------------|------------------------------|
| id            | INTEGER       | PRIMARY KEY                  |
| username      | VARCHAR(100)  | UNIQUE, NOT NULL, INDEXED    |
| email         | VARCHAR(255)  | UNIQUE, NOT NULL, INDEXED    |
| password_hash | VARCHAR(255)  | NOT NULL                     |
| role          | VARCHAR(50)   | NOT NULL, DEFAULT 'USER'     |
| created_at    | TIMESTAMP     | NOT NULL, DEFAULT NOW()      |

### Documents Table

| Column        | Type          | Constraints                  |
|---------------|---------------|------------------------------|
| id            | INTEGER       | PRIMARY KEY                  |
| user_id       | INTEGER       | FK(users.id), NOT NULL, INDEXED |
| doc_type      | VARCHAR(50)   | NOT NULL                     |
| title         | VARCHAR(500)  | NULLABLE                     |
| prompt_input  | TEXT          | NULLABLE                     |
| content       | TEXT          | NOT NULL                     |
| tone          | VARCHAR(50)   | NOT NULL                     |
| structure     | VARCHAR(50)   | NULLABLE                     |
| created_at    | TIMESTAMP     | NOT NULL, DEFAULT NOW(), INDEXED |

**Indexes:**

- `idx_user_created` on (user_id, created_at) for efficient user history queries

### Audit Logs Table

| Column            | Type          | Constraints                  |
|-------------------|---------------|------------------------------|
| id                | INTEGER       | PRIMARY KEY                  |
| user_id           | INTEGER       | FK(users.id), NULLABLE, INDEXED |
| action            | VARCHAR(100)  | NOT NULL                     |
| entity_type       | VARCHAR(50)   | NULLABLE                     |
| entity_id         | INTEGER       | NULLABLE                     |
| request_context_id| VARCHAR(100)  | NULLABLE, INDEXED            |
| details           | TEXT          | NULLABLE                     |
| created_at        | TIMESTAMP     | NOT NULL, DEFAULT NOW(), INDEXED |

**Indexes:**

- `idx_user_created_audit` on (user_id, created_at) for efficient user audit queries
- `idx_action_created` on (action, created_at) for admin audit queries

## 🔐 Security Notes

- **Never commit the `.env` file** - it contains sensitive credentials
- Use strong, unique values for `SECRET_KEY` in production
- Always use environment variables for database credentials
- Password hashes are stored, never plain text passwords
- Consider using parameterized queries (SQLAlchemy handles this)

## 🗂️ Migration Management

### Create a New Migration

```powershell
flask db migrate -m "Description of changes"
```

### Apply Migrations

```powershell
flask db upgrade
```

### Rollback a Migration

```powershell
flask db downgrade
```

### View Migration History

```powershell
flask db history
```

## 🏃 Running the Application

```powershell
python app.py
```

## 📖 API Documentation (Swagger)

The backend serves interactive Swagger UI and the OpenAPI spec:

- Swagger UI: <http://127.0.0.1:5000/api/docs>
- OpenAPI YAML: <http://127.0.0.1:5000/api/openapi.yaml>

Admin-only management is available via Swagger:

- Create admin user: POST /api/admin/users (requires ADMIN JWT)

### Optional: Bootstrap a First Admin (Dev Only)

If you don’t have any admin user yet, you can bootstrap one on startup by setting:

```env
ADMIN_BOOTSTRAP_ENABLED=true
ADMIN_BOOTSTRAP_USERNAME=admin
ADMIN_BOOTSTRAP_EMAIL=admin@example.com
ADMIN_BOOTSTRAP_PASSWORD=ChangeMe123!
```

The bootstrap runs only if no ADMIN exists. After creation, set
`ADMIN_BOOTSTRAP_ENABLED=false`.

You can also hit the root endpoint for quick links:

- <http://127.0.0.1:5000/>

The application will start on `http://localhost:5000`.

Test the health endpoint:

```powershell
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "healthy",
  "message": "GenAI Email & Report Drafting System - Backend API"
}
```

## 🐛 Troubleshooting

### Database Connection Error

If you get a database connection error:

1. Verify PostgreSQL is running
2. Check database credentials in `.env`
3. Ensure database exists: `CREATE DATABASE genai_email_report;`
4. Test connection with psql: `psql -U username -d genai_email_report`

### Import Errors

If you get module import errors:

1. Ensure virtual environment is activated
2. Verify all dependencies are installed:
   - If using uv: `uv pip install -r requirements.txt --link-mode=copy`
   - If using pip: `pip install -r requirements.txt`
3. Check Python path includes the backend directory

### Migration Errors

If migrations fail:

1. Check database connection
2. Ensure migrations directory exists: `flask db init`
3. Review migration files in `migrations/versions/`
4. Drop and recreate database if needed (development only)

## 📝 Development Notes

### Adding New Models

1. Create model file in `models/` directory
2. Import model in `models/__init__.py`
3. Generate migration: `flask db migrate -m "Add new model"`
4. Apply migration: `flask db upgrade`
5. Write tests in `tests/test_models.py`

### Database Access Patterns

The schema is optimized for these common queries:

1. **User Document History:**

   ```python
   Document.query.filter_by(user_id=user_id).order_by(Document.created_at.desc()).all()
   ```

2. **Admin Audit Logs:**

   ```python
   AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
   ```

3. **User-specific Audit Logs:**

   ```python
   AuditLog.query.filter_by(user_id=user_id).order_by(AuditLog.created_at.desc()).all()
   ```

## ✅ Implementation Status

All core features are implemented:

- ✅ Authentication endpoints with JWT and RBAC
- ✅ Google Gemini API integration with prompt engineering
- ✅ Document generation endpoints (email and report)
- ✅ Frontend integration complete
- ✅ Rate limiting and security hardening
- ✅ Comprehensive test coverage (127+ tests)
- ✅ Production-ready deployment configuration

## 🤝 Contributing

See the main repository [CONTRIBUTING.md](../../CONTRIBUTING.md) for contribution guidelines.

## 📄 License

See the main repository [LICENSE](../../LICENSE) file.
