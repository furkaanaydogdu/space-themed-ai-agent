# ISS Illustration — Development Spec v1

Status: written from the UI design work (4 November 2026), ready to implement. It sits beside `asteroid-illustration-dev-spec-v2.md` and plays the same role for the ISS overlay: it says **how the illustration is computed and drawn**. What the screen looks like around it (text column, facts rows, warning box, "Ask again") stays in `docs/ui/04-iss-entry/ui-spec.md`. Product-level decisions stay in the UX PRD (section 7.4).

The matching mockups are the canvas boards "ISS entry — desktop, fresh snapshot", "ISS entry — phone, fresh snapshot", and the two "old snapshot" boards. **The boards draw the dots at hard-coded positions with made-up sample numbers; this spec decides where the dots really go.** If a board and this spec disagree, this spec wins.

Decisions by Furkan on 4 November 2026 (all marked **Decided** below): the ISS service gives the day/night flag for every future point; the caption gets no extra sentence about uneven spacing; the "Now" marker reads "Then" on old snapshots; the wording "about 1,000× farther than the ISS" stays; the check for dots or labels landing on the Moon's dashed line is postponed until real data is available.

## 1. What the illustration shows

One ISS answer = one illustration of the ISS's position at the moment of the question and where it will be at each 10 minutes up to +90 minutes. Earth is a circle in the middle, a dotted ring around it is the orbit, the ISS ("Now") sits at the **top** of the ring, and 9 more dots follow the ring **clockwise**.

Explicitly **not** to scale or meaningful (the caption says "Orbit height is exaggerated"):
- **Orbit height.** The ring is drawn at 1.67 × Earth's radius (250 / 150); the real orbit is about 1.07 ×.
- **The Moon.** Drawn small and near, with a broken line to show it is far away. The label says "about 1,000× farther than the ISS" (**Decided**: kept as is, although the real ratio is about 900×: 384,400 km against about 420 km of altitude).
- **Angles.** A dot's angle on the ring is **how far the ISS has moved eastwards over the ground since the snapshot** (section 3). It is not the time and not the position along the real orbit. Dots are therefore **not evenly spaced** (see section 3.3), and that is correct. The caption does **not** mention this (**Decided**).
- **Earth's markings.** The two faint ellipses on Earth are decoration. No continents are drawn and Earth does not turn to match the real longitude.

## 2. Input data

One request returns 10 points, at the snapshot time and every 10 minutes after it (the service allows exactly 10 timestamps per call):

| Field | Meaning |
|---|---|
| `k` | index 0 to 9; the offset is `10 × k` minutes |
| `timestamp` | the moment of the point (shown as local 24-hour time, "16:22") |
| `lat` | latitude in degrees, north positive (the ISS stays within about ±51.6°) |
| `lon` | longitude in degrees, east positive, **normalised to −180…180** (if the source gives 0…360, normalise first with `lon = ((lon + 180) mod 360) − 180`) |
| `daylight` | true if the ISS is in sunlight at that point, false if in Earth's shadow |

Also from point 0 only: `altitude_km`, `speed_kmh` (shown in the facts rows, not drawn).

**Day/night flag (Decided):** the ISS service returns the day/night flag for every one of the 10 points, including the future ones (Furkan checked this on 4 November 2026). The illustration uses it as given and does not calculate it.

Everything else (angle, pixel position, label position) is derived.

## 3. Where each dot goes: the angle rule

### 3.1 The rule

Place point `k` on the orbit ring at angle `θ_k`, measured **clockwise from straight up**:

```
θ_0 = 0                                   // "Now" is always at the top
for k = 1..9:
    d = lon_k - lon_(k-1)                 // change since the previous point
    if d < -180: d = d + 360              // the ISS crossed the 180° line eastwards
    if d >  180: d = d - 360              // (only possible with bad data; keeps the path continuous)
    θ_k = θ_(k-1) + d
x = cx + R * sin(θ_k in radians)
y = cy - R * cos(θ_k in radians)
```

- It is the **change between consecutive points**, summed up. Do **not** use `lon_k - lon_0` directly and do **not** use the raw longitude.
- `θ` is never wrapped back into 0…360: it simply grows to about 330°. Only the sine and cosine are taken.
- The ISS always moves **east** (longitude increases), so with correct data every `d` is positive.

### 3.2 Why the fix is needed, and how often

The ISS covers about 326° of longitude in 90 minutes, so the path crosses the ±180° line in **most** snapshots (86 % in the simulation below), not rarely. Without the fix, a point that crosses the line jumps from about +170° to about −148°, so its "change" is about −318° and the dot flies to the wrong side of the ring.

Example (start longitude 170° E, simulated, section 6):

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| raw `lon` | 170.0 | −147.7 | −92.4 | −60.1 | −37.9 | −9.3 | 42.3 | 90.2 | 116.6 | 139.3 |
| `lon_k − lon_0` (wrong) | 0 | −317.7 | −262.4 | −230.1 | −207.9 | −179.3 | −127.7 | −79.8 | −53.4 | −30.7 |
| `θ_k` with the fix (right) | 0 | 42.3 | 97.6 | 129.9 | 152.1 | 180.7 | 232.3 | 280.2 | 306.6 | 329.3 |

In the simulation the naive version produced a broken (non-increasing) path for 824 of 960 start positions (86 %); the fixed rule for none.

### 3.3 What to expect (so it is not mistaken for a bug)

Simulated over 960 start positions (section 6):
- The step between two dots is **22° to 57°**, never constant: the ground track moves faster in longitude near the northern and southern ends of the orbit. This is why the dots are unevenly spaced on the ring.
- The last dot (+90) lands at **321° to 331°**. The **gap** between it and "Now" is therefore **29° to 39°**, always open. This is the deliberate gap in the drawing.
- Because the smallest step is 22°, neighbouring dots are never closer than about **97 px** (desktop, R = 250) or **46 px** (phone, R = 118) along the ring. This is why 44 px phone hit areas never overlap.

### 3.4 Guard for bad data

After the fix, expect every `d` to be between about 15° and 65°. If any `d` is ≤ 0° or ≥ 120° (should not happen with real data), do not draw a wrong picture: use **equal steps of 36°** for the angles (the facts and panel texts still use the real data) and log the problem. **Default.**

### 3.5 What the texts show

The dot panel, the aria-labels and the facts rows always use the **real, normalised longitude** (−180…180), never `θ`. See 7.2.

## 4. Stage geometry

The illustration is a fixed-size **stage**, scaled down uniformly if the frame is smaller (never scaled up, **Default**). Values are CSS pixels from the boards.

| | Desktop stage | Phone stage |
|---|---|---|
| Size | 760 × 760 | 390 × 380 (fills the frame width; frame 380 high) |
| Earth centre (cx, cy) | (380, 400) | (195, 196) |
| Earth radius | 150 | 66 |
| Atmosphere ring | r 158, stroke 6, `rgba(170,210,255,0.28)` | r 72, stroke 4, same colour |
| Orbit ring radius **R** | 250, dotted (`2 7`), `rgba(255,255,255,0.22)`, width 1.5 | 118, dotted (`2 6`), same |
| Earth fill | radial gradient: day `#6AA1E8 → #1B4A94`, night `#34609F → #0F2850` (centre 38 % / 32 %, radius 80 %) | same colours |
| Earth decoration | two ellipses, `rgba(255,255,255,0.2)`, width 1: 150 × 42 and 62 × 150 | 66 × 18 and 27 × 66 |
| "Now" marker | 34 px circle, amber fill, 3 px white border, satellite icon 18 px; hit area 44 px | 28 px circle, same style, icon 14 px; hit area 44 px |
| Dots (+10 … +90) | 20 px visible, 2 px border; hit area **32 px** | 16 px visible; hit area **44 px** (the boards show 36; this spec wins) |
| Label distance from the ring | labels centred on the same angle at **R + 38** (288) | **R + 27** (145) |
| Label text | "Now" (600, white) and "+10 min" … "+90 min" (500, `#E3E7F0`), 13 px | "Now", "+10" … "+90", 12 px |

On an **old snapshot** the "Now" label and marker read **"Then"** (see 7.3); everything else in the table is unchanged.

Day and night colours: day dot fill `#F2B66B`, border `#FFE3B8`; night dot fill `#142044`, border `#8FB0FF`. The selected dot gets a white ring (3 px, spread). The backdrop behind the stage is set by the **"Now" point's** `daylight` flag: day = radial gradient `#2F5FA5 → #1B3C70 (45 %) → #0D1A38`; night = `#060A16` with about 60 small star dots at fixed (seeded) positions, so the picture is identical every time it is drawn.

Drawing order, bottom to top: backdrop, stars (night), Moon connector and Moon, orbit ring, Earth and atmosphere, path arc, direction arrow, labels, dots, "Now" marker, panel.

## 5. Path arc, arrow and Moon

### 5.1 Path arc
An amber arc (`#F2B66B`, width 2.5, opacity 0.9, round caps) along the orbit ring from `θ_0 = 0` clockwise to `θ_9`. Because `θ_9` is above 180°, the SVG arc uses the large-arc flag = 1. The arc **stops at the last dot**; it is never joined to "Now" (that is the gap, section 3.3).

### 5.2 Direction arrow
A small filled triangle (amber), pointing clockwise along the tangent, placed on the arc at the **middle of the first segment** (`θ_1 / 2`). The boards show it at about 14°. Middle of the first segment keeps it clear of both the "Now" marker and the +10 dot, even for the smallest step.

### 5.3 Moon (decoration, not data)
Fixed position, up and to the right, the same on every snapshot:
- **Desktop:** Moon circle centre (690, 80), radius 28, fill `#D5D8E2`, three darker craters (`#AEB2C0`: (680,72) r5, (699,92) r7, (696,66) r3). Label top right: "**Moon**" (600) and "about 1,000× farther than the ISS" (13 px, `#E3E7F0`), right-aligned.
- **Phone:** centre (350, 34), radius 14, two craters; label at the top right as one block "Moon · about 1,000×" / "farther than the ISS" (11 px).
- A **dashed line** (`#C9CFDD`, width 2, dash 6 6 on desktop, 5 5 on phone) runs from the orbit ring at about 40° towards the Moon, with a **break mark** (two short parallel slashes) in the middle, meaning "the real distance is much longer". Desktop coordinates: segment 1 from (541, 208.5) to (600, 157), break marks around (596–613, 144–161), segment 2 from (609, 149.5) to (668, 98). Phone: (270.8, 105.6) to (297, 83), then (311, 70) to (338, 45).
- **Collision (postponed, Decided 4 Nov 2026).** Because dot angles depend on the data, a dot or its label can sit on the Moon line (the line leaves the ring around 40°). Furkan will check this with real data later; no extra rule is added now. The build starts with the **Default** treatment: the line is drawn **under** the dots and labels, and every label has a 4 px halo in the backdrop colour (`paint-order: stroke`) so text stays readable.

## 6. What was measured, and what was not

Measured with a simple Python simulation: a circular orbit with 51.6° inclination, a 92.68-minute period, the Earth turning 360° per 1,436 minutes, 10 points at 10-minute steps, **960 starts** = 24 start phases (every 15° of orbit) × 40 start longitudes (every 10° from −180° to 170°, plus 178°, −178°, 179.9° and −179.9°):

| Check | Result |
|---|---|
| Step between consecutive dots after the fix | 22.2° to 56.7° |
| `θ_9` (last dot) | 321.0° to 330.9° |
| Gap between the last dot and "Now" | 29.1° to 39.0° |
| Starts where the naive "lon_k − lon_0" gives a non-increasing path | 824 of 960 (86 %) |
| Starts where the fixed rule gives a non-increasing path | 0 |

**Not done:** no real ISS-service data was run through the rule; the simulation ignores the real orbit's small eccentricity, drag and the exact timestamps. The real gap may differ by a degree or two. The boards' sample numbers are not one consistent dataset (for example "Position now 12° N, 150° W" while the +30 min dot says "112° E"); do not use them as test data.

## 7. Interaction and text

### 7.1 Selecting a dot
Hover (desktop) or tap/click opens the panel for one dot at a time; opening another closes the first; clicking or tapping the background, or pressing Esc, closes it. The "Now" marker is also a dot with a panel ("Now · 15:52"). Dots are real buttons in Tab order from "Now" to +90; Enter or Space opens the panel. Selected dot: white ring.

### 7.2 Panel content and formatting
- Line 1: relative time and actual time: "+30 min · 16:22" ("Now · 15:52" for k = 0). Time is local 24-hour.
- Line 2: position: "24° N, 112° E". Rounded to whole degrees; hemisphere letters from the sign of the **real** value (negative latitude = S, negative longitude = W). Longitude is the normalised −180…180 value, never `θ`. A value that rounds to 0 keeps the letter of its unrounded sign.
- Line 3: sun icon and "In daylight" or moon icon and "In darkness" (colour is never the only signal).
- aria-label of each dot: "Plus 30 minutes, 16:22, 24 degrees north, 112 degrees east, in daylight"; for the marker "Now, 15:52, …".
- **Desktop panel:** 215 px wide, floats just below and to the right of the dot (the board shows it about 41 px under the dot centre and 62 px left of the dot's left edge); if it would leave the frame it flips above and is clamped inside the frame (**Default**). **Phone panel:** 160 px wide, same rule (the board shows it at (215, 160)); it must never cover the selected dot (**Default**).

### 7.3 Old snapshots
The stage is drawn exactly the same from the stored data: backdrop and Earth colours follow the stored `daylight` of point 0, and the caption changes to "was predicted to be". Nothing is refreshed in place.

**"Then" instead of "Now" (Decided 4 Nov 2026):** on an old snapshot the marker's label under the ring reads **"Then"**. Its panel's first line reads "Then · 09:14" (time of the snapshot), and its aria-label starts "Then, 09:14, …". The other dots keep "+10 min … +90 min" (minutes after the snapshot). The panel and aria wording for the marker follows from the decision and is a **Default**.

### 7.4 When a snapshot counts as old
Same threshold as the UI spec: older than about 10 minutes. The marker label is decided once when the overlay opens; it does not flip while the overlay stays open (**Default**).

## 8. Test scenarios (from `docs/business/test-plan.md`, area 4)

1. Start longitude 170° (crossing the line). Expect the table in 3.2: a smooth path, `θ_9` about 329°, a gap of about 31°, every dot on its correct side of the ring, and panel longitudes like "148° W", never a value above 180.
2. Start near +178° and near −178° (crossing right at the start), and start near −180° and +180° exactly.
3. Start near 0° (no crossing in the first half of the path).
4. Start at the northern and southern extremes of the latitude (smallest and largest steps), checking labels do not touch.
5. All 10 points in daylight; all in darkness; day then night (backdrop follows point 0 only).
6. Bad-data guard (3.4): feed a repeated longitude or a decreasing one and confirm equal 36° steps and no crash.
7. Phone width 375 px: stage scaled, all 10 dots reachable with 44 px targets, panel readable.
8. Panel for the dot closest to the Moon line (section 5.3) is readable (to be checked with real data).
9. Old snapshot (more than 10 minutes old): the marker reads "Then", its panel and aria-label say "Then", the other dots still say "+10 min …", and the caption says "was predicted to be".

## 9. Open items

- Panel placement details on the phone (the Default in 7.2) and the Moon-line collision (5.3), once real data is available.

Resolved 4 Nov 2026: source of the per-point day/night flag (the service gives it); no caption sentence about uneven spacing; "Then" on old snapshots; "about 1,000×" wording kept.
