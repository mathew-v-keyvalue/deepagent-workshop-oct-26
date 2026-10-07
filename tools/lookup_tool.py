"""Stage 2: the lookup tool. Wraps `search_wikipedia` as a tool the agent can call."""

from langchain_core.tools import tool

from wikipedia_lookup import search_wikipedia


@tool
def lookup(query: str) -> dict:
    """Search Wikipedia for factual information on a topic and return up to
    3 short, sourced extracts. Always call this before answering a new
    research question; only use the facts it returns."""
    return {"results": search_wikipedia(query)}
