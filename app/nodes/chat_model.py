from utils.graph_state import State
from utils.model_api import llm


class ChatModel:
    def __call__(self, state: State):
        response = {"messages": [llm.invoke(state["messages"])]}
        return response
