"""Stage 2 exercise: build the lookup tool.

TODO(stage-2): write a @tool-decorated function named `lookup` that:
  - takes a `query: str` argument
  - has a docstring describing what it does and when to call it (the model
    reads this to decide when to use the tool)
  - calls search_wikipedia(query) from wikipedia_lookup.py
  - returns {"results": [...]}
"""

from langchain_core.tools import tool

from wikipedia_lookup import search_wikipedia


@tool
def lookup(query: str) -> dict:
    """TODO(stage-2): describe what this tool does and when to call it."""
    # TODO(stage-2): call search_wikipedia(query) and return {"results": [...]}
    raise NotImplementedError
