# Frontend - GenAI Email & Report Drafting System

## Overview

React + TypeScript frontend application with Tailwind CSS and Redux Toolkit for state management.

## Tech Stack

- **React 19** with TypeScript
- **Vite** - Build tool and dev server
- **Tailwind CSS v4** - Utility-first CSS framework
- **Redux Toolkit** - State management
- **React Router v7** - Client-side routing

## Getting Started

> **📖 Full Setup Guide**: For complete installation and configuration instructions, see [docs/04_setup.md](../../docs/04_setup.md).

### Quick Start (Frontend)

Please refer to the **[Setup Guide](../../docs/04_setup.md)** for authoritative installation and startup instructions.

The setup guide covers:
1.  **Dependency Installation** (`npm install`)
2.  **Environment Configuration** (`.env` setup)
3.  **Running the Development Server** (`npm run dev`)

### Build for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

## Project Structure

```text
frontend/
├── src/
│   ├── api/              # API client and backend communication
│   ├── components/       # Reusable React components
│   ├── pages/            # Page components
│   ├── store/            # Redux store configuration
│   ├── types/            # TypeScript type definitions
│   ├── App.tsx           # Main app component with routing
│   ├── main.tsx          # Application entry point
│   └── index.css         # Global styles with Tailwind
├── .env.example          # Environment variables template
├── package.json
└── README.md
```

## Features

### Authentication

- User registration and login
- JWT token management
- Protected routes requiring authentication

### Document Generation

- **Email Generator**: Generate professional emails with customizable tone
- **Report Generator**: Generate structured reports with customizable tone
- Real-time generation status with loading states

### History

- View all generated documents
- Filter by document type (email/report)
- Document metadata display

### UI/UX

- Soft color palette with modern design
- Fully responsive layout (mobile, tablet, desktop)
- Accessible form controls with focus states

## License

This project is intended for academic and educational use.
