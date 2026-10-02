from __future__ import annotations

from typing import Any


def route_after_triage(state: dict[str, Any]) -> str:
    return "supervisor"


def route_after_supervisor(state: dict[str, Any]) -> str:
    return "data_agent" if state.get("decision") != "request_more_data" else "triage"


def route_after_validation(state: dict[str, Any]) -> str:
    result = state.get("validation_result", "PASS")
    if result == "HUMAN_REVIEW":
        return "human_approval"
    return "response"
