# Triageo Graph — Node by Node

## The State object

```python
class TriageState(TypedDict):
    raw_text: str           # original ticket text
    category: str           # output of classifier node
    confidence: float       # 0.0 - 1.0
    kb_results: list[str]   # retrieved knowledge base chunks
    draft_reply: str        # LLM-generated response
    needs_human: bool       # routing flag
    final_response: str     # what we return to the caller
```

State is immutable per step — each node returns a **partial update dict**.
LangGraph merges it. This is why you never mutate state in-place.

## Node 1: `classify_ticket`

**What**: Sends ticket text to an LLM with a classification prompt.
**Why**: Separates intent detection from response generation.
**Returns**: `{ "category": "billing", "confidence": 0.91 }`

## Node 2: `retrieve_knowledge`

**What**: Queries your local knowledge base (text files or Chroma vector DB)
for chunks relevant to the category + raw text.
**Why**: Grounds the reply in real documentation, reduces hallucination.
**Returns**: `{ "kb_results": ["...", "..."] }`

## Node 3 (conditional): `route_on_confidence`

**What**: Not an LLM call — pure Python logic.
```python
def route_on_confidence(state: TriageState) -> str:
    if state["confidence"] < 0.7:
        return "human_review"
    return "generate_reply"
```
**Why**: LangGraph conditional edges take a function that returns the
**name of the next node as a string**. This is the core routing primitive.

## Node 4a: `generate_reply`

**What**: Sends category + KB chunks to LLM → draft reply.
**Returns**: `{ "draft_reply": "...", "needs_human": False }`

## Node 4b: `human_review`

**What**: In Phase 1, this just flags the ticket. In Phase 3, this is
where you pause the graph and emit to a review queue.
**Returns**: `{ "needs_human": True, "final_response": "Queued for review." }`