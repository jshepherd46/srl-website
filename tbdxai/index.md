---
layout: default
title: "TBDXA.I. — Deep Learning on Total-Body DXA Scans"
description: "Self-supervised deep learning applied to Total-Body DXA scans from the Health ABC Study to predict CVD, mortality, cancer, hip fracture, and metabolic outcomes."
---

<section class="section">
<div class="container" markdown="1" style="max-width: 820px;">

# Deep Learning and Total-Body DXA Scans (TBDXA.I.)

<nav style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1.25rem 0 1.5rem;">
<a href="{{ site.baseurl }}/studies/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">← All studies</a>
<a href="{{ site.baseurl }}/research/ai/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">AI research →</a>
<a href="{{ site.baseurl }}/research/body-composition/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">Body Composition research →</a>
</nav>

![Whole-body DXA scan]({{ site.baseurl }}/wp-content/uploads/2022/01/whole-body-dxa-1024x576-1-930x576.jpg)

This research applies deep-learning methods to total-body DXA (dual-energy X-ray absorptiometry) scans to extract predictive information about body composition and health outcomes. The project uses **self-supervised learning on whole-body images from the Health, Aging and Body Composition (Health ABC) Study**, which includes over 3,000 participants with follow-up scans at years 3, 6, and 10.

The approach generates algorithms to predict clinical outcomes — cardiovascular disease, mortality, cancer, hip fracture, physical disability, diabetes-related measures — extracting features from unlabeled DXA images without requiring labeled outcome data during the initial learning phase.

</div>
</section>

<section class="section section--alt">
<div class="container" markdown="1" style="max-width: 820px;">

## Specific aims

1. **Predict clinical endpoints** — generate predictive algorithms for CVD, CVD death, overall mortality, cancer, cancer death, hip fracture, physical disability, incident insulin-resistant diabetes, and metabolic markers by applying deep learning to baseline and follow-up Total-Body DXA images.
2. **Predict physical performance and inflammation** — algorithms for gait speed, corridor walk speed, and IL-6 concentration.
3. **Explain the model** — explore image features accounting for algorithm accuracy using saliency mapping techniques.

</div>
</section>

<section class="section">
<div class="container" markdown="1" style="max-width: 820px;">

## Research team

**Principal Investigators**

- **Steve Cummings, MD, FAPC** — San Francisco Coordinating Center
- **John Shepherd, PhD** — UH Cancer Center

**Co-Investigator**

- **Peter Sadowski, PhD** — UH Mānoa, Information and Computer Sciences

**Additional team members**

- **Warren Browner, MD, MPH** — CEO, California Pacific Medical Center
- **Eleanor Simonsick, PhD** — Epidemiologist, National Institute on Aging (NIH)
- **Yannik Glaser** — Graduate Student, UH Mānoa ICS
- **Lily Liu** — Statistician, California Pacific Medical Center

## Funding

**Sutter Health / California Medical Center Research Institute** — Grant 2805096-0100 · 11/01/2019 – 10/31/2020.

</div>
</section>

<section class="section section--alt">
<div class="container" markdown="1" style="max-width: 820px;">

## Key publication

Glaser Y, Shepherd J, Leong L, Wolfgruber T, Lui L-Y, Sadowski P, et al. **Deep learning predicts all-cause mortality from longitudinal total-body DXA imaging.** *Communications Medicine* 2022 Aug 16;2. [DOI: 10.1038/s43856-022-00166-9](https://doi.org/10.1038/s43856-022-00166-9)

The strongest model achieved an area under the ROC curve of **0.79** on held-out test data from over 15,000 scans. The study employed explainable-AI techniques to interpret predictions and evaluate input contributions.

## Presentation

Glaser Y, Sadowski P, Wolfgruber T, Lui L-Y, Cummings S, Shepherd J. **Hip fracture risk modelling using DXA and artificial intelligence.** Poster, American Society for Bone Mineral and Research Annual Meeting; 2020 Sep 11; Virtual.

</div>
</section>
