from __future__ import annotations

from typing import Any

from backend.app.rag.vector_store import vector_store


def policy_rag_agent(state: dict[str, Any]) -> dict[str, Any]:
    query = state.get("user_query", "") + " " + (state.get("issue_category") or "")
    results = vector_store.search_documents(query=query, limit=3)
    policy_context = "\n\n".join(f"{item['title']} ({item['section']}): {item['excerpt']}" for item in results)
    return {
        "retrieved_documents": results,
        "policy_context": policy_context,
        "current_stage": "policy_retrieval",
    }
