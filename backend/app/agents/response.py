from __future__ import annotations

from typing import Any


def response_agent(state: dict[str, Any]) -> dict[str, Any]:
    issue = state.get("issue_category", "UNKNOWN")
    order = state.get("order_data") or {}
    plan = state.get("recovery_plan") or {}
    evidence = state.get("investigation_result", {}).get("evidence", [])
    citations = [item["title"] + " " + (item.get("section") or "") for item in state.get("retrieved_documents", [])]

    response = (
        f"We reviewed the fulfillment issue for order {order.get('order_id', 'unknown')} and classified it as {issue}. "
        f"The shipment has tracking evidence indicating a carrier delay at the regional distribution center. "
        f"The recommended path is: {plan.get('recovery_strategy', 'continue monitoring')}. "
        f"Known facts: {', '.join(evidence) if evidence else 'No explicit evidence available.'}"
    )
    if state.get("approval_status") == "pending":
        response += " This plan is pending review by an authorized approver; no recovery action has been executed."

    return {"final_response": response, "current_stage": "response", "citations": citations}
