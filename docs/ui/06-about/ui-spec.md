# About screen — UI spec

Boards (save screenshots here): **"About screen — desktop (full length)"** (`AboutDesktop`, 1440×2680) and **"About screen — phone (full length)"** (`AboutPhone`, 390×3140). Both boards show the **whole scrolling page** at full length, not just one viewport.

**Text content** comes from `docs/business/about-screen-content.md` (owned by the product docs; this spec only covers presentation). If the two disagree on wording, the content doc wins.

Shared values: `docs/ui/00-shared/ui-conventions.md`. Marks: **Decided**, **Default**, **Open**.

## Purpose
Static information: what the product can and can't answer, one question at a time, how to read the illustrations, where the information comes from, independence from NASA, and a contact for removal requests.

## Entry and exit (Decided)
- Opened by the **About** link on the landing screen and the conversation header.
- It is a **full-screen view like the overlays** (not a separate page/URL required). **Closing returns the user to where they were** (landing or conversation, with scroll position and conversation intact).
- Esc closes it (**Default**). Focus moves into the view on open and back to the About link on close (**Default**).
- No contents list / table of contents (Decided: not needed yet).

## Layout
- Header (fixed): small label **"About"** (uppercase caption style) on the left and a **44 px close button** on the right (`aria-label` "Close").
- Body scrolls. **Single column, about 680 px wide on desktop, full width on phone** with 20 px side padding (**Default**), centred, on `#07090F`/overlay panel colours as in the other overlays (16 px page padding + 16 px radius frame on desktop, full-bleed on phone).
- Sections in this order (headings from the content doc): the opening paragraph under the page title, **What you can ask**, **What it can't answer**, **One question at a time**, **How to read the illustrations**, **Where the information comes from**, **Independence**, **Contact and removal requests**.

## Type
- Page title **"About Discover the Cosmos"** — Sora 36 px desktop / 28 px phone.
- Section headings — Sora 22 px / 20 px, with a **thin divider line above each section heading** (1 px, 8 % white) and generous spacing (about 40 px above).
- Body 16 px (phone 15–16 px), line height 1.7, `#E3E7F0`. Lead words that act as sub-headings in the content (e.g. "Pictures from the archive.", "Asteroids.", "The space station.") are **bold**.
- Source list under "Where the information comes from" is a plain bulleted list.

## Small visual additions (Decided; Furkan liked them)
Inside **How to read the illustrations**:
- A small **red ringed dot** (matching the asteroid hazard marker) placed before the phrase "A red circle with a ring".
- A small **day dot (amber) and night dot (dark with blue ring)** next to the phrase "shaded for day or night".
These are decorative (`aria-hidden`) because the text already says everything.

## Links
- **Email address** (<contact-info>) is a `mailto:` link in **amber** `#F2B66B`.
- Any other link (e.g. to NASA sources, if added) opens in a new tab, amber, underlined on hover (**Default**).

## Accessibility
- Real heading hierarchy: one `<h1>` (title), `<h2>` per section. The overlay behaves as a dialog (`role="dialog"`, labelled by the title, focus trapped while open — **Default**).
- Contrast AA on all text; focus ring amber 2 px.

## Open items
- Final wording changes live in the content doc, not here.
- Whether About should have its own URL (e.g. `/about`) for sharing: not decided; not required by the design.
