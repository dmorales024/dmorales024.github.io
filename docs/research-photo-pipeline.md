# Photo storage and delivery pipeline

Research for issue #6. Written 2026-08-23. All measurements in this doc were taken against the
real files in `content/` on that date, not estimated.

**Scope: images only.** Video was settled separately on 2026-08-23 — clips go to YouTube and are
embedded via `youtube-nocookie.com`, interleaved in the prose like any other body content (#4).
Nothing below applies to video.

Assumes the #5 outcome: **Astro 7 + `@astrojs/mdx` + content collections.** Where a
recommendation depends on that, it is marked **[Astro]**. Where it holds regardless, it is marked
**[stack-independent]**.

---

## Recommendation

**Commit one 1600 px WebP per photo. Nothing else. Masters stay out of git.**

1. **Every image in `content/*/photos/` is a ≤1600 px WebP**, EXIF-stripped and auto-oriented.
   That is the *only* thing the repo stores per photo — average **164 KB** measured, versus the
   **2.6 MB** the current process commits. **[stack-independent]**
2. **Astro generates the small sizes at build**, not the script. A committed 1600 px canonical
   plus `image.layout: 'constrained'` gives grid cards their 480/960 `srcset` for free, with no
   extra bytes in the repo. **[Astro]**
3. **Full-resolution masters live outside git** — iCloud Photos plus a local archive folder — with
   a committed `photos/manifest.json` recording which master each derivative came from and its
   capture date. Losing the *mapping* is what makes an archive unrecoverable; losing a copy of a
   file that iCloud also holds is not. **[stack-independent]**
4. **Two entry points, because Dmitri uploads through the GitHub web UI.** A local
   `scripts/ingest-photos.py` for the clean path, *and* a `photo-normalize.yml` GitHub Action that
   runs the same conversion on push and commits the result back. The Action makes the web-UI path
   correct; the local script makes it clean. Both are needed. **[stack-independent]**
5. **Kill `scripts/convert-heic.py` in its current form.** It is actively making things worse — see
   below.
6. **Git LFS is a trap.** It does technically work behind an Actions-based Pages deploy, but it
   solves nothing here and costs quota. Do not use it.

**Immediate action item, unrelated to size:** the committed
`content/ftc-vanta-31000/photos/9356BC72-…jpg` carries **GPS EXIF data** (`file` reports
`GPS-Data`, iPhone 16). That is a public repo. Strip EXIF from everything published.

---

## 1. Storage ceiling — is the worry real?

### Verified limits (2026-08-23)

| Limit | Value | Applies to |
|---|---|---|
| Per-file warning | 50 MiB | any push |
| Per-file **hard block** | **100 MiB** | any push — GitHub rejects it |
| Browser (drag-and-drop) upload | **25 MiB per file**, 100 files per upload | the web UI, i.e. how Dmitri works |
| Repo size — ideal | **< 1 GB** | recommendation, not enforced |
| Repo size — strongly recommended | **< 5 GB** | recommendation, not enforced |
| **GitHub Pages published site** | **1 GB** | the **build output**, not the repo |
| Pages bandwidth | 100 GB/month, **soft** | irrelevant at this traffic |
| Pages builds | 10/hour soft — **does not apply** to custom Actions workflows | we will use a custom workflow |

The distinction that matters most: **the 1 GB Pages limit is on the published site**, so files that
sit in the repo but never reach `dist/` do not count against it. They only cost repo size and
clone time.

### Ground truth in `content/` today

`content/` is 14.3 MB across **12 images in 4 of 17 projects**. `.git` is another 21.7 MB.

| File | Dimensions | Size |
|---|---|---|
| `ftc-vanta-31000/…9356BC72.jpg` | 3760×5014 | 3.07 MB |
| `eeg-turned-emg/…34ABB43E.jpg` | 4032×3024 | 2.62 MB |
| `ftc-vanta-31000/…2C7053B4.jpg` | 4032×3024 | 2.62 MB |
| `rotom/IMG_0130.jpg` | 4032×3024 | 2.49 MB |
| `chess-board-coaster/…5785F3A6.jpg` | 4032×3024 | 2.15 MB |
| `ftc-vanta-31000/…7866D394.jpeg` | 3840×1728 | 418 KB |
| 4 × Rotom PNG screenshots | ≤1288 px | 128–208 KB each |
| 2 × FTC 1600×900 JPEGs | 1600×900 | 129 / 169 KB |

The five iPhone photos average **2.59 MB** and are all ~4000 px wide. A grid card displays them at
roughly 300–500 CSS px.

### Projection

Realistic photo counts for prose-interleaved detail pages (#4): ~6 for a standard card, 10–20 for
lead tier.

| Scenario | 100 photos | 170 photos | 340 photos |
|---|---|---|---|
| **Status quo** (one 2.59 MB full-res JPEG each) | 259 MB | 441 MB | **881 MB** |
| **Recommended** (one 164 KB 1600 px WebP each) | 16 MB | 28 MB | **56 MB** |
| Recommended + masters kept in repo (+1.61 MB each) | 177 MB | 302 MB | 603 MB |

### Verdict: the worry is real, but the storage ceiling is the wrong thing to worry about

At 340 photos the naive approach reaches **881 MB of published site against a 1 GB hard Pages
limit** — it breaks, but only at the far end, and only after years. That is not the problem.

**The page weight is the problem, and it breaks immediately.** The landing grid shows all 17 cards
at once (#3) — no pagination, no lazy sections:

| Landing grid, 17 hero images | Total transfer |
|---|---|
| Status quo (full-res 2.59 MB each) | **44 MB** |
| 480 px WebP (measured avg 23.8 KB) | **405 KB** |
| 960 px WebP for 2× DPR (measured avg 66 KB) | 1.1 MB worst case |

44 MB is not a slow page, it is a broken page on a phone. **A 100× reduction is available and the
repo-size question resolves itself as a side effect.**

The second real cost is **git history**, which never shrinks. The repo currently carries 5 HEIC
originals (7.68 MB, deleted from the working tree but permanent in history) *plus* their 12.36 MB
of JPEG replacements — **20.7 MB of history for 5 delivered photos, 4.1 MB each.** Images are
already entropy-coded, so zlib and delta compression recover essentially nothing. Extrapolated to
170 photos on the current path: ~700 MB of `.git` that can never be reclaimed without a history
rewrite.

---

## 2. Git LFS — confirmed trap, with a nuance

**The plain statement holds: Git LFS pointers are not resolved by the legacy branch-based Pages
build.** GitHub Pages serves the ~130-byte pointer text file, and the image is broken. GitHub's
official position in the community discussion is *"There is no plans to support Git LFS in GitHub
Pages."*

**The nuance:** if Pages is deployed from a **custom GitHub Actions workflow** (which #5's Astro
build will be anyway), `actions/checkout` with `lfs: true` materializes the real files before the
build, and they land in `dist/` as normal bytes. So LFS is not *technically* impossible.

**It is still the wrong choice here, for four reasons:**

1. **It buys nothing against the binding limit.** The materialized files count fully against the
   1 GB *published site* limit. LFS moves bytes out of the git object store, not off the site.
2. **Every deploy re-downloads every LFS object**, burning bandwidth quota. A user in the linked
   discussion blew through their org's quota in **three commits** doing exactly this.
3. **Free-tier quota is 10 GiB storage / 10 GiB bandwidth**, now billed as metered overage rather
   than pre-paid packs. A recurring bill for a personal archive is a bad trade.
4. **It breaks the web-UI workflow entirely.** Files dropped into the browser are committed as
   normal blobs regardless of `.gitattributes` — so LFS would silently not apply to the exact path
   Dmitri actually uses.

**Document the pointer-file behaviour as a trap in the repo.** It is the kind of thing that gets
rediscovered painfully, and the "but it works with Actions" nuance makes it easy to talk yourself
back into.

---

## 3. The processing pipeline

### 3a. Why the current JPEGs came out *larger* — two compounding causes

Measured from git history, HEIC original → committed JPEG:

| Photo | HEIC | JPEG (sips q80) | Change |
|---|---|---|---|
| chess-board-coaster | 1.26 MB | 2.05 MB | **+62%** |
| eeg-turned-emg | 1.65 MB | 2.50 MB | **+52%** |
| ftc `2C7053B4` | 1.50 MB | 2.50 MB | **+67%** |
| ftc `9356BC72` | 1.86 MB | 2.93 MB | **+58%** |
| rotom `IMG_0130` | 1.42 MB | 2.38 MB | **+68%** |
| **Total** | **7.68 MB** | **12.36 MB** | **+61%** |

**Cause 1 — nothing is downscaled.** `convert-heic.py` calls `sips` with no `-Z`, so a 4032×3024
phone photo stays 4032×3024. That alone accounts for most of it.

**Cause 2 — `sips` is a genuinely bad JPEG encoder.** Measured on the same source, resized to
1600 px by each tool:

| Encoder | Setting | Output |
|---|---|---|
| `sips` | q80 | **534,667 B** |
| `sips` | q70 | 458,235 B |
| `sips` | q60 | 350,784 B |
| ImageMagick | q80 | **309,895 B** |

**`sips` at q80 is 1.73× larger than ImageMagick at q80. `sips` at q60 is still worse than
ImageMagick at q80.** Dropping `sips` quality to compensate would degrade the image *and* still
lose. Cause 3 is simply that HEIC (HEVC intra) is a better codec than JPEG, so a like-for-like
full-resolution transcode is *expected* to grow — which is why the fix is not "tune the quality
number", it is "downscale and use a modern format".

Also worth knowing: **`sips` cannot write WebP at all** (`sips --formats` lists
`org.webmproject.webp` as read-only). It *can* write AVIF, and does it well — but see 3c.

### 3b. Recommended pixel widths

| Width | Purpose | Measured avg WebP q80 |
|---|---|---|
| **480 px** | Grid card, standard tier, 1× DPR | **23.8 KB** |
| **960 px** | Grid card at 2× DPR; lead-tier card at 1× | **66.3 KB** |
| **1600 px** | In-prose full-width body image, and the click-through/lightbox image. Prose columns run ≤800 CSS px, so 1600 is the 2× retina size. | **164.5 KB** |

**Do not generate 2400 px.** Measured: 344 KB versus 205 KB at 1600 px on the same photo, for a
width no prose column on this site will ever request. If a genuine "view full size" affordance is
ever wanted, it should link to the archived master (§5), not ship a fourth derivative.

**1600 px is the canonical committed asset.** Every smaller size is derivable from it; nothing
larger is needed.

### 3c. Format: **WebP only. No AVIF, no JPEG fallback.**

**WebP over JPEG** — measured, same source, same 1600 px:

| Format | q72 | q80 |
|---|---|---|
| JPEG (4:2:0, progressive) | 257 KB | 310 KB |
| **WebP** (`method=6`) | 163 KB | **205 KB** |

WebP is ~34% smaller at matched quality. Browser support is **~97.4%** (caniuse, 2026).

**Against AVIF.** At 1600 px: AVIF q60 = 192 KB (`avifenc`) or 167 KB (`sips`), versus WebP q80 =
205 KB. That is a **6–19% saving depending on encoder**, or roughly **10–35 KB per image**, in
exchange for a second format, `<picture>` markup, ~3 s/image encode time, and support dropping to
~94.9%. Not worth it at these absolute sizes. **[Astro]** If this ever changes, Astro can emit AVIF
by config alone (`format: 'avif'` or a `<Picture>` with `formats={['avif','webp']}`) — so this is a
one-line future upgrade, not a decision that needs making now.

**Against a JPEG fallback.** Measured: adding 1600 px JPEG fallbacks for the 8 photos currently in
the repo costs **1.95 MB**, which is **+76% on top of the entire WebP payload**, to serve the
~2.6% of browsers without WebP (essentially pre-iOS-14 devices and IE). Skip it. **[Astro]** If it
is ever needed, `<Picture formats={['webp']} fallbackFormat="jpg">` adds it at build with no repo
cost.

### 3d. Quality settings

| Source type | Encode | Rationale |
|---|---|---|
| Phone photos, PDF renders | **WebP lossy, q80, `method=6`** | q72 saves ~20% but this is a permanent archive; q80 is the right side of that trade. |
| **UI screenshots** (Rotom's PNGs) | **WebP *lossless*** | Measured: 208 KB PNG → **45.8 KB lossless WebP** (−78%) with zero text degradation. Lossy q80 gets to 17 KB but introduces ringing around text — unacceptable for a screenshot whose point is legible UI. |

Do not downscale screenshots below native. Rotom's are already ≤1288 px, i.e. under the 1600 cap.
Applying a 1600 cap to them is a no-op, which is the correct behaviour.

### 3e. `srcset` — worth it, in exactly one place

- **Grid cards: yes.** 17 images on one page, retina displays common, and the difference between
  serving 480 and 960 across 17 cards is 405 KB versus 1.1 MB. This is where responsive selection
  pays.
- **In-prose images: no.** The prose column is a fixed max-width. A single 1600 px source with
  `loading="lazy"` is correct and simpler. Adding `srcset` here buys nothing measurable.

**[Astro]** Both fall out of Astro's responsive image handling: set `image.layout: 'constrained'`
and `image.responsiveStyles: true` in `astro.config.mjs`, and Astro generates `srcset`/`sizes`
automatically for `<Image>`, `<Picture>`, *and* markdown/MDX `![]()` images. Nothing needs to be
hand-authored.

### 3f. PDF-sourced assets (`bme290` / Thor's Hammer PCB)

`bme290`'s best visuals are KiCad 3D render PDFs (#2, #3 — it is the only fully-evidenced lead-tier
card). Rasterize once at ingest, then treat the result as an ordinary photo. Verified working
locally; ImageMagick has the `gslib` delegate compiled in and Ghostscript is installed:

```
magick -density 200 'render.pdf[0]' -background white -alpha remove -alpha off \
       -resize 1600x1600\> -strip -quality 80 -define webp:method=6 out.webp
```

- `[0]` selects page 1 — required, or you get one file per page.
- `-density 200` sets the rasterization DPI *before* the resize. Raising density then downscaling
  is what produces clean edges on vector line art; omitting it renders at 72 DPI and looks soft.
- `-background white -alpha remove -alpha off` — PDFs have a transparent background that would
  otherwise composite to black.
- Flat-shaded / line-art renders may come out smaller as **lossless** WebP. Encode both, keep the
  smaller. The ingest script should do this automatically for any source that is PDF or PNG.

The 3D renders are the source for `thors-hammer-pcb` and mean **no new photo shoot is needed** for
that card (per `content/README.md`).

### 3g. The `-auto-orient` gotcha — verified, and it will bite

`content/chess-board-coaster/…5785F3A6.jpg` has EXIF `orientation=upper-right` (rotated 90°).
`-strip` removes the orientation tag. If `-strip` runs *before* `-auto-orient`, the rotation is
silently lost and the photo publishes sideways. Measured on that exact file:

```
magick src.jpg -auto-orient -resize 1600x1600\> -strip …   →  1200x1600   correct
magick src.jpg -strip -resize 1600x1600\> …                →  1600x1200   sideways
```

**`-auto-orient` must precede `-strip`.** Always. This is the single most likely way the pipeline
produces visibly wrong output.

---

## 4. Where the pipeline runs

### The measured result

Converting all 12 current images to a three-size WebP set (480/960/1600, lossless for the PNGs):

**14,300,202 bytes → 2,563,632 bytes across 36 files.** A **5.6× reduction while producing three
times as many files.** Committing only the 1600 px canonical instead is 164 KB average — a **15.8×
reduction** versus what is in the repo now.

### The split: what the script owns vs. what Astro owns

**[Astro]** Astro processes local images referenced from `src/` and from content-collection
entries, converting to WebP and — with `image.layout` configured — generating the full `srcset`.
Relative `![](./photos/foo.webp)` inside an MDX body is handled natively at build. Files in
`public/` are **never** optimized, so `content/*/photos/` must be wired in as a content-collection
asset path, not dropped into `public/`.

**What Astro does NOT do, and therefore what must happen before commit:**

| Job | Owner | Why |
|---|---|---|
| HEIC → browser format | **Script** | Astro's Sharp pipeline does not decode HEIC. A `.heic` in the repo is a broken image no matter what the build does. |
| **Cap at 1600 px** | **Script** | This is the load-bearing one. Astro generates *smaller* widths from what you give it — it does not shrink the committed source. Ship it a 4032 px original and the 4032 px original stays in git forever, even though the site only ever serves 480/960/1600. **Astro fixes the page weight; only the script fixes the repo weight.** |
| **Strip EXIF/GPS** | **Script** | The master should keep its EXIF (capture dates are collected at intake per #10/#3). The committed copy must not. That is an ingest-time decision, not a build-time one. |
| PDF rasterization | **Script** | Sharp has no PDF decoder. |
| Lossless-vs-lossy choice for screenshots | **Script** | Astro applies one global policy; screenshots and photographs want different ones. |
| 480/960 derivative widths + `srcset` | **Astro** | Free at build, zero repo cost. Do not commit these. |
| Content hashing, cache-busting filenames | **Astro** | Build concern. |

**The rule: the script normalizes, the framework derives.** That split survives a stack change —
if Astro were ever swapped out, the committed 1600 px WebPs are still exactly right, and the
fallback is to have the script emit 480/960 too (measured cost: +90 KB per photo).

### One Astro caveat to verify during implementation

`content/` sits at the repo root, outside `src/`. Astro's content-layer `glob()` loader can point
its `base` there, but **relative image resolution from MDX bodies outside `src/` is the part to
smoke-test first** — build one project page with an interleaved image and confirm a hashed WebP
appears in `dist/`, before authoring 17 pages against an assumption. If it does not resolve, the
fix is a symlink or moving `content/` under `src/content/`; either is cheap *now* and expensive
after the intake queue fills.

### `hero` typed as Zod's `image()` — effect on layout and naming

The #5 agent's recommendation to type `hero` as `image()` rather than `string` is right, and it
constrains this doc in three useful ways:

1. **`image()` resolves paths relative to the entry file**, so frontmatter must read
   `hero: ./photos/01-cnc-first-cut.webp`, not a bare filename. **Keep the current layout** —
   `content/<slug>/index.mdx` alongside `content/<slug>/photos/` — which makes that relative path
   short and stable. No change needed.
2. **A missing or misspelled `hero` fails the build**, which mechanically enforces #2's *no photo →
   no card* rule instead of leaving it to discipline. Strictly better than a `string`.
3. **`image()` returns `ImageMetadata` with `width`, `height`, and `format`**, so **do not encode
   dimensions in filenames.** No `foo-1600.webp`. Use stable human names — `01-cnc-first-cut.webp`,
   `02-breaker-panel-fit.webp` — per the `content/README.md` numbering convention. (#4 retired
   "lowest number is the hero"; numbering now only orders, and `hero` is explicit.) Width and
   `aspect-ratio` come from the metadata, which also eliminates layout shift for free.

The provenance link back to the original filename lives in `manifest.json` (§5), not in the
filename.

---

## 5. Do originals stay in the repo?

**No. Derivatives only. Masters live outside git, with a committed manifest.**

**Why not:**

- **Git keeps every version forever, and images do not delta-compress.** Already demonstrated in
  this repo: 20.7 MB of permanent history for 5 delivered photos. Every rotate, recrop, or
  re-upload adds a *full* copy. Storing masters means every future correction costs another 1.6 MB
  of unreclaimable history.
- **A public repo is a bad backup.** No redundancy guarantee, and anything committed by mistake —
  a face, a whiteboard, GPS coordinates — cannot be removed without a force-push history rewrite.
- **The masters already exist somewhere better.** The HEICs came from iCloud Photos, which is
  already redundant, already versioned, and already backed up. Committing a second copy to a public
  git repo does not increase durability in any meaningful way.
- **340 masters ≈ 550 MB of clone weight** that every future checkout pays for, permanently.

**Why the counter-argument deserves a real answer:** this is meant to be a permanent personal
archive, and losing originals *is* a real cost — the 2022 EEG-turned-EMG photos are not
re-shootable. But the failure mode is not "the file was deleted." It is **"the file still exists in
a 40,000-photo iCloud library and nobody knows which one it is."** The mapping is the fragile
thing, and the mapping is cheap to make durable.

**So: commit a `manifest.json` per project.** Machine-written by the ingest script, human-readable,
a few hundred bytes:

```json
{
  "01-cnc-first-cut.webp": {
    "master": "IMG_0130.HEIC",
    "captured": "2026-01-11T10:52:28",
    "device": "iPhone 11",
    "source_px": [4032, 3024],
    "sha256": "…"
  }
}
```

This buys: provenance forever, capture dates preserved in the repo after EXIF is stripped (which
#10 and #3 want collected but not displayed), and a checksum to confirm a recovered master is the
right file. It costs kilobytes.

**Where the masters go:** `~/Archive/dmorales024-site-masters/<slug>/`, mirrored to an external
drive or Backblaze, *in addition to* iCloud. The ingest script should **refuse to run** if the
archive directory does not exist, so the discipline is enforced by the tool rather than by memory.

**One honest note in favour of repo-resident masters:** because the 1 GB Pages limit applies to the
*published site*, masters kept in `content/` but excluded from `dist/` would not break Pages — only
repo size. That makes it survivable, not advisable. The clone-weight cost is permanent and grows
monotonically; the durability benefit is near zero given iCloud. Recommendation stands.

---

## 6. Dmitri's actual workflow

He takes photos on his phone and **uploads them by drag-and-drop through the GitHub web UI.** Git
history confirms it — four commits titled *"Add files via upload"*. **Nothing local runs at upload
time.** Any recommendation that assumes a pre-commit hook is a recommendation that will not
execute.

### Path A — phone-only (what he does today, made safe)

```
iPhone → github.com in the browser → drag into content/<slug>/photos/ → Commit
                                              ↓
                          GitHub Action `photo-normalize.yml` fires on push
                          → converts HEIC/PNG/JPEG → 1600px WebP, strips EXIF,
                            rasterizes PDFs, updates manifest.json
                          → commits the result back with GITHUB_TOKEN
                                              ↓
                          Pages deploy workflow builds the site
```

**Verified: a push made with the default `GITHUB_TOKEN` does not retrigger workflows** — GitHub's
docs state a workflow that pushes with `GITHUB_TOKEN` will not start a new run on `push`. So the
normalize Action cannot loop. The Pages build must therefore be triggered from within the normalize
workflow (`workflow_call`, or a job dependency in the same workflow), *not* by a separate
`on: push` deploy workflow — otherwise the deploy silently never fires after a normalize commit.
This is the single most likely wiring bug.

Requirements: `permissions: contents: write`, and `git pull --rebase` before pushing back in case a
second web-UI commit lands mid-run. ImageMagick and `libheif` are available on `ubuntu-latest`
runners; Sharp installs from npm and the Astro build needs it anyway.

**What Path A costs:** the oversized original is committed *before* the Action rewrites it, so it
is in git history permanently — **~2.6 MB of dead weight per photo.** At 170 photos that is ~440 MB
of `.git` that never shrinks. **The site is always correct; the repo slowly is not.** This is an
acceptable trade for the next few uploads and an unacceptable one for a hundred.

### Path B — phone-only, but small (the realistic upgrade, still no desktop)

Build an **iOS Shortcut** on the share sheet: *Resize Image → 1600 px longest edge → Convert Image
→ JPEG → Save to Files*. Select photos in Photos.app, run the shortcut, upload the already-small
JPEGs through the same web UI.

This is the highest-leverage change available, because it fixes the one thing Path A cannot: the
oversized blob never enters history at all. The Action then only does JPEG → WebP and manifest
upkeep. Same number of taps as today.

*Verify when building it:* confirm the Shortcuts "Resize Image" and "Convert Image" actions behave
as expected on a multi-select batch — this was not tested during this research.

### Path C — desktop (the clean path, for bulk intake)

```
AirDrop from phone → ~/Desktop/site-intake/
  → python3 scripts/ingest-photos.py --slug rotom ~/Desktop/site-intake
      · copies masters to ~/Archive/dmorales024-site-masters/rotom/  (refuses to run if missing)
      · writes 1600px WebP into content/rotom/photos/
      · writes manifest.json
  → rename the outputs to 01-…, 02-… descriptive names
  → set `hero:` in content/rotom/index.mdx
  → git add / commit / push
```

Best for the lead-tier cards, where 10–20 photos land at once and naming them properly matters
anyway. `bme290`'s PDF renders must go through Path C — the Action can rasterize them, but choosing
which page of which render tells the story is a human decision.

### Recommendation on paths

**Ship the Action first** (Path A) — it makes the current behaviour safe with zero change to what
Dmitri does. **Then build the Shortcut** (Path B) — it is 20 minutes of work and removes the only
real cost of Path A. **Keep Path C for bulk intake.** Do not try to move him off the web UI; make
the web UI correct.

### Also worth knowing about the web UI

- **25 MiB per file, 100 files per upload.** Not binding for photos, but it is binding if masters
  are ever uploaded — another small argument for §5.
- The web UI cannot create nested folders easily, but `content/<slug>/photos/` already exists with
  `.gitkeep` files, so drag-and-drop into an existing folder works. Keep the `.gitkeep` files.
- The web UI **does not** strip EXIF or recompress. What is dropped in is what is committed —
  including the GPS data already in the repo.

---

## Proposed script: `scripts/ingest-photos.py`

Replaces `scripts/convert-heic.py`. Single dependency: **ImageMagick 7** (`brew install
imagemagick`). Verified on this machine — the installed build has `heic`, `webp`, and `gslib`
delegates compiled in, so one tool covers HEIC decode, PDF rasterization, resize, EXIF strip, and
WebP encode. `sips` is not used: it cannot write WebP and its JPEG encoder is 1.73× worse.

The same conversion function is what `photo-normalize.yml` should invoke, so there is exactly one
implementation of the rules.

```python
#!/usr/bin/env python3
"""Ingest photos into content/<slug>/photos/ as web-ready WebP.

    python3 scripts/ingest-photos.py --slug rotom ~/Desktop/site-intake
    python3 scripts/ingest-photos.py --in-place content/rotom/photos   # CI / web-UI cleanup
    python3 scripts/ingest-photos.py --slug rotom --dry-run ~/Desktop/site-intake

Rules, in one place:
  * cap at 1600px on the long edge, never upscale        (-resize 1600x1600\\>)
  * -auto-orient BEFORE -strip, or rotated photos publish sideways
  * photographs and PDF renders -> lossy WebP q80, method 6
  * screenshots and other PNGs  -> try lossless AND lossy, keep the smaller
  * PDFs rasterize at 200 DPI, page 1, composited on white
  * masters are copied to ARCHIVE_ROOT before anything is stripped
  * manifest.json records master filename, capture date, device, source px, sha256
"""

import argparse, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

MAX_EDGE   = 1600
QUALITY    = "80"
PDF_DPI    = "200"
ARCHIVE_ROOT = Path(os.environ.get(
    "SITE_MASTERS", Path.home() / "Archive/dmorales024-site-masters"))

PHOTO_EXT  = {".heic", ".heif", ".jpg", ".jpeg"}
FLAT_EXT   = {".png"}          # screenshots, line art -> try lossless
PDF_EXT    = {".pdf"}
ALL_EXT    = PHOTO_EXT | FLAT_EXT | PDF_EXT


def probe(src: Path) -> dict:
    """Pull EXIF we want to keep in the manifest before we strip it."""
    fmt = "%[EXIF:DateTimeOriginal]|%[EXIF:Model]|%w|%h"
    out = subprocess.run(["magick", "identify", "-format", fmt, f"{src}[0]"],
                         capture_output=True, text=True).stdout
    date, model, w, h = (out.split("|") + ["", "", "", ""])[:4]
    return {"captured": date or None, "device": model or None,
            "source_px": [int(w or 0), int(h or 0)]}


def encode(src: Path, dest: Path, lossless: bool, is_pdf: bool) -> int:
    cmd = ["magick"]
    if is_pdf:
        cmd += ["-density", PDF_DPI]
    cmd += [f"{src}[0]" if is_pdf else str(src)]
    if is_pdf:
        cmd += ["-background", "white", "-alpha", "remove", "-alpha", "off"]
    # -auto-orient MUST come before -strip. See docs/research-photo-pipeline.md §3g.
    cmd += ["-auto-orient", "-resize", f"{MAX_EDGE}x{MAX_EDGE}>", "-strip"]
    cmd += (["-define", "webp:lossless=true"] if lossless
            else ["-quality", QUALITY])
    cmd += ["-define", "webp:method=6", str(dest)]
    subprocess.run(cmd, check=True, capture_output=True)
    return dest.stat().st_size


def convert(src: Path, outdir: Path, dry: bool) -> tuple[Path, dict] | None:
    ext = src.suffix.lower()
    if ext not in ALL_EXT:
        return None
    dest = outdir / (src.stem + ".webp")
    if dry:
        print(f"  would  {src.name} -> {dest.name}")
        return None

    meta = probe(src)
    is_pdf = ext in PDF_EXT

    if ext in FLAT_EXT or is_pdf:
        # Flat/line-art content: lossless sometimes wins outright. Measure, don't guess.
        a, b = dest.with_suffix(".ll.webp"), dest.with_suffix(".ly.webp")
        sa = encode(src, a, lossless=True,  is_pdf=is_pdf)
        sb = encode(src, b, lossless=False, is_pdf=is_pdf)
        winner, loser = (a, b) if sa <= sb else (b, a)
        loser.unlink(); winner.rename(dest)
        mode = "lossless" if winner is a else f"lossy q{QUALITY}"
    else:
        encode(src, dest, lossless=False, is_pdf=False)
        mode = f"lossy q{QUALITY}"

    before, after = src.stat().st_size, dest.stat().st_size
    print(f"  ok     {src.name} -> {dest.name}  "
          f"{before//1024}KB -> {after//1024}KB  ({mode})")

    meta |= {"master": src.name,
             "sha256": hashlib.sha256(src.read_bytes()).hexdigest()}
    return dest, meta


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+")
    p.add_argument("--slug", help="content/<slug>/photos/ — required unless --in-place")
    p.add_argument("--in-place", action="store_true",
                   help="convert files where they already sit; used by CI to clean up "
                        "web-UI uploads. Skips the master archive step.")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    if not shutil.which("magick"):
        print("error: ImageMagick not found. brew install imagemagick", file=sys.stderr)
        return 1
    if not a.in_place and not a.slug:
        print("error: --slug is required unless --in-place", file=sys.stderr)
        return 1
    if not a.in_place and not ARCHIVE_ROOT.exists():
        print(f"error: master archive {ARCHIVE_ROOT} does not exist.\n"
              f"       Create it (and make sure it is backed up) or set $SITE_MASTERS.\n"
              f"       Masters are deliberately NOT stored in git — see "
              f"docs/research-photo-pipeline.md §5.", file=sys.stderr)
        return 1

    outdir = (Path("content") / a.slug / "photos") if a.slug else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)

    sources = sorted(f for root in a.paths for f in Path(root).rglob("*")
                     if f.suffix.lower() in ALL_EXT and f.suffix.lower() != ".webp")
    if not sources:
        print("Nothing to ingest.")
        return 0

    manifest_dir = outdir or Path(a.paths[0])
    manifest_path = manifest_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    for src in sources:
        target = outdir or src.parent
        if not a.in_place and not a.dry_run:
            shutil.copy2(src, ARCHIVE_ROOT / a.slug / src.name)
        result = convert(src, target, a.dry_run)
        if result:
            dest, meta = result
            manifest[dest.name] = meta
            if a.in_place:
                src.unlink()   # the web-UI original is superseded

    if not a.dry_run:
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        print(f"\nWrote {manifest_path}")
        if not a.in_place:
            print(f"Masters archived to {ARCHIVE_ROOT / a.slug}/ (not committed).")
        print("Next: rename outputs to 01-…, 02-… and set `hero:` in the MDX frontmatter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

`photo-normalize.yml` then reduces to: checkout → `apt-get install -y imagemagick libheif1` →
`python3 scripts/ingest-photos.py --in-place content` → `git pull --rebase` → commit if dirty →
push → call the Pages build job.

---

## Risks and open items

| Risk | Severity | Mitigation |
|---|---|---|
| **GPS EXIF already committed** in the FTC iPhone 16 photo, in a public repo | **High — act now** | Strip on every published derivative. Note that removing it from *history* needs a rewrite (see below). |
| **Astro re-encodes the committed WebP**, causing generation loss (q80 → q80 twice) | Medium | Loss at 1600 px is small but real. Verify visually on one photo. If it matters, have Astro downscale only, or accept it — the 480/960 derivatives are viewed small enough that it will not show. |
| **Relative MDX image paths may not resolve** from `content/` outside `src/` | Medium | Smoke-test one page before authoring 17. Fixing the directory layout is cheap now, expensive later. |
| **Deploy silently stops firing** after the normalize Action's `GITHUB_TOKEN` push | Medium | Chain the Pages build inside the normalize workflow rather than on a separate `on: push` trigger. |
| **Masters archive discipline lapses** — Path C skipped, only Path A used | Medium | Script refuses to run without `ARCHIVE_ROOT`. But Path A/B do not archive at all, so iCloud remains the real backstop. Accept this; do not build more machinery. |
| **WebP-only breaks ~2.6% of browsers** | Low | Known and quantified. One-line Astro config change adds a JPEG fallback if it ever matters. |
| Normalize Action races a second web-UI commit | Low | `git pull --rebase` before push. Volume makes this near-impossible anyway. |
| Existing 20.7 MB of history for 5 photos | Low, but **cheapest to fix now** | The repo is 8 commits old. A `git filter-repo` to drop the HEIC blobs and oversized JPEGs is trivial today and infeasible in a year. **Decide now, not later.** Requires a force-push and coordination with the parallel work in flight. |
| `magick` is at `/usr/local/bin` (Intel path) while `cwebp`/`avifenc` are Homebrew arm64 | Low | Cross-arch install; works today but may need a native reinstall. `brew install imagemagick` resolves it. |

---

## Sources

- [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) — 50 MiB warning, 100 MiB hard block, 25 MiB browser upload, <1 GB ideal / <5 GB strongly recommended repo size
- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) — 1 GB published site, 100 GB/month soft bandwidth, 10 builds/hour soft (waived for custom Actions workflows)
- [Adding a file to a repository](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) — 25 MiB per file, 100 files per browser upload
- [Git LFS + GitHub Pages: any plans to support? (community discussion #50337)](https://github.com/orgs/community/discussions/50337) — official *"no plans to support Git LFS in GitHub Pages"*; the `actions/checkout` `lfs: true` workaround and the quota-exhaustion report
- [github pages serving the reference file instead of the actual binary (git-lfs#1342)](https://github.com/git-lfs/git-lfs/issues/1342) — the pointer-file behaviour
- [git-lfs doesn't work with GitHub Pages (git-lfs#3498)](https://github.com/git-lfs/git-lfs/issues/3498)
- [About storage and bandwidth usage (Git LFS)](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-storage-and-bandwidth-usage) — 10 GiB free storage and bandwidth on Free/Pro; pre-paid data packs removed in favour of metered billing
- [Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) — *"if a workflow run pushes code using the repository's `GITHUB_TOKEN`, a new workflow will not run"*
- [Astro: Images](https://docs.astro.build/en/guides/images/) — `image()` schema helper, markdown/MDX `![]()` optimization, `image.layout` / `image.responsiveStyles` automatic `srcset`, `public/` never optimized
- [WebP browser support in 2026](https://webhelpagency.com/blog/webp-browser-support/) — ~97.4% global
- [AVIF browser support in 2026](https://wildandfreetools.com/blog/avif-browser-support-2026-is-it-safe/) — ~94.9% global
- All size, dimension, and encoder measurements: taken 2026-08-23 against the 12 real images in
  `content/`, using `sips`, `magick` 7.1.0-48, `cwebp` 1.2.4, and `avifenc`, plus HEIC originals
  recovered from git history via `git cat-file -s`.


---

## History rewrite — DECLINED, 2026-08-27

Dmitri's decision: **do not rewrite history.** Closed; do not raise again.

The pre-strip version of `content/ftc-vanta-31000/photos/9356BC72…jpg` remains reachable in commit `925d2d04` carrying `GPSLatitude 29/1,45/1,1296/100` / `GPSLongitude 95/1,21/1,2675/100` (Houston — an FTC competition venue, not a private address). Five HEIC originals also remain in history.

**Consequences accepted:**
- Those coordinates stay publicly retrievable.
- `.git` stays at ~37 MB for 12 photos, and every future photo compounds it. This is a *repo* weight issue, not a *published site* weight issue — Pages serves the working tree, so it does not affect page load or the 1 GB site limit.

**Still in force:** EXIF is stripped from all photos going forward, and `-auto-orient` must precede `-strip`.
