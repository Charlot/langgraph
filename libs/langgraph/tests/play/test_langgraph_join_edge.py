import asyncio
from datetime import datetime
from functools import wraps
from io import BytesIO
from typing import TypedDict

from IPython.display import Image, display

from langgraph.graph import StateGraph


class State(TypedDict):
    hello_a: str
    hello_b: str
    hello_c: str
    hello_d: str
    hello_e: str
    hello_f: str
    hello_g: str
    hello_h: str
    hello_i: str

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

def node_h(state: State) -> State:
    print("node_h")
    return {"hello_h": "hello_h"}

def node_i(state: State) -> State:
    print("node_i")
    return {"hello_i": "hello_i"}


def test_join_edge():
    buider = StateGraph(State)
    buider.add_node("a", node_a)
    buider.add_node("b", node_b)
    buider.add_node("c", node_c)

    buider.add_edge(["a", "b"], "c")
    buider.set_entry_point("a")
    buider.set_entry_point("b")

    buider.set_finish_point("c")

    graph = buider.compile()

    # print(graph.get_graph().draw_ascii())

    graph.invoke({})

def test_join_edge_defer():
    buider = StateGraph(State)
    buider.add_node("a", node_a)
    buider.add_node("b", node_b)
    buider.add_node("c", node_c, defer=True)

    buider.add_edge(["a", "b"], "c")
    buider.set_entry_point("a")
    buider.set_entry_point("b")

    buider.set_finish_point("c")

    graph = buider.compile()

    # print(graph.get_graph().draw_ascii())

    graph.invoke({})


if __name__ == "__main__":
    test_join_edge_defer()