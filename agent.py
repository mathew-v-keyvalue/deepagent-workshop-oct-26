"""Stage 2 exercise: wire up the lookup tool.

TODO(stage-2): once tools/lookup_tool.py's `lookup` function is implemented:
  1. import it: `from tools.lookup_tool import lookup`
  2. pass it to create_deep_agent: `tools=[lookup]`
  3. add a rule to SYSTEM_PROMPT: always call lookup before answering a new
     topic, cite the source field, and say so if it returns no results.
"""

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
# TODO(stage-2): add the tool-use rule above, and register `tools=[lookup]` below.

agent = create_deep_agent(model=llm, system_prompt=SYSTEM_PROMPT)
