from langgraph.graph import END
from utils.summary_state import SummaryState


class ShouldContinue:
    def __call__(self, state: SummaryState):
        messages = state["messages"]

        if len(messages) == 6:
            return "summarize_conversation"

        return END
