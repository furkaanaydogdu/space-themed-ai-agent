# ADR 0006: No database in version 1

- Status: Accepted
- Date: 2026-10
- Repo: app
- Related: [ADR 0003](0003-stateless-agent-each-question-alone.md), [ADR 0010](0010-conversation-held-in-the-browser.md)

## Context
There are no user accounts, no cross-session history and no data written by the product. The archive index is read-only and ships inside the MCP image.

## Decision
- The product has no database. The conversation lives in the browser, the index is baked into an immutable image, and logs go to the platform's logging.
- Services are stateless and scale to zero.

## Alternatives considered
- A managed database for conversations: rejected, no accounts and no need to persist beyond the tab.
- A persistent disk for the index: rejected, the index never changes at runtime.

## Consequences
- An instance shutdown loses nothing that matters.
- If accounts or persistent history ever return, a store is a new ADR.
