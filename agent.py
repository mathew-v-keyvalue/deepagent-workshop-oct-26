"""Stage 4 exercise: planning and subagent delegation.

TODO(stage-4): in subagents.py, fill in `research_subagent` and
`writer_subagent` (system_prompt + tools).

TODO(stage-4): here, replace `tools=[lookup]` with
`subagents=[research_subagent, writer_subagent]`, add
`middleware=[TodoListMiddleware()]` (from langchain.agents.middleware), and
update SYSTEM_PROMPT to plan sub-questions with write_todos, delegate each
to research-agent, then delegate the write-up to writer-agent.
"""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

from model import llm
from tools.lookup_tool import lookup

SYSTEM_PROMPT = """
You are a research assistant that gives concise, factual summaries.
Output format:
- A title
- 3 to 5 bullet points
- A one-line conclusion
- A sources list
Keep the summary under 150 words.
If the user asks you to change a previous answer (for example "make it shorter"), rewrite your previous summary.
Always call the lookup tool before answering a new research topic. Only use facts it returns.
Cite the source field. If it returns no results, say you have no information on that topic.
"""

store = InMemoryStore()

backend = CompositeBackend(
    default=StateBackend(),
    routes={
        "/memories/": StoreBackend(namespace=lambda rt: ("memories",), store=store),
    },
)

agent = create_deep_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    tools=[lookup],
    backend=backend,
    store=store,
    checkpointer=MemorySaver(),
)
