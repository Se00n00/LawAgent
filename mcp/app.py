import asyncio
from fastmcp import Client
# from fastmcp import FastMCPClient
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import os

client_url = os.getenv("MCP_CLIENT")
client = Client(client_url)

async def call_tool(name:str):
    async with client:
        result = await client.call_tool("greet",{"name":name})
        print(result.data)
        # return result

async def call_curate(data, query):
    async with client:
        results = await client.call_tool("curate",{"data":data,"query":query})
        results = results.data
        if isinstance(results, np.ndarray) and results.shape == ():
            results = results.item()

        if not isinstance(results, (list, dict, str)):
            results = [results]

        print(results)
        return results

async def call_embeddings(q):
    async with client:
        result = await client.call_tool("embeddings",{"data":q})
        print(result.data)

async def call_papers(q):
    async with client:
        result = await client.call_tool("papers",{"query":q})
        print(result.data)

async def call_paper(q):
    async with client:
        result = await client.call_tool("paper",{"query":q})
        print(result.data)
    
data = [
    {"title": "Amazon Rainforest", 
    "content": "The Amazon rainforest is the largest tropical rainforest in the world."},
    {"title": "Life on Earth", 
    "content": "The life on earth is very good"},
]

# Sample query
query = "environment and life on Earth"

query1 = "Me"
query2 = {"data":data,"query":query}
query3 = ["Hello! there, how are you","I am fine! than you!"]
query4 = "Attention is all you need" 
query5 = "https://arxiv.org/pdf/2501.06425"

res = asyncio.run( call_embeddings(query3))