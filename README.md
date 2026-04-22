# Shepherd Research Lab — Site Repo

Static Jekyll site for [shepherdresearchlab.org](https://shepherdresearchlab.org), hosted on GitHub Pages.

This repo houses two independent concerns that share the same home:
- **Website** (Jekyll) — source of the public site. Everything described below.
- **Publications pipeline** (Python) — monthly OpenAlex → Claude classify → YAML → HTML/RIS/BibTeX. See `AGENT.md` and `scripts/`.

The two don't interfere: Jekyll's `exclude:` in `_config.yml` keeps the pipeline's files out of the site build, and the pipeline writes its rendered HTML into a `publications/` directory that Jekyll then serves normally.

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
