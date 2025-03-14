from config import MODEL
from langchain_openai import ChatOpenAI
from utils.tools import tools

llm = ChatOpenAI(model=MODEL)
llm_with_tools = llm.bind_tools(tools)
