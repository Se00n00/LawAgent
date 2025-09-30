from fastmcp import FastMCP

from embedding import EmbeddingModel
import numpy as np


mcp = FastMCP("Curator")
embedder = EmbeddingModel("model.onnx","sentence-transformers/all-MiniLM-L6-v2")

# @mcp.tool()
# class InputRequest(BaseModel):
#     data: dict
#     query: str

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def curate(data, query) -> list:
    """Return the indexes of data items whose similarity to query is above threshold."""
    if len(data) == 0:
        return []
    
    data_strings = ["\n".join([f"{k}:{v}" for k,v in item.items()]) for item in data]
    query_emb = embedder([query])
    data_emb = embedder(data_strings)

    sims = np.dot(data_emb, query_emb.T).squeeze()

    curated_indexes = [i for i, score in enumerate(sims) if score > 0.3]

    return curated_indexes
    


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
