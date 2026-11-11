# ADR 0004: Read the archive from the NASA Science `apod-basic` endpoint, not the legacy API

- Status: Accepted
- Date: 2026-11-05
- Repo: index
- Related: [Index ADR 0001](0001-private-index-repo-with-manifest-and-release.md), [Index ADR 0005](0005-builder-fetch-rules-and-defences.md), [main architecture document](../../space-agent-architecture.md)

## Context
In late September 2026 the Astronomy Picture of the Day moved to science.nasa.gov. The old endpoint (`api.nasa.gov/planetary/apod`) still answers, but for every date it returns a placeholder: the title "NASA Science", the NASA logo as the image, and a generic explanation. It is due to be archived on 2026-12-01. A build that reads it would produce a valid-looking index full of identical placeholder entries.

The first design assumed the old API: an API key, and a date-range query. Both assumptions are out of date.

The facts below come from real responses inspected on 2026-10-27 and 2026-10-28 and from NASA's published guide for the new endpoint. The guide and third-party reports do not always agree with real responses, so the builder checks what it receives (see Index ADR 0005).

## Decision
- The source is `https://science.nasa.gov/wp-json/wp/v2/apod-basic`. No API key is needed, so the index repo holds no NASA secret.
- The builder reads a list newest first with `per_page` and `page`, and a single day with `/YYMMDD`. A day with no entry returns 404.
- The builder does not use `date_from` and `date_to` (never tested, and not needed, see Index ADR 0005). It does not use `?date=` (reported as silently ignored, which returns the latest entries instead of an error), `count`, `thumbs` or `hd`.
- New entries appear at about 00:05 US Eastern on their date. Entries can be edited after publishing.

**Record to entry.** The builder keeps only these fields and drops the rest while reading, including the full page HTML (`basic_html`), which makes records heavy.

| Record field | Becomes |
| --- | --- |
| `date`, `title` | as is |
| `media_type` | used to filter; values seen are `image`, `video`, `iframe`, and occasionally none |
| `hdurl` | the image address, stored without its query string (see below) |
| `permalink` | the link to the NASA entry (`url` is only the article page and is ignored) |
| `explanation` | cleaned text, see below |
| `credit` | cleaned text, see below |
| `alt` | image alt text |

**Cleaning.**
- Explanation: unwrap links and keep their text, remove the leading "Explanation:" label, remove the trailing "Tomorrow's picture:" teaser, decode HTML entities, collapse whitespace.
- Credit: strip tags and keep the text only. Link targets are dropped on purpose, because some contain obfuscated email addresses that must not be stored or shown.

**Image address.** `hdurl` carries a query string such as `?w=4144&h=2822&fit=clip&crop=faces%2Cfocalpoint`. The index stores the address without the query string, plus the original width and height read from `w` and `h` when they are present (in the three records seen so far they equal the original pixel size). Width and height give the aspect ratio without downloading the image. Resized variants are not stored; the address of a resized image is built where it is shown.

A manual test on 2026-11-05 confirmed that changing the query changes the size of the returned image. Still to check before the app relies on it: whether `w` alone keeps the aspect ratio, whether the service enlarges beyond the original, and which `fit` values never crop. The `crop=faces,focalpoint` part of the original address shows the service can crop, and the layout requires uncropped images, so `fit=clip` is the only candidate so far.

## Alternatives considered
- The legacy `api.nasa.gov` endpoint: rejected. It returns placeholders and is being archived.
- Date-range requests on the new endpoint: not used, see above.

## Consequences
- No NASA secret in the index repo, one less thing to rotate or leak.
- The endpoint has no stated uptime promise or quota, and the response shape is not guaranteed. The builder fails loudly on anything unexpected (Index ADR 0005); the previous release stays pinned until a later build succeeds.
- Documents or notes that name the legacy endpoint or an APOD API key are out of date.
- Other NASA services used by the MCP service (near-Earth objects) are separate from this decision and are not covered by it.
