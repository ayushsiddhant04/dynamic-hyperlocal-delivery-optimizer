from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Location(BaseModel):
    """Geographic coordinate representation."""
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    address: Optional[str] = Field(None, description="Human-readable address or landmark name")
    name: Optional[str] = Field(None, description="Identifier or label for this location")


class DeliveryStop(BaseModel):
    """Delivery stop with geographic coordinates and constraints."""
    id: str = Field(..., description="Unique delivery stop ID")
    location: Location
    package_count: int = Field(1, ge=1, description="Number of packages to deliver")
    priority: int = Field(1, ge=1, le=5, description="Delivery priority 1 (low) to 5 (urgent)")
    notes: Optional[str] = Field(None, description="Dispatcher notes or customer instructions")


class AlgorithmMetadata(BaseModel):
    """Metadata describing a route optimization algorithm."""
    id: str
    name: str
    description: str
    paradigm: str
    time_complexity: str
    is_exact: bool
    status: str = "scaffolded"


class RouteMetrics(BaseModel):
    """Computed metrics for a delivery route."""
    total_distance_km: float = 0.0
    estimated_duration_minutes: float = 0.0
    stop_count: int = 0


class OptimizationRequest(BaseModel):
    """Request payload to optimize delivery stops."""
    depot: Location
    stops: List[DeliveryStop]
    algorithm: str = "nearest_neighbor"
    parameters: Optional[Dict[str, Any]] = None


class OptimizationResult(BaseModel):
    """Result of an optimization execution."""
    algorithm_used: str
    ordered_stop_ids: List[str]
    metrics: RouteMetrics
    computation_time_ms: float
    status: str = "success"
    message: Optional[str] = None


class HealthResponse(BaseModel):
    """Lightweight liveness probe response."""
    status: str = "healthy"
    service: str = "routeflow-backend"
    timestamp: str


class SystemStatusResponse(BaseModel):
    """Comprehensive system diagnostics response."""
    status: str = "operational"
    service: str = "routeflow-backend"
    version: str
    environment: str
    uptime_seconds: float
    available_algorithms: List[AlgorithmMetadata]
    timestamp: str
