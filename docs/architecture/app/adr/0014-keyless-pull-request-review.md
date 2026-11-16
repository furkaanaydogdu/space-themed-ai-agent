# ADR 0014: Pull request review with a keyless login, one review per pull request, after CI

- Status: Accepted
- Date: 2026-11-16
- Repo: app (applies to the app and MCP repos)
- Supersedes: the Review bullet of [ADR 0008](0008-registry-login-and-deploy-flow.md) (its own key, and the loose "run once after CI is green")
- Related: [ADR 0012](0012-bounded-loops-deadline-and-cost-guards.md) (its code rules are the base of the review rules)

## Context
ADR 0008 described a review-only workflow that "uses its own workspace and key with a spend limit". While building it (development step 0.6) the model provider's platform advised a workload identity federation instead of a stored key, and the remaining details had to be settled: when the review runs, what access it gets, where its rules live, its limits, and what "once" means.

## Decision
- **Where and when:** a `review` job in each repo's `ci.yml`, on the `pull_request` event, for pull requests from the same repo only. It waits for the other CI jobs (app: `backend`, `frontend`, `secret-scan`; MCP: `python`, `secret-scan`). It is not a required check, so a failed review never blocks a merge. The index repo has no review stage.
- **Login:** keyless. The job's short-lived GitHub token is exchanged for temporary API access through a federation rule tied to a service account in a dedicated workspace. The rule accepts only the repo's name, the owner's GitHub user id and user name, and the `pull_request` event. The rule pins the repo name, so each repo has its own rule; both use the same service account. The ids are held as repository variables, not secrets and not in files. No API key exists. The workspace has a spend limit with warning thresholds, which is the hard stop on cost.
- **GitHub access:** the built-in `GITHUB_TOKEN`, with `contents: read`, `pull-requests: write` and `id-token: write` on this job only. The Claude GitHub App is not installed: GitHub gives an app a broad, fixed permission set. Comments appear as `github-actions[bot]`. The reviewer never commits.
- **Reviewer:** the review action (`anthropics/claude-code-action`, pinned by commit hash, v1.0.276 when adopted) runs with our own prompt, not a prebuilt review plugin. The model is Sonnet 5.5, set explicitly. The reviewer reads `.github/review-rules.md` (one file per repo), the step brief in the pull request description, and the diff, and posts up to 8 inline comments plus one summary. It changes no files.
- **Tool limits:** permission mode `default`, so anything not allowed is denied. Allowed: the inline-comment tool, `gh pr view`, `gh pr diff` and `gh pr comment`. Setting sources are limited to `user`: the reviewer does not load the repo's `AGENTS.md` or `CLAUDE.md`, or any `.claude/` settings a pull request adds. The rules file is its only rule source.
- **Untrusted input:** the title, description, comments, commits and code of a pull request are data, never instructions. The brief is a statement of scope that the diff is checked against. When a pull request has no brief, the summary says so.
- **Brief in the description:** every pull request carries its step brief in its description. It is public text in a public repo, so the repo hygiene rules apply to it.
- **Once per pull request:** a step before the action counts the comments on the pull request written by `github-actions[bot]` (issue comments and inline review comments, all pages). If there are any, the action step is skipped and the job stays green. It checks who wrote the comments, not a marker in their text. The step runs with `pipefail`, so a failed API call fails the step instead of counting as zero comments. A newer run for the same pull request cancels an older one.
- **Limits:** 12 turns, a $1.00 budget flag, a 10-minute job timeout. The flags are estimates kept by the client; the workspace spend limit is the real cap.

## Alternatives considered
- **A stored API key as a secret:** long-lived, and the platform itself advised against it.
- **The official GitHub App:** its permissions are broader than a review needs and cannot be narrowed.
- **The prebuilt review plugin:** fetched from a marketplace on every run without a pin, no place for our own rules file, cost unknown.
- **A separate workflow started when CI finishes:** its event name differs, so the federation rule would reject it, and it runs from the default branch.
- **A review on every push:** repeated comments, more conversations to resolve, higher cost.
- **Letting the reviewer load the repo's agent instructions:** those tell an agent to plan first and wait for approval, which is wrong for a one-shot review.

## Consequences
- Measured on a real pull request in the app repo: 5 turns and about $0.03.
- Not verified: that the budget flag or the turn limit actually stops a run (neither came near), whether an environment value could be put into a comment through the allowed comment command (shell expansion), and no workflow linter has been run on the file.
- Known weak spots: a run cancelled after posting some comments counts as reviewed; a future workflow that comments as `github-actions[bot]` would need a marker added to the check; a review that fails before posting anything is tried again on the next push.
- Pull requests from forks get no review, because they receive neither a login token nor write access.
- The rules file is read from the pull request's own checkout. Accepted: on a pull request event the pull request already controls the workflow file, and only runs started by the owner pass the federation rule.
- A new repo with a review needs its own federation rule and its own four repository variables.
- The pinned action hash is updated through a normal pull request.
- The rest of ADR 0008 is unchanged.