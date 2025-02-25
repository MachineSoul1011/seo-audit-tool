from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/seo-audit/")
def seo_audit(url: str):
    try:
        response = requests.get(url)
        status_code = response.status_code
        using_https = url.startswith("https")

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title_tag = soup.find("title")
        title = title_tag.text if title_tag else "Not Found"

        # Meta Description
        meta_description_tag = soup.find("meta", attrs={"name": "description"})
        meta_description = meta_description_tag["content"] if meta_description_tag else "Not Found"

        # Word Count
        words = soup.get_text().split()
        word_count = len(words)

        # Links Summary
        links = soup.find_all("a")
        total_links = len(links)
        internal_links = sum(1 for link in links if link.get("href", "").startswith(url))
        external_links = total_links - internal_links

        return {
            "success": True,
            "message": "Report Generated Successfully",
            "result": {
                "URL": url,
                "HTTP Status": status_code,
                "Using HTTPS": using_https,
                "Title": title,
                "Meta Description": meta_description,
                "Word Count": word_count,
                "Total Links": total_links,
                "Internal Links": internal_links,
                "External Links": external_links,
            }
        }

    except Exception as e:
        return {"success": False, "message": str(e)}

