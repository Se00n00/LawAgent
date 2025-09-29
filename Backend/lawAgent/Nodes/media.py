from .state import WorkerState, image_arguments
from .utils.utils import get_text
from .tools.images import get_images
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
image_prompt_path = 'lawAgent/Nodes/prompts/image_synthesizer.txt'
image_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(image_prompt_path)),
    MessagesPlaceholder("msg")
])


# Node : Prompt Synthesizer(image_synthesizer) > get_articles(tools) > Curator(images_curator)
Synthesizer = llm.with_structured_output(image_arguments)
def image_synthesizer(state: WorkerState):
    res = Synthesizer.invoke(
        image_prompt.invoke({"msg":[HumanMessage(content =state["worker_query"])]})
    )
    result = get_images(
        query=res.worker_query,
        timelimit=res.timelimit,
        region=res.region
    )
    index = asyncio.run(curated_index(data=result["search_results"], query=state["worker_query"]))
    
    to_send = [result["search_results"][int(i)] for i in index]
    writer = get_stream_writer()
    writer({"type":"Media","content":to_send})

    return {"curated_results": to_send}

def images_curator(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {p['title']}\n" for p in state["search_results"]]
    )
    msg = llm.invoke([
        HumanMessage(content=f"From these titles of images that contains articles, select the most relevant ones for the query '{state['worker_query']}'. "
        f"Return only the chosen titles.\n\n{papers_text}")
    ])

    chosen_titles = msg.content.splitlines()
    curated = [p for p in state["search_results"] if p["title"] in chosen_titles]
    
    return {"curated_results":curated}

images = (
    StateGraph(WorkerState)
    .add_node("image_synthesizer",image_synthesizer)
    .add_edge(START, "image_synthesizer")
    .add_edge("image_synthesizer", END)
    .compile()
)