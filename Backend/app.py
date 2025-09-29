from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from lawAgent.agent import agent

# --- Setup : Agent---
# llm = ChatOpenAI(
#     model="x-ai/grok-4-fast:free",
#     streaming=True,
#     api_key=os.environ["OPENROUTER_API_KEY"],
#     base_url="https://openrouter.ai/api/v1"
# )


# def model(state: MessagesState):
#     response = llm.invoke(state['messages'])
#     return {"messages": response}

# memory = MemorySaver()
# bot = (
#     StateGraph(state_schema=MessagesState)
#     .add_node("model", model)
#     .add_edge(START, "model")
#     .compile(checkpointer=memory)
# )

# --- Setup: FAST API ---
app = FastAPI()

origins = [
    "http://localhost:4200",   # Angular dev server
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # or ["*"] for open access
    allow_credentials=True,
    allow_methods=["*"],          # very important: allows OPTIONS
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

config = {"configurable": {"thread_id": "abc123"}}

@app.get("/")
def home():
    return {"Ok":"Yay XD"}

@app.post("/chat")
def chat(req: ChatRequest):
    input_message = req.message

    try:
        def event_generator():
            for stream_mode in agent.stream(
            {"user_query": input_message},config, subgraphs=True, stream_mode=["messages","custom"]):
                
                if stream_mode[1] == 'messages':
                    # print(stream_mode[2])
                    if isinstance(stream_mode[2][0], AIMessage):
                        yield stream_mode[2][0].content
                else:
                    yield str(stream_mode[2])
                # print(stream_mode)


        return StreamingResponse(event_generator(), media_type="text/plain")
    except Exception as e:
        return {"error":f"Exception: {e}"}