from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
import os

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# --- Setup ---
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "")

llm = ChatOpenAI(
    model="openrouter/sonoma-sky-alpha",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    streaming=True
)

def model(state: MessagesState):
    response = llm.invoke(state['messages'])
    return {"messages": response}

memory = MemorySaver()
bot = (
    StateGraph(state_schema=MessagesState)
    .add_node("model", model)
    .add_edge(START, "model")
    .compile(checkpointer=memory)
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

config = {"configurable": {"thread_id": "abc123"}}

@app.post("/chat")
async def chat(req: ChatRequest):
    input_message = [HumanMessage(content=req.message)]

    
    def event_generator():
        for chunk, metadata in bot.stream(
        {"messages": input_message},config, stream_mode="messages",):
            if isinstance(chunk, AIMessage):
                yield chunk.content


    return StreamingResponse(event_generator(), media_type="text/plain")
