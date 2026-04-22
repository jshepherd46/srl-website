# Shepherd Research Lab — Site Repo

Static Jekyll site for [shepherdresearchlab.org](https://shepherdresearchlab.org), hosted on GitHub Pages.

This repo houses two independent concerns that share the same home:
- **Website** (Jekyll) — source of the public site. Everything described below.
- **Publications pipeline** (Python) — monthly OpenAlex → Claude classify → YAML → HTML/RIS/BibTeX. See `AGENT.md` and `scripts/`.

The two don't interfere: Jekyll's `exclude:` in `_config.yml` keeps the pipeline's files out of the site build, and the pipeline writes its rendered HTML into a `publications/` directory that Jekyll then serves normally.

## Migration status

Mid-migration from WordPress. The old WP site remains canonical at the custom domain; this Jekyll site is a staging ground at `https://jshepherd46.github.io/shepherdresearchlab/` until content is complete and DNS is cut over.

- ✅ Scaffold — Jekyll config, layouts, includes, stylesheet (UH Mānoa green)
- 🟡 Content — homepage migrated (pilot); 36 pages remaining (`about/`, `team/`, `contact/`, research pages, 18 team-member pages, etc.)
- ⬜ Services — Mailchimp / Formspree embeds not yet wired
- ⬜ Publications pipeline handoff — pipeline runs monthly and emits YAML/HTML/RIS/BibTeX; output is not yet routed into the Jekyll site's `publications/` path
- ⬜ DNS cutover — custom domain `shepherdresearchlab.org` still points at the WordPress host

## Content conventions

- **URL preservation.** We match WordPress URLs where feasible. Keeping permalinks stable means existing external links (papers, partner sites, search engines) still resolve after DNS cutover. This is why subdomains (`blog.`, `shapeup.`, `aiphi.`) stay on WordPress for now — migrating them would mean a second-phase URL discussion.
- **Images live at `wp-content/uploads/YYYY/MM/` at the repo root**, not under `/assets/`. That mirrors WP's original image URLs, so a link like `shepherdresearchlab.org/wp-content/uploads/2022/03/figure.png` keeps working after cutover. Reference from Markdown as `{{ site.baseurl }}/wp-content/uploads/…`.
- **Content extraction.** The old WP site is built with Elementor (a visual page builder), which produces nested widget markup that doesn't convert cleanly to Markdown by scraping. We extract page content via AI-assisted fetch and write it as simple Markdown inside HTML section wrappers. See `index.html` for the pattern — each section is `<section class="section">…<div class="container" markdown="1">…Markdown…</div></section>`, alternating with `.section--alt` for visual separation.

## How to update content

### Homepage
Edit `index.html`.

### Inner pages
Each lives at its own path (e.g. `about/index.html`, `team/index.html`). Pages use the single layout `_layouts/default.html`.

### Team, sponsors, etc.
Data-driven — edit YAML files in `_data/` instead of HTML. (Populated during Phase 2 of the migration.)

### Navigation
Edit the `nav:` list in `_config.yml`.

## Local development

```bash
bundle install
bundle exec jekyll serve
# Open http://localhost:4000/shepherdresearchlab/
```

## Services wired into the site

- **Newsletter** — Mailchimp embed (placeholder until Phase 3)
- **Contact form** — Formspree (placeholder until Phase 3)
- **Join A Study form** — Formspree (placeholder until Phase 3)

API keys / form IDs live in the embed snippets; subscribers and submissions live in the respective services, never in this repo.

## Deployment

Push to `main` → GitHub Pages builds automatically.

Currently served at: `https://jshepherd46.github.io/shepherdresearchlab/`

To cut over the custom domain (later phase):
1. Add a `CNAME` file to this repo containing: `shepherdresearchlab.org`
2. In GitHub repo Settings → Pages → Custom domain: enter `shepherdresearchlab.org`
3. Update DNS at the registrar: CNAME `www` → `jshepherd46.github.io`; A records for apex → GitHub Pages IPs (`185.199.108.153`, `.109.153`, `.110.153`, `.111.153`)
