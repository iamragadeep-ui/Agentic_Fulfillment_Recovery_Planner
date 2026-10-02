from __future__ import annotations

import logging
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.graph.workflow import build_workflow
from backend.app.schemas import ApprovalRequest, ChatRequest, ChatResponse, WorkflowSummary
from backend.app.services.memory_service import memory_service
from backend.app.tools.fulfillment_tools import get_order

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("fulfillment_app")

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/orders/{order_id}")
async def get_order_endpoint(order_id: str) -> dict[str, object]:
    try:
        return get_order(order_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id or str(uuid4())
    workflow_id = str(uuid4())
    if not request.user_query.strip():
        raise HTTPException(status_code=400, detail="user_query is required")

    memory_service.add_message(session_id, "user", request.user_query)
    initial_state = {
        "session_id": session_id,
        "workflow_id": workflow_id,
        "user_id": request.user_id or "demo-user",
        "user_query": request.user_query,
        "conversation_history": memory_service.get_session_history(session_id),
        "entities": {"order_id": request.order_id, "customer_id": None},
        "issue_category": "UNKNOWN",
        "priority": "MEDIUM",
        "confidence": 0.0,
        "retrieved_documents": [],
        "tool_results": [],
        "errors": [],
        "retry_count": 0,
        "current_stage": "start",
    }

    workflow = build_workflow().compile()
    result = workflow.invoke(initial_state)
    memory_service.save_workflow_state(workflow_id, result)
    memory_service.add_message(session_id, "assistant", result.get("final_response", ""))
    response = ChatResponse(
        session_id=session_id,
        workflow_id=workflow_id,
        status="completed",
        intent=result.get("intent", "recover_fulfillment_exception"),
        issue_category=result.get("issue_category", "UNKNOWN"),
        final_response=result.get("final_response", "No response generated."),
        evidence=result.get("investigation_result", {}).get("evidence", []),
        citations=[doc["title"] for doc in result.get("retrieved_documents", [])],
        recovery_plan=result.get("recovery_plan"),
        approval_status=result.get("approval_status"),
    )
    return response


@app.post("/api/agent/run")
async def run_agent(request: dict[str, str]) -> dict[str, object]:
    return {"status": "ok", "message": "agent workflow executed", "request": request}


@app.post("/api/documents/upload")
async def upload_documents() -> dict[str, str]:
    return {"status": "ok", "message": "document upload endpoint ready"}


@app.post("/api/documents/ingest")
async def ingest_documents() -> dict[str, str]:
    return {"status": "ok", "message": "ingest endpoint ready"}


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str) -> dict[str, object]:
    return {"session_id": session_id, "messages": memory_service.get_session_history(session_id)}


@app.get("/api/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str) -> WorkflowSummary:
    state = memory_service.get_workflow_state(workflow_id)
    if not state:
        raise HTTPException(status_code=404, detail="workflow not found")
    return WorkflowSummary(
        workflow_id=workflow_id,
        session_id=state.get("session_id", "unknown"),
        status="completed",
        current_stage=state.get("current_stage", "response"),
        confidence=float(state.get("confidence", 0.0)),
        validation_result=state.get("validation_result"),
        human_approval=state.get("approval_status"),
        final_response=state.get("final_response"),
    )


@app.post("/api/approval/{workflow_id}")
async def approval_endpoint(workflow_id: str, request: ApprovalRequest) -> dict[str, str]:
    state = memory_service.get_workflow_state(workflow_id)
    state["human_approval"] = {"decision": request.decision, "notes": request.notes or ""}
    memory_service.save_workflow_state(workflow_id, state)
    return {"workflow_id": workflow_id, "approval_status": request.decision}


@app.get("/api/metrics")
async def metrics() -> dict[str, str]:
    return {"status": "ok", "metrics": "placeholder"}
