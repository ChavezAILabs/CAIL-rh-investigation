#!/usr/bin/env python3
"""
phase77_q14_reconciliation.py — CAIL-RH Investigation, Phase 77 Q-14
Chavez AI Labs LLC — Applied Pathological Mathematics

Q-14: Reconcile the Phase 73-75 baseline encoding constants with the
Phase 76 Documented Encoding, using the Gateway Linear Law (Phase 76):

    c_g(x)   = -2 * <x, P_g + Q_g>
    |M_g|^2  = ||x||^2 + 4*(c_g^2 + 4*(2*sigma)^2)

Sections:
  1. ARCHAEOLOGY  — identify the old "standard prime encoding template"
                    constants (positions 3-13) against cos/sin(gamma_n * ln p)
                    candidate families.
  2. LINEAR LAW   — evaluate the old sigma=0.3/0.5/0.7 baseline vectors under
                    the v2.1.4 law (magnitudes, B/A, pairings, convergence).
  3. PAIRINGS     — explicit functional conditions for |M_i| = |M_j| for all
                    15 gateway pairs; evaluated on the old vector and on the
                    Phase 76 Documented Encoding over a t-grid.
  4. CERTIFICATE  — infeasibility certificate: Phase 75 published magnitudes
                    are unreachable by ANY 16D input under the v2.1.4 law.
  5. COLLAPSE     — c_g(t) closed forms under the documented encoding; the
                    t ~ 18-22 dip mechanism (Class A scalar zero crossings).
  6. RECONCILE    — reproduce the recorded Phase 73 observables (AIEX-584-588,
                    AIEX-621, Q-10) from the law; compare the law's documented-
                    encoding predictions against the Phase 75 Q-4 table.

Provenance of the old vectors: CAILculator_Phase73_Runs_AB.md (May 5, 2026),
Run B input vectors, verbatim. No Phase 73-75 generator script exists in the
repo (newest is phase70_*); the doc is the only source.

Output: ../results/phase77_q14_reconciliation.json + console summary.
"""
import json
import math

SQRT2 = math.sqrt(2.0)
PRIMES = (2, 3, 5, 7, 11, 13)
LN = {p: math.log(p) for p in PRIMES}
GAMMAS = {1: 14.134725, 2: 21.022040, 3: 25.010858, 4: 30.424876}
GAMMA1_4DP = 14.1347  # the 4-dp value actually used in the Phase 73 doc


def vec(*pairs, n=16):
    v = [0.0] * n
    for i, val in pairs:
        v[i] = val
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
U = {g: [p + q for p, q in zip(P, Q)] for g, (P, Q) in PATTERNS.items()}
CLASS_B = (1, 4, 5)
CLASS_A = (2, 3, 6)

# ---- verbatim Phase 73/74 baseline vectors (Run B, gamma_1 = 14.1347) ------
OLD_TEMPLATE = [-0.8651, 0.3546, -0.935, 0.6283, 0.778,
                0.1288, -0.9917, 0.4154, -0.9097, 0.7071, 0.7071]  # pos 3..13


def old_vector(sigma):
    return [sigma, GAMMA1_4DP, sigma + 0.0019] + OLD_TEMPLATE + [0.0, 0.0]


# ---- Phase 76 Documented Encoding ------------------------------------------
def f_encoding(sigma, t):
    v = [0.0] * 16
    v[0], v[1], v[2] = sigma, t, sigma - 0.5 + 0.0019
    v[3] = math.cos(t * LN[2])
    v[4] = math.sin(t * LN[3]) / SQRT2
    v[5] = math.sin(t * LN[3])
    v[6] = math.cos(t * LN[5])
    v[7] = math.sin(t * LN[5]) / SQRT2
    v[8] = math.cos(t * LN[7])
    v[9] = math.sin(t * LN[7]) / SQRT2
    v[10] = math.cos(t * LN[11])
    v[11] = math.sin(t * LN[11]) / SQRT2
    v[12] = math.cos(t * LN[13])
    v[13] = math.sin(t * LN[13]) / SQRT2
    return v


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def law_magnitudes(x):
    sigma = x[0]
    n2 = dot(x, x)
    out = {}
    for g in range(1, 7):
        c = -2.0 * dot(x, U[g])
        out[g] = (c, math.sqrt(n2 + 4.0 * (c * c + 4.0 * (2.0 * sigma) ** 2)))
    return out


def convergence(mags):
    v = [m for _, m in mags.values()]
    mean = sum(v) / 6
    std = math.sqrt(sum((a - mean) ** 2 for a in v) / 6)
    return 1.0 - std / mean


# =========================================================================
# Section 1 — ARCHAEOLOGY: identify the old template constants
# =========================================================================
def archaeology(tol=2.5e-4):
    """Match positions 3..13 of the old template against candidate families.

    Candidates: +/- cos/sin(gamma_n * ln p) for n=1..4, p in PRIMES, each
    also scaled by 1/sqrt(2); plus the constants 1/sqrt(2), 1/2, and the
    documented-encoding values at (sigma=1/2, t=gamma_1).
    Tolerance 2.5e-4 reflects the 4-dp rounding of the recorded vector.
    """
    cands = {}
    for n, gam in GAMMAS.items():
        for p in PRIMES:
            ang = gam * LN[p]
            for fn, fname in ((math.cos, "cos"), (math.sin, "sin")):
                val = fn(ang)
                base = f"{fname}(g{n}*ln{p})"
                cands[base] = val
                cands[f"-{base}"] = -val
                cands[f"{base}/sqrt2"] = val / SQRT2
                cands[f"-{base}/sqrt2"] = -val / SQRT2
    cands["1/sqrt2"] = 1.0 / SQRT2
    cands["1/2"] = 0.5

    report = {}
    for k, target in enumerate(OLD_TEMPLATE, start=3):
        hits = sorted(
            ((name, val, abs(val - target)) for name, val in cands.items()
             if abs(val - target) < tol),
            key=lambda h: h[2])
        report[f"pos{k}"] = {
            "value": target,
            "matches": [{"formula": n, "value": round(v, 6),
                         "residual": round(r, 7)} for n, v, r in hits[:4]],
        }
    return report


# =========================================================================
# Section 3 — PAIRING functional conditions (all 15 pairs)
# =========================================================================
def pairing_conditions(x):
    """|M_i| = |M_j|  <=>  c_i^2 = c_j^2  <=>  <x,u_i-u_j> * <x,u_i+u_j> = 0.

    Returns, per pair, the two linear functionals and their values.
    """
    out = {}
    for i in range(1, 7):
        for j in range(i + 1, 7):
            dm = [a - b for a, b in zip(U[i], U[j])]
            dp = [a + b for a, b in zip(U[i], U[j])]
            out[f"S{i}=S{j}"] = {
                "support_minus": {k: c for k, c in enumerate(dm) if c != 0},
                "support_plus": {k: c for k, c in enumerate(dp) if c != 0},
                "val_minus": dot(x, dm),   # = (c_j - c_i)/2... sign-free test
                "val_plus": dot(x, dp),
                "paired": abs(dot(x, dm) * dot(x, dp)) < 1e-12,
            }
    return out


def pairing_scan_documented(sigma=0.5, t_lo=0.5, t_hi=50.0, n=1981):
    """Which pair conditions vanish identically vs occasionally vs never
    under the documented encoding on the critical line?"""
    stats = {f"S{i}=S{j}": {"max_abs_minus": 0.0, "max_abs_plus": 0.0,
                            "zero_crossings_minus": 0, "zero_crossings_plus": 0}
             for i in range(1, 7) for j in range(i + 1, 7)}
    prev = {}
    for k in range(n):
        t = t_lo + (t_hi - t_lo) * k / (n - 1)
        x = f_encoding(sigma, t)
        for i in range(1, 7):
            for j in range(i + 1, 7):
                key = f"S{i}=S{j}"
                dm = dot(x, [a - b for a, b in zip(U[i], U[j])])
                dp = dot(x, [a + b for a, b in zip(U[i], U[j])])
                s = stats[key]
                s["max_abs_minus"] = max(s["max_abs_minus"], abs(dm))
                s["max_abs_plus"] = max(s["max_abs_plus"], abs(dp))
                if key in prev:
                    if prev[key][0] * dm < 0:
                        s["zero_crossings_minus"] += 1
                    if prev[key][1] * dp < 0:
                        s["zero_crossings_plus"] += 1
                prev[key] = (dm, dp)
    return stats


# =========================================================================
# Section 4 — INFEASIBILITY CERTIFICATE
# =========================================================================
def certificate():
    """Under the v2.1.4 law at sigma = 1/2 (pos0 = sigma):
       |M_g|^2 = ||x||^2 + 4 c_g^2 + 16 (2 sigma)^2 / 4 ... explicitly:
       |M_g|^2 = ||x||^2 + 4 c_g^2 + 16  >=  sigma^2 + 16  =  16.25
       =>  |M_g| >= sqrt(16.25) = 4.0311  for EVERY 16D input with pos0=1/2.

    Phase 75 published magnitudes (RH_Phase75_Runs_Q2_Q4 doc, May 11 2026):
       t = +/-20:  S3 = 2.570, S4 = 2.565, S5 = 2.565, S6 = 2.570
    All four are BELOW the floor => unreachable by any input under v2.1.4.
    Conclusion: the Phase 75 (v2.0.4) magnitude pipeline differed structurally
    from v2.1.4, or its published numbers were post-processed. Cross-phase
    magnitude comparisons (73-75 vs 76+) are formally invalid.
    """
    floor = math.sqrt(0.25 + 16.0)
    phase75_t20 = {"S1": 8.124, "S2": 8.124, "S3": 2.570,
                   "S4": 2.565, "S5": 2.565, "S6": 2.570}
    return {
        "law_floor_sigma_half": floor,
        "phase75_t20_published": phase75_t20,
        "violations": {k: v for k, v in phase75_t20.items() if v < floor},
        "verdict": "Phase 75 magnitudes 2.565-2.570 < 4.0311 floor: "
                   "unreachable under v2.1.4 law. Cross-phase magnitude "
                   "comparability formally refuted.",
    }


# =========================================================================
# Section 5 — c_g(t) closed forms + dip mechanism
# =========================================================================
C_CLOSED_FORMS = {
    "c1": "-2*( t + cos(t ln2) + cos(t ln13) )",
    "c2": "-2*( cos(t ln2) + cos(t ln13) + sin(t ln3) + cos(t ln11) )",
    "c3": "-2*( sin(t ln3)/sqrt2 + sin(t ln11)/sqrt2 + cos(t ln5) + sin(t ln7)/sqrt2 )",
    "c4": "-2*( t + cos(t ln2) - cos(t ln13) )",
    "c5": "-2*( t + sin(t ln3) + cos(t ln11) )",
    "c6": "-2*( (sigma-1/2+0.0019) - sin(t ln13)/sqrt2 + cos(t ln5) + sin(t ln7)/sqrt2 )",
}


def class_a_zero_crossings(sigma=0.5, t_lo=15.0, t_hi=25.0, n=4001):
    """Class A scalars c2, c3, c6 are bounded oscillators in t. Their zero
    crossings are where the corresponding |M_g| dips to its floor
    sqrt(||x||^2 + 16) — the mechanism behind the t ~ 18-22 'collapse'.
    Class B scalars c1, c4, c5 ~ -2t never vanish for t > 2: no dips."""
    crossings = {g: [] for g in range(1, 7)}
    prev = {}
    for k in range(n):
        t = t_lo + (t_hi - t_lo) * k / (n - 1)
        x = f_encoding(sigma, t)
        for g in range(1, 7):
            c = -2.0 * dot(x, U[g])
            if g in prev and prev[g][1] * c < 0:
                t0, c0 = prev[g]
                # linear interpolation for the crossing
                tc = t0 + (t - t0) * (-c0) / (c - c0)
                crossings[g].append(round(tc, 4))
            prev[g] = (t, c)
    return crossings


# =========================================================================
# Section 6 — RECONCILIATION against recorded Phase 73/75 observables
# =========================================================================
def reconcile_phase73():
    """Recorded Phase 73 observables (KSJ AIEX-584-588, AIEX-621; run docs):
       - mean 256D magnitude at gamma_1:  35.38         (AIEX-587)
       - convergence at gamma_1:          0.4274        (AIEX-586)
       - B/A ratio at gamma_1:            3.66          (Phase 73 Run A doc)
       - mean magnitude growth:           mu ~ 2.5*gamma_n   (AIEX-621, Q-9)
       - std/mean invariant:              0.57-0.62     (Q-10)
       - convergence descent:             0.4274 -> 0.3950 (gamma_1..4, AIEX-586)
    All are reproduced/explained by the Gateway Linear Law."""
    x = old_vector(0.5)
    mags = law_magnitudes(x)
    vals = [m for _, m in mags.values()]
    mean = sum(vals) / 6
    std = math.sqrt(sum((a - mean) ** 2 for a in vals) / 6)
    mb = sum(mags[g][1] for g in CLASS_B) / 3
    ma = sum(mags[g][1] for g in CLASS_A) / 3
    s17 = math.sqrt(17.0)
    # law asymptotics for F(s)-type inputs (pos1 = t dominant):
    #   Class B |M| -> sqrt(17) t, Class A |M| -> t
    asym_mean_coeff = (3 * s17 + 3) / 6
    asym_vals = [s17, s17, s17, 1, 1, 1]
    am = sum(asym_vals) / 6
    asym_std_over_mean = math.sqrt(sum((v - am) ** 2 for v in asym_vals) / 6) / am
    return {
        "gamma1_mean_mag": {"law": mean, "recorded_AIEX587": 35.38,
                            "delta": abs(mean - 35.38)},
        "gamma1_convergence": {"law": convergence(mags), "recorded_AIEX586": 0.4274,
                               "delta": abs(convergence(mags) - 0.4274)},
        "gamma1_BA_ratio": {"law": mb / ma, "recorded_run_doc": 3.66,
                            "delta": abs(mb / ma - 3.66)},
        "gamma1_std_over_mean": {"law": std / mean, "recorded_Q10_band": "0.57-0.62"},
        "asymptotic_mean_coeff": {"law": asym_mean_coeff,
                                  "recorded_AIEX621": 2.5,
                                  "note": "(3*sqrt17+3)/6 = 2.5616"},
        "asymptotic_std_over_mean": {"law": asym_std_over_mean,
                                     "recorded_Q10": "~0.57-0.62",
                                     "note": "sqrt(var)/mean of {sqrt17 x3, 1 x3}"},
        "asymptotic_convergence": {"law": 1.0 - asym_std_over_mean,
                                   "recorded_AIEX586_gamma4": 0.3950,
                                   "note": "monotone descent 0.4274->0.3950 is "
                                           "approach to the 0.3904 law asymptote"},
    }


def phase75_comparison():
    """Phase 75 Q-4 published magnitudes (RH_Phase75_Runs_Q2_Q4, May 11 2026)
    vs the law's prediction under the Phase 76 Documented Encoding."""
    published = {
        1.0:  {"S1": 8.220, "S2": 8.220, "S3": 9.586, "S4": 6.408,
               "S5": 6.408, "S6": 9.586, "conv": 0.84},
        20.0: {"S1": 8.124, "S2": 8.124, "S3": 2.570, "S4": 2.565,
               "S5": 2.565, "S6": 2.570, "conv": 0.41},
    }
    out = {}
    for t, pub in published.items():
        x = f_encoding(0.5, t)
        mags = law_magnitudes(x)
        out[f"t_{t}"] = {
            "published_v2.0.4": pub,
            "law_documented_encoding": {f"S{g}": round(mags[g][1], 4)
                                        for g in range(1, 7)},
            "law_convergence": round(convergence(mags), 4),
        }
    return out


# =========================================================================
if __name__ == "__main__":
    results = {"phase": "77", "question": "Q-14",
               "law": "c_g = -2<x,P_g+Q_g>; |M|^2 = ||x||^2 + 4(c^2 + 4(2 sigma)^2)",
               "old_vector_provenance":
                   "CAILculator_Phase73_Runs_AB.md Run B (May 5 2026), verbatim"}

    # -- Section 1
    arch = archaeology()
    results["archaeology"] = arch
    print("=== 1. ARCHAEOLOGY — old template positions 3-13 ===")
    for pos, rec in arch.items():
        m = rec["matches"]
        tag = m[0]["formula"] + f" (res {m[0]['residual']:.1e})" if m else "UNIDENTIFIED"
        print(f"  {pos} = {rec['value']:>8}: {tag}")

    # -- Section 2
    print("\n=== 2. LINEAR LAW on old baseline vectors ===")
    results["old_vectors_under_law"] = {}
    for sigma in (0.3, 0.5, 0.7):
        x = old_vector(sigma)
        mags = law_magnitudes(x)
        mb = sum(mags[g][1] for g in CLASS_B) / 3
        ma = sum(mags[g][1] for g in CLASS_A) / 3
        rec = {"vector": x,
               "c": {f"S{g}": mags[g][0] for g in range(1, 7)},
               "mag": {f"S{g}": mags[g][1] for g in range(1, 7)},
               "B_mean": mb, "A_mean": ma, "BA_ratio": mb / ma,
               "convergence": convergence(mags)}
        results["old_vectors_under_law"][f"sigma_{sigma}"] = rec
        print(f"  sigma={sigma}: " +
              " ".join(f"S{g}={mags[g][1]:.4f}" for g in range(1, 7)) +
              f"  B/A={mb/ma:.4f} conv={convergence(mags):.4f}")

    # -- Section 3
    print("\n=== 3. PAIRING conditions on old sigma=0.5 vector ===")
    pc = pairing_conditions(old_vector(0.5))
    results["pairing_old_vector"] = pc
    for key, rec in pc.items():
        if rec["paired"]:
            print(f"  {key}: PAIRED (minus={rec['val_minus']:.3e}, plus={rec['val_plus']:.3e})")
    paired_any = [k for k, r in pc.items() if r["paired"]]
    if not paired_any:
        print("  -> NO pair condition satisfied: the old template does NOT")
        print("     produce S1=S2 / S3=S6 / S4=S5 under the v2.1.4 law.")
        print("     The Phase 75 sigma=1/2 pairing collapse is a property of the")
        print("     retired v2.0.4 pipeline, not of these inputs under the law.")

    scan = pairing_scan_documented()
    results["pairing_scan_documented_encoding"] = scan
    print("\n  Documented encoding, sigma=1/2, t in [0.5,50] (1981 pts):")
    for key, s in scan.items():
        ident_m = s["max_abs_minus"] < 1e-12
        ident_p = s["max_abs_plus"] < 1e-12
        if ident_m or ident_p:
            print(f"  {key}: IDENTICALLY PAIRED on the line "
                  f"(minus ident={ident_m}, plus ident={ident_p})")
    print("  (non-identical pairs cross zero only at isolated t — counts in JSON)")

    # -- Section 4
    cert = certificate()
    results["infeasibility_certificate"] = cert
    print("\n=== 4. INFEASIBILITY CERTIFICATE ===")
    print(f"  v2.1.4 floor at sigma=1/2: |M| >= {cert['law_floor_sigma_half']:.4f} for ANY input")
    print(f"  Phase 75 published (t=+/-20): {cert['phase75_t20_published']}")
    print(f"  Violations: {sorted(cert['violations'])}")
    print(f"  VERDICT: {cert['verdict']}")

    # -- Section 5
    results["c_closed_forms"] = C_CLOSED_FORMS
    cross = class_a_zero_crossings()
    results["class_scalar_zero_crossings_15_25"] = {f"S{g}": cross[g] for g in range(1, 7)}
    print("\n=== 5. c_g(t) zero crossings, sigma=1/2, t in [15,25] ===")
    for g in range(1, 7):
        cls = "B" if g in CLASS_B else "A"
        print(f"  S{g} (Class {cls}): {cross[g] or 'none (Class B: |c| ~ 2t, no dips)'}")
    print("  Dip mechanism: Class A |M_g| -> sqrt(||x||^2+16) wherever c_g(t)=0;")
    print("  crossings are set by prime-log oscillators, NOT by gamma_n.")

    # -- Section 6
    rec73 = reconcile_phase73()
    results["phase73_reconciliation"] = rec73
    print("\n=== 6. RECONCILIATION vs recorded Phase 73 observables ===")
    for k, r in rec73.items():
        law = r["law"]
        recd = next(v for key, v in r.items() if key.startswith("recorded"))
        delta = f"  delta={r['delta']:.4f}" if "delta" in r else ""
        print(f"  {k}: law={law:.4f}  recorded={recd}{delta}")

    cmp75 = phase75_comparison()
    results["phase75_q4_comparison"] = cmp75
    print("\n  Phase 75 Q-4 published vs law (documented encoding, sigma=1/2):")
    for tkey, r in cmp75.items():
        print(f"  {tkey}: published={r['published_v2.0.4']}")
        print(f"         law      ={r['law_documented_encoding']}"
              f" conv={r['law_convergence']}")

    with open("../results/phase77_q14_reconciliation.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print("\nwrote ../results/phase77_q14_reconciliation.json")
