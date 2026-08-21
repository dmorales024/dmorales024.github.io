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

### One number, two jobs

Weight (card size, from #2) and position (from #3) are **the same ranking**. A project's rank sets both how big its card is and where it sits. No separate dial.

## Order at launch

**`bme290` (Thor's Hammer PCB) leads** — and it leads partly by default: it is the only lead-tier card that is *already fully evidenced*. 3D render PDFs, gerbers, BOM PDFs and DRC reports are in the repo today; it needs nothing from Dmitri.

Named for the top, in rough order: **`bme290` or `bme474`, then Rotom, then FTC mentorship.**

Rotom and the mentorship are at **zero material today** — the same condition that demoted the tympanometer. **The order re-sorts as the #10 intake queue fills.**

> **Open:** the full 17-card rank order is not pinned. Only the top is. Revisit once photos and blurbs land.

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
