from fastapi import APIRouter, HTTPException

from app.algorithms.registry import algorithm_registry
from app.models.schemas import (
    OptimizationRequest,
    OptimizationResult,
)


router = APIRouter(
    tags=["Route Optimization"],
)


@router.post(
    "/optimize",
    response_model=OptimizationResult,
)
def optimize_route(request: OptimizationRequest) -> OptimizationResult:
    """
    Optimize a delivery route using the selected algorithm.

    The endpoint delegates route sequencing to the registered
    RouteFlow optimization algorithm.
    """
    optimizer = algorithm_registry.get(request.algorithm)

    if optimizer is None:
        available_algorithms = [
            metadata.id
            for metadata in algorithm_registry.list_metadata()
        ]

        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Unknown optimization algorithm: {request.algorithm}",
                "available_algorithms": available_algorithms,
            },
        )

    try:
        algorithm_parameters = {
            **(request.parameters or {}),
            "distance_weight": request.objective.distance_weight,
            "time_weight": request.objective.time_weight,
        }

        return optimizer.optimize(
            depot=request.depot,
            stops=request.stops,
            parameters=algorithm_parameters,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Route optimization failed.",
        ) from exc