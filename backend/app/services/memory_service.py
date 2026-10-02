from __future__ import annotations

from collections import defaultdict
from typing import Any


class MemoryService:
    def __init__(self) -> None:
        self.session_history: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.workflow_state: dict[str, dict[str, Any]] = {}

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.session_history[session_id].append({"role": role, "content": content})

    def get_session_history(self, session_id: str) -> list[dict[str, Any]]:
        return self.session_history.get(session_id, [])

    def save_workflow_state(self, workflow_id: str, state: dict[str, Any]) -> None:
        self.workflow_state[workflow_id] = state

    def get_workflow_state(self, workflow_id: str) -> dict[str, Any]:
        return self.workflow_state.get(workflow_id, {})


memory_service = MemoryService()
