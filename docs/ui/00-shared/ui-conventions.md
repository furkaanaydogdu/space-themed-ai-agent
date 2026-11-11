# Shared UI conventions

Applies to every screen. Values were read from the design canvas boards (Nov 3 2026). Marks: **Decided**, **Default**, **Open** as in `docs/ui/README.md`. **Wording of fixed texts** (system messages, refusals, backups, limits) lives in `docs/business/static-texts.md`; the screen specs say where and how each one appears.

## 1. Look

A dark, space-themed interface. No light theme (**Default**: do not add one now).

### Colours
| Use | Value |
|---|---|
| Page background (landing base, conversation) | `#07090F` / landing base `#0B1020` |
| Outer frame behind overlays | `#04060B` |
| Overlay panel / text column | `#0D1322` |
| Picture frame (dark, behind pictures and loading states) | `#05070C`, loading/failed frame radial `#101829` to `#05070C` |
| Cards, history chips, input (conversation) | `#0F1524` |
| Question bubble | `#1B2438` |
| Question bubble, not answered | fill `#2B1D24`, border `rgba(255,149,152,0.45)`, label `#FF9598` |
| Icon tile behind asteroid/ISS/placeholder chip icon | `#16203A` |
| Text — primary / secondary / tertiary | `#F2F4F8` / `#E3E7F0` / `#AEB5C6` (also `#C9CFDD` for descriptions on the landing) |
| Links and outlined-button text | `#E8EBF2` (link hover `#F2B66B`; inside overlays links are `#F2B66B`, hover `#FFD39A`) |
| Accent (primary button, chip labels, daylight) | amber `#F2B66B`; text on amber `#1A1306` |
| Accent (night, ISS icon) | blue `#8FB0FF` |
| Notice box (warnings and soft errors) | border `rgba(242,182,107,0.5)`, fill `rgba(242,182,107,0.12)`, text `#F6D9AE`, amber warning icon |
| Borders | white at 8 % (dividers) to 32 % (outlined controls, example chips) |
| Hazard / safe (asteroids) | red `#E5484D` (edge `#FF9598`), green `#2FAE6B` (edge `#6FE3A4`) |

### Type
- **Sora** (500/600) for the product name and screen/entry titles. **Inter** (400/500/600) for everything else.
- Desktop landing title 68 px, phone 40 px; overlay entry title 26 px desktop / 22 px phone; About title 36 px / 28 px; section headings 22 px / 20 px.
- Body 15–16 px, line height 1.5–1.7. Small captions 12–14 px. "Your question" label: 11 px, uppercase, letter spacing 0.06 em, `#AEB5C6`.
- Chip labels (history chips): 12 px (11 px phone), bold, uppercase, amber.

### Shape
Radii: cards and inputs 14–16 px, buttons 12 px, pills 999 px, circular icon buttons 50 %. Overlay panel on desktop: 16 px outer padding, 16 px radius, 1 px border at 12 % white.

## 2. Components

- **Example chip** (pill): 13 px text, border `rgba(255,255,255,0.32)`, fill `rgba(12,16,28,0.62)` (phone 0.65). Min height **34 px desktop, 40 px phone** (Furkan asked for chips to be smaller than the input; **Decided**). Clicking one sends its text as a question. Disabled while an answer is pending (**Default**).
- **History chip** (card button): 340 px wide on desktop, full width on phone; thumbnail or icon tile 56 px desktop / 52 px phone; amber caps label; a second line of 15 px (14 px phone) text; chevron on the right. See `02-conversation`.
- **Primary button**: amber fill, `#1A1306` text, 15 px, weight 600, radius 12. The "Ask" button is 48 px high. **Disabled** look: same colours at 40 % opacity, `not-allowed` cursor.
- **Secondary (outlined) button**: transparent, 1 px border at 30 % white, `#E8EBF2` text, 15 px weight 500, **min height 44 px**, radius 12. **Busy** look (used by "Show more"): disabled, border 18 % white, text `#AEB5C6`, three small pulsing dots before the label.
- **Circular icon buttons**: close 44 px (border 22 % white); image arrows 48 px desktop / 44 px phone (border 30 % white, fill `rgba(7,9,15,0.72)`); expand icon 44 px. Disabled = 35 % opacity.
- **Loading dots**: three round dots in `#AEB5C6`, 6–10 px depending on context (7 px in "Thinking…", 6 px in the busy button, 10 px / 8 px in a picture frame), pulsing opacity 0.25 to 1 over 1.2 s with 0.2 s offsets. Static at 70 % opacity under reduced motion. Always `aria-hidden`; the surrounding element carries `role="status"` and a label.
- **Notice box**: amber-tinted box (colours above) with a warning icon and 14 px text; radius 12, padding 12×14. Used for the old-ISS-snapshot warning, the "Show more" failure and the "conversation can't be saved" notice. `role="alert"` for errors, `role="status"` for the can't-save notice. **Not** used for system failure messages in the thread (timeout, failed request, sign-in expired): those are plain replies (see below).
- **Plain reply**: an assistant paragraph in the normal answer style (16 px / phone 15 px, `#E3E7F0`, no box, no icon, no colour). Used for system messages, refusals and explanations. See `02-conversation`.
- **Question bubble, not answered** (Decided Nov 3 2026; drawn: `ConversationFailed*`): the normal bubble shape with the red-tinted fill and border from the colour table, plus a label under it, right-aligned: circled-exclamation icon (14 px) and "Not answered" (12 px, weight 600, `#FF9598`). Used for every question that went back to the input box (timeout, failed request, sign-in expired, agent too slow). The label is text, so colour is not the only signal.
- **Character counter row** (Decided Nov 3 2026; drawn: `InputLimit*`, `ConversationFailed*`): a 20 px high row directly under the input container (6 px gap). Right: counter "44 / 300" (13 px, phone 12 px, `#AEB5C6`, tabular numbers), shown once there is at least one character. At 300 the counter turns amber `#F2B66B`, weight 600, and the hint "Questions can be up to 300 characters." appears on the left (same size, `#AEB5C6`, no icon). The hint is `aria-live="polite"` and linked with `aria-describedby`; the counter is not a live region.
- **Placeholder tile**: the `#16203A` rounded tile with a neutral outlined picture icon, used in an archive chip while its thumbnail loads or if it fails.
- **Text input row**: rounded 16 px container with the text field (48 px high, 17 px desktop / 16 px phone) and the Ask button, with the counter row under it. The field accepts at most **300 characters** (Decided Nov 3 2026; paste is cut at the limit, no error message).
- **Focus**: every control shows a 2 px amber `#F2B66B` outline with 2 px offset on keyboard focus.

## 3. Layout rules
- Reference widths: desktop board 1440 px, phone board 390 px. Desktop layouts must also work in narrower windows.
- **Breakpoint (Decided)**: below roughly **900 px window width** the desktop side-by-side overlay switches to the phone layout (image/illustration on top). The conversation uses a centred column (max 760 px) and shrinks naturally.
- Touch targets are at least 44 px, except example chips (34/40 px, see above).
- Page scrolls inside overlays: the header ("Your question" + close) and the footer button stay fixed; the text column between them scrolls.

## 4. Overlay frame (archive, ISS, asteroid)
- Header row: "Your question" label above the question text, close button (44 px) on the right. **Decided** (Furkan wanted the question line).
- Desktop: image or illustration frame on the left filling the space, a **400 px text column on the right**. Phone: header, then the frame on top (300 px archive, 380 px ISS, about 460 px asteroid), then the text column, then the footer button.
- Opens only when the whole answer is ready (for archive answers also when picture 1 has loaded, or after a 3-second cap, see `03-archive-overlay`) **and nothing else is open** (see section 8). Closing returns the user to the conversation with the chip still there.

## 5. Images and loading (Decided Nov 3 2026)
- Pictures are shown **from their NASA address**. The app keeps **no copy** of any image (not on the server, not in the tab). Only addresses and text are stored with the conversation in the tab.
- First open waits for picture 1 inside "Thinking…" with a **3-second cap**, then falls back to the in-frame loading state. The next picture (n+1) is preloaded. Details: `03-archive-overlay`.
- Every picture can show: loading (dots), failed (message + NASA link + "Try again"), or loaded.

## 6. Motion and accessibility
- "Thinking…" shows three dots pulsing (1.2 s cycle, 0.2 s offsets). With `prefers-reduced-motion` the animation stops and the dots stay at 70 % opacity. **Decided**. Details of the indicator: `02-conversation`.
- The landing hero fades out when the first question is sent (**Decided** as an idea; duration is up to the implementer, **Default** around 300–400 ms, none under reduced motion).
- Decorative images and icons are `aria-hidden`; every icon-only button has an `aria-label`; form fields have labels (visually hidden where the design shows none).
- Colour is never the only signal: hazardous asteroids also have a ring; day/night dots also have a legend and text; a not-answered bubble also has its label.
- Esc closes the topmost open layer (**Default**); Tab order follows the visual order.

## 7. Writing style on screen
Plain, short sentences. No jargon without explaining it. Distances in lunar distances (never kilometres on screen), times in the user's local time. Typographic apostrophes and quotes.
- **First person, calm tone** in replies that speak for the product ("I couldn't find…", "I answer each question on its own"), as in `static-texts.md`. Failure messages say what happened, what happened to the question ("Your question is back in the box") and what to do next; they never blame the visitor.
- Fixed texts are copied from `docs/business/static-texts.md` word for word (with typographic quotes and apostrophes). Do not paraphrase them in code or boards.

## 8. Layers, auto-open and the Back button (Decided Nov 3 2026)
- **Layers** stack on top of the conversation: an answer overlay (archive, ISS or asteroid) **or** the About screen sits directly on the conversation, and the full-size view sits on top of an archive overlay. Only one overlay or About is open at a time.
- **Auto-open rule:** a new answer's first chip opens its overlay automatically **only when no layer is open**. If an overlay, the full-size view or About is open when the answer arrives, nothing opens: the answer (or failure message) and its chips appear behind the open layer and the user opens the chip later. See `02-conversation`.
- **Back button:** pressing the browser's Back button **closes the topmost open layer**, in this order: full-size view, then the overlay or About. Closing by the X button or Esc behaves the same, so each open layer corresponds to one step back and Back never skips over a layer. With no layer open, Back behaves as the browser normally does (it can leave the app). Forward does nothing special (**Default**).
- On phones this is the expected way to close a layer.
