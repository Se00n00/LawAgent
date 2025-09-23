from .state import WorkerState,refine_query
from .utils.utils import get_text
from .tools.news import get_news

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
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
retriver_prompt_path = 'lawAgent/Nodes/prompts/retriver_synthesizer.txt'
retriver_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(retriver_prompt_path)),
    MessagesPlaceholder("msg")
])


# Node : Prompt Synthesizer(news_synthesizer) > get_news(tools) > Curator(news_curator) > Extractor(news_extractor)
Retreiver = llm.with_structured_output(refine_query)
def news_synthesizer(state: WorkerState):
    res = Retreiver.invoke(
        retriver_prompt.invoke({"msg":[HumanMessage(content =state["worker_query"])]})
    )
    return {"worker_query": res.query}


def news_curator(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {p['title']}\n" for p in state["search_results"]]
    )
    msg = llm.invoke([
        HumanMessage(content=f"From these articles, select the most relevant ones for the query '{state['worker_query']}'. "
        f"Return only the chosen titles.\n\n{papers_text}")
    ])

    chosen_titles = msg.content.splitlines()
    curated = [p for p in state["search_results"] if p["title"] in chosen_titles]
    
    return {"curated_results":curated}



def news_extractor(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {p['title']} ({p['date']})" for p in state["curated_results"]]
    )
    msg = llm.invoke([
        HumanMessage(content=f"Extract the most important findings and insights from these articles:\n\n{papers_text}")
    ])
    return {"extracted_content":["News Articles: ", msg.content]}

news_articles = (
    StateGraph(WorkerState)
    .add_node("news_synthesizer",news_synthesizer)
    .add_node("get_news",get_news)
    .add_node("news_curator",news_curator)
    .add_node("news_extractor",news_extractor)
    .add_edge(START, "news_synthesizer")
    .add_edge("news_synthesizer", "get_news")
    .add_edge("get_news", "news_curator")
    .add_edge("news_curator","news_extractor")
    .add_edge("news_extractor",END)
    .compile()
)