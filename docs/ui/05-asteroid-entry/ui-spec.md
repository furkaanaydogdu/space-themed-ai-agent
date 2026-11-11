# Asteroid entry overlay — UI spec

Boards (save screenshots here):
- **"Asteroid entry — desktop, detail panel open"** (`AsteroidDesktop`)
- **"Asteroid entry — phone, detail panel open"** (`AsteroidPhone`)
- **"Asteroid illustration — scatter layout, busy weeks (40 and 60 asteroids)"** (`AsteroidBusy`, a stress test, not a screen)

The **drawing itself** (scale, placement algorithm, label rules, tiers, colours) is specified in `docs/business/asteroid-illustration-dev-spec-v2.md`. This file specifies the **screen around it**.

Shared values and overlay frame: `docs/ui/00-shared/ui-conventions.md`. Marks: **Decided**, **Default**, **Open**.

## Purpose
Shows every near-Earth asteroid passing in the 7-day window in one drag-to-explore illustration, with Earth on the left. Opens from the `Asteroids · 2–9 Nov` chip or automatically if it is the first kind in the answer.

## Layout
- **Desktop**: illustration frame left (fills available space), **400 px text column right**. **Phone** (and windows < ~900 px): header, illustration frame on top (**about 460 px high**), docked detail panel at the bottom of the frame, then the text column.
- The illustration canvas is **2090×648** regardless of asteroid count; the frame shows part of it and the user **drags** (or scrolls) horizontally to see the rest. Opening scroll offsets in the mockups: 200 px desktop, 400 px phone (Default: start with Earth and the nearest asteroids visible).
- Cues that more is off-screen (**Decided**): a **"Drag to explore" pill** in the frame, **fading edges**, and visible scroll bars.

## Illustration (summary of v2 spec)
- Earth at the left (radius 220, centre x 260). **Distance runs left to right on a log scale**; ruler at the bottom with ticks at 5, 10, 20, 50, 100, 200 lunar distances and faint dotted guide lines rising from the ticks.
- Height has no meaning; asteroids are spread vertically inside a 520 px band by a seeded layout so positions are the same on every visit and every label stays visible.
- Circles by size tier: car 5, bus 7, house 10, stadium 14, skyscraper 19 px radius. **Green `#2FAE6B` = not hazardous, red `#E5484D` = potentially hazardous with an extra ring** (radius + 4). Selected circle: white ring.
- Labels above the circle (below if they collide), cut at 15 characters plus "…". Tap/hit areas 32 px desktop, **44 px phone**.
- In a crowded week some circles may overlap but **none is hidden**.

## Detail panel (Decided)
Opens on hover (desktop) or click/tap, one at a time.
- Contents: **hazard tag** ("Potentially hazardous" / "Not hazardous"), **full name** (e.g. "(2019 SG8)"), **"Passes Wed 4 Nov"** (date of closest approach), **"Closest approach: X lunar distances"**, **"Estimated size: min–max m (tier name)"**.
- **Desktop**: floats above the selected circle. **Phone**: **docked at the bottom of the frame**.
- The mockups show the panel open on a hazardous asteroid "(2019 SG8)" (desktop) and "(2025 BQ1)" (phone).
- Closes on tapping empty space, another circle replaces it, Esc closes (**Default**).

## Text column
Top to bottom (header row first: "Your question" + question + 44 px close):
1. **Title** "Near-Earth asteroids" (Sora 26 / 22).
2. **Window line**: **"2–9 Nov · 22 asteroids"** (window dates and count).
3. **Agent explanation** — short, plain, 2–4 sentences, written by the agent (placeholder on boards).
4. **Legend**: green dot "Not hazardous", red dot with ring "Potentially hazardous", then the **five size groups with ranges** (car, bus, house, stadium, skyscraper) and the line **"Circle sizes are groups, not exact sizes."**
5. **Hazard note**: "'Potentially hazardous' is NASA's label for asteroids of a certain size whose orbits pass close to Earth's. It doesn't mean an impact is expected."
6. **Illustrative note**: "Illustrative only: distance is drawn on a compressed scale, and sizes and Earth are not drawn to a common scale. Height has no meaning: asteroids are spread out only so that every one stays visible. Tap a circle for details."
7. Footer: **"Ask again"** — **outlined** secondary button, 44 px min.

## "Ask again" (Decided)
Closes the overlay and sends the asteroid example question as a new message; new chip; nothing refreshed in place. **There is no stale warning** on this overlay because the window dates are always shown. The question text is, by assumption, the asteroid example chip on the landing ("Which asteroids are passing Earth this week?") — **Open, confirm**.

## States
- **Empty week**: no overlay and no chip; the conversation shows a fixed sentence (see `02-conversation`). Nothing to draw here.
- **One asteroid / all at the same distance / very busy week (40–60)**: must render readably; stress test is the `AsteroidBusy` board.
- Reopened later: shows the window and data as of the original question.

## Accessibility
- Circles are buttons in Tab order (left to right by distance); `aria-label` carries the same facts as the detail panel (hazard, name, date, distance, size). A text list alternative (**Default**, not drawn): the explanation and legend carry the meaning; a sortable list is out of scope for v1 (**Open**).
- Hazard is shown by colour **and** ring **and** the panel's tag text.
- Dragging must also work with keyboard (scroll container focusable, arrow keys scroll) and with trackpad/wheel.

## Open items
- Ask-again question text, list alternative for screen readers, opening scroll position rule.
