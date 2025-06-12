from typing import TypedDict,Annotated
import pytest
from langgraph.graph import StateGraph
from langgraph.errors import InvalidUpdateError
from IPython.display import display, Image
import operator
def test_graph_build() -> None:
    class State(TypedDict):
        hello_a: str
        hello_b: str
        hello_c: str
        hello_d: str

    def node_a(state: State) -> State:
        return {"hello_a": "world_a", "hello_a_1": "world_a_1"}
    

    def node_b(state: State) -> State:
        return {"hello_b": "world_c"}
    
    def node_c(state: State) -> State:
        return {"hello_c": "world_c",
                "hello_a": "world_c_a"}
    
    def node_d(state: State) -> State:
        return {"hello_d": "world_d"}

    def node_d_route_fun(state: State)->bool:
        return True

    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)
    builder.add_node("d", node_d)
    builder.set_entry_point("a")
    builder.add_edge("a", "b")
    builder.add_edge("a", "c")
    builder.add_conditional_edges("a", node_d_route_fun, {True: "d", False: "__end__"} )
    graph = builder.compile()
    graph.nodes["a"].node

    # display(Image(graph.get_graph().draw_mermaid_png()))
    # print(graph.get_graph().draw_ascii())


    result = graph.invoke({"helloa": "there"})
    print("result:----->", result)


if __name__ == "__main__":
    test_graph_build()