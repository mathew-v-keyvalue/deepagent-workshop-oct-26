"""The ONE place the LLM is configured.

LiteLLM exposes an OpenAI-compatible API, so a plain `ChatOpenAI` pointed at
the proxy's base URL works directly - no custom integration needed.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model=os.environ["LITELLM_MODEL"],
    base_url=os.environ["LITELLM_BASE_URL"],
    api_key=os.environ["LITELLM_API_KEY"],
)
