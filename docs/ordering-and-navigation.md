# Ordering and navigation

Settled in the issue #3 grilling, 2026-08-21.

## The ordering rule

**Curated rank — no derivable rule.** Order is Dmitri's judgment, blending:

- hours sunk in
- how hard it was
- how much was learned
- **how proud he is of it** (the tiebreaker)

…and then **capped by how much the card can actually show.**

That cap is the load-bearing part. #2 established *no photo → no card*; #3 extends it: **evidence gates position, not just presence.** The mHealth Tympanometer is the case that proved it — Dmitri's proudest item, demoted out of the lead slot because the project is closed-source and unfinished, so the card would be thin.

### Consequence for the content model

Rank must be **stored explicitly per project** — an integer or an ordered list. Nothing in the data can compute it. (Chronological or category ordering would have come free from a date or tag field; curation does not.)

### One number, one job — amended by #7 (2026-08-23)

Originally: rank set both card size and position. **The prototype retired the size half.** Study D was chosen — **all plates are identical**, so `rank` now controls **position only**, and #2's three weight tiers (lead / standard / grouped) are gone. The Flutter group is an ordinary plate like everything else.

**Order is supplied by hand.** Dmitri provides the explicit sequence.

## Order at launch

**`bme290` (Thor's Hammer PCB) leads — confirmed by Dmitri 2026-08-23**, not merely by default. It is also the only lead card *already fully evidenced*: 3D render PDFs, gerbers, BOM PDFs and DRC reports are in the repo today; it needs nothing from Dmitri.

Named for the top, in rough order: **Thor's Hammer PCB (position 1, confirmed), then `bme474`, then Rotom, then FTC mentorship.** The tympanometer is explicitly *not* the lead card — demoted on thin content (closed-source, still in development).

Rotom and the mentorship are at **zero material today** — the same condition that demoted the tympanometer. **The order re-sorts as the #10 intake queue fills.**

> **Open:** the full 17-card rank order is not pinned. Only the top is. Revisit once photos and blurbs land.


## Amended 2026-09-20 — the site is now three pages

The root is no longer the grid. Dmitri asked for the head-scan page as the home page,
with the archive and a links page reachable from it.

| Path | What it is |
|---|---|
| `/` | **Home.** The scan card — one screen, no scroll, contact links at its foot. Promoted from prototype variant A. |
| `/archive/` | **The grid**, unchanged in design. Moved here from `/`. |
| `/links/` | **Links** — GitHub, LinkedIn, Onshape, email, with a photo of Dmitri. Built on prototype variant F (module grid). |
| `/<project>/` | Unchanged. |

### What this changed elsewhere

- **The nine project pages each had one line changed** — `<a class="back" href="../">`
  became `href="../archive/"`, so "← Archive" still lands on the archive rather than on
  the new home page. Nothing else on those pages was touched.
- The archive page's own links were rewritten one level up (`../<project>/`,
  `../<project>/photos/...`).
- **Navigation is no longer "scroll, that's it."** A drawer in the top left carries
  Home / Archive / Links and now appears on the home, archive and links pages. The
  project pages still rely on their single back link — deliberately, to keep the change
  to them to one line. Worth revisiting if the drawer proves useful.
- The "no dates, no search, no filter" rules for the grid itself still stand.

## Page structure

- **One grid, all 17 cards, visible at once.** No featured strip, no sections. A "featured" area would be the site editorializing about itself and would split the page into the good stuff and the rest — against the archive-first thesis.
- **No dates anywhere in the grid.** No year on cards, no era markers. *"It's just the projects I've done."* The archive is a set of things made, not a timeline.
  - Years are still **collected** during intake (#10) — storing an undisplayed date costs nothing; un-collecting is expensive. Display stays off. Whether the detail page shows a year is #4's call.
- **Accepted cost:** ordering by intensity destroys chronology. The arc (high school → Duke BME → Godot for fun → Mondo's) is not visible on the landing page. Accepted deliberately.

## Navigation

**Scroll. That's it.** No search, no filter, no tags — 17 cards do not need them. This resolves the map's open "Search / filter / tags" item.

A card carries exactly **two pieces of information** before a click:

1. The project name
2. Its status

### Status vocabulary — two states

`in progress` · `complete`

Binary, settled. No "abandoned" state: a stalled project reads as in progress indefinitely, and Dmitri accepts that as an honest description of how his projects actually go. (`doodlejump` is the case in point — *"I will get back around to it once I finish my other project."*)

This settles the status indicator left open by #2.

## Chosen layout — issue #7, 2026-08-23

**Study D — "Plates".** Photo-maximal, **fixed two-up**, sized so **four plates land in one screen**. Every plate identical; no size hierarchy.

Rejected: *A — contact sheet* (dense uniform tiles), *B — weighted mosaic* (the only study that rendered the three tiers literally), *C — index* (text-dominant).

Prototype: https://claude.ai/code/artifact/9bcd1c94-2afd-48ec-a283-99433235f9a6

**Visual direction, approved:** exposed-copper amber as the sole accent, solder-mask green for status only, cool paper neutrals. `Archivo` display / `Newsreader` body / `IBM Plex Mono` labels. Deliberately unlike Mondo's neon.

**Detail page approved as prototyped** — prose with images interleaved, links woven in as calls to action, status pill, no year, no tech list.
