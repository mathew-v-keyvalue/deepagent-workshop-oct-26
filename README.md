# Research Assistant (Deep Agents + LiteLLM)

Day 2 companion to `../Mastra-research-assistant`: the same research assistant,
rebuilt on [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview)
(a Python harness built on LangGraph) instead of Mastra, so the two harnesses
can be compared directly.

Tutorial project built in stages, same convention as the Mastra repo:

- **`checkpoint-N`** is the **exercise** for stage N: everything up to stage N-1
  is done, the stage-N code is blanked out, and `# TODO(stage-N)` comments give
  hints. It still imports, so the UI runs even before you finish.
- **`stage-N`** is the **answer** for that exercise (and the starting point for
  `checkpoint-(N+1)`'s work). `stage-5` is the complete mini project.

| Exercise | Answer | You build | Try it |
|---|---|---|---|
| `checkpoint-1` | `stage-1` | `agent.py`: write the system prompt | Ask "solar energy" |
| `checkpoint-2` | `stage-2` | `tools/lookup_tool.py`: the lookup tool's docstring and body; register it and add the tool-use rule in `agent.py` | Same prompt; the Activity log panel shows the `lookup` call |
| `checkpoint-3` | `stage-3` | `agent.py`: wire up `checkpointer`, `backend` (with a `/memories/` route), and `store` | Ask "make it shorter" (same thread id) -> works; new thread id -> forgets |
| `checkpoint-4` | `stage-4` | `subagents.py`: the `research-agent` / `writer-agent` subagent specs | The To-dos panel fills in; `/report.md` appears in Files |
| `checkpoint-5` | `stage-5` | `tools/save_note_tool.py`'s body; add `save_note` to `interrupt_on` in `agent.py` | Ask it to save a note -> Approve/Reject prompt appears before `notes/notes.md` is written |

Hints name the Deep Agents APIs to use. Stuck? Compare with the matching
`stage-N` branch.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # LITELLM_BASE_URL (ends in /v1), LITELLM_API_KEY, LITELLM_MODEL
streamlit run app.py
```

The lookup tool queries the public Wikipedia API, so it needs internet access
but no API key. `LANGSMITH_API_KEY` / `LANGSMITH_TRACING=true` in `.env` are
optional but turn on full nested tracing in [LangSmith](https://smith.langchain.com) -
Deep Agents has no bundled Studio equivalent, so the included `app.py` is a
small Streamlit UI showing the chat, the agent's to-do list, its virtual
files (e.g. `/report.md`), a tool-call activity log, and the Approve/Reject
prompt for human-in-the-loop approval. It's unchanged across every stage.

## Project layout

```
model.py              # LLM config (LiteLLM, OpenAI-compatible) - provided
wikipedia_lookup.py    # Wikipedia search helper - provided
agent.py               # create_deep_agent(...) wiring - grows stage by stage
tools/lookup_tool.py    # Stage 2
tools/save_note_tool.py # Stage 5
subagents.py            # Stage 4
app.py                  # Streamlit UI - same on every branch
```

## Mastra and Deep Agents, side by side

| Dimension | Mastra (Day 1) | Deep Agents (Day 2) |
|---|---|---|
| Language | TypeScript | Python |
| Kind | Framework with harness features | Harness on LangGraph |
| Tools | `createTool` with a Zod schema | Python function with a docstring (`@tool`) |
| Memory | History, working, semantic, observational | Checkpointer, virtual files, store, AGENTS.md |
| Orchestration | Workflows you define, or a supervisor | The agent plans (`write_todos`) and delegates (`task`) |
| Human approval | `suspend`/`resume`, `requireApproval` | `interrupt_on` and `Command(resume=...)` |
| Dev UI and traces | Studio, locally | LangSmith and LangGraph Studio |
