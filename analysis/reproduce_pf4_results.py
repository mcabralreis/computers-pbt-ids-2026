#!/usr/bin/env python3
"""Reproduce the manuscript-grade PF4-A1 tables from the sealed final evidence ZIP.

This script is read-only with respect to the scientific evidence. It does not load
models, execute SHAP, retrain, or modify checkpoints. It parses committed
scientific.json records from the final PF4-A1 evidence archive and regenerates the
summary tables used for the manuscript audit.

Usage:
    python reproduce_pf4_results.py --evidence-zip FINAL_EVIDENCE.zip --outdir out

Tested against the final archive with SHA-256:
3878071e423383dfaa8c1d4a7ebf558681618137f6badfd8edbc913110accebe
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

FINAL_EVIDENCE_SHA256 = "3878071e423383dfaa8c1d4a7ebf558681618137f6badfd8edbc913110accebe"
SCIENTIFIC_RE = re.compile(r"^primary_store/([^/]+)/([^/]+)/seed_(\d+)/checkpoints/ordinal_(\d+)/scientific\.json$")


def sha256_file(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def exact_signflip_p(diffs: np.ndarray) -> float:
    diffs = np.asarray(diffs, dtype=float)
    diffs = diffs[np.isfinite(diffs)]
    n = len(diffs)
    if n == 0:
        return float("nan")
    obs = abs(diffs.mean())
    vals = []
    for signs in itertools.product([-1.0, 1.0], repeat=n):
        vals.append(abs((diffs * np.asarray(signs)).mean()))
    return float(np.mean(np.asarray(vals) >= obs - 1e-15))


def same_nonzero_sign(values: np.ndarray) -> bool:
    a = np.asarray(values, dtype=float)
    a = a[np.isfinite(a)]
    if len(a) == 0 or np.any(np.isclose(a, 0.0, atol=1e-15)):
        return False
    return bool(np.all(a > 0) or np.all(a < 0))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence-zip", required=True, type=Path)
    ap.add_argument("--outdir", required=True, type=Path)
    ap.add_argument("--skip-sha-check", action="store_true")
    args = ap.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    actual_sha = sha256_file(args.evidence_zip)
    if not args.skip_sha_check and actual_sha != FINAL_EVIDENCE_SHA256:
        raise SystemExit(f"EVIDENCE_SHA256_MISMATCH expected={FINAL_EVIDENCE_SHA256} actual={actual_sha}")

    clean_rows = []
    stab_rows = []
    abl_rows = []
    add_rows = []

    with zipfile.ZipFile(args.evidence_zip) as z:
        receipt = json.loads(z.read("audit/PF4_A1_G3_R3_RECEIPT.json"))
        if receipt.get("final_sealed") != 81000 or receipt.get("status") != "PASS":
            raise SystemExit("FINAL_RECEIPT_NOT_PASS_81000")

        sci_names = [n for n in z.namelist() if SCIENTIFIC_RE.match(n)]
        if len(sci_names) != 81000:
            raise SystemExit(f"SCIENTIFIC_COUNT_MISMATCH::{len(sci_names)}")

        for ix, name in enumerate(sci_names, 1):
            obj = json.loads(z.read(name))
            task = obj["task"]
            family = obj["family"]
            seed = int(obj["seed"])
            ordinal = int(obj["ordinal"])
            prof = obj["profile"]
            clean_rows.append({
                "task": task,
                "family": family,
                "seed": seed,
                "ordinal": ordinal,
                "x_test_index": int(obj["x_test_index"]),
                "clean_class": int(obj["clean_class"]),
                "encoded_profile_sha256": prof["encoded_profile_sha256_raw_float32"],
            })

            for s in obj["stability"]:
                stab_rows.append({
                    "task": task,
                    "family": family,
                    "seed": seed,
                    "ordinal": ordinal,
                    "x_test_index": int(s["x_test_index"]),
                    "intensity": float(s["intensity"]),
                    "prediction_stable": bool(s["prediction_stable"]),
                    "jaccard5": s.get("jaccard_5"),
                    "jaccard10": s.get("jaccard_10"),
                    "spearman": s.get("spearman"),
                    "normalized_L1": s.get("normalized_L1"),
                    "jaccard5_status": s.get("jaccard_5_status", "DEFINED" if s.get("jaccard_5") is not None else "NA"),
                    "jaccard10_status": s.get("jaccard_10_status", "DEFINED" if s.get("jaccard_10") is not None else "NA"),
                    "perturbed_feature": s.get("perturbed_source_feature"),
                })

            for a in obj["ablation"]:
                status = a.get("status", "LEGACY_DEFINED")
                abl_rows.append({
                    "task": task,
                    "family": family,
                    "seed": seed,
                    "ordinal": ordinal,
                    "k": int(a["k"]),
                    "status": status,
                    "prediction_changed": a.get("prediction_changed"),
                    "score_drop": a.get("score_drop"),
                    "effective_count": a.get("effective_count"),
                    "encoded_noop": a.get("encoded_noop"),
                })

            add = obj.get("additivity")
            if isinstance(add, list):
                for a in add:
                    add_rows.append({
                        "task": task,
                        "family": family,
                        "seed": seed,
                        "ordinal": ordinal,
                        "level": a.get("level"),
                        "absolute_residual": a.get("absolute_residual"),
                        "native_score": a.get("native_score"),
                        "reconstructed_score": a.get("reconstructed_score"),
                    })

            if ix % 10000 == 0:
                print(f"parsed {ix}/81000 scientific records", flush=True)

    clean = pd.DataFrame(clean_rows)
    stab = pd.DataFrame(stab_rows)
    abl = pd.DataFrame(abl_rows)
    add = pd.DataFrame(add_rows)

    # Normalize numeric columns; NAs remain NAs.
    for c in ["jaccard5", "jaccard10", "spearman", "normalized_L1"]:
        stab[c] = pd.to_numeric(stab[c], errors="coerce")
    stab["prediction_stable_rate"] = stab["prediction_stable"].astype(float)

    metric_cols = ["prediction_stable_rate", "jaccard5", "jaccard10", "spearman", "normalized_L1"]

    # Seed-level pooled means across all three intensities.
    seed_means = stab.groupby(["task", "family", "seed"], as_index=False)[metric_cols].mean()
    seed_means = seed_means.rename(columns={
        "jaccard5": "j5_mean", "jaccard10": "j10_mean",
        "spearman": "spearman_mean", "normalized_L1": "l1_mean"
    })
    seed_means.to_csv(args.outdir / "seed_level_means.csv", index=False)

    # Main manuscript mean +/- between-seed SD.
    rows = []
    for (task, family), g in seed_means.groupby(["task", "family"], sort=True):
        rows.append({
            "task": task, "family": family,
            "prediction_stability_mean": g["prediction_stable_rate"].mean(),
            "prediction_stability_sd": g["prediction_stable_rate"].std(ddof=1),
            "jaccard5_mean": g["j5_mean"].mean(), "jaccard5_sd": g["j5_mean"].std(ddof=1),
            "jaccard10_mean": g["j10_mean"].mean(), "jaccard10_sd": g["j10_mean"].std(ddof=1),
            "spearman_mean": g["spearman_mean"].mean(), "spearman_sd": g["spearman_mean"].std(ddof=1),
            "normalized_L1_mean": g["l1_mean"].mean(), "normalized_L1_sd": g["l1_mean"].std(ddof=1),
        })
    main_df = pd.DataFrame(rows)
    main_df.to_csv(args.outdir / "main_metrics_mean_sd.csv", index=False)

    # Seed-aware family contrasts, paired by seed.
    metric_names = ["prediction_stable_rate", "j5_mean", "j10_mean", "spearman_mean", "l1_mean"]
    families = sorted(seed_means["family"].unique())
    contrast_rows = []
    for task in sorted(seed_means["task"].unique()):
        t = seed_means[seed_means.task == task]
        for a, b in itertools.combinations(families, 2):
            ga = t[t.family == a].set_index("seed")
            gb = t[t.family == b].set_index("seed")
            common = sorted(set(ga.index) & set(gb.index))
            for metric in metric_names:
                diffs = np.array([ga.loc[s, metric] - gb.loc[s, metric] for s in common], dtype=float)
                contrast_rows.append({
                    "task": task, "family_A": a, "family_B": b, "metric": metric,
                    "n_paired_seeds": len(common), "mean_difference_A_minus_B": diffs.mean(),
                    "median_difference": np.median(diffs), "min_difference": diffs.min(), "max_difference": diffs.max(),
                    "same_direction_all_5_seeds": same_nonzero_sign(diffs),
                    "exact_two_sided_signflip_p": exact_signflip_p(diffs),
                })
    pd.DataFrame(contrast_rows).to_csv(args.outdir / "model_contrasts_seed_paired.csv", index=False)

    # Intensity effects 0.10 - 0.01 at seed level.
    by_i = stab.groupby(["task", "family", "seed", "intensity"], as_index=False)[metric_cols].mean()
    by_i = by_i.rename(columns={"jaccard5": "j5_mean", "jaccard10": "j10_mean", "spearman": "spearman_mean", "normalized_L1": "l1_mean"})
    irows = []
    for (task, family), g in by_i.groupby(["task", "family"]):
        lo = g[np.isclose(g.intensity, 0.01)].set_index("seed")
        hi = g[np.isclose(g.intensity, 0.10)].set_index("seed")
        common = sorted(set(lo.index) & set(hi.index))
        for metric in metric_names:
            diffs = np.array([hi.loc[s, metric] - lo.loc[s, metric] for s in common], dtype=float)
            irows.append({
                "task": task, "family": family, "metric": metric,
                "contrast": "intensity_0.10_minus_0.01", "n_paired_seeds": len(common),
                "mean_difference": diffs.mean(), "median_difference": np.median(diffs),
                "min_difference": diffs.min(), "max_difference": diffs.max(),
                "same_sign_all_seeds": same_nonzero_sign(diffs),
                "exact_two_sided_signflip_p": exact_signflip_p(diffs),
            })
    pd.DataFrame(irows).to_csv(args.outdir / "intensity_effects_seed_paired.csv", index=False)

    # Ablation prediction-change rates; exclude structural NA.
    abl_defined = abl[abl["status"] != "NA_BOUNDARY_TIE"].copy()
    abl_defined["prediction_change_rate"] = pd.to_numeric(abl_defined["prediction_changed"], errors="coerce").astype(float)
    abl_seed = abl_defined.groupby(["task", "family", "seed", "k"], as_index=False)["prediction_change_rate"].mean()
    arows = []
    for (task, family), g in abl_seed.groupby(["task", "family"]):
        g5 = g[g.k == 5].set_index("seed")["prediction_change_rate"]
        g10 = g[g.k == 10].set_index("seed")["prediction_change_rate"]
        common = sorted(set(g5.index) & set(g10.index))
        diffs = np.array([g10.loc[s] - g5.loc[s] for s in common], dtype=float)
        arows.append({
            "task": task, "family": family,
            "top5_prediction_change_mean": g5.mean(), "top5_prediction_change_sd": g5.std(ddof=1),
            "top10_prediction_change_mean": g10.mean(), "top10_prediction_change_sd": g10.std(ddof=1),
            "top10_minus_top5_mean_difference": diffs.mean(),
            "same_direction_all_5_seeds": same_nonzero_sign(diffs),
            "exact_two_sided_signflip_p": exact_signflip_p(diffs),
        })
    pd.DataFrame(arows).to_csv(args.outdir / "ablation_prediction_change.csv", index=False)

    # Boundary-tie accounting.
    tie_rows = []
    clean_tied = set()
    for (task, family, seed, k), g in abl[abl.status == "NA_BOUNDARY_TIE"].groupby(["task", "family", "seed", "k"]):
        events = len(g)
        tie_rows.append({"scope": "clean", "task": task, "family": family, "seed": seed, "k": k, "events": events})
        for ordinal in g.ordinal.tolist():
            clean_tied.add((task, family, int(seed), int(ordinal), int(k)))
    for k, status_col in [(5, "jaccard5_status"), (10, "jaccard10_status")]:
        q = stab[stab[status_col] == "NA_BOUNDARY_TIE"]
        counts = {}
        for r in q.itertuples(index=False):
            key = (r.task, r.family, int(r.seed), int(r.ordinal), k)
            if key not in clean_tied:
                ckey = (r.task, r.family, int(r.seed), k)
                counts[ckey] = counts.get(ckey, 0) + 1
        for (task, family, seed, k2), events in counts.items():
            tie_rows.append({"scope": "perturbed_only", "task": task, "family": family, "seed": seed, "k": k2, "events": events})
    ties_df = pd.DataFrame(tie_rows).sort_values(["scope", "task", "family", "seed", "k"])
    ties_df.to_csv(args.outdir / "boundary_ties.csv", index=False)

    # Duplicate weighting sensitivity: one canonical ordinal per unique encoded profile in each task/family/seed cell.
    keep = (clean.sort_values("ordinal")
                  .drop_duplicates(["task", "family", "seed", "encoded_profile_sha256"])
                  [["task", "family", "seed", "ordinal"]])
    unique_stab = stab.merge(keep, on=["task", "family", "seed", "ordinal"], how="inner")
    canonical = stab.groupby(["task", "family"], as_index=False)[metric_cols].mean()
    unique = unique_stab.groupby(["task", "family"], as_index=False)[metric_cols].mean()
    dup = canonical.merge(unique, on=["task", "family"], suffixes=("_canonical", "_unique_profile_weighted"))
    dup.to_csv(args.outdir / "duplicate_weighting_sensitivity.csv", index=False)

    # Class and feature heterogeneity at intensity 0.10.
    s10 = stab[np.isclose(stab.intensity, 0.10)].merge(clean[["task", "family", "seed", "ordinal", "clean_class"]], on=["task", "family", "seed", "ordinal"], how="left")
    class_summary = s10.groupby(["task", "family", "clean_class"], as_index=False).agg(
        n=("ordinal", "size"), prediction_stable_rate=("prediction_stable_rate", "mean"), j5_mean=("jaccard5", "mean"))
    class_summary.to_csv(args.outdir / "class_stability_intensity_0p10.csv", index=False)
    feature_summary = s10.groupby(["task", "family", "perturbed_feature"], as_index=False).agg(
        n=("ordinal", "size"), prediction_stable_rate=("prediction_stable_rate", "mean"), j5_mean=("jaccard5", "mean"))
    feature_summary.to_csv(args.outdir / "feature_stability_intensity_0p10.csv", index=False)

    # Additivity support table (descriptive only).
    if len(add):
        add["relative_residual"] = add["absolute_residual"] / np.maximum(np.abs(add["native_score"]), 1e-12)
        add_summary = add.groupby(["task", "family", "level"], as_index=False).agg(
            n=("absolute_residual", "size"),
            absolute_residual_mean=("absolute_residual", "mean"),
            absolute_residual_median=("absolute_residual", "median"),
            relative_residual_mean=("relative_residual", "mean"),
            relative_residual_median=("relative_residual", "median"),
        )
        add_summary.to_csv(args.outdir / "additivity_support.csv", index=False)

    summary = {
        "evidence_sha256": actual_sha,
        "final_sealed_ordinals": int(len(clean)),
        "perturbation_records": int(len(stab)),
        "ablation_records": int(len(abl)),
        "additivity_records": int(len(add)),
        "prediction_stable": int(stab.prediction_stable.sum()),
        "prediction_changed": int((~stab.prediction_stable).sum()),
        "jaccard5_defined": int(stab.jaccard5.notna().sum()),
        "jaccard10_defined": int(stab.jaccard10.notna().sum()),
        "clean_top5_ties": int(((abl.status == "NA_BOUNDARY_TIE") & (abl.k == 5)).sum()),
        "clean_top10_ties": int(((abl.status == "NA_BOUNDARY_TIE") & (abl.k == 10)).sum()),
        "unique_profile_max_abs_metric_delta": float(max(abs((dup[c.replace('_canonical','_unique_profile_weighted')] - dup[c]).dropna()).max() for c in [x for x in dup.columns if x.endswith('_canonical')])),
    }
    (args.outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
