"""Stage 3: + memory.

A checkpointer scopes conversation history to a thread_id: same thread id =
the agent remembers earlier turns; new thread id = it forgets. The
CompositeBackend below routes anything written under /memories/ to a
cross-thread store instead of per-thread state, so it survives even a new
thread id.
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

# Long-term store: anything written under /memories/ survives across threads.
store = InMemoryStore()

backend = CompositeBackend(
    default=StateBackend(),  # per-thread scratch files
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
