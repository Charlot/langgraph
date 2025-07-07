from langgraph.graph import StateGraph,START,END
from typing import TypedDict
import copy

class State(TypedDict):
    hello_a: str
    hello_b: str
    hello_c: str
    hello_d: str

def node_a(state: State) -> State:
    return {"hello_a": "hello_a"}

def route_fun(state: State)->bool:
    return 0

def node_b(state: State) -> State:
    return {"hello_b": "hello_b"}

def node_c(state: State) -> State:
    return {"hello_c": "hello_c"}

def node_d(state: State) -> State:
    return {"hello_d": "hello_d"}


def test_conditional_edge() -> None:
    builder=StateGraph(State)
    builder.add_node("a",node_a)
    builder.add_node("b",node_b)
    builder.add_node("c",node_c)
    builder.add_node("d",node_d)

    builder.add_edge(START, "a")
    builder.add_node("branch", lambda x:x)
    builder.add_conditional_edges("a", path=route_fun,path_map={0:"branch",1:"d"})
    builder.add_edge("branch", "b")
    builder.add_edge("branch", "c")
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())

    graph.invoke(input={})


if __name__ == "__main__":
    test_conditional_edge()



