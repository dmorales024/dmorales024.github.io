# Project detail page — content model

Settled in the issue #4 grilling, 2026-08-23.

## The page is a story, not a spec sheet

Dmitri, on what a detail page should contain:

> "A story of the process, what the thing did, and the inspiration. Essentially telling the story of what happened."

This eliminated almost every field the ticket proposed. Date range, tech/tools, role, structured links, one-line summary — all cut in favour of prose. A detail page is a few hundred words with a shape: inspiration → process → what it did → what was learned.

## Images are interleaved

Pictures sit **at the moment in the prose where they are relevant** — a board render appears where the layout work is described — not in a gallery below the text.

**Architectural consequence:** the page cannot be modelled as `blurb: string` + `photos: string[]`. Prose and images are one authored document. That means **Markdown/MDX per project**, metadata in frontmatter, body hand-authored. This is a live input to #5 — stacks with a good Markdown authoring story rank higher.

## The type

```ts
type Project = {
  slug: string;      // content/<slug>/ — also the URL
  title: string;     // display name; never a course code
  status: 'in-progress' | 'complete';
  hero: string;      // explicitly chosen file in photos/ — the grid's cover image
  rank: number;      // sets BOTH card size (#2) and scroll position (#3)
};
```

The story is the Markdown body. **No optional fields exist** — so the ticket's "what does the page look like when a field is empty" question dissolves. #2's *no photo → no card* rule guarantees `hero` always resolves.

## Field decisions

- **`hero` is explicit.** Set per project, not inferred from filename order. **This retires the `01-is-the-hero` convention** from the intake sheets; numbering may still order photos, but it no longer designates the cover.
- **No year, anywhere.** Not in the grid (#3), not on the detail page. Deferred twice and settled here: *"no year."* Years are still **collected** at intake (#10) — storing an undisplayed date is free, re-gathering is not.
- **Links are prose, not metadata.** Woven in at the relevant moment, phrased as calls to action — *"click here to see the CAD."* No `repo` / `demo` / `article` fields.
  - *Accepted cost:* with no structured link data the site can never generate e.g. "every project with a public repo." Fine at 17 cards with no filtering (#3).
- **Embeds (YouTube, CAD viewers, 3D) are body content**, not metadata — they interleave like images.
- **Credit is prose.** Dmitri describes the work he personally owned and credits teammates in the writing. No structured team/role field. (`bme474` was four people; the CPAP monitor was two.)

## Borrowed images — resolved

**No image Dmitri does not own will appear on the site.** The Duke Pratt tympanometer photos are **link-out only**; the reader clicks through to the article.

This removes the need for any caption or image-credit mechanism, and keeps the schema at four fields. It also means **every file under `content/*/photos/` is Dmitri's own** — a useful invariant.

## The hard cases, checked

| Case | Survives? |
|---|---|
| **Tympanometer** — no public repo, can't say much, borrowed press photos | Yes. Short story, own photos only, links out to Duke. |
| **Rotom** — physical object, no software, no "tech stack" | Yes. Prose has no stack field to leave empty. |
| **`bme290`** — best assets are PDF renders, not photos | Yes. Renders are story images like any other. |
| **High school CAD** — no repo *and* no photo | N/A — cut entirely in #8. |
| **Flutter ×7** — one page, seven repos | Yes. One slug, one story, links to all seven in prose. |
