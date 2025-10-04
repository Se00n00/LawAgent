from .state import WorkerState, image_arguments
from .utils.utils import get_text
from .tools.images import get_images
from .tools.mcp_client import mcp

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
worker_llm = os.getenv("WORKER_LLM")
openrouter_api = os.getenv("OPENROUTER_APIKEY")

llm = ChatOpenAI(
    model = worker_llm,
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

async def curated_index(data, query):
    return await mcp.call("curate", {"data": data, "query": query})



# Node : Prompt Synthesizer(image_synthesizer) > get_articles(tools) > Curator(images_curator)
Synthesizer = llm.with_structured_output(image_arguments)
async def image_synthesizer(state: WorkerState):
    writer = get_stream_writer()
    try:
        res = await Synthesizer.ainvoke(
            image_prompt.invoke({"msg":[HumanMessage(content =state["worker_query"])]})
        )
        result = get_images(
            query=res.worker_query,
            timelimit=res.timelimit,
            region=res.region
        )
        index = await curated_index(data=result, query=state["worker_query"])
        to_send = [result[int(i)] for i in index]
        writer({"type":"Media","content":to_send})

        return {"curated_results": to_send}
    
    except Exception as e:
        writer({"type":"Error","content": str(e)})

# def images_curator(state: WorkerState) -> WorkerState:
#     papers_text = "\n\n".join(
#         [f"Title: {p['title']}\n" for p in state["search_results"]]
#     )

#     writer = get_stream_writer()
#     try:
#         msg = llm.invoke([
#             HumanMessage(content=f"From these titles of images that contains articles, select the most relevant ones for the query '{state['worker_query']}'. "
#             f"Return only the chosen titles.\n\n{papers_text}")
#         ])

#         chosen_titles = msg.content.splitlines()
#         curated = [p for p in state["search_results"] if p["title"] in chosen_titles]
        
#         return {"curated_results":curated}
    
#     except Exception as e:
#         writer({"type":"Error","content": str(e)})

images = (
    StateGraph(WorkerState)
    .add_node("image_synthesizer",image_synthesizer)
    .add_edge(START, "image_synthesizer")
    .add_edge("image_synthesizer", END)
    .compile()
)