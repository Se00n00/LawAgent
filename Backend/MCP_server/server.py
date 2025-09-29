from mcp.server.fastmcp import FastMCP
from embedding import EmbeddingModel
import numpy as np

mcp = FastMCP("ResourceCurator")
embedder = EmbeddingModel("MCP_server/model.onnx","sentence-transformers/all-MiniLM-L6-v2")

@mcp.tool()
def curate(data, query, threshold=0.5) -> list:
    """Return the indexes of data items whose similarity to query is above threshold."""
    if len(data) == 0:
        return []
    
    data_strings = ["\n".join([f"{k}:{v}" for k,v in item.items()]) for item in data]
    query_emb = embedder([query])
    data_emb = embedder(data_strings)

    sims = np.dot(data_emb, query_emb.T).squeeze()

    curated_indexes = [i for i, score in enumerate(sims) if score > threshold]

    return curated_indexes
    

if __name__ == "__main__":
    mcp.run(transport="stdio")
