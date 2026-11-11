# ADR 0003: Split only long entries into overlapping chunks; keep one stored text per entry

- Status: Accepted
- Date: 2026-11-04 (written down; based on a token-length test of the embedding step)
- Repo: index
- Related: [Index ADR 0001](0001-private-index-repo-with-manifest-and-release.md), [Index ADR 0002](0002-multi-qa-minilm-embedding-model.md), [MCP ADR 0002](../../mcp/adr/0002-index-and-model-baked-into-image.md)

## Context
An embedding model reads a limited number of word pieces per input. `multi-qa-MiniLM-L6-cos-v1` accepts up to 512 and silently drops anything beyond that, but it was trained on passages of up to about 250 word pieces and its card warns that longer text may not work well. A long explanation therefore risks a vector that represents it poorly, and nothing in the pipeline would say so.

Measured on 30 real entries (three build runs of 10 randomly sampled entries, exact counts from the model's own tokenizer):

- Length: minimum 118, maximum 279, mean about 191 tokens.
- Two entries (about 7%) were at or above 256 tokens. Two more (about 13% together with the first two) were between 230 and 255.
- No sampled entry came near the 512 hard limit, so nothing was cut. The risk is a weaker vector for the longest entries, not lost text.

The entry text itself is always stored in full. Chunking only affects what is embedded and searched.

## Decision
- Entries that approach or pass the trained range (about 250 tokens) are split into chunks of about 200 tokens with an overlap of 30 to 40 tokens. Shorter entries stay whole.
- The splitter respects sentence boundaries.
- Each chunk is embedded separately and carries the date and title of its entry. The full, untruncated explanation is stored once per entry; chunks point to it.
- Chunk parameters are written to the manifest. Validate checks that no chunk is empty or oversized.
- Retrieval takes the top matches, merges chunks of the same entry into one result (by date), and returns the stored full explanation, never the chunk fragment. This merge happens in the MCP service.

## Alternatives considered
- Embed every entry whole and accept the loss: rejected, because roughly one entry in seven is near the trained range already and longer entries would degrade quietly.
- Raise the token limit of the model: rejected, because the model was not trained beyond about 250 word pieces, so a higher limit does not make longer inputs represent better.
- Chunk every entry: rejected, because it multiplies vectors and merge work for the majority that fit in one piece.
- Embed only the title and the start of the text: rejected, because it throws away the content visitors ask about.

## Consequences
- The index holds somewhat more vectors than entries; the exact count is in the manifest.
- Results need the merge-by-date step, and the "Show more" exclusion list works on entry ids, never chunk ids.
- The sample is small (30 entries). The share of long entries on the full archive is unknown until the first real build reports its token statistics; build should log them.
- The thresholds are settings, not code. If the model changes (Index ADR 0002), they are revisited together.
