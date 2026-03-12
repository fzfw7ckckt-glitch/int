from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_security_headers():
    """Перевірка наявності захисних заголовків (Золотий стандарт 2026)"""
    response = client.get("/")
    assert response.status_code == 200
    
    # Перевірка X-Frame-Options
    assert response.headers["X-Frame-Options"] == "DENY"
    
    # Перевірка X-Content-Type-Options
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    
    # Перевірка CSP
    assert "Content-Security-Policy" in response.headers
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]
    
    # Перевірка HSTS
    assert "Strict-Transport-Security" in response.headers
    
    # Перевірка Referrer-Policy
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"

def test_cors_headers():
    """Перевірка налаштувань CORS"""
    response = client.options("/", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    })
    assert response.status_code == 200
    # При allow_origins=["*"], FastAPI повертає Origin з запиту
    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
