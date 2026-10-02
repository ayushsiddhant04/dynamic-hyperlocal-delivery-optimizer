from typing import List, Optional, Dict, Any
from app.algorithms.base import BaseRouteOptimizer
from app.models.schemas import Location, DeliveryStop, OptimizationResult


class NearestNeighborOptimizer(BaseRouteOptimizer):
    """
    Greedy Nearest Neighbor heuristic for TSP/VRP route sequencing.
    Starts at depot and incrementally visits the closest unvisited stop.
    """

    id: str = "nearest_neighbor"
    name: str = "Nearest Neighbor (Greedy)"
    description: str = "Constructive heuristic that visits the closest unvisited stop at each step."
    paradigm: str = "Greedy Heuristic"
    time_complexity: str = "O(N²)"
    is_exact: bool = False

    def optimize(
        self,
        depot: Location,
        stops: List[DeliveryStop],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> OptimizationResult:
        """Stub method for foundation phase."""
        raise NotImplementedError("Nearest Neighbor implementation is scheduled for the optimization phase.")
