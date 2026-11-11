# ADR 0001: A separate, private index repo that publishes a validated index as a release

- Status: Accepted
- Date: 2026-10 (privacy constraint added 2026-10-31)
- Repo: index
- Related: [Index ADR 0002](0002-multi-qa-minilm-embedding-model.md), [Index ADR 0003](0003-chunk-only-long-entries.md), [Index ADR 0004](0004-archive-source-nasa-science-endpoint.md), [Index ADR 0005](0005-builder-fetch-rules-and-defences.md), [MCP ADR 0002](../../mcp/adr/0002-index-and-model-baked-into-image.md), [main architecture document](../../space-agent-architecture.md)

## Context
The archive search needs a vector index built from the APOD archive (about two years of entries). Building it takes time and should not run on every deploy. The index is kept in a private place. The embedding model, chunk settings and library versions must match between the builder and the search service, otherwise search silently degrades.

## Decision
- The index is built in its own repo, separate from the service that uses it. This repo holds the build script, the validate script and the publish step. It deploys nothing and needs no cloud credentials.
- The repo is private.
- GitHub Actions builds it on a manual trigger, a monthly schedule, or a push that touches pipeline code.
- Build: fetch the archive from the NASA Science endpoint and keep image entries only ([ADR 0004](0004-archive-source-nasa-science-endpoint.md), [ADR 0005](0005-builder-fetch-rules-and-defences.md)), split long entries into chunks of about 200 tokens with a small overlap, embed them with `multi-qa-MiniLM-L6-cos-v1`, write the index plus a manifest.
- The manifest records model name, chunk parameters, date range, entry and chunk counts, commit, sha256 of the index, and library versions (the persisted format of the index library can change between versions).
- Validate is a separate script that reads only the output folder and shares no code with the builder. It checks that the entry count and date range are plausible, that no placeholder entries slipped in, that no chunk is empty or oversized, that vector count equals chunk count with no zero or NaN vectors, that a few smoke searches return a known entry, and that the manifest is complete. It catches gross breakage, not subtle quality problems (evals do that).
- Publish is a single release step (`index-<date>`) that runs only if validate exits 0.
- The service repo pins the index by release tag in a one-line file. Publishing is automatic; moving the pin is a manual pull request.

## Alternatives considered
- Build the index inside the service's image build: slow builds, a fetch that can fail for reasons outside the service pipeline, no independent validation.
- Public index repo: rejected, the index stays private.
- Share code between builder and validator: rejected, a shared bug would pass its own check.

## Consequences
- Two independent checks protect the service: the validate gate here, and the manifest check at the service's image build and startup.
- The service build needs authenticated access to this private repo (see MCP ADR 0002).
- The archive source needs no key, so this repo holds no NASA secret. Source failures stop the build (ADR 0005).
- Automating the pin pull request later runs into GitHub's rule that pull requests created with the default workflow token do not trigger CI; deferred.
