from __future__ import annotations

from typing import Any, TypedDict


class FulfillmentRecoveryState(TypedDict, total=False):
    session_id: str
    workflow_id: str
    user_id: str
    user_query: str
    conversation_history: list[dict[str, Any]]
    intent: str
    issue_category: str
    priority: str
    entities: dict[str, str | None]
    missing_information: list[str]
    customer_data: dict[str, Any]
    order_data: dict[str, Any]
    inventory_data: dict[str, Any]
    warehouse_data: dict[str, Any]
    shipment_data: dict[str, Any]
    carrier_events: list[dict[str, Any]]
    retrieved_documents: list[dict[str, Any]]
    policy_context: str
    investigation_result: dict[str, Any]
    recovery_plan: dict[str, Any]
    proposed_actions: list[str]
    tool_results: list[dict[str, Any]]
    confidence: float
    validation_result: str
    human_approval: dict[str, Any]
    approval_status: str
    retry_count: int
    errors: list[str]
    final_response: str
    current_stage: str
