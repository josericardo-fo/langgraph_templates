from langchain_core.messages import SystemMessage
from utils.model_api import llm
from utils.summary_state import SummaryState


class SummaryModel:
    def __call__(self, state: SummaryState):
        summary = state.get("summary", "")

        if summary:
            system_message = f"Resumo da conversa anterior: {summary}"
            messages = [SystemMessage(system_message) + state["messages"]]
        else:
            messages = state["messages"]

        response = llm.invoke(messages)
        return {"messages": response}
