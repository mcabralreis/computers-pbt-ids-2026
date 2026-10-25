# Reproducibility Guide

## What can be reproduced without the original datasets?

The complete PF4 post-execution analysis can be reproduced from the sealed final PF4 evidence ZIP. This is intentional: the evidence archive contains committed per-ordinal scientific JSON records, case context, the PF4-A1 amendment, the amended primary scientific source, and transaction/audit material.

The analysis script in `analysis/reproduce_pf4_results.py` is read-only. It does not retrain models, load model artifacts, execute SHAP, modify checkpoints, execute PF5, or execute RF in PF4.

## Expected PF4 integrity counts

A correct final evidence archive yields:

- committed ordinals: 81,000;
- perturbation records: 243,000;
- prediction stable: 234,056;
- prediction changed: 8,944;
- Jaccard@5 defined: 242,588;
- Jaccard@10 defined: 242,086;
- clean Top-5 boundary ties: 137;
- clean Top-10 boundary ties: 304;
- perturbation-only Top-5 ties: 1;
- perturbation-only Top-10 ties: 2;
- ablation records: 162,000;
- additivity records: 216,000.

The maximum absolute change in a principal pooled PF4 metric after unique-profile weighting is approximately 0.003112.

## Statistical interpretation

The seed is the inferential unit for PF4 model-family contrasts. There are five paired seeds per task/model cell. Exact two-sided sign-flip tests therefore have coarse resolution; even a five-of-five directional result yields a minimum two-sided p-value of 0.0625. The manuscript emphasizes effect magnitude, between-seed variability, and directional consistency rather than a conventional p<0.05 threshold.

## Model–explainer scope

PF4 uses model-appropriate SHAP paths:

- LIN: `LinearExplainer`;
- HGB: interventional `TreeExplainer`;
- MLP: `GradientExplainer`.

Thus, cross-family PF4 contrasts characterize frozen **model–explainer pairs**, not architecture-only causal effects.

## Why the final evidence archive is separate from Git

The final archive is approximately 314 MB and contains more than 162,000 files. It is intentionally distributed as one ZIP for archival storage and DOI deposition rather than committed as unpacked Git history.
