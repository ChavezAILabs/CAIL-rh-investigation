#!/usr/bin/env python3
"""
phase78_q18_candidate3_higher_primes.py -- CAIL-RH Investigation, Phase 78 Q-18
Chavez AI Labs LLC -- Applied Pathological Mathematics

Q-18 Candidate 3: Higher Prime Truncation (k=1 -> k=2 style extension).

Slot-availability correction vs. the handoff doc: the doc suggested adding
p=17/19 into "unused u_2 slots" {4,7} and p=23 into "unused u_6 slot" 8. But
under the actual Canonical Six support sets, index 7 and 8 are NOT in the
support of ANY of the six gateways (U1..U6) -- a signal placed there is
invisible to every reading, dead weight. Index 4 IS live: it's in U3's
support {4,11,6,9}. Since indices 6,9 (shared with S6) are already occupied
by p=5,7, and index 11 is free, index 4 is the correct place to add a new
prime, and it is read out through gateway S3 -- NOT through S2 or S6, so
this does not disturb the existing detector at all. Concretely:

  c_S3 = -2*(X[4] + X[11] + X[6] + X[9])
       = -2*w17*cos(t ln17) + c_S6      (since X[11]=0, X[6],X[9] shared with S6)

  => detector_extended = c_S2 + c_S3 = c_S2 + c_S6 - 2*w17*cos(t ln17)

which is exactly the natural 7-prime (p=2,3,5,7,11,13,17) explicit-formula
detector, realized via THREE signed gateway readings (S2, S3, S6 -- though
S6 is redundant with S3 here) instead of two. A further prime (p=19) can be
added the same way via index 11 (also in U3's support), yielding an 8-prime
detector via c_S2 + c_S3 alone (no need for S6 at all once both u3 slots are
used):

  c_S3' = -2*(w17*cos(t ln17) + w19*cos(t ln19) + w5*cos(t ln5) + w7*cos(t ln7))

Protocol: quick feasibility check on the first 20 zeros (doc's own bar:
"if z doesn't jump to ~8.5+, stop"); if promising, extend to full 101 and
try adding p=19 too.

Output: ../results/phase78_q18_candidate3_results.json + console summary.
"""
import json
import math

import numpy as np

PRIMES = (2, 3, 5, 7, 11, 13)
NEWPRIMES = (17, 19)
ALLP = PRIMES + NEWPRIMES
LN = {p: math.log(p) for p in ALLP}
W = {p: math.log(p) / math.sqrt(p) for p in ALLP}


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


def base_detector_encoding_batch(sigma, T):
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
    z20 = zin[:20]
    print(f"grid: {len(T)} pts in [{T_LO},{T_HI}]; zeros in range: {len(zin)}; "
          f"quick-check zeros: {len(z20)}")

    results = {"phase": "78", "question": "Q-18", "candidate": "3_higher_primes",
               "grid": {"t_lo": T_LO, "t_hi": T_HI, "dt": DT, "n": int(len(T))},
               "zeros_in_range": len(zin)}

    X = base_detector_encoding_batch(0.5, T)
    cS2, cS3, cS6 = c_channel(X, 2), c_channel(X, 3), c_channel(X, 6)
    base = cS2 + cS6

    # sanity: c_S3 should equal c_S6 - 2*w17*cos(t ln17) once slot 4 carries p=17
    X17 = X.copy()
    X17[:, 4] = W[17] * np.cos(T * LN[17])
    cS3_17 = c_channel(X17, 3)
    theory = cS6 - 2.0 * W[17] * np.cos(T * LN[17])
    resid = float(np.max(np.abs(cS3_17 - theory)))
    print(f"sanity: max|c_S3(with p=17 in slot4) - (c_S6 - 2 w17 cos(t ln17))| = {resid:.3e}")
    results["identity_residual_p17"] = resid

    detector7 = cS2 + cS3_17   # = base - 2*w17*cos(t ln17)

    # ---- quick feasibility check: first 20 zeros ------------------------------
    d_base_20 = t1_value_at_zeros(T, base, z20)
    d_det7_20 = t1_value_at_zeros(T, detector7, z20)
    print(f"\n=== QUICK CHECK (first 20 zeros) ===")
    print(f"  baseline (2,3,5,7,11,13) z = {d_base_20['z']:.2f}")
    print(f"  +p=17 (7 primes)         z = {d_det7_20['z']:.2f}")
    results["quick20"] = {"baseline": d_base_20, "plus_p17": d_det7_20}

    proceed = d_det7_20["z"] > d_base_20["z"] + 0.3  # doc bar: jump toward ~8.5+ on 20 zeros
    print(f"  proceed to full validation? {proceed}  (doc bar: meaningful jump on 20 zeros)")
    results["proceed_to_full"] = bool(proceed)

    if proceed:
        d_base_full = t1_value_at_zeros(T, base, zin)
        d_det7_full = t1_value_at_zeros(T, detector7, zin)
        print(f"\n=== FULL (101 zeros): +p=17 ===")
        print(f"  baseline z = {d_base_full['z']:.2f}   +p17 z = {d_det7_full['z']:.2f}")
        results["full101_plus_p17"] = {"baseline": d_base_full, "plus_p17": d_det7_full}

        # also try p=17 + p=19 together via slot 4 and slot 11
        X1719 = X.copy()
        X1719[:, 4] = W[17] * np.cos(T * LN[17])
        X1719[:, 11] = W[19] * np.cos(T * LN[19])
        cS3_1719 = c_channel(X1719, 3)
        detector8 = cS2 + cS3_1719
        d_det8_full = t1_value_at_zeros(T, detector8, zin)
        print(f"  +p17+p19 (8 primes) z = {d_det8_full['z']:.2f}")
        results["full101_plus_p17_p19"] = {"detector": d_det8_full}
        verdict_z = max(d_det7_full["z"], d_det8_full["z"])
        verdict = ("IMPROVEMENT" if verdict_z > d_base_full["z"] + 0.01 else "NO IMPROVEMENT") + \
                  (": best higher-prime z = %.2f vs baseline z = %.2f"
                   % (verdict_z, d_base_full["z"]))
    else:
        verdict = ("STOPPED AT QUICK CHECK: +p17 on first 20 zeros (z=%.2f) did not clear "
                   "the baseline (z=%.2f) by a meaningful margin; higher primes are not the "
                   "bottleneck per the doc's own stated criterion." % (d_det7_20["z"], d_base_20["z"]))

    print(f"\nVERDICT: {verdict}")
    results["verdict"] = verdict

    with open("../results/phase78_q18_candidate3_results.json", "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("\nwrote ../results/phase78_q18_candidate3_results.json")
