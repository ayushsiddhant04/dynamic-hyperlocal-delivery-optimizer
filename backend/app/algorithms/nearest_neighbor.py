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
    compute_distance_matrix,
    estimate_travel_time_minutes,
)


class NearestNeighborOptimizer(BaseRouteOptimizer):
    id = "nearest_neighbor"
    name = "Nearest Neighbor (Greedy)"
    description = (
        "Constructive greedy heuristic that visits the closest "
        "unvisited delivery stop at each step."
    )
    paradigm = "Greedy Heuristic"
    time_complexity = "O(N²)"
    is_exact = False

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
            raise ValueError("average_speed_kmh must be greater than 0.")

        if not stops:
            return OptimizationResult(
                algorithm_used=self.id,
                ordered_stop_ids=[],
                metrics=RouteMetrics(
                    total_distance_km=0.0,
                    estimated_duration_minutes=0.0,
                    stop_count=0,
                ),
                computation_time_ms=round(
                    (perf_counter() - start_time) * 1000,
                    3,
                ),
                status="success",
                message="No delivery stops were provided.",
            )

        locations = [depot] + [stop.location for stop in stops]

        distance_matrix = compute_distance_matrix(locations)

        unvisited = list(range(1, len(locations)))
        ordered_stop_ids: List[str] = []

        current_index = 0
        total_distance_km = 0.0
        estimated_duration_minutes = 0.0

        stop_by_index = {
            index: stop
            for index, stop in enumerate(stops, start=1)
        }

        while unvisited:
            next_index = min(
                unvisited,
                key=lambda index: (
                    distance_matrix[current_index][index],
                    stop_by_index[index].id,
                ),
            )

            leg_distance_km = distance_matrix[current_index][next_index]

            total_distance_km += leg_distance_km
            estimated_duration_minutes += estimate_travel_time_minutes(
                leg_distance_km,
                average_speed_kmh,
            )

            ordered_stop_ids.append(stop_by_index[next_index].id)

            current_index = next_index
            unvisited.remove(next_index)

        return_distance_km = distance_matrix[current_index][0]

        total_distance_km += return_distance_km
        estimated_duration_minutes += estimate_travel_time_minutes(
            return_distance_km,
            average_speed_kmh,
        )

        return OptimizationResult(
            algorithm_used=self.id,
            ordered_stop_ids=ordered_stop_ids,
            metrics=RouteMetrics(
                total_distance_km=round(total_distance_km, 3),
                estimated_duration_minutes=round(
                    estimated_duration_minutes,
                    1,
                ),
                stop_count=len(stops),
            ),
            computation_time_ms=round(
                (perf_counter() - start_time) * 1000,
                3,
            ),
            status="success",
            message=(
                "Route generated using Nearest Neighbor "
                "with Mapbox road distances and a return to the depot."
            ),
        )