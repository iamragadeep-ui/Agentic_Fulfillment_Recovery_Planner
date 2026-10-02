from __future__ import annotations

from typing import Any

from backend.app.data.synthetic_data import DATASTORE


class PolicyVectorStore:
    def __init__(self) -> None:
        self.documents = DATASTORE.get_policy_documents()

    def add_documents(self, documents: list[dict[str, Any]]) -> None:
        self.documents.extend(
            [
                type("Doc", (), {"document_id": doc["document_id"], "title": doc["title"], "source": doc["source"], "content": doc["content"], "category": doc.get("category", "fulfillment_policy"), "section": doc.get("section"), "version": doc.get("version"), "effective_date": doc.get("effective_date")})()
                for doc in documents
            ]
        )

    def search_documents(self, query: str, category: str | None = None, limit: int = 3) -> list[dict[str, Any]]:
        normalized_query = (query or "").lower()
        rows: list[tuple[float, dict[str, Any]]] = []
        for doc in self.documents:
            if category and doc.category != category:
                continue
            score = 0.0
            for token in normalized_query.split():
                if token in (doc.title.lower() + " " + doc.content.lower()):
                    score += 1.0
            if score > 0 or not normalized_query:
                rows.append((score, {"document_id": doc.document_id, "title": doc.title, "source": doc.source, "section": doc.section, "excerpt": doc.content[:220], "score": round(score, 2), "category": doc.category}))
        rows.sort(key=lambda item: item[0], reverse=True)
        return [row[1] for row in rows[:limit]]

    def metadata_filter(self, category: str | None = None) -> list[dict[str, Any]]:
        if not category:
            return [self._serialise(doc) for doc in self.documents]
        return [self._serialise(doc) for doc in self.documents if doc.category == category]

    @staticmethod
    def _serialise(doc: Any) -> dict[str, Any]:
        return {
            "document_id": doc.document_id,
            "title": doc.title,
            "source": doc.source,
            "category": doc.category,
            "section": doc.section,
            "version": doc.version,
            "effective_date": doc.effective_date,
            "content": doc.content,
        }


vector_store = PolicyVectorStore()
