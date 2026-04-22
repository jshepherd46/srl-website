# AGENT.md — SRL Publications System
## Operating Manual for the Claude Code Webmaster Agent

This file tells you everything you need to know to manage the SRL publications pipeline.
Read this before taking any action on this repository.

---

## What This Repo Does

This repository manages publications for the Shepherd Research Lab website.
It is the canonical source of truth for all publications displayed at shepherdresearchlab.org.

**The pipeline:**
1. `publications.yaml` — master library of all publications with tags
2. `tags.yaml` — the classification taxonomy (study tags, research areas, modalities, cohorts)
3. `scripts/scraper.py` — finds new papers on Google Scholar
4. `scripts/classify.py` — uses Claude API to propose tags for new papers
5. `scripts/merge.py` — merges approved papers into publications.yaml
6. `scripts/build_pubs.py` — generates HTML pages, RIS, and BibTeX from the library

---

## Tasks You Can Do Autonomously

### Add a new publication manually
1. Open `publications.yaml`
2. Add the entry following the existing schema (key, title, authors, year, journal, doi, tags)
3. Use `tags.yaml` as the tag reference — only use tags that exist there
4. Run `python3 scripts/build_pubs.py` to verify it builds without errors
5. Commit and push — the site will rebuild automatically

### Run the discovery pipeline
```bash
python3 scripts/scraper.py          # find new papers
python3 scripts/classify.py         # auto-tag them
# Review classified_papers.yaml
python3 scripts/merge.py --auto     # merge if auto-approved
python3 scripts/build_pubs.py       # rebuild site
```

### Check papers for a specific tag
```bash
python3 scripts/build_pubs.py --tag hipimr
python3 scripts/build_pubs.py --tag body-composition
```

### Regenerate RIS/BibTeX exports only
```bash
python3 scripts/build_pubs.py --ris-only
```

---

## Tasks That Require John's Approval (via Slack)

- Adding a new tag to `tags.yaml`
- Removing or renaming an existing tag
- Changing the tags on existing publications
- Removing a publication from the library
- Any changes to the build scripts themselves

**When in doubt, ask.**

---

## Tag Rules

- A paper must have at least ONE research area tag (`breast-density`, `body-composition`, etc.)
- Study tags (`hipimr`, `shape-up`, etc.) should only be applied when the paper explicitly
  uses data from or was produced by that study
- Multiple tags are encouraged — err toward more tags rather than fewer
- Never invent tags not in `tags.yaml` — add them to the taxonomy first

---

## Data Schema for publications.yaml

```yaml
- key: lastname-year-shortword        # unique identifier, lowercase-hyphenated
  title: "Full paper title"
  authors: "Last F, Last F, ..."      # comma-separated, standard bibliographic format
  year: 2024                          # integer
  journal: "Journal Name"             # or conference name
  volume: "7"                         # string or empty
  pages: "298"                        # or "1-12" format
  doi: "10.1038/s41746-024-01289-0"   # without https://doi.org/ prefix
  abstract: "First 500 chars..."      # optional, truncate long abstracts
  scholar_url: "https://..."          # Google Scholar link if available
  tags:
    - body-composition
    - dxa
    - shape-up
  added: "2025-04-21"                 # ISO date when added to library
  notes: ""                           # optional internal notes
```

---

## What NOT to Do

- Do not delete `publications_backup_*.yaml` files for 30 days
- Do not modify `publications.yaml` without running build_pubs.py to verify
- Do not push directly to main if you have unreviewed papers — open a PR instead
- Do not change the RIS or BibTeX output files directly — they are generated artifacts

---

## Environment Variables Required

- `ANTHROPIC_API_KEY` — for classify.py (set in GitHub Actions secrets)
- `GITHUB_TOKEN` — auto-provided by GitHub Actions

---

## Contact

This system is managed for John Shepherd (johnshep@hawaii.edu)
University of Hawaiʻi Cancer Center
