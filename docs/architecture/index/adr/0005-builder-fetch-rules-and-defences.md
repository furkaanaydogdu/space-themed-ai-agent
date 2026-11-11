# ADR 0005: Builder design: full rebuild, paged fetch, images only, fail loudly

- Status: Accepted
- Date: 2026-11-05
- Repo: index
- Related: [Index ADR 0001](0001-private-index-repo-with-manifest-and-release.md), [Index ADR 0003](0003-chunk-only-long-entries.md), [Index ADR 0004](0004-archive-source-nasa-science-endpoint.md)

## Context
The source (Index ADR 0004) has no uptime promise, no quota, and a response shape that real data does not always follow. Its failures can also be silent: the legacy endpoint answered every request with valid-looking placeholders, and only inspecting raw records revealed the cause. Two throwaway measurement scripts established the fetch approach below on two and ten years of data (the ten-year run returned 3,649 records for a 3,652-day span). Splitting failed windows in half had helped a little earlier, but could not fix bad data.

## Decision

**Scope**
- Every run rebuilds the whole window from scratch. There are no incremental builds. The window is today minus N years (N times 365.25 days), with N set in configuration (about two years for the demo). This also picks up entries that were edited after publishing, such as one that was published at 00:05 and modified at 15:40 US Eastern the same day.
- Only entries with `media_type` equal to `image` are indexed. In a two-year check that was 677 of 730 days, about 93%. Videos and embedded pages are left out, so a question about one of them finds no match.
- A local raw cache of fetched pages may be used while developing so re-runs do not hit the endpoint. CI always fetches fresh.

**Fetch**
- Page newest first with `per_page` and `page`. Collect records by date, which also removes duplicates. Stop when the oldest date on a page is at or before the cutoff.
- The page size is negotiated, not assumed. On page 1 try 100, then 50, 20, 10, keep the first size the server accepts and use it for the rest. A 400 or 404 on page 1 for every size means paging is unsupported and fails the build. One project reports a maximum of 25 per page, so the builder starts high and adapts.
- Other stop conditions: an empty page, a 400 or 404 on a later page (past the end), or a page with nothing new (a sign that the server ignores `page`).
- Every request is isolated: up to 3 attempts with waits of 3 s times the attempt number, a User-Agent header, a 0.5 s pause between requests, and a clear message on each failure. A 400 or 404 is not retried.
- After paging, list every day in the window without a record. Fetch each through the single-day route; a 404 there means NASA published nothing that day. The two-year check found only the not-yet-published current day. Days that still have no record are reported, not an error.

**Defences (any of these fails the build)**
- A record titled "NASA Science" (the symptom of a broken or legacy source).
- An image entry missing `hdurl` or `explanation`.
- A record that does not match the expected schema. Records are validated one by one against a schema and the failure names the field.
- Zero entries, or a date range that does not reach near today.

**Visibility**
- The build prints statistics: records fetched, counts per media type, entries indexed, entries skipped and why, days without a record, the date range reached, the token-length statistics from Index ADR 0003, and the number of placeholder titles (must be 0).
- The log keeps the first record of the first page, with long fields cut, so a change in the source's shape can be seen without re-running.
- The manifest records the entry count, chunk count and date range, so the validate script can check them (Index ADR 0001).
- A `--quick` mode makes two requests per step. It exists for smoke testing the script and was worth it in the measurement runs: it found a flaw in a test design before the full run.

**Validate (separate script, no shared code)**
- Repeats the placeholder check on the output: no entry titled "NASA Science".
- Checks every entry is an image and has an image address and an explanation.
- Expects the entry count to be close to 93% of the days in the window, not every day, with a tolerance, and a date range that ends near today.

## Alternatives considered
- Incremental builds with date-range parameters: rejected. Two years is about 730 records, a full fetch is a few dozen requests, and a full rebuild is the only way to pick up later edits. The parameters are also untested.
- One request per day for everything: rejected, hundreds of requests where paging needs a few dozen. The single-day route is kept only for gaps.
- Fixed page size and fixed retry-free requests: rejected, the real maximum page size is not confirmed and a transient error would otherwise break the monthly build.
- Include videos: rejected by decision. The index and the answer cards are built around still images.

## Consequences
- A change in the source's shape, or a placeholder response, stops the build with a clear message instead of publishing a bad index. The previously published release stays pinned, so the demo keeps working.
- The monthly build can fail for reasons outside our control. A failed run is visible in the repository and is re-run by hand.
- Open items:
  - Confirm the maximum page size.
  - Find out which 3 days had no record in the ten-year check.
  - Check how an interrupted or rate-limited run behaves; the endpoint states no quota.
