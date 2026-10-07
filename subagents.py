"""Stage 4 exercise: subagents for the agent-driven research pipeline.

TODO(stage-4): define two subagent specs:
  - research_subagent: add a "system_prompt" instructing it to call the
    lookup tool and cite sources, and "tools": [lookup].
  - writer_subagent: add a "system_prompt" instructing it to turn research
    notes into a final sourced summary and write it to /report.md (the
    built-in write_file tool).

See the Lab 4 slide ("Delegation: subagents") for the shape of a subagent
dict: {"name": ..., "description": ..., "system_prompt": ..., "tools": [...]}
"""

from tools.lookup_tool import lookup

research_subagent = {
    "name": "research-agent",
    "description": "Answers one research question with short notes and sources.",
    # TODO(stage-4): add "system_prompt" and "tools": [lookup]
}

writer_subagent = {
    "name": "writer-agent",
    "description": "Turns gathered research notes into the final sourced summary.",
    # TODO(stage-4): add "system_prompt"
}
