#!/usr/bin/env python3
"""
phase77_q17_signed_channel.py — CAIL-RH Investigation, Phase 77 Q-17
Chavez AI Labs LLC — Applied Pathological Mathematics

Q-17: Characterize the Signed Gateway Channel (discovered in Q-15) as a
Riemann-zero detector.

  1. SCALE     — extend the c_S2 value-at-zeros statistic from gamma_1..31
                 to gamma_1..100; a genuine signal should strengthen ~sqrt(N).
  2. DETECTOR  — the Detector Encoding: u_2 support = {3,5,10,12} and
                 u_6 support = {2,6,9,13} are disjoint, so placing
                 w_p cos(t ln p), w_p = log p / sqrt p, in those slots makes

                   c_S2 + c_S6  =  -2 * sum_{p in {2,3,5,7,11,13}} w_p cos(t ln p)

                 — the full k=1 explicit-formula 6-prime detector, realized
                 EXACTLY as two signed readings of the existing instrument.
                 (Deliberate deviation from the Phase 76 Documented F(s)
                 Encoding; purpose-built detector input, documented here.)
  3. ROC       — value-based AUC (Mann-Whitney) and peak-matching
                 precision/recall/F1 against gamma_1..100.

All channels are linear functionals (Gateway Linear Law, Phase 76):
c_g(x) = -2 <x, P_g + Q_g>. Live server validation is recorded separately
in results/phase77_q17_live_validation.json.

Output: ../results/phase77_q17_results.json + console summary.
"""
import json
import math

import numpy as np

SQRT2 = math.sqrt(2.0)
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


def f_encoding_batch(sigma, T):
    """Phase 76 Documented F(s) Encoding."""
    X = np.zeros((len(T), 16))
    X[:, 0] = sigma
    X[:, 1] = T
    X[:, 2] = sigma - 0.5 + 0.0019
    X[:, 3] = np.cos(T * LN[2])
    X[:, 4] = np.sin(T * LN[3]) / SQRT2
    X[:, 5] = np.sin(T * LN[3])
    X[:, 6] = np.cos(T * LN[5])
    X[:, 7] = np.sin(T * LN[5]) / SQRT2
    X[:, 8] = np.cos(T * LN[7])
    X[:, 9] = np.sin(T * LN[7]) / SQRT2
    X[:, 10] = np.cos(T * LN[11])
    X[:, 11] = np.sin(T * LN[11]) / SQRT2
    X[:, 12] = np.cos(T * LN[13])
    X[:, 13] = np.sin(T * LN[13]) / SQRT2
    return X


def detector_encoding_batch(sigma, T):
    """Q-17 Detector Encoding (deviation from Documented Encoding, by design).

    u_2 support {3,5,10,12} <- w_p cos(t ln p), p = 2, 3, 11, 13
    u_6 support {6,9}       <- w_p cos(t ln p), p = 5, 7   (slots 2, 13 = 0)
    pos0 = sigma, pos1 = t (protocol slots; not in u_2/u_6 supports except
    pos2 which is set to 0 here so c_S6 is a pure prime functional).
    """
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
    """Mann-Whitney AUC: does the channel value rank near-zero points above
    far-from-zero points? Ground truth: dist(t, nearest zero) < delta."""
    zarr = np.asarray(zeros)
    dist = np.min(np.abs(T[:, None] - zarr[None, :]), axis=1)
    pos = Y[dist < delta]
    neg = Y[dist >= delta]
    # rank-based AUC
    ranks = np.argsort(np.argsort(np.concatenate([pos, neg]))) + 1
    r_pos = ranks[:len(pos)].sum()
    auc = (r_pos - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))
    return {"delta": delta, "n_pos": int(len(pos)), "n_neg": int(len(neg)),
            "auc": float(auc)}


def local_maxima(T, Y):
    idx = np.where((Y[1:-1] > Y[:-2]) & (Y[1:-1] > Y[2:]))[0] + 1
    return T[idx], Y[idx]


def peak_matching(T, Y, zeros, eps):
    """Sweep height threshold over the channel's local maxima; greedy 1-1
    matching of predicted peaks to zeros within eps; report best F1 and the
    precision/recall curve summary."""
    pt, pv = local_maxima(T, Y)
    order = np.argsort(-pv)
    zarr = np.asarray(zeros)
    best = {"f1": 0.0}
    curve = []
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
        curve.append((k, prec, rec, f1))
        if f1 > best["f1"]:
            best = {"f1": f1, "precision": prec, "recall": rec,
                    "n_predictions": k,
                    "threshold": float(pv[order[k - 1]])}
    return {"eps": eps, "n_maxima": int(len(pt)), "best": best,
            "recall_at_full": curve[-1][2] if curve else 0.0}


if __name__ == "__main__":
    zeros_all = json.load(open("../data/riemann/rh_zeros.json"))
    T_LO, T_HI, DT = 10.0, 240.0, 0.005
    T = np.arange(T_LO, T_HI + DT / 2, DT)
    zin = [z for z in zeros_all if T_LO + 1 < z < T_HI - 1]   # ~gamma_1..101
    z31 = zin[:31]
    print(f"grid: {len(T)} pts in [{T_LO},{T_HI}]; zeros in range: {len(zin)}")

    Xdoc = f_encoding_batch(0.5, T)
    Xdet = detector_encoding_batch(0.5, T)

    cS2_doc = c_channel(Xdoc, 2)
    cS2_det = c_channel(Xdet, 2)
    cS6_det = c_channel(Xdet, 6)
    detector = cS2_det + cS6_det
    # exactness check: detector == -2 * sum_p w_p cos(t ln p)
    target = -2.0 * sum(W[p] * np.cos(T * LN[p]) for p in PRIMES)
    exact = float(np.max(np.abs(detector - target)))
    print(f"detector exactness |c_S2+c_S6 - (-2 sum w_p cos)|_max = {exact:.3e}")

    results = {"phase": "77", "question": "Q-17",
               "grid": {"t_lo": T_LO, "t_hi": T_HI, "dt": DT, "n": int(len(T))},
               "zeros_in_range": len(zin),
               "detector_identity_max_abs_residual": exact}

    # ---- 1. scale test ------------------------------------------------------
    print("\n=== 1. SCALE: c_S2 (documented) value-at-zeros ===")
    s31 = t1_value_at_zeros(T, cS2_doc, z31)
    s100 = t1_value_at_zeros(T, cS2_doc, zin)
    d100 = t1_value_at_zeros(T, detector, zin)
    results["scale"] = {"cS2_doc_gamma31": s31, "cS2_doc_gamma100": s100,
                        "detector_gamma100": d100,
                        "sqrtN_prediction_from_31":
                            s31["z"] * math.sqrt(len(zin) / 31)}
    print(f"  c_S2 doc, 31 zeros:  z={s31['z']:.2f}  p={s31['p_two_sided']:.4f}")
    print(f"  c_S2 doc, {len(zin)} zeros: z={s100['z']:.2f}  p={s100['p_two_sided']:.4f}"
          f"   (sqrt-N prediction {s31['z']*math.sqrt(len(zin)/31):.2f})")
    print(f"  detector, {len(zin)} zeros: z={d100['z']:.2f}  p={d100['p_two_sided']:.4f}")

    # ---- 2. ROC -------------------------------------------------------------
    print("\n=== 2. ROC (value-based AUC; positive = within delta of a zero) ===")
    results["roc"] = {}
    for name, Y in (("cS2_documented", cS2_doc), ("detector", detector)):
        results["roc"][name] = [roc_auc(T, Y, zin, d) for d in (0.25, 0.5)]
        for r in results["roc"][name]:
            print(f"  {name:16s} delta={r['delta']:4}: AUC = {r['auc']:.4f}")

    # ---- 3. peak matching ---------------------------------------------------
    print("\n=== 3. PEAK MATCHING (local maxima vs zeros) ===")
    results["peaks"] = {}
    for name, Y in (("cS2_documented", cS2_doc), ("detector", detector)):
        results["peaks"][name] = [peak_matching(T, Y, zin, e) for e in (0.5, 1.0)]
        for r in results["peaks"][name]:
            b = r["best"]
            print(f"  {name:16s} eps={r['eps']:3}: best F1={b['f1']:.3f} "
                  f"(P={b.get('precision',0):.3f} R={b.get('recall',0):.3f} "
                  f"@ {b.get('n_predictions',0)} predictions; "
                  f"{r['n_maxima']} maxima total)")

    results["notes"] = (
        "Detector Encoding deviates from the Phase 76 Documented F(s) Encoding "
        "by design: u_2/u_6 support slots carry w_p cos(t ln p), w_p = "
        "log p/sqrt p; pos2 = 0. The identity c_S2 + c_S6 = -2 sum_p w_p "
        "cos(t ln p) is exact (residual above) and is a direct consequence of "
        "the Gateway Linear Law — a candidate Lean lemma over "
        "GatewayLinearLaw.lean infrastructure (standard axioms). The zero-"
        "detection statistics quantify a 6-prime k=1 explicit-formula "
        "truncation; they are number-theoretic, not instrument, properties.")

    with open("../results/phase77_q17_results.json", "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("\nwrote ../results/phase77_q17_results.json")
