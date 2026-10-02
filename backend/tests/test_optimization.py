from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_optimize_route_with_nearest_neighbor():
    payload = {
        "depot": {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "name": "Depot",
        },
        "stops": [
            {
                "id": "A",
                "location": {
                    "latitude": 12.9720,
                    "longitude": 77.5950,
                    "name": "Customer A",
                },
            },
            {
                "id": "B",
                "location": {
                    "latitude": 12.9800,
                    "longitude": 77.6000,
                    "name": "Customer B",
                },
            },
            {
                "id": "C",
                "location": {
                    "latitude": 12.9750,
                    "longitude": 77.5960,
                    "name": "Customer C",
                },
            },
        ],
        "algorithm": "nearest_neighbor",
    }

    response = client.post("/api/optimize", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["algorithm_used"] == "nearest_neighbor"
    assert data["ordered_stop_ids"] == ["A", "C", "B"]
    assert data["metrics"]["stop_count"] == 3
    assert data["metrics"]["total_distance_km"] > 0
    assert data["metrics"]["estimated_duration_minutes"] > 0
    assert data["computation_time_ms"] >= 0