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


# server_params = StdioServerParameters(
#     command="python",
#     args=["MCP_server/server.py"],
# )

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

class MCPHelper:
    def __init__(self, url: str):
        self.url = url

    async def call(self, tool_name: str, params: dict):
        async with Client(self.url) as client:
            results = await client.call_tool(tool_name, params)
            results = results.data

            # Normalize numpy types
            if isinstance(results, np.ndarray) and results.shape == ():
                results = results.item()

            if not isinstance(results, (list, dict, str)):
                results = [results]

            return results


# Create a global helper instance
mcp = MCPHelper(url)

# print(asyncio.run(curated_index(data, query)))