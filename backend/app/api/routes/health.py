import time
from datetime import datetime, timezone
from fastapi import APIRouter
from app.core.config import settings
from app.algorithms.registry import algorithm_registry
from app.models.schemas import HealthResponse, SystemStatusResponse

router = APIRouter(tags=["Health & Status"])

# Track service launch time
_START_TIME = time.time()


@router.get("/health", response_model=HealthResponse)
async def get_health():
    """
    Lightweight liveness probe for monitoring and load balancers.
    """
    return HealthResponse(
        status="healthy",
        service="routeflow-backend",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.get("/status", response_model=SystemStatusResponse)
async def get_status():
    """
    Comprehensive diagnostics endpoint returning service details,
    uptime, environment, and registered route optimization algorithms.
    """
    uptime = round(time.time() - _START_TIME, 2)
    return SystemStatusResponse(
        status="operational",
        service="routeflow-backend",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        uptime_seconds=uptime,
        available_algorithms=algorithm_registry.list_metadata(),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
