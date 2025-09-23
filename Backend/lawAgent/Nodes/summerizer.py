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
sumerizer_prompt_path = 'lawAgent/Nodes/prompts/summerizer.txt'
summerizer_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(sumerizer_prompt_path)),
    MessagesPlaceholder("msg")
])

# Node
summerizer = llm.with_structured_output(SummerizerOutput)
def SummerizerNode(state:State):
    text = state["complete_section"]
    res = summerizer.invoke(
        summerizer_prompt.invoke({"msg":[HumanMessage(content=text)]})
    )
    return {"Summeries": res.Summeries}