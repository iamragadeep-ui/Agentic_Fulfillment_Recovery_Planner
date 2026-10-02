from __future__ import annotations

from typing import Any


def investigation_agent(state: dict[str, Any]) -> dict[str, Any]:
    issue_category = state.get("issue_category", "UNKNOWN")
    shipment = state.get("shipment_data") or {}
    events = state.get("carrier_events") or []
    policy_context = state.get("policy_context", "")

    if issue_category == "DELAYED_SHIPMENT":
        root_cause = "Shipment remained stalled at the regional distribution center beyond the carrier SLA."
        evidence = [
            f"Order {state.get('entities', {}).get('order_id')} was shipped successfully.",
            f"Carrier event includes: {events[0].get('event', 'No movement beyond hub') if events else 'No carrier events available'}",
            "Delivery SLA has been exceeded based on the current shipment status.",
        ]
        recommended_action = "Create carrier escalation and schedule follow-up with customer notification."
        confidence = 0.92
        requires_human_review = True
    else:
        root_cause = "The issue was not sufficiently evidenced by operational data and policy retrieval."
        evidence = ["Insufficient evidence for a confident determination."]
        recommended_action = "Request additional order or shipment data."
        confidence = 0.45
        requires_human_review = True

    return {
        "investigation_result": {
            "issue_type": "CARRIER_DELAY" if issue_category == "DELAYED_SHIPMENT" else issue_category,
            "root_cause_summary": root_cause,
            "evidence": evidence,
            "policy_references": ["Fulfillment Recovery Policy Section 4.2", "Carrier Exception Procedure Section 7.1"],
            "recommended_action": recommended_action,
            "confidence": confidence,
            "requires_human_review": requires_human_review,
        },
        "confidence": confidence,
        "current_stage": "investigation",
    }
