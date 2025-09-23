from .utils.utils import get_text
from .state import SummerizerOutput, State

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage

import os
from dotenv import load_dotenv

# LLM
load_dotenv()
primary_llm = os.getenv("PRIMARY_LLM")
secondary_llm = os.getenv("SECONDARY_LLM")
openrouter_api = os.getenv("OPENROUTER_APIKEY")

llm = ChatOpenAI(
    model = primary_llm,
    api_key=openrouter_api,
    base_url = "https://openrouter.ai/api/v1",
    streaming=True
)

# Prompt
finalanswer_prompt_path = 'lawAgent/Nodes/prompts/finalanswer.txt'
answer_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(finalanswer_prompt_path)),
    MessagesPlaceholder("msg")
])

# Node
def FinalNode(state:State):
    text = state["complete_section"]
    res = llm.invoke(
        answer_prompt.invoke({"msg":[HumanMessage(content=text)]})
    )
    state["final_answer"] = res.content
    return state