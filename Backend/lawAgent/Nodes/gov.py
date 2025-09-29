from .state import WorkerState, gov_arguments
from .tools.gov import get_articles
from .utils.utils import get_text
from .tools.mcp_client import curated_index

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage

import os
import asyncio
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
synthesizer_prompt_path = 'lawAgent/Nodes/prompts/gov_synthesizer.txt'
synthesizer_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(synthesizer_prompt_path)),
    MessagesPlaceholder("msg")
])


# Node : Prompt Synthesizer(gov_synthesizer) > get_images(tools) > Curator(gov_curator) > Extractor(gov_extractor)
Synthesizer = llm.with_structured_output(gov_arguments)
def gov_synthesizer(state: WorkerState):
    res = Synthesizer.invoke(
        synthesizer_prompt.invoke({"msg":[HumanMessage(content =state["worker_query"])]})
    )
    result = get_articles(
        query=res.worker_query,
        region=res.region,
        max_results=res.max_results
    )
    index = asyncio.run(curated_index(data=result["search_results"], query=state["worker_query"]))
    return {"curated_results": [result["search_results"][int(i)] for i in index]}

def gov_curator(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {p['title']}\n Body: {p['snippet']}" for p in state["search_results"]]
    )
    msg = llm.invoke([
        HumanMessage(content=f"From these articles, select the most relevant ones for the query '{state['worker_query']}'. "
        f"Return only the chosen titles.\n\n{papers_text}")
    ])

    chosen_titles = msg.content.splitlines()
    curated = [p for p in state["search_results"] if p["title"] in chosen_titles]
    
    return {"curated_results":curated}


def gov_extractor(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {p['title']} Body: {p['snippet']}" for p in state["curated_results"]]
    )
    msg = llm.invoke([
        HumanMessage(content=f"Extract the most important findings and insights from these articles:\n\n{papers_text}")
    ])

    return {"extracted_content":["Official Governement Articles: ", msg.content]}


gov_articles = (
    StateGraph(WorkerState)
    .add_node("gov_synthesizer",gov_synthesizer)
    .add_node("gov_extractor",gov_extractor)
    .add_edge(START, "gov_synthesizer")
    .add_edge("gov_synthesizer", "gov_extractor")
    .add_edge("gov_extractor",END)
    .compile()
)