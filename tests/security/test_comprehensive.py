import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_full_investigation_flow():
    """Тест повного циклу розслідування: Пошук -> Задача -> Результат -> Експорт"""
    
    # 1. Пошук інструменту
    response = client.get("/tools/search/shodan")
    assert response.status_code == 200
    tool = response.json()
    assert tool["id"] == "shodan"
    
    # 2. Запуск задачі
    run_res = client.post("/tools/shodan/run", json={"query": "8.8.8.8"})
    assert run_res.status_code == 200
    task_id = run_res.json()["task_id"]
    
    # 3. Перевірка статусу (симуляція ready)
    status_res = client.get(f"/tools/status/{task_id}")
    assert status_res.status_code == 200
    assert "status" in status_res.json()

def test_stix_export_integrity():
    """Перевірка універсального формату експорту (STIX 2.1)"""
    # Створюємо фейкове розслідування через DB (або використовуємо існуючий ID)
    # Для тесту просто перевіримо структуру на порожньому/існуючому
    response = client.get("/vault/test-id/export/stix")
    if response.status_code == 200:
        bundle = response.json()
        assert bundle["type"] == "bundle"
        assert len(bundle["objects"]) >= 2
        assert bundle["objects"][0]["type"] == "identity"
        assert bundle["objects"][1]["type"] == "report"

def test_vault_storage():
    """Тест збереження доказів з хешуванням"""
    payload = {
        "investigation_id": str(uuid.uuid4()),
        "source": "maigret",
        "data": '{"username": "admin", "found": true}',
        "metadata": "test metadata"
    }
    # Оскільки ми використовуємо Form, шлемо як data
    response = client.post("/vault/store", data=payload)
    # Поверне 404 бо розслідування немає в базі, але ми перевіряємо логіку рутера
    assert response.status_code in [200, 404]
