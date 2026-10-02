from app.algorithms.brute_force import BruteForceOptimizer
from app.models.schemas import DeliveryStop, Location


def test_brute_force_finds_best_round_trip(monkeypatch):
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

    distance_matrix = [
        [0.0, 1.0, 8.0, 9.0],
        [1.0, 0.0, 4.0, 2.0],
        [8.0, 4.0, 0.0, 3.0],
        [9.0, 2.0, 3.0, 0.0],
    ]

    duration_matrix = [
        [0.0, 1.0, 8.0, 9.0],
        [1.0, 0.0, 4.0, 2.0],
        [8.0, 4.0, 0.0, 3.0],
        [9.0, 2.0, 3.0, 0.0],
    ]

    monkeypatch.setattr(
        "app.algorithms.brute_force.compute_road_matrices",
        lambda locations: (distance_matrix, duration_matrix),
    )

    optimizer = BruteForceOptimizer()

    result = optimizer.optimize(
        depot=depot,
        stops=stops,
        parameters={
            "distance_weight": 0.5,
            "time_weight": 0.5,
        },
    )

    assert result.status == "success"
    assert result.algorithm_used == "brute_force"
    assert result.ordered_stop_ids == ["A", "C", "B"]
    assert result.metrics.stop_count == 3
    assert result.metrics.total_distance_km == 14.0
    assert result.metrics.total_duration_minutes == 14.0
    assert result.computation_time_ms >= 0