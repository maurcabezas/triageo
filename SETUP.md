# Triageo Setup Instructions

## 1. Create the repository

Suggested repo name:

```bash
git init triageo
cd triageo
```

## 2. Create the folder structure

```bash
mkdir -p apps/api/app apps/web data/knowledge_base docs infra/docker scripts tests
```

## 3. Copy documentation files

Place these files in the repo root or `docs/` as appropriate:

- README.md
- ARCHITECTURE.md
- ROADMAP.md
- AGENT.md
- RULES.md
- SETUP.md

## 4. Add `.gitignore`

Use the provided `.gitignore` from this starter pack.

## 5. Reserve ports

Before writing the app, update the server `arch.md` file with a new allocation.

Recommended tentative allocation:
- `3004` for web
- `8004` for api

Only keep these if they are truly free.

## 6. Create environment file

```bash
cp .env.example .env
```

## 7. Build phase one first

Phase one target:
- FastAPI app running
- `/health` works
- `/api/v1/triage` accepts JSON
- Docker Compose starts containers cleanly

## 8. Home server deployment pattern

Use these conventions:

```yaml
container_name: triageo-api
container_name: triageo-web
networks:
  - triageo-network
```

Port mapping pattern:

```yaml
ports:
  - "${HOST_IP:-10.0.1.36}:${API_PORT:-8004}:8000"
```

## 9. Suggested first commit order

1. docs and repo scaffold
2. FastAPI hello world
3. Docker Compose
4. first triage schema
5. first LangGraph workflow
6. basic frontend
