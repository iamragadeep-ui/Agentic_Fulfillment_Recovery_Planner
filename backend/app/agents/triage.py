from __future__ import annotations

import re
from typing import Any

from backend.app.services.llm_service import llm_service


def triage_agent(state: dict[str, Any]) -> dict[str, Any]:
    query = state.get("user_query", "")
    order_id = state.get("entities", {}).get("order_id") if state.get("entities") else None
    detected = llm_service.classify_issue(query, order_id)
    new_state = {
        "intent": detected["intent"],
        "issue_category": detected["category"],
        "priority": detected["priority"],
        "confidence": detected["confidence"],
        "recommended_route": detected["recommended_route"],
        "missing_information": [],
        "current_stage": "triage",
    }
    extracted_order_id = None
    matches = re.findall(r"\bORD\d+\b", query.upper())
    if matches:
        extracted_order_id = matches[0]
    if extracted_order_id:
        order_id = extracted_order_id
    if order_id:
        new_state["entities"] = {"order_id": order_id, "customer_id": state.get("entities", {}).get("customer_id") if state.get("entities") else None}
    else:
        new_state["entities"] = {"order_id": None, "customer_id": None}
    return new_state
