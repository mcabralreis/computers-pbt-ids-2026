# Full-Evidence Reproduction Test — R1

The repository analysis script was executed against the complete final PF4-A1 evidence archive.

Input evidence SHA-256:

`3878071e423383dfaa8c1d4a7ebf558681618137f6badfd8edbc913110accebe`

Observed integrity summary:

- ordinals: 81,000;
- perturbations: 243,000;
- ablations: 162,000;
- additivity records: 216,000;
- prediction stable: 234,056;
- prediction changed: 8,944;
- Jaccard@5 defined: 242,588;
- Jaccard@10 defined: 242,086;
- clean Top-5 ties: 137;
- clean Top-10 ties: 304;
- largest unique-profile weighting delta: 0.0031122276.

Validation against the canonical R3 outputs:

```text
PF4_REPRODUCTION_VALIDATION=PASS
MAIN_TABLE_MAX_ABS_DELTA=1.69023877672e-07
ABLATION_TABLE_MAX_ABS_DELTA=3.33066907388e-16
BOUNDARY_TIES=EXACT_MATCH
```

The tiny Jaccard-table delta is below 2e-7 and reflects numerical aggregation/serialization precision rather than a scientific discrepancy.
