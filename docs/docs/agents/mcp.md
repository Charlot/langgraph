---
search:
  boost: 2
tags:
  - agent
hide:
  - tags
---

# Use MCP

The Model Context Protocol (MCP) is an open protocol that standardizes how applications provide tools and context to language models. LangGraph agents can use tools defined on MCP servers through the `langchain-mcp-adapters` library.

## Use MCP tools

The `langchain-mcp-adapters` package enables agents to use tools defined across one or more MCP servers.

=== "In an agent"

    ```python title="Agent using tools defined on MCP servers"
    # highlight-next-line
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langgraph.prebuilt import create_react_agent

    # highlight-next-line
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Replace with absolute path to your math_server.py file
                "args": ["/path/to/math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                # Ensure you start your weather server on port 8000
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )
    # highlight-next-line
    tools = await client.get_tools()
    agent = create_react_agent(
        "anthropic:claude-3-7-sonnet-latest",
        # highlight-next-line
        tools
    )
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    )
    ```

=== "In a workflow"

    ```python
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langgraph.graph import StateGraph, MessagesState, START
    from langgraph.prebuilt import ToolNode, tools_condition

    from langchain.chat_models import init_chat_model
    model = init_chat_model("openai:gpt-4.1")

    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["./examples/math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/mcp/",
                "transport": "streamable_http",
            }
        }
    )
    tools = await client.get_tools()

    def call_model(state: MessagesState):
        response = model.bind_tools(tools).invoke(state["messages"])
        return {"messages": response}

    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    graph = builder.compile()
    math_response = await graph.ainvoke({"messages": "what's (3 + 5) x 12?"})
    weather_response = await graph.ainvoke({"messages": "what is the weather in nyc?"})
    ```



## Custom MCP servers

To create your own MCP servers, you can use the `mcp` library. This library provides a simple way to define tools and run them as servers.

Install the MCP library:

```bash
pip install mcp
```
Use the following reference implementations to test your agent with MCP tool servers.

```python title="Example Math Server (stdio transport)"
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

```python title="Example Weather Server (Streamable HTTP transport)"
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return "It's always sunny in New York"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

## Additional resources

- [MCP documentation](https://modelcontextprotocol.io/introduction)
- [MCP Transport documentation](https://modelcontextprotocol.io/docs/concepts/transports)
- [langchain_mcp_adapters](https://github.com/langchain-ai/langchain-mcp-adapters)