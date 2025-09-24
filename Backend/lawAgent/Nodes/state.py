from pydantic import BaseModel, Field
from typing import TypedDict,List, Dict, Any, Annotated
import operator
from langgraph.graph import MessagesState

# NODE: Conversation
class ConverstationOutput(BaseModel):
    proceed2Orchestration:bool
    conversation:str

# NODE: Gaurd 
class GaurdRailState(BaseModel):
    gaurdrail_index:int

# NODE: Redirector
class RedirectionState(BaseModel):
    follow_up_Question:str

# NODE: Worker: Gov_articles
class refine_query(BaseModel):
    query:str

# Node: Summerizer
class SummerizerOutput(BaseModel):
    Summeries: List[Dict[str, Any]]

class Worker_Output(BaseModel):
    name:str = Field(..., description="Name of Selected Worker")
    description:str = Field(..., description="Description of the work assigned by the Orchestrator")

# Node: Orchestrator
# How the output state schema would looks like if Agent is multi-step (Cycle in StateGraph) ??
class Orchestrator_Output(BaseModel):
    works: List[Worker_Output]


class SearchState(TypedDict):
    search_results: List[Dict[str, Any]]
    curated_results: List[Dict[str, Any]]


# Graph State
class State(TypedDict):
    user_query:str
    gaurd_index:int
    redirection:str
    proceed2Orchestration:bool
    conversation:list[MessagesState]
    works: List[Worker_Output]
    extracted_content: Annotated[List[str], operator.add]
    complete_section:str
    final_answer:str
    Summeries: List[Dict[str, Any]]

# Worker State
class WorkerState(TypedDict):
    worker_query:str
    search_results: List[Dict[str, Any]]
    curated_results: List[Dict[str, Any]]
    extracted_content: Annotated[List[str], operator.add]