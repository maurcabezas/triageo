# AGENT.md

You are building Triageo, a production-style LangGraph support triage application.

## Product intent

Triageo is not a toy chatbot. It is a realistic support automation backend and demo app designed to show:
- LangGraph workflow orchestration
- FastAPI service design
- Dockerized deployment
- support-ticket classification and routing
- human-review decision logic

## Core rules

1. Prefer simple, working, inspectable solutions over ambitious architecture.
2. Keep the app deployable on a home server.
3. Preserve explicit state transitions in the LangGraph workflow.
4. Use clean folder structure and descriptive naming.
5. Avoid premature complexity.

## Technical decisions to preserve

- Backend language: Python
- API framework: FastAPI
- Workflow engine: LangGraph
- Persistence: SQLite first
- Deployment: Docker Compose
- Frontend: minimal and functional
- Container names must be explicit
- Docker network must be isolated

## Do not do this in phase one

- no microservices split
- no Kubernetes-first design
- no event bus
- no authentication system
- no vector DB unless retrieval is already working simply
- no heavy frontend framework complexity if a simple UI works

## User context

The project is being built by a developer learning LangGraph while already comfortable with Python, Docker, REST APIs, and agent workflows. The app should teach by doing, not by maximizing abstraction.

## Output quality bar

Every implementation should be:
- runnable
- readable
- debuggable
- easy to explain in an interview

## Preferred development order

1. backend skeleton
2. mock endpoint
3. LangGraph state and nodes
4. local retrieval
5. minimal UI
6. persistence
7. deployment polish

## Naming conventions

- project name: `triageo`
- API container: `triageo-api`
- Web container: `triageo-web`
- Docker network: `triageo-network`

## Definition of success

A hiring manager should be able to look at the repo and quickly understand:
- what problem it solves
- what technologies were used
- how the graph works
- that it runs in Docker
- that it reflects realistic engineering judgment
