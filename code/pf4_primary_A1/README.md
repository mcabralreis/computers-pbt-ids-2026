# R7-D35-PF4-PRIMARY-P1 — original full-XAI 45-case campaign

The user explicitly approved primary PF4 on 2026-10-02. This **new separate authorization** does not amend the historical D32 contract (where `primary_PF4_approved=false`) and DOES NOT authorize PF5 or RF. Model weights, encoders, raw cohorts, XAI indices, D24 case manifest, PF1 representation-effective generator, thresholds, and score adapters are unchanged.

The immutable canonical XAI has 3,400 CIC34 ordinals per case and 1,000 TON10/TON2 ordinals per case. All 45 task/family/seed cases are in the exact static D24 manifest (15 per task; 5 seeds per family). **TON ordinals 0 and 1 may have identical encoded features; they remain separate canonical XAI observations with duplicate membership to be recorded at population-summary time. Do not swap ordinal 1 for ordinal 8 in primary.** C3 ordinal 8 was exploratory only and is not used for selection here.

Each original XAI ordinal is processed as one clean + original PF1 draw-0 candidate at each intensity 0.01/0.05/0.10 (NA remains NA). The exact frozen train-only 256-row background; actual SHAP native outputs; fixed clean-class axis except binary LIN/HGB native scalar zero; source-feature SHAP magnitude=sum(abs(encoded SHAP)), signed=sum(SHAP). Top-k Jaccard@5/@10, tied-average Spearman, normalized L1. An unresolved boundary tie fails closed; no hidden tie rule. Historical clean-class score is used for raw missing/baseline top-5/top-10 ablations, with TON2 `p1` or `1-p1` independently of native SHAP. Signed negative drops stay negative. LIN and HGB native additivity residual with no threshold; MLP N/A. Prediction stability is reported; **PF5 is not evaluated or authorized in this package**.

One checkpoint directory per canonical XAI ordinal: `primary_store/TASK/FAMILY/seed_N/checkpoints/ordinal_000000/{scientific.json,COMMITTED.json}`; SHA256 and byte lengths checked upon each resume. A checkpoint is atomically renamed from `.staging` only after verified. A partial `.staging`, missing/malformed seal, unknown file, changed model/hash/manifest, or top-k tie is fail-closed; never delete or overwrite automatically. `CASE_CONTEXT.json` pins source package, case, and D24. Tranches use `--max-new-per-case N`, **not cohort subsampling**. First actual primary tranche is TON2/LIN_SGD_LOGISTIC/seed 11, up to 8 original ordinals, and the same case will continue from ordinal 8 onward if successful.

Usage (Python 3.10 in original frozen Windows ROOT):

```
py -3.10 run_primary.py --self-test
py -3.10 run_primary.py --root ROOT --store NEW_PRIMARY_STORE --transaction-dir NEW_LOG_DIR --evidence NEW_EVIDENCE_ZIP --task TON2 --family LIN_SGD_LOGISTIC --seed 11 --max-new-per-case 8
py -3.10 run_primary.py --status --store PRIMARY_STORE
```

Subsequent explicit transactions may use `--all --max-new-per-case 25` (new `--transaction-dir`, new `--evidence` for each). Completed sealed ordinals are always independently verified and reused. The per-case model/explainer is loaded once per transaction (not once per ordinal). With 45 cases, full primary can be computationally substantial: checkpoint/resume is a requirement, not an optional pilot. Each transaction archives its logs, source and applicable sealed checkpoint state even on failure, with full archive SHA256. On failure, preserve the `.staging` and send the ZIP; no blind reruns. ZIP output and logs are always **outside** the extracted frozen source package to avoid the previous `SOURCE_PACKAGE_FILESET` error.

Offline source selftests cannot substitute for a genuine Windows SHAP run. After the first real tranche, independently adjudicate true scientific checkpoint output before increasing compute allocation. Any batch of 8 is **primary partial execution**, not a separate exploratory pilot and not the complete primary claim.
