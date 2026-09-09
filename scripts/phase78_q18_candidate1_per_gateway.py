#!/usr/bin/env python3
"""
phase78_q18_candidate1_per_gateway.py -- CAIL-RH Investigation, Phase 78 Q-18
Chavez AI Labs LLC -- Applied Pathological Mathematics

Q-18 Candidate 1: Per-Gateway Explicit-Formula Weighting.

Hypothesis (per CLAUDE_CODE_HANDOFF_PHASE78_Q18.md Sec 3): reading all six
Canonical Six gateways under the Detector Encoding and combining them with
inverse-variance (z-score) weights beats the two-gateway Detector (c_S2+c_S6,
z=8.42) baseline from Phase 77 Q-17.

Structural pre-check (done analytically before running): under the Detector
Encoding (pos2=0, u_2/u_6 slots only), gateway c_g(x) = -2<x, U_g> reduces to:
  S2 = -2*(w2 cos + w3 cos + w11 cos + w13 cos)   [documented primary]
  S6 = -2*(w5 cos + w7 cos)                        [documented secondary]
  S3 = -2*(w5 cos + w7 cos)                        == S6 EXACTLY (support
       indices {4,11} are zeroed by the encoding, leaving only {6,9} shared
       with S6)
  S1 = -2*t - 2*w2 cos - 2*w13 cos                 [t-dominated]
  S4 = -2*t - 2*w2 cos + 2*w13 cos                 [t-dominated]
  S5 = -2*t - 2*w3 cos - 2*w11 cos                 [t-dominated]
This script verifies that algebra numerically, then implements the doc's
literal Step 1-4 ensemble design, evaluated BOTH in-sample (full 101 zeros,
matching the doc's literal instructions) and on a held-out split (train
weights on the first 50 zeros, evaluate on the remaining 51) to guard against
the lookahead bias of fitting per-gateway weights and the final z-score on
the same data.

Output: ../results/phase78_q18_candidate1_results.json + console summary.
"""
import json
import math

import numpy as np

PRIMES = (2, 3, 5, 7, 11, 13)
LN = {p: math.log(p) for p in PRIMES}
W = {p: math.log(p) / math.sqrt(p) for p in PRIMES}


def vec(*pairs, n=16):
    v = np.zeros(n)
    for i, val in pairs:
        v[i] = val
    return v


PATTERNS = {
    1: (vec((1, 1), (14, 1)),  vec((3, 1), (12, 1))),
    2: (vec((3, 1), (12, 1)),  vec((5, 1), (10, 1))),
    3: (vec((4, 1), (11, 1)),  vec((6, 1), (9, 1))),
    4: (vec((1, 1), (14, -1)), vec((3, 1), (12, -1))),
    5: (vec((1, 1), (14, -1)), vec((5, 1), (10, 1))),
    6: (vec((2, 1), (13, -1)), vec((6, 1), (9, 1))),
}
U = {g: P + Q for g, (P, Q) in PATTERNS.items()}
CLASS_A = (2, 3, 6)
CLASS_B = (1, 4, 5)


def detector_encoding_batch(sigma, T):
    """Q-17 Detector Encoding, unmodified (see phase77_q17_signed_channel.py)."""
    X = np.zeros((len(T), 16))
    X[:, 0] = sigma
    X[:, 1] = T
    X[:, 3] = W[2] * np.cos(T * LN[2])
    X[:, 5] = W[3] * np.cos(T * LN[3])
    X[:, 10] = W[11] * np.cos(T * LN[11])
    X[:, 12] = W[13] * np.cos(T * LN[13])
    X[:, 6] = W[5] * np.cos(T * LN[5])
    X[:, 9] = W[7] * np.cos(T * LN[7])
    return X


def c_channel(X, g):
    return -2.0 * X @ U[g]


def t1_value_at_zeros(T, Y, zeros, n_trials=5000, seed=20260612):
    rng = np.random.default_rng(seed)
    obs = float(np.mean(np.interp(zeros, T, Y)))
    null = np.array([
        np.mean(np.interp(rng.uniform(T[0], T[-1], len(zeros)), T, Y))
        for _ in range(n_trials)])
    z = float((obs - null.mean()) / null.std())
    p_two = float(min(1.0, 2 * min(np.mean(null <= obs), np.mean(null >= obs))))
    return {"n_zeros": len(zeros), "observed": obs, "null_mean": float(null.mean()),
            "null_std": float(null.std()), "z": z, "p_two_sided": p_two}


def roc_auc(T, Y, zeros, delta):
    zarr = np.asarray(zeros)
    dist = np.min(np.abs(T[:, None] - zarr[None, :]), axis=1)
    pos = Y[dist < delta]
    neg = Y[dist >= delta]
    ranks = np.argsort(np.argsort(np.concatenate([pos, neg]))) + 1
    r_pos = ranks[:len(pos)].sum()
    auc = (r_pos - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))
    return {"delta": delta, "n_pos": int(len(pos)), "n_neg": int(len(neg)), "auc": float(auc)}


def local_maxima(T, Y):
    idx = np.where((Y[1:-1] > Y[:-2]) & (Y[1:-1] > Y[2:]))[0] + 1
    return T[idx], Y[idx]


def peak_matching(T, Y, zeros, eps):
    pt, pv = local_maxima(T, Y)
    order = np.argsort(-pv)
    zarr = np.asarray(zeros)
    best = {"f1": 0.0}
    for k in range(1, len(order) + 1):
        sel = np.sort(pt[order[:k]])
        used = np.zeros(len(zarr), bool)
        tp = 0
        for p in sel:
            d = np.abs(zarr - p)
            d[used] = np.inf
            j = int(np.argmin(d))
            if d[j] < eps:
                used[j] = True
                tp += 1
        prec = tp / k
        rec = tp / len(zarr)
        f1 = 2 * prec * rec / (prec + rec) if prec + rec > 0 else 0.0
        if f1 > best["f1"]:
            best = {"f1": f1, "precision": prec, "recall": rec, "n_predictions": k}
    return {"eps": eps, "n_maxima": int(len(pt)), "best": best}


if __name__ == "__main__":
    zeros_all = json.load(open("../data/riemann/rh_zeros.json"))
    T_LO, T_HI, DT = 10.0, 240.0, 0.005
    T = np.arange(T_LO, T_HI + DT / 2, DT)
    zin = [z for z in zeros_all if T_LO + 1 < z < T_HI - 1]
    print(f"grid: {len(T)} pts in [{T_LO},{T_HI}]; zeros in range: {len(zin)}")

    X = detector_encoding_batch(0.5, T)
    C = {g: c_channel(X, g) for g in range(1, 7)}
    detector_baseline = C[2] + C[6]

    results = {"phase": "78", "question": "Q-18", "candidate": "1_per_gateway_weighting",
               "grid": {"t_lo": T_LO, "t_hi": T_HI, "dt": DT, "n": int(len(T))},
               "zeros_in_range": len(zin)}

    # ---- 0. structural pre-check: verify the redundancy/degeneracy claims ----
    print("\n=== 0. STRUCTURAL PRE-CHECK ===")
    s3_eq_s6 = float(np.max(np.abs(C[3] - C[6])))
    print(f"  max|c_S3 - c_S6| = {s3_eq_s6:.3e}  (should be ~0: S3 degenerates to S6"
          f" under Detector Encoding)")
    t_slope_s1 = float(np.polyfit(T, C[1], 1)[0])
    print(f"  linear slope of c_S1 vs t = {t_slope_s1:.4f} (expect approx -2: t-dominated)")
    results["structural_precheck"] = {
        "max_abs_cS3_minus_cS6": s3_eq_s6,
        "cS1_linear_slope_vs_t": t_slope_s1,
        "note": "S3 is algebraically identical to S6 under the Detector Encoding "
                "(their differentiating support indices {4,11} vs {2,13} are all "
                "zeroed by the encoding, leaving only the shared {6,9} slots). "
                "S1/S4/S5 (Class B) are dominated by a -2t linear term from the "
                "shared pos1=t protocol slot in their support.",
    }

    # ---- 1. per-gateway z-scores (doc Step 2) --------------------------------
    print("\n=== 1. PER-GATEWAY z-SCORES (T1 value-at-zeros, full 101) ===")
    z_full = {g: t1_value_at_zeros(T, C[g], zin)["z"] for g in range(1, 7)}
    for g in range(1, 7):
        cls = "A" if g in CLASS_A else "B"
        print(f"  S{g} ({cls}): z = {z_full[g]:+.3f}")
    results["per_gateway_z_full101"] = z_full

    # ---- 2. doc's literal ensemble (Step 3), evaluated in-sample -------------
    sumz = sum(z_full.values())
    weights_insample = {g: (z_full[g] / sumz) ** 2 for g in range(1, 7)}
    ensemble_insample = sum(weights_insample[g] * C[g] for g in range(1, 7))
    d_ens_full = t1_value_at_zeros(T, ensemble_insample, zin)
    d_base_full = t1_value_at_zeros(T, detector_baseline, zin)
    print("\n=== 2. ENSEMBLE, IN-SAMPLE (weights fit AND evaluated on same 101 zeros) ===")
    print(f"  weights (z_g/sum z)^2: " +
          ", ".join(f"S{g}={weights_insample[g]:.3f}" for g in range(1, 7)))
    print(f"  ensemble z = {d_ens_full['z']:.2f}   baseline (c_S2+c_S6) z = {d_base_full['z']:.2f}")
    results["insample"] = {"weights": weights_insample,
                            "ensemble_t1": d_ens_full, "baseline_t1": d_base_full,
                            "caveat": "weights are fit on the same 101 zeros used to "
                                      "evaluate z here -- optimistic, matches the doc's "
                                      "literal Step 2-4 instructions but is lookahead-biased."}

    # ---- 3. honest held-out split (train weights on first 50, test on rest) --
    train, test = zin[:50], zin[50:]
    z_train = {g: t1_value_at_zeros(T, C[g], train)["z"] for g in range(1, 7)}
    sumz_t = sum(z_train.values())
    weights_train = {g: (z_train[g] / sumz_t) ** 2 for g in range(1, 7)}
    ensemble_test_signal = sum(weights_train[g] * C[g] for g in range(1, 7))
    d_ens_test = t1_value_at_zeros(T, ensemble_test_signal, test)
    d_base_test = t1_value_at_zeros(T, detector_baseline, test)
    print(f"\n=== 3. HELD-OUT: weights fit on first {len(train)} zeros, "
          f"evaluated on remaining {len(test)} ===")
    print(f"  weights (z_g/sum z)^2: " +
          ", ".join(f"S{g}={weights_train[g]:.3f}" for g in range(1, 7)))
    print(f"  ensemble z = {d_ens_test['z']:.2f}   baseline (c_S2+c_S6) z = {d_base_test['z']:.2f}"
          f"   (baseline uses no fitting, so this is the fair comparison)")
    results["heldout"] = {"train_n": len(train), "test_n": len(test),
                           "weights": weights_train,
                           "ensemble_t1": d_ens_test, "baseline_t1": d_base_test}

    # ---- 4. ROC / peak-matching for the in-sample ensemble (for completeness) -
    print("\n=== 4. ROC / PEAK MATCHING (in-sample ensemble vs baseline, full 101) ===")
    results["roc"] = {}
    results["peaks"] = {}
    for name, Y in (("ensemble_insample", ensemble_insample), ("baseline", detector_baseline)):
        results["roc"][name] = [roc_auc(T, Y, zin, d) for d in (0.25, 0.5)]
        results["peaks"][name] = [peak_matching(T, Y, zin, e) for e in (0.5, 1.0)]
        for r in results["roc"][name]:
            print(f"  {name:20s} delta={r['delta']:4}: AUC = {r['auc']:.4f}")

    verdict = ("NO IMPROVEMENT: held-out ensemble z (%.2f) does not beat the unfitted "
               "baseline (%.2f); in-sample 'improvement' is a fitting artifact from "
               "reusing the evaluation zeros to set weights, amplified by the S3=S6 "
               "degeneracy (double-counts the {5,7} prime channel) and t-dominated "
               "noise from S1/S4/S5."
               % (d_ens_test["z"], d_base_test["z"]))
    if d_ens_test["z"] > d_base_test["z"]:
        verdict = ("HELD-OUT IMPROVEMENT: ensemble z (%.2f) beats baseline z (%.2f) "
                   "on data not used to fit weights." % (d_ens_test["z"], d_base_test["z"]))
    print(f"\nVERDICT: {verdict}")
    results["verdict"] = verdict

    with open("../results/phase78_q18_candidate1_results.json", "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("\nwrote ../results/phase78_q18_candidate1_results.json")
