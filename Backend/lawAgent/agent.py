from Nodes.state import State
from Nodes.gaurd import gaurdrail
from Nodes.redirector import redirection
from Nodes.summerizer import SummerizerNode
from Nodes.final import FinalNode
from Nodes.orchestrator import sub_graph

from langgraph.graph import StateGraph, START, END

from typing import Literal

# Conditional Node 
def gaurdrail_to_others(state:State) -> Literal["Redirector","Normal","DeadEnd"]:
    if(state["gaurd_index"] == 0):
        return "Normal"
    elif(state["gaurd_index"] > 0 and state["gaurd_index"] < 3):
        return "Redirector"
    else:
        return "DeadEnd"

def pre_end(state:State):
    return state

builder = StateGraph(State)
builder.add_node("gaudrail", gaurdrail)
builder.add_node("redirector", redirection)
builder.add_node("summerizer", SummerizerNode)
builder.add_node("orchestrator_worker", sub_graph)
builder.add_node("pre_end", pre_end)
builder.add_node("final_answer",FinalNode)

builder.add_edge(START, "gaudrail")
builder.add_conditional_edges(
    "gaudrail", gaurdrail_to_others,
    {
        "Normal":"orchestrator_worker",
        "Redirector":"redirector",
        "DeadEnd":END
    })
builder.add_edge("redirector", END)
builder.add_edge("orchestrator_worker", "final_answer")
builder.add_edge("orchestrator_worker", "summerizer")
builder.add_edge("final_answer", "pre_end")
builder.add_node("summerizer", "pre_end")
builder.add_edge("pre_end", END)

agent = builder.compile()