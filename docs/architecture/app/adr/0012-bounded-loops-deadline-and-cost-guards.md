# ADR 0012: Bounded loops, a propagated deadline and layered runaway-cost guards

- Status: Accepted (residual risk recorded)
- Date: 2026-11-01
- Repo: app
- Related: [ADR 0002](0002-langgraph-skeleton-with-plain-python-nodes.md), [ADR 0004](0004-code-owns-facts-model-owns-words.md)

## Context
An agent with a loop, model calls and a pay-as-you-go cloud can run up cost when something hangs or spins. Cloud Run's request timeout returns a 504 and closes the connection, but it does not stop the container: the handler may keep running. So the platform timeout cannot be relied on for cost safety.

## Decision
- **Deadline:** one absolute deadline (about 90 s, config) is created when the request arrives and travels in the agent state. Every MCP and model call gets a timeout equal to the smaller of its own limit and the time remaining. Before each round, and before compose, a conditional edge checks the remaining time; if too little is left, the agent ends gracefully (compose from what was gathered, otherwise the agent-written timeout message with a static fallback). No time checks are scattered inside pure functions.
- **Loop limits:** `MAX_ROUNDS` (start 3), at most one compose return, no identical repeated call, only tools listed by MCP, schema-checked arguments, a token cap per question, and an explicit LangGraph step limit.
- **Per-call limits:** timeouts on every MCP call (and limits inside the MCP service on its own outside calls), timeouts on every model call, caps on output length and on any thinking budget, and bounded retries counted against the deadline.
- **Code rules** (for the project's review rules): no unbounded `while` loops; no regexes on long or untrusted text without a length cap, preferring plain string operations or validation libraries; length caps on the question, model output and the shown-ids list; tests with oversized and adversarial strings and with a fake tool and a fake model that never answer.
- **Infrastructure:** at most one instance on each service, kept small; a spend limit on the model provider's workspace; the `--ingress internal` setting as a kill switch for outside traffic; and Cloud Run's 120 s request timeout as a backstop only.

## Alternatives considered
- A watchdog thread that ends the process past a hard limit, and a server setting that restarts silent workers: rejected, disliked for restarting the container; the gunicorn timeout measures worker silence, not request duration, and was not confirmed to catch a blocked event loop.
- Relying on Cloud Run's timeout: rejected, see context.

## Consequences
- Residual risk: a never-yielding loop in our own code would burn CPU until the instance ends. Bounded by the single small instance, and listed in the risk log.
- Not yet verified: the model SDKs' per-request timeout and retry options; whether the model provider stops billing when a non-streamed request is dropped.
- Google budget alerts only notify; they do not stop spending.
