#!/usr/bin/env python3
"""
classify.py — Auto-tag new papers using Claude
Reads new_papers_staging.yaml, calls Claude API to propose tags
from the taxonomy in tags.yaml, writes classified_papers.yaml for review.

Requirements: pip install anthropic pyyaml
Run: python3 classify.py
"""

import yaml
import json
import os
import sys
import anthropic

STAGING_FILE = "new_papers_staging.yaml"
CLASSIFIED_FILE = "classified_papers.yaml"
TAGS_FILE = "tags.yaml"


def load_yaml(filepath):
    with open(filepath, "r") as f:
        return yaml.safe_load(f) or []


def build_tag_list(taxonomy):
    """Flatten taxonomy into a list of (tag, description) tuples."""
    tags = []
    for category in ["studies", "research_areas", "modalities", "cohorts"]:
        for item in taxonomy.get(category, []):
            tags.append({
                "tag": item["tag"],
                "label": item["label"],
                "description": item.get("description", "")
            })
    return tags


def classify_paper(client, paper, tag_list):
    """Call Claude to propose tags for a single paper."""
    
    tag_descriptions = "\n".join(
        f"  - {t['tag']}: {t['label']} — {t['description']}"
        for t in tag_list
    )
    
    prompt = f"""You are classifying a scientific publication for the Shepherd Research Lab at the University of Hawaii Cancer Center.

Paper to classify:
Title: {paper['title']}
Authors: {paper['authors']}
Year: {paper['year']}
Journal: {paper['journal']}
Abstract: {paper.get('abstract', 'Not available')}

Available tags:
{tag_descriptions}

Instructions:
- Select ALL tags that apply to this paper
- A paper about body composition DXA in NHANES would get: body-composition, dxa, nhanes, maps (if relevant)
- A paper about breast density AI would get: breast-density, ai, mammography, hipimr (if from Hawaii data)
- Be liberal with research_area tags, conservative with study tags (only tag a study if clearly related)
- Return ONLY a JSON object with this exact format:
{{"tags": ["tag1", "tag2"], "confidence": "high/medium/low", "reasoning": "one sentence"}}"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text.strip()
    
    # Strip markdown if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    
    return json.loads(response_text)


def main():
    if not os.path.exists(STAGING_FILE):
        print(f"No staging file found at {STAGING_FILE}")
        print("Run scraper.py first.")
        return
    
    papers = load_yaml(STAGING_FILE)
    taxonomy = load_yaml(TAGS_FILE)
    tag_list = build_tag_list(taxonomy)
    
    print(f"Papers to classify: {len(papers)}")
    print(f"Available tags: {len(tag_list)}")
    
    # Initialize Anthropic client (uses ANTHROPIC_API_KEY env var)
    client = anthropic.Anthropic()
    
    classified = []
    
    for i, paper in enumerate(papers):
        print(f"\n[{i+1}/{len(papers)}] {paper['title'][:70]}...")
        
        try:
            result = classify_paper(client, paper, tag_list)
            paper["tags"] = result.get("tags", [])
            paper["tag_confidence"] = result.get("confidence", "low")
            paper["tag_reasoning"] = result.get("reasoning", "")
            paper["notes"] = f"AUTO-TAGGED ({result.get('confidence','?')} confidence) - please review"
            print(f"  Tags: {paper['tags']}")
            print(f"  Confidence: {paper['tag_confidence']}")
        except Exception as e:
            print(f"  Classification failed: {e}")
            paper["tags"] = []
            paper["notes"] = "AUTO-IMPORTED - classification failed, tags required manually"
        
        classified.append(paper)
    
    with open(CLASSIFIED_FILE, "w") as f:
        yaml.dump(classified, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"\nClassified papers written to: {CLASSIFIED_FILE}")
    print("Next step: review tags in classified_papers.yaml, then run merge.py to add to publications.yaml")


if __name__ == "__main__":
    main()
