import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
import numpy as np

server_params = StdioServerParameters(
    command="python",
    args=["MCP_server/server.py"],
)

async def curated_index(data, query):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Load MCP tools
            tools = await load_mcp_tools(session)
            curate = next(t for t in tools if t.name == "curate")

            results = await curate.ainvoke({"data":data,"query":query})
            if isinstance(results, np.ndarray) and results.shape == ():
                results = results.item()

            if not isinstance(results, (list, dict, str)):
                results = [results]

            return results

data = [
    {"title": "Amazon Rainforest", 
    "content": "The Amazon rainforest is the largest tropical rainforest in the world."},
    
    {"title": "Python Programming", 
    "content": "Python is a programming language widely used in data science."},
    
    {"title": "Solar System", 
    "content": "Earth is the third planet from the Sun and has life-supporting environment."},
    {"title": "Solar System", 
    "content": "Earth is the third planet from the Sun and has life-supporting environment."}
]

# Sample query
query = "environment and life on Earth"
# print(asyncio.run(curated_index(data, query)))