# Content intake queue

Index of all 17 confirmed project cards (issue #2). One folder per slug under `content/`, each
with its own `README.md` intake sheet and a `photos/` drop folder. Ranking axis is "coolness"
(Dmitri's own taste), not recruiter-impressiveness.

Display name, tier, and status decisions live in `docs/project-inventory.md` — this table is a
queue view, not the source of truth.

## Lead tier (4)

| Slug | Display name | Tier | What's still needed |
|---|---|---|---|
| [`tympanometer`](tympanometer/) | mHealth Tympanometer (Palmeri Lab) — **name TBD** | Lead | Highest priority. Dmitri's own photos, his narrative, Altium→KiCad writeup. Display name decision (#4). Duke article photos must stay credited-link-only, never copied in. |
| [`eeg-turned-emg`](eeg-turned-emg/) | EEG-turned-EMG | Lead | Photos, narrative. **Recover the blink-to-LED demo video** — repo README still has `*INSERT HERE*`; highest-value asset recovery in the archive. |
| [`thors-hammer-pcb`](thors-hammer-pcb/) | Thor's Hammer PCB | Lead | Photos (can be exported from existing `bme290` 3D-render PDFs/gerbers/BOM — no new shoot needed), narrative. |
| [`bme474`](bme474/) | **DISPLAY NAME NEEDED** | Lead | Display name decision (#4). Photos, including rendered `diagrams/state_diagram.puml`. Narrative. |

## Standard (12)

| Slug | Display name | Tier | What's still needed |
|---|---|---|---|
| [`cpap-sleep-monitor`](cpap-sleep-monitor/) | CPAP Sleep Monitor | Standard | Photos, narrative. |
| [`notuber`](notuber/) | NotUber | Standard | Photos, narrative. |
| [`bother-dmitri`](bother-dmitri/) | Bother Dmitri | Standard | Photos, narrative. |
| [`workflow-tracker`](workflow-tracker/) | Workflow Tracker | Standard | Photos, narrative. |
| [`workday-autofill`](workday-autofill/) | Workday Autofill | Standard | Photos, narrative. |
| [`adventure-game`](adventure-game/) | Adventure Game (Godot) | Standard | Photos, narrative. |
| [`first-godot-game`](first-godot-game/) | First Godot Game | Standard | Photos, narrative. |
| [`doodlejump`](doodlejump/) | DoodleJump | Standard | **In-progress/unfinished status.** Photos, narrative. |
| [`mondos`](mondos/) | Mondo's | Standard | **Mid-build status.** Photos, narrative, live demo URL once available. |
| [`rotom`](rotom/) | Rotom | Standard | Photos (in situ + in-progress CNC shots), "what was learned on the CNC" narrative, year. Repo to be created (#9, public). |
| [`ftc-vanta-31000`](ftc-vanta-31000/) | FTC Vanta 31000 Mentorship | Standard | Photos, narrative, year. No repo (mentorship role). |
| [`chess-board-coaster`](chess-board-coaster/) | Chess Board Coaster | Standard | Photos (one known to exist — get it in), narrative, year. Collapsed entire makerspace category into this one card. |

## Grouped area (1)

| Slug | Display name | Tier | What's still needed |
|---|---|---|---|
| [`flutter-tutorials`](flutter-tutorials/) | Flutter Tutorials | Grouped, minimal weight | Photos (a handful across all 7 apps, not per-app), **one shared blurb** covering all 7 repos. |

## Conventions

- Photos go directly in each project's `photos/` folder.
- Naming: `01-description.jpg`, `02-description.jpg`, … — lowest number is the hero/cover image.
- Blurbs are the story, not a spec sheet: what it was, why it was made, what was learned, what
  went wrong (per issue #10).
- No photo, no card — a project with nothing to show stays off the page.
