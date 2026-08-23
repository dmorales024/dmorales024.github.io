# Stack research — what builds this site

Research for issue #5. Read-only brief; nothing implemented. Verified against live docs and the npm registry on **2026-08-23**.

Inputs that constrain this: [#2 project inventory](project-inventory.md), [#3 ordering and navigation](ordering-and-navigation.md), [#4 detail page model](detail-page-model.md). Issue #6 owns the image pipeline; this brief stops at "which framework's image story is credible" and does not specify formats, sizes, or budgets.

---

## Recommendation

**Astro 7, with `@astrojs/mdx`, content collections over a folder-per-project layout, and deployment via `withastro/action@v6` + `actions/deploy-pages`.**

It is the only option on the list where every hard requirement is a first-party, documented feature rather than an assembly job:

- **#1 (prose and images as one document)** is Astro's core content model, not a plugin. A content collection of `.mdx` files renders to a `<Content />` component; relative `![alt](./photo.jpg)` inside that body is picked up by the build and optimized. Nothing else on the list gives image optimization *inside markdown body syntax* for free.
- **#3 (embeds in the body)** is MDX: import a `<YouTube />` or `<ModelViewer />` `.astro` component at the top of the file and drop it mid-prose. The component can be static HTML (an nocookie iframe needs no JS), so the page ships zero JavaScript unless a viewer actually needs it.
- **#2 (four-field frontmatter)** is a ten-line Zod schema in `src/content.config.ts` that fails the build on a typo. `slug` comes from the directory name via the glob loader.
- **#5 (17 pages, no search/filter/tags/dates)** — Astro is content-shaped and adds nothing here. No router, no client bundle, no hydration by default.
- **#4 (user site at root)** — set `site: 'https://dmorales024.github.io'` and **omit `base` entirely**. Root deployment is the simple case.

The real cost is that React familiarity from Mondo's mostly does not transfer, and Dmitri would learn `.astro` syntax. That syntax is JSX-shaped markup with frontmatter-style script at the top — close enough to Angular templates and to the JSX he is already learning that the ramp is days, not weeks. Against that: the Mondo's stack cannot do requirement #1 without him hand-building an MDX-plus-image-optimization pipeline and maintaining it alone for years. Reuse value is real but it is reuse of the *wrong shape* — Mondo's is an app with data files; this is documents with pictures.

**Second choice, if the Astro learning curve is rejected:** Vite + React Router v8 (the Mondo's path) with `@mdx-js/rollup` and `vite-imagetools`. It works. It is roughly three integration decisions Dmitri owns forever instead of zero.

---

## Options compared

Judged against: **#1** markdown/MDX body with interleaved images · **#2** four-field frontmatter · **#3** body embeds · **#4** static, user site at root · **#5** genuinely simple, no cut features re-added · **#6** photo-heavy, image optimization credible · **#7** two card sizes driven by `rank`.

### Astro 7.2.4 (latest, released 6.x → 7.0 on 2026-06-22)

| Req | Verdict |
|---|---|
| #1 | **Best in class.** Content collections + `glob()` loader; `render(entry)` returns `<Content />`. Markdown `![]()` on local images is optimized by the build; `public/` images are not (so co-locate under `src/`). |
| #2 | Zod schema in `src/content.config.ts`; build fails on schema violation. Exactly the four fields, nothing optional. |
| #3 | MDX: import components, use them inline. `components` prop can also remap markdown elements (e.g. every `<img>` in every body → one wrapper component). |
| #4 | Documented first-party path. `site` set, `base` omitted for a user site. |
| #5 | Zero-JS by default. Nothing to disable. |
| #6 | Sharp is the default image service (no install step since 6.1). `<Image />` / `<Picture />`, `image.layout` for responsive `srcset`/`sizes`, `image.responsiveStyles`. Detail is #6's call. |
| #7 | `rank` from frontmatter → a class on the card in the grid `.astro` file. Trivial either way. |

**Watch items for v7 specifically.** Two of the three headline v7 changes touch exactly this project:
- **Sätteri** — a Rust markdown/MDX pipeline replaced remark/rehype as the default. It has GFM, smart punctuation, and math built in. If a needed remark/rehype plugin has no Sätteri equivalent, install `@astrojs/markdown-remark` and configure the unified pipeline explicitly. This site needs almost no plugins, so the exposure is low — but Sätteri is ~2 months old.
- **Rust `.astro` compiler** — strict about HTML. Unclosed tags now error instead of being auto-corrected. This only bites during authoring of layout components, and errors loudly rather than silently.
- Node 22+ (from v6). Vite 8 / Rolldown under the hood.
- If either bites, **pinning to Astro 6.x is a legitimate fallback** — same content collections API, same MDX story, remark/rehype still default.

**Governance note:** Cloudflare acquired The Astro Technology Company in January 2026. Public commitments: MIT license, open governance, platform-agnostic (no Cloudflare lock-in), team employed full-time on Astro. For a personal archive with a 5-year horizon this reads as *more* maintenance funding, not less — but it is a single-vendor dependency now, and worth recording as a known unknown.

### Vite + React Router v8 (the Mondo's path)

Correction to the ticket framing: **Mondo's is on React Router `^8` and Vite `^8` today**, not v7. `ssr: false` + `prerender: true`, output `build/client/`, deployed to S3/CloudFront.

| Req | Verdict |
|---|---|
| #1 | **Requires assembly.** No content model exists. Add `@mdx-js/rollup`, import each `.mdx` as a component, glob them with `import.meta.glob`. Images in the body: MDX turns `![]()` into `<img src="./photo.jpg">` with a **string** src — Vite will not hash or optimize it. You either add `vite-imagetools` and stop using markdown image syntax (import + `<Image>` per photo), or write a rehype plugin that rewrites relative image paths into imports. The second is the right answer and it is a plugin Dmitri owns. |
| #2 | Frontmatter needs `remark-frontmatter` + `remark-mdx-frontmatter` and validation is hand-rolled (or Zod, manually invoked). No build-time guarantee unless he writes the check. |
| #3 | Fine — MDX with React components is the one thing this stack does natively. |
| #4 | Prerender emits one HTML file per route; works at root. Needs `404.html` and the standard GitHub Pages SPA-redirect shim **only if** he wants client-side routing to survive deep-link 404s; with full prerendering + `.html` files GitHub Pages serves the real files, so a plain `404.html` is enough. |
| #5 | Ships React + React Router to the client for a site with no interactivity beyond hover and scroll. This is the SPA-emitting-static-pages tax the ticket warns about. |
| #6 | No built-in image optimization. `vite-imagetools` or `unplugin-imagemin`, configured by hand, plus `<picture>` markup written by hand. This is the biggest gap. |
| #7 | Trivial. He already built a flip-card grid; the card *feel* is portable as CSS regardless of framework. |

Honest reading: three owned integrations (MDX loading, frontmatter validation, image optimization) versus zero. For a site he touches twice a year, "owned integration" means "thing that breaks on a dependency bump when he has forgotten how it works."

### Next.js 16.3.2, `output: 'export'`

| Req | Verdict |
|---|---|
| #1 | Workable via `@next/mdx` or Content Collections/Contentlayer-style tooling, but the ecosystem here has churned repeatedly (Contentlayer unmaintained, successors varied). |
| #6 | **Disqualifying friction.** `next/image` optimization is a *runtime server API*. With `output: 'export'` you must set `images: { unoptimized: true }` — source files pass through as-is, no resize, no WebP — or bolt on `next-image-export-optimizer` / a Cloudinary loader. For a site whose entire point is photos, the flagship feature is the one that doesn't work. |
| #5 | App Router, RSC, caching semantics, middleware — a large surface for 18 pages. |
| #4 | Static export to root works; `.nojekyll` matters here because Next emits `_next/`. |

Rejected. Heaviest option, worst image story of the four.

### Eleventy 3.1.6 (v4 is `4.0.0-alpha.10`, canary only)

| Req | Verdict |
|---|---|
| #1 | Markdown-native, and **shortcodes satisfy #3 without MDX** — markdown files are preprocessed as Liquid, so `{% youtube "id" %}` works inline. This is a genuinely good answer to the embed requirement. |
| #2 | Frontmatter is native. Schema validation is not — no Zod equivalent, so a typo'd `status` silently produces a broken card. Writable as a build-time check he owns. |
| #3 | Shortcodes: yes. MDX: supported as a language, but it uses Remark instead of Eleventy's markdown-it, requires ESM, and is not preprocessed by Liquid — i.e. mixing MDX and shortcodes in the same project is two parallel authoring models. Pick one. |
| #6 | `@11ty/eleventy-img` v7 is capable (Sharp under the hood) but is **opt-in per image via shortcode**. Plain `![alt](photo.jpg)` in a body is *not* optimized unless he wires a markdown-it rule. That is exactly requirement #1's authoring surface. |
| #4 | Cleanest deploy of the lot — plain files, no framework opinions. |
| #5 | Lightest tool here. Genuinely simple. |

The strongest non-Astro contender on philosophy — smallest tool, longest-lived, no client JS at all. It loses on the intersection of #1 and #6: getting *body images optimized automatically* is the thing Astro does out of the box and Eleventy makes you build. Also v4 has been in alpha for a while; committing to 3.x means committing to a version line that will eventually be superseded.

### Plain Markdown, no framework

Markdown-it or similar in a small Node script, plus a template engine. Requirement #3 forces you to invent a shortcode syntax; requirement #6 forces you to invent an image pipeline; #2 forces you to invent schema validation. You end up with a worse Eleventy that only Dmitri knows how to operate. **Rejected** — the ceremony saved at build-config time is repaid with interest at every future change.

---

## What adding project #18 looks like (Astro)

A year from now, from a cold start. This is the criterion that decides it.

1. `mkdir src/content/projects/rotom`
2. Drop photos in `src/content/projects/rotom/` (or a `photos/` subfolder — the collection glob only matches `.mdx`, so images alongside are just files).
3. Create `src/content/projects/rotom/index.mdx`:

   ```mdx
   ---
   title: Rotom
   status: complete
   hero: ./cover.jpg
   rank: 3
   ---
   import YouTube from '../../../components/YouTube.astro';

   I needed a cover for the circuit breaker panel...

   ![The stock tacked down on the wamboo](./setup.jpg)

   ...and then the first cut went exactly as badly as you'd expect.

   <YouTube id="abc123" />
   ```
4. Bump the `rank` of anything it displaces (the one genuinely manual step, and it is inherent to #3's curated ordering, not to the stack).
5. `npm run dev`, look at it, commit, push. Actions builds and deploys.

**Files touched: one new folder, plus `rank` edits in a few sibling files. Zero code changes.** No route registration, no index/manifest to update, no import to add anywhere — `getCollection('projects')` picks it up, sorts by `rank`, and `[...slug].astro` generates the page. That is the whole argument.

For comparison, the same operation on the Vite + React Router path: new folder, new `.mdx`, and then verify the glob picked it up, verify the frontmatter shape by hand (no schema), and per-photo decide whether it goes through markdown syntax (unoptimized) or an explicit import (optimized) — an authoring decision he has to re-learn each time.

### Suggested shape (not a spec — that's a later ticket)

```
src/
  content.config.ts          # 4-field Zod schema, glob loader
  content/projects/
    bme290/index.mdx + photos
    rotom/index.mdx  + photos
    ... 17 of these
  pages/
    index.astro              # the grid; getCollection, sort by rank, size by rank
    projects/[...slug].astro # getStaticPaths from the collection
  components/                # Card, YouTube, ModelViewer
  layouts/
```

**Verify before committing to this layout:** the docs state `glob()` derives ids with `github-slugger` from the path relative to `base`, but do **not** document index-file handling — so `rotom/index.mdx` may produce the id `rotom` or `rotom/index`. The `generateId` callback is the documented escape hatch and makes it deterministic either way. Confirm empirically in the first spike.

Also: keep content under `src/`, not a repo-root `content/`. Image optimization applies to images under `src/`; `public/` images are explicitly never processed.

---

## Deployment — GitHub Pages user site

**Use GitHub Actions, not a branch.** Set Settings → Pages → Source to *GitHub Actions*. Branch-based publishing (`gh-pages`, or `/docs` on `main`) means committing build output to the repo — noise in every diff, and the sole reason it ever existed (no CI) no longer applies.

Astro's documented workflow:

```yaml
# .github/workflows/deploy.yml  (shape, from the Astro deploy guide)
on:
  push: { branches: [main] }
  workflow_dispatch:
permissions: { contents: read, pages: write, id-token: write }
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
      - uses: withastro/action@v6      # installs deps, builds, uploads the artifact
  deploy:
    needs: build
    environment: github-pages
    steps:
      - uses: actions/deploy-pages@v5
```

**User-site specifics:**

- **Root path confirms as the simple case.** `site: 'https://dmorales024.github.io'`, and **no `base`**. Every base-path bug class (broken assets on a subpath, links needing a prefix, `import.meta.env.BASE_URL` threading) simply does not exist here. This is a real advantage of a user site over a project site and it applies to every option in this brief.
- **`.nojekyll`:** the Actions-artifact deploy path does not run Jekyll — the artifact is served as-is — so it should be unnecessary. It also costs nothing: an empty `public/.nojekyll` is one file and removes the entire question. Astro's own deploy guide does not mention it. **Recommendation: add it anyway.** It is the cheapest possible insurance against underscore-prefixed build output (`_astro/`) being swallowed.
- **`_astro/`** is where Astro puts hashed assets — the exact directory Jekyll would ignore. See above.
- The repo must be named exactly `dmorales024.github.io` and be public (it is).
- A concurrency group (`group: pages, cancel-in-progress: false`) is worth adding if pushes ever land close together.
- Build time is not a constraint here, but node_modules caching in the workflow is free and worth it.

---

## Risks and open questions

| Risk | Assessment |
|---|---|
| **Astro 7 is ~2 months old and swapped its markdown engine** | Real. Sätteri replaced remark/rehype as default in June 2026. This site needs few or no markdown plugins, which is the low-exposure case. Mitigation: `@astrojs/markdown-remark` restores the unified pipeline; failing that, Astro 6.x has the same content-collections and MDX APIs. **Decide at spike time whether to start on 7 or 6.** |
| **Learning curve** | `.astro` files are new. Mitigated by: no client-side state, no hydration, ~4 components total. The React knowledge from Mondo's is not wasted — Astro can render React islands via `@astrojs/react` if a CAD/3D viewer needs one. |
| **Card feel from Mondo's** | The flip-card is CSS and a tiny bit of interaction. It ports to any of these stacks. Not a differentiator — do not let it be one. |
| **CAD / 3D viewer embeds** | Unresolved. `<model-viewer>` is a web component and drops into MDX cleanly; anything heavier becomes a React or Svelte island. **Open: which projects actually need a 3D viewer, and what format the files are in.** Worth answering before the first build, because "a React island exists" changes the `@astrojs/react` decision. |
| **Overlap with #6** | This brief asserts only that Astro's image story is first-party and Sharp-backed. Formats, sizes, `image.layout` choice, hero vs body treatment, and whether PDFs-as-renders (`bme290`) need a separate path are #6's. **Flag: `bme290`'s best assets are PDF renders, which no framework image pipeline handles — they need converting to raster at intake.** That is an intake question (#10), not a stack question, but the stack choice does not rescue it. |
| **`hero` field type** | #4 specifies `hero` as a filename. In Astro the natural encoding is Zod's `image()` helper, which validates the path and hands back optimized-image metadata — a strictly better version of "filename". Does not change the four-field count; does change the field's type. **Open for #4 or the implementation ticket.** |
| **Cloudflare stewardship of Astro** | Publicly committed to MIT + open governance + platform-agnostic. Low risk over the archive's horizon, but it is now a single-company project. Recorded, not acted on. |
| **Eleventy v4** | Still `4.0.0-alpha.10`. Not a reason to avoid Eleventy, but it means the Eleventy path starts on a version line with a known future migration. |

---

## Sources

Verified 2026-08-23. Version numbers from the npm registry the same day: `astro@7.2.4`, `@astrojs/mdx@7.0.7`, `@astrojs/react@6.0.4`, `next@16.3.2`, `react-router@8.3.0`, `@11ty/eleventy@3.1.6` (canary `4.0.0-alpha.10`), `@11ty/eleventy-img@7.0.0`, `sharp@0.35.3`.

- Astro 7.0 release — https://astro.build/blog/astro-7/
- Astro v7 upgrade guide (breaking changes, Sätteri) — https://docs.astro.build/en/guides/upgrade-to/v7/
- Astro 6.0 release (Node 22, live collections) — https://astro.build/blog/astro-6/
- Astro — Deploy to GitHub Pages — https://docs.astro.build/en/guides/deploy/github/
- Astro — Content collections — https://docs.astro.build/en/guides/content-collections/
- Astro — Content loader reference (`glob()`, `generateId`) — https://docs.astro.build/en/reference/content-loader-reference/
- Astro — Images (markdown/MDX, responsive, `public/` not optimized) — https://docs.astro.build/en/guides/images/
- Astro — Configuration reference (`site`, `base`, `image.*`) — https://docs.astro.build/en/reference/configuration-reference/
- Astro — `@astrojs/mdx` integration — https://docs.astro.build/en/guides/integrations-guide/mdx/
- The Astro Technology Company joins Cloudflare — https://astro.build/blog/joining-cloudflare/
- React Router — Pre-rendering — https://reactrouter.com/how-to/pre-rendering
- Eleventy — MDX — https://www.11ty.dev/docs/languages/mdx/
- Eleventy — Shortcodes — https://www.11ty.dev/docs/shortcodes/
- Eleventy — Release history — https://www.11ty.dev/docs/versions/
- Next.js static export + image optimization discussion — https://github.com/vercel/next.js/discussions/60977
- `next-image-export-optimizer` — https://github.com/Niels-IO/next-image-export-optimizer
- `dmorales024/mondos` — README, `package.json`, `docs/adr/0002-frontend-stack.md` (inspected via `gh`)
