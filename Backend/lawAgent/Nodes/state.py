from pydantic import BaseModel, Field
from typing import TypedDict,List, Dict, Any, Annotated
import operator
from langgraph.graph import MessagesState

# NODE: Gaurd 
class GaurdRailState(BaseModel):
    type:str
    content:int

# NODE: Redirector
class RedirectionState(BaseModel):
    type:str
    content:str

# NODE: Conversation
class conv(BaseModel):
    proceed2Orchestration:bool
    conversation:str

class ConverstationOutput(BaseModel):
    type:str
    content: conv    

# NODE: Worker: Gov_articles
class refine_query(BaseModel):
    query:str

# NODE: Worker: News Synthesizer
class news_arguments(BaseModel):
    worker_query: str
    timelimit: str
    max_results: int
    page: int
    region: str

# NODE: Worker: research Synthesizer
class research_arguments(BaseModel):
    worker_query: str
    

# NODE: Worker: Image Synthesizer
class image_arguments(BaseModel):
    worker_query: str
    timelimit: str
    region: str

# NODE: Worker: Gov Synthesizer
class gov_arguments(BaseModel):
    worker_query: str
    region: str
    max_results: int

# Node: Summerizer
class SummerizerOutput(BaseModel):
    type:str
    content: List[Dict[str, Any]]

# Node: Final Answer
class FinalOutput(BaseModel):
    type:str
    content:str

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