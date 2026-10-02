from __future__ import annotations

from typing import Any

from backend.app.tools.fulfillment_tools import (
    create_carrier_escalation,
    create_support_case,
    send_customer_notification,
)


def action_agent(state: dict[str, Any]) -> dict[str, Any]:
    plan = state.get("recovery_plan") or {}
    actions = plan.get("actions", [])
    tool_results = []
    for action in actions:
        if action == "notify_customer":
            output = send_customer_notification(state.get("entities", {}).get("order_id") or "ORD123")
        elif action == "create_carrier_escalation":
            output = create_carrier_escalation((state.get("shipment_data") or {}).get("tracking_number") or "TRK-5521")
        elif action == "create_support_case":
            output = create_support_case("Recovery automation created a support case.")
        else:
            output = {"success": True, "status": action}
        tool_results.append({"action": action, **output})
    return {"tool_results": tool_results, "current_stage": "action_execution"}
