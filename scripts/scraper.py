#!/usr/bin/env python3
"""
scraper.py — OpenAlex → publications.yaml pipeline

Fetches all works for John Shepherd (OpenAlex author A5069392685 /
ORCID 0000-0003-2280-2541), diffs against publications.yaml by DOI
(primary) and normalized title (fallback), and writes new entries to
new_papers_staging.yaml for classification + merge.

OpenAlex was chosen over Google Scholar because:
  - stable, documented free API (no CAPTCHAs / bot blocks)
  - reliable DOIs on most records
  - broad coverage (journals, conferences, preprints)
  - author disambiguation via ORCID

Requirements: pip install pyyaml requests
Run: python3 scripts/scraper.py
"""

import os
import re
import sys
import time
from datetime import datetime

import requests
import yaml

AUTHOR_ID = "A5069392685"               # John Shepherd, confirmed by ORCID + UH Mānoa affiliation
ORCID = "0000-0003-2280-2541"
OPENALEX_MAILTO = os.environ.get("OPENALEX_MAILTO", "jshepherd46@gmail.com")
PUBLICATIONS_FILE = "publications.yaml"
NEW_PAPERS_FILE = "new_papers_staging.yaml"
PAGE_SIZE = 200


def load_yaml(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def save_yaml(data, path):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def norm_title(t):
    return re.sub(r"\s+", " ", (t or "").lower().strip())


def norm_doi(d):
    if not d:
        return ""
    d = d.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "http://dx.doi.org/", "doi:"):
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d


def existing_index(pubs):
    dois = {norm_doi(p.get("doi")) for p in pubs if p.get("doi")}
    dois.discard("")
    titles = {norm_title(p.get("title")) for p in pubs if p.get("title")}
    titles.discard("")
    return dois, titles


def reconstruct_abstract(inverted):
    """OpenAlex returns abstracts as {word: [positions]}. Rebuild into prose."""
    if not inverted:
        return ""
    positions = []
    for word, idx_list in inverted.items():
        for i in idx_list:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)


def make_key(authors, year, title):
    """lastname-year-firstword, lowercase-hyphenated, stable across runs."""
    last = ""
    if authors:
        first_author = authors.split(",")[0].strip()
        # "Shepherd JA" → "shepherd"; "John A. Shepherd" → "shepherd"
        tokens = first_author.split()
        last = (tokens[-1] if len(tokens) > 1 and len(tokens[-1]) > 2 else tokens[0]).lower()
        last = re.sub(r"[^a-z]", "", last)
    first_word = ""
    if title:
        for w in title.lower().split():
            clean = re.sub(r"[^a-z0-9]", "", w)
            if clean and clean not in {"a", "an", "the", "of", "for", "and", "on", "in", "to"}:
                first_word = clean
                break
    parts = [p for p in (last, str(year) if year else "", first_word) if p]
    return "-".join(parts) or "unknown"


def format_authors(authorships):
    """OpenAlex authorships → 'Lastname FM, Lastname FM' bibliographic string."""
    names = []
    for a in authorships or []:
        author = a.get("author") or {}
        raw = author.get("display_name") or ""
        if not raw:
            continue
        tokens = raw.split()
        if len(tokens) == 1:
            names.append(tokens[0])
            continue
        last = tokens[-1]
        initials = "".join(t[0].upper() for t in tokens[:-1] if t and t[0].isalpha())
        names.append(f"{last} {initials}".strip())
    return ", ".join(names)


def parse_work(w):
    title = w.get("title") or w.get("display_name") or "Untitled"
    year = w.get("publication_year")
    authors = format_authors(w.get("authorships"))
    doi = norm_doi(w.get("doi"))

    host = (w.get("primary_location") or {}).get("source") or {}
    journal = host.get("display_name") or ""

    biblio = w.get("biblio") or {}
    volume = biblio.get("volume") or ""
    issue = biblio.get("issue") or ""
    first_page = biblio.get("first_page") or ""
    last_page = biblio.get("last_page") or ""
    if first_page and last_page and first_page != last_page:
        pages = f"{first_page}-{last_page}"
    else:
        pages = first_page or ""

    abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
    if len(abstract) > 500:
        abstract = abstract[:500] + "..."

    return {
        "key": make_key(authors, year, title),
        "title": title,
        "authors": authors,
        "year": int(year) if isinstance(year, int) or (isinstance(year, str) and year.isdigit()) else year,
        "journal": journal,
        "volume": str(volume) if volume else "",
        "issue": str(issue) if issue else "",
        "pages": pages,
        "doi": doi,
        "abstract": abstract,
        "openalex_id": w.get("id", "").rsplit("/", 1)[-1],
        "source_url": (w.get("primary_location") or {}).get("landing_page_url") or "",
        "tags": [],
        "added": datetime.today().strftime("%Y-%m-%d"),
        "notes": "AUTO-IMPORTED - tags required",
    }


def fetch_all_works(author_id):
    url = "https://api.openalex.org/works"
    params = {
        "filter": f"author.id:{author_id}",
        "per-page": PAGE_SIZE,
        "cursor": "*",
        "mailto": OPENALEX_MAILTO,
    }
    all_works = []
    page = 0
    while True:
        page += 1
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        batch = data.get("results", [])
        all_works.extend(batch)
        meta = data.get("meta") or {}
        print(f"  page {page}: +{len(batch):4d}  (total {len(all_works)} / {meta.get('count','?')})")
        next_cursor = meta.get("next_cursor")
        if not next_cursor or not batch:
            break
        params["cursor"] = next_cursor
        time.sleep(0.1)
    return all_works


def main():
    existing = load_yaml(PUBLICATIONS_FILE)
    print(f"Existing publications in {PUBLICATIONS_FILE}: {len(existing)}")
    known_dois, known_titles = existing_index(existing)

    print(f"Fetching works for OpenAlex author {AUTHOR_ID} (ORCID {ORCID})...")
    works = fetch_all_works(AUTHOR_ID)
    print(f"Retrieved {len(works)} works from OpenAlex.")

    new_papers, skipped_dup = [], 0
    seen_dois, seen_titles = set(), set()

    for w in works:
        parsed = parse_work(w)
        doi = parsed["doi"]
        tkey = norm_title(parsed["title"])
        if (doi and doi in known_dois) or (tkey and tkey in known_titles):
            skipped_dup += 1
            continue
        if (doi and doi in seen_dois) or (tkey and tkey in seen_titles):
            skipped_dup += 1
            continue
        if doi:
            seen_dois.add(doi)
        if tkey:
            seen_titles.add(tkey)
        new_papers.append(parsed)

    print(f"\nResults:")
    print(f"  Already in library: {skipped_dup}")
    print(f"  New papers found:   {len(new_papers)}")

    if new_papers:
        def year_key(p):
            try:
                return int(p.get("year"))
            except (TypeError, ValueError):
                return 0
        new_papers.sort(key=year_key, reverse=True)
        save_yaml(new_papers, NEW_PAPERS_FILE)
        print(f"\nNew papers written to: {NEW_PAPERS_FILE}")
        print("Next step: run classify.py to auto-propose tags, then review and merge.")
    else:
        print("\nNo new papers found. Library is up to date.")

    return len(new_papers)


if __name__ == "__main__":
    main()
    sys.exit(0)
