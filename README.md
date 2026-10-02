# RouteFlow — Dynamic Hyperlocal Delivery Optimizer

> Intelligent hyperlocal delivery route optimization platform with modular algorithmic routing engines, dynamic re-routing, and map visualization.

---

## 1. Project Overview

RouteFlow is designed for local dispatchers to optimize multi-stop delivery routes. It provides:
1. **Interactive Map Visualization**: Visualizing depots, delivery stops, and paths via Mapbox GL JS.
2. **Modular Route Optimization Engine**: Custom-built Python algorithms (Nearest Neighbor, 2-Opt, Genetic Algorithm, Simulated Annealing) rather than relying exclusively on black-box routing APIs.
3. **Dynamic Re-optimization**: Adapting routes in real time based on simulated traffic events.
4. **Benchmarking & Comparison**: Side-by-side comparison of execution times, total distances, and solution qualities across optimization algorithms.

---

## 2. Architecture & Tech Stack

```
dynamic-hyperlocal-route-optimizer/
├── .gitignore                      # Universal gitignore (Node, Python, venv, secrets)
├── README.md                       # Root architecture and developer documentation
├── backend/                        # Python FastAPI Backend Engine
│   ├── requirements.txt            # Python dependencies (fastapi, uvicorn, pydantic, etc.)
│   ├── .env.example                # Template for backend environment variables
│   ├── .env                        # Local development environment settings
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_health.py          # Pytest suite for API endpoints
│   └── app/
│       ├── __init__.py
│       ├── main.py                 # FastAPI application instance, CORS, router mounting
│       ├── core/
│       │   ├── __init__.py
│       │   └── config.py           # Pydantic Settings (CORS, app configuration)
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes/
│       │       ├── __init__.py
│       │       └── health.py       # /api/health and /api/status endpoints
│       ├── algorithms/             # Modular optimization solvers
│       │   ├── __init__.py
│       │   ├── base.py             # BaseRouteOptimizer abstract base class
│       │   ├── nearest_neighbor.py # Greedy Nearest Neighbor heuristic stub
│       │   ├── two_opt.py          # 2-Opt local search improvement stub
│       │   ├── genetic.py          # Genetic algorithm evolutionary stub
│       │   ├── simulated_annealing.py # Simulated annealing probabilistic stub
│       │   └── registry.py         # Dynamic algorithm registry & metadata catalog
│       ├── models/
│       │   ├── __init__.py
│       │   └── schemas.py          # Pydantic domain models (Location, Stop, Result, etc.)
│       └── services/
│           ├── __init__.py
│           └── distance.py         # Haversine distance, travel times, matrix generator
└── frontend/                       # Next.js 16 + TypeScript Frontend
    ├── package.json
    ├── tsconfig.json
    ├── next.config.ts
    ├── .env.example                # Template for frontend environment variables
    ├── .env.local                  # Local development environment settings
    └── src/
        ├── app/
        │   ├── layout.tsx          # Root HTML layout and metadata
        │   ├── page.tsx            # Foundation status & connectivity diagnostic page
        │   └── globals.css         # Modern Vanilla CSS design system (tokens, dark theme)
        ├── lib/
        │   └── api.ts              # Typed client for backend communication
        └── types/
            └── index.ts            # TypeScript interfaces matching backend models
```

### Technology Matrix
| Layer | Technology | Key Capabilities |
| :--- | :--- | :--- |
| **Frontend** | Next.js 16 (App Router) + TypeScript | Responsive UI, client components, typed API client |
| **Styling** | Vanilla CSS with Design Tokens | Modern dark theme, glassmorphism, responsive grid, zero external CSS bloat |
| **Map Rendering** | Mapbox GL JS | Vector maps configured via `NEXT_PUBLIC_MAPBOX_TOKEN` |
| **Backend** | Python 3.12+ / FastAPI | High performance asynchronous REST API with OpenAPI docs |
| **Data Contracts** | Pydantic v2 | Strictly validated request/response payloads |
| **Distance Services** | Haversine Formula | Mathematical distance & travel-time calculations without paid APIs |

---

## 3. Algorithm Engine Design Pattern

All route optimization algorithms inherit from the abstract base class `BaseRouteOptimizer`:

```python
class BaseRouteOptimizer(ABC):
    id: str
    name: str
    description: str
    paradigm: str
    time_complexity: str
    is_exact: bool

    @classmethod
    def get_metadata(cls) -> AlgorithmMetadata:
        ...

    @abstractmethod
    def optimize(
        self,
        depot: Location,
        stops: List[DeliveryStop],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> OptimizationResult:
        ...
```

Registered solvers are cataloged in `AlgorithmRegistry` and queryable via `/api/status`:
1. **Nearest Neighbor**: Greedy constructive heuristic ($O(N^2)$).
2. **2-Opt**: Iterative local search to eliminate crossing edges ($O(N^2 \text{/iter})$).
3. **Genetic Algorithm**: Evolutionary metaheuristic with crossover and mutation ($O(G \cdot P \cdot N)$).
4. **Simulated Annealing**: Thermodynamic metaheuristic escaping local optima ($O(T \cdot N)$).

---

## 4. API Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Service root and navigation links |
| `GET` | `/api/health` | Lightweight liveness probe |
| `GET` | `/api/status` | Comprehensive diagnostics, uptime, and registered algorithms |
| `GET` | `/docs` | Interactive Swagger API documentation |
| `GET` | `/redoc` | ReDoc API documentation |

---

## 5. Getting Started (Running Independently)

### Prerequisites
- Node.js 18+ (tested with v24)
- Python 3.10+ (tested with v3.12)

---

### Backend Setup & Execution

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run backend tests:
   ```bash
   pytest -v
   ```

5. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will be available at:
- API Root: `http://localhost:8000`
- Health Probe: `http://localhost:8000/api/health`
- System Status: `http://localhost:8000/api/status`
- Swagger Documentation: `http://localhost:8000/docs`

---

### Frontend Setup & Execution

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies (if not already installed):
   ```bash
   npm install
   ```

3. Configure environment variables (optional):
   ```bash
   # Copy template if needed
   cp .env.example .env.local
   ```
   Set `NEXT_PUBLIC_MAPBOX_TOKEN` when ready for live maps.

4. Build and verify TypeScript types:
   ```bash
   npm run build
   ```

5. Start the Next.js development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`.

---

## 6. Environment Variables

### Backend (`backend/.env`)
- `HOST`: Server host binding (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `ENVIRONMENT`: Deployment environment (default: `development`)
- `CORS_ORIGINS`: Allowed origins (default: `["http://localhost:3000","http://127.0.0.1:3000"]`)

### Frontend (`frontend/.env.local`)
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: `http://localhost:8000`)
- `NEXT_PUBLIC_MAPBOX_TOKEN`: Public Mapbox access token (optional in foundation phase)
