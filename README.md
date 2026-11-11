# Discover the Cosmos

A space-themed AI agent. You ask a question in plain language; the agent looks at the right source (a searchable archive of astronomy pictures, near-Earth asteroids this week, or the position of the International Space Station) and answers with a short text and a picture or drawing.

**Status:** under construction. See [`docs/progress.md`](docs/progress.md).

This is the application repository (web page and API). Two companion repositories:

- `space-mcp-server`: the MCP server that gives the agent its tools.
- `space-index`: builds the search index (private).

## Documentation

Start with [`docs/README.md`](docs/README.md): architecture overview, decision records, screen specifications.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (installs Python 3.13 and the backend packages)
- [Node.js](https://nodejs.org/) 20.19+ or 22.12+ (for the frontend)

## Run the checks locally

Backend (from `backend/`):

```
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Frontend (from `frontend/`):

```
npm ci
npm run lint
npm run typecheck
npm run format:check
npm test
npm run build
```

## Configuration

Copy `.env.example` to `.env`. It currently has no variables.

## Licence and credits

To be added before release.
