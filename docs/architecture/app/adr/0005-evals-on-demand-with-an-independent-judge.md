# ADR 0005: Evals run on demand, scored by code plus a judge model from the other provider

- Status: Accepted (storage and display of results still open)
- Date: 2026-10
- Repo: app
- Related: [ADR 0004](0004-code-owns-facts-model-owns-words.md)

## Context
Model behaviour is non-deterministic and costs money, so it cannot be a normal CI gate. We still need evidence that answers stay grounded and that out-of-scope questions are declined properly.

## Decision
- A fixed question set (the five groups of the test plan plus adversarial ones such as tricky trivia and "ignore the rules") runs through the real agent code on demand, as a command-line job in the app repo, never from a web request and not in CI.
- Each result is scored automatically: code checks (outcome type, overlay or decline, entry counts, facts match the source through the validator's extractor, decline guard) and a judge model from the other provider (does a claim go beyond the data, does a decline avoid answering, are the required elements present).
- Results are rates, not exact-text assertions.
- The same set compares models per node (a config swap), round caps and prompt versions: accuracy, latency, cost per question and flagged hallucinations, side by side.
- Evals are not the same as monitoring: evals use a fixed set offline; monitoring uses the audit log of real usage.
- Per question the audit log writes one structured line (identity, outcome, process, tool calls, models and tokens, totals, returned entry ids only, never archive text).

## Alternatives considered
- Evals in CI: rejected, cost and non-determinism.
- Same-provider judge: rejected, weaker independence.

## Consequences
- Open: where results are stored without a database, how the admin view is shown and what protects it. No archive text may appear in anything public.
- Evals do not replace manual testing (illustration layout, usability sessions).
