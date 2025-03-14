from langchain_core.messages import RemoveMessage
from utils.graph_state import State


class FilterMessages:
    def __call__(self, state: State):
        # Remove all messages except the last four
        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-4]]
        return {"messages": delete_messages}
