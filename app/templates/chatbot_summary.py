from IPython.display import Image
from langchain_core.messages.human import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from nodes.should_continue import ShouldContinue
from nodes.summarize import Summarize
from nodes.summary_model import SummaryModel
from utils.memory import config
from utils.summary_state import SummaryState


def create_graph():
    builder = StateGraph(SummaryState)

    builder.add_node("conversation", SummaryModel())
    builder.add_node("summarize_conversation", Summarize())

    builder.add_edge(START, "conversation")
    builder.add_conditional_edges("conversation", ShouldContinue())
    builder.add_edge("summarize_conversation", END)

    memory = MemorySaver()

    graph = builder.compile(checkpointer=memory)

    try:
        Image(
            graph.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
                output_file_path="graphs/chatbot_summary.png",
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
