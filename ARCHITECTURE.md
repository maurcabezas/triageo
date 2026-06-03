# Triageo Architecture

## Overview

Triageo is a small but realistic GenAI web application for support-ticket triage. The backend exposes a REST API via FastAPI and runs a LangGraph workflow that transforms an incoming ticket into a structured triage decision.

## System components

### 1. Web UI

Purpose:
- submit synthetic or manual tickets
- display triage results
- inspect confidence, route, and retrieved context

Suggested implementation:
- simple React or Next.js frontend
- one main dashboard page
- one debug/trace panel

### 2. API service

Purpose:
- receive ticket payloads
- validate request schema
- call the LangGraph workflow
- persist input and output
- return structured JSON

Suggested implementation:
- FastAPI
- Pydantic request/response models
- modular service layer

### 3. LangGraph workflow

Purpose:
- orchestrate deterministic ticket-processing steps
- make graph state visible and inspectable

Initial nodes:
- ingest_ticket
- classify_ticket
- retrieve_context
- evaluate_confidence
- route_ticket
- decide_human_review
- finalize_output

### 4. Knowledge base

Purpose:
- simulate policy, documentation, and routing rules
- provide retrieval context for classification

MVP format:
- Markdown or JSON documents in `/data/knowledge_base`
- simple keyword retrieval first
- vector retrieval later

### 5. Persistence

MVP:
- SQLite file at `./data/triageo.db`

Stores:
- submitted tickets
- graph outputs
- retrieved snippets
- processing timestamps

### 6. Deployment layer

MVP deployment:
- Docker Compose
- one API container
- one web container
- shared project network

## Request lifecycle

1. User submits ticket through UI.
2. Frontend POSTs to `/api/v1/triage`.
3. API validates payload.
4. API invokes LangGraph workflow.
5. Workflow classifies, enriches, scores, routes.
6. API stores result.
7. Frontend renders structured response.

## Repository Layout

```text
triageo/
├── .github/workflows/
│   └── ci.yml             # GitHub Actions CI syntax & test pipeline
├── apps/
│   ├── api/               # FastAPI application
│   │   ├── app/
│   │   │   ├── api/       # Router endpoints
│   │   │   ├── core/      # Config and LLM drivers
│   │   │   ├── graph/     # LangGraph nodes and compilation
│   │   │   ├── models/    # Pydantic schema types
│   │   │   └── services/  # Knowledge Base and SQLite DB layers
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── web/               # Frontend dashboard static assets
│       ├── index.html
│       ├── style.css
│       ├── app.js
│       └── Dockerfile     # Nginx server
├── data/
│   └── knowledge_base/    # Local policy markdown docs
├── tests/                 # Complete unit and integration test suite
│   ├── conftest.py        # Global fixtures and state configuration
│   ├── integration/
│   │   └── test_api.py    # Integration tests for FastAPI endpoints
│   └── unit/
│       ├── test_nodes.py  # Unit tests for LangGraph nodes with mock LLM calls
│       └── test_routing.py# Unit tests for routing and human escalation decider
├── .env.example
├── docker-compose.yml     # Local/dev docker stack
├── docker-compose.prod.yml# Production stack with log caps
├── pytest.ini             # Pytest settings and warning suppression
└── README.md
```

## State model

Suggested LangGraph state:

```python
class TriageState(TypedDict):
    ticket_id: str
    subject: str
    description: str
    customer_tier: str
    category: str
    priority: str
    retrieved_context: list[str]
    confidence: float
    recommended_team: str
    requires_human_review: bool
    reasoning: str
```

## Testing Architecture

The project implements a testing architecture built using `pytest` to guarantee code correctness, fast validation, and offline readiness:

### 1. Fixtures & Setup (`conftest.py`)
- Sets up Python path injection so tests can resolve the nested `app` package.
- Registers standard `client` (FastAPI `TestClient`) and predefined state fixtures (`base_state`, `high_confidence_state`, `low_confidence_state`) mimicking the actual `TriageState` TypedDict structure.

### 2. Unit Testing Layer (`tests/unit/`)
- **`test_routing.py`**: Asserts deterministic routing tables (category queue targets) and edge cases for the human-escalation decision matrix.
- **`test_nodes.py`**: Validates individual LangGraph node behaviors. Crucially, the Gemini/OpenAI LLM calls are patched/mocked using `unittest.mock` (mocking the `with_structured_output` response) to allow the test suite to run keyless and completely offline.

### 3. Integration Testing Layer (`tests/integration/`)
- **`test_api.py`**: Validates end-to-end FastAPI endpoint logic including:
  - `/health` check status codes and payloads.
  - `/api/v1/triage/history` querying and data representation.
  - `/api/v1/triage` processing requests (with the LangGraph runner output mocked to isolate the REST api layer).
  - Schema validation bounds triggering custom 422 JSON validation responses.

### 4. Suppression & Warning Config (`pytest.ini`)
- Filters third-party deprecation warnings (e.g., from LangGraph, Starlette, or LangChain core) to ensure clean test runner reports.

## Engineering decisions

### Why FastAPI
- async-friendly Python API framework
- easy schema validation with Pydantic
- Swagger docs out of the box
- good fit for model-backed HTTP services

### Why LangGraph
- explicit workflow steps
- visible state transitions
- easier debugging than opaque agent loops
- strong alignment with production-style agent orchestration

### Why SQLite first
- low overhead
- easy local deployment
- good enough for MVP demos
- easy later migration to Postgres

## Home server deployment rules

Based on the current architecture blueprint:

- explicit container names: `triageo-api`, `triageo-web`
- explicit Docker network: `triageo-network`
- local persistent mounts only
- choose next free host ports before deploy

## Suggested ports

Tentative proposal:
- frontend host port: `3004`
- backend host port: `8004`

Before using them, confirm they are still free in the live port registry.
