"""PROVIDED HELPER: you do not need to write or edit this file.

It is the real data source behind the lookup tool (Stage 2): the public
Wikipedia API, no API key needed. Ported from the Mastra research assistant's
src/lib/wikipedia.ts.
"""

import requests

API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "deepagents-research-assistant-tutorial/1.0"


def search_wikipedia(query: str, limit: int = 3) -> list[dict[str, str]]:
    """Search Wikipedia and return the top matches with a short intro extract and the page URL as the source."""
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": str(limit),
        "prop": "extracts",
        "exintro": "1",
        "explaintext": "1",
        "exsentences": "3",
        "format": "json",
        "formatversion": "2",
    }
    response = requests.get(API, params=params, headers={"User-Agent": USER_AGENT}, timeout=10)
    response.raise_for_status()
    data = response.json()
    pages = data.get("query", {}).get("pages", [])
    pages.sort(key=lambda p: p.get("index", 0))
    return [
        {
            "title": page["title"],
            "snippet": page["extract"].strip(),
            "source": f"https://en.wikipedia.org/?curid={page['pageid']}",
        }
        for page in pages
        if page.get("extract")
    ]
