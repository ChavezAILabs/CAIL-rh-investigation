#!/usr/bin/env python3
"""
phase78_q18_runC_high_zeros.py -- CAIL-RH Investigation, Phase 78 Run C + Q-18
Chavez AI Labs LLC -- Applied Pathological Mathematics

Run C (carried over from the July 11, 2026 Phase 78 opening handoff, Sec 4A),
executed together with the Q-18 Candidate 3 result (8-prime k=2 detector,
z=9.84 on gamma_1..101) since Candidate 3 was found "hot":

  Question: does the detector z-score keep growing sub-sqrt(N) beyond
  gamma_101, or plateau -- and does the higher-prime (k=2) extension found in
  Q-18 Candidate 3 hold up at high zeros, or was it a small-N artifact?

Protocol (per the handoff): t in [10, 600], dt = 0.005 (118,001 points);
T1 value-at-zeros with the corrected null (randomize query t-points against
the fixed channel -- the same null already used throughout Q-17/Q-18; the
"fixed minima" correction (AIEX-742) applies to the T2 extremum-proximity
statistic, not used here, so no methodology change needed for T1).

Two detectors, both realized as signed gateway readings (no free parameters,
same construction as Q-17/Q-18 Candidate 3):
  baseline6 = c_S2 + c_S6                    (p in {2,3,5,7,11,13})
  extended8 = c_S2 + c_S3(p17 in slot4, p19 in slot11)
            = baseline6 - 2*w17*cos(t ln17) - 2*w19*cos(t ln19)

Control: the pure explicit-formula scalar (no gateway indirection) at both
prime counts, run over the same range, to separate "does k=2 help" from
"does the gateway architecture dilute at high zero density."

Output: ../results/phase78_q18_runC_results.json + console summary.
"""
import json
import math

import numpy as np

PRIMES6 = (2, 3, 5, 7, 11, 13)
PRIMES8 = PRIMES6 + (17, 19)
LN = {p: math.log(p) for p in PRIMES8}
W = {p: math.log(p) / math.sqrt(p) for p in PRIMES8}


def vec(*pairs, n=16):
    v = np.zeros(n)
    for i, val in pairs:
        v[i] = val
    return v


PATTERNS = {
    2: (vec((3, 1), (12, 1)),  vec((5, 1), (10, 1))),
    3: (vec((4, 1), (11, 1)),  vec((6, 1), (9, 1))),
    6: (vec((2, 1), (13, -1)), vec((6, 1), (9, 1))),
}
U = {g: P + Q for g, (P, Q) in PATTERNS.items()}


def encoding_batch(sigma, T, with_higher_primes):
    X = np.zeros((len(T), 16))
    X[:, 0] = sigma
    X[:, 1] = T
    X[:, 3] = W[2] * np.cos(T * LN[2])
    X[:, 5] = W[3] * np.cos(T * LN[3])
    X[:, 10] = W[11] * np.cos(T * LN[11])
    X[:, 12] = W[13] * np.cos(T * LN[13])
    X[:, 6] = W[5] * np.cos(T * LN[5])
    X[:, 9] = W[7] * np.cos(T * LN[7])
    if with_higher_primes:
        X[:, 4] = W[17] * np.cos(T * LN[17])
        X[:, 11] = W[19] * np.cos(T * LN[19])
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


if __name__ == "__main__":
    zeros_all = json.load(open("../data/riemann/rh_zeros.json"))
    T_LO, T_HI, DT = 10.0, 600.0, 0.005
    T = np.arange(T_LO, T_HI + DT / 2, DT)
    zin = [z for z in zeros_all if T_LO + 1 < z < T_HI - 1]
    print(f"grid: {len(T)} pts in [{T_LO},{T_HI}]; zeros in range: {len(zin)}")

    X6 = encoding_batch(0.5, T, with_higher_primes=False)
    X8 = encoding_batch(0.5, T, with_higher_primes=True)
    base6 = c_channel(X6, 2) + c_channel(X6, 6)
    ext8 = c_channel(X8, 2) + c_channel(X8, 3)   # S3 carries p17,p19 now

    # identity sanity: ext8 == base6 - 2 w17 cos(t ln17) - 2 w19 cos(t ln19)
    theory = base6 - 2.0 * W[17] * np.cos(T * LN[17]) - 2.0 * W[19] * np.cos(T * LN[19])
    resid = float(np.max(np.abs(ext8 - theory)))
    print(f"sanity: max|extended8 - theory| = {resid:.3e}")

    # pure explicit-formula controls (no gateway indirection)
    f6 = -2.0 * sum(W[p] * np.cos(T * LN[p]) for p in PRIMES6)
    f8 = -2.0 * sum(W[p] * np.cos(T * LN[p]) for p in PRIMES8)

    results = {"phase": "78", "question": "RunC+Q18cand3",
               "grid": {"t_lo": T_LO, "t_hi": T_HI, "dt": DT, "n": int(len(T))},
               "zeros_in_range": len(zin), "identity_residual": resid,
               "by_n_zeros": {}}

    checkpoints = [101, 150, 200, len(zin)]
    print(f"\n{'N':>5s} {'gamma_N':>10s} {'base6 z':>9s} {'ext8 z':>9s} "
          f"{'f6ctrl z':>9s} {'f8ctrl z':>9s} {'sqrtN pred (base6)':>20s} {'sqrtN pred (ext8)':>18s}")
    z_at_101 = None
    for n in checkpoints:
        if n > len(zin):
            continue
        sub = zin[:n]
        r = {
            "gamma_n": sub[-1],
            "base6": t1_value_at_zeros(T, base6, sub),
            "ext8": t1_value_at_zeros(T, ext8, sub),
            "f6_control": t1_value_at_zeros(T, f6, sub),
            "f8_control": t1_value_at_zeros(T, f8, sub),
        }
        if n == 101:
            z_at_101 = {"base6": r["base6"]["z"], "ext8": r["ext8"]["z"]}
        pred_base6 = (z_at_101["base6"] * math.sqrt(n / 101)) if z_at_101 else float("nan")
        pred_ext8 = (z_at_101["ext8"] * math.sqrt(n / 101)) if z_at_101 else float("nan")
        r["sqrtN_prediction_base6"] = pred_base6
        r["sqrtN_prediction_ext8"] = pred_ext8
        results["by_n_zeros"][str(n)] = r
        print(f"{n:5d} {sub[-1]:10.2f} {r['base6']['z']:9.2f} {r['ext8']['z']:9.2f} "
              f"{r['f6_control']['z']:9.2f} {r['f8_control']['z']:9.2f} "
              f"{pred_base6:20.2f} {pred_ext8:18.2f}")

    n_max = checkpoints[-1] if checkpoints[-1] <= len(zin) else len(zin)
    r_max = results["by_n_zeros"][str(n_max if n_max in checkpoints else len(zin))]
    growth6 = "GROWTH" if r_max["base6"]["z"] > r_max["sqrtN_prediction_base6"] * 0.9 else \
        ("PLATEAU" if r_max["base6"]["z"] < r_max["sqrtN_prediction_base6"] * 0.6 else "SUB-PREDICTED")
    growth8 = "GROWTH" if r_max["ext8"]["z"] > r_max["sqrtN_prediction_ext8"] * 0.9 else \
        ("PLATEAU" if r_max["ext8"]["z"] < r_max["sqrtN_prediction_ext8"] * 0.6 else "SUB-PREDICTED")
    verdict = (f"At N={len(zin)} zeros (gamma_{len(zin)}={zin[-1]:.2f}): "
               f"base6 z={r_max['base6']['z']:.2f} ({growth6} vs sqrt-N pred "
               f"{r_max['sqrtN_prediction_base6']:.2f}); "
               f"ext8 z={r_max['ext8']['z']:.2f} ({growth8} vs sqrt-N pred "
               f"{r_max['sqrtN_prediction_ext8']:.2f}); "
               f"ext8 vs base6 margin holds: {r_max['ext8']['z'] - r_max['base6']['z']:+.2f}")
    print(f"\nVERDICT: {verdict}")
    results["verdict"] = verdict

    with open("../results/phase78_q18_runC_results.json", "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("\nwrote ../results/phase78_q18_runC_results.json")
