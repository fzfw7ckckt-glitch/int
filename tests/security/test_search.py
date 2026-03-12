from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_recorded_future():
    """Перевірка пошуку інструменту Recorded Future"""
    response = client.get("/tools/search/recorded")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "recorded_future"
    assert data["name"] == "Recorded Future"
    assert data["category"] == "SIGINT"

def test_search_clearview():
    """Перевірка пошуку інструменту Clearview AI"""
    response = client.get("/tools/search/clearview")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "clearview_ai"
    assert data["category"] == "IMINT"

def test_get_new_categories():
    """Перевірка доступу до нових категорій через API"""
    categories = ["IMINT", "CRYPTOINT", "DEEPFAKE", "ARCHIVE", "AI_OSINT"]
    for cat in categories:
        response = client.get(f"/tools/category/{cat}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] is not None
        assert len(data["tools"]) > 0

def test_search_non_existent():
    """Перевірка поведінки при пошуку неіснуючого інструменту"""
    response = client.get("/tools/search/non_existent_tool_123")
    assert response.status_code == 404
