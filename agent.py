"""Stage 3 exercise: add memory.

TODO(stage-3): wire up:
  1. `checkpointer=MemorySaver()` (from langgraph.checkpoint.memory) so the
     agent remembers earlier turns within the same thread_id.
  2. a `backend=CompositeBackend(default=StateBackend(), routes={"/memories/":
     StoreBackend(namespace=lambda rt: ("memories",), store=store)})` (from
     deepagents.backends) so anything written under /memories/ survives
     across threads.
  3. `store=InMemoryStore()` (from langgraph.store.memory), passed to both
     StoreBackend above and create_deep_agent below.
"""

from deepagents import create_deep_agent

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

agent = create_deep_agent(model=llm, system_prompt=SYSTEM_PROMPT, tools=[lookup])
