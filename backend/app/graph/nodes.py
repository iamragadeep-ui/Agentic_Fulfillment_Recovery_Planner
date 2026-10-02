from __future__ import annotations

from backend.app.agents.approval import approval_agent
from backend.app.agents.data_agent import data_agent
from backend.app.agents.investigation import investigation_agent
from backend.app.agents.policy_rag import policy_rag_agent
from backend.app.agents.recovery_planner import recovery_planner_agent
from backend.app.agents.response import response_agent
from backend.app.agents.supervisor import supervisor_agent
from backend.app.agents.triage import triage_agent
from backend.app.agents.validator import validator_agent

NODE_MAP = {
    "triage": triage_agent,
    "supervisor": supervisor_agent,
    "data_agent": data_agent,
    "policy_rag": policy_rag_agent,
    "investigation": investigation_agent,
    "recovery_planner": recovery_planner_agent,
    "validator": validator_agent,
    "human_approval": approval_agent,
    "response": response_agent,
}
