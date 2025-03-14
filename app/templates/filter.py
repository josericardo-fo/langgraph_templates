from IPython.display import Image
from langchain_core.messages.human import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from nodes.chat_model import ChatModel
from nodes.reducer import FilterMessages
from utils.graph_state import State
from utils.memory import config


def create_graph():
    builder = StateGraph(State)

    builder.add_node("filter", FilterMessages())
    builder.add_node("chat_model", ChatModel())

    builder.add_edge(START, "filter")
    builder.add_edge("filter", "chat_model")
    builder.add_edge("chat_model", END)

    memory = MemorySaver()

    graph = builder.compile(checkpointer=memory)

    try:
        Image(
            graph.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
                output_file_path="graphs/filter.png",
            )
        )
    except Exception as e:
        print(e)

    return graph


global_graph = create_graph()


def get_response(message):
    output = global_graph.invoke({"messages": HumanMessage(content=message)}, config)
    ai_message = output["messages"][-1:]
    response = ai_message[0].content
    return response
