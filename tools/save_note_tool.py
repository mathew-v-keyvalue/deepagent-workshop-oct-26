"""Stage 5: a tool with a real side effect (writes to disk), gated by human
approval via `interrupt_on` in agent.py.

Optional stretch goal, ported from the Mastra research assistant's
save-note tool.
"""

from pathlib import Path

from langchain_core.tools import tool

NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"


@tool
def save_note(topic: str, note: str) -> dict:
    """Save a short research note to disk when the user explicitly asks to
    save or remember a note. Do not call it otherwise."""
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    file = NOTES_DIR / "notes.md"
    with file.open("a") as f:
        f.write(f"## {topic}\n{note}\n\n")
    return {"saved": True, "file": str(file)}
