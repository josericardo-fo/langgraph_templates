from IPython.display import Image
from langchain_core.messages.human import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from nodes.tool_calling import ToolCallingLLM
from utils.graph_state import State
from utils.tools import tools


def create_graph():
    builder = StateGraph(State)

    builder.add_node("tool_calling_llm", ToolCallingLLM())
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges(
        "tool_calling_llm",
        # If the latest message (result) from tool_calling_llm is a tool call -> tools_condition routes to tools
        # If the latest message (result) from tool_calling_llm is a not a tool call -> tools_condition routes to END
        tools_condition,
    )
    builder.add_edge("tools", "tool_calling_llm")

    graph = builder.compile()

    try:
        Image(
            graph.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
                output_file_path="graphs/agent.png",
            )
        )
    except Exception as e:
        print(e)

    return graph


global_graph = create_graph()


def get_response(message):
    output = global_graph.invoke({"messages": HumanMessage(content=message)})
    ai_message = output["messages"][-1:]
    response = ai_message[0].content
    return response
