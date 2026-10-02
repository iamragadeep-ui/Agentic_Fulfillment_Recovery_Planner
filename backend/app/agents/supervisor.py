from __future__ import annotations

from typing import Any


def supervisor_agent(state: dict[str, Any]) -> dict[str, Any]:
    issue_category = state.get("issue_category", "UNKNOWN")
    if not state.get("entities", {}).get("order_id"):
        return {"missing_information": ["order_id"], "current_stage": "supervisor", "decision": "request_more_data"}
    if issue_category == "UNKNOWN":
        return {"missing_information": ["issue_classification"], "current_stage": "supervisor", "decision": "request_more_data"}
    return {"current_stage": "supervisor", "decision": "continue", "recommended_route": "fulfillment_data_agent"}
