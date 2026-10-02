import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from backend.app.auth import require_approver, require_user
from backend.app.config import settings
from backend.app.main import app
from backend.app.services.memory_service import MemoryService, create_storage_engine, memory_service

app.dependency_overrides[require_user] = lambda: "test-user"
app.dependency_overrides[require_approver] = lambda: "test-user"
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
    assert payload["approval_status"] == "pending"
    assert "no recovery action has been executed" in payload["final_response"]


def test_chat_requires_authentication() -> None:
    app.dependency_overrides.pop(require_user)
    try:
        response = client.post("/api/chat", json={"user_query": "Check order ORD123"})
    finally:
        app.dependency_overrides[require_user] = lambda: "test-user"

    assert response.status_code == 401


def test_persistent_state_is_shared_and_user_scoped() -> None:
    engine = create_storage_engine("sqlite://", "development")
    writer = MemoryService(engine)
    writer.add_message("session-1", "user-1", "user", "hello")
    writer.save_workflow_state("workflow-1", "user-1", {"session_id": "session-1"})

    reader = MemoryService(engine)
    assert reader.get_session_history("session-1", "user-1") == [
        {"role": "user", "content": "hello"}
    ]
    assert reader.get_workflow_state("workflow-1", "user-1")["session_id"] == "session-1"
    assert reader.get_workflow_state("workflow-1", "user-2") == {}
    with pytest.raises(PermissionError):
        reader.get_session_history("session-1", "user-2")


def test_production_rejects_sqlite_storage() -> None:
    with pytest.raises(RuntimeError, match="PostgreSQL"):
        create_storage_engine("sqlite://", "production")


def test_approval_rejects_unknown_workflow() -> None:
    response = client.post(
        "/api/approval/missing-workflow",
        json={"workflow_id": "missing-workflow", "decision": "approve"},
    )
    assert response.status_code == 404


def test_non_approver_role_is_forbidden(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "backend.app.auth._decode_token",
        lambda credentials: {"sub": "test-user", "org_role": "org:member"},
    )
    with pytest.raises(HTTPException) as exc_info:
        require_approver()
    assert exc_info.value.status_code == 403


def test_approval_decision_is_persisted() -> None:
    response = client.post(
        "/api/chat",
        json={"user_query": "Order ORD123 was supposed to arrive yesterday.", "order_id": "ORD123"},
    )
    workflow_id = response.json()["workflow_id"]

    approval = client.post(
        f"/api/approval/{workflow_id}",
        json={"workflow_id": workflow_id, "decision": "reject", "notes": "Review evidence"},
    )

    assert approval.status_code == 200
    state = memory_service.get_workflow_state(workflow_id, "test-user")
    assert state["approval_status"] == "reject"
    assert state["human_approval"]["approved_by"] == "test-user"


def test_production_chat_rejects_synthetic_data(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "app_env", "production")
    response = client.post("/api/chat", json={"user_query": "Check order ORD123"})
    assert response.status_code == 503
    assert "Live fulfillment data" in response.json()["detail"]
