from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class SummaryState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    summary: str
