# RouteFlow Architecture Specification

## 1. System Architecture
RouteFlow is structured as a decoupled client-server architecture:
- **Frontend**: Next.js 16 App Router with TypeScript and Tailwind CSS.
- **Backend**: Python FastAPI application exposing asynchronous REST endpoints.
- **Data & Algorithms**: Self-contained mathematical optimization engine adhering to `BaseRouteOptimizer`.

## 2. Core Directories
- `frontend/`: Next.js web application
- `backend/`: FastAPI backend API & routing algorithms
- `data/`: Geographic datasets and delivery test manifests
- `docs/`: System documentation and architectural blueprints
