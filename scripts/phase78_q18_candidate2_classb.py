#!/usr/bin/env python3
"""
phase78_q18_candidate2_classb.py -- CAIL-RH Investigation, Phase 78 Q-18
Chavez AI Labs LLC -- Applied Pathological Mathematics

Q-18 Candidate 2: Class B Sign-Structure Hybrid.

detector_hybrid(t; lambda) = c_S2(t) + c_S6(t) + lambda * (c_S1(t) - c_S4(t))

Rationale (per Claude Desktop's follow-up recommendation after Candidate 1's
failure): under the Detector Encoding, c_S1 - c_S4 = -4*w13*cos(t*ln13)
exactly (the shared -2t drift and the w2 term cancel between S1 and S4,
Candidate-1 pre-check). This is NOT new prime information -- p=13 is already
inside c_S2 -- but it lets lambda retune the *relative weight* the detector
gives cos(t*ln13) versus the other five explicit-formula primes, without
reintroducing the t-dominated noise that sank Candidate 1's squared-weight
ensemble. So this candidate really asks: is the standard explicit-formula
weight w_p = log(p)/sqrt(p) optimal for p=13, or does empirically retuning
it (by fitting lambda on a training slice of zeros) improve zero detection?

Protocol: fit lambda by grid search maximizing the T1 (value-at-zeros)
z-score on the first 30 zeros; evaluate that lambda, held out, on the
remaining 71. Compare against the unfitted baseline (c_S2+c_S6) evaluated on
the same held-out 71, which is the fair comparison (one free parameter fit
vs zero free parameters).

Output: ../results/phase78_q18_candidate2_results.json + console summary.
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
    4: (vec((1, 1), (14, -1)), vec((3, 1), (12, -1))),
    6: (vec((2, 1), (13, -1)), vec((6, 1), (9, 1))),
}
U = {g: P + Q for g, (P, Q) in PATTERNS.items()}


def detector_encoding_batch(sigma, T):
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


if __name__ == "__main__":
    zeros_all = json.load(open("../data/riemann/rh_zeros.json"))
    T_LO, T_HI, DT = 10.0, 240.0, 0.005
    T = np.arange(T_LO, T_HI + DT / 2, DT)
    zin = [z for z in zeros_all if T_LO + 1 < z < T_HI - 1]
    print(f"grid: {len(T)} pts in [{T_LO},{T_HI}]; zeros in range: {len(zin)}")

    X = detector_encoding_batch(0.5, T)
    cS1, cS2, cS4, cS6 = c_channel(X, 1), c_channel(X, 2), c_channel(X, 4), c_channel(X, 6)
    base = cS2 + cS6
    s1_minus_s4 = cS1 - cS4

    # sanity: s1_minus_s4 should equal -4*w13*cos(t ln13) exactly
    theory = -4.0 * W[13] * np.cos(T * LN[13])
    resid = float(np.max(np.abs(s1_minus_s4 - theory)))
    print(f"sanity: max|(c_S1-c_S4) - (-4 w13 cos(t ln13))| = {resid:.3e}")

    train, test = zin[:30], zin[30:]
    print(f"train (fit lambda): {len(train)} zeros; test (held out): {len(test)} zeros")

    results = {"phase": "78", "question": "Q-18", "candidate": "2_classb_hybrid",
               "grid": {"t_lo": T_LO, "t_hi": T_HI, "dt": DT, "n": int(len(T))},
               "zeros_in_range": len(zin), "train_n": len(train), "test_n": len(test),
               "s1_minus_s4_identity_residual": resid}

    # ---- grid search lambda on train, maximize T1 z ---------------------------
    lambdas = np.linspace(-3.0, 3.0, 121)  # step 0.05
    train_z = []
    for lam in lambdas:
        Y = base + lam * s1_minus_s4
        train_z.append(t1_value_at_zeros(T, Y, train)["z"])
    train_z = np.array(train_z)
    best_i = int(np.argmax(train_z))
    lam_star = float(lambdas[best_i])
    print(f"\nbest lambda on train: {lam_star:+.2f}  (train z = {train_z[best_i]:.2f}; "
          f"lambda=0 train z = {train_z[len(lambdas)//2]:.2f})")

    hybrid_star = base + lam_star * s1_minus_s4
    d_hybrid_test = t1_value_at_zeros(T, hybrid_star, test)
    d_base_test = t1_value_at_zeros(T, base, test)
    d_hybrid_full = t1_value_at_zeros(T, hybrid_star, zin)
    d_base_full = t1_value_at_zeros(T, base, zin)

    print(f"\nheld-out (test, {len(test)} zeros): hybrid z = {d_hybrid_test['z']:.2f}  "
          f"baseline z = {d_base_test['z']:.2f}")
    print(f"in-sample (full 101, lambda fit on train only, not refit): "
          f"hybrid z = {d_hybrid_full['z']:.2f}  baseline z = {d_base_full['z']:.2f}")

    results["lambda_grid"] = {"lo": -3.0, "hi": 3.0, "n": len(lambdas)}
    results["lambda_star"] = lam_star
    results["train_z_at_lambda_star"] = float(train_z[best_i])
    results["train_z_at_lambda_zero"] = float(train_z[len(lambdas) // 2])
    results["heldout_test"] = {"hybrid": d_hybrid_test, "baseline": d_base_test}
    results["full101_lambda_fixed"] = {"hybrid": d_hybrid_full, "baseline": d_base_full}

    verdict = ("NO IMPROVEMENT: held-out hybrid z (%.2f) does not beat baseline (%.2f)."
               % (d_hybrid_test["z"], d_base_test["z"]))
    if d_hybrid_test["z"] > d_base_test["z"] + 0.01:
        verdict = ("HELD-OUT IMPROVEMENT: hybrid z (%.2f) beats baseline z (%.2f) with "
                   "lambda=%.2f fit on an independent training slice."
                   % (d_hybrid_test["z"], d_base_test["z"], lam_star))
    print(f"\nVERDICT: {verdict}")
    results["verdict"] = verdict

    with open("../results/phase78_q18_candidate2_results.json", "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("\nwrote ../results/phase78_q18_candidate2_results.json")
