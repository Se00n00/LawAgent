from .utils.utils import get_text
from .state import SummerizerOutput, State, FinalOutput

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
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

# # Prompt
# finalanswer_prompt_path = 'lawAgent/Nodes/prompts/finalanswer.txt'
# answer_prompt = ChatPromptTemplate([
#     SystemMessage(content=get_text(finalanswer_prompt_path)),
#     MessagesPlaceholder("msg")
# ])

# Node
final_llm = llm.with_structured_output(FinalOutput)
async def FinalNode(state:State):
    text = state["complete_section"]
    writer = get_stream_writer()
    try:
        res = await final_llm.ainvoke(f"""
            You are a final answer assistant. 

            Your task is to provide a **final answer** to the user's question. keep it very short (50-70 words) but keep it detailed 
            Do NOT explain your reasoning or any ask questions.
                            
            Schema for answering: 
                class FinalOutput(BaseModel):
                    type:"FinalAnswer" -- keep this string intact
                    content:final_content -- your answer
                where final_answer is:
                    class final_content(BaseModel):
                        answer_title:str  -- What tile you give for your answer
                        final_answer:str  -- Your Answer
            Information: {text}
            User Question: {state['user_query']}
        """)
        writer(res.model_dump())
        return {}
        # return {"final_answer":res.content}
    except Exception as e:
        writer({"type":"Error","content": str(e)})

    # state["final_answer"] = res.content
    # return state