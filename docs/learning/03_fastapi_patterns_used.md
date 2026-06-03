# FastAPI Patterns in Triageo

## Why FastAPI?

- **Auto-generated OpenDocs** at `/docs` — critical for testing triage endpoints
- **Pydantic models** validate all input/output schemas automatically
- **Async-native** — LangGraph runs can be awaited without blocking

## Pattern: Dependency Injection for the graph

```python
# Don't instantiate the graph on every request
# Compile it once at startup and inject it

from functools import lru_cache

@lru_cache(maxsize=1)
def get_triage_graph():
    return build_graph().compile()

@app.post("/api/v1/triage")
async def triage(req: TriageRequest, graph=Depends(get_triage_graph)):
    result = await graph.ainvoke({"raw_text": req.text})
    return TriageResponse(**result)
```

**Why lru_cache**: LangGraph compilation is expensive (it validates the
graph structure). Cache it. One instance, shared across all requests.

## Pattern: Structured error handling

```python
@app.exception_handler(GraphExecutionError)
async def graph_error_handler(request, exc):
    return JSONResponse(status_code=500, content={
        "error": "graph_failed",
        "detail": str(exc),
        "node": exc.failing_node   # custom field
    })
```