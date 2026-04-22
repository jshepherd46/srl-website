#!/usr/bin/env python3
"""
build_pubs.py — Generate HTML, RIS, and BibTeX from publications.yaml
Run as part of the site build, or standalone to preview outputs.

Usage:
  python3 build_pubs.py                  # build all outputs
  python3 build_pubs.py --tag hipimr     # preview papers for a specific tag
  python3 build_pubs.py --ris-only       # generate RIS export only

Outputs:
  _site/publications/index.html         Full publication list
  _site/publications/[tag].html         Per-tag filtered pages
  _site/publications/publications.ris   EndNote/Zotero/Mendeley import
  _site/publications/publications.bib   BibTeX/LaTeX import
"""

import yaml
import os
import sys
import re
from datetime import datetime

PUBLICATIONS_FILE = "publications.yaml"
TAGS_FILE = "tags.yaml"
OUTPUT_DIR = "_site/publications"


def load_yaml(filepath):
    with open(filepath, "r") as f:
        return yaml.safe_load(f) or []


def slugify(text):
    return re.sub(r"[^a-z0-9-]", "", text.lower().replace(" ", "-"))


def format_authors_html(authors_str):
    """Bold 'Shepherd' in author list."""
    if not authors_str:
        return ""
    parts = [a.strip() for a in authors_str.split(",")]
    formatted = []
    for part in parts:
        if "Shepherd" in part:
            formatted.append(f"<strong>{part}</strong>")
        else:
            formatted.append(part)
    return ", ".join(formatted)


def pub_to_html_entry(pub):
    title = pub.get("title", "Untitled")
    authors = format_authors_html(pub.get("authors", ""))
    year = pub.get("year", "")
    journal = pub.get("journal", "")
    volume = pub.get("volume", "")
    pages = pub.get("pages", "")
    doi = pub.get("doi", "")
    
    # Build citation string
    cite_parts = []
    if journal:
        cite_parts.append(f"<em>{journal}</em>")
    if volume:
        cite_parts.append(f"vol. {volume}")
    if pages:
        cite_parts.append(f"pp. {pages}")
    if year:
        cite_parts.append(f"({year})")
    
    citation = ". ".join(filter(None, cite_parts))
    
    doi_link = ""
    if doi:
        doi_clean = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "")
        doi_link = f'<a href="https://doi.org/{doi_clean}" target="_blank" class="pub-doi">DOI: {doi_clean}</a>'
    
    tags_html = " ".join(
        f'<span class="pub-tag">{t}</span>' for t in pub.get("tags", [])
    )
    
    return f"""<div class="publication-entry" data-tags="{' '.join(pub.get('tags', []))}">
  <div class="pub-title">{title}</div>
  <div class="pub-authors">{authors}</div>
  <div class="pub-citation">{citation}</div>
  {f'<div class="pub-doi-line">{doi_link}</div>' if doi_link else ''}
  <div class="pub-tags">{tags_html}</div>
</div>"""


def generate_html(publications, tag=None, tag_label=None):
    if tag:
        pubs = [p for p in publications if tag in p.get("tags", [])]
        title = f"{tag_label or tag} — Publications"
        heading = f"Publications: {tag_label or tag}"
    else:
        pubs = publications
        title = "Publications — Shepherd Research Lab"
        heading = "All Publications"
    
    entries = "\n".join(pub_to_html_entry(p) for p in pubs)
    count = len(pubs)
    built = datetime.today().strftime("%B %d, %Y")
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="/assets/css/main.css">
  <style>
    .publication-entry {{ margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid #eee; }}
    .pub-title {{ font-weight: 600; margin-bottom: 0.2rem; }}
    .pub-authors {{ color: #555; font-size: 0.9rem; margin-bottom: 0.2rem; }}
    .pub-citation {{ color: #333; font-size: 0.9rem; margin-bottom: 0.3rem; }}
    .pub-doi {{ font-size: 0.85rem; color: #0066cc; }}
    .pub-tags {{ margin-top: 0.4rem; }}
    .pub-tag {{ display: inline-block; background: #f0f4f8; color: #446; 
                font-size: 0.75rem; padding: 2px 8px; border-radius: 3px; margin-right: 4px; }}
    .pub-count {{ color: #777; font-size: 0.9rem; margin-bottom: 1.5rem; }}
    .pub-updated {{ color: #999; font-size: 0.8rem; margin-top: 2rem; }}
    .ris-download {{ margin-bottom: 2rem; }}
    .ris-download a {{ display: inline-block; padding: 8px 16px; background: #2c5f8a; 
                       color: white; text-decoration: none; border-radius: 4px; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <main class="container">
    <h1>{heading}</h1>
    <p class="pub-count">{count} publication{'s' if count != 1 else ''}</p>
    <div class="ris-download">
      <a href="/publications/publications.ris" download>⬇ Download RIS (EndNote/Zotero)</a>
      &nbsp;
      <a href="/publications/publications.bib" download>⬇ Download BibTeX</a>
    </div>
    <div class="publications-list">
{entries}
    </div>
    <p class="pub-updated">Last updated: {built}</p>
  </main>
</body>
</html>"""


def generate_ris(publications):
    """Generate RIS format for EndNote/Zotero/Mendeley import."""
    lines = []
    
    for pub in publications:
        pub_type = "JOUR"  # Default to journal article
        journal = pub.get("journal", "")
        if any(word in journal.lower() for word in ["conference", "proceedings", "workshop", "symposium"]):
            pub_type = "CONF"
        elif not journal:
            pub_type = "GEN"
        
        lines.append(f"TY  - {pub_type}")
        lines.append(f"TI  - {pub.get('title', '')}")
        
        # Authors - one AU tag per author
        authors_str = pub.get("authors", "")
        if authors_str:
            for author in authors_str.split(","):
                author = author.strip()
                if author:
                    lines.append(f"AU  - {author}")
        
        if pub.get("year"):
            lines.append(f"PY  - {pub['year']}")
        if journal:
            lines.append(f"JO  - {journal}")
        if pub.get("volume"):
            lines.append(f"VL  - {pub['volume']}")
        if pub.get("pages"):
            pages = pub["pages"].replace("–", "-").replace("—", "-")
            if "-" in pages:
                sp, ep = pages.split("-", 1)
                lines.append(f"SP  - {sp.strip()}")
                lines.append(f"EP  - {ep.strip()}")
            else:
                lines.append(f"SP  - {pages}")
        
        doi = pub.get("doi", "")
        if doi:
            doi_clean = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "")
            lines.append(f"DO  - {doi_clean}")
            lines.append(f"UR  - https://doi.org/{doi_clean}")
        
        if pub.get("abstract"):
            lines.append(f"AB  - {pub['abstract']}")
        
        # Tags as keywords
        for tag in pub.get("tags", []):
            lines.append(f"KW  - {tag}")
        
        lines.append("ER  - ")
        lines.append("")
    
    return "\n".join(lines)


def generate_bibtex(publications):
    """Generate BibTeX format."""
    entries = []
    
    for pub in publications:
        key = pub.get("key", slugify(pub.get("title", "unknown")[:30]))
        year = pub.get("year", "")
        journal = pub.get("journal", "")
        
        if any(word in journal.lower() for word in ["conference", "proceedings", "workshop"]):
            entry_type = "inproceedings"
        elif journal:
            entry_type = "article"
        else:
            entry_type = "misc"
        
        fields = []
        fields.append(f'  title = {{{pub.get("title", "")}}}')
        fields.append(f'  author = {{{pub.get("authors", "")}}}')
        if year:
            fields.append(f'  year = {{{year}}}')
        if journal:
            if entry_type == "article":
                fields.append(f'  journal = {{{journal}}}')
            else:
                fields.append(f'  booktitle = {{{journal}}}')
        if pub.get("volume"):
            fields.append(f'  volume = {{{pub["volume"]}}}')
        if pub.get("pages"):
            fields.append(f'  pages = {{{pub["pages"]}}}')
        doi = pub.get("doi", "")
        if doi:
            doi_clean = doi.replace("https://doi.org/", "")
            fields.append(f'  doi = {{{doi_clean}}}')
        
        fields_str = ",\n".join(fields)
        entries.append(f"@{entry_type}{{{key},\n{fields_str}\n}}")
    
    return "\n\n".join(entries)


def main():
    tag_filter = None
    if "--tag" in sys.argv:
        idx = sys.argv.index("--tag")
        tag_filter = sys.argv[idx + 1]
    
    ris_only = "--ris-only" in sys.argv
    
    publications = load_yaml(PUBLICATIONS_FILE)
    taxonomy = load_yaml(TAGS_FILE)
    
    print(f"Loaded {len(publications)} publications.")
    
    if tag_filter:
        filtered = [p for p in publications if tag_filter in p.get("tags", [])]
        print(f"Tag '{tag_filter}': {len(filtered)} papers")
        for p in filtered:
            print(f"  [{p.get('year','')}] {p['title'][:70]}")
        return
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # RIS export
    ris_content = generate_ris(publications)
    ris_path = os.path.join(OUTPUT_DIR, "publications.ris")
    with open(ris_path, "w", encoding="utf-8") as f:
        f.write(ris_content)
    print(f"RIS export: {ris_path} ({len(publications)} entries)")
    
    # BibTeX export
    bib_content = generate_bibtex(publications)
    bib_path = os.path.join(OUTPUT_DIR, "publications.bib")
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(bib_content)
    print(f"BibTeX export: {bib_path}")
    
    if ris_only:
        return
    
    # Full publications page
    html = generate_html(publications)
    html_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML: {html_path}")
    
    # Build a tag label lookup
    tag_labels = {}
    for category in ["studies", "research_areas", "modalities", "cohorts"]:
        for item in taxonomy.get(category, []):
            tag_labels[item["tag"]] = item["label"]
    
    # Per-tag pages
    all_tags = set()
    for pub in publications:
        all_tags.update(pub.get("tags", []))
    
    for tag in sorted(all_tags):
        tag_html = generate_html(publications, tag=tag, tag_label=tag_labels.get(tag, tag))
        tag_path = os.path.join(OUTPUT_DIR, f"{tag}.html")
        with open(tag_path, "w", encoding="utf-8") as f:
            f.write(tag_html)
    
    print(f"Per-tag pages: {len(all_tags)} tags")
    print("\nBuild complete.")


if __name__ == "__main__":
    main()
