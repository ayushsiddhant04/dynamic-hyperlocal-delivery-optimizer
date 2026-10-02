from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "RouteFlow" in data["service"]
    assert data["status"] == "online"
    assert "/api/health" in data["health_check"]


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "routeflow-backend"
    assert "timestamp" in data


def test_status_endpoint():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["service"] == "routeflow-backend"
    assert data["version"] == "0.1.0"
    assert data["uptime_seconds"] >= 0
    assert len(data["available_algorithms"]) >= 4
    algorithm_ids = [alg["id"] for alg in data["available_algorithms"]]
    assert "nearest_neighbor" in algorithm_ids
    assert "two_opt" in algorithm_ids
    assert "genetic" in algorithm_ids
    assert "simulated_annealing" in algorithm_ids
