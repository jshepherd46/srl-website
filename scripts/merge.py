#!/usr/bin/env python3
"""
merge.py — Merge reviewed/classified papers into publications.yaml
Run after reviewing classified_papers.yaml.
Deduplicates by DOI and title before merging.

Usage: python3 merge.py [--auto]
  --auto: skip confirmation prompt (for agent use)
"""

import yaml
import sys
import os
from datetime import datetime

PUBLICATIONS_FILE = "_data/publications.yaml"
CLASSIFIED_FILE = "classified_papers.yaml"
BACKUP_FILE = f"publications_backup_{datetime.today().strftime('%Y%m%d')}.yaml"


def load_yaml(filepath):
    with open(filepath, "r") as f:
        return yaml.safe_load(f) or []


def save_yaml(data, filepath):
    """Dump YAML with a blank line between top-level list items for readability.

    yaml.dump does not emit blank separators between list items natively, so
    we post-process the dumped string and insert one blank line before each
    top-level `- ` marker (except the first). The blank lines are pure
    whitespace that yaml.safe_load ignores, so this only changes the on-disk
    shape — not what any consumer loads.
    """
    text = yaml.dump(
        data,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
    lines = text.split("\n")
    out = []
    for i, line in enumerate(lines):
        # Top-level list items start with "- " at column 0; nested items are
        # indented by two+ spaces.
        if i > 0 and line.startswith("- ") and out and out[-1] != "":
            out.append("")
        out.append(line)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(out))


def doi_exists(existing, doi):
    if not doi:
        return False
    return any(p.get("doi", "").lower().strip() == doi.lower().strip() for p in existing)


def title_exists(existing, title):
    clean = title.lower().strip()
    return any(p.get("title", "").lower().strip() == clean for p in existing)


def main():
    auto = "--auto" in sys.argv
    
    if not os.path.exists(CLASSIFIED_FILE):
        print(f"No classified file found at {CLASSIFIED_FILE}")
        return
    
    existing = load_yaml(PUBLICATIONS_FILE) if os.path.exists(PUBLICATIONS_FILE) else []
    new_papers = load_yaml(CLASSIFIED_FILE)
    
    print(f"Existing publications: {len(existing)}")
    print(f"Classified papers to merge: {len(new_papers)}")
    
    # Check for untagged papers
    untagged = [p for p in new_papers if not p.get("tags")]
    if untagged and not auto:
        print(f"\nWarning: {len(untagged)} papers have no tags:")
        for p in untagged:
            print(f"  - {p['title'][:70]}")
        resp = input("\nContinue anyway? (y/n): ")
        if resp.lower() != "y":
            print("Aborted. Add tags to classified_papers.yaml and retry.")
            return
    
    to_add = []
    skipped = []
    
    for paper in new_papers:
        if doi_exists(existing, paper.get("doi")) or title_exists(existing, paper.get("title", "")):
            skipped.append(paper["title"][:60])
        else:
            to_add.append(paper)
    
    if skipped:
        print(f"\nSkipping {len(skipped)} duplicates already in library.")
    
    if not to_add:
        print("Nothing new to add.")
        return
    
    print(f"\nReady to add {len(to_add)} papers to {PUBLICATIONS_FILE}:")
    for p in to_add:
        print(f"  [{p.get('year','')}] {p['title'][:70]}")
        print(f"    Tags: {p.get('tags', [])}")
    
    if not auto:
        resp = input("\nConfirm merge? (y/n): ")
        if resp.lower() != "y":
            print("Aborted.")
            return
    
    # Backup existing
    if os.path.exists(PUBLICATIONS_FILE):
        import shutil
        shutil.copy(PUBLICATIONS_FILE, BACKUP_FILE)
        print(f"Backup saved: {BACKUP_FILE}")
    
    # Merge and sort by year descending
    merged = existing + to_add
    merged.sort(key=lambda p: (p.get("year") or 0), reverse=True)
    
    save_yaml(merged, PUBLICATIONS_FILE)
    
    # Clean up staging files
    os.remove(CLASSIFIED_FILE)
    if os.path.exists("new_papers_staging.yaml"):
        os.remove("new_papers_staging.yaml")
    
    print(f"\nDone. {len(to_add)} papers added. Total library: {len(merged)} publications.")
    print(f"Staging files cleaned up.")


if __name__ == "__main__":
    main()
