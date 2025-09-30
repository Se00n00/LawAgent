import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(name:str):
    async with client:
        result = await client.call_tool("greet",{"name":name})
        print(result)

async def call_curate(data, query):
    async with client:
        result = await client.call_tool("curate",{"data":data,"query":query})
        # print(result)
        return result.data
    
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