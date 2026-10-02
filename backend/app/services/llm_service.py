from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from backend.app.config import settings


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def classify_issue(self, user_query: str, order_id: str | None = None) -> dict[str, Any]:
        text = (user_query or "").lower()
        if (
            "delayed" in text
            or "hasn't arrived" in text
            or "has not arrived" in text
            or "supposed to arrive" in text
            or "late" in text
            or "not arrived" in text
        ):
            category = "DELAYED_SHIPMENT"
        elif "lost" in text:
            category = "LOST_SHIPMENT"
        elif "inventory" in text or "out of stock" in text:
            category = "INVENTORY_SHORTAGE"
        elif "damaged" in text:
            category = "DAMAGED_DELIVERY"
        elif "address" in text:
            category = "ADDRESS_EXCEPTION"
        else:
            category = "UNKNOWN"

        return {
            "intent": "recover_fulfillment_exception",
            "category": category,
            "priority": "HIGH" if "urgent" in text or order_id else "MEDIUM",
            "confidence": 0.92,
            "recommended_route": "fulfillment_data_agent",
        }

    def generate_policy_summary(self, question: str, documents: list[str]) -> str:
        if not documents:
            return "No policy evidence was retrieved."
        summary = "The relevant policy guidance is: " + " | ".join(documents[:3])
        return summary


llm_service = LLMService()
