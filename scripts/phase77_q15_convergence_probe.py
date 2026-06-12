#!/usr/bin/env python3
"""
phase77_q15_convergence_probe.py — CAIL-RH Investigation, Phase 77 Q-15
Chavez AI Labs LLC — Applied Pathological Mathematics

Q-15: Does the convergence / bilateral-annihilation channel carry a genuine
gamma_n (Riemann zero) signature?

Background: Phase 76 proved the 256D magnitude channel is a smooth closed-form
law of x — its dips are set by prime-log oscillators, not gamma_n (Q-6
resolved negative). This probe targets what the LINEAR law does NOT cover:

  Channel A (control):  conv(t) = 1 - std/mean over the six |M_g|
                        (law-determined; expected NO gamma_n signature)
  Channel B:  r_g(t) = ||(x*P_g)*(Q_g*x)|| / ||x||^2   (sandwich residual,
              bilinear in x — genuinely outside the scalar-contraction law)
  Channel C:  s_g(t) = ||(P_g*x)*(x*Q_g)|| / ||x||^2   (opposite sandwich)

All inputs use the Phase 76 Documented F(s) Encoding on the critical line
(sigma = 1/2). Sedenion products use the Cayley-Dickson structure tensor
(validated against the live CAILculator v2.1.4 server in Phase 76 to 1e-9).

Statistics (per channel, aggregated over gateways and per class):
  T1 value-at-zeros: mean channel value at gamma_1..gamma_29 vs Monte Carlo
     null of 29 uniform t-values (5000 trials, two-sided empirical p).
  T2 extremum proximity: mean distance from each gamma_n to the nearest local
     minimum of the channel vs Monte Carlo null of equally many uniform
     "minima" (2000 trials, one-sided empirical p: closer than chance).

Output: ../results/phase77_q15_results.json + console summary.
"""
import json
import math

import numpy as np

SQRT2 = math.sqrt(2.0)
LN = {p: math.log(p) for p in (2, 3, 5, 7, 11, 13)}


# ------------------------------------------------------------ Cayley-Dickson
def cd_mult(a, b):
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    h = n // 2
    a1, a2 = a[:h], a[h:]
    b1, b2 = b[:h], b[h:]
    conj = lambda v: [v[0]] + [-x for x in v[1:]]
    p1 = [x - y for x, y in zip(cd_mult(a1, b1), cd_mult(conj(b2), a2))]
    p2 = [x + y for x, y in zip(cd_mult(b2, a1), cd_mult(a2, conj(b1)))]
    return p1 + p2


def structure_tensor(n=16):
    """G[i,j,k] with e_i * e_j = sum_k G[i,j,k] e_k."""
    G = np.zeros((n, n, n))
    for i in range(n):
        ei = [0.0] * n
        ei[i] = 1.0
        for j in range(n):
            ej = [0.0] * n
            ej[j] = 1.0
            G[i, j, :] = cd_mult(ei, ej)
    return G


G16 = structure_tensor()


def batch_mul(A, B):
    """Row-wise sedenion product of (N,16) x (N,16) -> (N,16)."""
    return np.einsum("ni,nj,ijk->nk", A, B, G16)


def vec_mul_const(A, c):
    """(N,16) x (16,) -> (N,16): each row times constant sedenion c."""
    return np.einsum("ni,j,ijk->nk", A, c, G16)


def const_mul_vec(c, A):
    return np.einsum("i,nj,ijk->nk", c, A, G16)


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
CLASS_B = (1, 4, 5)
CLASS_A = (2, 3, 6)


def f_encoding_batch(sigma, T):
    """Documented encoding for an array of t values -> (N,16)."""
    N = len(T)
    X = np.zeros((N, 16))
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


def law_convergence_batch(X):
    n2 = np.sum(X * X, axis=1)
    sigma = X[:, 0]
    mags = np.zeros((X.shape[0], 6))
    for g in range(1, 7):
        c = -2.0 * X @ U[g]
        mags[:, g - 1] = np.sqrt(n2 + 4.0 * (c * c + 4.0 * (2.0 * sigma) ** 2))
    mean = mags.mean(axis=1)
    std = mags.std(axis=1)
    return 1.0 - std / mean


def local_minima(T, Y):
    idx = np.where((Y[1:-1] < Y[:-2]) & (Y[1:-1] < Y[2:]))[0] + 1
    return T[idx]


def test_value_at_zeros(T, Y, zeros, n_trials=5000, seed=20260612):
    rng = np.random.default_rng(seed)
    obs = float(np.mean(np.interp(zeros, T, Y)))
    lo, hi = T[0], T[-1]
    null = np.array([
        np.mean(np.interp(rng.uniform(lo, hi, len(zeros)), T, Y))
        for _ in range(n_trials)])
    p_low = float(np.mean(null <= obs))
    p_high = float(np.mean(null >= obs))
    p_two = float(min(1.0, 2 * min(p_low, p_high)))
    z = float((obs - null.mean()) / null.std()) if null.std() > 0 else 0.0
    return {"observed_mean_at_zeros": obs, "null_mean": float(null.mean()),
            "null_std": float(null.std()), "z": z, "p_two_sided": p_two}


def test_extremum_proximity(T, Y, zeros, n_trials=5000, seed=20260613):
    """Null model: hold the channel's minima FIXED (they are quasi-regularly
    spaced by the prime-log oscillators — randomizing them would fake a
    proximity signal), and ask whether the zeros sit closer to those minima
    than equally many uniform random query points do."""
    rng = np.random.default_rng(seed)
    mins = local_minima(T, Y)
    if len(mins) == 0:
        return {"n_minima": 0, "verdict": "no minima"}
    obs = float(np.mean([np.min(np.abs(mins - z)) for z in zeros]))
    lo, hi = T[0], T[-1]
    null = np.array([
        np.mean(np.min(np.abs(mins[None, :]
                              - rng.uniform(lo, hi, len(zeros))[:, None]),
                       axis=1))
        for _ in range(n_trials)])
    z_sc = float((obs - null.mean()) / null.std()) if null.std() > 0 else 0.0
    return {"n_minima": int(len(mins)),
            "observed_mean_dist": obs, "null_mean_dist": float(null.mean()),
            "null_std": float(null.std()), "z": z_sc,
            "p_closer_than_chance": float(np.mean(null <= obs))}


if __name__ == "__main__":
    zeros = json.load(open("../data/riemann/rh_zeros.json"))
    T_LO, T_HI, DT = 10.0, 105.0, 0.005
    T = np.arange(T_LO, T_HI + DT / 2, DT)
    zin = [z for z in zeros if T_LO + 1 < z < T_HI - 1]
    print(f"grid: {len(T)} points in [{T_LO},{T_HI}], zeros in range: {len(zin)}")

    X = f_encoding_batch(0.5, T)
    n2 = np.sum(X * X, axis=1)

    channels = {}
    # Channel A — convergence (law control)
    channels["conv_law_control"] = law_convergence_batch(X)

    # Channels B, C — sandwich residuals per gateway
    rB = {}
    rC = {}
    for g in range(1, 7):
        P, Q = PATTERNS[g]
        xP = vec_mul_const(X, P)        # x * P_g
        Qx = const_mul_vec(Q, X)        # Q_g * x
        Px = const_mul_vec(P, X)        # P_g * x
        xQ = vec_mul_const(X, Q)        # x * Q_g
        rB[g] = np.linalg.norm(batch_mul(xP, Qx), axis=1) / n2
        rC[g] = np.linalg.norm(batch_mul(Px, xQ), axis=1) / n2
    channels["sandwich_B_classA_mean"] = np.mean([rB[g] for g in CLASS_A], axis=0)
    channels["sandwich_B_classB_mean"] = np.mean([rB[g] for g in CLASS_B], axis=0)
    channels["sandwich_B_total"] = np.mean([rB[g] for g in range(1, 7)], axis=0)
    channels["sandwich_C_total"] = np.mean([rC[g] for g in range(1, 7)], axis=0)
    for g in range(1, 7):
        channels[f"sandwich_B_S{g}"] = rB[g]

    # Weighted-encoding variant: scale each prime block by w_p = log p/sqrt p
    # (the explicit-formula weight). Tests whether the INSTRUMENT's own
    # channels recover the gamma_n signature when fed the weighted encoding.
    W = {p: LN[p] / math.sqrt(p) for p in (2, 3, 5, 7, 11, 13)}
    Xw = X.copy()
    Xw[:, 3] *= W[2]
    Xw[:, 4] *= W[3]
    Xw[:, 5] *= W[3]
    Xw[:, 6] *= W[5]
    Xw[:, 7] *= W[5]
    Xw[:, 8] *= W[7]
    Xw[:, 9] *= W[7]
    Xw[:, 10] *= W[11]
    Xw[:, 11] *= W[11]
    Xw[:, 12] *= W[13]
    Xw[:, 13] *= W[13]
    n2w = np.sum(Xw * Xw, axis=1)
    channels["W_conv_law"] = law_convergence_batch(Xw)
    rBw = []
    for g in range(1, 7):
        P, Q = PATTERNS[g]
        rBw.append(np.linalg.norm(
            batch_mul(vec_mul_const(Xw, P), const_mul_vec(Q, Xw)), axis=1) / n2w)
    channels["W_sandwich_B_total"] = np.mean(rBw, axis=0)
    # Class A gateway scalars (bounded oscillators; Class B are t-dominated)
    for g in CLASS_A:
        channels[f"c_S{g}_documented"] = -2.0 * X @ U[g]
        channels[f"c_S{g}_weighted"] = -2.0 * Xw @ U[g]

    # Positive control: explicit-formula-weighted 6-prime scalar.
    # f_pc(t) = -sum_p (log p / sqrt p) cos(t log p) is the theoretically
    # optimal zero detector constructible from the same six prime oscillators
    # (k=1 truncation of the von Mangoldt explicit formula). If even this
    # shows no signature, the Q-15 negative is information-theoretic.
    f_pc = -sum((LN[p] / math.sqrt(p)) * np.cos(T * LN[p])
                for p in (2, 3, 5, 7, 11, 13))
    channels["explicit_formula_control"] = f_pc
    channels["explicit_formula_control_neg"] = -f_pc

    results = {"phase": "77", "question": "Q-15",
               "encoding": "Phase 76 Documented F(s), sigma=1/2",
               "grid": {"t_lo": T_LO, "t_hi": T_HI, "dt": DT, "n": int(len(T))},
               "zeros_in_range": len(zin),
               "channels": {}}

    print(f"\n{'channel':28s} {'T1 z':>7s} {'T1 p':>7s} {'T2 p_close':>10s} {'n_min':>6s}")
    for name, Y in channels.items():
        t1 = test_value_at_zeros(T, Y, zin)
        t2 = test_extremum_proximity(T, Y, zin)
        results["channels"][name] = {"T1_value_at_zeros": t1,
                                     "T2_extremum_proximity": t2}
        print(f"{name:28s} {t1['z']:7.2f} {t1['p_two_sided']:7.4f} "
              f"{t2.get('p_closer_than_chance', float('nan')):10.4f} "
              f"{t2.get('n_minima', 0):6d}")

    # nearest-minimum table for the aggregate nonlinear channel
    mins = local_minima(T, channels["sandwich_B_total"])
    table = [{"gamma_n": i + 1, "gamma": round(z, 6),
              "nearest_min": round(float(mins[np.argmin(np.abs(mins - z))]), 4),
              "dist": round(float(np.min(np.abs(mins - z))), 4)}
             for i, z in enumerate(zin[:10])]
    results["sandwich_B_total_nearest_min_table_first10"] = table

    # interpretive note
    results["interpretation"] = (
        "T1 tests whether the channel takes systematically extreme values AT "
        "the Riemann zeros; T2 tests whether channel minima cluster NEAR the "
        "zeros. conv_law_control is fully determined by the proved linear law "
        "and serves as the no-signal reference. The encoding contains only "
        "six prime oscillators, so any genuine signal is necessarily a "
        "6-prime truncation effect of explicit-formula type.")

    with open("../results/phase77_q15_results.json", "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("\nwrote ../results/phase77_q15_results.json")
    print("\nnearest-minimum table (sandwich_B_total), first 10 zeros:")
    for r in table:
        print(f"  gamma_{r['gamma_n']:>2d} = {r['gamma']:9.4f}  "
              f"nearest min {r['nearest_min']:9.4f}  dist {r['dist']:.4f}")
