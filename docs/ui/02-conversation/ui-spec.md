# Conversation screen — UI spec

Boards (save screenshots here):
- **"Conversation — desktop"** (`Conversation`), **"Conversation — phone"** (`ConversationPhone`)
- **"Conversation — mixed answer, desktop / phone"** (`ConversationMixed`, `ConversationMixedPhone`)
- **Added Nov 3 2026:**
  - **"Conversation — after a reload, archive thumbnails loading, desktop / phone"** (`ConversationRestoredDesktop`, `ConversationRestoredPhone`)
  - **"Thinking indicator — first question just sent, desktop / phone"** (`ThinkingDesktop`, `ThinkingPhone`)
  - **"Thinking indicator — long wait, desktop / phone"** (`ThinkingLongDesktop`, `ThinkingLongPhone`)
  - **"Conversation — question not answered, desktop / phone"** (`ConversationFailedDesktop`, `ConversationFailedPhone`): marked bubble, plain failure reply, question back in the input, counter.
  - **"Input — 300-character limit reached, desktop / phone"** (`InputLimitDesktop`, `InputLimitPhone`): hint and amber counter.

**Board status (Nov 3 2026):** all boards use the final chip labels. The first two (`Conversation`, `ConversationPhone`) were updated from the older "Open the answer" / "ISS · position and path" text to "Open the pictures" and "ISS · 15:52" / "Open the illustration". The out-of-scope reply on those boards shows draft wording; **the backup text in `docs/business/static-texts.md` (section 3) is now the reference** and wins over the board. **The older conversation boards (and the landing boards) do not show the character counter under the input; the two new board pairs do, and the spec below applies to every input.** The "can't save" notice and the agent's explanation replies (including a mixed answer with an explanation) are not drawn; they are specified in words.

Shared values: `docs/ui/00-shared/ui-conventions.md`. Fixed texts and what the agent's explanations must say: `docs/business/static-texts.md` (**source of truth for every wording**; this spec says where and how they appear). Marks: **Decided**, **Default**, **Open**.

## Purpose
The main view. Questions and short answers stack in one column. Each answer is one overview sentence plus up to three **chips** (Archive, Asteroids, ISS). Chips open the full-screen overlays and stay in the conversation.

## Structure (top to bottom)
1. **Header** — product name (Sora 600, 18 px desktop / 16 px phone) on the left, **About** link on the right (15 px, 44 px tap area). Thin bottom border `rgba(255,255,255,0.08)`. Padding 16×48 desktop, 6×20 phone. The product name is plain text, not a link or button (Decided, see "Starting over").
2. **Thread** — scrolling column, centred, **max 760 px**, padding 32×24 desktop / 20 phone, 28 px (desktop) or 20 px (phone) between items.
3. **Input** pinned at the bottom (same form as the landing: 48 px field, amber Ask button; container max 760 px; placeholder "Ask about space pictures, asteroids or the ISS…" / phone "Ask about space…"; hidden label "Ask a question about space"), with the **character counter row** directly under it (see "Question length limit and counter").
- The page background is `#07090F`. The landing hero is gone.
- The thread scrolls to the newest item whenever a question is sent or an answer arrives (**Default**).

## Thread items
### Question bubble
Right-aligned, background `#1B2438`, radius 18/18/4/18, text 16 px (phone 15 px), line height 1.5, max width 520 px (phone 290 px), padding 12×18 (phone 10×16). At most 300 characters (see "Question length limit and counter"), so it never gets very tall.

### Question bubble — not answered (Decided Nov 3 2026; drawn: `ConversationFailed*`)
When a question could not be answered and went back to the input box (timeout, failed request, sign-in expired, or the agent stopped itself for taking too long), its bubble stays in the thread but is **marked**, so the thread never looks as if that question was answered:
- **Background** `#2B1D24` (a dark red tint instead of `#1B2438`) and a 1 px border `rgba(255,149,152,0.45)`; same shape, text colour and size as a normal bubble.
- **Label** directly under the bubble, right-aligned with it, 6 px below: a small circled exclamation icon (14 px) and the text **"Not answered"** (wording confirmed by Furkan), 12 px, weight 600, `#FF9598`. The colour is never the only signal: the label carries the meaning. The label is part of the bubble's accessible text (read after the question).
- The mark is permanent: it stays after a successful retry (the retry is a new bubble below) and after a reload (it is stored with the conversation).
- Refusals and "nothing matched" replies are real answers, so their bubble is **not** marked.

### Assistant answer
Left-aligned block, max width 620 px, 14 px gap (phone 12 px):
- **Overview sentence** — 16 px (phone 15 px), line height 1.6, `#E3E7F0`. Written by the agent, one sentence, ties the kinds together.
- **Chips**, stacked with 10 px gap (phone 8 px), in a **fixed order: Archive, Asteroids, ISS**, only the kinds that were answered.

### History chip (a button)
- 340 px wide on desktop, full width on phone; padding 10/16/10/10 (phone 8/14/8/8); radius 14; border `rgba(255,255,255,0.18)`; fill `#0F1524`; hover brightens the border (**Default**).
- Left: 56 px (phone 52 px) rounded-10 tile:
  - **Archive**: thumbnail of the first picture (cover), or the **placeholder tile** (below).
  - **Asteroids**: amber rock icon on tile `#16203A`.
  - **ISS**: blue `#8FB0FF` globe-with-orbit icon on tile `#16203A`.
- Middle: **label** (12 px, phone 11 px, bold, uppercase, letter spacing 0.06 em, amber) and a **second line** (15 px, phone 14 px).
- Right: chevron icon `#AEB5C6`.
- **Final texts (Decided):**

| Kind | Label | Second line |
|---|---|---|
| Archive | `Archive · 3 pictures` (number = pictures held; **grows** when "Show more" adds pictures; singular "1 picture") | `Open the pictures` |
| Asteroids | `Asteroids · 2–9 Nov` (the 7-day window) | `Open the illustration` |
| ISS | `ISS · 09:14` (time of the snapshot, user's local time, 24 h) | `Open the illustration` |

- A chip opens its overlay. Closing the overlay returns here; the chip stays. Chips are reopenable for as long as the tab is open (survives a reload; a new tab starts empty).
- Accessible name = label + second line (e.g. "Archive, 3 pictures, open the pictures").

### Archive thumbnail and placeholder tile (Decided Nov 3 2026; drawn: `ConversationRestored*`)
- The thumbnail is the first picture, loaded from its NASA address (the app keeps no copy). When the answer arrives, picture 1 is already loaded (see `03-archive-overlay`), so the thumbnail shows at once.
- After a **page reload**, restored chips load their thumbnails **lazily**: only when the chip scrolls into view, so a long conversation does not download many large pictures at once.
- **Placeholder tile** while a thumbnail is loading **and** if it fails to load: the same `#16203A` rounded tile as the asteroid/ISS chips, with a neutral outlined **picture icon** in `#AEB5C6` (26–30 px). The chip is fully usable either way. No spinner on the tile.

### Thinking indicator (drawn: `Thinking*`, `ThinkingLong*`)
Shown from the moment a question is sent until the **whole answer is ready** (and picture 1 has loaded, within the 3-second cap, see `03-archive-overlay`). It is the only waiting indicator in the thread; "Show more" has its own busy button.
- **Position:** in the assistant's column, directly under the question bubble, left-aligned with the answer text (max width as an answer). Nothing else appears with it: no overlay, no chips, no partial text. The agent's answer arrives all at once.
- **Look:** three **7 px dots**, 5 px apart, `#AEB5C6`, pulsing (1.2 s cycle, 0.2 s offset between dots, opacity 0.25 to 1), followed by the text, 10 px gap, 15 px (phone 14 px) `#AEB5C6`, line height 1.5. Dots align with the first text line.
- **Standard text (Decided):** **"Thinking…"**
- **Long wait (Decided Nov 3 2026; wording and threshold to be adjusted after tests):** after about **8 seconds** (Default, configurable) the same text line is replaced by **"Still thinking… this one is taking longer than usual."** Same place, same dots, no layout jump (the line may wrap to two lines on phone). Reason: a cold start or a multi-step answer can take well over 10 seconds, and silence reads as a hang.
- **When it ends:** it disappears and is replaced **in the same place** by either the answer (overview sentence and chips, then the first chip's overlay opens if nothing else is open, see "Mixed answers") or a reply from "Replies that are not answers" (failure messages, explanations).
- **Reduced motion:** dots do not pulse and stay at 70 % opacity.
- **Accessibility:** `role="status"` with `aria-live="polite"`, so a screen reader hears "Thinking…" once and the later change; the dots are `aria-hidden`.
- **First question:** the landing hero and text fade away (see `01-landing`), leaving header, the user's bubble, the indicator and the input (drawn: `Thinking*`). The empty space below is normal.

### Input while an answer is pending (Default; drawn: `Thinking*`)
- The **Ask button is disabled**: same amber at 40 % opacity, `not-allowed` cursor, `aria-disabled`. The text field stays editable, so the user can type the next question; Enter does nothing until the answer is shown.
- Example chips in an earlier decline reply are disabled while an answer is pending, too.
- The About link and **all history chips keep working** while an answer is pending (this is why the auto-open rule below exists). If the user opens About or an old chip and closes it, the indicator is still there.
- "Ask again" from an overlay closes the overlay, adds the new question bubble and shows the indicator as usual.
- **If the user typed something while waiting and the request then fails**, the text they typed is kept and the failed question is **not** put back (their new text is more recent). The failed bubble is still marked "Not answered". **Default**; rare case.

### Question length limit and counter (Decided Nov 3 2026; drawn: `ConversationFailed*`, `InputLimit*`)
Same rule as the landing input (see `01-landing`): at most **300 characters**; the field stops accepting characters at the limit (paste is cut at 300); no error message.
- **Counter row** directly under the input container, 6 px below, always the same height (20 px, so nothing jumps). On the right: the **counter "44 / 300"** (13 px, phone 12 px, `#AEB5C6`, tabular numbers). It shows as soon as there is at least one character; with an empty field the row is empty (**Default**).
- **At 300 characters** the counter turns amber `#F2B66B`, weight 600 ("300 / 300"), and the **hint "Questions can be up to 300 characters."** appears on the left of the same row (same size, `#AEB5C6`, no icon). Both disappear or change back as soon as the text is shorter.
- The counter is **not** a live region (it would announce every keystroke); the hint is `aria-live="polite"` and linked to the field with `aria-describedby`. The counter text is read when the user navigates to it.
- On the conversation screen the row sits inside the pinned input area, so the thread's bottom padding already accounts for it.
- When a failed question goes back into the box the counter shows its length ("44 / 300").

## Replies that are not answers
A reply with no chips is a short paragraph in the same assistant style: **plain text, no box, no icon, no colour** (**Decided**: the static-texts doc calls them "plain replies"; the only marking is on the user's bubble, see above). There are two families. All wording is in `docs/business/static-texts.md`; the texts below are quoted so the build does not need the other doc open, but if they differ, `static-texts.md` wins.

### A. System messages (fixed text, shown by the product)
Each replaces the thinking indicator in the same place.

| Situation | Text | What else happens |
|---|---|---|
| **Timeout** | "That took longer than I could wait, so I stopped. Your question is back in the box. Try again, or ask something simpler." | The question returns to the input box; its bubble is marked "Not answered". |
| **Failed request** (lost connection, server error, anything else) | "Something went wrong and I couldn't get an answer. Your question is back in the box. Press Ask to try again." | Same. (Drawn: `ConversationFailed*`.) |
| **Sign-in expired** | "Your sign-in has expired. The page will reload so you can sign in again." | After **3 seconds** the page reloads on its own (**Decided**); the visitor signs in again and the conversation is restored, with the unanswered question back in the input box and its bubble marked. |
| **Empty asteroid week** | "NASA's data lists no near-Earth asteroids passing Earth between 2 and 9 Nov." (the dates are the window's) | No overlay, no chip, no example chips; the bubble is **not** marked (it is an answer). In a mixed question the sentence is added to the overview sentence. |

How "the question returns to the input box" looks (**Default** except the mark, which is Decided): the user's **bubble stays in the thread** above the failure message with the "Not answered" mark; the input field is filled with the same text; **focus moves to the field with the cursor at the end**; the Ask button is enabled again; the thread scrolls to the failure message. Pressing Ask sends it again as a **new** bubble (a normal one), so after a retry the failed question appears twice in the thread, the first one marked; that is accepted. The failure message is announced politely like any answer.

Sign-in expired: no button. If the reload does not happen, the message simply stays. If the very first question hits an expired sign-in, the same applies (the conversation screen is already showing).

### B. Explanations written by the agent, with a fixed backup
When the agent cannot answer, it writes a short explanation itself (about three sentences, never answering the question or hinting at the answer). The product shows the **backup text** instead when the agent cannot write its own message safely (it fails, or states something the data does not support). Both look identical to the user.

| Reason | What the explanation says | Backup text (fixed) | Extra |
|---|---|---|---|
| **Relies on an earlier answer** ("tell me more about that one") | Each question is answered on its own; ask the visitor to name what they mean (for example a picture's title); point to the earlier answer, which can be reopened | "I answer each question on its own, so I can't tell what you're referring to. Please name it, for example a picture's title. Your earlier answer is still in the conversation above: tap it to open it again." | No chips. |
| **Outside what the product can answer** (including questions about one specific asteroid, comparisons between asteroids, one point on the ISS path) | Plainly what the product can answer: the picture archive, near-Earth asteroids for the next 7 days, the ISS's current position and path | Desktop: "I can't answer that one. I only use three sources: NASA's Astronomy Picture of the Day archive, near-Earth asteroids for the next 7 days, and the ISS's current position and path. You could try one of these:" Phone: "I can't answer that one. I only use NASA's picture archive, near-Earth asteroids for the next 7 days, and the ISS's position and path. You could try:" | **The four example chips from the landing follow**, as in the earlier boards. Chips are the same size and look as on the landing (34 / 40 px). |
| **Nothing in the picture archive matches** | Nothing matched well; the archive covers roughly the last two years; describe the picture another way | "I couldn't find a good match for that in NASA's picture archive, which covers roughly the last two years. Try describing it another way, for example by its name or what it shows." | No chips. |
| **A source is unavailable** | Which part could not be loaded; try again later; any part that did load is still shown | "I couldn't reach {NASA's picture archive / NASA's asteroid data / the ISS position service} just now, so that part is missing. Please try again in a moment." | Parts that did load appear as normal chips. |
| **The agent stops itself because the answer takes too long** | It stopped because it was taking too long; try again or ask something simpler | Same text as the **Timeout** system message above | The question returns to the input box and its bubble is marked "Not answered" (as for Timeout). |

- **Mixed questions (Decided Nov 3 2026, not drawn).** When one question has a part the product can answer and a part it cannot (or a source is down), the answerable part is answered normally and the agent's explanation is **added after the overview sentence**. Example: "Show me a nebula picture and tell me about the asteroid Apophis" → overview sentence about the nebula pictures, then the explanation ("I can't answer questions about one specific asteroid. I can show the near-Earth asteroids passing Earth in the next 7 days…"), then the Archive chip. The order in the column is therefore **overview sentence, explanation, chips**. **The four example chips are shown only when the whole question was outside what the product can answer**, never under a mixed answer. The bubble of a mixed question is not marked, because part of it was answered.
- Facts in these messages (names, dates, numbers, which source was unreachable) come from code; the agent only writes the words around them.

## Conversation that cannot be saved (Decided Nov 3 2026, text from `static-texts.md`)
When the browser blocks saving, or the saved conversation no longer fits, the screen shows **once per tab**: **"This page can't save the conversation in your browser, so it will be lost if you reload or close the tab."** The conversation keeps working on screen. This replaces the earlier open question about what happens to the oldest chips at the size cap: nothing is removed, the user is just told that saving no longer works.
- Look (**Default**, not drawn; Furkan agreed to the notice box): the **notice box** from the shared conventions (amber tint, warning icon, 14 px text), shown as an item in the thread directly after the answer during which saving first failed, same width as an answer. No button. It scrolls away with the conversation and is not shown again in this tab. `role="status"`, since nothing is blocked.
- If saving fails on the very first answer, the notice appears right under that answer.

## Mixed answers (boards `ConversationMixed*`)
- Example turn 1: question "Show me a nebula picture, the asteroids passing this week and where the ISS is" → overview "Here are nebula pictures from NASA's archive, this week's near-Earth asteroids and the ISS's current position." → three chips (Archive · 3 pictures / Asteroids · 2–9 Nov / ISS · 09:14).
- Example turn 2: "Where is the ISS right now?" → "Here is the ISS's current position and its path over the next 90 minutes." → one chip `ISS · 15:52`.
- **When an answer arrives, its first chip's overlay opens automatically** (order Archive → Asteroids → ISS). Overlays never switch on their own; the user closes one and taps another chip. The conversation behind the overlay already contains the new answer, so closing shows it.
- **Auto-open only when nothing else is open (Decided Nov 3 2026).** If an overlay, the full-size view or the About screen is open at the moment the answer arrives, **no overlay opens**: the thinking indicator is replaced by the overview sentence and chips behind the open layer, and the user opens the chip when they come back. The answer is never pushed over something the user is reading. No toast or badge (**Default**; a "new answer ready" cue is Open if tests show people miss it). The same holds for failure messages: they appear behind the open layer.
- Replies with no chips (section above) never open an overlay.

## Starting over (Decided Nov 3 2026)
There is **no "new conversation" control** and the product name in the header is not clickable. The landing screen is not reachable again within a tab; to start over the user closes the tab (a new tab starts empty).

## Behaviour summary
- Ask again (from asteroid/ISS overlay) closes the overlay and appends a **new** question bubble with the fixed question text, then a new answer with a new chip. Nothing is refreshed or stacked in place.
- "Show more" (archive overlay) changes the existing Archive chip's label count; it adds **no** new bubble and shows **no** thinking indicator in the thread.
- Each question is answered on its own; the screen keeps the history visually.
- **No usage limit (Decided by Furkan, Nov 3 2026):** the server is stateless and answers every request it receives, so there is no "limit reached" message. A request that is refused for any reason is a "Failed request".
- **Reload (Default):** the conversation comes back as it was; if an overlay was open it reopens on the same picture, circle or dot; if a question was still pending it returns to the input box to be sent again (architecture note: question restored in the input) and its bubble is marked "Not answered".
- **Window resized across the 900 px breakpoint (Default):** the layout switches between desktop and phone; whatever is open and selected stays open and selected.
- **Browser Back button:** see `docs/ui/00-shared/ui-conventions.md`, section 8.

## Accessibility
- Thread is a list/log region; new answers and failure messages are announced politely (**Default** `aria-live="polite"` on the thread).
- All chips and the About link are real buttons/links with visible focus (amber ring). Icons are `aria-hidden`.
- The 300-character hint is read through `aria-describedby` on the field and announced politely; the counter is not a live region.
- The "Not answered" mark is text, not colour alone.

## Open items
- Final example-chip texts (landing); tune the long-wait text and the 8-second threshold after tests.
- Whether a "new answer ready" cue is needed when an answer arrives behind an open layer.
