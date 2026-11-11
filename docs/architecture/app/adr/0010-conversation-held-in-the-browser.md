# ADR 0010: The conversation is held in the browser (sessionStorage), not on the server

- Status: Accepted
- Date: 2026-11-01
- Repo: app
- Related: [ADR 0003](0003-stateless-agent-each-question-alone.md), [ADR 0006](0006-no-database.md), [ADR 0007](0007-access-gate-with-cloud-run-iap.md), [ADR 0009](0009-react-and-python-api-in-one-container.md)

## Context
A refresh or a re-sign-in reloads the page and discards everything in memory. The server forgets everything when an instance shuts down. There are no accounts or cookies for conversation loading, and the product requires only that a conversation survive a refresh within a tab.

## Decision
- The page saves the conversation in `sessionStorage` on every change and restores it on load. No id in the address, no cookies, no server-side store.
- **Saved:** the conversation entries (each question with its answer as structured data, so illustrations are redrawn and history entries reopen the same way), the draft in the input box, and which answer view is open. Only what the answer displays is saved, never raw archive chunks or index data.
- **Not saved:** scroll position and a pinned hover panel. A question still unanswered at reload comes back in the input for a re-send.
- The same logic serves a plain refresh and the re-sign-in after an expired IAP session.
- The saved state carries a schema version. If it does not match the running build, the page discards it and starts fresh.
- Per tab: two tabs hold two conversations; closing the tab ends the conversation; a copied link opens a fresh one. If browser storage is blocked, the page falls back to memory only. Size is capped (storage limit is about 5 MB; figure unverified).
- `sessionStorage` is used, not `localStorage`, so nothing persists after the tab closes.

## Alternatives considered
- A conversation id in the address with server memory (the Google AI Mode pattern): worked for Streamlit, but needs server state that an idle shutdown loses.
- Cookie plus address id: rejected, conversation loading is an accounts job.
- Persistent `localStorage`: rejected, would keep conversation data after the tab closes.

## Consequences
- The stored copy lives only on the visitor's device for the life of the tab and holds only what the answer already displayed.
- The server needs no expiry timer or memory cap; the "one instance only" rule stays only as a cost guard.
