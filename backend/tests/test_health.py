# test_health.py — Teste que le endpoint /health répond correctement
# But : s'assurer que personne ne casse ce comportement de base
# en modifiant le code plus tard (régression)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "docintel"