---
layout: default
title: "Publications — Cancer"
description: "Shepherd Research Lab publications on cancer — breast density, cancer screening, and risk modeling."
---

<section class="section">
<div class="container" markdown="1" style="max-width: 900px;">

# Cancer — Publications

The lab's cancer research surfaces under three research-area tags in our taxonomy. Each section below filters to papers carrying one of those tags. Some papers appear in more than one section when they cross topics.

<nav style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1.25rem 0 1.5rem;">
<a href="{{ site.baseurl }}/publications/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">← All publications</a>
<a href="{{ site.baseurl }}/research/cancer/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">Cancer research page →</a>
</nav>

## Breast Density

{% assign active = site.data.publications | where_exp: "p", "p.exclude != true" %}
{% assign bd = active | where_exp: "p", "p.tags contains 'breast-density'" %}
{% include publications-list.html entries=bd %}

## Cancer Screening

{% assign cs = active | where_exp: "p", "p.tags contains 'cancer-screening'" %}
{% include publications-list.html entries=cs %}

## Risk Modeling

{% assign rm = active | where_exp: "p", "p.tags contains 'risk-modeling'" %}
{% include publications-list.html entries=rm %}

</div>
</section>
