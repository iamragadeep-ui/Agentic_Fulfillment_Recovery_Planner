from __future__ import annotations

from typing import Any


def approval_agent(state: dict[str, Any]) -> dict[str, Any]:
    approval = state.get("human_approval") or {"decision": "pending", "notes": "Awaiting an authorized approver"}
    return {"approval_status": approval.get("decision", "pending"), "current_stage": "human_approval"}
