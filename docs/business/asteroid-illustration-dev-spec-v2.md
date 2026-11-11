# Asteroid Illustration — Development Spec v2 (scatter layout)

Status: Approved direction from the UI design work (November 2026), ready to implement. It follows an earlier wave-and-lane design (v1), which is not included in this repository.

What changed from v1, in one paragraph: v1 laid asteroids along a decorative sine wave and pushed crowded ones into "lanes" with connector curves. v2 drops the wave, the lanes and the connectors. Horizontal position still comes from distance (same log scale, same ruler). Vertical position is spread out inside a fixed-height band, deterministically from each asteroid's name, and a collision step keeps circles and name labels from touching. Tiers, colours, the ruler, the fixed-size canvas and the hover/tap behaviour carry over, with the changes listed in section 10.

This document is about *how the illustration is drawn and behaves*. Product-level decisions (data sources, what can be asked) stay in the UX PRD. The matching mockups are the canvas boards "Asteroid entry — desktop, detail panel open", "Asteroid entry — phone, detail panel open" and "Asteroid illustration — scatter layout, busy weeks" in the design canvas.

## 1. What the illustration shows

One asteroid answer = one illustration holding every near-Earth asteroid in the current rolling 7-day window. Earth is drawn at the left. Each asteroid is a circle placed left to right by its closest-approach distance, with a name label next to it.

Explicitly **not** to scale or meaningful:
- Earth's size, the asteroid sizes and the distance axis are each scaled independently.
- **Vertical position carries no meaning.** Asteroids are spread out only so that every one stays visible and tappable.

Honesty text shown to the user (shortened from v1, full text on the About screen):
> "Illustrative only: distance is drawn on a compressed scale, and sizes and Earth are not drawn to a common scale. Height has no meaning: asteroids are spread out only so that every one stays visible. Tap a circle for details."

## 2. Input data per asteroid

- `name` — display name as returned by the source (for example "(2019 SG8)" or "376848 (2001 RY47)").
- `ld` — closest approach in lunar distances (`miss_distance_km / 384400`). Kilometres are never shown.
- `diameter_min_m`, `diameter_max_m` — estimated diameter range in metres.
- `hazard` — boolean, potentially-hazardous flag.
- **`date` — date of closest approach (new in v2).** Shown in the detail panel as "Passes Wed 4 Nov". The data source returns it; it was missing from the v1 field list.

Everything else (tier, radius, pixel position, label position) is derived.

## 3. Horizontal position: log-scale distance (unchanged from v1)

```
lo = smallest ld in the window, hi = largest ld in the window
pos = (log10(ld) - log10(lo)) / (log10(hi) - log10(lo))      // 0..1
x   = pos * LINE_PX                                           // LINE_PX = 1500
screen_x = MARGIN_L + x                                       // MARGIN_L = 530
```

**Degenerate case (explicit branch, no epsilon):** if `hi == lo` (one asteroid, or all identical distances), set `pos = 0.5` for every asteroid and draw no ruler ticks. A tie inside a varied set is ordinary: tied asteroids get the same `screen_x` and are separated vertically by section 6.

Horizontal position is **never** moved by the collision step.

## 4. Size tiers and colours (unchanged from v1)

Size uses the midpoint of `diameter_min_m` and `diameter_max_m`:

| Tier | Midpoint | Circle radius (px) |
|---|---|---|
| car-sized | under 30 m | 5 |
| bus-sized | 30 m to under 80 m | 7 |
| house-sized | 80 m to under 200 m | 10 |
| stadium-sized | 200 m to under 500 m | 14 |
| skyscraper-sized | 500 m or more | 19 |

Colour comes from `hazard`:
- Not hazardous: fill `#2FAE6B`, edge `#6FE3A4`.
- Potentially hazardous: fill `#E5484D`, edge `#FF9598`, **plus an outer ring** (radius + 4, stroke `#E5484D` at 75 % opacity, width 2) so the difference does not rely on red versus green alone.
- Selected (panel open): white ring, width 2.5, at radius + 6 (radius + 9 for hazardous, outside the hazard ring).

**Visual radius** `vr = radius + 4` for hazardous, `radius` otherwise. All collision maths in section 6 uses `vr`.

Wording note: "potentially hazardous" is NASA's classification based on size and orbit. The legend must say it does not mean an impact is expected.

## 5. Canvas layout (fixed size, replaces v1 section 8)

All values are CSS pixels. The drawing never shrinks to fit its container.

```
LINE_PX  = 1500        // length of the distance line
EARTH_R  = 220
MARGIN_L = EARTH_R*2 + 90   = 530
MARGIN_R = 60
BAND     = 520         // height of the area asteroids are spread over
TOP      = 30          // space above the band
MARGIN_Y = 44          // asteroids stay this far from the band's top and bottom edge

width   W = MARGIN_L + LINE_PX + MARGIN_R              = 2090
earthCx   = EARTH_R + 40                               = 260
earthCy   = TOP + BAND/2                               = 290
rulerY    = TOP + BAND + 34                            = 584
height  H = rulerY + 64                                = 648
```

**Height no longer depends on how many asteroids there are** (in v1 it grew with the number of lanes). A busy week is denser, not taller. Earth (diameter 440) fits inside the band height.

Decorative elements, none carrying data: a faint star field (seeded, about 120 small dots), Earth with a soft atmosphere ring and two faint grid ellipses, the label "Earth" at its centre, and faint dotted vertical guide lines running from each ruler tick up to the top of the band (stroke `rgba(255,255,255,0.07)`, dash 3 6).

## 6. Vertical position and collision handling (replaces v1 sections 5 to 7)

### 6.1 Labels

- Text: the name, cut to 15 characters followed by "…" if longer (the v3 demo cut at 16; either is fine, pick one and keep it). The detail panel always shows the full name.
- Font 12 px, weight 500 (600 for the selected asteroid), colour `#E3E7F0` (`#FFFFFF` selected), centred on the circle.
- Width estimate for placement: `6.5 px × characters`. A real implementation should measure the rendered text instead.
- **Above** position: baseline at `y - vr - 6`. **Below** position: baseline at `y + vr + 16`.
- Label rectangle for collision tests: from `baseline - 10` to `baseline + 3`, and `x ± width/2`.

### 6.2 What "colliding" means

Two things collide when any of these is true:
- Circle against circle: the distance between centres is less than `vr_a + vr_b + CGAP`, with `CGAP = 8`.
- Label against label: the rectangles come closer than 3 px.
- Label against circle: a label rectangle comes closer than 1 px to any other asteroid's circle (visual radius).

### 6.3 Placement (deterministic)

Process asteroids sorted by `x` ascending. Keep a list of placed asteroids.

1. **Random heights, seeded by name.** Create a pseudo-random generator seeded from the asteroid's name (for example a CRC32 of the name). Try up to `TRIES = 80` heights drawn uniformly from `[TOP + MARGIN_Y, TOP + BAND - MARGIN_Y]`. At each height try the label **above**, then **below**. Take the first combination with no collision.
2. **Grid scan.** If step 1 fails, scan heights from the top of that range to the bottom in 6 px steps, again above then below, taking the first free combination.
3. **Nudge neighbours (repair).** If step 2 fails, scan the heights again (label below first, then above). At each height, find which placed asteroids block it. If one or two do, try to move each of them up or down by 6, 12, … up to 60 px (alternating down and up), also allowed to flip their own label above/below, to a position that is free of everything else and no longer blocks the new asteroid. If every blocker can move, keep the moves and place the new asteroid there. Otherwise put every blocker back where it was and continue scanning.
4. **Accept an overlap.** If nothing works, place the asteroid at the vertical centre of the band with its label above, and accept the overlap. Labels are never hidden.

Because the generator is seeded by name, **an asteroid ends up in the same place every time the same week is drawn**, including when an old answer is reopened. (Neighbour nudges are also deterministic because the order and the rules are fixed.) The exact random-number algorithm is the implementer's choice; positions only need to be stable, not identical to the mockups.

### 6.4 Why this replaces the lanes

v1's lane step checked spacing only along the line, so circles in neighbouring lanes could still touch on sloped parts of the wave (the illustration spike measured one 8.4 px circle overlap in a 60-asteroid week), and it said nothing about labels. v2 checks real final positions for circles *and* labels, and vertical room is fixed, not growing.

## 7. Distance ruler (same idea as v1 section 11)

A horizontal line at `rulerY` from `MARGIN_L` to `MARGIN_L + LINE_PX`, drawn at the bottom of the canvas. Tick marks (6 px above and below the line) at 5, 10, 20, 50, 100 and 200 lunar distances, placed with the same log formula as section 3. Ticks outside `[lo, hi]` are omitted (the open question from the spike about drawing 5 LD at −1 px stays open: this spec chooses the strict reading). Tick numbers 12 px below the line, caption "Rough distance guide (lunar distances)" under it. No ticks when `hi == lo`. Ticks are rounded reference points, not per-asteroid values.

## 8. Interaction and screen behaviour

### 8.1 Frame and scrolling
- **Desktop:** the drawing sits in the left frame of the answer overlay (about 1,000 px wide on a 1,440 px window, right column 400 px). It is dragged or scrolled sideways (drag, trackpad, scrollbar). If the frame is shorter than 648 px it also scrolls vertically.
- **Phone:** the frame is about 460 px tall, full width, and can be dragged in both directions. The text and legend sit below it and scroll with the page; the page scrolls when the touch starts outside the frame. The docked panel (8.3) covers the lower part of the frame.
- **Opening position:** scrolled so the edge of Earth and the closest asteroids are visible. The mockups use a sideways offset of 200 px on desktop and 400 px on phone; the vertical offset on phone puts the selected asteroid in the upper part of the frame, above the docked panel. Intent: show Earth's limb plus the nearest asteroids first, do not open on a view that is mostly Earth.
- **Cues:** soft fading edges (70 and 90 px on desktop, 30 and 40 px on phone), a "Drag to explore" pill that disappears after the first scroll, and thin scroll-position bars (horizontal, plus vertical on phone).

### 8.2 Tap targets
Visible circles keep their tier size. Each has an invisible button over it: **32 px on desktop, 44 px on phone**, with an `aria-label` such as "Asteroid (2019 SG8), potentially hazardous, closest approach Wed 4 Nov".

### 8.3 Detail panel
Hover (desktop) or tap (phone) opens it; click/tap pins it. Opening another closes the first; tapping the background closes it. Contents:
1. Hazard tag: "Potentially hazardous" (text `#FF9598` on `rgba(229,72,77,0.25)`) or "Not hazardous" (text `#6FE3A4` on `rgba(47,174,107,0.25)`).
2. Full name (15 px, weight 600).
3. "Passes Wed 4 Nov" (new in v2).
4. "Closest approach: X lunar distances" (one decimal under 10, whole number from 10 up).
5. "Estimated size: min–max m (tier name)".

Panel background `#3A1A1C` with a red-tinted border for hazardous, `#163325` with a green-tinted border for not hazardous.

- **Desktop:** floats above the circle and its label (about 252 px wide), with a small pointer, flipping below the circle if there is no room above.
- **Phone:** docked at the bottom of the frame (12 px side margins, 20 px from the bottom) so a finger never covers it and it never clips at an edge.

## 9. Rest of the screen

Right column on desktop, below the frame on phone:
- Question line and close button; title "Near-Earth asteroids"; subtitle "2–9 Nov · 22 asteroids" (window dates and count).
- Agent explanation (two or three sentences, using only numbers in the illustration).
- Legend: not hazardous / potentially hazardous, five size groups drawn at their true circle sizes with their ranges ("Circle sizes are groups, not exact sizes").
- The hazard-wording note and the shortened honesty text from section 1.
- Outlined "Ask again" button, same behaviour as on the ISS entry (closes the overlay and sends the question again as a new message). **No stale-snapshot warning**: the window dates in the subtitle already say which week it was.

## 10. What carries over from v1 and what does not

| v1 part | v2 |
|---|---|
| §2 input data | kept, plus `date` |
| §3 log-scale position and zero-spread fallback | kept unchanged |
| §4 tiers and colours | kept; hazardous ring and selected ring added |
| §5 wave, §6 lane packing, §7 perpendicular offset and connectors | **removed**, replaced by section 6 here |
| §8 canvas sizing (grows with lanes) | **replaced** by fixed band (section 5 here) |
| §9 fixed-size canvas inside a scrolling container | kept in spirit; scrolling rules in 8.1 |
| §10 hover/tap behaviour | kept; panel content gains the date; phone panel docks |
| §11 ruler | kept; guide lines added |
| Footer copy | shortened, full text on About |

## 11. What was measured, and what was not

Measured in a Python prototype of this algorithm on **made-up** asteroids with real-style names (names up to 18 characters, 22 to 60 asteroids per week):

| Sample week | Circle overlaps | Label overlaps | Labels touching a circle | Labels moved below | Could not be placed |
|---|---|---|---|---|---|
| 22 asteroids (desktop and phone mockups) | 0 | 0 | 0 | 1 | 0 |
| 40 asteroids | 0 | 0 | 0 | 6 | 0 |
| 60 asteroids | 0 | 0 | 0 | 10 | 0 |

Before step 3 (nudging neighbours) existed, the 40-asteroid week left one asteroid unplaced inside a dense cluster of 14 asteroids within about 130 px; step 3 resolved it. For comparison, the v1 lane approach with the same labels left 3 overlapping label pairs and 11 labels on circles in the 40-asteroid week and needed a 674 px canvas, and a variant that placed by real positions without the band needed 950 px.

**Not yet done:** the real 35-asteroid week from the v3 demo and the spike has not been run through this algorithm, and no week with a much denser cluster has been tried. Overlap is still possible in an extreme cluster; it is accepted and nothing is hidden.

## 12. Open items

- Confirm the label cut-off (15 characters plus "…" in this spec, 16 in the v3 demo).
- Decide whether to measure label text for real or keep the 6.5 px per character estimate.
- Tick slack at the line ends (strict omit here; the demo drew ticks up to 15 px outside).
- Empty week (no asteroids): the algorithm and the screen are not specified; needs a plain message instead of an illustration.
- Exact opening scroll position rule (mockup values above) once real sizes are known.
- Run the real sample week and two or three more real weeks through section 6 before implementation.
- Update the UX PRD wording: date in the panel, scatter layout, height has no meaning.
