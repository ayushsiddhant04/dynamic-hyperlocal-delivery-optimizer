from time import perf_counter
from typing import Any, Dict, List, Optional

from app.algorithms.base import BaseRouteOptimizer
from app.models.schemas import (
    DeliveryStop,
    Location,
    OptimizationResult,
    RouteMetrics,
)
from app.services.distance import (
    estimate_travel_time_minutes,
    haversine_distance_km,
)


class NearestNeighborOptimizer(BaseRouteOptimizer):
    """
    Greedy Nearest Neighbor heuristic for delivery route sequencing.

    The algorithm starts at the depot and repeatedly selects the
    closest unvisited delivery stop. After all stops are visited,
    the route returns to the depot.
    """

    id: str = "nearest_neighbor"
    name: str = "Nearest Neighbor (Greedy)"
    description = (
        "Constructive greedy heuristic that visits the closest "
        "unvisited delivery stop at each step."
    )
    paradigm: str = "Greedy Heuristic"
    time_complexity: str = "O(N²)"
    is_exact: bool = False

    def optimize(
        self,
        depot: Location,
        stops: List[DeliveryStop],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> OptimizationResult:
        start_time = perf_counter()

        parameters = parameters or {}

        average_speed_kmh = float(
            parameters.get("average_speed_kmh", 30.0)
        )

        if average_speed_kmh <= 0:
            raise ValueError(
                "average_speed_kmh must be greater than 0."
            )

        # No delivery stops: route has zero travel cost.
        if not stops:
            computation_time_ms = (
                perf_counter() - start_time
            ) * 1000

            return OptimizationResult(
                algorithm_used=self.id,
                ordered_stop_ids=[],
                metrics=RouteMetrics(
                    total_distance_km=0.0,
                    estimated_duration_minutes=0.0,
                    stop_count=0,
                ),
                computation_time_ms=round(
                    computation_time_ms, 3
                ),
                status="success",
                message="No delivery stops provided.",
            )

        unvisited = list(stops)
        ordered_stop_ids: List[str] = []

        current_location = depot

        total_distance_km = 0.0
        estimated_duration_minutes = 0.0

        while unvisited:
            # Choose the nearest unvisited delivery stop.
            next_stop = min(
                unvisited,
                key=lambda stop: (
                    haversine_distance_km(
                        current_location,
                        stop.location,
                    ),
                    stop.id,
                ),
            )

            leg_distance_km = haversine_distance_km(
                current_location,
                next_stop.location,
            )

            total_distance_km += leg_distance_km

            estimated_duration_minutes += (
                estimate_travel_time_minutes(
                    leg_distance_km,
                    average_speed_kmh,
                )
            )

            ordered_stop_ids.append(next_stop.id)

            current_location = next_stop.location
            unvisited.remove(next_stop)

        # Return to the depot after the final delivery.
        return_distance_km = haversine_distance_km(
            current_location,
            depot,
        )

        total_distance_km += return_distance_km

        estimated_duration_minutes += (
            estimate_travel_time_minutes(
                return_distance_km,
                average_speed_kmh,
            )
        )

        computation_time_ms = (
            perf_counter() - start_time
        ) * 1000

        return OptimizationResult(
            algorithm_used=self.id,
            ordered_stop_ids=ordered_stop_ids,
            metrics=RouteMetrics(
                total_distance_km=round(
                    total_distance_km,
                    3,
                ),
                estimated_duration_minutes=round(
                    estimated_duration_minutes,
                    1,
                ),
                stop_count=len(stops),
            ),
            computation_time_ms=round(
                computation_time_ms,
                3,
            ),
            status="success",
            message=(
                "Route generated using Nearest Neighbor "
                "with a return to the depot."
            ),
        )