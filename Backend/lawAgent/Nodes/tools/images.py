from state import WorkerState

from ddgs import DDGS

def get_images(state:WorkerState):
    query = state['worker'].description

    try:
        results = DDGS().images(
            query=query,
            region="in-en",
            safesearch="off",
            timelimit=None,
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