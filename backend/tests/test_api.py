from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_endpoint() -> None:
    response = client.post(
        "/api/chat",
        json={
            "user_query": "Order ORD123 was supposed to arrive yesterday but it has not arrived. What should we do?",
            "session_id": "demo-session",
            "user_id": "ops-user",
            "order_id": "ORD123",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["issue_category"] in {"DELAYED_SHIPMENT", "UNKNOWN"}
    assert "final_response" in payload
