# Project inventory — working draft

Status of issue #2. Enumerate everything first, rank by "coolness" second (Dmitri's call, 2026-08-20).

Evidence column: **repo** = code exists on GitHub · **artifact** = files exist but not code (PDFs, CAD) · **none** = nothing tracked, needs excavation (#8)

## A. Has a repo

| Project | Year | Evidence | Notes |
|---|---|---|---|
| mHealth Tympanometer (Palmeri Lab) | — | none | ~~Lead candidate~~ **— demoted 2026-08-23; Thor's Hammer PCB leads.** NIH-funded, Duke Pratt article, South Africa field test. Dmitri's contribution: **software, plus a full Altium → KiCad migration of the board design**. Project is **still under active development — he can't speak freely about it.** No repo on the account. |
| `bme474` — nRF52833 Zephyr firmware + pressure processing | 2024 | repo | Jupyter + firmware, 4-person team (Herzberg, Morales, Duerr, Breit) |
| `bme290` — Thor's Hammer PCB | 2024 | repo (artifacts) | KiCad, 3D render PDFs, BOM PDFs, one-shot blinking circuit |
| `EEG-turned-EMG-` — BME354 final | 2022 | repo | Own circuit design: bandpass + notch filters, RPi Pico, LED on blink. Set out to read alpha waves, pivoted to EMG. Video slot in README is still `*INSERT HERE*`. |
| `sleep-study-monitor-GUI` — CPAP monitor | 2024 | repo (private) | Flask + MongoDB, patient GUI + central ward GUI, pytest CI. Co-authored w/ Connor Shovlin. |
| `NotUber` — CS330 case study | 2023 | repo | 5 matching algorithms over NYC road graph: brute force → straight-line → Dijkstra → KD-tree + A* → predictive |
| `botherDmitri` — BLE knock notifier | 2026 | repo | nRF52833 DK, C, Zephyr/NCS |
| `workflow-tracker` — SDLC VS Code extension | 2026 | repo (private) | TypeScript, sidebar checklist for Cursor skills workflow |
| `workday-autofill` | 2024 | repo | Python, 12KB |
| `adventureGame` (Godot) | 2025 | repo | GDScript, 59MB — largest asset set |
| `first-godot-game` | 2025 | repo | GDScript |
| `doodlejump` | 2025 | repo | |
| Flutter tutorials ×7 | 2022 | repo | `flutterApp1`, `quiz-`, `expense-tracker`, `meals-`, `places-`, `shop-`, `story-` — all Sept 2022 |
| Mondo's — restaurant static site | 2024–26 | repo (private) | **IN.** Vite + React Router v7 prerendered, AWS. Still in progress. |

## B. No repo yet — needs creating or excavating

| Project | Evidence | Blocked on |
|---|---|---|
| Rotom — first CNC job, circuit-breaker cover | none | **IN.** Dmitri supplies photos (#9) |
| FTC Vanta 31000 mentorship | none | **IN as a project card** — settled 2026-08-20 |
| Makerspace builds → **chess board coaster** | one photo Dmitri can take | Scope corrected 2026-08-20: not a set of builds, one item. Card can expand later if more surfaces. |
| High school CAD / ECAD / Arduino | none | **OUT for now** (2026-08-20) — no evidence Dmitri can produce. Science Olympiad photos exist but not enough for a card. Revisit only if material surfaces. |

## C. Excluded (settled, do not revisit)

Disney (`wai`, People Counter, Signal4, Figaro, MagicMobile) · GFC ops platform — incl. my-calendar, briefly reconsidered 2026-08-20 and omitted again · `yomando` · `bme301` · `bme303` · `first-react-app` · `starter-git` · `resume` repo (LaTeX source, not a project) · forks (`flutter_blue_plus`, `flutter-ble`, `Cuff_less_BP_Prediction`)

## Decisions so far (issue #2)

- **Ranking axis: "coolness"** — Dmitri's own taste, not recruiter-impressiveness. Enumerate first, rank second. (2026-08-20)
- **Lead group (4):** `bme290` Thor's Hammer PCB **(lead card, position 1 — confirmed 2026-08-23)** · `bme474` · EEG-turned-EMG · mHealth Tympanometer *(demoted from lead: closed-source, thin content)*
- **What the lead tier has in common:** not "hardware" — hardware *with substantial code behind it*. Both bme474 and the EEG/EMG span an analog/physical build and real software. Use this as the lens for weighting the rest.
- **Cards carry status.** A "little status bar" on the card — the archive is honest about work that isn't finished, not just work that's amateur. Vocabulary TBD.
- **`doodlejump` is unfinished** and would move up if ever completed. Mondo's is mid-build. EEG README still has `*INSERT HERE*` for its demo video.
- **Course-code names must be renamed** for display — "Thor's Hammer PCB" is a name, `bme290` is a filing code. Feeds #4.
- **Tympanometer card contents:** the device/design is **not public**, so the card carries Dmitri's own photos + a narrative of his experience + the **Altium → KiCad conversion** as the concrete technical contribution. The public Duke Pratt article can be linked and credited (per map standing preference) — Duke's photos are Duke's.
- **KiCad is a through-line** — appears in both the tympanometer migration and `bme290`. Possible connective tissue between cards.
- **Flutter tutorials ×7 → one grouped area, minimal weight.** Present because the work happened; not seven cards. Resolves sub-question 1 of #2.
- **Godot games get individual cards** — `first-godot-game`, `adventureGame`, `doodlejump` are self-directed, not tutorials.
- **Grouping principle (derived):** work done by *following someone else's instructions* groups into one area; work where *Dmitri chose what to build* gets its own card. This is the placement rule for future additions.
- **No photo → no card.** A project with nothing to show stays off the page rather than appearing as an empty card. High school CAD is out on these grounds; Science Olympiad photos exist but aren't enough. Resolves sub-question 4 of #2.
- **Weight structure (3 levels):** ~~lead tier (4) · standard card · grouped area~~ — **RETIRED by #7 (2026-08-23).** Study D uses uniform plates; every card is the same size. `rank` is position only. The lead four still lead, but by *order*, not by size. The Flutter group is an ordinary plate.
- **FTC Vanta 31000 is a project card,** not an about-page or leadership surface. Resolves sub-question 3.
- **`first-react-app` and `starter-git` are OUT** (2026-08-20).


---

## Cut list revised — 2026-08-31

**Removed from the archive** (pages and grid plates deleted):

- `adventureGame` — Godot platformer
- `first-godot-game`
- `Learning Flutter, 2022` (the seven-repo grouped card)
- `workday-autofill`
- `workflow-tracker`

Dmitri's call. This retires the **grouped-area tier** entirely, since the Flutter card was its only member — the placement rule from #2 (followed instructions → group; chose what to build → own card) no longer has anything to apply to.

**Added:** **Millionaire Club Frame** — 3D-printed picture frame, 2025. Printed lettered base, webbed shaka, etched photo panel. CAD on Onshape. Intake tracked in #29.

**Card count: 17 → 13.**

**`doodlejump` cut too** (2026-08-31). Its repo is a Godot project file, one empty `Node2D`, zero scripts, and the previous project's assets copied across — created and abandoned the same day as `adventureGame`. No image could exist for it, so #2's *no photo → no card* rule already covered the case. Reinstate if it is ever actually built.

**Card count: 17 → 12.**


## Mondo's removed — 2026-08-31

Cut at Dmitri's request. It was the only client work in the archive and the only in-progress card carrying a long engineering write-up; the page had already been reduced to a three-line note before removal.

**Card count: 17 → 9.**

The animated neon card went with it, which also **retires the grid-animation exception** — `docs/visual-direction.md`'s rule that the grid page carries no animation is once again true without qualification.
