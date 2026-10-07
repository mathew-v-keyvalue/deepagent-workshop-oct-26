"""Stage 4: subagents for the agent-driven research pipeline.

The main agent plans sub-questions with write_todos, then delegates each one
to research-agent via the built-in task tool, and finally delegates the
write-up to writer-agent, which writes the final report to a virtual file.
"""

from tools.lookup_tool import lookup

research_subagent = {
    "name": "research-agent",
    "description": (
        "Answers one research question with short notes and sources. "
        "Call once per sub-question."
    ),
    "system_prompt": (
        "You are a careful researcher. Call the lookup tool, then write 2-3 "
        "short bullet notes with the source URL for each fact. Cite every "
        "source. If lookup returns nothing, say you found no information."
    ),
    "tools": [lookup],
}

writer_subagent = {
    "name": "writer-agent",
    "description": (
        "Turns gathered research notes into the final sourced summary and "
        "writes it to /report.md."
    ),
    "system_prompt": (
        "You are a careful technical writer. Given research notes from one "
        "or more sub-questions, write a final summary: a title, 3-5 bullet "
        "points, a one-line conclusion, and a sources list. Keep it under "
        "150 words and cite every source. Write the result to /report.md "
        "using the write_file tool."
    ),
}
