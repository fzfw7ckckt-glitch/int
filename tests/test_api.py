import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_health_liveness():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"

def test_tools_list():
    response = client.get("/tools/")
    assert response.status_code == 200
    assert "total_tools" in response.json()
    assert response.json()["total_tools"] > 0

def test_get_tool():
    response = client.get("/tools/shodan")
    assert response.status_code == 200
    assert response.json()["name"] == "Shodan"

def test_get_nonexistent_tool():
    response = client.get("/tools/nonexistent")
    assert response.status_code == 404

def test_run_tool():
    response = client.post("/tools/shodan/run?query=test")
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "queued"

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_duplicate_user():
    # First registration
    client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "email": "dup@example.com",
            "password": "pass123"
        }
    )
    # Second registration with same username
    response = client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "email": "dup2@example.com",
            "password": "pass123"
        }
    )
    assert response.status_code == 400

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
