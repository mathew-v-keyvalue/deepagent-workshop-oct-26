"""Stage 5 exercise: add human approval.

TODO(stage-5): once tools/save_note_tool.py's `save_note` is implemented:
  1. import it: `from tools.save_note_tool import save_note`
  2. add it to the top-level tools: `tools=[save_note]`
  3. add `interrupt_on={"save_note": {"allowed_decisions": ["approve", "reject"]}}`
  4. add a line to SYSTEM_PROMPT: if the user asks to save/remember a note,
     use the save_note tool.
"""

from langchain.agents.middleware import TodoListMiddleware
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

from model import llm
from subagents import research_subagent, writer_subagent

SYSTEM_PROMPT = """
You are a research assistant that gives concise, factual, sourced summaries.

For a new research topic:
1. Break it into 2-3 short sub-questions with write_todos.
2. Delegate each sub-question to the research-agent subagent via the task tool.
3. Delegate the final write-up to the writer-agent subagent, which writes a
   sourced summary to /report.md.
4. Report the final summary back to the user.

If the user asks to change a previous answer (for example "make it
shorter"), rewrite the previous summary yourself instead of re-researching.
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
    subagents=[research_subagent, writer_subagent],
    middleware=[TodoListMiddleware()],
    backend=backend,
    store=store,
    checkpointer=MemorySaver(),
)
