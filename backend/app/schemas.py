from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class IssueCategory(str, Enum):
    DELAYED_SHIPMENT = "DELAYED_SHIPMENT"
    LOST_SHIPMENT = "LOST_SHIPMENT"
    INVENTORY_SHORTAGE = "INVENTORY_SHORTAGE"
    PARTIAL_FULFILLMENT = "PARTIAL_FULFILLMENT"
    CARRIER_EXCEPTION = "CARRIER_EXCEPTION"
    DAMAGED_DELIVERY = "DAMAGED_DELIVERY"
    FAILED_DELIVERY = "FAILED_DELIVERY"
    ADDRESS_EXCEPTION = "ADDRESS_EXCEPTION"
    WAREHOUSE_DELAY = "WAREHOUSE_DELAY"
    ORDER_PROCESSING_ERROR = "ORDER_PROCESSING_ERROR"
    UNKNOWN = "UNKNOWN"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ValidationResult(str, Enum):
    PASS = "PASS"
    RETRY = "RETRY"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    BLOCK = "BLOCK"


class TriageResult(BaseModel):
    intent: str = "recover_fulfillment_exception"
    category: IssueCategory = IssueCategory.UNKNOWN
    priority: Priority = Priority.MEDIUM
    entities: dict[str, str | None] = Field(default_factory=dict)
    missing_information: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    recommended_route: str = "fulfillment_data_agent"


class OrderItem(BaseModel):
    item_id: str
    sku: str
    quantity: int
    unit_price: float
    status: str


class OrderSummary(BaseModel):
    order_id: str
    customer_id: str
    status: str
    fulfillment_center: str
    expected_delivery: str | None = None
    total_value: float
    items: list[OrderItem] = Field(default_factory=list)


class ShipmentSummary(BaseModel):
    order_id: str
    shipment_id: str
    tracking_number: str
    carrier: str
    status: str
    last_event: str
    warehouse_id: str | None = None


class PolicyDocument(BaseModel):
    document_id: str
    title: str
    source: str
    content: str
    category: str
    page: int | None = None
    section: str | None = None
    version: str | None = None
    effective_date: str | None = None


class RetrievalResult(BaseModel):
    document_id: str
    title: str
    source: str
    section: str | None = None
    excerpt: str
    score: float


class InvestigationResult(BaseModel):
    issue_type: str
    root_cause_summary: str
    evidence: list[str]
    policy_references: list[str]
    recommended_action: str
    confidence: float
    requires_human_review: bool = True


class RecoveryPlan(BaseModel):
    recovery_strategy: str
    actions: list[str]
    reason: str
    policy_basis: list[str]
    risk_level: str
    estimated_confidence: float
    human_approval_required: bool = False


class ChatRequest(BaseModel):
    user_query: str
    session_id: str | None = None
    user_id: str | None = None
    order_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    workflow_id: str
    status: str
    intent: str
    issue_category: str
    final_response: str
    evidence: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    recovery_plan: dict[str, Any] | None = None
    approval_status: str | None = None


class ApprovalRequest(BaseModel):
    workflow_id: str
    decision: Literal["approve", "reject", "modify"]
    notes: str | None = None


class AgentRun(BaseModel):
    workflow_id: str
    stage: str
    status: str
    latency_ms: int
    details: dict[str, Any] = Field(default_factory=dict)


class WorkflowSummary(BaseModel):
    workflow_id: str
    session_id: str
    status: str
    current_stage: str
    confidence: float
    validation_result: str | None = None
    human_approval: str | None = None
    final_response: str | None = None
