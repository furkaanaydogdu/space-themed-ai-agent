# ADR 0003: A stateless agent that answers each question on its own

- Status: Accepted; the Show more mechanism is superseded by [ADR 0013](0013-show-more-by-reserved-ids.md)
- Date: 2026-10 (Show more round trip refined 2026-11-01)
- Repo: app
- Related: [ADR 0010](0010-conversation-held-in-the-browser.md), [ADR 0011](0011-one-api-contract-with-generated-types.md)

## Context
Follow-up questions ("tell me more about that one") caused the most ambiguity for the least value and would need multi-turn evals. The product requirements therefore state that every question is answered on its own, with the one exception of the "Show more" button on archive results.

## Decision
- The agent sees only the latest question. Two entry points exist: `ask(question)` and `show_more(query, exclude_ids)`.
- `show_more` skips the decide step: search, compose, validate.
- A question that cannot be understood without an earlier answer receives a plain explanation and a pointer to the earlier answer's history entry. The agent never guesses and never asks a clarifying question.
- "Show more" works without server memory. The answer carries `show_more_query`, the exact archive query the agent used (possibly a rephrase). Empty means no more matches. The browser sends it back unchanged with the ids of all entries it holds. The same query gives the same ranking, so the search returns the next best unseen entries; a fresh rephrase could skip or repeat entries.
- An answer's archive part comes from one final query; only that query continues with "Show more".
- The code keeps a dormant slot for history in the decide state and an optional context argument on `ask()`, so follow-ups can return later without a redesign.

## Alternatives considered
- Chat history passed on every request: rejected for this version, see above.
- Server-side conversation memory: rejected, see [ADR 0010](0010-conversation-held-in-the-browser.md).

## Consequences
- The server holds no conversation state, so an idle shutdown loses nothing.
- The query sent back by the browser is untrusted input: length-capped and treated as plain search text.
