from langchain_core.messages import HumanMessage, RemoveMessage
from utils.model_api import llm
from utils.summary_state import SummaryState


class Summarize:
    def __call__(self, state: SummaryState):
        summary = state.get("summary", "")

        if summary:
            summary_message = (
                f"Esse é um resumo da conversa até agora: {summary}\n\n"
                "Extenda o resumo levando em consideração as novas mensagens acima:"
            )
        else:
            summary_message = "Crie um resumo da conversa acima:"

        messages = state["messages"] + [HumanMessage(content=summary_message)]
        response = llm.invoke(messages)

        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-4]]
        return {"summary": response.content, "messages": delete_messages}
