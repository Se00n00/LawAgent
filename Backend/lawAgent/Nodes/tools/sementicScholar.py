from lawAgent.Nodes.state import WorkerState

import asyncio
import uvloop

# Set default loop to asyncio's default instead of uvloop
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

from semanticscholar import SemanticScholar
sch = SemanticScholar()

def get_papers(state:WorkerState):
    query = state["worker_query"]
    result = []
    try:
        response = sch.search_paper(query=query,limit=100)
        
        for item in response.items:
            names = [i['name'] for i in item["authors"]]
            authors = ", ".join(names)

            if (item['abstract'] != None):
                result.append(
                    {
                        "urls":item["externalIds"],
                        "pdfs":item["openAccessPdf"],
                        "year":item['year'],
                        "authors":authors,
                        "title":item['title'],
                        "abstract":item['abstract']
                    }
                )
    except Exception as e:
        print(f"Error: {e}")
    
    return {"search_results":result}