import marimo

__generated_with = "0.14.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    from langchain_openai import ChatOpenAI
    return (ChatOpenAI,)


@app.cell
def _(ChatOpenAI):
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


@app.cell
def _(llm):
    from typing import Annotated, List, TypedDict
    import operator
    from pydantic import BaseModel,Field

    # Schema for structured output to use in planning
    class Section(BaseModel):
        name: str = Field(
            description="Name for this section of the report.",
        )
        description: str = Field(
            description="Brief overview of the main topics and concepts to be covered in this section.",
        )


    class Sections(BaseModel):
        sections: List[Section] = Field(
            description="Sections of the report.",
        )


    # Augment the LLM with schema for structured output
    planner = llm.with_structured_output(Sections)
    return Annotated, Section, TypedDict, operator, planner


@app.cell
def _():
    from typing_extensions import Literal
    from langchain_core.messages import HumanMessage, SystemMessage
    from langgraph.graph import StateGraph, START, END
    from IPython.display import Image, display
    from langgraph.types import Send
    return END, HumanMessage, START, Send, StateGraph, SystemMessage


@app.cell
def _(
    Annotated,
    END,
    HumanMessage,
    START,
    Section,
    Send,
    StateGraph,
    SystemMessage,
    TypedDict,
    llm,
    operator,
    planner,
):

    # Graph state
    class State(TypedDict):
        topic: str  # Report topic
        sections: list[Section]  # List of report sections
        completed_sections: Annotated[
            list, operator.add
        ]  # All workers write to this key in parallel
        final_report: str  # Final report


    # Worker state
    class WorkerState(TypedDict):
        section: Section
        completed_sections: Annotated[list, operator.add]


    # Nodes
    def orchestrator(state: State):
        """Orchestrator that generates a plan for the report"""

        # Generate queries
        report_sections = planner.invoke(
            [
                SystemMessage(content="Generate a plan for the report."),
                HumanMessage(content=f"Here is the report topic: {state['topic']}"),
            ]
        )

        return {"sections": report_sections.sections}


    def llm_call(state: WorkerState):
        """Worker writes a section of the report"""

        # Generate section
        section = llm.invoke(
            [
                SystemMessage(
                    content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."
                ),
                HumanMessage(
                    content=f"Here is the section name: {state['section'].name} and description: {state['section'].description}"
                ),
            ]
        )

        # Write the updated section to completed sections
        return {"completed_sections": [section.content]}


    def synthesizer(state: State):
        """Synthesize full report from sections"""

        # List of completed sections
        completed_sections = state["completed_sections"]

        # Format completed section to str to use as context for final sections
        completed_report_sections = "\n\n---\n\n".join(completed_sections)

        return {"final_report": completed_report_sections}


    # Conditional edge function to create llm_call workers that each write a section of the report
    def assign_workers(state: State):
        """Assign a worker to each section in the plan"""

        # Kick off section writing in parallel via Send() API
        a = [Send("llm_call", {"section": s}) for s in state["sections"]]
        print(a)
        return a


    # Build workflow
    orchestrator_worker_builder = StateGraph(State)

    # Add the nodes
    orchestrator_worker_builder.add_node("orchestrator", orchestrator)
    orchestrator_worker_builder.add_node("llm_call", llm_call)
    orchestrator_worker_builder.add_node("synthesizer", synthesizer)

    # Add edges to connect nodes
    orchestrator_worker_builder.add_edge(START, "orchestrator")
    orchestrator_worker_builder.add_conditional_edges(
        "orchestrator", assign_workers, ["llm_call"]
    )
    orchestrator_worker_builder.add_edge("llm_call", "synthesizer")
    orchestrator_worker_builder.add_edge("synthesizer", END)

    # Compile the workflow
    orchestrator_worker = orchestrator_worker_builder.compile()

    # Show the workflow
    # display(Image(orchestrator_worker.get_graph().draw_mermaid_png()))

    # Invoke
    state = orchestrator_worker.invoke({"topic": "Create a report on LLM scaling laws"})

    from IPython.display import Markdown
    Markdown(state["final_report"])
    return


@app.cell
def _(Section, Send):
    a = [Send(node='llm_call', arg={'section': Section(name='Introduction to LLM Scaling Laws', description='Overview of large language models (LLMs), the concept of scaling laws, and their significance in AI development.')}), Send(node='llm_call', arg={'section': Section(name='Theoretical Foundations', description='Explanation of the mathematical models behind scaling laws, including key equations from seminal papers like those by Kaplan et al.')}), Send(node='llm_call', arg={'section': Section(name='Empirical Evidence and Experiments', description='Review of experimental results showing how model performance scales with compute, data, and parameters, including case studies from major models.')}), Send(node='llm_call', arg={'section': Section(name='Factors Influencing Scaling', description='Discussion of variables such as data quality, architecture efficiency, and optimization techniques that affect scaling outcomes.')}), Send(node='llm_call', arg={'section': Section(name='Implications and Challenges', description='Analysis of practical implications for AI research, economic costs, environmental impact, and potential limitations of scaling laws.')}), Send(node='llm_call', arg={'section': Section(name='Future Directions and Conclusion', description='Exploration of emerging trends beyond traditional scaling and a summary of key takeaways.')})]
    return (a,)


@app.cell
def _(a):
    len(a)
    return


@app.cell
def _(a):
    a[0]
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
