from langgraph.graph import StateGraph,START,END
from typing import TypedDict
import copy

class State(TypedDict):
    hello_a: str
    hello_b: str
    hello_c: str
    hello_d: str

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


def test_conditional_edge_branch_merge() -> None:
    """简单merge测试    
    """
    builder=StateGraph(State)
    builder.add_node("a",node_a)
    builder.add_node("b",node_b)
    builder.add_node("c",node_c)
    builder.add_node("d",node_d)
    builder.add_node("e",node_e)

    builder.add_edge(START, "a")
    builder.add_node("branch", lambda x:{})
    builder.add_conditional_edges("a", path=route_fun_a_1,path_map={0:"branch",1:"d"})
    builder.add_edge("branch", "b")
    builder.add_edge("branch", "c")
    builder.add_edge("b", "e")
    builder.add_edge("c", "e")
    builder.add_edge("d", "e")
    builder.add_edge("e", END)
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())

    graph.invoke(input={})





if __name__ == "__main__":
    test_conditional_edge_branch_merge()



