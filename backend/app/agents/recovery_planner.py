from __future__ import annotations

from typing import Any


def recovery_planner_agent(state: dict[str, Any]) -> dict[str, Any]:
    issue_category = state.get("issue_category", "UNKNOWN")
    investigation = state.get("investigation_result") or {}
    if issue_category == "DELAYED_SHIPMENT":
        recovery_plan = {
            "recovery_strategy": "Carrier recovery and customer communication",
            "actions": ["notify_customer", "create_carrier_escalation", "schedule_follow_up"],
            "reason": "Carrier delay exceeded SLA and policy requires escalation and communication.",
            "policy_basis": ["Fulfillment Recovery Policy Section 4.2", "Carrier Exception Procedure Section 7.1"],
            "risk_level": "MEDIUM",
            "estimated_confidence": 0.9,
            "human_approval_required": True,
        }
    elif issue_category == "INVENTORY_SHORTAGE":
        recovery_plan = {
            "recovery_strategy": "Inventory reallocation",
            "actions": ["request_inventory_reallocation", "notify_customer", "schedule_follow_up"],
            "reason": "Customer order can be fulfilled from an alternate warehouse if available.",
            "policy_basis": ["Inventory Reallocation Policy Section 3.1"],
            "risk_level": "MEDIUM",
            "estimated_confidence": 0.8,
            "human_approval_required": True,
        }
    else:
        recovery_plan = {
            "recovery_strategy": "Escalation and investigation",
            "actions": ["create_support_case"],
            "reason": "The issue requires more evidence before a consequential recovery action is recommended.",
            "policy_basis": ["Fulfillment Recovery Policy Section 4.2"],
            "risk_level": "LOW",
            "estimated_confidence": 0.4,
            "human_approval_required": False,
        }

    return {"recovery_plan": recovery_plan, "proposed_actions": recovery_plan["actions"], "current_stage": "recovery_planning"}
