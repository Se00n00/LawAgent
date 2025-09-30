from lawAgent.Nodes.state import WorkerState

from ddgs import DDGS

def get_news(query, timelimit="y", max_results=5, page=1, region="us-en"):
    """
    Fetch news based on worker state and optional parameters.

    query: search query
    timelimit: 'd', 'w', 'm', 'y'
    max_results: max number of results to fetch
    page: which page of results
    region: language/region
    """
    try:
        News = DDGS().news(
            query=query,
            region="us-en",
            safesearch="off",
            timelimit="y",
            max_results=5,
            page=1,
            backend="auto"
        )
    except Exception as e:
        News = []

    results = []
    for item in News:
        results.append({
            "title": item.get("title", ""),
            "body": item.get("body", ""),
            "article_url": item.get("url", ""),
            "image_url": item.get("image", ""),
            "source": item.get("source", ""),
            "date": item.get("date", "")
        })


    return results