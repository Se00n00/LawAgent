import re
import requests
from bs4 import BeautifulSoup

from fastapi import FastAPI
from pydantic import BaseModel
from semanticscholar import SemanticScholar
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
sch = SemanticScholar()



def get_link(text: str) -> str:
    match = re.search(r'https?://[^\s,]+', text)
    if match:
        link = match.group(0)
        return link.replace("/abs/", "/pdf/")
    return None

def get_papers(query: str):
    result = []
    try:
        response = sch.search_paper(query=query, limit=10)
        
        for item in response.items:
            authors = ", ".join([a['name'] for a in item["authors"]])
            pdf_info = item['openAccessPdf']
            url = pdf_info["url"]

            if not url and 'disclaimer' in pdf_info:
                url = get_link(pdf_info['disclaimer'])

            result.append({
                "urls": item["externalIds"],
                "pdf": url,
                "year": item['year'],
                "authors": authors,
                "title": item['title'],
                "abstract": item['abstract'],
            })
    except Exception as e:
        return {"Error": str(e)}

    return {"search_results": result}

def get_paper(query):
    result = {}
    try:
        url = query
        url = re.sub(r'/pdf/', '/abs/', url)

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("meta", {"name": "citation_title"})
        result["title"] = title_tag["content"] if title_tag else "Title not found"

        authors_tags = soup.find_all("meta", {"name": "citation_author"})
        result["authors"] = ', '.join([a["content"] for a in authors_tags]) if authors_tags else "Authors not found"

        abstract_tag = soup.find("meta", {"name": "citation_abstract"})
        result["abstract"] = abstract_tag["content"] if abstract_tag else "Abstract not found"

        result['pdf'] = query

        match = re.search(r'(?:abs|pdf)/(\d+\.\d+)', query)
        arxiv_id = match.group(1) if match else ''
        result['urls'] = {'arXiv ID': arxiv_id}

        return {"search_results":[result]}
    except requests.RequestException as e:
        return {"Error":str(e)}

class PaperRequest(BaseModel):
    query: str

@app.post("/paper")
def papers(request: PaperRequest):
    return get_papers(request.query)


@app.post("/paper_using_link")
def papers(request: PaperRequest):
    return get_paper(request.query)
