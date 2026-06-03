# Triageo Roadmap

## Phase 0 - Project bootstrap

Goal: create a clean repo foundation.

Tasks:
- create repository structure
- add README, architecture, roadmap, and setup docs
- add `.gitignore`
- add `.env.example`
- add base Docker Compose
- reserve ports in server architecture file

Definition of done:
- repo initialized
- docs committed
- Docker services stubbed

## Phase 1 - Minimal backend MVP

Goal: make one end-to-end triage API work.

Tasks:
- scaffold FastAPI app
- define ticket input schema
- define triage output schema
- implement `/health`
- implement `/api/v1/triage`
- return deterministic mock result first

Definition of done:
- Swagger docs load
- sample request returns valid JSON
- container runs on server

## Phase 2 - First LangGraph workflow

Goal: replace mock logic with a real graph.

Tasks:
- add typed graph state
- implement nodes for classify, retrieve, route, review
- support synthetic support categories
- include confidence score and reasoning summary

Definition of done:
- graph executes successfully
- outputs traceable state
- three sample tickets behave correctly

## Phase 3 - Knowledge base retrieval

Goal: enrich triage with local documentation.

Tasks:
- create 10-30 synthetic KB docs
- implement simple retrieval layer
- inject matched snippets into graph state
- expose retrieved snippets in API response

Definition of done:
- output references retrieved docs
- routing improves versus no-context baseline

## Phase 4 - Minimal UI

Goal: make the project demoable.

Tasks:
- build one-page interface
- add sample ticket presets
- add results panel
- add graph trace/debug panel

Definition of done:
- user can submit tickets from browser
- results are readable and presentation-ready

## Phase 5 - Persistence and history

Goal: keep a record of processed tickets.

Tasks:
- add SQLite integration
- store requests and outputs
- add recent triage history panel

Definition of done:
- page reload keeps history
- API stores and fetches recent decisions

## Phase 5.5 - UI Refinement with Stitch

Goal: Refine and overhaul the UI using Stitch MCP to elevate it past generic templates.

Tasks:
- Define a cohesive design system using Stitch
- Enhance layout aesthetics and modern UI styling components based on Stitch designs
- Integrate the Triage History panel seamlessly into the updated design

Definition of done:
- Complete dashboard matches custom design system assets
- Interactive states and components feel premium and polished

## Phase 6 - Deployment polish & Testing

Goal: make it portfolio-ready and fully validated.

Tasks:
- [x] add Docker Compose for prod
- [x] add GitHub Actions for lint/test/build
- [x] create a comprehensive unit & integration test suite (`pytest`)
- [x] add screenshots and banners to README
- [x] improve error handling and 422 JSON validators
- [x] write setup instructions for home server deploy

Definition of done:
- fresh clone can run locally and tests pass with 100% success
- repo looks credible and fully tested to hiring managers

## Nice-to-have later

- vector search
- evaluation dataset
- feedback loop / correction mode
- human review queue
- webhook ingestion from real helpdesk
- Postgres upgrade
- Kubernetes/k3s deployment
