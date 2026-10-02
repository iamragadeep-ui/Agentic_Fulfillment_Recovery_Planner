from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, Column, DateTime, MetaData, String, Table, create_engine, select, update
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool

from backend.app.config import settings

metadata = MetaData()
sessions = Table(
    "conversation_sessions",
    metadata,
    Column("session_id", String(255), primary_key=True),
    Column("user_id", String(255), nullable=False, index=True),
    Column("messages", JSON, nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)
workflows = Table(
    "workflow_states",
    metadata,
    Column("workflow_id", String(255), primary_key=True),
    Column("session_id", String(255), nullable=False, index=True),
    Column("user_id", String(255), nullable=False, index=True),
    Column("state", JSON, nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)


def create_storage_engine(database_url: str, app_env: str) -> Engine:
    if app_env.lower() == "production" and not database_url.startswith(
        ("postgres://", "postgresql://", "postgresql+psycopg2://")
    ):
        raise RuntimeError("Production requires a PostgreSQL DATABASE_URL.")

    if database_url.startswith("postgres://"):
        database_url = "postgresql://" + database_url.removeprefix("postgres://")

    options: dict[str, Any] = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        options["connect_args"] = {"check_same_thread": False}
        if database_url in {"sqlite://", "sqlite:///:memory:"}:
            options["poolclass"] = StaticPool
    else:
        options.update({"pool_size": 1, "max_overflow": 0})

    return create_engine(database_url, **options)


class MemoryService:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        metadata.create_all(self.engine)

    def add_message(self, session_id: str, user_id: str, role: str, content: str) -> None:
        now = datetime.now(timezone.utc)
        with self.engine.begin() as connection:
            row = connection.execute(
                select(sessions).where(sessions.c.session_id == session_id)
            ).mappings().one_or_none()
            if row and row["user_id"] != user_id:
                raise PermissionError("Session does not belong to this user.")

            messages = list(row["messages"]) if row else []
            messages.append({"role": role, "content": content})
            if row:
                connection.execute(
                    update(sessions)
                    .where(sessions.c.session_id == session_id)
                    .values(messages=messages, updated_at=now)
                )
            else:
                connection.execute(
                    sessions.insert().values(
                        session_id=session_id,
                        user_id=user_id,
                        messages=messages,
                        updated_at=now,
                    )
                )

    def get_session_history(self, session_id: str, user_id: str) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            row = connection.execute(
                select(sessions).where(sessions.c.session_id == session_id)
            ).mappings().one_or_none()
        if not row:
            return []
        if row["user_id"] != user_id:
            raise PermissionError("Session does not belong to this user.")
        return list(row["messages"])

    def save_workflow_state(self, workflow_id: str, user_id: str, state: dict[str, Any]) -> None:
        now = datetime.now(timezone.utc)
        with self.engine.begin() as connection:
            row = connection.execute(
                select(workflows).where(workflows.c.workflow_id == workflow_id)
            ).mappings().one_or_none()
            if row and row["user_id"] != user_id:
                raise PermissionError("Workflow does not belong to this user.")

            values = {
                "session_id": state.get("session_id", "unknown"),
                "user_id": user_id,
                "state": state,
                "updated_at": now,
            }
            if row:
                connection.execute(
                    update(workflows)
                    .where(workflows.c.workflow_id == workflow_id)
                    .values(**values)
                )
            else:
                connection.execute(
                    workflows.insert().values(workflow_id=workflow_id, **values)
                )

    def get_workflow_state(self, workflow_id: str, user_id: str) -> dict[str, Any]:
        with self.engine.connect() as connection:
            row = connection.execute(
                select(workflows).where(workflows.c.workflow_id == workflow_id)
            ).mappings().one_or_none()
        if not row or row["user_id"] != user_id:
            return {}
        return dict(row["state"])


engine = create_storage_engine(settings.database_url, settings.app_env)
memory_service = MemoryService(engine)
