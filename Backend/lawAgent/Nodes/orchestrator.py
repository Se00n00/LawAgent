from .utils.utils import get_text
from .state import Orchestrator_Output, State
from .gov import gov_articles
from .media import images
from .researcher import research_articles
from .retreiver import news_articles

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

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
orchestrator_prompt_path = 'lawAgent/Nodes/prompts/orchestrator.txt'
orchestraor_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(orchestrator_prompt_path)),
    MessagesPlaceholder("msg")
])

# Node
orchestrator = llm.with_structured_output(Orchestrator_Output)
def OrchestratorNode(state:State):
    res = orchestrator.invoke(
        orchestraor_prompt.invoke({"msg":[HumanMessage(content = state["user_query"])]})
    )
    print(res.works)
    return {"works": res.works}

def assign_task(state:State):
    workers = {
        "Retreive":"news_articles",
        "Media":"images",
        "Researcher":"research_articles",
        "Gov":"gov_articles"
    }

    return [
        Send(workers.get(w.name,"news_articles"), {"worker_query":w.description}) 
        for w in state['works']
    ]

def synthesizer(state: State):
    completed_sections = state["extracted_content"]
    final_report = "\n\n---\n\n".join(completed_sections)
    return {"complete_section":final_report}

builder = StateGraph(State)
builder.add_node("orch",OrchestratorNode)
builder.add_node("synthesizer", synthesizer)
builder.add_node("news_articles",news_articles)
builder.add_node("research_articles",research_articles)
builder.add_node("images",images)
builder.add_node("gov_articles",gov_articles)

builder.add_edge(START, "orch")
builder.add_conditional_edges(
    "orch",assign_task,["research_articles", "news_articles", "images", "gov_articles"]
)

builder.add_edge("gov_articles","synthesizer")
builder.add_edge("images","synthesizer")
builder.add_edge("news_articles","synthesizer")
builder.add_edge("research_articles","synthesizer")
builder.add_edge("synthesizer",END)
sub_graph = builder.compile()