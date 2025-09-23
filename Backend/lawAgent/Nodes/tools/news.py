from state import WorkerState

from ddgs import DDGS

def get_news(state:WorkerState):
    query = state['worker'].description
    try:
        results = DDGS().news(
            query=query,
            region="us-en",
            safesearch="off",
            timelimit="d",
            max_results=10,
            page=1,
            backend="auto"
        )
    except Exception as e:
        results = []
    for item in results:
        print(item)
    News = []
    for item in results:
        News.append({
            "title":item["title"],
            "date": item["date"],
            "article_url":item["url"],
            "image_url":item["image"],
            "source":item["source"]
        })

    return {"search_results":News}