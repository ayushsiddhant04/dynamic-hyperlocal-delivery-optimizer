from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.models.schemas import (
    Location,
    DeliveryStop,
    OptimizationResult,
    AlgorithmMetadata,
)


class BaseRouteOptimizer(ABC):
    """
    Abstract base class for RouteFlow route optimization algorithms.
    All custom optimization algorithms must inherit from this class.
    """

    id: str = "base"
    name: str = "Base Optimizer"
    description: str = "Base interface for route optimization algorithms."
    paradigm: str = "Abstract"
    time_complexity: str = "O(1)"
    is_exact: bool = False

    @classmethod
    def get_metadata(cls) -> AlgorithmMetadata:
        """Returns structured metadata about this algorithm."""
        return AlgorithmMetadata(
            id=cls.id,
            name=cls.name,
            description=cls.description,
            paradigm=cls.paradigm,
            time_complexity=cls.time_complexity,
            is_exact=cls.is_exact,
            status="scaffolded",
        )

    @abstractmethod
    def optimize(
        self,
        depot: Location,
        stops: List[DeliveryStop],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> OptimizationResult:
        """
        Executes route optimization over the given delivery stops starting from depot.

        Args:
            depot: Starting and ending location.
            stops: List of delivery stops to visit.
            parameters: Optional algorithm-specific hyperparameters.

        Returns:
            OptimizationResult containing ordered stop IDs, metrics, and execution time.
        """
        raise NotImplementedError("Optimization algorithm not yet implemented in foundation phase.")
