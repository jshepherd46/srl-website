---
layout: default
title: "Publications — DXA Quality Control"
description: "Shepherd Research Lab publications tagged dxa-qc."
auto_generated: true
---

<section class="section">
<div class="container" markdown="1" style="max-width: 900px;">

# DXA Quality Control — Publications

Papers tagged `dxa-qc` — DXA quality control systems and cross-manufacturer harmonization

<nav style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1.25rem 0 1.5rem;">
<a href="{{ site.baseurl }}/publications/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">← All publications</a>
</nav>

{% assign filtered = site.data.publications | where_exp: "p", "p.exclude != true" %}
{% assign filtered = filtered | where_exp: "p", "p.tags contains 'dxa-qc'" %}

{% include publications-list.html entries=filtered %}

</div>
</section>
