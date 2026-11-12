# ADR 0013: Show more fetches reserved entries by id, not by repeating the query

- Status: Accepted
- Date: 2026-11-12
- Repo: app
- Supersedes: the Show more mechanism of [ADR 0003](0003-stateless-agent-each-question-alone.md) (the `show_more_query` round trip) and the matching request and response fields in [ADR 0011](0011-one-api-contract-with-generated-types.md)
- Related: [MCP ADR 0004](../../mcp/adr/0004-archive-search-and-lookup-by-id.md), [ADR 0010](0010-conversation-held-in-the-browser.md), [ADR 0012](0012-bounded-loops-deadline-and-cost-guards.md)

## Context
ADR 0003 made "Show more" work without server memory by sending the exact archive query back to the server, together with the ids of every entry already shown. The server repeated the search, excluded those ids, and relied on the same query giving the same ranking. It needed an "ask for one extra result" rule to know whether more matches existed. Chunks of the same entry (Index ADR 0003) added a further case: entries already shown could take up places in the repeated search.

A simpler way gives the same result. The first search already ranks the matches, so it can keep more entries than it shows, and later requests can fetch those entries directly by id.

## Decision
- The first archive search keeps more entries than it shows. By default the answer shows up to 3 and holds up to 6 more in reserve. Both numbers are configuration values. Chunks are merged and the relevance cut-off is applied once, in that search (MCP ADR 0004).
- The response field `show_more_query` is replaced by `more_ids`: the ordered ids of the reserved entries, ids only and no archive text. An empty list means no more entries and the Show more button is off.
- The browser keeps `more_ids` with the answer in `sessionStorage` (ADR 0010).
- Show more sends the next ids only, at most 3 per request. The browser removes them from its list when it sends them and turns the button off when the list is empty. The server holds no state about the reserve.
- The agent skips decide. Act fetches those entries by id through the MCP lookup tool, compose writes the explanations, and validate checks them, exactly as for a normal answer. Facts are copied by code from the lookup result; the model writes only the words. New entries come back in the same `entries` field. In a Show more response `more_ids` is always empty, because the server does not know the rest of the list.
- The incoming ids are untrusted input. A request with more than 3 ids, or an id that is not in the plain id format, is rejected as a bad request (ADR 0012, input caps).
- If some ids are no longer in the index, those entries are skipped. If none are found, the answer is a decline with reason `no_match` and the browser clears its list.
- Ids are entry ids, never chunk ids.

## Alternatives considered
- Repeat the search with the saved query and an exclusion list (ADR 0003): rejected, it needs the query round trip, a stable ranking, an extra result to detect more matches, and care with chunks.
- Keep the reserve on the server: rejected, the server holds no conversation state (ADR 0010).
- Send the whole reserve list with every Show more request and get the remainder back: rejected, a larger request with no benefit; the browser can trim its own list.

## Consequences
- Depth is fixed at the first search. A visitor can reach only as many extra entries as the reserve holds (6 by default, two presses). Raising it is a configuration change.
- The first response is slightly larger because of the id list. It is only ids.
- The saved browser state changes shape, so its schema version is increased and older saved states are discarded (ADR 0010).
- The generated API types change (ADR 0011). The audit log keeps its fields: a Show more is logged as call kind `show_more`, with the lookup tool call and the returned entry ids.
- Evals cover Show more as a lookup-and-compose path, with no search involved.
