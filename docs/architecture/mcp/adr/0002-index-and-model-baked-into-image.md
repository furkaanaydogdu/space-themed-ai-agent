# ADR 0002: Embedding model and index are baked into the MCP image at build time

- Status: Accepted
- Date: 2026-10-31
- Repo: mcp
- Related: [Index ADR 0001](../../index/adr/0001-private-index-repo-with-manifest-and-release.md), [App ADR 0008](../../app/adr/0008-registry-login-and-deploy-flow.md)

## Context
The archive search needs the embedding model weights and the vector index at runtime. Scale-to-zero means every cold start would otherwise download them. The index comes from a private repo, so the resulting image must stay private. The model name, chunk settings and library versions must match what built the index.

## Decision
- The MCP image is built in multiple stages. The build stage reads the pin file (one line naming an index release tag), downloads that release asset from the private index repo with a BuildKit build secret (`--mount=type=secret`, never an `ARG` or `ENV`, so nothing lands in a layer or in the image history), verifies its sha256, and downloads the model weights.
- A manifest check script compares the index manifest with the service's own config (model name, chunk parameters, library versions). A mismatch fails the build, so no image is produced.
- The final stage holds the service, the model weights and the index. It runs as a non-root user on `0.0.0.0:8080`, uses a slim pinned Python base, installs dependencies from the lock file with uv, uses CPU-only PyTorch, carries an OCI source label and is tagged with the commit.
- The same check runs again at service startup.
- The index is searched in-process (FAISS through LlamaIndex). Each instance holds its own copy in memory, which is small at this scale. A server-mode vector database or memory-mapped file would be documented in a future ADR, not built.
- The required CI image-build job runs this same Dockerfile, so a pin change that points to a mismatching index fails the pull request. There is no separate download or manifest job.
- The image is stored in a private registry (see App ADR 0008).

## Alternatives considered
- Download in the workflow and `COPY` the files in: rejected, the check would then need the credential in two places.
- Download at startup: rejected, slows every cold start and needs the credential at runtime.
- A persistent disk or bucket for the index: rejected, nothing is written at runtime, an immutable image is simpler.

## Consequences
- Each CI build downloads the index and model on a fresh runner (size not yet measured).
- A local image build needs the secret passed in; locally the service is normally run from Python.
- Image size and build time are not measured yet; measure with the real image.
- An invalid or missing credential makes the build fail with an authorization error.
