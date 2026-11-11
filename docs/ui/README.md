# UI specs — Discover the Cosmos

Written Nov 3 2026, from the UI design work with Furkan. These specs describe **what users see and how they interact**. They contain no architecture. They are written so a developer can build the screens without having been part of the design work.

How to read them: the visual truth is the design canvas (a private design file, boards named below). Where a board and a spec disagree, **the spec wins**, and the disagreement is listed in the spec's board-status note. Screenshots of the boards will be saved by Furkan into the matching folder.

**Wording:** every fixed text (system messages, refusals and their backups, character limit, "can't save" notice, empty asteroid week) is defined in `docs/business/static-texts.md`, which is the source of truth. The UI specs say where and how those texts appear and quote them for convenience; if a quote differs, the static-texts doc wins.

Marks used in the specs:
- **Decided** — Furkan decided or approved it.
- **Proposed** — my suggestion, not yet approved (none at the moment; "Try again" on failed pictures, the long-wait thinking text, the layer/Back-button/starting-over rules, the marked failed bubble and its "Not answered" label, the 3-second sign-in reload, the character counter and the mixed-answer order were approved Nov 3 2026).
- **Default** — not discussed; a sensible default so the build is not blocked. Confirm before relying on it.
- **Open** — not decided yet. Do not guess it in code.

## Folders

| Folder | Spec | Boards (design canvas) |
|---|---|---|
| `00-shared/` | `ui-conventions.md` — colours, type, components, rules that apply to every screen (incl. section 8: layers, auto-open and the Back button) | — |
| `01-landing/` | `ui-spec.md` | "Landing — desktop" (Main), "Landing — phone" (Mobile); these two do not show the character counter row |
| `02-conversation/` | `ui-spec.md` | "Conversation — desktop/phone", "Conversation — mixed answer, desktop/phone", "Conversation — after a reload, archive thumbnails loading, desktop/phone", "Thinking indicator — first question just sent, desktop/phone", "Thinking indicator — long wait, desktop/phone", "Conversation — question not answered, desktop/phone", "Input — 300-character limit reached, desktop/phone" |
| `03-archive-overlay/` | `ui-spec.md` | "Overlay v2 — fullscreen, image left … (landscape / tall)", "Overlay v2 — phone … (1, 2, 3 of 3)", "Archive overlay — picture still loading", "… picture could not be loaded", "… Show more loading", "… Show more failed" (each desktop/phone) |
| `04-iss-entry/` | `ui-spec.md` (+ `docs/business/iss-illustration-dev-spec.md` for the drawing: dot angles, the ±180° longitude fix, geometry, Moon, panel rules, test scenarios) | "ISS entry — desktop/phone, fresh snapshot", "ISS entry — desktop/phone, old snapshot" (the boards' dot positions and sample numbers are placeholders, and the old-snapshot boards still say "Now" where the decision is "Then"; the specs decide) |
| `05-asteroid-entry/` | `ui-spec.md` (+ `docs/business/asteroid-illustration-dev-spec-v2.md` for the drawing) | "Asteroid entry — desktop/phone, detail panel open", "Asteroid illustration — scatter layout, busy weeks" |
| `06-about/` | `ui-spec.md` (+ `docs/business/about-screen-content.md` for the text) | "About screen — desktop/phone (full length)" |
| `07-full-size-view/` | `ui-spec.md` | "Full-size view — desktop/phone" (fit-to-screen only; the zoomed state is specified in words, approved) |

The board "Overlay v2 — fullscreen, image on top (landscape image)" is a **rejected** layout and must be ignored.

## Product facts every screen relies on

- Three data sources only: NASA's Astronomy Picture of the Day (APOD) archive, near-Earth asteroids for a rolling 7-day window (distances in lunar distances), and the ISS position now plus 90 minutes of path.
- Each question is answered on its own; the agent has no history. The **screen** keeps the whole conversation visible and its chips reopenable for as long as the browser tab is open (it also survives a reload; a new tab starts empty).
- Refusals and other explanations are **written by the agent** (about three sentences, never answering the question); each has a fixed **backup text** used when the agent cannot write its own safely. Facts (names, dates, numbers, which source failed) come from code.
- A question is at most **300 characters**.
- **No usage limit:** the server is stateless and answers every request it receives (Furkan, Nov 3 2026), so there is no "limit reached" message.
- The hero image on the landing screen is **one static bundled image** (the Spitzer Tarantula Nebula). It is not fetched from APOD. (Decided Nov 3 2026; supersedes the earlier "latest APOD image" idea.)
- Images shown in answers are only archive entries that have an image (videos are excluded when the index is built).

## Cross-screen decisions (details live in the screen specs)

1. Answers are grouped into **chips by kind**: one Archive chip (up to 3 pictures), one Asteroids chip, one ISS chip. Each chip opens its own full-screen overlay.
2. For a mixed question, one overview sentence sits above the chips, and the **first chip in the fixed order Archive → Asteroids → ISS opens automatically**. Overlays never switch on their own.
3. **Ask again** (asteroid and ISS overlays) closes the overlay and sends a fixed question as a new message, which creates a new chip. Entries are never refreshed or stacked in place.
4. Empty and error cases for asteroids/ISS/archive are **plain text replies in the conversation**, no extra chips, no overlay.
5. The About screen opens from the About link; closing it returns the user to where they were.
6. The full-size view sits on top of the archive overlay; closing it (Esc or X) returns to the same picture in the overlay.
7. **Images (Decided Nov 3 2026):** pictures are shown from their NASA address and **never copied** (not on the server, not in the tab); only addresses and text are stored in the tab. The first archive open waits for picture 1 inside "Thinking…" with a 3-second cap, then falls back to an in-frame loading state; the next picture (n+1) is preloaded; "Show more" shows its own busy button and jumps to the first new picture only if the user is still on the same picture. Chip thumbnails load lazily after a reload, with a placeholder tile while loading or failed. A failed picture shows a message, a NASA link and a "Try again" button.
8. **Thinking indicator:** one indicator in the thread under the question, dots plus "Thinking…" (after about 8 seconds: "Still thinking… this one is taking longer than usual."); the Ask button is disabled while an answer is pending.
9. **Auto-open only when no layer is open (Decided Nov 3 2026):** if an overlay, the full-size view or About is open when an answer arrives, nothing opens by itself; the answer and its chips appear behind the open layer. No toast or badge (a "new answer ready" cue stays Open).
10. **Back button closes the topmost layer (Decided Nov 3 2026):** full-size view first, then the overlay or About; X and Esc behave the same. With no layer open, Back behaves as the browser normally does. Forward does nothing special. See `00-shared/ui-conventions.md`, section 8.
11. **No "new conversation" control (Decided Nov 3 2026):** the product name in the header is plain text, not clickable. The landing screen is not reachable again within a tab; closing the tab starts over.
12. **Failures and refusals (Decided Nov 3 2026, texts in `static-texts.md`):** timeout, failed request and sign-in-expired messages are **plain replies** that replace the thinking indicator. When a question could not be answered and goes back to the input box (timeout, failed request, sign-in expired, agent too slow), its **bubble stays in the thread and is marked**: red-tinted background and a "Not answered" label (drawn, wording confirmed). Focus moves to the field. Sign-in expired reloads the page after **3 seconds** and the conversation is restored. Explanations from the agent (earlier-answer, outside scope, no match, source unavailable) are plain replies too and their bubbles are not marked. The "conversation can't be saved" notice appears once per tab.
13. **Mixed question with something the product cannot answer (Decided Nov 3 2026):** the order is overview sentence, then the agent's explanation, then the chips. The four example chips appear **only** when the whole question was out of scope.
14. **Question limit and counter (Decided Nov 3 2026):** 300 characters; the field stops accepting characters, no error. A counter "44 / 300" sits under the input (landing and conversation) from the first character; at the limit it turns amber and the hint "Questions can be up to 300 characters." appears beside it (drawn on `InputLimit*`).
15. **No usage limit** (Furkan, Nov 3 2026): no "limit reached" text. A refused request is a failed request.
16. **ISS illustration (Decided Nov 4 2026):** dots are placed by how far the ISS has moved east since the snapshot, summed step by step with the ±180° longitude fix; they are not evenly spaced, and the gap before the marker is always open (29°–39°). The caption gets no sentence about the uneven spacing. The ISS service gives the day/night flag for all 10 points. On an old snapshot the "Now" marker reads **"Then"**. The label "about 1,000× farther than the ISS" stays. Full rule in `docs/business/iss-illustration-dev-spec.md`.

## Defaults not yet confirmed

Only the look and place of the replies that are not drawn (the agent's explanations, the can't-save notice, which uses the amber notice box he accepted), and the wording of the "Then" panel and screen-reader label on old ISS snapshots. Details in `02-conversation` and `04-iss-entry`.

## Still open

Final example-chip wording; tuning of the long-wait text and 8-second threshold after tests; whether a "new answer ready" cue is needed; ISS: whether a dot or label lands on the Moon's dashed line (to be checked with real data later), the age-label ladder, the Ask-again question text. Resolved Nov 3 2026 by the static texts and decisions: question length cap, storage blocked/full, oldest chips at the size cap (nothing is removed), wording of the earlier-answer reply and of the error and timeout messages, usage limit (none).

## Order to build / review

Landing → Conversation (with thinking indicator) → Archive overlay (with loading states) → Full-size view → ISS entry → Asteroid entry → About.
