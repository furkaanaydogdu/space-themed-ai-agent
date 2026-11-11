# ADR 0009: React frontend and Python API in one container (supersedes the Streamlit plan)

- Status: Accepted. Supersedes the earlier choice of Streamlit.
- Date: 2026-10-31
- Repo: app
- Related: [ADR 0007](0007-access-gate-with-cloud-run-iap.md), [ADR 0010](0010-conversation-held-in-the-browser.md), [ADR 0011](0011-one-api-contract-with-generated-types.md)

## Context
The first plan used Streamlit for the interface. An illustration spike showed Streamlit's HTML element removes every `<svg>`, and the workaround (a static image plus positioned elements) could not pin or close detail panels, clipped panels on phones and leaked styles. Streamlit also keeps a WebSocket open per tab: a refresh creates a new session (state lost), and an abandoned open tab kept an instance busy and billed; the 15-minute idle period of Cloud Run is not configurable. Cold start to a usable page was about 12.55 s.

## Decision
- The frontend is React (Vite static build, TypeScript) in `frontend/`. The API and agent are Python (FastAPI) in `backend/`. Both are in the app repo.
- One multi-stage Dockerfile: a Node stage builds the static files, a Python stage copies only the finished build next to the API. No Node at runtime.
- FastAPI answers `/api/...`, serves `/assets/...` from the build, and returns `index.html` for every other path so client-side routes survive a reload (routes declared in that order).
- One Cloud Run service behind one IAP gate serves the page and the API from the same address. It reaches the private MCP service over Direct VPC egress as before. The repo count stays at three and the service count at two.
- The illustrations are drawn in the browser from raw data (a TypeScript port of the approved asteroid demo, with the layout maths as pure, unit-tested functions). The answer overlay is an ordinary React view.
- Local development uses the Vite dev server with a proxy to the API; IAP is tested only in the cloud.

## Alternatives considered
- Staying with Streamlit and adding a component for the illustrations: keeps the WebSocket, refresh and billing issues.
- A separate frontend repo and service: adds an image, a pipeline, cross-origin settings and IAP cookie problems for no necessity.
- Other server-driven UI frameworks (NiceGUI, Reflex): not verified, keep long-lived connections.

## Consequences
- Verified in the React spike: a slow request held for 10, 60 and 180 s returned one answer; a short stream arrived unbuffered; the private MCP link worked; cold start to a usable page was about 3 s or less; an idle instance shut down with the tab still open; the abandoned-tab billing problem did not appear (to be confirmed with the next billing report).
- Cost: two languages, a JavaScript toolchain and tests, more code to review.
- The ISS illustration still needs its own spec.
