"""Stage 1: hello agent. No tools yet - just a model and a system prompt."""

from deepagents import create_deep_agent

from model import llm

SYSTEM_PROMPT = """
You are a research assistant that gives concise, factual summaries.
Output format:
- A title
- 3 to 5 bullet points
- A one-line conclusion
Keep the summary under 150 words.
"""

agent = create_deep_agent(model=llm, system_prompt=SYSTEM_PROMPT)
