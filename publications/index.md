---
layout: default
title: "Publications"
description: "Peer-reviewed publications from the Shepherd Research Lab — rendered from the monthly OpenAlex pipeline output."
---

<section class="section">
<div class="container" markdown="1" style="max-width: 900px;">

# Publications

<nav style="display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; margin: 1.25rem 0 1.5rem;">
<strong style="margin-right: 0.5rem; color: var(--gray-500); font-size: 0.9rem; font-weight: 600;">Browse by topic:</strong>
<a href="{{ site.baseurl }}/publications/ai/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">AI for Health</a>
<a href="{{ site.baseurl }}/publications/body-composition/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">Body Composition</a>
<a href="{{ site.baseurl }}/publications/cancer/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">Cancer</a>
</nav>

{% assign filtered = site.data.publications | where_exp: "p", "p.exclude != true" %}
{% include publications-list.html entries=filtered show_downloads=true empty_message="The full publications list is regenerated each month from our automated pipeline — OpenAlex discovery, Claude-assisted classification, and exports to RIS and BibTeX — and will appear here once the first pipeline run completes." %}

</div>
</section>
