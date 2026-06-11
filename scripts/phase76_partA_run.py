#!/usr/bin/env python3
"""
phase76_partA_run.py — CAIL-RH Investigation, Phase 76 Part A execution
Chavez AI Labs LLC — Applied Pathological Mathematics

Executes Q-5 (pairing collapse), Q-6 (gamma_4 approach curve), and Q-8
(B/A asymptote extension) using the validated exact replica of the
CAILculator v2.1.4 ZDTP v2.0 magnitude pipeline.

Replica law (derived Phase 76, validated to 1e-15 against the live server
on 22 gateway readings across sigma in {0, 0.4, 0.6}):

    c_g(x)   = -2 * <x, P_g + Q_g>          (gateway scalar contraction)
    |M_g|^2  = ||x||^2 + 4*(c_g^2 + 4*(2*sigma)^2)
    conv     = 1 - std/mean over the six |M_g|

Server validation points are recorded in phase76_partA_raw.json.
"""
import json
import math

SQRT2 = math.sqrt(2.0)


def vec(*pairs, n=16):
    v = [0.0] * n
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
U = {g: [p + q for p, q in zip(P, Q)] for g, (P, Q) in PATTERNS.items()}
CLASS_B = (1, 4, 5)   # investigation Class B (bilateral-breaking)
CLASS_A = (2, 3, 6)   # investigation Class A (bilateral-preserving)


def f_encoding(sigma, t):
    v = [0.0] * 16
    v[0], v[1], v[2] = sigma, t, sigma - 0.5 + 0.0019
    for k, p in enumerate((2, 3, 5, 7, 11, 13)):
        ang = t * math.log(p)
        if p == 2:
            v[3] = math.cos(ang)
        elif p == 3:
            v[4] = math.sin(ang) / SQRT2
            v[5] = math.sin(ang)
        else:
            base = {5: 6, 7: 8, 11: 10, 13: 12}[p]
            v[base] = math.cos(ang)
            v[base + 1] = math.sin(ang) / SQRT2
    return v


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def magnitudes(sigma, t):
    x = f_encoding(sigma, t)
    n2 = dot(x, x)
    out = {}
    for g in range(1, 7):
        c = -2.0 * dot(x, U[g])
        out[g] = math.sqrt(n2 + 4.0 * (c * c + 4.0 * (2.0 * sigma) ** 2))
    return out


def convergence(m):
    v = list(m.values())
    mean = sum(v) / 6
    std = math.sqrt(sum((a - mean) ** 2 for a in v) / 6)
    return 1.0 - std / mean


GAMMA = [79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
         92.491899, 94.651344, 95.870634, 98.831194, 101.317851]  # g21..g30

results = {"Q5": [], "Q6": [], "Q8": []}

# ---- Q-5: pairing across sigma -------------------------------------------
PAIRS = [(i, j) for i in range(1, 7) for j in range(i + 1, 7)]
for sigma in (0.40, 0.45, 0.49, 0.50, 0.51, 0.55, 0.60):
    for t in (1.0, 10.0):
        m = magnitudes(sigma, t)
        diffs = {f"S{i}-S{j}": m[i] - m[j] for i, j in PAIRS}
        results["Q5"].append({"sigma": sigma, "t": t,
                              "mags": {f"S{g}": m[g] for g in range(1, 7)},
                              "pair_diffs": diffs, "conv": convergence(m)})

# ---- Q-6: gamma_4 approach curve ------------------------------------------
t = 18.0
while t <= 22.0 + 1e-9:
    m = magnitudes(0.5, t)
    results["Q6"].append({"t": round(t, 3),
                          "mags": {f"S{g}": round(m[g], 6) for g in range(1, 7)},
                          "conv": round(convergence(m), 6)})
    t += 0.05
m = magnitudes(0.5, 21.022040)  # exact gamma_4
results["Q6"].append({"t": 21.022040,
                      "mags": {f"S{g}": round(m[g], 6) for g in range(1, 7)},
                      "conv": round(convergence(m), 6)})

# ---- Q-8: B/A ratio g21..g30 ----------------------------------------------
for n, g_t in enumerate(GAMMA, start=21):
    m = magnitudes(0.5, g_t)
    mb = sum(m[g] for g in CLASS_B) / 3
    ma = sum(m[g] for g in CLASS_A) / 3
    results["Q8"].append({"n": n, "gamma": g_t, "B_mean": mb, "A_mean": ma,
                          "BA_ratio": mb / ma,
                          "mags": {f"S{g}": round(m[g], 6) for g in range(1, 7)}})

# analytic asymptote of the B/A ratio under the linear scalar law
results["Q8_asymptote"] = {"value": math.sqrt(17.0),
                           "derivation": "|M_B| ~ sqrt(t^2 + 16 t^2) = sqrt(17) t; "
                                         "|M_A| ~ t; ratio -> sqrt(17) = 4.1231..."}

with open("../results/phase76_partA_results.json", "w") as fh:
    json.dump(results, fh, indent=2)

# ---- console summary -------------------------------------------------------
print("=== Q-5 pair equality scan (|diff| < 1e-9 marked EQ) ===")
for r in results["Q5"]:
    eq = [k for k, v in r["pair_diffs"].items() if abs(v) < 1e-9]
    print(f"  sigma={r['sigma']:.2f} t={r['t']:>4} conv={r['conv']:.4f} EQ pairs: {eq or 'none'}")

print("\n=== Q-5 magnitudes at t=10 ===")
for r in results["Q5"]:
    if r["t"] == 10.0:
        print(f"  sigma={r['sigma']:.2f}: " +
              "  ".join(f"S{g}={r['mags'][f'S{g}']:.4f}" for g in range(1, 7)))

print("\n=== Q-6 per-gateway minima in [18,22] ===")
for g in range(1, 7):
    pts = [(r["t"], r["mags"][f"S{g}"]) for r in results["Q6"]]
    tmin, vmin = min(pts, key=lambda p: p[1])
    print(f"  S{g}: min |M|={vmin:.4f} at t={tmin}   (gamma_4 = 21.02204)")
cv = [(r["t"], r["conv"]) for r in results["Q6"]]
tcv, vcv = min(cv, key=lambda p: p[1])
print(f"  convergence min {vcv:.4f} at t={tcv}")

print("\n=== Q-8 B/A ratio g21..g30 ===")
for r in results["Q8"]:
    print(f"  g{r['n']} (gamma={r['gamma']:9.6f}): B/A = {r['BA_ratio']:.6f}")
print(f"  analytic asymptote sqrt(17) = {math.sqrt(17):.6f}")
