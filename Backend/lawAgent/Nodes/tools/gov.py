import urllib.parse
from ddgs import DDGS
from state import WorkerState

def get_original_link(url: str) -> str:
    try:
        parsed_url = urllib.parse.urlparse(url)
        original_link = f"{parsed_url.scheme}://{parsed_url.netloc}"

        return original_link
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return ""

def get_articles(state:WorkerState):
    query = state['worker'].description
    query += " site:.gov.in"
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=20):
                url = r.get("href")
                print(url)
                if(r.get('body') != None and url and get_original_link(url).endswith(".gov.in")):
                    results.append({
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "snippet": r.get("body")
                    })
    except Exception as e:
        pass
    
    return {"search_results":results}