from utils.utils import get_text
from state import RedirectionState, State, GaurdRailState

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

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
redirect_prompt_path = 'prompts/redirection.txt'
prompt_template = ChatPromptTemplate([
    ("system", get_text(redirect_prompt_path)),
    ("user", "{prompt}")
])

# Node
structured_llm = llm.with_structured_output(RedirectionState)
def redirection(conv_state:State, index_state:GaurdRailState):
    redirect_prompt = prompt_template.invoke({"prompt": conv_state['user_query']+"Index of user's loss: "+str(index_state["gaurdrail_index"])})
    msg = structured_llm.invoke(redirect_prompt)
    return {"redirection":msg.content}