# Landing screen — UI spec

Boards: **"Landing — desktop"** (`Main`, 1440×900) and **"Landing — phone"** (`Mobile`, 390×844). Save screenshots of both into this folder.
Shared values: `docs/ui/00-shared/ui-conventions.md`. Fixed texts: `docs/business/static-texts.md`. Marks: **Decided**, **Default**, **Open**.

**Board status (Nov 3 2026):** the two landing boards do **not** show the character counter row under the input (added after they were drawn). The counter is drawn on `InputLimit*` and `ConversationFailed*` (see `02-conversation`); the rule below applies to the landing input too.

## Purpose
First screen a visitor sees. Tells them what the product is in one line, shows a striking picture, and offers four example questions plus a text input. It collapses into the conversation on the first question (it is not a separate page).

## Hero image (Decided Nov 3 2026)
- **One static image bundled with the app**: the Spitzer three-colour Tarantula Nebula (NASA/JPL-Caltech, PIA23647). It is **not** fetched from APOD, there is no "latest image" logic and no fallback logic.
- Credit line, always visible at the bottom: **"Courtesy NASA/JPL-Caltech · Tarantula Nebula, Spitzer · View on NASA"**. "View on NASA" is a link to `https://www.jpl.nasa.gov/images/pia23647-tarantula-nebula-spitzer-3-color-image/` (opens in a new tab). Credit text 12 px, `#AEB5C6`; link underlined.
- Image fills the whole screen, `object-fit: cover`, focal point 30 % / 60 % on desktop and 28 % / 62 % on phone. Decorative: empty alt, `aria-hidden`.
- Dark overlay on top so text stays readable: vertical gradient, desktop from `rgba(7,9,15,0.50)` at the top through ~0.76 at 50 % to 0.92 at the bottom; phone 0.50 → 0.80 → 0.94.
- While the image loads the page shows the base colour `#0B1020` (**Default**), so text and input are usable immediately.

## Layout — desktop (1440×900)
- **About** link, top right (15 px, weight 500, `#E8EBF2`, min tap area 44 px). Opens the About screen (see `06-about`).
- Content block **centred horizontally and vertically**, max width about 680–760 px:
  1. Title **"Discover the Cosmos"** — Sora 600, 68 px, tight letter spacing, `#F2F4F8`.
  2. One-liner **"Ask about NASA's space pictures, nearby asteroids and the ISS."** — 20 px, `#C9CFDD`. (Typographic apostrophe.)
  3. Four example chips (below), wrapping and centred.
  4. Input form, max width 680 px, with the counter row under it.
- Credit line pinned to the bottom, centred.

## Layout — phone (390×844)
- Same elements, but the content block is **pinned to the bottom** (above the credit line), left-aligned; the picture shows through at the top.
- Title 40 px, one-liner 17 px, chips 40 px high, input placeholder shortened.
- About link top right with 44 px tap area.

## Example chips
- Four pill buttons: 13 px text, 1 px border `rgba(255,255,255,0.32)`, fill `rgba(12,16,28,0.62)`; **34 px high on desktop, 40 px on phone**; hover raises border opacity; keyboard focus = amber ring.
- Order and split (Decided in PRD): two archive, one asteroid, one ISS.
- **Text on the boards is dummy text. Final wording is Open** until tested against the real index:
  1. "Show me the most stunning nebula pictures" (archive)
  2. "What is a pulsar?" (archive)
  3. "Which asteroids are passing Earth this week?" (asteroids)
  4. "Where is the ISS right now?" (ISS)
- Clicking a chip **sends its text as the question** immediately (no need to press Ask). The asteroid and ISS chip texts are also what the "Ask again" buttons send (see `04-iss-entry`, `05-asteroid-entry`), so they must stay self-contained questions.
- The same four example questions are shown again as chips after an "outside what the product can answer" reply (see `02-conversation`).

## Input form
- Container max 680 px wide, radius 16, 1 px border `rgba(255,255,255,0.28)`, fill `#0F1524` (slightly translucent over the picture, **Default**).
- Text field 48 px high, 17 px (phone 16 px). Placeholder: desktop **"Ask about space pictures, asteroids or the ISS…"**, phone **"Ask about space…"**.
- **Ask** button: amber `#F2B66B`, text `#1A1306`, 48 px high, radius 12, weight 600.
- A visually hidden `<label>` reads **"Ask a question about space"**.
- Enter submits. Empty input: **Default** — Ask does nothing (no error text); button may look disabled.
- Pending (Open for the implementer): none needed; the screen switches to the conversation immediately.

### Question length limit and counter (Decided Nov 3 2026, hint text from `static-texts.md`; drawn on `InputLimit*`)
- A question can be at most **300 characters**. The field stops accepting characters at the limit (typing, and pasting, which is cut at 300). There is **no error message**.
- **Counter row** directly under the input container (6 px below, fixed height 20 px so nothing jumps). Right side: the **counter** "44 / 300", 13 px (phone 12 px), `#AEB5C6`; it appears once there is at least one character. Over the hero picture the row text keeps AA contrast through the dark gradient (**Default**).
- **At 300 characters** the counter turns amber and bold ("300 / 300") and the **hint "Questions can be up to 300 characters."** appears on the left of the same row. Both go back as soon as the text is shorter.
- The counter is not a live region; the hint is `aria-live="polite"` and linked to the field with `aria-describedby`.
- On the phone layout the row sits between the input and the credit line; the content block grows upward, nothing else moves.
- The same rule and look apply to the input of the conversation screen (see `02-conversation`).

## Behaviour
- **First question → conversation.** The question appears as a bubble, the "Thinking…" indicator shows, and the hero image and the landing text **fade away** (**Decided** as intent; **Default** timing 300–400 ms, instant under `prefers-reduced-motion`). The user then sees the conversation layout from `02-conversation`.
- When the app opens, the landing is shown only if the tab has no conversation yet. After a reload with an existing conversation the conversation is shown instead (PRD: the conversation survives a reload).
- No loading state, no error state on this screen. If the very first question fails, the user is already in the conversation screen, where the failure message appears (see `02-conversation`).

## Accessibility
- One `<h1>`: the title. Chips and input reachable by Tab in visual order: About, chips, input, Ask, credit link.
- Text contrast over the picture must stay AA; the overlay gradient exists for that reason.

## Open items
- Final example-chip texts (see above).
- Whether the credit line should move or be dimmed once the conversation starts (not needed, since the hero fades away).
