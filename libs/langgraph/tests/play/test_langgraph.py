from typing import TypedDict,Annotated
import pytest
from langgraph.graph import StateGraph,START,END
from langgraph.errors import InvalidUpdateError
from IPython.display import display, Image
import operator

class SimpleState(TypedDict):
    hello_a: str
    hello_b: str

class State(TypedDict):
    hello_a: str
    hello_b: str
    hello_c: str
    hello_d: str
    hello_e: str
    hello_f: str
    

def node_a(state: State) -> State:
    print(f"----> node a is called: {state}")

    return {"hello_a": "world_a", "hello_a_1": "world_a_1"}


def node_b(state: State) -> State:

    print(f"----> node b is called: {state}")

    return {"hello_b": "world_b"}

def node_c(state: State) -> State:
    print(f"----> node c is called: {state}")

    return {"hello_c": "world_c",
            "hello_c_a": "world_c_a"}

def node_d(state: State) -> State:    
    print(f"----> node d is called: {state}")

    return {"hello_d": "world_d"}


def node_e(state: State) -> State:  
    print(f"----> node e is called: {state}")

    return {"hello_e": "world_e"}


def node_f(state: State) -> State:
    print(f"----> node f is called: {state}")

    return {"hello_f": "world_f"}

def node_d_route_fun(state: State)->bool:
    return True


def test_simple_graph_build():
    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.set_entry_point("a")
    builder.add_edge("a", "b")
    builder.set_finish_point("b")

    graph = builder.compile()

    # print(graph.get_graph().draw_ascii())

    result = graph.invoke(input={"hello_a": "there"})
    print("result:----->", result)


def test_graph_build() -> None:
    

    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)
    builder.add_node("d", node_d)
    builder.add_node("e", node_e)
    builder.add_node("f", node_f)

    builder.set_entry_point("a")
    builder.add_edge("a", "b")
    builder.add_edge("a", "c")
    builder.add_conditional_edges("a", node_d_route_fun, {True: "d", False: "f"} )
    builder.add_edge("a", "e")
    builder.add_edge("e", "b")
    builder.add_edge("b", "f")
    builder.add_edge("c", "f")
    builder.add_edge("d", "f")


    graph = builder.compile()
    graph.nodes["a"].node

    # display(Image(graph.get_graph().draw_mermaid_png()))
    # print(graph.get_graph().draw_ascii())
#                 +-----------+                  
#                 | __start__ |                  
#                 +-----------+                  
#                       *                        
#                       *                        
#                       *                        
#                     +---+                      
#                   **| a |.                     
#                *** *+---+*....                 
#           *****  **   .    ** ....             
#        ***     **     .      *    ...          
#     ***      **       .       **     ....      
# +---+       *         .         *        ..    
# | e |      *          .         *         .    
# +---+     *           .         *         .    
#      *    *           .         *         .    
#       *  *            .         *         .    
#        **             .         *         .    
#      +---+            .       +---+     +---+  
#      | b |**          .       | c |   **| d |  
#      +---+  **        .      *+---+***  +---+  
#               ***     .    ** *****            
#                  **   .  *****                 
#                    ** . ***                    
#                     +---+                      
#                     | f |                      
#                     +---+                      
#                       *                        
#                       *                        
#                       *                        
#                  +---------+                   
#                  | __end__ |                   
#                  +---------+                   
# ----> node a is called
# ----> node b is called
# ----> node c is called
# ----> node d is called
# ----> node e is called
# ----> node b is called
# ----> node f is called
# ----> node f is called

    result = graph.invoke(input={"hello_a": "there"})
    print("result:----->", result)


def test_parallel_graph_build():
    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)
    builder.add_node("d", node_d)

    builder.add_edge(START, "a")

    builder.add_edge("a", "b")
    builder.add_edge("a", "c")

    # builder.add_edge("a","d")
    # builder.add_edge("b","d")
    # builder.add_edge("c","d")

    builder.add_edge(["a", "b", "c"], "d")
    builder.set_finish_point("d")

    graph = builder.compile()
    print(graph.get_graph().draw_ascii())
    result = graph.invoke(input={"hello_a": "there"})
    print("result:----->", result)

if __name__ == "__main__":
    test_parallel_graph_build()