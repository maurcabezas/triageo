# What is LangGraph?

LangGraph is a library by LangChain for building **stateful, multi-step AI workflows**
as a directed graph. Instead of a linear chain (A → B → C), you define:

- **Nodes**: individual units of work (an LLM call, a tool, a classifier)
- **Edges**: the transitions between nodes (can be conditional)
- **State**: a typed dict that flows through and mutates as the graph runs

## Why not just use a for-loop?

A for-loop has no concept of branching, human-in-the-loop pauses, or streaming.
LangGraph gives you:
- **Conditional routing** → send ticket to human review OR auto-resolve
- **Cycles** → retry a node if confidence is low
- **Persistence** → pause and resume mid-graph (useful for approval flows)
- **Streaming** → emit partial results to the UI as the graph runs