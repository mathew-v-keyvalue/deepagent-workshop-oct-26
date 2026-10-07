"""Stage 5 exercise: a tool with a real side effect, gated by human approval.

TODO(stage-5): write a @tool-decorated function named `save_note` that:
  - takes topic: str and note: str
  - appends "## {topic}\n{note}\n\n" to notes/notes.md (create the dir if
    it doesn't exist)
  - returns {"saved": True, "file": <path as str>}

Then, in agent.py, add "save_note" to interrupt_on so the agent pauses for
human approval before the file is written.
"""

from pathlib import Path

from langchain_core.tools import tool

NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"


@tool
def save_note(topic: str, note: str) -> dict:
    """TODO(stage-5): describe what this tool does and when to call it."""
    # TODO(stage-5): implement me
    raise NotImplementedError
