from lawAgent.Nodes.state import WorkerState

from ddgs import DDGS

def get_images(query, timelimit="y", region="us-en"):
    try:
        Images = DDGS().images(
            query=query,
            region=region,
            safesearch="off",
            timelimit=timelimit,
            page=1,
            backend="auto",
            size=None,
            type_image=None,
            layout=None,
            license_image=None,
            max_results=4
        )
    except Exception as e:
        Images = []
        
    results = []
    for item in Images:
        results.append({
            "title":item["title"],
            "article_url":item["url"],
            "image_url":item["image"]
        })

    return results