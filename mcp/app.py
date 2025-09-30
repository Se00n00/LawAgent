import asyncio
from fastmcp import Client
import numpy as np

client = Client("https://57d169b444ff.ngrok-free.app/mcp")

async def call_tool(name:str):
    async with client:
        result = await client.call_tool("greet",{"name":name})
        print(result)

async def call_curate(data, query):
    async with client:
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

# asyncio.run(call_tool("Ford"))
res = asyncio.run(call_curate(data, query))
print(res)