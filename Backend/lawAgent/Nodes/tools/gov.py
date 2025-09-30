import urllib.parse
from ddgs import DDGS
from lawAgent.Nodes.state import WorkerState

def get_original_link(url: str) -> str:
    try:
        parsed_url = urllib.parse.urlparse(url)
        original_link = f"{parsed_url.scheme}://{parsed_url.netloc}"

        return original_link
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return ""


def get_articles(query, region="us-en", max_results=5):
    results = []

    try:
        with DDGS() as ddgs:
            news_results = ddgs.text(
                query=query,
                region=region,
                safesearch="off",
                max_results=5
            )
            for r in news_results:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        print("Error fetching articles:", e)

    return {"search_results": results}