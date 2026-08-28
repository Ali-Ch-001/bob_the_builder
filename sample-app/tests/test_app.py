# NOTE: fastapi.testclient.TestClient requires the `httpx` package at runtime.
# It is not listed in pyproject.toml; install it to actually run these tests.

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.json() == []


def test_create_order():
    payload = {"id": 0, "customer": "acme", "items": ["widget"], "total": 19.99}
    response = client.post("/orders", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["customer"] == "acme"
    assert body["items"] == ["widget"]


def test_create_order_total():
    payload = {"id": 0, "customer": "acme", "items": ["widget"], "total": 19.99}
    response = client.post("/orders", json=payload)
    assert response.status_code == 200
    assert response.json()["total"] == 999.0
