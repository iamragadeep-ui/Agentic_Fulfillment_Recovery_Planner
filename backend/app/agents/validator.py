from __future__ import annotations

from typing import Any


def validator_agent(state: dict[str, Any]) -> dict[str, Any]:
    if state.get("confidence", 0) < 0.55:
        result = "RETRY"
    elif state.get("recovery_plan", {}).get("human_approval_required"):
        result = "HUMAN_REVIEW"
    elif state.get("issue_category") == "UNKNOWN":
        result = "RETRY"
    else:
        result = "PASS"

    return {"validation_result": result, "current_stage": "validation"}
