# Repository Structure

**Project:** GenAI Email & Report Drafting System  
**Last Updated:** 2026-01-12  
**Status:** Repository Skeleton (scaffolding in progress)

---

## Overview

This document reflects the current, minimal structure of the repository. The initial commit lays out the top-level folders for backend, frontend, database assets, and documentation so that code, schema, and design notes can evolve independently while still following the planned N-tier architecture described in the README.

---

## Current Directory Structure

```text
genai-email-report-drafting/
├── .gitignore
├── .python-version
├── LICENSE
├── README.md
├── database/
│   └── .gitkeep
├── docs/
│   ├── 01_abstract.md
│   ├── 02_requirements.md
│   ├── 07_repository_structure.md
│   ├── diagrams/
│   │   ├── README.md
│   │   ├── system-architecture-basic.mmd
│   │   ├── system-architecture-requirements.mmd
│   │   ├── system-architecture-simple.mmd
│   │   └── system-architecture.mmd
│   └── images/
│       └── .gitkeep
└── src/
    ├── backend/
    │   └── .gitkeep
    └── frontend/
        └── .gitkeep
```

**Notes:**

- `.gitkeep` files mark folders that are intentionally empty but required for future work.
- Documentation already includes Mermaid diagrams so design work can continue while code is being scaffolded.

---

## Layer Overview

### Presentation Layer (src/frontend)

- Planned React + TypeScript single-page application per the README technology stack.
- `src/frontend/.gitkeep` keeps the folder under version control until actual code (components, pages, state) is added.
- When implementation starts, sub-folders such as `src/frontend/src`, `public`, and configuration files (`package.json`, Vite config, etc.) will live here.

### Application Layer (src/backend)

- Reserved for the Flask REST API, Gemini integration clients, and tests.
- `.gitkeep` placeholder ensures the backend folder remains in git even before `app.py`, `requirements.txt`, and service modules are committed.
- The backend will eventually expose the endpoints described in the README (auth, documents, history, admin).

### Data Layer (database)

- Central location for SQL schema files, seed scripts, or migration notes.
- Currently empty aside from `.gitkeep`; schemas will be added once ER design from the docs is materialized.

### Documentation Layer (docs)

- Active area of the repository: requirements, architecture plans, and diagram sources already exist.
- The diagrams directory stores Mermaid definitions, enabling architecture discussions before implementation.
- The images directory is ready for rendered diagrams or UI mock-ups once available.

---

## Documentation Assets

- [docs/01_abstract.md](01_abstract.md) and [docs/02_requirements.md](02_requirements.md) capture the problem space and expectations early.
- This file, [docs/07_repository_structure.md](07_repository_structure.md), will expand as backend/frontend code lands.
- [docs/diagrams/README.md](diagrams/README.md) explains how to regenerate the Mermaid diagrams and ensures consistent visual updates.

---

## Planned Evolution

1. **Frontend implementation**: introduce Vite + React scaffolding under `src/frontend`, followed by components, routes, and Redux slices that align with the documented flows.
2. **Backend implementation**: add Flask application factory, route blueprints, service modules, and tests beneath `src/backend`.
3. **Database schema**: draft and version SQL DDL files under `database` once entity definitions from the requirements stabilize.
4. **Tooling and automation**: incorporate CI scripts or auxiliary tooling (if needed) at the root after core code exists.

These steps keep parity with the high-level architecture while acknowledging the repository is currently in its early scaffolding phase.

---

**Maintained By:** Vattem Hema
