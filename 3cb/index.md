---
layout: default
title: "3CB — Three-Compartment Breast Lesion Detection"
description: "Dual-energy compositional breast imaging (3CB) for distinguishing malignant from benign lesions and reducing unnecessary biopsies."
---

<section class="section">
<div class="container" markdown="1" style="max-width: 820px;">

# Three-Compartment Breast Lesion Detection (3CB)

<nav style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1.25rem 0 1.5rem;">
<a href="{{ site.baseurl }}/studies/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">← All studies</a>
<a href="{{ site.baseurl }}/research/cancer/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">Cancer research →</a>
<a href="{{ site.baseurl }}/publications/3cb/" style="padding: 0.35rem 0.8rem; border: 1px solid var(--gray-300); border-radius: 100px; font-size: 0.85rem; text-decoration: none; color: var(--gray-700); font-weight: 600;">3CB publications →</a>
</nav>

![3CB study cover]({{ site.baseurl }}/wp-content/uploads/2022/01/3cb-cover-01-1024x576-1-930x576.jpg)

The Shepherd Research Lab has developed a novel breast-imaging technique that analyzes lesion composition using three compartmental measurements: **protein, lipid, and water (3CB)**. The study investigates whether lipid-protein-water signatures of mammographically suspicious breast lesions can improve cancer diagnosis and reduce unnecessary biopsies.

The first five years of research (March 2013 – June 2017) are complete. Current funding focuses on developing and evaluating novel mammographic biomarkers combined with quantitative image analysis (QIA) and radiomics methods — collectively termed **q3CB**.

</div>
</section>

<section class="section section--alt">
<div class="container" markdown="1" style="max-width: 820px;">

## Long-term goals

- Determine whether biological diagnostic measures can improve CADe (computer-aided detection) algorithms
- Quantify lipid-protein-water signatures to predict malignant findings
- Combine 3CB biomarkers with existing QIA/radiomics methods to improve sensitivity and specificity
- Reduce unnecessary biopsies

</div>
</section>

<section class="section">
<div class="container" markdown="1" style="max-width: 820px;">

## Aim 1 — Sensitivity & specificity of 3CB signatures

Recruitment adjusted from 600 to 498 FFDM patients due to a 17% budget reduction. As of the last update, **425 women enrolled** (215 UCSF / 210 Moffitt) with biopsy-confirmed subtypes: 61 invasive ductal carcinoma (IDC), 40 ductal carcinoma in situ (DCIS), 66 fibroadenomas, 324 benign findings.

A calibration phantom with **51 combinations of water, lipid (wax), and protein (Delrin)** was created for standardizing 3CB across FFDM and DBT systems.

Early analysis of 45 lesions demonstrated 3CB features distinguishing between lesion types:

- IDC from DCIS by lipid skewness — **AUC = 0.71**
- Fibroadenomas by water texture relative to background — **AUC = 0.75**
- Benign lesions by peripheral water content — **AUC = 0.71**

Combined 3CB signature achieved **AUC = 0.72** in cross-validation for invasive-cancer detection.

## Aim 2 — Comparison with CAD/QIA methods

Merged QIA/radiomics signatures yielded **AUC = 0.81** in distinguishing lesions requiring biopsy from those not requiring it. Key QIA features identified:

- **Invasive cancer:** spiculation
- **DCIS:** circularity
- **Fibroadenoma:** radial gradient index
- **Other benign findings:** texture heterogeneity

Deep-learning approaches for microcalcification classification showed promising results. In a dataset of 99 biopsy-proven lesions, the deep-learning method "could have avoided 21 biopsies of the 80 benign lesions...versus only 8 avoidable biopsies based on radiologists (p < .001)."

## Aim 3 — Combined 3CB and QIA performance

The combination of 3CB and QIA (q3CB) significantly improved classification:

| Lesion type | 3CB alone | QIA alone | Combined |
|---|---|---|---|
| Overall | 0.71 | 0.81 | **0.86** |
| Masses | — | 0.83 | **0.89** |
| Microcalcifications | — | 0.84 | **0.91** |
| Asymmetry / arch. distortion | — | 0.61 | **0.87** (p = 0.006) |

3CB compositional information and QIA features provide complementary diagnostic information with little correlation between them.

## Future directions

Extension to 3D tomosynthesis imaging and reader studies to validate whether 3CB knowledge influences radiologist decision-making and reduces unnecessary biopsies.

</div>
</section>

<section class="section section--alt">
<div class="container" markdown="1" style="max-width: 820px;">

## Funding

**General Electric** — GE Contract · 08/01/2018 – 07/31/2020.

## Key publications

1. Leong LT, Malkov S, Drukker K, et al. **Dual-energy three-compartment breast imaging for compositional biomarkers to improve detection of malignant lesions.** *Communications Medicine.* 2021 Aug 31;1(1):29. [DOI: 10.1038/s43856-021-00024-0](https://doi.org/10.1038/s43856-021-00024-0)

2. Hinton B, Ma L, Mahmoudzadeh AP, et al. **Derived mammographic masking measures based on simulated lesions predict the risk of interval cancer after controlling for known risk factors.** *Med Phys.* 2019 Mar;46(3):1309–16. [DOI: 10.1002/mp.13410](https://doi.org/10.1002/mp.13410)

3. Drukker K, Giger ML, Joe BN, et al. **Combined benefit of quantitative three-compartment breast image analysis and mammography radiomics in the classification of breast masses in a clinical data set.** *Radiology.* 2019;290(3):621–8. [DOI: 10.1148/radiol.2018180608](https://doi.org/10.1148/radiol.2018180608)

4. Gierach GL, Patel DA, Falk RT, et al. **Relationship of serum estrogens and metabolites with area and volume mammographic densities.** *Hormones and Cancer.* 2015;6(2–3):107–19. [DOI: 10.1007/s12672-015-0216-3](https://doi.org/10.1007/s12672-015-0216-3)

5. Malkov S, Kerlikowske K, Shepherd J. **Automated volumetric breast density derived by shape and appearance modeling.** *Proc SPIE Int Soc Opt Eng.* 2014 Mar 22;9034:90342t. [DOI: 10.1117/12.2043990](https://doi.org/10.1117/12.2043990)

## Media coverage

- [Novel technique may significantly reduce breast biopsies ↗](https://www.eurekalert.org/pub_releases/2018-12/rson-ntm120418.php) — EurekAlert! / RSNA
- [UH Cancer Center unveils new technique to fight breast cancer ↗](https://www.kitv.com/story/39631450/uh-cancer-center-unveils-new-technique-to-fight-breast-cancer) — KITV4

</div>
</section>
