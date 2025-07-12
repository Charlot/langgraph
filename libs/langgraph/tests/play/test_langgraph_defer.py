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
    hello_f: str

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

def node_f(state: State) -> State:
    print("node_f")
    return {"hello_f": "hello_f"}

def node_g(state: State) -> State:
    print("node_g")
    return {"hello_g": "hello_g"}

def test_defer():
    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)
    builder.add_node("d", node_d, defer=True)
    builder.add_node("f", node_f, defer=True)

    builder.set_entry_point("a")

    builder.add_edge("a", "b")
    builder.add_edge("a", "c")
    builder.add_edge("a", "d")
    builder.add_edge("a", "f")
    builder.add_edge("b", "f")
    builder.add_edge("c", "f")
    builder.add_edge("d", "f")

    builder.set_finish_point("f")


    graph = builder.compile()

    # display(Image(graph.get_graph().draw_mermaid_png()))
    # print(graph.get_graph().draw_ascii())
    graph.invoke(input={})



def test_graph_build(defer=False) -> None:
    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)
    builder.add_node("d", node_d)
    builder.add_node("e", node_e, defer=defer)

    builder.set_entry_point("a")
    builder.add_edge("a", "b")
    builder.add_edge("b", "c")
    builder.add_edge("c", "e")
    builder.add_edge("a", "e")
    builder.add_edge("e", "d")
    builder.set_finish_point("d")

    graph = builder.compile()

    # display(Image(graph.get_graph().draw_mermaid_png()))
    # print(graph.get_graph().draw_ascii())
    graph.invoke(input={})

def test_multi_defer():
    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)
    builder.add_node("d", node_d)
    builder.add_node("e", node_e, defer=True)
    builder.add_node("f", node_f)
    builder.add_node("g", node_g, defer=True)

    builder.set_entry_point("a")
    builder.add_edge("a", "b")
    builder.add_edge("b", "c")
    builder.add_edge("c", "e")
    builder.add_edge("a", "e")
    builder.add_edge("e", "d")
    builder.add_edge("e", "f")
    builder.add_edge("d", "g")

    builder.set_finish_point("g")

    graph = builder.compile()

    # display(Image(graph.get_graph().draw_mermaid_png()))
    # print(graph.get_graph().draw_ascii())
    graph.invoke(input={})


if __name__ == "__main__":
    test_defer()