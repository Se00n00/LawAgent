import marimo

__generated_with = "0.14.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import os
    os.environ["OPENAI_API_KEY"] = ""

    # ✅ Get the environment variable
    value = os.getenv("OPENAI_API_KEY")
    return


@app.cell
def _():
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model = "openrouter/sonoma-sky-alpha",
        base_url = "https://openrouter.ai/api/v1",
            streaming=True
    
    )
    return (llm,)


@app.cell
def _(llm):
    from langgraph.graph import MessagesState

    def model(state: MessagesState):
        response = llm.invoke(state['messages'])
        return {"messages": response}
    return MessagesState, model


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""MessagesState: {"messages":AIMessage}  ?""")
    return


@app.cell
def _(MessagesState, model):
    from langgraph.graph import StateGraph, START
    from langgraph.checkpoint.memory import MemorySaver

    memory = MemorySaver()
    bot = (StateGraph(state_schema = MessagesState)
        .add_node("model",model)
        .add_edge(START, "model")
        .compile(checkpointer=memory))
    return (bot,)


@app.cell
def _(bot):
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    config = {"configurable": {"thread_id": "abc123"}} # Why Do we need this config ??

    exit = False
    language = "English"

    while(not exit):
        ask = str(input("Ask Anything"))
        if(ask.split(" ")[-1] == "Q"):
            exit = True

        input_message = [HumanMessage(content=ask)]
        # ai = bot.invoke({"messages":input_message},config) # Why Did we invoke in this particular template ?

        for chunk, metadata in bot.stream(
            {"messages": input_message, "language": language},config, stream_mode="messages",):
            if isinstance(chunk, AIMessage):  # Filter to just model responses
                print(chunk.content, end="")

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
