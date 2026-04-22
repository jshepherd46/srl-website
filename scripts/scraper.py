#!/usr/bin/env python3
"""
scraper.py — Google Scholar → publications.yaml pipeline
Fetches all publications from John Shepherd's Scholar profile,
diffs against the existing publications.yaml, and outputs new
entries for review/tagging.

Requirements: pip install scholarly pyyaml
Run: python3 scraper.py
"""

import json
import yaml
import sys
import os
import hashlib
from datetime import datetime
from scholarly import scholarly

SCHOLAR_ID = "1r51d_AAAAAJ"
PUBLICATIONS_FILE = "publications.yaml"
NEW_PAPERS_FILE = "new_papers_staging.yaml"


def load_existing(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return yaml.safe_load(f) or []


def make_key(title):
    """Generate a stable key from title."""
    clean = title.lower().strip()
    words = clean.split()[:4]
    return "-".join(w.strip(".,;:") for w in words)


def doi_exists(existing, doi):
    if not doi:
        return False
    return any(p.get("doi", "").lower() == doi.lower() for p in existing)


def title_exists(existing, title):
    clean = title.lower().strip()
    return any(p.get("title", "").lower().strip() == clean for p in existing)


def fetch_scholar_publications(scholar_id):
    print(f"Connecting to Google Scholar (ID: {scholar_id})...")
    author = scholarly.search_author_id(scholar_id)
    print(f"Found: {author.get('name', 'Unknown')}")
    print("Filling publication list (this may take a minute)...")
    author = scholarly.fill(author, sections=["publications"])
    pubs = author.get("publications", [])
    print(f"Found {len(pubs)} publications on Scholar profile.")
    return pubs


def parse_scholar_pub(pub):
    """Convert a scholarly pub object to our YAML schema."""
    bib = pub.get("bib", {})
    
    title = bib.get("title", "Untitled")
    authors = bib.get("author", "")
    year = bib.get("pub_year", "")
    journal = bib.get("journal", bib.get("booktitle", ""))
    volume = bib.get("volume", "")
    pages = bib.get("pages", "")
    abstract = bib.get("abstract", "")
    
    # Try to get DOI - scholarly sometimes has it
    doi = pub.get("pub_url", "")
    if "doi.org" in doi:
        doi = doi.split("doi.org/")[-1]
    else:
        doi = ""
    
    scholar_url = f"https://scholar.google.com/citations?view_op=view_citation&user={SCHOLAR_ID}&citation_for_view={pub.get('author_pub_id', '')}"
    
    key = make_key(title)
    
    return {
        "key": key,
        "title": title,
        "authors": authors,
        "year": int(year) if str(year).isdigit() else year,
        "journal": journal,
        "volume": volume,
        "pages": pages,
        "doi": doi,
        "abstract": abstract[:500] + "..." if len(abstract) > 500 else abstract,
        "scholar_url": scholar_url,
        "tags": [],  # To be filled by classify.py or manually
        "added": datetime.today().strftime("%Y-%m-%d"),
        "notes": "AUTO-IMPORTED - tags required"
    }


def main():
    existing = load_existing(PUBLICATIONS_FILE)
    print(f"Existing publications in {PUBLICATIONS_FILE}: {len(existing)}")
    
    scholar_pubs = fetch_scholar_publications(SCHOLAR_ID)
    
    new_papers = []
    skipped = 0
    
    for pub in scholar_pubs:
        bib = pub.get("bib", {})
        title = bib.get("title", "")
        doi = pub.get("pub_url", "")
        
        if doi_exists(existing, doi) or title_exists(existing, title):
            skipped += 1
            continue
        
        parsed = parse_scholar_pub(pub)
        new_papers.append(parsed)
    
    print(f"\nResults:")
    print(f"  Already in library: {skipped}")
    print(f"  New papers found:   {len(new_papers)}")
    
    if new_papers:
        # Sort by year descending
        def _year_key(p):
            y = p.get("year")
            try:
                return int(y)
            except (TypeError, ValueError):
                return 0
        new_papers.sort(key=_year_key, reverse=True)
        
        with open(NEW_PAPERS_FILE, "w", encoding="utf-8") as f:
            yaml.dump(new_papers, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        print(f"\nNew papers written to: {NEW_PAPERS_FILE}")
        print("Next step: run classify.py to auto-propose tags, then review and merge.")
        print("\nNew paper titles:")
        for p in new_papers:
            line = f"  [{p['year']}] {p['title'][:80]}"
            try:
                print(line)
            except UnicodeEncodeError:
                sys.stdout.buffer.write(line.encode("utf-8", errors="replace") + b"\n")
    else:
        print("\nNo new papers found. Library is up to date.")
    
    return len(new_papers)


if __name__ == "__main__":
    main()
    sys.exit(0)
