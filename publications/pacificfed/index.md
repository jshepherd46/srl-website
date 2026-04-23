---
layout: default
title: "Publications — PacificFed"
description: "Shepherd Research Lab publications tagged pacificfed."
auto_generated: true
---

<section class="section">
<div class="container" markdown="1" style="max-width: 900px;">

# PacificFed — Publications

Papers tagged `pacificfed` — Federated clinical AI for USAPI/CCPI networks

<nav style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1.25rem 0 1.5rem;">
<a href="{{ site.baseurl }}/publications/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">← All publications</a>
</nav>

{% assign filtered = site.data.publications | where_exp: "p", "p.exclude != true" %}
{% assign filtered = filtered | where_exp: "p", "p.tags contains 'pacificfed'" %}

{% include publications-list.html entries=filtered %}

</div>
</section>
