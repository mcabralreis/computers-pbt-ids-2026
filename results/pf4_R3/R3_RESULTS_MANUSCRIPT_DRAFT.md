# PF4-A1 manuscript-grade results synthesis (R3)

## Prediction robustness and explanation stability

Across the three evaluation tasks, prediction stability and explanation stability behaved as related but clearly distinct properties. LIN showed the most stable SHAP explanations in every task, with the highest Jaccard@5 and Jaccard@10 overlap, the highest Spearman rank agreement, and the lowest normalized L1 deviation. In contrast, the MLP retained highly stable predicted classes while its SHAP explanations changed substantially more under the same frozen perturbation protocol. This decoupling was strongest in CIC34 and TON2, where MLP prediction stability remained close to 0.98–0.99 while mean Jaccard@5 was only about 0.83–0.84.

HGB showed a different robustness profile. Its explanations were generally more stable than those of MLP, but its predicted classes were more sensitive to perturbation, particularly in CIC34 and TON10. Prediction-level robustness therefore cannot be used as a proxy for explanation-level robustness.

## Seed-aware contrasts

The main between-model patterns were highly consistent across the five seeds. Of 45 task-by-metric paired family contrasts, 44 had the same direction in all five seeds. The only exception was the very small LIN-versus-MLP difference in TON10 prediction stability. For Jaccard@5, the mean paired LIN advantage over MLP was approximately +0.165 in CIC34, +0.093 in TON10, and +0.144 in TON2. The corresponding normalized-L1 differences were approximately -0.133, -0.109, and -0.151.

With five seeds, an exact two-sided sign-flip test is intrinsically coarse: even a five-of-five directional effect gives p=0.0625. The manuscript should therefore emphasize effect magnitude, between-seed dispersion, and directional consistency rather than conventional p<0.05 claims.

## Perturbation intensity

Increasing intensity from 0.01 to 0.10 generally reduced robustness. Thirty-nine of 45 task-by-family-by-metric contrasts had the same direction in all five seeds. HGB showed clear intensity sensitivity; its mean prediction-stability change was approximately -0.068 in CIC34 and -0.064 in TON10. MLP was less strictly monotonic for overlap and rank metrics, although prediction stability still generally deteriorated.

## Predicted-class and perturbed-feature heterogeneity

Global averages conceal multiclass heterogeneity. At intensity 0.10, the range between the most and least prediction-stable predicted-class strata was about 0.300 for CIC34/HGB and 0.250 for TON10/HGB. These are clean predicted-class strata, not ground-truth class-specific error rates.

Robustness also depends on the perturbed source feature. In CIC34/HGB, perturbations involving Tot sum, Max and Rate were among the most disruptive, whereas Variance and Time_To_Live were comparatively robust. In TON10 and TON2, src_ip_bytes was among the most prediction-sensitive HGB perturbations. Feature-level results also reveal local prediction/explanation decoupling: a perturbation may leave the class almost unchanged while still altering Top-k SHAP composition.

## Top-k ablation

Ablation should be treated as functional masking/fidelity evidence rather than direct causal importance. Prediction-change rates are high for many task/model combinations, but the response is not always monotonic in k. The clearest example is TON2/LIN: the mean prediction-change rate falls from about 0.491 under Top-5 masking to about 0.201 under Top-10 masking, with the same direction in all five seeds. The current analysis establishes this non-monotonic response but does not assign a unique mechanism. Raw score-drop magnitude should not be compared across HGB/LIN/MLP because their score semantics/scales are not guaranteed to be common.

## Protocol robustness

PF4-A1 retained Top-k boundary ties as structural NA rather than resolving them by arbitrary ordering. The full campaign contains 137 clean Top-5 ties, 304 clean Top-10 ties, and three perturbation-only ties.

Canonical ordinals were intentionally preserved even when encoded profiles repeated. Reweighting to one ordinal per unique encoded profile did not change the substantive results; the largest absolute change in a principal pooled metric across the nine task/model cells was only about 0.0031.

## Recommended hierarchy

Primary: (1) prediction/explanation decoupling; (2) LIN explanation robustness; (3) HGB prediction sensitivity with stable explanations; (4) intensity effects. Secondary/supplementary: predicted-class heterogeneity, feature sensitivity, Top-k ablation non-monotonicity, boundary ties, duplicate-profile sensitivity, and additivity diagnostics.
