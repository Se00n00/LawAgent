import marimo

__generated_with = "0.14.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from ddgs import DDGS
    return (DDGS,)


@app.cell
def _(mo):
    mo.md(r"""### Media Node""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Filter Out Relvent and remove dedundant results""")
    return


@app.cell
def _(DDGS):
    def Media(query):
        try:
            results = DDGS().images(
                query=query,
                region="us-en",
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

        return Images
    return (Media,)


@app.cell
def _(Media):
    Media("Law inforcement of usa")
    return


@app.cell
def _(mo):
    mo.md(r"""### Retreiver""")
    return


@app.cell
def _(DDGS):
    def Retreiver(query):
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

        return News
    return (Retreiver,)


@app.cell
def _(Retreiver):
    Retreiver("Bihar Pollitics")
    return


@app.cell
def _():
    import requests

    url = 'https://www.news18.com/opinion/the-social-justice-myth-how-lalus-legacy-narrowed-bihars-politics-ws-l-9582490.html'
    return (url,)


@app.cell
def _():
    from newspaper import Article
    return (Article,)


@app.cell
def _(Article, url):
    article = Article(url)
    return (article,)


@app.cell
def _(article):
    article.download()
    article.parse()
    return


@app.cell
def _(article):
    article.text
    return


@app.cell
def _(article):
    article.summary
    return


@app.cell
def _():
    import urllib.parse

    def get_original_link(url: str) -> str:
        try:
            # Use urlparse to break the URL into components
            parsed_url = urllib.parse.urlparse(url)

            # The base URL consists of the scheme (https, http, etc.) and the netloc (domain)
            original_link = f"{parsed_url.scheme}://{parsed_url.netloc}"

            return original_link
        except Exception as e:
            print(f"Error parsing URL: {e}")
            return ""
    return (get_original_link,)


@app.cell
def _(get_original_link):
    get_original_link("https://www.linkedin.com/pulse/beyond-mileage-myths-why-ethanol-blending-makes-sense-thiagarajan-gimcf")
    return


@app.cell
def _(DDGS, get_original_link):

    # Define your search query
    query = "Ethanol blending site:.gov.in"
    def get_articles(query):
        query += " site:.gov.in"
        print(query)
        results = []
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=20):
                    url = r.get("href")
                    print(url)
                    if(r.get('body') != None and url and get_original_link(url).endswith(".gov.in")):
                        results.append({
                            "Title": r.get("title"),
                            "URL": r.get("href"),
                            "Snippet": r.get("body")
                        })
        except Exception as e:
            pass
        return results
    return (get_articles,)


@app.cell
def _(get_articles):
    get_articles("Ethanol Blending ")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
