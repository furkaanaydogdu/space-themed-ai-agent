# ISS entry overlay — UI spec

Boards (save screenshots here):
- **"ISS entry — desktop, fresh snapshot"** (`IssDesktop`)
- **"ISS entry — desktop, old snapshot (reopened later)"** (`IssDesktopStale`)
- **"ISS entry — phone, fresh snapshot"** (`IssPhone`)
- **"ISS entry — phone, old snapshot (reopened later)"** (`IssPhoneStale`)

Shared values and the overlay frame: `docs/ui/00-shared/ui-conventions.md`. Marks: **Decided**, **Default**, **Open**.

**How the illustration is computed and drawn (dot angles, the ±180° longitude fix, geometry, Moon, panel rules, test scenarios): `docs/business/iss-illustration-dev-spec.md`.** This spec covers the screen around it. Board status (Nov 4 2026): the boards draw the dots at hard-coded positions with sample numbers that are not one consistent dataset ("Position now 12° N, 150° W" vs the +30 min dot "112° E"), the phone boards show 36 px dot hit areas where the spec says 44 px, and the old-snapshot boards still label the marker "Now" where the decision is "Then". The dev spec and this spec win over the boards.

## Purpose
Shows where the International Space Station was **at the moment of the question** and where it will be over the next **90 minutes** (a dot every 10 minutes), with the Moon drawn for scale. Opens from an ISS chip (`ISS · 09:14`) or automatically when ISS is the first kind in an answer.

## Layout
Same overlay frame as the archive overlay: **desktop** = illustration frame left, **400 px text column right**; **phone** (and windows < ~900 px) = header, illustration frame on top (about 380 px high), text below, footer button.

## Illustration frame
(Exact geometry and rules: `docs/business/iss-illustration-dev-spec.md`.)
- **Backdrop** depends on whether the ISS is in daylight at the snapshot moment (**Decided**):
  - Day: radial gradient `#2F5FA5 → #1B3C70 (45 %) → #0D1A38` centred (phone centred at 50 % / 52 %).
  - Night: dark `#060A16` with small star-like dots.
- **Stage** (desktop 760×760, scaled to fit the frame; phone fills the frame width):
  - **Earth** as a circle in the middle, with a dotted **orbit ring** around it. **Orbit height is exaggerated** (stated in the caption).
  - **Path**: an amber arc along the orbit for the next 90 minutes, with a **direction arrow**. The gap at the end of the arc is deliberate (the ISS does not return to exactly the same spot after 90 minutes); it is always between about 29° and 39° wide.
  - **Dot positions (Decided Nov 4 2026):** each dot sits at the angle of how far the ISS has moved eastwards since the snapshot, summed step by step with the ±180° longitude fix. Dots are therefore **not evenly spaced** (22°–57° apart). Details in the dev spec.
  - **"Now" marker**: 34 px circle with a satellite icon at the top of the ring, with a text "Now" (**"Then" on an old snapshot**, Decided Nov 4 2026).
  - **Dots every 10 minutes** (+10 … +90): 20 px visible dots in **32 px hit areas** (44 px on phone). Day dot: amber `#F2B66B` fill, border `#FFE3B8`. Night dot: `#142044` fill, border `#8FB0FF`. Dot labels: desktop "Now, +10 min … +90 min"; **phone "+10 … +90"** with the caption "Numbers are minutes from now." (On an old snapshot this caption reads "Numbers are minutes after the snapshot." — **Default**, follows from the "Then" decision.) Day or night for every dot comes from the ISS service, which gives the flag for all 10 points (**Decided**).
  - **Moon**: drawn small at the top right with a **dashed broken line** from the stage and the label **"Moon"** / **"about 1,000× farther than the ISS"** (**Decided**: wording kept), to give a sense of scale.
  - **Legend** (bottom of frame): amber dot = "In daylight", dark dot with blue ring = "In darkness".
- **Dot panel** (click/tap a dot): small floating panel next to the dot, e.g. **"+30 min · 16:22"**, **"24° N, 112° E"**, **"In daylight"**. Panel shows one dot at a time; tapping elsewhere or pressing Esc closes the panel (**Default**). Time is local 24 h. Hover shows the panel on desktop (**Default**: hover and click both work). The position always shows the real longitude from −180° to 180° (for example "148° W"), never the angle used for drawing.
- Selected dot gets a white ring (**Default**, same as asteroids).

## Text column — fresh snapshot (`IssDesktop`, `IssPhone`)
1. Header row: "Your question" + question + close (44 px).
2. **Title** "International Space Station" (Sora 26 px / 22 px).
3. **Snapshot line**: **"Snapshot from 15:52 · just now"**.
4. **Facts rows** (label left, value right): **Position now** (e.g. "28° N, 94° E", with a place-friendly wording if available — **Open**), **Altitude** (km), **Speed** (km/h), **Right now** ("In daylight" / "In darkness").
5. **Agent explanation** — a short plain explanation written by the agent (2–4 sentences; placeholder text on the boards).
6. **Caption** (**Decided Nov 4 2026**: no extra sentence about uneven dot spacing): "Dots show where the ISS will be every 10 minutes. It circles the Earth about every 90 minutes, and the gap at the end is because it doesn't return to exactly the same spot. Orbit height is exaggerated. Tap a dot for details."
7. Footer: **"Ask again"** — **outlined** secondary button (fresh state).

## Text column — old snapshot (`IssDesktopStale`, `IssPhoneStale`)
Shown when the chip is reopened and the snapshot is **older than about 10 minutes** (Decided).
- Snapshot line shows the age: **"Snapshot from 09:14 · 6 hours ago"**.
- **Amber warning box** under it: **"This snapshot is old, so the ISS has moved since then. Ask again for a new one."**
- Labels change to the past tense: **"Position then"**, **"At that moment"** (instead of "Position now", "Right now").
- The caption says the dots show where the ISS **"was predicted to be"** from that snapshot.
- **"Ask again"** becomes a **filled amber primary button** (it is the main action now).
- The illustration is unchanged (still the old snapshot's data), except that the marker is labelled **"Then"** instead of "Now" (**Decided Nov 4 2026**). Its panel reads "Then · 09:14" and its screen-reader label starts "Then, 09:14, …" (**Default**, follows from the decision). The label is set once when the overlay opens.

## "Ask again" (Decided)
Closes the overlay and sends a fixed question as a **new message**. The new answer gets a **new chip**; the old chip is never refreshed or stacked. The fixed question text is, by assumption, the same as the ISS example chip on the landing ("Where is the ISS right now?") — **Open, confirm**.

## Age labels
- Fresh: **"just now"** for snapshots under about 10 minutes (the point where the warning begins; Decided).
- Older: relative labels such as "6 hours ago". **The full ladder (minutes / hours / days) is Open**; **Default**: "N minutes ago" up to 59, "N hours ago" up to 23, then "yesterday" / "N days ago".

## Accessibility
- The illustration has a text equivalent: the facts rows give the current position, altitude, speed and daylight status; the dot panel's content is also reachable by keyboard (dots are buttons in Tab order, `aria-label` like "Plus 30 minutes, 16:22, 24 degrees north, 112 degrees east, in daylight").
- Day/night is shown by colour **and** legend **and** panel text.
- Reduced motion: no animation is required in this view.

## Open items
- Age-label ladder, the Ask-again question text, place-friendly position wording.
- Whether a dot or its label lands on the Moon's dashed line: to be checked with real data later (Furkan, Nov 4 2026). Until then the dev spec's Default applies (line under the dots, text halo).

Resolved Nov 4 2026: the "Now" marker reads "Then" on old snapshots; no extra caption sentence about uneven spacing; "about 1,000×" wording kept; the day/night flag for every point comes from the ISS service.
