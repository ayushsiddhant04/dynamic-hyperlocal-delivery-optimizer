from typing import Dict, List, Type, Optional
from app.algorithms.base import BaseRouteOptimizer
from app.algorithms.nearest_neighbor import NearestNeighborOptimizer
from app.algorithms.two_opt import TwoOptOptimizer
from app.algorithms.genetic import GeneticOptimizer
from app.algorithms.simulated_annealing import SimulatedAnnealingOptimizer
from app.models.schemas import AlgorithmMetadata


class AlgorithmRegistry:
    """
    Central registry for RouteFlow optimization algorithms.
    Supports dynamic lookup, instantiation, and metadata enumeration.
    """

    def __init__(self):
        self._registry: Dict[str, Type[BaseRouteOptimizer]] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register(NearestNeighborOptimizer)
        self.register(TwoOptOptimizer)
        self.register(GeneticOptimizer)
        self.register(SimulatedAnnealingOptimizer)

    def register(self, optimizer_cls: Type[BaseRouteOptimizer]):
        """Register an optimizer class."""
        self._registry[optimizer_cls.id] = optimizer_cls

    def get(self, algorithm_id: str) -> Optional[BaseRouteOptimizer]:
        """Get an instance of an optimizer by its ID."""
        optimizer_cls = self._registry.get(algorithm_id)
        if optimizer_cls:
            return optimizer_cls()
        return None

    def list_metadata(self) -> List[AlgorithmMetadata]:
        """List metadata for all registered algorithms."""
        return [cls.get_metadata() for cls in self._registry.values()]


# Global registry singleton instance
algorithm_registry = AlgorithmRegistry()
