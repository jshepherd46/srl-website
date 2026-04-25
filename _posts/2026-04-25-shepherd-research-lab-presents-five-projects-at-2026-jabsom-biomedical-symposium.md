---
title: "Shepherd Research Lab presents five projects at 2026 JABSOM Biomedical Sciences Symposium"
date: 2026-04-25
thumbnail: "/wp-content/uploads/2026/04/comic-architecture.png"
---

Shepherd Research Lab members presented **five posters** at the 2026 Annual Biomedical Sciences Symposium hosted by the John A. Burns School of Medicine on April 24 and 25 at the Kakaʻako campus. The symposium showcases research from graduate students, postdoctoral fellows, residents, and medical students across the University of Hawaiʻi system.

The lab's projects this year spanned breast-cancer registry infrastructure, liver-cancer risk phenotyping, AI for skin-cancer detection, and electronic health-record models for cancer-risk prediction in Pacific Island populations. The unifying theme across all five is straightforward: build cancer-risk tools that work for the populations served in Hawaiʻi and the Pacific, rather than borrow models trained elsewhere and hope they fit.

### The Hawaii and Pacific Islands Mammography Registry (HIPIMR)

*Presented by Thomas Wolfgruber, with Brandon Quon, Dustin Valdez, Arianna Bunnell, and collaborators from Hawaii Diagnostic Radiology Services, The Queen's Health Systems, and Hawaii Pacific Health.*

The poster reported the current scope of HIPIMR: **126,064 unique women, 680,343 visits between 2009 and 2025, and more than 92 million images** across full-field digital mammography, digital breast tomosynthesis, ultrasound, and MRI from three imaging centers. The registry has already enabled published studies on regional advanced-breast-cancer rates, AI-based density prediction from breast ultrasound, explainable concept-bottleneck models for lesion detection, and open-source ultrasound preprocessing tools. HIPIMR is the multi-modal foundation that lets us evaluate whether existing risk models — developed largely on continental US and European populations — perform adequately for Native Hawaiian, Pacific Islander, and Asian subgroups.

### FibroScan signal discordance in a multiethnic Hawaiʻi cohort

*Presented by Dustin Valdez, with Arianna Bunnell, Brenda Hernandez, and John Shepherd.*

In a 244-adult cohort from Oʻahu, **63 percent of participants showed a tertile mismatch** between FibroScan-derived steatosis (CAP) and liver stiffness (LSM). The discordance is not random. Participants with higher fibrosis than expected were leaner (mean BMI 24.3) and showed lower triglycerides and lower insulin resistance, while participants with lower fibrosis than expected carried the highest BMI (28.0) and the most adverse lipid profile. Chinese participants were enriched in the higher-fibrosis group and Caucasian participants in the lower-fibrosis group. The findings motivate AI-based extraction of richer signal from FibroScan images for liver-cancer risk stratification across populations.

### Collaborative Mixing of Clinical Concepts (CoMiC) for explainable skin-cancer detection

*Presented by Arianna Bunnell, with Samuel Yang, Eujin Cho, Thomas Wolfgruber, Kevin Cassel, John Shepherd, and Peter Sadowski.*

![CoMiC architecture diagram]({{ site.baseurl }}/wp-content/uploads/2026/04/comic-architecture.png)

CoMiC is a concept-bottleneck model that combines computational and dermatologist-defined ABCD features (Asymmetry, Border, Color, Differential structures) for skin-lesion classification. Trained on **8,116 dermoscopy images** from the ISIC and PH2 datasets, CoMiC achieved a Dice coefficient of **0.89 for lesion segmentation** and AUROC up to **0.97 for individual concept prediction**. The full model classified malignancy at AUROC **0.85**, rising to **0.87** when intervention was allowed on the asymmetry concept. The work demonstrates for the first time that combining expert-defined and computationally-derived concepts can improve performance in concept-bottleneck models built from clinical lexica.

### AI in the skin-cancer screening pathway: an umbrella review

*Presented by Lydia Sollis, with Arianna Bunnell, Eujin Cho, Mark Willingham, Gabriela Cruz-Mattos, Anson Arii, Christopher Lum, Kevin Cassel, and John Shepherd.*

This PRISMA 2020 umbrella review (PROSPERO CRD42024605934) synthesized evidence across the four phases of the skin-cancer screening pathway: self-screening apps, primary-care evaluation, specialist dermoscopy, and histopathology. **Performance was setting-specific.** Self-screening apps showed unsafe variability (sensitivity **0 to 98 percent**), specialist dermoscopy reached **82 to 91 percent** sensitivity, and generalists gained **27.9 percentage points of sensitivity** from AI augmentation — compared with 2.1 points for expert dermatologists. Equity gaps remain fundamental: over **70 percent of training datasets are drawn from light-skinned populations**, and only 10.8 percent of reviews analyzed Fitzpatrick-type reporting. The current evidence does not support unsupervised clinical deployment of AI-based skin-cancer detection.

### ShepBERT: transformer-based EHR cancer-risk prediction for Pacific Island populations

*Presented by Pavel Bushuyev, with Lydia Sollis, Arianna Bunnell, Thomas Wolfgruber, Todd Seto, Igor Molybog, and John Shepherd.*

ShepBERT is a BERT-style transformer model in development for cancer-risk prediction across the **five cancers with the heaviest burden in Hawaiʻi and Pacific Island communities**: breast, prostate, colorectal, lung, and liver. The model standardizes longitudinal EHR data into the OMOP Common Data Model, pre-trains on the 365,000-patient MIMIC-IV cohort, and will be fine-tuned on EHR data from Queen's Medical Center as IRB review and data-use agreements proceed. The project, supported by the **NIH AIM-AHEAD Consortium to Advance Health Equity**, also includes interactive interpretability dashboards designed for use in local clinical workflows.

### Closing thoughts

Existing clinical risk models — whether for breast cancer, liver cancer, skin cancer, or general cancer surveillance — are trained predominantly on continental US and European populations. The lab's research program is organized around the question of how to extract richer, population-relevant signal from imaging and clinical data already being collected in Hawaiʻi and the Pacific. Each of these five posters answers a piece of that question, and each was led by a trainee or staff scientist driving the work forward.

Congratulations to **Thomas, Dustin, Arianna, Lydia, and Pavel**, and to all of their collaborators across UH Cancer Center, UH Mānoa, Queen's Medical Center, Hawaii Diagnostic Radiology Services, Hawaii Pacific Health, and Complete Dermatology.

The 2026 Biomedical Sciences Symposium was hosted by the John A. Burns School of Medicine on April 24 and 25, 2026. More information at [biosymp.jabsom.hawaii.edu ↗](https://biosymp.jabsom.hawaii.edu).
