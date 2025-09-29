from .state import WorkerState, research_arguments
from .utils.utils import get_text
from .tools.sementicScholar import get_papers
from .tools.mcp_client import curated_index

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.config import get_stream_writer

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
research_prompt_path = 'lawAgent/Nodes/prompts/research_synthesizer.txt'
research_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(research_prompt_path)),
    MessagesPlaceholder("msg")
])


# Node : Prompt Synthesizer(reserach_synthesizer) > get_papers(tools) > Curator(research_curator) > Extractor(research_extractor)
Synthesizer = llm.with_structured_output(research_arguments)
def research_synthesizer(state: WorkerState):
    res = Synthesizer.invoke(
        research_prompt.invoke({"msg":[HumanMessage(content =state["worker_query"])]})
    )
    result = get_papers(query=res.worker_query)

    index = asyncio.run(curated_index(data=result["search_results"], query=state["worker_query"]))
    
    to_send = [result["search_results"][int(i)] for i in index]
    writer = get_stream_writer()
    writer({"type":"Research","content":to_send})

    return {"curated_results": to_send}

def research_curator(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {p['title']}\nAbstract: {p.get('abstract','')}" for p in state["search_results"]]
    )
    msg = llm.invoke([
        HumanMessage(content=f"From these papers, select the most relevant ones for the query '{state['worker_query']}'. "
        f"Return only the chosen titles.\n\n{papers_text}")
    ])

    chosen_titles = msg.content.splitlines()
    curated = [p for p in state["search_results"] if p["title"] in chosen_titles]
    
    return {"curated_results":curated}



def research_extractor(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {p['title']} ({p['year']})\nAbstract: {p.get('abstract','')}" for p in state["curated_results"]]
    )
    msg = llm.invoke([
        HumanMessage(content=f"Extract the most important findings and insights from these papers:\n\n{papers_text}")
    ])
    return {"extracted_content":["Researched Content: ", msg.content]}

research_articles = (
    StateGraph(WorkerState)
    .add_node("research_synthesizer",research_synthesizer)
    .add_node("research_extractor",research_extractor)
    .add_edge(START, "research_synthesizer")
    .add_edge("research_synthesizer", "research_extractor")
    .add_edge("research_extractor",END)
    .compile()
)