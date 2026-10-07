"""Stage 1 exercise: hello agent.

TODO(stage-1): write a short system prompt describing the research
assistant's output format (a title, a few bullet points, a one-line
conclusion, under 150 words), then pass it to create_deep_agent along with
the model from model.py.
"""

from deepagents import create_deep_agent

from model import llm

SYSTEM_PROMPT = ""  # TODO(stage-1): write a system prompt

agent = create_deep_agent(model=llm, system_prompt=SYSTEM_PROMPT)
