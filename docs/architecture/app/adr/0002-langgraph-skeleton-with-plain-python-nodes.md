# ADR 0002: LangGraph as the agent skeleton, with plain Python inside every node

- Status: Accepted
- Date: 2026-10
- Repo: app
- Related: [ADR 0003](0003-stateless-agent-each-question-alone.md), [ADR 0004](0004-code-owns-facts-model-owns-words.md), [ADR 0012](0012-bounded-loops-deadline-and-cost-guards.md)

## Context
The agent must call tools, possibly several times, then write and check an answer. We want a recognisable, inspectable structure without handing control to framework abstractions that hide behaviour and make evals harder.

## Decision
- LangGraph provides the skeleton: nodes, edges and state.
- Every node body is plain Python. Chat-model wrappers are used only inside nodes, so swapping the model provider for evals is a one-line change.
- No LangChain agents, chains, retrievers or tool abstractions. The official MCP client library is used directly (the LangChain MCP adapter package is archived and its successor was still in beta).
- LlamaIndex is used only in the index and MCP repos.
- Nodes: **decide** (small model: sees the question, the tool list and a short capability statement; returns tool calls, a decline, or done), **act** (code: runs calls in parallel with timeouts and schema checks), **compose** (mid-tier model: writes the overview and per-entry explanations, or a short note saying what is missing), **validate** (code), **finish** (code: writes the audit log line and returns the answer).
- Routes: decide, act, decide, and so on until done or the round cap; then compose, validate, finish. A compose note routes back to decide once. A decline with no tool calls goes straight to finish.
- The loop has a real purpose under this product: retrieval refinement (rephrase and retry when archive matches are weak or missing).
- State holds the question, round and return counters, decide messages, full tool results by source with status, trimmed text for the model, the writer note, the decline, the draft and the final answer.
- Per-node model names, caps and timeouts are config values.

## Alternatives considered
- Plain functions with no framework: simpler, but loses the graph structure that reviewers and evals benefit from.
- LangChain agent abstractions: rejected, less control and less visibility.

## Consequences
- The graph and its guards are the main thing to test deterministically (with fake tools and fake models).
- Loop guards and deadlines are defined in [ADR 0012](0012-bounded-loops-deadline-and-cost-guards.md).
