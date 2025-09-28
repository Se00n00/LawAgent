import marimo

__generated_with = "0.14.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    from langchain_openai.chat_models import ChatOpenAI
    return (ChatOpenAI,)


@app.cell
def _():


    return


@app.cell
def _(ChatOpenAI, openrouter_api, primary_llm):

    llm = ChatOpenAI(
        model = primary_llm,
        api_key=openrouter_api,
        base_url = "https://openrouter.ai/api/v1",
        streaming=True
    )
    return (llm,)


@app.cell
def _(llm):
    try:
        llm.invoke("Hii").content
    except Exception as e:
        print({"type":"Error"})
    return


@app.cell
def _():
    from langchain_core.messages import AIMessage
    from langgraph.graph import StateGraph, MessagesState, START
    return START, StateGraph


@app.cell
def _(State, llm):
    def chat(state: State):
        try:
            res = llm.invoke(state["messages"])
            return {"messages": res.content}
        except Exception as e:
            # return JSON-like error as node output
            return {"type": "Error"}
    return (chat,)


@app.cell
def _():
    from pydantic import BaseModel
    from typing import List
    class State(BaseModel):
        type:str
        messages: str
    return (State,)


@app.cell
def _(START, State, StateGraph, chat):
    graph = (StateGraph(State)
            .add_node("chat", chat)
            .add_edge(START,"chat")
            .compile())
    return (graph,)


@app.cell
def _(graph):
    graph.invoke({"messages":"Hii"})
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
