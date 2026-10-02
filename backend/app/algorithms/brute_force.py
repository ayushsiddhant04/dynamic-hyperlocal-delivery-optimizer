from itertools import permutations
from time import perf_counter
from typing import Any, Dict, List, Optional, Tuple

from app.algorithms.base import BaseRouteOptimizer
from app.models.schemas import (
    DeliveryStop,
    Location,
    OptimizationResult,
    RouteMetrics,
)
from app.services.distance import compute_road_matrices


class BruteForceOptimizer(BaseRouteOptimizer):
    id = "brute_force"
    name = "Brute Force (Exact)"
    description = (
        "Exhaustively evaluates every possible delivery order and "
        "selects the route with the lowest combined distance-and-time cost."
    )
    paradigm = "Exhaustive Search"
    time_complexity = "O(N!)"
    is_exact = True

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
                    estimated_duration_minutes=0.0,
                    stop_count=0,
                ),
                computation_time_ms=0.0,
                status="success",
                message="No delivery stops were provided.",
            )

        distance_weight = float(
            parameters.get("distance_weight", 0.5)
        )
        time_weight = float(
            parameters.get("time_weight", 0.5)
        )
        reference_speed_kmh = float(
            parameters.get("reference_speed_kmh", 30.0)
        )

        if distance_weight < 0 or time_weight < 0:
            raise ValueError(
                "distance_weight and time_weight cannot be negative."
            )

        if distance_weight == 0 and time_weight == 0:
            raise ValueError(
                "At least one of distance_weight or time_weight must be greater than 0."
            )

        if reference_speed_kmh <= 0:
            raise ValueError(
                "reference_speed_kmh must be greater than 0."
            )

        weight_sum = distance_weight + time_weight
        distance_weight /= weight_sum
        time_weight /= weight_sum

        locations = [depot] + [stop.location for stop in stops]

        distance_matrix, duration_matrix = compute_road_matrices(locations)

        stop_count = len(stops)

        best_route: Optional[Tuple[int, ...]] = None
        best_distance_km = float("inf")
        best_duration_minutes = float("inf")
        best_cost = float("inf")

        algorithm_start = perf_counter()

        for route in permutations(range(1, stop_count + 1)):
            current_index = 0

            total_distance_km = 0.0
            total_duration_minutes = 0.0

            for next_index in route:
                total_distance_km += distance_matrix[
                    current_index
                ][next_index]

                total_duration_minutes += duration_matrix[
                    current_index
                ][next_index]

                current_index = next_index

            total_distance_km += distance_matrix[current_index][0]
            total_duration_minutes += duration_matrix[current_index][0]

            time_equivalent_km = (
                total_duration_minutes
                * reference_speed_kmh
                / 60.0
            )

            combined_cost = (
                distance_weight * total_distance_km
                + time_weight * time_equivalent_km
            )

            route_ids = tuple(
                stops[index - 1].id
                for index in route
            )

            best_route_ids = (
                tuple(
                    stops[index - 1].id
                    for index in best_route
                )
                if best_route is not None
                else ()
            )

            candidate_key = (
                combined_cost,
                total_distance_km,
                total_duration_minutes,
                route_ids,
            )

            best_key = (
                best_cost,
                best_distance_km,
                best_duration_minutes,
                best_route_ids,
            )

            if candidate_key < best_key:
                best_route = route
                best_distance_km = total_distance_km
                best_duration_minutes = total_duration_minutes
                best_cost = combined_cost

            current_index = 0

        computation_time_ms = (
            perf_counter() - algorithm_start
        ) * 1000.0

        ordered_stop_ids = [
            stops[index - 1].id
            for index in best_route
        ]

        return OptimizationResult(
            algorithm_used=self.id,
            ordered_stop_ids=ordered_stop_ids,
            metrics=RouteMetrics(
                total_distance_km=round(
                    best_distance_km,
                    3,
                ),
                total_duration_minutes=round(
                    best_duration_minutes,
                    1,
                ),
                stop_count=stop_count,
            ),
            computation_time_ms=round(
                computation_time_ms,
                3,
            ),
            status="success",
            message=(
                "Exact route selected by exhaustive search using "
                f"{distance_weight:.0%} distance and "
                f"{time_weight:.0%} travel-time weighting, "
                "with a return to the depot."
            ),
        )