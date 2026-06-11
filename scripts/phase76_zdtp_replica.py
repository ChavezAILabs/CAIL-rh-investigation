#!/usr/bin/env python3
"""
phase76_zdtp_replica.py — CAIL-RH Investigation, Phase 76
Chavez AI Labs LLC — Applied Pathological Mathematics

Derives the gateway scalar-contraction formula of the CAILculator v2.1.4
ZDTP v2.0 lift from observed server states, then replicates magnitude_256d
and convergence locally. Validation target: exact agreement (1e-9) with the
CAILculator server on all observed gateway readings.

Observed structure (from raw zdtp_transmit states, Phase 76 runs R1, R2):
  32D state  = [input_16d | lift_block_16d]
  lift_block = [c_g(x)] at slot 0, plus +/- 2*sigma at the 4 support
               indices of the gateway's P,Q vectors (sign = vector sign)
  256D state = input + 4 copies of lift_block (offsets 16, 32, 64, 128)
  magnitude_256d = sqrt(||x||^2 + 4*(c_g^2 + 4*(2*sigma)^2))
  convergence    = 1 - std/mean over the six gateway magnitudes
The unknown is c_g(x): derived below by hypothesis testing against server data.
"""
import itertools
import math

# ---------------------------------------------------------------- Cayley-Dickson
def cd_mult(a, b):
    """Cayley-Dickson multiplication, recursive, dimension = power of 2."""
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


def basis(i, n=16):
    v = [0.0] * n
    v[i] = 1.0
    return v


def vec(*pairs, n=16):
    v = [0.0] * n
    for idx, val in pairs:
        v[idx] = val
    return v


# Canonical Six patterns (server structural_info, CAILculator v2.1.4)
PATTERNS = {
    1: (vec((1, 1), (14, 1)),  vec((3, 1), (12, 1))),    # S1: (e1+e14)(e3+e12)
    2: (vec((3, 1), (12, 1)),  vec((5, 1), (10, 1))),    # S2: (e3+e12)(e5+e10)
    3: (vec((4, 1), (11, 1)),  vec((6, 1), (9, 1))),     # S3: (e4+e11)(e6+e9)
    4: (vec((1, 1), (14, -1)), vec((3, 1), (12, -1))),   # S4: (e1-e14)(e3-e12)
    5: (vec((1, 1), (14, -1)), vec((5, 1), (10, 1))),    # S5: (e1-e14)(e5+e10)
    6: (vec((2, 1), (13, -1)), vec((6, 1), (9, 1))),     # S6: (e2-e13)(e6+e9)
}

# ------------------------------------------------- observed server data (R1, R2)
X_R1 = [0.4, 1, -0.0981, 0.769238901363972, 0.629680786133636, 0.890503533592275,
        -0.038577106877709, 0.706566865005955, -0.366363725537506, 0.657903983348526,
        -0.736012640726367, 0.478746442882959, -0.838295995494708, 0.385482701514812, 0, 0]
X_R2 = [0.4, 10, -0.0981, 0.797086402186577, -0.707106584485894, -0.999999847465196,
        -0.926263462847407, -0.266472968058111, 0.819906978636232, 0.404789229911839,
        0.40504461571237, -0.646527727332829, 0.869437521797386, 0.349432666609844, 0, 0]

C_R1 = {1: -1.861885811738528, 2: -0.17086759747034397, 3: -3.4555082109748234,
        4: -5.21506979371736, 5: -2.308981785731816, 6: -0.27148834991200993}
C_R2 = {1: -23.333047847967926, 2: -2.143137384462274, 3: 3.750217089508582,
        4: -19.85529776077838, 5: -18.81008953649435, 6: 1.938013799090824}

MAG_R1 = {1: 5.454113717979988, 2: 3.9997080253820636, 3: 7.977658135649975,
          4: 11.165513564463456, 5: 6.099710558068282, 6: 4.021903161613457}


def e0(v):
    return v[0]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def candidates(x, P, Q):
    """Candidate scalar contractions built from sedenion products of x, P, Q."""
    xP, Px = cd_mult(x, P), cd_mult(P, x)
    xQ, Qx = cd_mult(x, Q), cd_mult(Q, x)
    return {
        "e0((xP)Q)": e0(cd_mult(xP, Q)),
        "e0(P(xQ))": e0(cd_mult(P, xQ)),
        "e0((Px)Q)": e0(cd_mult(Px, Q)),
        "e0(P(Qx))": e0(cd_mult(P, cd_mult(Q, x))),
        "e0(Q(xP))": e0(cd_mult(Q, xP)),
        "e0((xQ)P)": e0(cd_mult(xQ, P)),
        "e0((Qx)P)": e0(cd_mult(Qx, P)),
        "e0(x(PQ))": e0(cd_mult(x, cd_mult(P, Q))),   # = 0, control
        "<xP,Q>": dot(xP, Q),
        "<Px,Q>": dot(Px, Q),
        "<xQ,P>": dot(xQ, P),
        "<Qx,P>": dot(Qx, P),
        "<xP,xQ>": dot(xP, xQ),
        "-<x,P><x,Q>": -dot(x, P) * dot(x, Q),
    }


def derive():
    print("Hypothesis testing for c_g(x) against server runs R1, R2:")
    winners = {}
    for g in range(1, 7):
        P, Q = PATTERNS[g]
        c1 = candidates(X_R1, P, Q)
        c2 = candidates(X_R2, P, Q)
        for name in c1:
            if abs(c1[name] - C_R1[g]) < 1e-9 and abs(c2[name] - C_R2[g]) < 1e-9:
                winners.setdefault(g, []).append(name)
    for g in range(1, 7):
        print(f"  S{g}: {winners.get(g, ['NO MATCH'])}")
    return winners


# -------------------------------------------------------- replica (post-derivation)
def gateway_scalar(x, g, formula="e0((xP)Q)"):
    P, Q = PATTERNS[g]
    if formula == "e0((xP)Q)":
        return e0(cd_mult(cd_mult(x, P), Q))
    raise ValueError(formula)


def zdtp_magnitudes(x, formula="e0((xP)Q)"):
    sigma = x[0]
    norm_in_sq = dot(x, x)
    mags = {}
    for g in range(1, 7):
        c = gateway_scalar(x, g, formula)
        mags[g] = math.sqrt(norm_in_sq + 4.0 * (c * c + 4.0 * (2.0 * sigma) ** 2))
    return mags


def convergence(mags):
    vals = list(mags.values())
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    return 1.0 - math.sqrt(var) / mean, mean, math.sqrt(var)


if __name__ == "__main__":
    w = derive()
    if all(w.get(g) for g in range(1, 7)):
        common = set(w[1])
        for g in range(2, 7):
            common &= set(w[g])
        print(f"\nFormulas matching ALL six gateways on both runs: {sorted(common)}")
        # validate magnitudes on R1
        print("\nMagnitude validation vs server (R1):")
        mags = zdtp_magnitudes(X_R1)
        for g in range(1, 7):
            print(f"  S{g}: replica={mags[g]:.12f}  server={MAG_R1[g]:.12f}  "
                  f"delta={abs(mags[g]-MAG_R1[g]):.2e}")
        sc, mean, std = convergence(mags)
        print(f"  convergence replica={sc:.12f}  server=0.6121566050228198")
