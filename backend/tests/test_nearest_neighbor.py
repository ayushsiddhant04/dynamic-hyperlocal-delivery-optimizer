from app.algorithms.nearest_neighbor import NearestNeighborOptimizer
from app.models.schemas import DeliveryStop, Location


def test_nearest_neighbor_orders_stops_greedily():
    depot = Location(
        latitude=12.9716,
        longitude=77.5946,
        name="Depot",
    )

    stops = [
        DeliveryStop(
            id="A",
            location=Location(
                latitude=12.9720,
                longitude=77.5950,
                name="Customer A",
            ),
        ),
        DeliveryStop(
            id="B",
            location=Location(
                latitude=12.9800,
                longitude=77.6000,
                name="Customer B",
            ),
        ),
        DeliveryStop(
            id="C",
            location=Location(
                latitude=12.9750,
                longitude=77.5960,
                name="Customer C",
            ),
        ),
    ]

    optimizer = NearestNeighborOptimizer()

    result = optimizer.optimize(
        depot=depot,
        stops=stops,
    )

    assert result.status == "success"
    assert result.algorithm_used == "nearest_neighbor"
    assert result.ordered_stop_ids == ["A", "C", "B"]
    assert result.metrics.stop_count == 3
    assert result.metrics.total_distance_km > 0
    assert result.metrics.estimated_duration_minutes > 0
    assert result.computation_time_ms >= 0