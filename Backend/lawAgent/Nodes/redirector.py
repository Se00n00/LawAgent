from lawAgent.Nodes.utils.utils import get_text
from lawAgent.Nodes.state import State, RedirectionState, GaurdRailState

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
    model = primary_llm,
    api_key=openrouter_api,
    base_url = "https://openrouter.ai/api/v1",
    streaming=False
)

# Prompt
redirect_prompt_path = 'lawAgent/Nodes/prompts/redirection.txt'
prompt_template = ChatPromptTemplate([
    ("system", get_text(redirect_prompt_path)),
    ("user", "{prompt}")
])

# Node
structured_llm = llm.with_structured_output(RedirectionState)
async def redirection(state:State):
    writer = get_stream_writer()
    try:
        redirect_prompt = prompt_template.invoke({"prompt": f"{state['user_query']} Gaurd_Index of user's loss: {str(state['gaurd_index'])}"})
        msg = await structured_llm.ainvoke(redirect_prompt)
        writer({"type":"redirector","content":msg.content})
        # return {"redirection":msg.content.redirection_str}

        return {}
    except Exception as e:
        writer({"type":"Error","content": str(e)})
