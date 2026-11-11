# Full-size image view — UI spec

Boards (save screenshots here): **"Full-size view — desktop"** (`FullSizeDesktop`, 1440×900) and **"Full-size view — phone"** (`FullSizePhone`, 390×844). The boards show only the **fit-to-screen** state. The **zoomed state is not drawn**; it is specified in words below. Furkan approved it on Nov 3 2026, and no board is needed: the only new element is one button in the header (see "Zoomed state").

Shared values: `docs/ui/00-shared/ui-conventions.md`. Marks: **Decided** (drawn on the boards or approved), **Default**, **Open**.

## Purpose
Lets the user look at one archive picture as large as the screen allows, and zoom in to see detail. Opens from the archive overlay when the user clicks the image or the 44 px expand icon ("View full size"). Closing it returns to the archive overlay on the **same picture** (PRD flow: overlay → full-size → overlay).

## Frame (Decided, from boards)
- Covers the whole viewport on top of the archive overlay. Background **pure black `#000`**, no blurred backdrop, no panel border or radius.
- Three bands, top to bottom: **header**, **picture area**, **caption**.

### Header
- Right-aligned row, padding 12×16 desktop / 10 phone.
- **Close button**: 44 px circle, border `rgba(255,255,255,0.3)`, fill `rgba(255,255,255,0.06)`, white X icon, `aria-label` "Close full-size view".
- **Desktop only**: a hint **"Esc to close"** (13 px, `#AEB5C6`) to the left of the close button, 14 px gap. Not shown on phone.

### Picture area
- Fills all space between header and caption; side margin **24 px on desktop, 0 on phone**.
- The picture is **fitted (contain) and centred, never cropped, never upscaled beyond its own size** (`max-width/max-height: 100%`, so a small image is not blown up) (**Default** for the "not upscaled" part; the boards use max-width/max-height).
- **Alt text (Decided Nov 3 2026): the entry title** (the same text as the caption title). The archive's own explanation text is not used anywhere, because the agent writes the explanations, so the title is the only description available. The board placeholder "[Description of the picture]" is replaced by the title in the build. Same rule as the archive overlay.
- The picture comes **from its NASA address**; the app keeps no copy (Decided Nov 3 2026, see `03-archive-overlay`).

### Caption (bottom band)
- Desktop: one wrapping row, baseline aligned, gap 6×18, padding 14/24/22: **Entry title** (14 px, `#E3E7F0`), **"Image credit: …"** (13 px, `#AEB5C6`), **"View on NASA"** link (13 px, weight 500, amber `#F2B66B`, hover `#FFD39A`, opens the NASA entry in a new tab).
- Phone: stacked column, gap 4, padding 14/20/24: title 14 px; credit 12 px with line height 1.5; link 13 px with a 32 px tap height (the boards use 32; **Default** raise to 44 px if it can be done without changing the look, per the shared touch-target rule).
- The caption stays visible while zoomed (Decided), so the credit is never hidden.

## Behaviour — fit-to-screen state (Decided)
- Opens in fit-to-screen. **Esc closes** the view (PRD). The X button closes too. Clicking the black area outside the picture does **not** close it (**Default**, avoids accidental closing while panning).
- Focus moves to the close button on open; on close it returns to the expand icon (or the image) in the archive overlay, which is still on the same picture.
- No previous/next arrows here (not on the boards): to change picture, close and use the overlay's arrows (**Default**).

## Zoomed state (Decided, approved by Furkan Nov 3 2026)
The PRD requires "zoom" and "an easy way back from zoom to fit-to-screen":
1. **Zoom in**: click/tap the picture, or double-tap on phone, to zoom to **actual pixel size** (100 %) centred on the clicked point. Mouse wheel / trackpad pinch zooms smoothly; **pinch** on phone. Maximum zoom = actual pixel size or 3× the fitted size, whichever is larger. Cursor: zoom-in over the picture in fit state, grab hand when zoomed.
2. **Pan**: when the picture is larger than the screen, drag to move it (mouse drag, finger drag); arrow keys also pan (**Default**). Panning stops at the picture's edges, so it can never be lost off-screen.
3. **Easy way back (the one new control)**: while zoomed, a **"Fit to screen" button** appears in the header, **to the left of the close button**, same 44 px height, outlined style (border `rgba(255,255,255,0.3)`, text `#F2F4F8` 14 px, a small "shrink" icon before the text; on phone the icon-only version with `aria-label` "Fit to screen" is acceptable). Clicking it returns to fit-to-screen. On desktop it replaces the "Esc to close" hint while zoomed.
4. Other ways back: click/tap the zoomed picture without dragging, double-tap on phone, or the `0` key (**Default**).
5. **Esc always closes the whole full-size view** (also while zoomed), as the PRD says. It does not step back to fit first.
6. Reduced motion: zoom and pan changes are instant, no easing.
- Zoom resets to fit-to-screen every time the view opens.

## States
| State | What the user sees |
|---|---|
| Loading | The view can only be opened once the picture has loaded in the archive overlay (the expand icon is disabled until then, see `03-archive-overlay`), so the picture is already in the browser and appears instantly. No spinner is needed (Decided Nov 3 2026). |
| Image fails to load | Not reachable the same way (expand is disabled when the picture failed). If the picture is dropped from the browser's cache and cannot be fetched again when the view opens, show the same message as the archive overlay, centred in the picture area: **"This picture couldn't be loaded. You can view it on NASA."** with "view it on NASA" as an amber link, plus a **"Try again"** outlined button (Proposed, as in the overlay). Caption and close keep working. |
| Fit-to-screen | As drawn. |
| Zoomed | Same frame plus the "Fit to screen" button in the header. |

## Responsive
- Same layout logic at all widths; the only differences are the header hint (desktop only), the side margin (24 px vs 0) and the caption layout (row vs column). Switch at the shared breakpoint of about 900 px.
- Landscape phone: header and caption keep their sizes; the picture area gets the remaining height.

## Accessibility
- Behaves as a dialog (`role="dialog"`, `aria-modal`, label "Full-size view"); focus trapped inside while open (**Default**).
- Every control has a visible amber focus ring and an `aria-label`. Keyboard: Esc close, Tab to Fit to screen / close / NASA link, `0` fit, arrows pan when zoomed.
- Zoom gestures have button/keyboard alternatives (click, `0`, Fit to screen); nothing depends on pinch alone.

## Open items
- Whether zooming should load a higher-resolution image is a data question and is **left out of this UI spec on purpose** (Furkan, Nov 3 2026).
