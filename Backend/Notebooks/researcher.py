import marimo

__generated_with = "0.14.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


app._unparsable_cell(
    r"""
    def researcher(query):

    """,
    name="_"
)


@app.cell
def _():
    import requests

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    # Optional: If you have an API key, add it here
    API_KEY = None  # replace with your key if you have one

    headers = {"x-api-key": API_KEY} if API_KEY else {}

    return BASE_URL, headers, requests


@app.cell
def _(BASE_URL, headers, requests):
    def get_paper(paper_id):
        url = f"{BASE_URL}/paper/{paper_id}"
        params = {"fields": "title,abstract,authors,citationCount,year"}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    paper = get_paper("First transformer paper")  # Example: "Attention is All You Need"
    print(paper)
    return


@app.cell
def _():
    from langgraph.graph import StateGraph
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_community.utilities.semanticscholar import SemanticScholarAPIWrapper
    from langchain_community.utilities import SearchApiAPIWrapper
    from langchain.tools import Tool

    # assume you have LLM, etc.

    # Tool wrappers
    sem_scholar = SemanticScholarAPIWrapper(top_k_results=3, load_max_docs=3)
    return SemanticScholarAPIWrapper, sem_scholar


@app.cell
def _(sem_scholar):
    def researcher_node(state: dict) -> dict:
        q = state["query"]
        # Use Semantic Scholar
        papers = sem_scholar.run(q)
        # papers is something like list of dicts with abstract etc
        summaries = []
        return papers
        for p in papers:
            title = p.get("Title")
            abstract = p.get("Abstract", "")
            # you could also use the LLM to summarize abstract semantically
            # But for now, include abstract truncated + metadata
            summaries.append({
                "title": title,
                "abstract": abstract[:500] + "..." if len(abstract) > 500 else abstract,
                "authors": p.get("Authors"),
                "year": p.get("year"),
                "url": p.get("openAccessPdf") or p.get("paperId")
            })
        return {"research_results": summaries}
    return (researcher_node,)


@app.cell
def _(researcher_node):
    res = researcher_node({"query":"Fastest Transformer"})
    return (res,)


@app.cell
def _(res):
    res
    return


@app.cell
def _(res):
    print(res)
    return


@app.cell
def _(SemanticScholarAPIWrapper):
    # from langchain_community.utilities.semanticscholar import SemanticScholarAPIWrapper 
    ss = SemanticScholarAPIWrapper(
        top_k_results = 3, load_max_docs = 3
    )
    return (ss,)


@app.cell
def _(ss):
    ss.run("biases in large language models")
    return


@app.cell
def _():
    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    try:
        response = sch.search_paper(query='Harms of ethanol blending in fuels',limit=100)
    except Exception as e:
        print(f"Error: {e}")
    return (response,)


@app.cell
def _(response):
    response.items
    return


@app.cell
def _(response):
    result = []
    for item in response.items:
        names = [i['name'] for i in item["authors"]]
        authors = ", ".join(names)

        if (item['abstract'] != None):
            result.append(
                {
                    "urls":item["externalIds"],
                    "pdfs":item["openAccessPdf"],
                    "year":item['year'],
                    "authors":authors,
                    "title":item['title'],
                    "abstract":item['abstract']
                }
            )
    return (result,)


@app.cell
def _(result):
    result
    return


@app.cell
def _(result):
    papers_text = "\n\n".join(
            [f"Title: {p['title']} ({p['year']})\nAbstract: {p.get('abstract','')}" for p in result]
        )
    return (papers_text,)


@app.cell
def _(papers_text):
    papers_text
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Prompt Engineer (From Orchestrator) <br>
    Sementic Scholar Search (tool) <br>
    Curator <br>
    """
    )
    return


if __name__ == "__main__":
    app.run()
