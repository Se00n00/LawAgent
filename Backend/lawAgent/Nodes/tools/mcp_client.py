import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
import numpy as np
from dotenv import load_dotenv
from fastmcp import Client
import os

load_dotenv()
url = os.getenv("MCP_CLIENT")
client = Client(url)


# server_params = StdioServerParameters(
#     command="python",
#     args=["MCP_server/server.py"],
# )

async def curated_index(data, query):
    async with client:
        # curate = next(t for t in tools if t.name == "curate")

        results = await client.call_tool("curate",{"data":data,"query":query})
        
        results = results.data
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