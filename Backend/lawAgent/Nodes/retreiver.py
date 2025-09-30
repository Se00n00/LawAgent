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
openrouter_api = os.getenv("OPENROUTER_APIKEY")

llm = ChatOpenAI(
    model = primary_llm,
    api_key=openrouter_api,
    base_url = "https://openrouter.ai/api/v1",
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
        res = Retreiver.invoke(
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



def news_curator(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {str(p['title'])}\n Date: {str(p['date'])} Body: {str(p['body'])}" for p in state["search_results"]]
    )
    msg = llm.invoke([
        HumanMessage(content=f"From these articles, select the most relevant ones for the query '{state['worker_query']}'. "
        f"Return only the chosen titles.\n\n{papers_text}")
    ])

    chosen_titles = [line.strip() for line in msg.content.splitlines() if line.strip()]

    # fuzzy match: include article if its title is similar enough to any chosen title
    curated = []
    for article in state["search_results"]:
        for title in chosen_titles:
            ratio = difflib.SequenceMatcher(None, article["title"], title).ratio()
            if ratio > 0.7:  # threshold, adjust as needed
                curated.append(article)
                break

    return {"curated_results": curated}



def news_extractor(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {str(p['title'])}\n Date: {str(p['date'])}\n Body: {str(p['body'])}\n Source: {str(p['source'])} " for p in state["curated_results"]]
    )

    writer = get_stream_writer()
    try:
        msg = llm.invoke([
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