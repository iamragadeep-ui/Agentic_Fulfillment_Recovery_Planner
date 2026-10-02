from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CustomerRecord:
    customer_id: str
    name: str
    email: str
    loyalty_tier: str


@dataclass
class OrderRecord:
    order_id: str
    customer_id: str
    status: str
    fulfillment_center: str
    expected_delivery: str | None
    total_value: float
    items: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ShipmentRecord:
    order_id: str
    shipment_id: str
    tracking_number: str
    carrier: str
    status: str
    last_event: str
    warehouse_id: str | None = None


@dataclass
class PolicyRecord:
    document_id: str
    title: str
    source: str
    content: str
    category: str
    page: int | None = None
    section: str | None = None
    version: str | None = None
    effective_date: str | None = None


class SyntheticDataStore:
    def __init__(self) -> None:
        self.customers = {
            "CUS101": CustomerRecord("CUS101", "Anya Sharma", "anya.sharma@example.com", "Gold"),
            "CUS102": CustomerRecord("CUS102", "Marcus Lee", "marcus.lee@example.com", "Silver"),
            "CUS103": CustomerRecord("CUS103", "Sofia Patel", "sofia.patel@example.com", "Platinum"),
        }
        self.orders = {
            "ORD123": OrderRecord(
                "ORD123",
                "CUS101",
                "SHIPPED",
                "FC01",
                "2026-10-01",
                245.00,
                [
                    {"item_id": "ITM-1001", "sku": "SKU-AB12", "quantity": 1, "unit_price": 120.0, "status": "SHIPPED"},
                    {"item_id": "ITM-1002", "sku": "SKU-CD34", "quantity": 2, "unit_price": 62.5, "status": "SHIPPED"},
                ],
            ),
            "ORD456": OrderRecord(
                "ORD456",
                "CUS102",
                "PROCESSING",
                "FC02",
                "2026-10-03",
                520.0,
                [{"item_id": "ITM-2001", "sku": "SKU-XF18", "quantity": 1, "unit_price": 500.0, "status": "ALLOCATED"}],
            ),
            "ORD789": OrderRecord(
                "ORD789",
                "CUS103",
                "DELIVERED",
                "FC03",
                "2026-09-20",
                179.0,
                [{"item_id": "ITM-3001", "sku": "SKU-QQ66", "quantity": 1, "unit_price": 179.0, "status": "DELIVERED"}],
            ),
        }
        self.shipments = {
            "ORD123": ShipmentRecord(
                "ORD123",
                "SHP-11",
                "TRK-5521",
                "UPS",
                "IN_TRANSIT",
                "Regional distribution center processing delay",
                "WH-01",
            ),
            "ORD456": ShipmentRecord(
                "ORD456",
                "SHP-22",
                "TRK-2018",
                "FedEx",
                "PENDING",
                "Awaiting warehouse handoff",
                "WH-02",
            ),
        }
        self.carrier_events = {
            "TRK-5521": [
                {"timestamp": "2026-09-28T08:00:00Z", "event": "Package accepted by carrier"},
                {"timestamp": "2026-09-29T14:00:00Z", "event": "Processing delay at regional hub"},
                {"timestamp": "2026-09-30T10:00:00Z", "event": "No movement beyond hub"},
            ],
            "TRK-2018": [
                {"timestamp": "2026-09-30T09:00:00Z", "event": "Order received at fulfillment center"},
            ],
        }
        self.inventory = {
            "SKU-AB12": {"FC01": 0, "FC02": 12, "FC03": 7},
            "SKU-CD34": {"FC01": 5, "FC02": 2, "FC03": 0},
            "SKU-XF18": {"FC01": 0, "FC02": 0, "FC03": 4},
            "SKU-QQ66": {"FC01": 14, "FC02": 6, "FC03": 10},
        }
        self.warehouses = {
            "FC01": {"warehouse_id": "FC01", "status": "OPERATIONAL", "capacity": 80, "region": "West"},
            "FC02": {"warehouse_id": "FC02", "status": "DELAYED", "capacity": 68, "region": "Central"},
            "FC03": {"warehouse_id": "FC03", "status": "OPERATIONAL", "capacity": 96, "region": "East"},
        }
        self.policies = [
            PolicyRecord(
                "POL-001",
                "Fulfillment Recovery Policy",
                "policy_manual.pdf",
                "For delayed shipment cases, a carrier processing delay exceeding 48 hours requires investigation and may authorize a replacement shipment if the package has not moved past the last carrier checkpoint. Customer notification is required for all recovery actions.",
                "fulfillment_policy",
                page=4,
                section="4.2",
                version="v1.0",
                effective_date="2026-01-01",
            ),
            PolicyRecord(
                "POL-002",
                "Carrier Exception Procedure",
                "carrier_sops.pdf",
                "If a shipment remains stalled at a regional distribution center for more than 48 hours, create a carrier escalation and document the last verified movement. Replacement and refund actions require manager approval.",
                "carrier_procedure",
                page=8,
                section="7.1",
                version="v1.0",
                effective_date="2026-01-01",
            ),
            PolicyRecord(
                "POL-003",
                "Inventory Reallocation Policy",
                "inventory_policies.pdf",
                "Inventory shortages at the assigned fulfillment center may be resolved via reallocation from alternate locations if stock is available and customer service is notified.",
                "inventory_policy",
                page=3,
                section="3.1",
                version="v1.2",
                effective_date="2026-01-01",
            ),
        ]

    def get_customer(self, customer_id: str) -> dict[str, Any] | None:
        customer = self.customers.get(customer_id)
        if not customer:
            return None
        return {"customer_id": customer.customer_id, "name": customer.name, "email": customer.email, "loyalty_tier": customer.loyalty_tier}

    def get_order(self, order_id: str) -> dict[str, Any] | None:
        order = self.orders.get(order_id)
        if not order:
            return None
        return {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "status": order.status,
            "fulfillment_center": order.fulfillment_center,
            "expected_delivery": order.expected_delivery,
            "total_value": order.total_value,
            "items": order.items,
        }

    def get_order_items(self, order_id: str) -> list[dict[str, Any]]:
        order = self.orders.get(order_id)
        return order.items if order else []

    def get_inventory(self, product_id: str) -> dict[str, int]:
        return self.inventory.get(product_id, {})

    def get_inventory_by_location(self, product_id: str, location: str | None = None) -> dict[str, Any]:
        result = self.inventory.get(product_id, {})
        if location is None:
            return {"product_id": product_id, "locations": result}
        return {"product_id": product_id, "location": location, "available": result.get(location, 0)}

    def get_warehouse_status(self, warehouse_id: str) -> dict[str, Any]:
        warehouse = self.warehouses.get(warehouse_id)
        return warehouse or {}

    def get_shipment(self, order_id: str) -> dict[str, Any] | None:
        shipment = self.shipments.get(order_id)
        if not shipment:
            return None
        return {
            "order_id": shipment.order_id,
            "shipment_id": shipment.shipment_id,
            "tracking_number": shipment.tracking_number,
            "carrier": shipment.carrier,
            "status": shipment.status,
            "last_event": shipment.last_event,
            "warehouse_id": shipment.warehouse_id,
        }

    def get_carrier_events(self, tracking_number: str) -> list[dict[str, Any]]:
        return self.carrier_events.get(tracking_number, [])

    def get_fulfillment_history(self, order_id: str) -> list[dict[str, Any]]:
        return [{"order_id": order_id, "event": "package shipped", "status": "SHIPPED"}]

    def get_customer_case_history(self, customer_id: str) -> list[dict[str, Any]]:
        if customer_id == "CUS101":
            return [{"case_id": "CASE-940", "issue_type": "DELAYED_SHIPMENT", "resolution": "carrier escalation"}]
        return []

    def get_policy_documents(self) -> list[PolicyRecord]:
        return self.policies


DATASTORE = SyntheticDataStore()
