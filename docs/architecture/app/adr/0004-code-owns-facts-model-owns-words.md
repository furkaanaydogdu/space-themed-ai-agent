# ADR 0004: Code owns the facts, the model owns the words

- Status: Accepted
- Date: 2026-10
- Repo: app
- Related: [MCP ADR 0003](../../mcp/adr/0003-tools-return-data-only.md), [ADR 0005](0005-evals-on-demand-with-an-independent-judge.md)

## Context
Answers must be accurate and grounded in the three data sources, never opinion or general knowledge. A model that writes everything can invent a date, a distance or a safety claim.

## Decision
- The answer is an overview sentence plus one explanation per entry, written by the model. Titles, dates, credits, links, distances and other facts are copied by code from tool results and merged by entry id.
- **Runtime validation, three levels.** (1) Structure and ids: every id exists in stored results, every shown entry has an explanation, no extras, length caps. (2) Facts inside prose: numbers, dates and capitalised names are extracted by pattern and must appear in that entry's source data, with tolerance for rounding and units. (3) Domain rules: for example, words like "dangerous" or "will hit" require NASA's hazardous flag, and an impact is never claimed.
- **Failure policy:** retry compose once with the failure reason; if it still fails, show code-built cards without model text plus a plain note.
- **Declines are written by the agent** in the same call as decide, so the product feels like talking to an agent. A runtime guard caps the message at about three sentences and rejects numbers, dates or capitalised names that do not come from the question or the capability statement. A fixed message per reason is the fallback (also used if the model call fails or times out).
- A mixed question (part answerable, part not) returns tool calls and a decline note together: the conversation shows the overview plus the checked note, and the overlay opens for the answerable part only.
- Similarity or judge-model checks (level 4) are part of the eval layer only.

## Alternatives considered
- A static refusal message: reliable but lifeless; replaced by guarded agent-written declines.
- Letting the model produce all fields: rejected, nothing could be verified.

## Consequences
- The guard cannot catch prose that leaks an answer without numbers or names; the evals carry that guarantee.
- Validation patterns run on untrusted text, so they follow the code rules in [ADR 0012](0012-bounded-loops-deadline-and-cost-guards.md).
