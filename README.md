# Beyond the Answer Key

Companion repository for **Beyond the Answer Key: Robustness Evaluation of Large Language Models for Step-Level Mathematical Verification**, by Fateme Mazdarani and Carlos Toxtli, ICMLA 2026, pp. 1043-1048.

[Published paper](https://doi.org/10.1109/ICMLA69890.2026.00158)

**Data availability: partial recovery, November 10, 2026.** This repository currently contains the published aggregate results, recovered figures, and paper-reported method settings. The original training/test traces, gold metadata, generator/checker, and model response logs have not been located and are **not included**. This is not yet the complete benchmark release described in the paper.

## Available files

| Path | Contents |
| --- | --- |
| [data/reported_results/](data/reported_results/) | Tables I-III in CSV and JSON: 36 model/variant/split rows, 432 reported accuracy values |
| [figures/](figures/) | Three original PNG figures recovered from the author source archive |
| [configs/paper_reported_settings.json](configs/paper_reported_settings.json) | Descriptive transcription of settings stated in the paper; not a runnable experiment configuration |
| [source/tables/](source/tables/) | Unmodified LaTeX table fragments used to produce the exports |
| [metadata/provenance.json](metadata/provenance.json) | Source filenames, SHA-256 hashes, transformations, and limitations |
| [metadata/release_inventory.json](metadata/release_inventory.json) | Available and missing release components |
| [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) | Missing files and requirements for completing the original release |

## Benchmark described in the paper

Models evaluate worked solutions to equations of the form `ax + b = cx + d`, with integer coefficients in `[-10, 10]` and `a != c`. The three judgments are final-answer correctness (Q1), full-trace correctness (Q2), and the first incorrect step (Q3). Step 0 is the original equation, and Q3 is `-1` for a valid trace.

T1 traces have valid steps and a correct answer. T2 traces contain an injected error leading to an incorrect answer. T3 traces contain an invalid intermediate step but restore the correct final answer. The paper compares canonical and perturbed traces for GPT-OSS 20B, Qwen3-14B, and Phi-4-Reasoning under Base, FT, GED-FT, and TTC variants.

The paper reports 27,000 training traces, 1,080 canonical test traces, 1,080 perturbed test traces, and 4,000 retained Gemini-enhanced training examples. These are **paper-reported counts**, not counts of records available here. The relationship between the 4,000 distilled examples and the 27,000 training traces cannot be verified without the original files.

## Using the reported results

`results_wide.csv` has one row per model, split, and variant; each metric column ends in `_pct`. `results_long.csv` has one row per accuracy value. `canonical` corresponds to the tables' **Baseline** section. `paper_reported_n` records the stated evaluation denominator, not a recovered observation count.

All percentages retain the published values and precision. No values have been corrected, and no per-item predictions or integer success counts have been inferred from rounded percentages. CSV readers can parse percentages as decimals; JSON stores them as strings to preserve trailing zeros. These aggregates support inspection of the published tables, but do not support independent re-scoring, confidence intervals, or retraining.

Python 3.9+ is sufficient for the included scripts; no third-party dependencies are required:

```bash
python3 scripts/export_reported_results.py --check
python3 scripts/verify_release.py
```

To regenerate the CSV/JSON exports from the recovered LaTeX table fragments:

```bash
python3 scripts/export_reported_results.py
```

These scripts were written when assembling this recovery package. They are not the original experiment code.

## Citation and reuse

See [CITATION.cff](CITATION.cff) to cite the paper. A reuse license has not yet been selected; see [RIGHTS.md](RIGHTS.md). The publisher PDF is linked through its DOI and is not redistributed here.
