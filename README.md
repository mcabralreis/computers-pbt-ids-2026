# Computers PBT IDS 2026 — Reproducibility Package

This repository accompanies the manuscript:

> **Beyond Accuracy in IoT Intrusion Detection: Property-Based Assurance of Predictive and SHAP Explanation Robustness**

It preserves the publication-facing code, protocol metadata, derived tables, and the path from the sealed PF4-A1 evidence archive to the manuscript-grade PF4 results.

## Scope

The study evaluates a frozen IoT intrusion-detection pipeline using CICIoT2023 and the TON_IoT network dataset. The executed assurance families are:

- **PF0** — exact metamorphic pipeline invariance;
- **PF1** — bounded, domain-constrained source-feature perturbation robustness;
- **PF2** — missing/degraded-information robustness;
- **PF3** — dataset-supported temporal-shift probe (TON10/TON2 only);
- **PF4** — prediction and SHAP explanation robustness.

**PF5 was not executed.** Random Forest is included in baseline/PF0–PF3 evaluation but **was not executed in PF4**.

## Repository layout

```text
analysis/                  Read-only PF4 evidence-to-table analysis
code/pf4_primary_A1/       Frozen PF4-A1 primary scientific source extracted from final evidence
results/pf4_R3/            Manuscript-grade PF4 R3 tables/figures
results/manuscript_tables/ Baseline/cohort/PF3 tables used by the manuscript
paper/                     Article-status note; full manuscript is not deposited as a preprint
metadata/                  Citation/deposit metadata drafts
environment/               Scientific and analysis software requirements
scripts/                   Integrity/reproduction helpers
cloud-evidence/            (not stored in Git; see evidence/)
evidence/                   Expected archival files, hashes, and provenance notes
docs/                       Reproducibility, data-availability, and release documentation
```

## Reproducibility levels

### Level 1 — verify published derived results

No third-party raw dataset is required. The canonical R3 outputs are under `results/pf4_R3/` and the manuscript-facing baseline/cohort/PF3 tables are under `results/manuscript_tables/`.

### Level 2 — reproduce PF4 tables from sealed evidence

Obtain the final PF4 evidence archive:

`R7_D35_PF4_PRIMARY_P1_A1_G3_R3_FINAL_COMPLETE_evidence.zip`

Expected SHA-256:

`3878071e423383dfaa8c1d4a7ebf558681618137f6badfd8edbc913110accebe`

Then run:

```bash
python analysis/reproduce_pf4_results.py \
  --evidence-zip R7_D35_PF4_PRIMARY_P1_A1_G3_R3_FINAL_COMPLETE_evidence.zip \
  --outdir reproduced_pf4
```

On Windows PowerShell:

```powershell
py .\analysis\reproduce_pf4_results.py `
  --evidence-zip .\R7_D35_PF4_PRIMARY_P1_A1_G3_R3_FINAL_COMPLETE_evidence.zip `
  --outdir .\reproduced_pf4
```

The script verifies the evidence SHA-256 by default, parses all 81,000 committed scientific ordinals, and regenerates the manuscript-grade summary tables without loading models or executing SHAP.

### Level 3 — re-run the scientific pipeline

The repository does **not** redistribute CICIoT2023 or TON_IoT. A full scientific rerun requires obtaining the original datasets from their providers and restoring the frozen upstream preprocessing/model artifacts described in the manuscript and project manifests. The exact PF4-A1 scientific worker source used in the final campaign is preserved under `code/pf4_primary_A1/` and inside the final evidence archive.

## Final PF4 campaign

- 45 task/model/seed cases;
- 81,000 canonical XAI ordinals;
- 243,000 applicable perturbations;
- 162,000 Top-k ablation records;
- 216,000 additivity diagnostic records;
- PF4-A1 boundary-tie policy: no arbitrary Top-k tie breaking;
- PF5 authorized/executed: **NO**;
- RF authorized/executed in PF4: **NO**.

## Large evidence files

The ~314 MB final evidence archive should **not** be committed to ordinary Git history. GitHub blocks regular Git objects above 100 MiB. The archival upload set is designed for a DOI-bearing archive such as Zenodo; see `docs/DEPOSIT_GUIDE.md` and `evidence/EXPECTED_ARCHIVAL_FILES.md`.

## Data availability

The third-party source datasets are not redistributed. See `docs/DATA_AVAILABILITY.md` for provider/citation information and the distinction between source datasets, frozen evidence, and derived outputs.

## License

This is a mixed-license reproducibility repository:

- **MIT** for original software/code (`analysis/`, `code/`, `scripts/`);
- **CC BY 4.0** for original documentation, figures, tables, and derived results.

See `LICENSE`, `LICENSE-CC-BY-4.0.md`, and `LICENSES.md` for exact scope.
CICIoT2023 and TON_IoT are not redistributed and remain governed by their
providers' terms.

## Manuscript status

The full manuscript source/PDF is intentionally not included in the public
reproducibility repository before submission/publication. Publication-facing
tables and figures required for reproduction remain under `results/`.

## Citation

A DOI-free citation file is provided in `CITATION.cff`. After archival deposition, update the DOI/repository fields before creating the final public release.

## Integrity

Run:

```bash
python scripts/verify_release.py
```

or on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_release.ps1
```

The archival evidence SHA-256 values are listed in `evidence/SHA256_ARCHIVAL_ARTIFACTS.txt`.
