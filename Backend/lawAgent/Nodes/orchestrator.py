from utils.utils import get_text
from state import Orchestrator_Output, State, OrchestratorState

# worker: reseracher, retreiver, media
from researcher import research_curator, research_extractor
from retreiver import news_curator, news_extractor
from media import images_curator
from gov import gov_curator, gov_extractor

# Worker tool Node
from tools.gov import get_articles
from tools.images import get_images
from tools.news import get_news
from tools.sementicScholar import get_papers

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

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
orchestrator_prompt_path = 'prompts/orchestrator.text'
orchestraor_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(orchestrator_prompt_path)),
    MessagesPlaceholder("msg")
])

# Node
orchestrator = llm.with_structured_output(Orchestrator_Output)
def OrchestratorNode(state:State):
    res = orchestrator.invoke(
        orchestraor_prompt.invoke({"msg":[HumanMessage(content=state["user_query"])]})
    )
    return {"Works": res.works}

def synthesizer(state:State):
    text = f"Researched Content: {state['research_content']}\n\n NewsArticles: {state['retreival_content']}\n\n Official Government Articles: {state['gov_content']}"
    return {"complete_section":text}

builder = StateGraph(OrchestratorState)
builder.add_node("orch",OrchestratorNode)
builder.add_node("synthesizer", synthesizer)

builder.add_node("get_papers",get_papers)
builder.add_node("get_news",get_news)
builder.add_node("get_images",get_images)
builder.add_node("get_articles",get_articles)
builder.add_node("reserach_curator", research_curator)
builder.add_node("research_extractor", research_extractor)
builder.add_node("news_curator", news_curator)
builder.add_node("news_extractor", news_extractor)
builder.add_node("image_curator",images_curator)
builder.add_node("gov_curator",gov_curator)
builder.add_node("gov_extractor",gov_extractor)

builder.add_edge(START, "orch")

builder.add_edge("get_papers","reserach_curator")
builder.add_edge("reserach_curator","research_extractor")
builder.add_edge("get_news","news_curator")
builder.add_edge("news_curator","news_extractor")
builder.add_edge("get_images","image_curator")
builder.add_edge("get_articles","gov_curator")
builder.add_edge("gov_curator","gov_extractor")
sub_graph = builder.compile()