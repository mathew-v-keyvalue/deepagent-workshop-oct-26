"""Simple Streamlit UI for the Deep Agents research assistant.

Deep Agents (unlike Mastra) has no bundled Studio - so this gives the same
visibility a trainee would get from Mastra Studio: chat, the agent's to-do
list, its virtual files, a chronological tool-call activity log, and an
Approve/Reject prompt whenever the agent pauses for human approval.

This file is identical across every stage of the tutorial - it only reads
keys that may not exist yet (todos/files/__interrupt__), so it degrades
gracefully on earlier stages (e.g. no to-do list before Stage 4).
"""

import uuid

import streamlit as st
from langgraph.types import Command

from agent import agent

st.set_page_config(page_title="Deep Agents Research Assistant", layout="wide")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "default-thread"
if "pending_interrupt" not in st.session_state:
    st.session_state.pending_interrupt = None
if "last_result" not in st.session_state:
    st.session_state.last_result = {}

with st.sidebar:
    st.header("Thread")
    st.session_state.thread_id = st.text_input("thread_id", value=st.session_state.thread_id)
    if st.button("New thread"):
        st.session_state.thread_id = f"thread-{uuid.uuid4().hex[:8]}"
        st.session_state.last_result = {}
        st.session_state.pending_interrupt = None
        st.rerun()
    st.caption(
        "Memory (Stage 3+) is scoped to the thread id above. Change it to "
        "start a fresh conversation with no memory of earlier ones."
    )

thread_id = st.session_state.thread_id
config = {"configurable": {"thread_id": thread_id}}

st.title("Deep Agents Research Assistant")

col_chat, col_side = st.columns([2, 1])


def run_agent(payload):
    with st.spinner("Thinking..."):
        return agent.invoke(payload, config=config)


def handle_result(result):
    st.session_state.last_result = result
    interrupts = result.get("__interrupt__")
    st.session_state.pending_interrupt = interrupts[0].value if interrupts else None


with col_chat:
    result = st.session_state.last_result
    for m in result.get("messages", []):
        kind = getattr(m, "type", None)
        content = getattr(m, "content", "")
        if kind == "human" and content:
            with st.chat_message("user"):
                st.write(content)
        elif kind == "ai" and content:
            with st.chat_message("assistant"):
                st.write(content)

    pending = st.session_state.pending_interrupt
    if pending:
        st.warning("The agent is waiting for approval before running a tool:")
        for req in pending.get("action_requests", []):
            st.write(f"**{req['name']}**")
            st.json(req.get("args", {}))
        n = len(pending.get("action_requests", []))
        c1, c2 = st.columns(2)
        if c1.button("Approve", type="primary"):
            decisions = [{"type": "approve"} for _ in range(n)]
            handle_result(run_agent(Command(resume={"decisions": decisions})))
            st.rerun()
        if c2.button("Reject"):
            decisions = [{"type": "reject", "message": "The user rejected this action."} for _ in range(n)]
            handle_result(run_agent(Command(resume={"decisions": decisions})))
            st.rerun()
    else:
        prompt = st.chat_input("Ask about a research topic...")
        if prompt:
            handle_result(run_agent({"messages": [{"role": "user", "content": prompt}]}))
            st.rerun()

with col_side:
    result = st.session_state.last_result

    with st.expander("To-dos", expanded=bool(result.get("todos"))):
        todos = result.get("todos") or []
        if not todos:
            st.caption("No to-do list yet (added in Stage 4: planning).")
        for t in todos:
            st.write(f"- `{t['status']}` {t['content']}")

    with st.expander("Files", expanded=bool(result.get("files"))):
        files = result.get("files") or {}
        if not files:
            st.caption("No virtual files yet (the writer-agent writes /report.md from Stage 4 on).")
        for path, data in files.items():
            st.write(f"**{path}**")
            st.code(data.get("content", ""), language="markdown")

    with st.expander("Activity log", expanded=True):
        messages = result.get("messages", [])
        if not messages:
            st.caption("Tool calls and subagent delegations will show up here.")
        for m in messages:
            for tc in getattr(m, "tool_calls", None) or []:
                st.write(f"→ calling `{tc['name']}`")
                st.json(tc.get("args", {}))
            if getattr(m, "type", None) == "tool":
                st.write(f"← `{getattr(m, 'name', 'tool')}` returned")
                st.code(str(getattr(m, "content", ""))[:800])
        st.caption("For the full nested trace (including inside subagents), open LangSmith.")
