# ADR 0002: Embed the archive with `multi-qa-MiniLM-L6-cos-v1`

- Status: Accepted
- Date: 2026-11-04 (written down; the choice was made while the index pipeline was designed)
- Repo: index
- Related: [Index ADR 0001](0001-private-index-repo-with-manifest-and-release.md), [Index ADR 0003](0003-chunk-only-long-entries.md), [MCP ADR 0002](../../mcp/adr/0002-index-and-model-baked-into-image.md)

## Context
Archive search turns a visitor's short question into a vector and looks for the closest entry explanations. The same model must embed the entries (here, at build time) and the questions (in the MCP service, at query time), so the choice is shared by two repos and is recorded in the manifest.

The shape of the task is asymmetric: a short natural-language question in, a longer explanation passage out. Two small models from the same family (6 layers, 384-dimension vectors, CPU friendly) were the candidates:

- `all-MiniLM-L6-v2` is the common default. It is trained for general sentence-to-sentence similarity, that is, "are these two sentences alike".
- `multi-qa-MiniLM-L6-cos-v1` is trained on about 215 million question-answer pairs for semantic search, that is, "which passage answers this question". Its card describes it as a model that encodes queries and text paragraphs into one vector space.

## Decision
- Use `multi-qa-MiniLM-L6-cos-v1` for both entries and questions.
- No query or passage prefix is needed at encode time.
- Its vectors are normalized, so dot product and cosine similarity give the same ranking.
- The model name is written to the manifest and compared with the MCP service's own configuration at image build and at startup (see MCP ADR 0002).

## Alternatives considered
- `all-MiniLM-L6-v2`: rejected as the default choice, because its training target (symmetric sentence similarity) fits our query-to-passage shape less well.
- Larger embedding models or a hosted embedding service: not evaluated for v1. A larger local model would slow the build and enlarge the image, and a hosted one would add a runtime dependency and a cost line to every question. The small model keeps the service CPU-only and the index build cheap.

## Consequences
- The ranking advantage over `all-MiniLM-L6-v2` is expected from how each model was trained; it has not been measured on this archive. If retrieval quality looks weak, the on-demand evals are the place to compare models, and this ADR gets a successor.
- The model was trained on passages of up to about 250 word pieces, and its card says it may not work well on longer text. This drives how long entries are handled (Index ADR 0003).
- Changing the model changes every vector. It means a full index rebuild, a new release, a new manifest, and a pin change in the MCP repo; the manifest check refuses a mismatched pair.
- The model weights are public and are downloaded when the image is built, not at runtime.
