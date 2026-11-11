# ADR 0007: Access gate with Identity-Aware Proxy on the app service

- Status: Accepted
- Date: 2026-10-30 (verified in the deployment spike)
- Repo: app
- Related: [MCP ADR 0001](../../mcp/adr/0001-http-mcp-server-on-a-private-link.md), [ADR 0009](0009-react-and-python-api-in-one-container.md)

## Context
The demo should be live but only reachable by invited people. Because the gate is infrastructure, it should be a cloud setting rather than application code, so a host switch later does not touch the code.

## Decision
- Identity-Aware Proxy (IAP) is enabled directly on the app Cloud Run service, with no load balancer. A project without an organization needs a custom OAuth client saved in the IAP settings.
- Only allow-listed Google accounts get in. The spike showed a refused account is blocked, and that both service address forms answer with a redirect to Google sign-in.
- The page and `/api` sit behind the same gate on one address, so the browser's calls carry the IAP cookie by themselves (no cross-origin settings).
- Expired or missing sign-in: the app detects an unauthenticated response (a 401 or an opaque redirect), reloads the page, the visitor passes the quick Google sign-in, and the browser restores the conversation (see [ADR 0010](0010-conversation-held-in-the-browser.md)). What an expired but present session returns is unconfirmed; both forms are handled.
- The IAP session follows the visitor's Google login session. No shorter re-authentication setting is configured.

## Alternatives considered
- An access code in application code: kept only as a replaceable fallback.
- Cloudflare Access: believed to need a domain and an origin lock-down; not verified.

## Consequences
- The gate and the private link are one-time cloud settings kept in a runbook; the pipeline only swaps the image.
- Real session lifetime is not published by Google and is not needed for the design.
