from lawAgent.Nodes.utils.utils import get_text
from lawAgent.Nodes.state import State, GaurdRailState

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.config import get_stream_writer


import os
from dotenv import load_dotenv

# LLM
load_dotenv()
primary_llm = os.getenv("PRIMARY_LLM")
secondary_llm = os.getenv("SECONDARY_LLM")
openrouter_api = os.getenv("OPENROUTER_APIKEY")

llm = ChatOpenAI(
    model = secondary_llm,
    api_key=openrouter_api,
    base_url = "https://openrouter.ai/api/v1",
    streaming=True
)


# Prompt
gaurd_prompt_path = 'lawAgent/Nodes/prompts/gaurd.txt'
prompt_template = ChatPromptTemplate([
    ("system", get_text(gaurd_prompt_path)),
    ("user", "{prompt}")
])

# Node
structured_llm = llm.with_structured_output(GaurdRailState)
def gaurdrail(state:State):
    gaurd_rail_prompt = prompt_template.invoke({"prompt": state['user_query']})
    msg = structured_llm.invoke(gaurd_rail_prompt)
    
    writer = get_stream_writer()
    writer({"type":"Status","content":20})
    return {"gaurd_index":msg.content}