# ADR 0001: Three repositories and two deployed services

- Status: Accepted
- Date: 2026-10-17
- Repo: app (front door)
- Related: [Index ADR 0001](../../index/adr/0001-private-index-repo-with-manifest-and-release.md), [MCP ADR 0001](../../mcp/adr/0001-http-mcp-server-on-a-private-link.md), [main architecture document](../../space-agent-architecture.md)

## Context
The product has three kinds of work: the user-facing app with the agent, a set of data tools served over MCP, and a periodically rebuilt search index. They change at different speeds, have different pipelines and different access needs. Readers of the project mostly look at the README and the decision records first.

## Decision
- **App repo:** React frontend, Python API and agent, eval job, product docs, ADRs, a front-door README linking to the other repos, and the review rules. Deploys one service.
- **MCP repo:** the MCP server and its tools, the Dockerfile that bakes in the model and index, and the pin file naming the index release. Own CI, review and deployment. Deploys one private service.
- **Index repo:** build, validate and publish scripts. Deploys nothing and needs no cloud credentials.
- No shared schema package. The MCP server is reusable by other products, the index builder is an upstream data source, and the one real cross-repo contract (embedding model, chunk settings, library versions) is covered by the index manifest, a CI check on the pin change and a startup check.

## Alternatives considered
- One repo for everything: simpler, but the MCP server and the index would not read as reusable pieces and pipelines would mix.
- A microservice per data capability: rejected, no necessity.
- A fourth repo and a third service for the frontend: rejected, see [ADR 0009](0009-react-and-python-api-in-one-container.md).

## Consequences
- Three pipelines to maintain, but each is small.
- Cross-repo decisions are recorded in the app repo and linked from the others.
