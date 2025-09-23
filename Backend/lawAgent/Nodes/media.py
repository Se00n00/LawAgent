from state import WorkerState

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

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

# Node : Curator
def images_curator(state: WorkerState) -> WorkerState:
    papers_text = "\n\n".join(
        [f"Title: {p['title']}\n" for p in state["search_results"]]
    )
    msg = llm([
        HumanMessage(content=f"From these titles of images that contains articles, select the most relevant ones for the query '{state['worker'].description}'. "
        f"Return only the chosen titles.\n\n{papers_text}")
    ])

    chosen_titles = msg.content.splitlines()
    curated = [p for p in state["search_results"] if p["title"] in chosen_titles]
    
    return {"curated_results":curated}