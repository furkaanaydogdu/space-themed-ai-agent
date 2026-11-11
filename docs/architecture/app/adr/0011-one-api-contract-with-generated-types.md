# ADR 0011: One API contract definition, with generated frontend types

- Status: Accepted
- Date: 2026-11-01
- Repo: app
- Related: [ADR 0003](0003-stateless-agent-each-question-alone.md), [ADR 0009](0009-react-and-python-api-in-one-container.md), [MCP ADR 0003](../../mcp/adr/0003-tools-return-data-only.md)

## Context
The React page and the Python backend ship in one image but are written in two languages, often by AI tools on each side. Without a single source of truth they drift and quietly disagree.

## Decision
- The backend defines the request and response shapes once, as data models. The framework generates the OpenAPI file from them, and the frontend's TypeScript types are generated from that file. CI fails if the generated types are stale.
- **Calls under `/api`:** ask (question text), show-more (archive query plus all shown ids), warm (wakes the MCP service, called by the landing page), health.
- **One response shape for ask and show-more:** outcome (answered or declined); conversation text (the overview sentence, or the agent-written decline, or the overview plus a checked note for a mixed question); decline reason (out of scope, relies on an earlier answer, no match, timeout); `entries` (empty means no overlay: up to three archive entries plus one asteroid entry and one ISS entry); unavailable sources; and `show_more_query` (empty means the Show more button is off).
- **Entry types:** archive (id, title, date, credit line, link to the NASA entry, image source address, explanation; the app hosts no image copies), asteroid (the 7-day window and every asteroid with name, size range, closest approach and hazard flag, plus explanation), ISS (ten timepoints with position, current altitude and speed, day or night, snapshot moment, plus explanation).
- Show more returns its new archive entries in the same `entries` field. The browser appends them and derives the shown-ids list from the entries it holds.
- The backend returns facts and words, never layouts.
- **Errors** are separate from results. Declines and agent-written timeouts are normal successful responses. Real failures use codes: an expired sign-in (401 or opaque redirect), a platform cut (504), or a small error body with a code and a plain message. The browser treats all of them as "failed, put the question back".
- Browser calls are made with redirects handled manually so an expired sign-in can be told apart from being offline.

## Alternatives considered
- Hand-written types on both sides: rejected, drift.
- Returning layouts from the backend: rejected, the browser draws the illustrations from data.

## Consequences
- One generator tool and one CI step to maintain.
- A new deploy that changes a response shape is handled by the schema version on the saved state ([ADR 0010](0010-conversation-held-in-the-browser.md)).
