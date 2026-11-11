# ADR 0003: MCP tools return data only; the app owns presentation and wording

- Status: Accepted
- Date: 2026-10
- Repo: mcp
- Related: [App ADR 0004](../../app/adr/0004-code-owns-facts-model-owns-words.md), [App ADR 0011](../../app/adr/0011-one-api-contract-with-generated-types.md)

## Context
The MCP server is meant to be reusable by other products, and the agent must be able to trust every fact it shows. If tools returned prose or layouts, the facts and the wording would mix and could not be checked.

## Decision
- Tools return structured data only: archive entries (id, title, date, credit, source link, image address, text), asteroid approach data for the 7-day window, and ISS positions (the current point plus the next 90 minutes in 10 timepoints).
- Every tool publishes an output schema, which the app can read through the tool listing.
- The app does not share a schema package with this repo. It keeps its own small models of what it expects from each tool and validates results against them. A schema failure becomes a per-source "unavailable" in the answer.
- Archive search accepts an exclusion list of entry ids so that "Show more" returns the next best unseen entries. For the same query the ranking is deterministic.
- The archive tool asks for one result beyond the requested number and uses a relevance cut-off to tell the app whether more matches exist. The cut-off is still to be specified when the tool is designed.
- An entry lookup tool is added only if follow-up questions ever return.
- Outside calls (NASA services, ISS source) have timeouts, and the service enforces its own limits on them.

## Alternatives considered
- Tools that return ready-made answer text: rejected, facts could no longer be checked against the source.
- A shared schemas package between repos: rejected, not worth it for a demo; the manifest check covers the one real cross-repo contract (the index).

## Consequences
- The ISS source is wheretheiss.at; its limit on timepoints per request and its rate limit are to be verified at design time.
- Result fields such as the error flag follow the pinned SDK version and are re-checked when the SDK is upgraded.
