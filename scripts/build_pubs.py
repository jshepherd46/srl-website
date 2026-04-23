#!/usr/bin/env python3
"""
build_pubs.py — Generate RIS and BibTeX exports from _data/publications.yaml.

HTML rendering is handled by Jekyll/Liquid in `publications/index.md`, which
reads `site.data.publications` directly. This script only produces the
EndNote/Zotero (RIS) and LaTeX (BibTeX) export files, committed alongside
the data file so users can download them.

Usage:
  python3 scripts/build_pubs.py           # regenerate publications/publications.{ris,bib}
  python3 scripts/build_pubs.py --tag X   # list papers with a given tag (no write)
"""

import yaml
import os
import sys

PUBLICATIONS_FILE = "_data/publications.yaml"
TAGS_FILE = "tags.yaml"
OUTPUT_DIR = "publications"   # Jekyll source path — files served verbatim

# Tags whose per-tag page is hand-curated and should NOT be auto-generated.
# (Cancer is a multi-tag union, not a single tag, but the URL /publications/cancer/
# collides with any auto-generated `cancer` tag page — none exists today, but list
# kept as a safety net.)
HAND_CURATED_SLUGS = {"cancer"}

# Map tag → /research/<slug>/ crosslink for pages where a matching research-area
# page exists. Tags not in this map simply link back to /publications/.
TAG_TO_RESEARCH_PAGE = {
    "ai": ("/research/ai/", "AI for Health"),
    "body-composition": ("/research/body-composition/", "Body Composition"),
    "breast-density": ("/research/cancer/", "Cancer"),
    "cancer-screening": ("/research/cancer/", "Cancer"),
    "risk-modeling": ("/research/cancer/", "Cancer"),
}


def load_yaml(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def generate_ris(publications):
    """Generate RIS format for EndNote/Zotero/Mendeley import."""
    lines = []

    for pub in publications:
        if pub.get("exclude"):
            continue  # tombstoned entries — skip

        pub_type = "JOUR"
        journal = pub.get("journal", "")
        if any(word in journal.lower() for word in ["conference", "proceedings", "workshop", "symposium"]):
            pub_type = "CONF"
        elif not journal:
            pub_type = "GEN"

        lines.append(f"TY  - {pub_type}")
        lines.append(f"TI  - {pub.get('title', '')}")

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

        for tag in pub.get("tags", []):
            lines.append(f"KW  - {tag}")

        lines.append("ER  - ")
        lines.append("")

    return "\n".join(lines)


def generate_bibtex(publications):
    """Generate BibTeX format."""
    entries = []

    for pub in publications:
        if pub.get("exclude"):
            continue

        key = pub.get("key", "unknown")
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


def generate_tag_page(tag, label, description, research_crosslink):
    """Return the markdown source for a per-tag publications page."""
    # Pill-styled nav links — matches the year-nav pattern on the publications
    # list so the clickability cue (rounded border) is consistent site-wide.
    pill = (
        "padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); "
        "border-radius: 100px; font-size: 0.85rem; text-decoration: none; "
        "color: var(--gray-700); font-weight: 600;"
    )
    pill_links = [
        f'<a href="{{{{ site.baseurl }}}}/publications/" style="{pill}">'
        f'← All publications</a>'
    ]
    if research_crosslink:
        research_url, research_label = research_crosslink
        pill_links.append(
            f'<a href="{{{{ site.baseurl }}}}{research_url}" style="{pill}">'
            f'{research_label} research page →</a>'
        )
    nav_html = (
        '<nav style="display: flex; flex-wrap: wrap; gap: 0.5rem; '
        'margin: 1.25rem 0 1.5rem;">\n'
        + "\n".join(pill_links)
        + "\n</nav>"
    )

    return f"""---
layout: default
title: "Publications — {label}"
description: "Shepherd Research Lab publications tagged {tag}."
auto_generated: true
---

<section class="section">
<div class="container" markdown="1" style="max-width: 900px;">

# {label} — Publications

Papers tagged `{tag}` — {description}

{nav_html}

{{% assign filtered = site.data.publications | where_exp: "p", "p.exclude != true" %}}
{{% assign filtered = filtered | where_exp: "p", "p.tags contains '{tag}'" %}}

{{% include publications-list.html entries=filtered %}}

</div>
</section>
"""


def write_per_tag_pages(publications, taxonomy):
    """Generate a /publications/<tag>/index.md page for every tag in the
    taxonomy that has at least one active (non-excluded) paper."""
    # Build tag → (label, description) lookup from the taxonomy
    tag_info = {}
    for category in ["studies", "research_areas", "modalities", "cohorts"]:
        for item in taxonomy.get(category, []):
            tag_info[item["tag"]] = (
                item.get("label", item["tag"]),
                item.get("description", ""),
            )

    # Find tags with at least one active paper
    active_tags = set()
    for p in publications:
        if p.get("exclude"):
            continue
        for t in p.get("tags", []) or []:
            if t in tag_info:
                active_tags.add(t)

    written = 0
    skipped = 0
    for tag in sorted(active_tags):
        if tag in HAND_CURATED_SLUGS:
            skipped += 1
            continue
        label, description = tag_info[tag]
        research_crosslink = TAG_TO_RESEARCH_PAGE.get(tag)

        page_dir = os.path.join(OUTPUT_DIR, tag)
        os.makedirs(page_dir, exist_ok=True)
        page_path = os.path.join(page_dir, "index.md")

        # Only rewrite the file if its content actually differs — keeps
        # git diffs clean across pipeline runs when tags don't change.
        new_content = generate_tag_page(tag, label, description, research_crosslink)
        if os.path.exists(page_path):
            with open(page_path, "r", encoding="utf-8") as f:
                old_content = f.read()
            if old_content == new_content:
                continue
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        written += 1

    print(f"Per-tag pages: {written} written, {skipped} skipped (hand-curated), {len(active_tags)} active tags total.")


def main():
    # --tag lookup (no-write; prints papers matching)
    if "--tag" in sys.argv:
        idx = sys.argv.index("--tag")
        tag_filter = sys.argv[idx + 1]
        publications = load_yaml(PUBLICATIONS_FILE)
        filtered = [p for p in publications if tag_filter in p.get("tags", []) and not p.get("exclude")]
        print(f"Tag '{tag_filter}': {len(filtered)} papers")
        for p in filtered:
            print(f"  [{p.get('year','')}] {p['title'][:70]}")
        return

    publications = load_yaml(PUBLICATIONS_FILE)
    active = [p for p in publications if not p.get("exclude")]
    print(f"Loaded {len(publications)} publications ({len(active)} active, {len(publications) - len(active)} excluded).")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ris_path = os.path.join(OUTPUT_DIR, "publications.ris")
    with open(ris_path, "w", encoding="utf-8") as f:
        f.write(generate_ris(publications))
    print(f"RIS export: {ris_path}")

    bib_path = os.path.join(OUTPUT_DIR, "publications.bib")
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(generate_bibtex(publications))
    print(f"BibTeX export: {bib_path}")

    taxonomy = load_yaml(TAGS_FILE) if os.path.exists(TAGS_FILE) else {}
    write_per_tag_pages(publications, taxonomy)

    print("\nBuild complete. Jekyll renders the HTML pages from _data/publications.yaml.")


if __name__ == "__main__":
    main()
