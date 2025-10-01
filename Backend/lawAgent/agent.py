from lawAgent.Nodes.utils.utils import get_text
from lawAgent.Nodes.state import State, ConverstationOutput
from lawAgent.Nodes.gaurd import gaurdrail
from lawAgent.Nodes.redirector import redirection
from lawAgent.Nodes.summerizer import SummerizerNode
from lawAgent.Nodes.final import FinalNode
from lawAgent.Nodes.orchestrator import sub_graph

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from langsmith import traceable
from langgraph.config import get_stream_writer
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Literal

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
    streaming=False
)

# Prompt
conversation_prompt_path = 'lawAgent/Nodes/prompts/conversation.txt'
conversation_prompt = ChatPromptTemplate([
    SystemMessage(content=get_text(conversation_prompt_path)),
    MessagesPlaceholder("msg")
])

# Node
chatbot = llm.with_structured_output(ConverstationOutput)
@traceable
async def ChatNode(state:State):
    if not state.get("conversation"):
        state["conversation"] = []
        
    state["conversation"].append({"role": "user", "content": state["user_query"]})
    
    writer = get_stream_writer()
    try:
        res = await chatbot.ainvoke(
            conversation_prompt.invoke({"msg":state["conversation"]})
        )
        # print(res)

        state["conversation"].append({"role": "assistant", "content": res.content.conversation})

        state['user_query'], state['proceed2Orchestration'] = res.content.conversation, res.content.proceed2Orchestration
        
        
        writer({"type":"Status","content":40})
        return state
    
    except Exception as e:
        writer({"type":"Error","content": str(e)})



# Conditional Node 
def gaurdrail_to_others(state:State) -> Literal["Redirector","Normal","DeadEnd"]:
    if(state["gaurd_index"] == 0):
        return "Normal"
    elif(0 < state["gaurd_index"] < 3):
        return "Redirector"
    else:
        return "DeadEnd"

def orchestrationOrEnd(state:State):
    if(state['proceed2Orchestration'] == False):
        return "END"
    else:
        return "ORCHESTRATION"

# Optional
# def high_orch(state:State):
#     res = sub_graph.invoke()
#     return res

def pre_end(state:State):
    writer = get_stream_writer()
    writer({"type":"Status","content":100})
    return state

builder = StateGraph(State)
builder.add_node("gaudrail", gaurdrail)
builder.add_node("redirector", redirection)
builder.add_node("chat_node", ChatNode)
builder.add_node("summerizer", SummerizerNode)
builder.add_node("orchestrator_worker", sub_graph)
builder.add_node("pre_end", pre_end)
builder.add_node("final_answer",FinalNode)

builder.add_edge(START, "gaudrail")
builder.add_conditional_edges(
    "gaudrail", gaurdrail_to_others,
    {
        "Normal":"chat_node",
        "Redirector":"redirector",
        "DeadEnd":"pre_end"
    })

builder.add_conditional_edges(
    "chat_node", orchestrationOrEnd,
    {
        "ORCHESTRATION":"orchestrator_worker",
        "END":"pre_end"
    }
)


builder.add_edge("redirector", "pre_end")
builder.add_edge("orchestrator_worker", "final_answer")
builder.add_edge("orchestrator_worker", "summerizer")
builder.add_edge("final_answer", "pre_end")
builder.add_edge("summerizer", "pre_end")
builder.add_edge("pre_end", END)

memory = MemorySaver()
agent = builder.compile(checkpointer=memory)