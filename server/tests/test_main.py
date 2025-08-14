from fastapi.testclient import TestClient

from src.app.main import app  # Adjusted import to match the new app name


def test_read_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert (
            "Welcome to Zen Task Manager Server" in response.json()["message"]
        )  # Adjusted message


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
