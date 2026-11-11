# ADR 0001: A real HTTP MCP server reached over a private network link

- Status: Accepted
- Date: 2026-10 (verified in the deployment spike, 2026-10-29/30)
- Repo: mcp
- Related: [App ADR 0007](../../app/adr/0007-access-gate-with-cloud-run-iap.md), [main architecture document](../../space-agent-architecture.md)

## Context
The agent reaches its data through MCP tools: archive search, near-Earth asteroids and ISS position. The tools need to be a real, separate service (the project demonstrates MCP tool-calling), but they must not be reachable from the internet. We want that restriction to live in cloud configuration, not in application code, so that moving to another host later does not change the code.

## Decision
- The MCP server speaks Streamable HTTP and is deployed as its own Cloud Run service. The server code is transport-agnostic.
- Privacy comes from the network, not from tokens: the service accepts only internal traffic (`--ingress internal`), is allowed unauthenticated on that private path, and has no login of its own.
- The app service reaches it through Direct VPC egress limited to private ranges, Private Google Access on the subnet, and a private Cloud DNS zone for `run.app.` that points the service hostname at Google's private-access addresses (199.36.153.8 to .11).
- Each question opens its own MCP connection (no long-lived connection manager, no background thread). The tools needed for one question run in parallel over it.
- The app calls a warm-up endpoint on the landing page so the MCP service wakes while the visitor reads.
- The MCP Python SDK is pinned to an exact version (2.3.0 in the spike). The SDK's host-header check is not active when the server binds `0.0.0.0`, so nothing in the code is relied on for privacy.

## Alternatives considered
- A child process (stdio) inside the app: rejected, a real HTTP server is the intent.
- A separate microservice per capability: rejected, no necessity.
- Service-to-service identity tokens (IAM invoker plus bearer token): kept as a fallback only, in case the network approach fails on another host.

## Consequences
- Verified in the spike: the app reached the private service; a request from the public internet was refused.
- Cold start of this service was about 4.3 s in the spike, which is why the warm-up call exists.
- A host switch means recreating the equivalent settings (private network, private DNS, gate), not changing code. The settings are kept in a runbook.
- Details of the private DNS zone differ between Google's documentation pages; the spike's working form is the one to follow.
