from .utils.utils import get_text
from .state import SummerizerOutput, State

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

# Prompt
sumerizer_prompt_path = 'lawAgent/Nodes/prompts/summerizer.txt'
summerizer_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(sumerizer_prompt_path)),
    MessagesPlaceholder("msg")
])

# Node
summerizer = llm.with_structured_output(SummerizerOutput)
async def SummerizerNode(state:State):
    text = state["complete_section"]

    writer = get_stream_writer()
    try:
        res = await summerizer.ainvoke(f"""
            You are a pointwise summerizer assistant. 

            Your task is to provide a point wise summerization to the user's question. 
            which is you would generate important point as list of [heading + heading_content] 
            Do NOT explain your reasoning or any ask questions.
            Schema for answering: 
                class SummerizerOutput(BaseModel):
                    type:"Summeries" -- keep this string intact
                    content: summeries_content

                where summeries_content is:
                    class summeries_content(BaseModel):
                        summeries:List[Dict[str, Any]] -- summeries in list of dict with keys : heading: , heading_content: 20-30 words of summaries under that headings
                        summary_title:str   -- What should be a main title for your summeries

            Information: {text}
        """)
        
        writer({"type":"summerizer","content":res.content})
        return {}
        # return {"Summeries": res.content.summeries}
    
    except Exception as e:
        writer({"type":"Error","content": str(e)})
