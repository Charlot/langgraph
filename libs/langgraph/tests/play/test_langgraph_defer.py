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

def test_error_defer():
    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c, defer=True)
    builder.add_node("d", node_d, defer=True)

    builder.set_entry_point("a")

    builder.add_edge("a", "b")
    builder.add_edge("a", "c")
    builder.add_edge("a", "d")
    builder.add_edge("b", "d")
    builder.add_edge("c", "d")

    builder.set_finish_point("d")


    graph = builder.compile()

    # display_graph(graph)
    # print(graph.get_graph().draw_ascii())
    graph.invoke(input={})


def test_multi_error_defer():
    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)
    builder.add_node("d", node_d)
    builder.add_node("e", node_e)

    builder.add_node("f", node_f, defer=True)
    builder.add_node("g", node_g, defer=True)
    builder.add_node("h", node_h, defer=True)

    builder.add_edge("a", "b")
    builder.add_edge("a", "c")
    builder.add_edge("a", "d")
    builder.add_edge("a", "e")

    builder.add_edge("b", "f")
    builder.add_edge("c", "f")

    builder.add_edge("d", "g")
    builder.add_edge("e", "g")

    builder.add_edge("d", "h")
    builder.add_edge("f", "h")
    builder.add_edge("g", "h")

    builder.set_entry_point("a")
    builder.set_finish_point("h")

    graph = builder.compile()

    # display_graph(graph=graph)
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

    display(Image(graph.get_graph().draw_mermaid_png()))
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

def display_graph(graph) -> None:
    """Display graph"""

    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    png_data = graph.get_graph().draw_mermaid_png()
    if png_data:
        img = mpimg.imread(BytesIO(png_data), format='png')
        plt.imshow(img)
        plt.axis('off')
        plt.show()


    

if __name__ == "__main__":
    test_multi_error_defer()