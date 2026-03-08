"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from langchain.agents import AgentState
from dataclasses import dataclass
from typing import Any, Dict

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime
from typing_extensions import TypedDict
import os
import getpass

class ContextSchema(TypedDict):
    model_name: str
    tool_name: str

def call_model(state, runtime: Runtime[ContextSchema]):
    if not os.environ.get("LANGSMITH_API_KEY"):
     os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter API key for langsmith : ")
    if not os.environ.get("GEMINI_API_KEY"):
     os.environ["GEMINI_API_KEY"] = getpass.getpass("Enter API key for Google Gemini : ")
    messages = state["messages"]
    print(" model called with message:", messages)
    if runtime.context is not None:
     base_model=runtime.context.get("model_name")
    else :
     base_model="google_genai:gemini-2.5-flash"
    model = init_chat_model(base_model)
    response = model.invoke(messages)
    print("response:",response)
    return {"messages": [response]}





#ContextSchema={"model_name":"Qwen/Qwen2.5-1.5B-Instruct"}
# Define the graph
graph = (
    StateGraph(AgentState, context_schema=ContextSchema)
    .add_node(call_model)
    .add_edge("__start__", "call_model")
    .compile(name="DynamicAgents")
)

