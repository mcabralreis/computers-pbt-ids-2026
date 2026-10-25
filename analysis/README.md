# PF4 Analysis Reproduction

`reproduce_pf4_results.py` reads the final sealed PF4-A1 evidence ZIP and regenerates the manuscript-grade summary tables without executing models or SHAP.

Example:

```bash
python analysis/reproduce_pf4_results.py --evidence-zip FINAL_EVIDENCE.zip --outdir reproduced_pf4
python analysis/validate_reproduction.py --reproduced reproduced_pf4
```

The full archive run was tested against the final evidence SHA-256 and completed with the expected 81,000 ordinals / 243,000 perturbation records. The canonical manuscript table agrees within numerical tolerance; ablation results and boundary-tie accounting agree exactly at the reported precision/semantics.
