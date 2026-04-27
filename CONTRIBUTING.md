# Contributing

Thanks for contributing to this project.

## Development Setup

1. Create and activate a virtual environment.
2. Install dependencies from `cyber-strategy-ai/requirements.txt`.
3. Copy `cyber-strategy-ai/.env.example` to `cyber-strategy-ai/.env` and set required values.
4. Start Qdrant and run the API.

## Branching

- Create feature branches from `main`.
- Use clear branch names, for example: `feat/add-report-export`.

## Pull Requests

- Keep PRs focused and small.
- Include a short summary and test notes.
- Update documentation when behavior or APIs change.

## Code Standards

- Follow existing style in the repository.
- Prefer clear function names and small, testable units.
- Do not commit secrets (`.env`, API keys, credentials).

## Suggested Checks Before PR

- Start the app locally without errors.
- Verify Swagger at `http://localhost:8000/docs`.
- Run a strategy flow (`/documents/*`, `/strategy/run`, `/strategy/results/{id}/report`).
