# Setup Guide: GenAI Email & Report Drafting System

**Project:** GenAI Email & Report Drafting System  
**Purpose:** Complete installation and configuration guide  

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Database Setup](#database-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Testing](#testing)

---

## Prerequisites

Before setting up the system, ensure you have the following installed:

- **Node.js** (v16 or higher) for frontend
- **TypeScript** (v4.5 or higher) for type checking
- **Python 3.8+** for backend
- **PostgreSQL database** - Choose one:
  - Docker or Podman with Compose (recommended for development)
  - Local PostgreSQL installation (v13+ recommended)
- **Google Gemini API key** (required for AI content generation)

---

## Installation

### Backend Setup

You have two options for setting up the Python backend:

#### Option 1: Using `uv` (Recommended - Faster)

`uv` is a modern Python package installer that's significantly faster than pip:

```powershell
# Install uv first (one-time setup)
# Windows (PowerShell):
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm https://astral.sh/uv/install.ps1 | iex

$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"

# Create virtual environment at root
uv venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate

# Navigate to backend directory
cd src/backend

# Install dependencies
uv pip install -r requirements.txt --link-mode=copy
```

#### Option 2: Using Traditional pip/venv

```powershell
# Create virtual environment at root
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r src/backend/requirements.txt

# Navigate to backend directory
cd src/backend
```

### Frontend Setup

```powershell
# Navigate to frontend directory
cd src/frontend

# Install dependencies (includes TypeScript)
npm install

# TypeScript will be included in the dependencies
# Verify TypeScript installation
npx tsc --version
```

---

## Database Setup

You have two options for setting up PostgreSQL:

### Option 1: Using Docker or Podman Compose (Recommended)

Docker/Podman Compose provides a consistent local development environment with minimal setup.
If you are using Podman, replace `docker compose` with `podman compose` in the commands below.

```powershell
# 1. Copy the environment file (from infra directory)
cp infra/.env.example infra/.env

# 2. (Optional) Edit infra/.env to customize database credentials
# Default values: POSTGRES_USER=postgres, POSTGRES_PASSWORD=postgres, POSTGRES_DB=genai_email_report

# 3. Navigate to infra directory
cd infra

# 4. Start PostgreSQL service
docker compose up -d

# 5. Check service health
docker compose ps

# 6. View logs (optional)
docker compose logs postgres

# The database schema (infra/database/schema.sql) will be automatically initialized
```

#### Managing the Docker/Podman Compose Environment

```powershell
# Navigate to infra directory
cd infra

# Stop services
docker compose down

# Stop and remove data (WARNING: destroys all data)
docker compose down -v

# View service status
docker compose ps

# Access PostgreSQL CLI (optional)
docker compose exec postgres psql -U postgres -d genai_email_report
```

#### Alternative: Run from Repository Root

```powershell
# From repository root
docker compose -f infra/docker-compose.yml up -d
docker compose -f infra/docker-compose.yml down
docker compose -f infra/docker-compose.yml ps
```

#### Connect Backend to Docker/Podman Compose PostgreSQL

Update your `src/backend/.env` file with:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/genai_email_report
```

(Adjust username/password if you customized them in `infra/.env`)

### Option 2: Using Local PostgreSQL Installation

If you prefer a local PostgreSQL installation:

```sql
-- Create database
CREATE DATABASE genai_email_report;

-- Run schema migration
-- (Schema will be created automatically via Flask-SQLAlchemy on first run)
-- Or manually run: psql -U postgres -d genai_email_report -f infra/database/schema.sql
```

---

## Configuration

### Backend Configuration

Create a `.env` file in the `src/backend/` directory (or copy from `src/backend/.env.example`):

```env
FLASK_APP=app.py
FLASK_ENV=development

# If using Docker/Podman Compose PostgreSQL:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/genai_email_report

# If using local PostgreSQL installation:
# DATABASE_URL=postgresql://user:password@localhost:5432/genai_email_report

JWT_SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-google-gemini-api-key
```

**Note:** See `src/backend/.env.example` for complete configuration options including SQLAlchemy settings, JWT configuration, and Gemini API parameters.

**Important Configuration Variables:**

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT token signing | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `FLASK_ENV` | Environment (development/production) | No (defaults to development) |

**Optional Admin Bootstrap (first-time setup):**

If you want the backend to create a single ADMIN user automatically on startup
(only when no ADMIN exists), set these in `src/backend/.env`:

```env
ADMIN_BOOTSTRAP_ENABLED=true
ADMIN_BOOTSTRAP_USERNAME=admin
ADMIN_BOOTSTRAP_EMAIL=admin@example.com
ADMIN_BOOTSTRAP_PASSWORD=ChangeMe123!
```

After the admin is created, disable the bootstrap by setting `ADMIN_BOOTSTRAP_ENABLED=false`.

### Frontend Configuration

Create a `.env` file in the `src/frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

---

## Running the Application

### Start Backend Server

```powershell
# Activate virtual environment (from project root)
.venv\Scripts\Activate.ps1

# Navigate to backend directory
cd src/backend

# Start Flask server
python app.py
```

Backend will run on `http://localhost:5000`

API docs:

- Swagger UI: `http://localhost:5000/api/docs`
- OpenAPI YAML: `http://localhost:5000/api/openapi.yaml`

### Start Frontend Development Server

```powershell
# Navigate to frontend directory
cd src/frontend

# Start Vite development server
npm run dev
```

Frontend will run on `http://localhost:5173` (or similar port - check console output)

### Access the Application

1. Open your browser and navigate to the frontend URL (e.g., `http://localhost:5173`)
2. You should see the login page
3. Register a new account or login with existing credentials
4. Start using the application!

---

## Troubleshooting

### Issue: Backend Won't Start

**Symptoms:** Error when running `python app.py`

**Solutions:**

1. **Check virtual environment is activated:**

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. **Verify database connection:**
   - If using Docker/Podman Compose: Run `docker compose ps` (or `podman compose ps`) from the infra/ directory to ensure PostgreSQL is healthy
   - If using local PostgreSQL: Ensure PostgreSQL service is running
   - Check `DATABASE_URL` in `src/backend/.env` file
   - Verify database exists
   - For Docker/Podman Compose: Test connection with `docker compose exec postgres psql -U postgres -d genai_email_report` (or `podman compose exec postgres psql -U postgres -d genai_email_report`)

3. **Check API key:**
   - Ensure `GEMINI_API_KEY` is set in `.env`
   - Verify the key is valid and active

4. **Check dependencies:**

   ```powershell
   # If using uv (from project root):
   uv pip install -r src/backend/requirements.txt --link-mode=copy
   # If using pip (from project root):
   pip install -r src/backend/requirements.txt
   ```

5. **Review error messages:** Check the console output for specific error messages

### Issue: Frontend Can't Connect to Backend

**Symptoms:** API calls failing, CORS errors, network errors

**Solutions:**

1. **Verify backend is running** on `http://localhost:5000`
   - Check the terminal where backend is running
   - Try accessing `http://localhost:5000/health` in your browser

2. **Check `VITE_API_BASE_URL`** in frontend `.env`
   - Should be `http://localhost:5000/api`
   - Restart frontend dev server after changing .env

3. **Verify CORS is enabled** in Flask backend (should be configured by default)

4. **Check firewall settings** that might block localhost connections

### Issue: Authentication Not Working

**Symptoms:** Can't login, JWT errors, unauthorized errors

**Solutions:**

1. **Check `JWT_SECRET_KEY`** is set in backend `.env`
2. **Clear browser localStorage** and try again:
   - Open browser DevTools (F12)
   - Go to Application → Local Storage
   - Clear all entries
   - Try logging in again

3. **Verify password hashing** is working correctly (check backend logs)

4. **Check database connection** - ensure users table exists

### Issue: Gemini API Errors

**Symptoms:** Document generation fails, API errors, timeout errors

**Solutions:**

1. **Verify `GEMINI_API_KEY`** is correct and active
   - Check Google Cloud Console
   - Ensure API is enabled

2. **Check API quota/limits** in Google Cloud Console
   - Verify you haven't exceeded rate limits
   - Check billing status

3. **Review error messages** in backend logs
   - Run backend in debug mode
   - Check specific error details

4. **Ensure internet connection** is stable

### Issue: Docker/Podman Compose PostgreSQL Issues

**Symptoms:** Docker/Podman Compose won't start, connection refused, data not persisting

**Solutions:**

1. **Service won't start:**

   ```powershell
   # Check Docker or Podman is running
   docker --version
   docker compose version
   # Or Podman
   podman --version
   podman compose version
   
   # Navigate to infra directory
   cd infra
   
   # View detailed logs
   docker compose logs postgres
   # Or Podman
   podman compose logs postgres
   
   # Restart services
   docker compose down
   docker compose up -d
   # Or Podman
   podman compose down
   podman compose up -d
   ```

2. **Connection refused from backend:**
   - Navigate to `infra/` directory first: `cd infra`
   - Verify PostgreSQL is healthy: `docker compose ps` (or `podman compose ps`) should show "healthy"
   - Check port mapping: Ensure port 5432 is not already in use
   - Verify `DATABASE_URL` uses `localhost:5432` in `src/backend/.env`
   - On Linux: Use `host.docker.internal` if connecting from another container

3. **Data not persisting:**
   - Ensure you're not using `docker compose down -v` (or `podman compose down -v`) which deletes volumes
   - Check volume exists: `docker volume ls | grep genai_email_report_data`
   - Use `docker compose down` (or `podman compose down`) without `-v` to preserve data

4. **Health check failing:**
   - Wait 10-15 seconds after starting for health check to pass
   - Check credentials match in `infra/.env` and `src/backend/.env`
   - View logs: `cd infra && docker compose logs postgres` (or `podman compose logs postgres`)

5. **Port already in use:**
   - Check if another PostgreSQL instance is running on port 5432
   - Stop the conflicting service or change the port in `docker-compose.yml`

### Issue: TypeScript Errors in Frontend

**Symptoms:** TypeScript compilation errors, type mismatches

**Solutions:**

1. **Reinstall dependencies:**

   ```powershell
   cd src/frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Check TypeScript version:**

   ```powershell
   npx tsc --version
   ```

3. **Verify tsconfig.json** is properly configured

### Issue: Python Import Errors

**Symptoms:** ModuleNotFoundError, import errors

**Solutions:**

1. **Verify virtual environment is activated**
2. **Reinstall dependencies:**

   ```powershell
   # From project root
   uv pip install -r src/backend/requirements.txt --link-mode=copy
   # OR using pip from src/backend/
   pip install -r requirements.txt
   ```

3. **Check Python version:**

   ```powershell
   python --version
   ```

4. **Ensure you're in the correct directory** (src/backend/)

---

## Testing

### Backend Testing

**Run backend tests:**

```powershell
# Activate virtual environment (from project root)
.venv\Scripts\Activate.ps1

# Navigate to backend directory
cd src/backend

# Run all tests
python -m pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test file
pytest tests/test_auth.py
```

**Run with coverage:**

```powershell
# Generate coverage report
pytest --cov=. --cov-report=html tests/

# View HTML coverage report
# Open htmlcov/index.html in your browser
```

**Available Test Files:**

- `test_models.py` - Database model tests
- `test_auth.py` - Authentication endpoint tests
- `test_documents.py` - Document generation tests
- `test_history.py` - History retrieval tests
- `test_admin.py` - Admin endpoint tests
- `test_gemini_service.py` - Gemini API integration tests
- `test_prompt_engine.py` - Prompt construction tests

### Frontend Testing

**Run frontend tests:**

```powershell
# Navigate to frontend directory
cd src/frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Integration Testing

Test the full stack:

1. Start Docker/Podman Compose PostgreSQL (if using)
2. Start backend server
3. Start frontend dev server
4. Run end-to-end tests (if configured)

**Manual Integration Test:**

1. Navigate to frontend URL
2. Register a new user
3. Login with credentials
4. Generate an email
5. Generate a report
6. View document history
7. Test admin features (if admin user)

---

## Next Steps

Once setup is complete:

1. **Explore the codebase** in `src/backend/` and `src/frontend/`
2. **Review the [Main README](../README.md)** for project overview.

---

## Additional Resources

- [Main README](../README.md) - Project overview
- [Abstract](01_abstract.md) - Project abstract
- [Key Features](02_key-features.md) - Key features breakdown

---

**Document Version:** 1.0  
**Last Updated:** January 13, 2026  
**Status:** Complete
