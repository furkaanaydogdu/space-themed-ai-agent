# AGENTS.md: Discover the Cosmos (app repo)

React frontend (`frontend/`) and Python API with the agent (`backend/`), built into one container. Companion repos: `space-mcp-server` (the agent's tools) and `space-index` (the search index, private). Start with `docs/README.md` for the architecture, decision records (ADRs) and screen specs.

Open Claude Code at the repo root, not inside `frontend/` or `backend/`.

## Commands

Backend, from `backend/`:

```
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Frontend, from `frontend/`:

```
npm ci
npm run lint
npm run typecheck
npm run format:check
npm test
npm run build
```

Run every check that applies to your change before saying a step is done, and report the real results. Do not invent commands; if one is missing, ask.

## How to work

- Work arrives as a step brief. Do only that step.
- Plan first. Before editing, list the files you will touch and the tests you will add, then wait for my approval.
- Keep each change small: at most about 3 files or 150 changed lines. If the step needs more, stop and propose how to split it.
- Do not add features, refactors, abstractions or dependencies that were not asked for. If you see something worth improving, mention it; do not do it.
- If a requirement is unclear, or a library API is not verified, ask or check the current docs. Do not guess from memory.
- Do not commit, push, create branches or edit `.github/` unless the step says so. I do the git work.
- When done, report: what changed and why; the one or two places most worth reading closely; any decision you made; anything you could not verify. I read every diff to learn from it, so prefer plain, idiomatic code over clever code, and explain an unfamiliar idiom in one line the first time you use it.

## Code rules

- Functions are short (under about 30 lines) and do one thing. If you need "and" to describe one, split it.
- Names say what a thing is or does. No abbreviations.
- Comments explain why, not what. No commented-out code. No TODO without a step reference.
- Strict types in both languages. No `Any`, `# type: ignore`, `as any`, `noqa` or lint-disable without a one-line reason and my approval.
- Do not swallow errors: no bare `except`, no empty `catch`. Fail loudly or return an explicit result.
- Prefer plain functions and data over classes and inheritance unless state is needed. Do not abstract until the same code appears a third time.
- Tests are deterministic: no network, no model calls. Use fake models and fake tools (including ones that never answer, and oversized or adversarial strings). One behaviour per test, named for it. When fixing a bug, write the failing test first.
- Versions are pinned exactly. Add no dependency without asking. Change lockfiles only through `uv` and `npm`, never by hand.

### Rules from ADR 0012 (the review also checks these)

- No unbounded `while` loops.
- No regex on long or untrusted text without a length cap; prefer plain string operations or validation libraries.
- Length caps on the question (300 characters), on model output and on the Show more id list: at most 3 ids, each in the plain id format, otherwise a bad request.
- Every MCP and model call has a timeout equal to the smaller of its own limit and the time left before the request deadline. Retries are bounded and count against the deadline.
- Loop limits come from config (`MAX_ROUNDS`, `MAX_COMPOSE_RETURNS`), plus an explicit LangGraph step limit. No repeated identical tool call; only tools the MCP server lists.

## Architecture rules

- **Code owns facts, the model owns words** (ADR 0004). Title, date, credit, link and distances are copied by code from tool results by entry id. The model writes only the overview and the explanations, and the output is validated.
- **LangGraph is only the skeleton** (ADR 0002): nodes, edges and state. Node bodies are plain Python. LangChain chat-model wrappers appear only inside nodes. No LangChain agents, chains, retrievers or tool abstractions. Use the official MCP client library directly.
- **Stateless agent** (ADR 0003): each question stands alone, and the server keeps no state about earlier answers.
- **Show more fetches reserved entries by id** (ADR 0013, which replaced the query round trip of ADR 0003). The first archive answer shows up to 3 entries and returns `more_ids`, the ids of up to 6 reserved entries (ids only, no archive text). The browser keeps them. Show more sends the next ids, at most 3. The agent then skips `decide`, fetches those entries through the MCP lookup tool, and runs compose and validate as for any answer. In a Show more response `more_ids` is always empty. Incoming ids are untrusted input.
- **No database** (ADR 0006). The conversation lives in the browser (ADR 0010).
- **One API contract** (ADR 0011): request and response shapes are defined once as backend models; the OpenAPI file and the TypeScript types are generated from them. Never edit generated files by hand. The backend returns facts and words, never layouts; the browser draws the illustrations.
- The app hosts no image copies; images load from their NASA address.
- Infrastructure restrictions (private link, IAP, ingress) live in cloud configuration, never in application code.
- UI follows the screen specs in `docs/`. Where a spec and a design board screenshot differ, the spec wins. Layout maths for the illustrations are pure functions with unit tests.

## Repo hygiene (this repo is public)

- No secrets, keys or `.env` files. Secrets come from the host's secret store or GitHub secrets.
- No archive text, no copyrighted images, no company or interviewer names. Only NASA-credited material in screenshots and examples.
- Design board screenshots stay local and are gitignored.
- The audit log line per question contains no archive text.

## Do not touch

- Accepted ADRs and the architecture and UI specs in `docs/`. A changed decision becomes a new ADR that supersedes the old one, and only when I ask.
- `docs/progress.md` and `docs/ai-corrections-log.md`. I keep them.
- `.env`, `frontend/.npmrc`, and anything under `.github/` unless the step says so.
