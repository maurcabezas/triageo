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

## Proposed repository layout

```text
triageo/
├── apps/
│   ├── api/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   ├── graph/
│   │   │   ├── models/
│   │   │   ├── services/
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── web/
│       ├── src/
│       ├── public/
│       └── Dockerfile
├── data/
│   ├── knowledge_base/
│   └── triageo.db
├── docs/
├── infra/
│   └── docker/
├── tests/
├── .env.example
├── docker-compose.yml
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
