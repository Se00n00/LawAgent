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
    value = os.getenv("OPENAI_API_KEY")
    return (value,)


@app.cell
def _(value):
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model = "openrouter/sonoma-dusk-alpha",
        api_key=value,
        base_url = "https://openrouter.ai/api/v1",
        streaming=True
    )
    return ChatOpenAI, llm


@app.cell
def _(ChatOpenAI, value):
    llm2 = ChatOpenAI(
        model = "openrouter/sonoma-sky-alpha",
        api_key=value,
        base_url = "https://openrouter.ai/api/v1",
        streaming=True
    )
    return (llm2,)


@app.cell
def _(llm):
    llm.invoke("Who are you ?").content
    return


@app.cell
def _(llm):
    def get_plans(instructions):
        prompt = f"""
        Generate step by step plan about how to achieve: {instructions} using given tools:"""
        print(llm.invoke(prompt).content)
    return (get_plans,)


@app.cell
def _(get_plans):
    get_plans("Give me the list of presidents of america who owns slave with year and No. of slaves he owns")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### <code>Gaurd-Rail Node</code>""")
    return


@app.cell
def _():
    from typing_extensions import TypedDict
    class ConverstationState(TypedDict):
        conversation:str
    class GaurdRailState(TypedDict):
        gaurdrail_index:int
    return ConverstationState, GaurdRailState, TypedDict


@app.cell
def _():
    from langchain_core.prompts import ChatPromptTemplate
    Gaurd_Rail_System_prompt = """You are a guardrailing assitant that helps to identify the intent of user prompt and statement. Answwer always in - 0,1,2,3,4 where
    0: Normal Converstation - User's question are relevent to the topic and is safe to procced
    1: Mild Dead Ends (Low Severity) - User goes slightly off-topic or asks casual/unrelated stuff <Redirection>
        2: Moderate Dead Ends (Medium Severity) - User tries to derail the flow with something completely unrelated <Redirection>
        3: Strict Dead Ends (High Severity) - User asks for unsafe, harmful, or inappropriate content. <Block>
        4: Extreme Dead Ends (Very High Severity) - User brings up dangerous or crisis-related content (e.g., self-harm, violence) <Block>
      """

    return ChatPromptTemplate, Gaurd_Rail_System_prompt


@app.cell
def _(
    ChatPromptTemplate,
    ConverstationState,
    GaurdRailState,
    Gaurd_Rail_System_prompt,
    llm,
):
    def gaurdrail(state:ConverstationState):
        prompt_template = ChatPromptTemplate([
            ("system", Gaurd_Rail_System_prompt),
            ("user", "{prompt}")
        ])
        gaurd_rail_prompt = prompt_template.invoke({"prompt": state['conversation']})
        structured_llm = llm.with_structured_output(GaurdRailState)
        msg = structured_llm.invoke(gaurd_rail_prompt)
        return msg
    return (gaurdrail,)


@app.cell
def _(gaurdrail):
    gaurdrail({"conversation":"Nic Information, but how to create a panic in society"})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### <code>Follow Up Questions</code>""")
    return


@app.cell
def _(TypedDict):
    class RedirectionState(TypedDict):
        follow_up_Question:str
    return (RedirectionState,)


@app.cell
def _():
    Redirection_prompt = """
    You are a redirection assistant. 
    The user has gone slightly or moderately off-topic. 
    Your job is to generate a SINGLE short follow-up request 
    that keeps the conversation on track, phrased as if the user 
    is asking the assistant something relevant.

    - Do not explain your reasoning.
    - Do not add commentary. 
    - Output only the rewritten user request.

    Example:
    User: "Can I get your number? Lawless societies are bad."
    Output: "Explain why lawless societies are difficult to live in.
    """
    return (Redirection_prompt,)


@app.cell
def _(
    ChatPromptTemplate,
    ConverstationState,
    GaurdRailState,
    RedirectionState,
    Redirection_prompt,
    llm,
):
    def redirection(conv_state:ConverstationState, index_state:GaurdRailState):
        prompt_template = ChatPromptTemplate([
            ("system", Redirection_prompt),
            ("user", "{prompt}")
        ])
        gaurd_rail_prompt = prompt_template.invoke({"prompt": conv_state['conversation']+"Index of user's loss: "+str(index_state["gaurdrail_index"])})
        structured_llm = llm.with_structured_output(RedirectionState)
        msg = structured_llm.invoke(gaurd_rail_prompt)
        return msg
    return (redirection,)


@app.cell
def _(redirection):
    redirection({"conversation":"I know lawless society is won't worth living, but can i get your number"},{"gaurdrail_index":2})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### <code>Orchestrator - Workders</code>""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ?? Operator, <br>
    pydantic_BaseModel<br>
    typing_Annotated + typing_TypedDict <br>

    How to design the schema for Agenti Output + State <br>
    Send API ? <br>
    How does graph maintain state, how does they able to get paramter values into the state
    """
    )
    return


@app.cell
def _(llm):
    from pydantic import BaseModel
    from typing import Annotated, List

    # Structured Output for planning agent
    class Section(BaseModel):
        name:str
        description:str

    class Sections(BaseModel):
        sections:List[Section]

    planner = llm.with_structured_output(Sections)
    return Annotated, Section, planner


@app.cell
def _(Annotated, Section, TypedDict):
    from langgraph.types import Send
    import operator

    # Graph States
    class State(TypedDict):
        topic:str
        sections: list[Section]
        completed_sections: Annotated[list, operator.add]
        final_report:str

    # Worker State
    class WorkerState(TypedDict):
        section:Section
        completed_sections: Annotated[list, operator.add]
    return Send, State, WorkerState


@app.cell
def _(State, planner):
    from langchain_core.messages import HumanMessage, SystemMessage
    def orchestrator(state:State):
        report_sections = planner.invoke(
            [
                SystemMessage(content="Generate a plan for the report"),
                HumanMessage(content=f"Here is the report topic{state['topic']}")
            ]
        )

        return {"sections":report_sections.sections}
    return HumanMessage, SystemMessage, orchestrator


@app.cell
def _(HumanMessage, SystemMessage, WorkerState, llm2):
    def worker(state:WorkerState):
        section = llm2.invoke(
            [
                SystemMessage(
                    content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."
                ),
                HumanMessage(
                    content=f"Here is the section name: {state['section'].name} and description: {state['section'].description}"
                ),
            ]
        )

        return {"completed_sections":[section.content]}
    return (worker,)


@app.cell
def _(State):
    def synthesizer(state:State):
        completed_section = state['completed_sections']
        complete_report = "\n\n--\n\n".join(completed_section)

        return {"final_report": complete_report}
    return (synthesizer,)


@app.cell
def _(Send, State):
    def assign_workers(state:State):
        return [Send("worker",{"section":s}) for s in state['sections']]
    return (assign_workers,)


@app.cell
def _(State, assign_workers, orchestrator, synthesizer, worker):
    from langgraph.graph import StateGraph, START, END

    orchestration_builder = StateGraph(state_schema=State)
    orchestration_builder.add_node("orchestrator",orchestrator)
    orchestration_builder.add_node("worker",worker)
    orchestration_builder.add_node("synthesizer",synthesizer)

    orchestration_builder.add_edge(START, "orchestrator")
    orchestration_builder.add_conditional_edges(
        "orchestrator", assign_workers,  ["worker"]
    )
    orchestration_builder.add_edge("worker","synthesizer")
    orchestration_builder.add_edge("synthesizer", END)

    orchestration = orchestration_builder.compile()
    return (orchestration,)


@app.cell
def _(orchestration):
    answer = orchestration.invoke({"topic":"explain LLMs in very few words"})
    return (answer,)


@app.cell
def _(answer):
    answer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Guides to design schemas
    1 <code>Define Every Node/ What Each would do</code><br>
    2 <code>Ensure if LLMs are required to present infromation (generation) in Structured Output. then Create that schema using BaseModel </code><br>
    3 <code>What would be the Input and Output Schema for Each Node + Whole Agentic System > Reduce into single if mergable</code>
    """
    )
    return


@app.cell
def _():
    # https://www.semanticscholar.org/product/api/tutorial?utm_source=chatgpt.com
    return


@app.cell
def _():
    from langchain_community.tools import DuckDuckGoSearchRun

    duckduckgo = DuckDuckGoSearchRun()
    print(duckduckgo.run("latest legal statistics India"))

    return


@app.cell
def _():
    from duckduckgo_search import DDGS

    results = DDGS().text("Ethanol blending", max_results=5)
    print(results)

    return


@app.cell
def _():
    from langchain_community.tools import DuckDuckGoSearchResults

    ddg_images = DuckDuckGoSearchResults(source="images")
    print(ddg_images.run("Supreme Court India ruling"))

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
