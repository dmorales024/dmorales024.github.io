# Visual direction

Settled 2026-08-27. **Reverses the direction approved in #7** (copper amber on cool paper). Dmitri asked for a TRON-esque treatment instead; the earlier reasoning — that neon is Mondo's identity rather than his — was raised once and overruled. This is the live spec.

Prototype: https://claude.ai/code/artifact/0bd59932-c707-4e69-9e0d-53bbab49c17a

## Palette — "rift"

Committed **single theme, dark only**. No light mode; the design does not survive one.

| Token | Value | Use |
|---|---|---|
| `--neon` | `#FF3DCB` | The only accent. Borders, headings, motif strokes, links. |
| `--alt` | `#38F0FF` | **Status only** — `in progress`. Never decorative. |
| `--ground` | `#08050C` | Page ground. Must be painted explicitly. |
| `--panel` | `#100A16` | Card surface. |
| `--line` | `#FF3DCB33` | Hairlines, dividers. |
| `--ink` / `--ink-soft` | `#DDEAF2` / `#7C93A3` | Body text / secondary. |

Rejected: grid cyan, legacy amber, encom green.

## Type

- **Display — `Orbitron`** (500/700). Card titles, headings, wordmark.
- **Body — `Rajdhani`** (400/600).
- **Labels/status — `IBM Plex Mono`** (400/500), uppercase, letter-spaced.

Rejected: Chakra Petch / Barlow; Michroma / Saira.

## Cards — "ignited edge"

- Border **2px** (`--ew`), at ~50% neon opacity at rest.
- On hover: border goes full neon, outer glow `0 0 34px -6px`, inner glow, lift 3px.
- Image sits at `saturate(.72)` at rest, `saturate(1)` on hover, scale 1.035.
- Status is a mono label with a glowing dot; `in progress` dots pulse in `--alt`.

Rejected: corner brackets, glass panels.

## Backdrop — the motif field

**This is the signature of the site.** Small silhouettes of the project's own item draw themselves across the background, continuously.

**Rules:**

1. **Detail pages only.** The **grid page has no animation at all** — no motif, no canvas, nothing. Verified in the prototype: grid renders 0 silhouettes.
2. **One item per page.** A project's detail page draws **only its own** motif — Rotom's page draws Rotoms. Never a mixture.
3. **Continuous.** It does not end, does not depend on scroll position, and has no completion state. Runs the whole time the reader is on the page.
4. **Drawn, never faded in.** Each instance animates `stroke-dashoffset` from full length to zero — an orthogonal **lead routes in first**, then the silhouette draws from it, so it reads as a trace arriving at a footprint.

**Timings (full motion):** draw 3400ms · hold 4200ms · fade 1500ms · new one every 520ms · **cap 26 concurrent**. Subtle: 2600 / 3600 / 1400 / 950 / cap 15. Off: a static field of 18, no animation.

Placement is random position and random scale (0.10–0.19 of a 1000-unit viewBox) — deliberately not a grid.

### Implementation notes — hard-won

- **Use the Web Animations API** (`element.animate()`), not CSS transitions on `stroke-dashoffset`. The CSS approach fails: setting the dash length via a custom property in the same style recalculation that also sets the target offset gives the browser no start state to animate from, so shapes appear instantly instead of drawing. This cost several rounds to find.
- **`vector-effect: non-scaling-stroke`** is required. Without it, scaling a silhouette to 13% scales its stroke to invisibility.
- Stagger **per silhouette**, not per path — per-path staggering made the field take 6+ seconds to fill.
- **Don't fake letterforms with path data.** An attempted "VANTA" wordmark rendered as "VAT" because it only had three letterforms. Any logo must come from a real vector file, or be replaced by an object silhouette. FTC now draws a robot.

### Motif library

Three exist: `rotom`, `hammer` (Thor's Hammer PCB), `robot` (FTC). **Each project needs its own** — roughly six lines of SVG path data each. Projects without one show a plain ground, which is acceptable graceful degradation.

Candidates: breadboard grid (EEG-turned-EMG), PCB outline (bme474), CPAP mask profile, game controller (Godot titles).

**Not doing:** Dmitri's face. Orthogonal traces render a face as noise rather than as a likeness. If ever wanted, it must be deliberately drawn line art — six to eight strokes — not a traced photo.

## Layout — unchanged from #7

Study D "Plates": photo-maximal, fixed two-up, four per screen, all plates identical, single column under 720px. `rank` sets position only.

## Accessibility

`prefers-reduced-motion: reduce` must suppress the motif field entirely (fall back to the static field), and the manual motion control must remain.
