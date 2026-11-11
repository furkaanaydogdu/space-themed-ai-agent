# ADR 0008: Artifact Registry, Workload Identity Federation and deploy-on-merge

- Status: Accepted
- Date: 2026-10-31
- Repo: app (applies to the app and MCP repos)
- Related: [MCP ADR 0002](../../mcp/adr/0002-index-and-model-baked-into-image.md), [ADR 0007](0007-access-gate-with-cloud-run-iap.md)

## Context
Images must be built, stored and deployed without long-lived cloud keys, and the MCP image contains data that must stay private. Cloud Run cannot pull a private image from GitHub's registry directly.

## Decision
- **Build:** GitHub Actions on a GitHub-hosted runner builds each image and tags it with the commit.
- **Registry:** one private Artifact Registry repository in europe-west4 (same region as Cloud Run, so pulls are free) holds both images under different names. A cleanup policy keeps the newest 5 versions per image (dry run first; changes take about a day to apply).
- **Login:** Workload Identity Federation with GitHub OIDC. For each run GitHub issues a short-lived signed token naming the repo and branch. Google trusts only tokens from this project's repos on `main` (a one-time pool and provider with an attribute condition) and exchanges them for temporary credentials of a small service account. There is one service account per repo, allowed to deploy only its own Cloud Run service, plus write access to the one registry repository.
- **Deploy:** the deploy job runs only on a merge or push to `main`, never on pull requests. The pipeline only swaps the image of the existing service. Ingress, VPC, IAP and DNS settings remain one-time cloud settings in a runbook. On a host switch only the deploy step changes.
- **Rollback:** redeploy an earlier commit tag.
- **CI on pull requests:** lint, types, deterministic tests (no model calls), secret scan and the image build. Evals are not part of CI.
- **Review:** a separate review-only workflow (anthropics/claude-code-action) with read-only code access, run once after CI is green. It uses its own workspace and key with a spend limit, turn and time limits, and reads review rules from a separate file. Comments are resolved through "require conversation resolution" (a solo developer cannot approve their own pull request).
- **Commits:** the developer commits; the review workflow never commits.

## Alternatives considered
- GitHub's container registry: free, but the MCP image must be private and Cloud Run cannot pull private images from it directly.
- A stored service-account key as a secret: long-lived and leaks work from anywhere.
- Cloud Build watching the repo: ties the build to Google, adds cost, goes against the host-switch goal.

## Consequences
- Exact deploy command, role names and the cleanup behaviour are verified when the pipelines are written (the cleanup must keep tags used by running revisions; Cloud Run keeps its own copy while a revision uses it).
- One environment only.
