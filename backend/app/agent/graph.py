from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from app.agent.llm import llm
from app.agent.tools import (
    log_interaction_tool,
    edit_interaction_tool,
    suggest_follow_up_tool,
    hcp_lookup_tool,
    material_recommendation_tool,
)


class AgentState(TypedDict):
    input: str
    intent: str
    output: dict


def intent_router_node(state: AgentState):
    prompt = f"""
Classify the user's CRM request into exactly one intent.

Allowed intents:
- log_interaction
- edit_interaction
- suggest_follow_up
- hcp_lookup
- material_recommendation

Return only the intent text. No explanation.

User request:
{state["input"]}
"""

    response = llm.invoke(prompt)
    intent = response.content.strip().lower()

    allowed = {
        "log_interaction",
        "edit_interaction",
        "suggest_follow_up",
        "hcp_lookup",
        "material_recommendation",
    }

    if intent not in allowed:
        intent = "log_interaction"

    return {"intent": intent}


def log_interaction_node(state: AgentState):
    result = log_interaction_tool.invoke(state["input"])
    return {"output": result}


def edit_interaction_node(state: AgentState):
    result = edit_interaction_tool.invoke(state["input"])
    return {"output": result}


def suggest_follow_up_node(state: AgentState):
    result = suggest_follow_up_tool.invoke(state["input"])
    return {"output": result}


def hcp_lookup_node(state: AgentState):
    result = hcp_lookup_tool.invoke(state["input"])
    return {"output": result}


def material_recommendation_node(state: AgentState):
    result = material_recommendation_tool.invoke(state["input"])
    return {"output": result}


def route_by_intent(state: AgentState) -> Literal[
    "log_interaction",
    "edit_interaction",
    "suggest_follow_up",
    "hcp_lookup",
    "material_recommendation"
]:
    return state["intent"]


builder = StateGraph(AgentState)

builder.add_node("intent_router", intent_router_node)
builder.add_node("log_interaction", log_interaction_node)
builder.add_node("edit_interaction", edit_interaction_node)
builder.add_node("suggest_follow_up", suggest_follow_up_node)
builder.add_node("hcp_lookup", hcp_lookup_node)
builder.add_node("material_recommendation", material_recommendation_node)

builder.set_entry_point("intent_router")

builder.add_conditional_edges(
    "intent_router",
    route_by_intent,
    {
        "log_interaction": "log_interaction",
        "edit_interaction": "edit_interaction",
        "suggest_follow_up": "suggest_follow_up",
        "hcp_lookup": "hcp_lookup",
        "material_recommendation": "material_recommendation",
    }
)

builder.add_edge("log_interaction", END)
builder.add_edge("edit_interaction", END)
builder.add_edge("suggest_follow_up", END)
builder.add_edge("hcp_lookup", END)
builder.add_edge("material_recommendation", END)

graph = builder.compile()