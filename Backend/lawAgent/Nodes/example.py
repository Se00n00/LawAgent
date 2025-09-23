from langgraph.graph import StateGraph, START
from typing import TypedDict

# Parent state
class ParentState(TypedDict):
    foo: str

# Subgraph state — includes foo (shared) plus extra keys
class SubState(TypedDict):
    foo: str     # shared key
    bar: str     # private to the subgraph

# Define subgraph
def sub_node1(state: SubState) -> dict:
    return {"bar": "hello"}  # set bar

def sub_node2(state: SubState) -> dict:
    # use foo and bar (both available)
    return {"foo": state["foo"] + state["bar"]}

sub_builder = StateGraph(SubState)
sub_builder.add_node("set_bar", sub_node1)
sub_builder.add_node("concat_foo_bar", sub_node2)
sub_builder.add_edge(START, "set_bar")
sub_builder.add_edge("set_bar", "concat_foo_bar")
subgraph_compiled = sub_builder.compile()

# Parent graph
def parent_node(state: ParentState) -> dict:
    return {"foo": "start: " + state["foo"]}

parent_builder = StateGraph(ParentState)
parent_builder.add_node("parent_start", parent_node)

# Add the compiled subgraph as a node
parent_builder.add_node("subgraph", subgraph_compiled)

# Build edges
parent_builder.add_edge(START, "parent_start")
parent_builder.add_edge("parent_start", "subgraph")

parent_graph = parent_builder.compile()

# Invoke
res = parent_graph.invoke({"foo": "world"})
print(res)  # foo should be something like "start: worldhello" etc.
