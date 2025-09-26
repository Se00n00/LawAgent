from lawAgent.Nodes.state import WorkerState

from ddgs import DDGS

def get_images(query, timelimit="y", region="us-en"):
    try:
        results = DDGS().images(
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
        )
    except Exception as e:
        results = []
    Images = []
    for item in results:
        Images.append({
            "title":item["title"],
            "article_url":item["url"],
            "image_url":item["image"]
        })

    return {"search_results":Images}