"""create_deep_agent wiring - the file that grows stage by stage.

Stage 1: a hello-world agent with a system prompt.
Stage 2: + the lookup tool.
Stage 3: + memory (checkpointer, thread-scoped files + a cross-thread
          /memories/ store).
Stage 4: + planning (write_todos) and subagent delegation - the mini project.
Stage 5: + human approval on save_note (interrupt_on).
"""

from langchain.agents.middleware import TodoListMiddleware
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

from model import llm
from subagents import research_subagent, writer_subagent
from tools.save_note_tool import save_note

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
If the user asks you to save or remember a note, use the save_note tool.
"""

# Long-term store: anything written under /memories/ survives across threads.
store = InMemoryStore()

backend = CompositeBackend(
    default=StateBackend(),  # per-thread scratch files (e.g. /report.md)
    routes={
        "/memories/": StoreBackend(namespace=lambda rt: ("memories",), store=store),
    },
)

agent = create_deep_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    tools=[save_note],
    subagents=[research_subagent, writer_subagent],
    middleware=[TodoListMiddleware()],
    backend=backend,
    store=store,
    checkpointer=MemorySaver(),
    interrupt_on={"save_note": {"allowed_decisions": ["approve", "reject"]}},
)
