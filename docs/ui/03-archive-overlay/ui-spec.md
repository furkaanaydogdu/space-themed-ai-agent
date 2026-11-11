# Archive overlay — UI spec

Boards (save screenshots here):
- **"Overlay v2 — fullscreen, image left and text right (landscape image)"** (`FullSide`)
- **"Overlay v2 — fullscreen, image left and text right (tall image)"** (`FullSideTall`)
- **"Overlay v2 — phone, landscape image (1 of 3)"** (`OverlayPhoneWide`)
- **"Overlay v2 — phone, tall image (2 of 3)"** (`OverlayPhoneTall`)
- **"Overlay v2 — phone, square image (3 of 3)"** (`OverlayPhone`)
- **Loading and failure states (added Nov 3 2026):**
  - **"Archive overlay — picture still loading, desktop / phone"** (`ArchiveLoadingDesktop`, `ArchiveLoadingPhone`)
  - **"Archive overlay — picture could not be loaded, desktop / phone"** (`ArchiveFailedDesktop`, `ArchiveFailedPhone`)
  - **"Archive overlay — Show more loading, desktop / phone"** (`ArchiveMoreBusyDesktop`, `ArchiveMoreBusyPhone`)
  - **"Archive overlay — Show more failed, desktop / phone"** (`ArchiveMoreErrorDesktop`, `ArchiveMoreErrorPhone`)
- **Ignore** "Overlay v2 — fullscreen, image on top (landscape image)" (`FullStacked`): rejected layout.

The full-size view that opens from the expand icon / image click is specified in `docs/ui/07-full-size-view/ui-spec.md` (boards `FullSize*`).

Shared values: `docs/ui/00-shared/ui-conventions.md`. Marks: **Decided**, **Default**, **Open**.

## Purpose
Full-screen view of an Archive answer: up to three NASA archive pictures, one at a time, each with title, date, credit, a link to NASA, and a short explanation written by the agent. Opens automatically if Archive is the first kind in the answer; otherwise from the Archive chip.

## Frame
Full viewport, background `#04060B`. **Desktop: 16 px page padding and a 16 px-radius panel** with a 1 px border at 12 % white. Phone: full-bleed.

## Desktop layout (≥ about 900 px wide)
- **Left: image frame** filling all remaining space.
  - Backdrop: the same picture, **blurred and darkened** (a second use of the same loaded image, no extra download); the picture itself is **fitted** (contain), **never cropped**, centred. Works for landscape, tall and square images (boards show landscape and tall).
  - **Previous / next arrows**: 48 px circles, vertically centred at the frame edges, border 30 % white, fill `rgba(7,9,15,0.72)`. The previous arrow is **disabled (35 % opacity)** on the first picture, next disabled on the last.
  - **Counter pill** "1 of 3" at the bottom centre of the frame. Number of pictures grows when "Show more" adds more.
  - **Expand icon** (44 px, top right of the frame), `aria-label` "View full size". Clicking the image does the same. Opens the full-size view (`07-full-size-view`). **Disabled (35 % opacity) while the picture is loading or failed** (drawn).
- **Right: text column, 400 px wide**, background `#0D1322`, left border at 8 % white. Top to bottom:
  1. **Header row** (fixed): label **"Your question"** (11 px caps, `#AEB5C6`) above the user's question text (15 px, up to two lines, ellipsis), and a **44 px close button** at the right (`aria-label` "Close").
  2. **Scrolling body**:
     - **Title** — Sora 26 px, `#F2F4F8`.
     - **Date** — e.g. "2 Nov 2023", 14 px `#AEB5C6`.
     - **"Image credit: …"** — 13–14 px `#AEB5C6` (credit text from the archive record; wording like "Image credit: NASA, ESA, …").
     - **"View on NASA"** link — amber `#F2B66B`, underlined on hover, opens the original APOD page in a new tab.
     - **Explanation** — **2–4 sentences written by the agent**, 15–16 px, line height 1.6, `#E3E7F0`. NASA's own explanation text is **not** copied; the link is the verifiable source.
  3. **Footer (fixed)**: optional notice (see "Show more" failure), then the **"Show more"** button (outlined secondary, 44 px min height, full width of the column), 12 px gap between them.

## Phone layout (390×844; also windows narrower than about 900 px)
- Top: header row (question label + text + 44 px close).
- Then the **image frame, 300 px high**, same fitted-on-blurred-backdrop treatment; arrows 44 px at the frame sides; counter pill at the bottom; expand icon top right.
- Then the scrolling text (title Sora 22 px, date, credit, "View on NASA", explanation).
- Footer: notice (if any) and **"Show more"** pinned at the bottom.
- First screenshot shows picture 1 of 3 with the previous arrow disabled.

## Loading the pictures (Decided Nov 3 2026)
Pictures are always shown **from their NASA address**; the app keeps no copy of any image (neither on the server nor in the tab). Only addresses and text are stored in the tab with the conversation.

**First open (new answer)**
1. When the answer arrives, the app first loads **picture 1** (it is also the chip's thumbnail), while the "Thinking…" indicator is still showing. The chips and the overlay appear together once it has loaded.
2. **Cap: 3 seconds** (Default value; configurable). If picture 1 has not loaded by then, the overlay opens anyway with the **in-frame loading state** and the picture swaps in when it arrives. The cap ends the wait, never the loading: loading continues.
3. Picture 2 and 3 are **not** loaded up front. The app **preloads the next picture (n+1)** of whatever picture is current, so pressing next is usually instant. (The previous picture is already loaded by then.)

**Reopening an old chip**: same behaviour. The browser requests the picture again from NASA (its normal cache often answers instantly). The current picture and the next one load; if the picture is not there yet the in-frame loading state shows.

**After a page reload** with an overlay open or chips restored: the same, nothing special.

### In-frame loading state (drawn: `ArchiveLoading*`)
- The frame shows a dark background (radial `#101829` to `#05070C`) with **three pulsing dots** centred (10 px desktop / 8 px phone, `#AEB5C6`, same pulse as "Thinking…"; static at 70 % opacity under reduced motion).
- No blurred backdrop, no picture. The frame keeps its normal size, so nothing jumps when the picture arrives.
- Arrows and counter work as usual; the expand icon is disabled until the picture has loaded. The text column (title, date, credit, link, explanation) is fully visible.
- `role="status"`, `aria-label="Loading picture"`.

### Picture failed to load (drawn: `ArchiveFailed*`)
- The frame shows, centred: a "picture off" icon (outlined picture with an amber slash), the line **"This picture couldn't be loaded."** (16 px desktop / 14 px phone, `#E3E7F0`, weight 500), the line **"You can view it on NASA."** (14 px / 13 px, `#AEB5C6`) where "view it on NASA" is an amber link to the NASA entry, and a **"Try again"** outlined button (44 px high) that requests the picture again and returns to the loading state. (All Decided; "Try again" approved by Furkan Nov 3 2026.)
- Arrows, counter and text column stay usable; the expand icon is disabled. `role="alert"`.
- The same wording is used in the full-size view (`07-full-size-view`).
- A thumbnail that fails (chip in the conversation) uses the placeholder tile, see `02-conversation`.

## "Show more" (Decided, PRD §7.2)
- Lives in the overlay of **every** Archive chip, including earlier chips the user reopens.
- Loads further **unseen** pictures for the same archive query **without adding a question** to the conversation.
- New pictures join the **same chip**: the chip label and the "n of N" counter grow.
- When all matches have been shown the button is **no longer shown** (hidden, not disabled).

**Waiting (drawn: `ArchiveMoreBusy*`)** — Decided Nov 3 2026
- On press the button becomes **disabled and busy**: three small pulsing dots (6 px) and the text **"Loading more…"** in `#AEB5C6`, border dimmed to 18 % white. `aria-busy="true"`. The rest of the overlay stays usable: the user can keep browsing the pictures already loaded.
- The busy state covers **both waits**: the server's answer, then the first new picture loading, with the same **3-second cap** as above (cap counted from when the server answer arrives).
- **When the wait ends:**
  - If the user is **still on the same picture** they were on when they pressed Show more: the overlay **jumps to the first new picture** (e.g. 3 of 3 becomes 4 of 6). If that picture has not loaded when the cap passes, the jump happens anyway and the in-frame loading state shows; the picture swaps in when it arrives (or the failure message shows).
  - If the user has **moved to another picture** meanwhile: no jump, only the counter and chip label grow.
- Preloading (n+1) continues from the picture that is now current; if the user sits on the last old picture, the first new picture starts loading as soon as the answer arrives.
- The button returns to its normal "Show more" look (or disappears if there is nothing more).

**Failure (drawn: `ArchiveMoreError*`)**
- If the server fails or times out: an **amber notice box** appears **above the button** in the fixed footer (same style as the ISS old-snapshot warning: border `rgba(242,182,107,0.5)`, fill `rgba(242,182,107,0.12)`, warning icon, text `#F6D9AE` 14 px): **"Couldn't load more pictures. Try again."**
- The button is enabled again with its normal "Show more" label; pressing it retries and hides the notice. `role="alert"`.
- The notice also disappears when the user presses next/previous or when a retry succeeds (**Default**).

## States
| State | What the user sees |
|---|---|
| Opening (new answer) | Opens when the whole answer is ready **and** picture 1 has loaded, or after the 3-second cap with the in-frame loading state. |
| Picture loading | In-frame loading state (dots); expand icon disabled. |
| Picture failed | Frame message with link and "Try again"; expand icon disabled. |
| Picture changes (arrows) | Image, title, date, credit, link and explanation all swap together; the text column scrolls back to the top (**Default**); the counter updates. |
| First / last picture | The unavailable arrow is dimmed and not focusable-clickable (**Default**: `aria-disabled`). |
| One picture only | No arrows, no counter pill (**Default**). |
| Show more waiting / failed | See "Show more". |
| Reopened later | Same text content as before, including pictures added by "Show more"; the pictures themselves are requested again from NASA. |
| Full-size view open | Sits on top; closing it returns here on the same picture. |

## Keyboard (**Default**, confirm)
- Left/Right arrow keys change picture; Esc closes the overlay; focus moves into the overlay on open and returns to the chip on close.
- While the full-size view is open, Esc closes **only** the full-size view (the overlay stays); a second Esc closes the overlay.
- Tab order: close, arrows, expand, links, Show more.

## Accessibility
- **Alt text (Decided Nov 3 2026): the picture's title.** The archive's own explanation text is not used anywhere (the agent writes the explanations), so the title is the only description available. The blurred backdrop copy is `aria-hidden` with empty alt. The full-size view uses the same alt text.
- Counter is announced politely when it changes ("2 of 3").
- Disabled arrows keep `aria-label`s: "Previous picture", "Next picture".
- Loading state is announced politely ("Loading picture"); failure messages use `role="alert"`.

## Open items
- The 3-second cap is a Default and may be tuned after real tests.
- Keyboard shortcuts (defaults above).
