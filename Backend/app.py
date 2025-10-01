from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
import os
import json

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
        async def event_generator():
            async for stream_mode in agent.astream(
                {"user_query": input_message}, config, subgraphs=True, stream_mode=["messages","custom"]
            ):
                mode_type, payload = stream_mode[1], stream_mode[2]

                if mode_type == "custom":
                #     if isinstance(payload[0], AIMessage):
                #         node = payload[1].get("langgraph_node")
                #         # if node in ["gaudrail","redirector","chat_node","summerizer","final_answer"]:
                #             # content = payload[0].content
                #             # if content:  # Only yield if there's content
                #             #     yield content
                # else:
                    try:
                    # Convert to JSON string and add newline
                        if hasattr(payload, "__dict__"):
                            serializable_payload = payload.__dict__
                        else:
                            serializable_payload = payload
                        yield json.dumps(serializable_payload, default=str) + "\n"
                    except Exception as e:
                        yield json.dumps({"type": "Error", "content": str(e)}) + "\n"
        


        return StreamingResponse(event_generator(), media_type="application/x-ndjson")
    except Exception as e:
        return {"error":f"Exception: {e}"}