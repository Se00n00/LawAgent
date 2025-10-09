from fastmcp import FastMCP

from embedding import EmbeddingModel
from get_papers import get_papers, get_paper
import numpy as np


mcp = FastMCP("Curator")
embedder = EmbeddingModel("model.onnx","sentence-transformers/all-MiniLM-L6-v2")

# @mcp.tool()
# class InputRequest(BaseModel):
#     data: dict
#     query: str

@mcp.tool()
def greet(name: str) -> dict:
    return {"message":f"Hello, {name}!"}

@mcp.tool
def curate(data, query) -> list:
    """Return the indexes of data items whose similarity to query is above threshold."""
    if len(data) == 0:
        return []
    
    data_strings = ["\n".join([f"{k}:{v}" for k,v in item.items()]) for item in data]
    query_emb = embedder([query])
    data_emb = embedder(data_strings)

    sims = np.atleast_1d(np.dot(data_emb, query_emb.T))


    curated_indexes = [i for i, score in enumerate(sims) if score > 0.3]

    return curated_indexes

@mcp.tool
def embeddings(data:list) -> list:
    """Returns the Embedding vectors for the given data"""
    if len(data) == 0:
        return []
    data_embed = embedder(data)
    return data_embed.tolist()

@mcp.tool
def papers(query: str) -> dict:
    return get_papers(query)

@mcp.tool
def paper(query: str) -> dict:
    return get_paper(query)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
