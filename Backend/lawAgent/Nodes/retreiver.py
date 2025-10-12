from .state import WorkerState,refine_query, news_arguments
from .utils.utils import get_text
from .tools.news import get_news
from .tools.mcp_client import mcp

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.config import get_stream_writer


import os
import asyncio
import difflib
from dotenv import load_dotenv

# LLM
load_dotenv()
primary_llm = os.getenv("PRIMARY_LLM")
secondary_llm = os.getenv("SECONDARY_LLM")
worker_llm = os.getenv("WORKER_LLM")
openrouter_api = os.getenv("OPENROUTER_APIKEY")
base_url = os.getenv("BASE_URL")

llm = ChatOpenAI(
    model = worker_llm,
    api_key = openrouter_api,
    base_url = base_url,
    streaming=True
)

# Prompt
retriver_prompt_path = 'lawAgent/Nodes/prompts/retriver_synthesizer.txt'
retriver_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(retriver_prompt_path)),
    MessagesPlaceholder("msg")
])

async def curated_index(data, query):
    return await mcp.call("curate", {"data": data, "query": query})



# Node : Prompt Synthesizer(news_synthesizer) > get_news(tools) > Curator(news_curator) > Extractor(news_extractor)
Retreiver = llm.with_structured_output(news_arguments)
async def news_synthesizer(state: WorkerState):
    writer = get_stream_writer()
    try:
        res = await Retreiver.ainvoke(
            retriver_prompt.invoke({"msg":[HumanMessage(content =state["worker_query"])]})
        )

        result = get_news(
            query=res.worker_query,
            timelimit=res.timelimit,
            max_results=res.max_results,
            page=res.page,
            region=res.region
        )
        index = await curated_index(data=result, query=state["worker_query"])
        to_send = [result[int(i)] for i in index]
        writer({"type":"News","content":to_send})

        return {"curated_results": to_send}
    except Exception as e:
            writer({"type":"Error","content": str(e)})


async def news_extractor(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {str(p['title'])}\n Date: {str(p['date'])}\n Body: {str(p['body'])}\n Source: {str(p['source'])} " for p in state["curated_results"]]
    )

    writer = get_stream_writer()
    try:
        msg = await llm.ainvoke([
            HumanMessage(content=f"Extract the most important findings and insights from these articles:\n\n{papers_text}")
        ])
        return {"extracted_content":["News Articles: ", msg.content]}
    except Exception as e:
        writer({"type":"Error","content": str(e)})


news_articles = (
    StateGraph(WorkerState)
    .add_node("news_synthesizer",news_synthesizer)
    .add_node("news_extractor",news_extractor)
    .add_edge(START, "news_synthesizer")
    .add_edge("news_synthesizer", "news_extractor")
    .add_edge("news_extractor",END)
    .compile()
)