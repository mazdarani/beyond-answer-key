# Data availability

As of November 10, 2026, the original trace-level dataset and experiment code have not been located in the searched local research folders, manuscript archives, accessible GitHub repositories, or targeted Google Drive searches. This does not establish that the originals do not exist on another machine or service.

This repository releases recovered aggregate results and supporting materials. Newly generated examples would constitute a reconstructed dataset and cannot be substituted for the samples used in the published experiments.

## Original components still needed

| Component | Paper-reported size or description | Status |
| --- | --- | --- |
| Canonical training traces | 9,000, balanced across T1/T2/T3 | Not located |
| Perturbed training traces | 18,000, balanced across type and family | Not located |
| Canonical held-out traces | 1,080; 360 per type | Not located |
| Perturbed held-out traces | 1,080; 360 per type, balanced across six families | Not located |
| Distillation examples | 4,000 retained Gemini-enhanced examples | Not located |
| Gold metadata | Equation tuple, trace type, family, obligation log, Q1/Q2/Q3, checker explanation | Not located |
| Generator and exact-arithmetic checker | Original executable source | Not located |
| Split membership | Equation identifiers, tuple-hash definition and seeds | Not located |
| Model responses | Raw outputs, parse failures, TTC samples and votes | Not located |
| Experiment artifacts | Prompts, runnable configurations, model revisions and adapters | Not located |

## Completing the original release

1. Recover the original files and record their source and checksums before conversion.
2. Confirm train/test counts, T1/T2/T3 and family balance, and equation-level disjointness against the frozen split membership.
3. Run the original checker over every released record, including candidate verification and obligation logs. Preserve original labels and record any corrections separately.
4. Recover the original prompts, exact model revisions, package versions, fine-tuning settings and TTC policy. The descriptive settings file here leaves unspecified values null.
5. Re-score original responses, including malformed responses, and reconcile the resulting metrics with Tables I-III. Record differences rather than overwriting published values.
6. Set component-specific reuse licenses, add dataset documentation, and update this page and the release inventory only after verifying the actual files.

No benchmark record schema has been invented in this package. The authentic record structure and obligation-log semantics must be recovered from the original implementation.
