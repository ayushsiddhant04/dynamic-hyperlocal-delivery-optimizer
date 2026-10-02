from time import perf_counter
from typing import Any, Dict, List, Optional

from app.algorithms.base import BaseRouteOptimizer
from app.models.schemas import (
    DeliveryStop,
    Location,
    OptimizationResult,
    RouteMetrics,
)
from app.services.distance import compute_road_matrices


class NearestNeighborOptimizer(BaseRouteOptimizer):
    id = "nearest_neighbor"
    name = "Nearest Neighbor (Greedy)"
    description = (
        "Constructive greedy heuristic that selects the next delivery "
        "using a weighted road-distance and road-travel-time cost."
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
        parameters = parameters or {}

        if not stops:
            return OptimizationResult(
                algorithm_used=self.id,
                ordered_stop_ids=[],
                metrics=RouteMetrics(
                    total_distance_km=0.0,
                    total_duration_minutes=0.0,
                    stop_count=0,
                ),
                computation_time_ms=0.0,
                status="success",
                message="No delivery stops were provided.",
            )

        distance_weight = float(
            parameters.get("distance_weight", 0.0)
        )

        time_weight = float(
            parameters.get("time_weight", 0.0)
        )

        if distance_weight < 0 or time_weight < 0:
            raise ValueError(
                "distance_weight and time_weight cannot be negative."
            )

        if distance_weight + time_weight <= 0:
            raise ValueError(
                "At least one of distance_weight or time_weight "
                "must be greater than 0."
            )

        weight_sum = distance_weight + time_weight
        distance_weight /= weight_sum
        time_weight /= weight_sum

        locations = [depot] + [stop.location for stop in stops]

        # External road-data retrieval is intentionally outside the
        # algorithm computation timer.
        distance_matrix, duration_matrix = compute_road_matrices(
            locations
        )

        max_distance = max(
            (
                value
                for row in distance_matrix
                for value in row
                if value > 0
            ),
            default=0.0,
        )

        max_duration = max(
            (
                value
                for row in duration_matrix
                for value in row
                if value > 0
            ),
            default=0.0,
        )

        if max_distance <= 0:
            raise ValueError(
                "Road distance data is insufficient for optimization."
            )

        if max_duration <= 0:
            raise ValueError(
                "Road travel-time data is insufficient for optimization."
            )

        start_time = perf_counter()

        unvisited = list(range(1, len(locations)))
        ordered_stop_ids: List[str] = []

        current_index = 0

        total_distance_km = 0.0
        total_duration_minutes = 0.0

        stop_by_index = {
            index: stop
            for index, stop in enumerate(stops, start=1)
        }

        def edge_cost(index: int) -> tuple[float, float, float, str]:
            distance_km = distance_matrix[current_index][index]
            duration_minutes = duration_matrix[current_index][index]

            normalized_distance = distance_km / max_distance
            normalized_duration = (
                duration_minutes / max_duration
            )

            combined_cost = (
                distance_weight * normalized_distance
                + time_weight * normalized_duration
            )

            return (
                combined_cost,
                distance_km,
                duration_minutes,
                stop_by_index[index].id,
            )

        while unvisited:
            next_index = min(
                unvisited,
                key=edge_cost,
            )

            total_distance_km += distance_matrix[
                current_index
            ][next_index]

            total_duration_minutes += duration_matrix[
                current_index
            ][next_index]

            ordered_stop_ids.append(
                stop_by_index[next_index].id
            )

            current_index = next_index
            unvisited.remove(next_index)

        # The delivery trip is a complete round trip:
        # depot -> all deliveries -> depot.
        total_distance_km += distance_matrix[current_index][0]

        total_duration_minutes += duration_matrix[
            current_index
        ][0]

        computation_time_ms = (
            perf_counter() - start_time
        ) * 1000.0

        return OptimizationResult(
            algorithm_used=self.id,
            ordered_stop_ids=ordered_stop_ids,
            metrics=RouteMetrics(
                total_distance_km=round(
                    total_distance_km,
                    3,
                ),
                total_duration_minutes=round(
                    total_duration_minutes,
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
                "Route generated using Nearest Neighbor with a "
                "weighted road-distance and road-travel-time objective, "
                "including the return to the depot."
            ),
        )