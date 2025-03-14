from prompts.arithmetic import sys_msg
from utils.graph_state import State
from utils.model_api import llm_with_tools


class ToolCallingLLM:
    def __init__(self):
        self.sys_msg = sys_msg

    def __call__(self, state: State):
        response = llm_with_tools.invoke([self.sys_msg] + state["messages"])
        return {"messages": [response]}
