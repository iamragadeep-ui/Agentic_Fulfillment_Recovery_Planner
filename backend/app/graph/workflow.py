from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from backend.app.agents.approval import approval_agent
from backend.app.agents.data_agent import data_agent
from backend.app.agents.investigation import investigation_agent
from backend.app.agents.policy_rag import policy_rag_agent
from backend.app.agents.recovery_planner import recovery_planner_agent
from backend.app.agents.response import response_agent
from backend.app.agents.supervisor import supervisor_agent
from backend.app.agents.triage import triage_agent
from backend.app.agents.validator import validator_agent
from backend.app.graph.state import FulfillmentRecoveryState


def _route_after_triage(state: dict[str, Any]) -> str:
    return "supervisor"


def _route_after_supervisor(state: dict[str, Any]) -> str:
    if state.get("decision") == "request_more_data":
        return "triage"
    return "data_agent"


def _route_after_validation(state: dict[str, Any]) -> str:
    result = state.get("validation_result", "PASS")
    if result == "HUMAN_REVIEW":
        return "human_approval"
    return "response"


def build_workflow() -> StateGraph:
    workflow = StateGraph(FulfillmentRecoveryState)
    workflow.add_node("triage", triage_agent)
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("data_agent", data_agent)
    workflow.add_node("policy_rag", policy_rag_agent)
    workflow.add_node("investigation", investigation_agent)
    workflow.add_node("recovery_planner", recovery_planner_agent)
    workflow.add_node("validator", validator_agent)
    workflow.add_node("human_approval", approval_agent)
    workflow.add_node("response", response_agent)

    workflow.add_edge(START, "triage")
    workflow.add_conditional_edges("triage", _route_after_triage, {"supervisor": "supervisor"})
    workflow.add_conditional_edges("supervisor", _route_after_supervisor, {"triage": "triage", "data_agent": "data_agent"})
    workflow.add_edge("data_agent", "policy_rag")
    workflow.add_edge("policy_rag", "investigation")
    workflow.add_edge("investigation", "recovery_planner")
    workflow.add_edge("recovery_planner", "validator")
    workflow.add_conditional_edges("validator", _route_after_validation, {"human_approval": "human_approval", "response": "response"})
    workflow.add_edge("human_approval", "response")
    workflow.add_edge("response", END)
    return workflow
