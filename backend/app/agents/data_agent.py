from __future__ import annotations

from typing import Any

from backend.app.tools.fulfillment_tools import (
    get_carrier_events,
    get_customer,
    get_customer_case_history,
    get_inventory,
    get_inventory_by_location,
    get_order,
    get_order_items,
    get_shipment,
    get_warehouse_status,
)


def data_agent(state: dict[str, Any]) -> dict[str, Any]:
    order_id = state.get("entities", {}).get("order_id") or "ORD123"
    data = {}
    tool_results = []
    order = get_order(order_id)
    data["order_data"] = order["data"]
    tool_results.append({"tool": "get_order", "status": "success", "input": {"order_id": order_id}})

    customer_id = data["order_data"].get("customer_id")
    if customer_id:
        customer = get_customer(customer_id)
        data["customer_data"] = customer["data"]
        tool_results.append({"tool": "get_customer", "status": "success", "input": {"customer_id": customer_id}})
        history = get_customer_case_history(customer_id)
        data["customer_history"] = history["data"]
        tool_results.append({"tool": "get_customer_case_history", "status": "success", "input": {"customer_id": customer_id}})

    items = get_order_items(order_id)
    data["order_items"] = items["data"]
    tool_results.append({"tool": "get_order_items", "status": "success", "input": {"order_id": order_id}})

    shipment = get_shipment(order_id)
    data["shipment_data"] = shipment["data"]
    tool_results.append({"tool": "get_shipment", "status": "success", "input": {"order_id": order_id}})

    tracking_number = shipment["data"].get("tracking_number")
    if tracking_number:
        events = get_carrier_events(tracking_number)
        data["carrier_events"] = events["data"]
        tool_results.append({"tool": "get_carrier_events", "status": "success", "input": {"tracking_number": tracking_number}})

    for item in items["data"]:
        sku = item["sku"]
        inventory = get_inventory(sku)
        data.setdefault("inventory_data", {})[sku] = inventory["data"]
        tool_results.append({"tool": "get_inventory", "status": "success", "input": {"product_id": sku}})
        break

    warehouse_id = data["order_data"].get("fulfillment_center")
    if warehouse_id:
        warehouse = get_warehouse_status(warehouse_id)
        data["warehouse_data"] = warehouse["data"]
        tool_results.append({"tool": "get_warehouse_status", "status": "success", "input": {"warehouse_id": warehouse_id}})

    return {"customer_data": data.get("customer_data"), "order_data": data.get("order_data"), "inventory_data": data.get("inventory_data"), "warehouse_data": data.get("warehouse_data"), "shipment_data": data.get("shipment_data"), "carrier_events": data.get("carrier_events", []), "tool_results": tool_results, "current_stage": "data_collection"}
