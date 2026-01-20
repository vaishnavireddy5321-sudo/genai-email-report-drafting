# GenAI Email & Report Drafting System

[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-success)](https://github.com/Srivari-Hema-SSPL-2026/genai-email-report-drafting)
[![Architecture](https://img.shields.io/badge/Architecture-N--Tier-FF6B35)](docs/06_architecture_plan.md)
[![Python](https://img.shields.io/badge/Python-3.12.10-ABCDEF?logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-pink?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Flask](https://img.shields.io/badge/Flask-3.x-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%2B-brown?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-yellow?logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![Maintainer](https://img.shields.io/badge/Maintainer-Viswanatha%20Swamy%20P%20K-blue)](https://github.com/Srivari-Hema-SSPL-2026)

An AI-driven application that generates professional emails and reports using `Google Gemini`, built with an `N-Tier enterprise architecture` comprising `React.js with TypeScript`, `Flask`, and `PostgreSQL`, with `JWT-based authentication and role-based access control`.

---

## CI Status

[![Python CI](https://github.com/Srivari-Hema-SSPL-2026/genai-email-report-drafting/actions/workflows/ci-python.yml/badge.svg)](https://github.com/Srivari-Hema-SSPL-2026/genai-email-report-drafting/actions/workflows/ci-python.yml)
[![Frontend CI](https://github.com/Srivari-Hema-SSPL-2026/genai-email-report-drafting/actions/workflows/ci-frontend.yml/badge.svg)](https://github.com/Srivari-Hema-SSPL-2026/genai-email-report-drafting/actions/workflows/ci-frontend.yml)

---

## 📑 Table of Contents

- [Abstract](#-abstract)
- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Repository Structure](#-repository-structure)
- [Quick Start](#-quick-start)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 📌 Abstract

Professional communication through emails and reports is a time-consuming and repetitive activity in corporate and academic environments. This project presents an `AI-Driven Email and Report Drafting System` that leverages `Generative Artificial Intelligence (GenAI)` using `Google Gemini Large Language Models` to automatically generate high-quality, context-aware written content.

The project successfully demonstrates the practical application of Generative AI within a secure, enterprise-style architecture. By balancing simplicity and architectural rigor, the system provides a strong academic foundation while remaining extensible for real-world deployment scenarios.

> 📖 **For the complete abstract (single source of truth), see [docs/01_abstract.md](docs/01_abstract.md).**

---

## 🎯 Problem Statement

Effective written communication plays a critical role in professional workflows. However, several challenges exist in the current approach to drafting professional emails and reports:

- Time Consumption: Manual drafting of emails and reports consumes significant time that could be better utilized for other tasks
- Consistency Challenges: Maintaining consistent tone and structure across multiple documents is challenging, especially when working under time constraints
- Security Gaps: Many AI-powered tools lack proper secure access control and data persistence, making them unsuitable for enterprise environments
- Architectural Limitations: Most small-scale AI tools ignore enterprise architectural principles, making them difficult to scale and maintain
- Quality Variability: Output quality often depends heavily on the writer's skill level and available time, leading to inconsistent results

This project addresses these challenges by providing a secure, enterprise-grade solution that automates content generation while maintaining professional standards and architectural best practices.

---

## 🎯 Key Features

> **✨ Feature Highlights**: For a detailed breakdown of all system features, see [Key Features Documentation](docs/02_key-features.md).

- **AI-Powered Content Generation**: Professional emails and reports using Google Gemini
- **Enterprise Architecture**: N-Tier design with clear separation of concerns
- **Security & RBAC**: JWT authentication, secure password hashing, and role-based access
- **Comprehensive Persistence**: PostgreSQL with full audit logging and history tracking
- **Production Readiness**: Thorough testing, error handling, and scalable design

---

## 🏗️ System Architecture

### High-Level Architecture Diagram

![High-Level Architecture Diagram](docs/diagrams/system-architecture-simple.png)

### Detailed Architecture Diagram

![Detailed Architecture Diagram](docs/diagrams/system-architecture.png)

### Architecture Layers

- **Presentation Layer**: React.js with TypeScript SPA for user interaction
- **Application Layer**: Flask REST API handling business logic and security
- **Data Layer**: PostgreSQL for persistent storage
- **AI Service Layer**: Google Gemini for text generation

---

## 🧰 Technology Stack

| Layer | Technology |
|-----|-----------|
| Frontend | React.js with TypeScript |
| Backend | Python (Flask) |
| Database | PostgreSQL |
| Authentication | JWT |
| AI Model | Google Gemini |
| Version Control | GitHub |

---

## 📂 Repository Structure

The project is organized into layers following the N-Tier architecture pattern:

| Directory | Layer | Description |
|-----------|-------|-------------|
| `src/frontend/` | **Presentation** | React.js application (Coming in Module 3) |
| `src/backend/` | **Application** | Flask REST API (Coming in Module 2) |
| `infra/database/` | **Data** | PostgreSQL database schema and migrations |
| `infra/` | **Infrastructure** | Docker Compose configuration for local development |
| `docs/` | **Documentation** | Project guides, architecture diagrams, and requirements |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12.10
- Node.js 18+
- PostgreSQL 13+ (Docker/Podman Compose recommended)
- Google Gemini API key

**For complete setup guide with detailed instructions, see [Setup Guide](docs/03_setup.md).**

### Quick Setup

```powershell
# 1. Start PostgreSQL (Docker/Podman Compose - recommended)
cd infra
docker compose up -d
podman compose up -d

# 2. Setup Backend
# Navigate back to root
cd ..

# Create and activate virtual environment at root
uv venv
.venv\Scripts\Activate.ps1

# Navigate to backend directory
cd src/backend

# Install dependencies
uv pip install -r requirements.txt --link-mode=copy

# Set environment variables
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/genai_email_report"
$env:GEMINI_API_KEY = "your-api-key"
$env:JWT_SECRET_KEY = "your-secret-key"

python app.py  # Backend runs on http://localhost:5000

# 3. Setup Frontend (new terminal)
cd src/frontend
npm install
npm run dev  # Frontend runs on http://localhost:5173
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

This project is intended for **academic and educational use**.

---

## 🙌 Acknowledgements

- **Google Gemini API** - For providing the AI capabilities
- **Flask & React Communities** - For excellent open-source frameworks
- **PostgreSQL** - For robust database capabilities
- **Open Source Contributors** - For the tools and libraries that made this possible

---

> 🎓 **GenAI Email & Report Drafting System** — Designed and maintained by `Viswanatha Swamy P K`  
> Demonstrating enterprise-grade architecture with Generative AI integration.  
> © 2026 Swamy's Tech Skills Academy, ShyvnTech & Srivari Software Solutions

**⭐ If you find this project useful, feel free to star the repository.**
