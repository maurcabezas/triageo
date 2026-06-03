# Triageo Rules

## Product rules

- The app must focus on support triage, not generic chat.
- Every response must produce structured output, not free-form prose only.
- Human review should be a first-class outcome.
- Confidence must always be explicit.

## Engineering rules

- Keep code modular.
- Keep graph nodes small and testable.
- Keep business logic out of route handlers when possible.
- Validate all request and response schemas.
- Use environment variables for all deploy-sensitive values.

## Server rules

- Follow the home server architecture blueprint.
- Do not reuse occupied ports.
- Use explicit `container_name` values.
- Use project-local persistent mounts.
- Use isolated Docker networks.

## Documentation rules

- Every major folder should be understandable from the README.
- Keep setup instructions copy-paste friendly.
- Include one architecture diagram in markdown form.
- Document current and planned ports.

## Portfolio rules

- The repo must look credible even before full completion.
- README should show screenshots later.
- Explain trade-offs and roadmap openly.
- Label in-progress features honestly.
