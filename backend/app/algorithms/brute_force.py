from itertools import permutations
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


class BruteForceOptimizer(BaseRouteOptimizer):
    id = "brute_force"
    name = "Brute Force (Exact)"
    description = (
        "Exhaustively evaluates every possible delivery order and "
        "selects the complete round-trip route with the lowest "
        "weighted road-distance and travel-time cost."
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
                    total_duration_minutes=0.0,
                    stop_count=0,
                ),
                computation_time_ms=0.0,
                status="success",
                message="No delivery stops were provided.",
            )

        distance_weight = parameters.get("distance_weight")
        time_weight = parameters.get("time_weight")

        if distance_weight is None or time_weight is None:
            raise ValueError(
                "distance_weight and time_weight must be provided."
            )

        distance_weight = float(distance_weight)
        time_weight = float(time_weight)

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

        distance_matrix, duration_matrix = compute_road_matrices(
            locations
        )

        stop_count = len(stops)

        algorithm_start = perf_counter()

        routes: List[Dict[str, Any]] = []

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

            # Complete round trip:
            # depot -> all deliveries -> depot
            total_distance_km += distance_matrix[
                current_index
            ][0]

            total_duration_minutes += duration_matrix[
                current_index
            ][0]

            routes.append(
                {
                    "route": route,
                    "distance_km": total_distance_km,
                    "duration_minutes": total_duration_minutes,
                }
            )

        min_distance = min(
            route["distance_km"]
            for route in routes
        )

        max_distance = max(
            route["distance_km"]
            for route in routes
        )

        min_duration = min(
            route["duration_minutes"]
            for route in routes
        )

        max_duration = max(
            route["duration_minutes"]
            for route in routes
        )

        distance_range = max_distance - min_distance
        duration_range = max_duration - min_duration

        for route_data in routes:
            if distance_range == 0:
                normalized_distance = 0.0
            else:
                normalized_distance = (
                    route_data["distance_km"] - min_distance
                ) / distance_range

            if duration_range == 0:
                normalized_duration = 0.0
            else:
                normalized_duration = (
                    route_data["duration_minutes"] - min_duration
                ) / duration_range

            route_data["cost"] = (
                distance_weight * normalized_distance
                + time_weight * normalized_duration
            )

        best_route_data = min(
            routes,
            key=lambda route_data: (
                route_data["cost"],
                route_data["distance_km"],
                route_data["duration_minutes"],
                tuple(
                    stops[index - 1].id
                    for index in route_data["route"]
                ),
            ),
        )

        computation_time_ms = (
            perf_counter() - algorithm_start
        ) * 1000.0

        ordered_stop_ids = [
            stops[index - 1].id
            for index in best_route_data["route"]
        ]

        return OptimizationResult(
            algorithm_used=self.id,
            ordered_stop_ids=ordered_stop_ids,
            metrics=RouteMetrics(
                total_distance_km=round(
                    best_route_data["distance_km"],
                    3,
                ),
                total_duration_minutes=round(
                    best_route_data["duration_minutes"],
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
                f"{distance_weight:.0%} road distance and "
                f"{time_weight:.0%} road travel time, "
                "including the return to the depot."
            ),
        )