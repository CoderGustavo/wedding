from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_check_app_invalid():
    response = client.post("/check_app", json={"app": "Sherlock"})
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "reason" in data
    assert "description" in data
    assert "play_store" in data
    assert "app_store" in data
    assert data.get("score") >= 70

def test_check_app_valid_ai():
    response = client.post("/check_app", json={"app": "ChatGPT"})
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "reason" in data
    assert "description" in data
    assert "play_store" in data
    assert "app_store" in data
    assert data.get("score") <= 20

def test_check_app_valid_game():
    response = client.post("/check_app", json={"app": "brawl stars"})
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "reason" in data
    assert "description" in data
    assert "play_store" in data
    assert "app_store" in data
    assert data.get("score") <= 20
