from __future__ import annotations

from typing import Any

from backend.app.data.synthetic_data import DATASTORE


def get_customer(customer_id: str) -> dict[str, Any]:
    customer = DATASTORE.get_customer(customer_id)
    if not customer:
        raise ValueError(f"Customer {customer_id} was not found.")
    return {"success": True, "data": customer}


def get_order(order_id: str) -> dict[str, Any]:
    order = DATASTORE.get_order(order_id)
    if not order:
        raise ValueError(f"Order {order_id} was not found.")
    return {"success": True, "data": order}


def get_order_items(order_id: str) -> dict[str, Any]:
    items = DATASTORE.get_order_items(order_id)
    return {"success": True, "data": items}


def get_inventory(product_id: str) -> dict[str, Any]:
    return {"success": True, "data": DATASTORE.get_inventory(product_id)}


def get_inventory_by_location(product_id: str, location: str | None = None) -> dict[str, Any]:
    return {"success": True, "data": DATASTORE.get_inventory_by_location(product_id, location)}


def get_warehouse_status(warehouse_id: str) -> dict[str, Any]:
    warehouse = DATASTORE.get_warehouse_status(warehouse_id)
    if not warehouse:
        raise ValueError(f"Warehouse {warehouse_id} was not found.")
    return {"success": True, "data": warehouse}


def get_shipment(order_id: str) -> dict[str, Any]:
    shipment = DATASTORE.get_shipment(order_id)
    if not shipment:
        raise ValueError(f"Shipment for order {order_id} was not found.")
    return {"success": True, "data": shipment}


def get_tracking(order_id: str) -> dict[str, Any]:
    shipment = DATASTORE.get_shipment(order_id)
    if not shipment:
        raise ValueError(f"Tracking for order {order_id} was not found.")
    return {"success": True, "data": {"tracking_number": shipment["tracking_number"], "carrier": shipment["carrier"]}}


def get_carrier_events(tracking_number: str) -> dict[str, Any]:
    events = DATASTORE.get_carrier_events(tracking_number)
    return {"success": True, "data": events}


def get_fulfillment_history(order_id: str) -> dict[str, Any]:
    history = DATASTORE.get_fulfillment_history(order_id)
    return {"success": True, "data": history}


def get_customer_case_history(customer_id: str) -> dict[str, Any]:
    history = DATASTORE.get_customer_case_history(customer_id)
    return {"success": True, "data": history}


def create_support_case(case_summary: str) -> dict[str, Any]:
    return {"success": True, "case_id": "CASE-9001", "details": case_summary}


def create_carrier_escalation(tracking_number: str) -> dict[str, Any]:
    return {"success": True, "escalation_id": "ESC-9001", "tracking_number": tracking_number}


def create_replacement_request(order_id: str) -> dict[str, Any]:
    return {"success": True, "replacement_id": f"RPL-{order_id}", "order_id": order_id}


def request_inventory_reallocation(product_id: str, location: str) -> dict[str, Any]:
    return {"success": True, "product_id": product_id, "location": location, "status": "reallocation_requested"}


def create_refund_request(order_id: str, amount: float) -> dict[str, Any]:
    return {"success": True, "refund_id": f"REF-{order_id}", "amount": amount}


def schedule_follow_up(order_id: str, date: str) -> dict[str, Any]:
    return {"success": True, "follow_up_id": f"FU-{order_id}", "date": date}


def send_customer_notification(order_id: str) -> dict[str, Any]:
    return {"success": True, "notification_id": f"NOTIFY-{order_id}", "status": "sent"}


def update_fulfillment_case(case_id: str, status: str) -> dict[str, Any]:
    return {"success": True, "case_id": case_id, "status": status}
