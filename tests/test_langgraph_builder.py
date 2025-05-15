import os
import random
from typing import Annotated,Literal
from dotenv import load_dotenv

from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Command

load_dotenv()

def test_builder():
    class State(TypedDict):
        foo: str


    def node_a(state: State) -> Command[Literal["node_b", "node_c"]]:
        print("Called A")
        value = random.choice(["a", "b"])
        # this is a replacement for a conditional edge function
        if value == "a":
            goto = "node_b"
        else:
            goto = "node_c"

        # note how Command allows you to BOTH update the graph state AND route to the next node
        return Command(
            # this is the state update
            update={"foo": value},
            # this is a replacement for an edge
            goto=goto,
        )


    def node_b(state: State):
        print("Called B")
        return {"foo": state["foo"] + "b"}


    def node_c(state: State):
        print("Called C")
        return {"foo": state["foo"] + "c"}
    
    def node_d(state: State):
        print("Called D")
        return {"foo": state["foo"] + "d"}

    def node_e(state: State):
        print("Called E")
        return {"foo": state["foo"] + "e"}

    def node_f(state: State):
        print("Called F")
        return {"foo": state["foo"] + "f"}
    

    builder = StateGraph(State)
    builder.add_edge(START, "node_a")
    builder.add_node(node_a)
    builder.add_node(node_b)
    builder.add_node(node_c)
    builder.add_node(node_d)
    builder.add_node(node_e)
    builder.add_node(node_f)

    builder.add_edge("node_c", "node_e")
    builder.add_edge("node_b", "node_e")
    builder.add_edge("node_e", "node_f")
    builder.add_edge("node_f", END)

    builder.set_entry_point("node_c")
    builder.set_finish_point("node_e")

    graph = builder.compile()

    print("---------------------------")
    print(builder.nodes)
    print("---------------------------")
    print("---------------------------")
    print(graph.get_graph().nodes)
    print("---------------------------")
    print(graph.get_graph().edges)

    # print(graph.get_graph().draw_mermaid())
    print("---------------------------")
    print(graph.get_graph().draw_ascii()) 
    print("---------------------------")



def test_chatboot_builder():
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    llm = ChatOpenAI(model="qwen2.5-instruct",
                     api_key=os.getenv("LLM_API_KEY"),
                     base_url="http://10.86.20.4:12080/v1",
                     temperature=0.5)

    def llm_chatbot(state:State):
        return {"messages": [llm.invoke(state["messages"])]}

    graph_builder = StateGraph(State)
    graph_builder.add_node(node="chatbot",action=llm_chatbot)
    graph_builder.add_edge(start_key=START, end_key="chatbot")
    graph_builder.add_edge(start_key="chatbot", end_key=END)

    graph = graph_builder.compile()

    print(graph_builder.nodes)
    print(graph.get_graph().draw_mermaid())
    print(graph.get_graph().draw_ascii()) 

    result = graph.invoke({"messages": [{"role": "user", "content": "hello"}]})
    
    print(f"result-->{result}")


if __name__ == "__main__":
    test_builder()