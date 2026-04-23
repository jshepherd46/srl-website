---
layout: default
title: "Publications — Cancer"
description: "Shepherd Research Lab publications on cancer — breast density, cancer screening, and risk modeling."
---

<section class="section">
<div class="container" markdown="1" style="max-width: 900px;">

# Cancer — Publications

The lab's cancer research surfaces under three research-area tags in our taxonomy. Each section below filters to papers carrying one of those tags. Some papers appear in more than one section when they cross topics.

See also: [all publications]({{ site.baseurl }}/publications/) · [Cancer research page]({{ site.baseurl }}/research/cancer/)

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
