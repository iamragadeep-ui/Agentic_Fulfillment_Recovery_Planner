from __future__ import annotations

from typing import Any


def approval_agent(state: dict[str, Any]) -> dict[str, Any]:
    approval = state.get("human_approval") or {"decision": "approve", "notes": "Approved by planner default"}
    return {"approval_status": approval.get("decision", "approve"), "current_stage": "human_approval"}
