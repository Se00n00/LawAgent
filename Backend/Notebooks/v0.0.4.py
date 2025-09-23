import marimo

__generated_with = "0.14.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Setting Up LLM""")
    return


@app.cell
def _():
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model = "x-ai/grok-4-fast:free",
        api_key="",
        base_url = "https://openrouter.ai/api/v1",
        streaming=True
    )
    return (llm,)


@app.cell
def _(llm):
    llm.invoke("Hii")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Global""")
    return


@app.cell
def _(List, Worker_Output):
    from typing import TypedDict

    class State(TypedDict):
        user:str
        initialized:bool
        works: List[Worker_Output]
    return (State,)


@app.cell
def _():
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage, SystemMessage
    return ChatPromptTemplate, HumanMessage, MessagesPlaceholder, SystemMessage


@app.cell
def _(ChatPromptTemplate, MessagesPlaceholder, SystemMessage):
    orchestraor_prompt = ChatPromptTemplate([
        SystemMessage(content="""
        You are an Orchestrator Assstant that breaks down the task to suitable and relevent agents. these workder agents includes:
        Retreive: Retreive legal articles, judgements, reports, cases and news, 
        Media: Gets images/links (court rulings, law portals, legal infographics),
        Statistic :Searches for legal statistics relevent to the query,
        Researcher: Research about given topic, mainly the relevent research articles,
        Now as per the Question assign works while mentioning the name of these worker and the work you provided them
        """),
        MessagesPlaceholder("msg")
    ])
    return (orchestraor_prompt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Orchestrator""")
    return


@app.cell
def _():
    from pydantic import BaseModel, Field
    from typing import List

    class Worker_Output(BaseModel):
        name:str = Field(..., description="Name of Selected Worker")
        description:str = Field(..., description="Description of the work assigned by the Orchestrator")

    # How the output state schema would looks like if Agent is multi-step (Cycle in StateGraph)
    class Orchestrator_Ouput(BaseModel):
        works: List[Worker_Output]
    return List, Orchestrator_Ouput, Worker_Output


@app.cell
def _(HumanMessage, Orchestrator_Ouput, State, llm, orchestraor_prompt):
    orchestrator = llm.with_structured_output(Orchestrator_Ouput)

    def OrchestratorNode(state:State):
        res = orchestrator.invoke(
            orchestraor_prompt.invoke({"msg":[HumanMessage(content=state["user"])]})
        )
        return {"Works": res.works}
    return (OrchestratorNode,)


@app.cell
def _(OrchestratorNode):
    answer = OrchestratorNode({"user":"I want to know if current law of ethanol blending does exist in the modern law framework of india, also what does the internet speaking about it"})
    return (answer,)


@app.cell
def _(answer):
    answer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Workers""")
    return


@app.cell
def _():
    import requests

    # Pronlem: Gets only syntactically similiar articles
    def researcher_node(state):
        query = state
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=2"
        resp = requests.get(url).text
        print(resp)
        # naive parsing
        summaries = []
        for entry in resp.split("<entry>")[1:]:
            title = entry.split("<title>")[1].split("</title>")[0].strip()
            summary = entry.split("<summary>")[1].split("</summary>")[0].strip()
            summaries.append({"title": title, "summary": summary[:300]})
        return {"research_results": summaries or ["No research found"]}
    return (requests,)


@app.cell
def _(requests):
    def retriever_node(state):
        query = state["query"]
        url = f"https://api.openlegaldata.io/v1/cases/?search={query}"
        resp = requests.get(url).json()
        cases = [c.get("title") for c in resp.get("results", [])[:3]]
        return {"retriever_results": cases or ["No cases found"]}

    return (retriever_node,)


@app.cell
def _(retriever_node):
    retriever_node({"query":"Bank robbery"})
    return


@app.cell
def _(requests):
    def media_node(state):
        query = state["query"]
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id=YOUR_FREE_KEY"
        resp = requests.get(url).json()
        images = [r["urls"]["small"] for r in resp.get("results", [])[:3]]
        return {"media_results": images or ["No images found"]}
    return


app._unparsable_cell(
    r"""
    media_node(\"query\":\"\")
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
