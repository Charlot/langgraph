import time
from typing import TypedDict
from langgraph.graph import StateGraph
from functools import wraps
from datetime import datetime
import asyncio



class State(TypedDict):
    hello_a: str
    hello_b: str
    hello_c: str
    hello_d: str
    hello_e: str

def node_a(state: State) -> State:
    print("node_a")
    return {"hello_a": "hello_a"}

def route_fun_a_1(state: State)->bool:
    print("route_fun_a_1")
    return 1

def node_b(state: State) -> State:
    print("node_b")
    return {"hello_b": "hello_b"}

def node_c(state: State) -> State:
    print("node_c")
    return {"hello_c": "hello_c"}

def node_d(state: State) -> State:
    print("node_d")
    return {"hello_d": "hello_d"}

def node_e(state: State) -> State:
    print("node_e")
    return {"hello_e": "hello_e"}


def test_graph_build() -> None:
    

    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)
    builder.add_node("d", node_d)
    builder.add_node("e", node_e)

    builder.set_entry_point("a")
    builder.add_edge("a", "b")
    builder.add_edge("b", "c")
    builder.add_edge("c", "e")
    builder.add_edge("a", "e")


    graph = builder.compile()

    # display(Image(graph.get_graph().draw_mermaid_png()))
    # print(graph.get_graph().draw_ascii())
    graph.invoke(input={})


if __name__ == "__main__":
    test_graph_build()