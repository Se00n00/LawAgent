from pydantic import BaseModel, Field
from typing import TypedDict,List, Dict, Any, Annotated
import operator

# NODE: Conversation
# class ConverstationState(TypedDict):
#     conversation:str

# NODE: Gaurd 
class GaurdRailState(TypedDict):
    gaurdrail_index:int

# NODE: Redirector
class RedirectionState(TypedDict):
    follow_up_Question:str

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
    initialized:bool
    works: List[Worker_Output]
    researcher: SearchState
    images: SearchState
    gov: SearchState
    retreiver: SearchState
    research_content: str
    retreival_content: str
    gov_content:str
    final_answer:str

    complete_section:str

# subGraph State  ??
class OrchestratorState(TypedDict):
    user_query:str
    initialized:bool
    works: List[Worker_Output]
    researcher: SearchState
    images: SearchState
    gov: SearchState
    retreiver: SearchState
    research_content: str
    retreival_content: str
    gov_content:str
    final_answer:str

    complete_section:str
    
    extracted_content: Annotated[List[str], operator.add]

# Worker State
class WorkerState(TypedDict):
    worker:Worker_Output
    search_results: List[Dict[str, Any]]
    curated_results: List[Dict[str, Any]]
    extracted_content: Annotated[List[str], operator.add]