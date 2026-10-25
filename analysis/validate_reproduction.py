#!/usr/bin/env python3
"""Validate reproduced PF4 tables against the canonical R3 outputs."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def compare_numeric(canonical: Path, reproduced: Path, keys: list[str], tol: float, numeric_cols: list[str] | None = None) -> float:
    a = pd.read_csv(canonical).sort_values(keys).reset_index(drop=True)
    b = pd.read_csv(reproduced).sort_values(keys).reset_index(drop=True)
    if numeric_cols is None:
        numeric_cols = [c for c in a.columns if c not in keys and pd.api.types.is_numeric_dtype(a[c])]
    merged_cols = [c for c in numeric_cols if c in b.columns]
    if len(a) != len(b):
        raise SystemExit(f"ROW_COUNT_MISMATCH::{canonical.name}::{len(a)}::{len(b)}")
    max_delta = 0.0
    for c in merged_cols:
        av = pd.to_numeric(a[c], errors="coerce").to_numpy(float)
        bv = pd.to_numeric(b[c], errors="coerce").to_numpy(float)
        delta = np.nanmax(np.abs(av - bv)) if len(av) else 0.0
        max_delta = max(max_delta, float(delta))
        if delta > tol:
            raise SystemExit(f"NUMERIC_MISMATCH::{canonical.name}::{c}::delta={delta}::tol={tol}")
    return max_delta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reproduced", required=True, type=Path)
    ap.add_argument("--canonical", default=Path(__file__).resolve().parents[1] / "results" / "pf4_R3", type=Path)
    args = ap.parse_args()

    d1 = compare_numeric(
        args.canonical / "R3_A_main_metrics_mean_sd.csv",
        args.reproduced / "main_metrics_mean_sd.csv",
        ["task", "family"],
        tol=2e-6,
    )
    d2 = compare_numeric(
        args.canonical / "R3_E_ablation_prediction_change.csv",
        args.reproduced / "ablation_prediction_change.csv",
        ["task", "family"],
        tol=1e-12,
        numeric_cols=[
            "top5_prediction_change_mean", "top5_prediction_change_sd",
            "top10_prediction_change_mean", "top10_prediction_change_sd",
            "top10_minus_top5_mean_difference", "exact_two_sided_signflip_p"
        ]
    )
    # Boundary ties must match exactly.
    a = pd.read_csv(args.canonical / "R3_H_boundary_ties.csv").sort_values(["scope","task","family","seed","k"]).reset_index(drop=True)
    b = pd.read_csv(args.reproduced / "boundary_ties.csv").sort_values(["scope","task","family","seed","k"]).reset_index(drop=True)
    if not a.equals(b):
        raise SystemExit("BOUNDARY_TIE_TABLE_MISMATCH")

    print("PF4_REPRODUCTION_VALIDATION=PASS")
    print(f"MAIN_TABLE_MAX_ABS_DELTA={d1:.12g}")
    print(f"ABLATION_TABLE_MAX_ABS_DELTA={d2:.12g}")
    print("BOUNDARY_TIES=EXACT_MATCH")

if __name__ == "__main__":
    main()
