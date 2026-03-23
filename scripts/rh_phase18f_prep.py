"""
Phase 18F — 2-Adic Tower: chi8 Companion Test
===============================================
Chavez AI Labs LLC · Applied Pathological Mathematics
Researcher: Paul Chavez
Date: March 23, 2026

Open Science: This script and its results are shared publicly on GitHub.

Background and redesign
-----------------------
Phase 18F was originally designed to test chi16 (conductor 2⁴ = 16) as the next
rung of the 2-adic conductor tower:

  chi4  (conductor 4):  mean Q2 ratio = 0.158  (Phase 18A)
  chi8  (conductor 8):  mean Q2 ratio = 0.298  (Phase 18A)
  chi16 (conductor 16): [planned]

However, THERE ARE NO REAL PRIMITIVE DIRICHLET CHARACTERS OF CONDUCTOR 16.
Proof: (Z/16Z)* ≅ Z/2 × Z/4. Any real (order-2) character chi mod 16 satisfies
chi(9) = chi(3)² = 1 (since chi(3) ∈ {±1}). The kernel of (Z/16Z)* → (Z/8Z)* is
{1, 9}, so chi(9)=1 means chi is induced from mod 8 — conductor divides 8. ∎

The 2-adic tower for REAL primitive characters terminates at chi8. This is a
mathematical theorem, not a computation error.

Redesigned question
-------------------
Since chi16 (real) does not exist, the natural test of "is chi8's Q2 elevation
conductor-specific or character-specific?" becomes:

  Test the chi8 COMPANION: the other real primitive character of conductor 8.

There are exactly two real primitive characters of conductor 8 (both are Kronecker
symbols for fundamental discriminants ±8):
  chi8a = dirichlet_char(8, 5):  chi(3)=-1, chi(5)=-1, chi(7)=+1  [Phase 18A]
  chi8b = dirichlet_char(8, 7):  chi values to be confirmed

If chi8a (Q2 ratio=0.298) AND chi8b show similar Q2 elevation:
  → Q2 elevation is a CONDUCTOR-8 PROPERTY (shared by all real primitive
    characters of conductor 8; structural, not character-specific)

If chi8a elevated but chi8b is not (or vice versa):
  → Q2 elevation is CHARACTER-SPECIFIC (tied to chi8a's chi-values at primes,
    not to conductor 8 as such)

This directly answers the Phase 18F question with a cleaner test than chi16
would have provided, because it isolates conductor vs character-value effects
while remaining within the real primitive character framework.

As a secondary check, the script confirms the tower-termination finding for
the record: all real characters mod 16 have conductor ≤ 8.

Character definitions
---------------------
  chi4  = dirichlet_char(4, 3):  chi(1)=+1, chi(3)=-1              conductor 4
  chi8a = dirichlet_char(8, 5):  chi(1)=+1, chi(3)=-1, chi(5)=-1,
                                  chi(7)=+1                          conductor 8
  chi8b = dirichlet_char(8, 7):  chi values computed below          conductor 8

All three have chi(2) = 0 (p=2 ramified). Route B predicts p=2 suppressed in
all three. The test question is about UNRAMIFIED primes only.

Dependencies: python-flint (v0.8.0), numpy, json
  pip install python-flint numpy
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import math
import os
import time

import flint

script_dir = os.path.dirname(os.path.abspath(__file__))

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]


# ---------------------------------------------------------------------------
# Tower-termination verification
# ---------------------------------------------------------------------------

def verify_no_real_primitive_conductor16():
    """
    Enumerate all characters mod 16 and confirm none are real+primitive+cond16.
    Returns a summary dict for recording.
    """
    summary = {"modulus": 16, "candidates_found": [], "conductor_16_real_primitive": []}
    for a in range(1, 16):
        if math.gcd(a, 16) != 1:
            continue
        try:
            chi = flint.dirichlet_char(16, a)
            cond = int(chi.conductor())
            is_real = bool(chi.is_real())
            is_prim = bool(chi.is_primitive())
            entry = {"conrey_index": a, "conductor": cond,
                     "is_real": is_real, "is_primitive": is_prim}
            summary["candidates_found"].append(entry)
            if is_real and is_prim and cond == 16:
                summary["conductor_16_real_primitive"].append(entry)
        except Exception as e:
            summary["candidates_found"].append({"conrey_index": a, "error": str(e)})
    summary["theorem_confirmed"] = len(summary["conductor_16_real_primitive"]) == 0
    return summary


# ---------------------------------------------------------------------------
# Character property reporting
# ---------------------------------------------------------------------------

def get_chi_at_primes(chi, primes):
    result = {}
    for p in primes:
        v = chi(p)
        r, im = float(v.real), float(v.imag)
        if abs(im) < 1e-9:
            result[p] = round(r)
        else:
            result[p] = complex(r, im)
    return result


def check_character_properties(name, chi):
    cond = int(chi.conductor())
    order = int(chi.order())
    is_real = bool(chi.is_real())
    is_prim = bool(chi.is_primitive())
    vals = get_chi_at_primes(chi, PRIMES)
    ramified = [p for p in PRIMES if vals.get(p) == 0]
    return {
        "name": name,
        "modulus": int(chi.modulus()),
        "conductor": cond,
        "order": order,
        "is_real": is_real,
        "is_primitive": is_prim,
        "chi_at_primes": {str(p): vals[p] for p in PRIMES},
        "ramified_primes_in_survey": ramified,
    }


# ---------------------------------------------------------------------------
# Zero computation (identical pipeline to Phase 18A)
# ---------------------------------------------------------------------------

def hardy_z_real(chi, t):
    z = chi.hardy_z(t)
    return float(z.real)


def find_sign_changes(chi, t_start, t_end, dt=0.25):
    brackets = []
    t = t_start
    z_prev = hardy_z_real(chi, t)
    t_prev = t
    while t + dt <= t_end:
        t += dt
        z_curr = hardy_z_real(chi, t)
        if z_prev * z_curr < 0:
            brackets.append((t_prev, t))
        z_prev = z_curr
        t_prev = t
    return brackets


def bisect_zero(chi, t_lo, t_hi, tol=1e-6):
    z_lo = hardy_z_real(chi, t_lo)
    for _ in range(50):
        t_mid = (t_lo + t_hi) / 2
        if t_hi - t_lo < tol:
            break
        z_mid = hardy_z_real(chi, t_mid)
        if z_lo * z_mid <= 0:
            t_hi = t_mid
        else:
            t_lo = t_mid
            z_lo = z_mid
    return (t_lo + t_hi) / 2


def compute_zeros(chi, name, t_max=2500.0, dt_coarse=0.25, target_n=1500,
                  cache_file=None):
    if cache_file and os.path.exists(cache_file):
        print(f"  Loading {name} zeros from cache: {os.path.basename(cache_file)}")
        with open(cache_file) as f:
            return json.load(f)

    print(f"  Computing {name} zeros to t={t_max:.0f} (dt={dt_coarse})...", flush=True)
    t_start = 1.0
    zeros = []
    t = t_start
    chunk = 100.0
    total_evals = 0
    t0 = time.time()

    while t < t_max and len(zeros) < target_n * 1.2:
        t_chunk_end = min(t + chunk, t_max)
        brackets = find_sign_changes(chi, t, t_chunk_end, dt=dt_coarse)
        total_evals += int((t_chunk_end - t) / dt_coarse) + 1

        for (t_lo, t_hi) in brackets:
            z = bisect_zero(chi, t_lo, t_hi, tol=1e-6)
            zeros.append(z)

        elapsed = time.time() - t0
        print(f"    t={t_chunk_end:.0f}: {len(zeros)} zeros found  "
              f"({total_evals} evals, {elapsed:.1f}s)", flush=True)
        t = t_chunk_end

    zeros.sort()
    zeros = zeros[:target_n] if len(zeros) > target_n else zeros
    print(f"  {name}: {len(zeros)} zeros found, "
          f"range [{zeros[0]:.3f}, {zeros[-1]:.3f}]")

    if cache_file:
        with open(cache_file, 'w') as f:
            json.dump(zeros, f)
        print(f"  Saved to {os.path.basename(cache_file)}")

    return zeros


def gaps_from_zeros(zeros):
    return [zeros[i + 1] - zeros[i] for i in range(len(zeros) - 1)]


# ---------------------------------------------------------------------------
# Log-prime DFT SNR (identical pipeline to Phases 17A/B, 18A)
# ---------------------------------------------------------------------------

def embed_pair(g1, g2):
    s = g1 + g2
    return (g1, g2, g1 - g2, g1 * g2 / s, (g1 + g2) / 2, g1 / s, g2 / s,
            (g1 - g2) ** 2 / s)


Q2 = (0, 0, -1, 0, 0,  1, 0, 0)   # q2 = e6-e3: broadband, 9/9 primes
Q4 = (0, 0,  0, 1, 1,  0, 0, 0)   # q4 = e4+e5: ultra-low-pass
P2 = (0, 0,  0, 1, -1, 0, 0, 0)   # v2 = e4-e5: high-pass (reference)

prime_omegas = {p: math.log(p) for p in PRIMES}
log_vals = sorted(prime_omegas.values())
ctrl_omegas = [(log_vals[i] + log_vals[i + 1]) / 2 for i in range(len(log_vals) - 1)]


def build_sequence(gaps, vec):
    return [
        sum(embed_pair(gaps[i], gaps[i + 1])[k] * vec[k] for k in range(8))
        for i in range(len(gaps) - 1)
    ]


def dft_power(seq, heights, omega):
    mu = sum(seq) / len(seq)
    n = len(seq)
    re = sum((x - mu) * math.cos(omega * t) for x, t in zip(seq, heights)) / n
    im = sum((x - mu) * math.sin(omega * t) for x, t in zip(seq, heights)) / n
    return re ** 2 + im ** 2


def snr_profile(gaps, zeros_list, vec):
    n_pairs = len(gaps) - 1
    seq = build_sequence(gaps, vec)
    hts = [zeros_list[i + 1] for i in range(n_pairs)]
    noise = sum(dft_power(seq, hts, om) for om in ctrl_omegas) / len(ctrl_omegas)
    return (
        {p: dft_power(seq, hts, prime_omegas[p]) / (noise or 1e-300) for p in PRIMES},
        noise,
        len(seq),
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Phase 18F — 2-Adic Tower: chi8 Companion Test")
    print("Chavez AI Labs LLC")
    print("=" * 70)

    results = {
        "experiment": "Phase 18F",
        "date": "2026-03-23",
        "researcher": "Paul Chavez, Chavez AI Labs LLC",
        "question": (
            "Is the chi8 Q2 chi/zeta elevation (0.298) a conductor-8 property "
            "(shared by both real primitive characters of conductor 8), "
            "or is it specific to dirichlet_char(8,5)?"
        ),
        "redesign_reason": (
            "No real primitive Dirichlet characters of conductor 16 exist. "
            "Proof: every real (order-2) character mod 16 satisfies chi(9)=chi(3)^2=1, "
            "so it is induced from mod 8 (kernel of (Z/16Z)*→(Z/8Z)* is {1,9}). "
            "The 2-adic tower for real primitive characters terminates at chi8."
        ),
        "phase18a_prior": {
            "chi4": {"conductor": 4, "mean_Q2_ratio": 0.158},
            "chi8a": {"conductor": 8, "mean_Q2_ratio": 0.298,
                      "conrey_index": 5, "note": "dirichlet_char(8,5)"},
        },
    }

    # --- Tower-termination verification ---
    print("\n[Verifying: no real primitive character of conductor 16]")
    tower_term = verify_no_real_primitive_conductor16()
    print(f"  Characters mod 16 scanned: {len(tower_term['candidates_found'])}")
    print(f"  Real + primitive + conductor=16 found: "
          f"{len(tower_term['conductor_16_real_primitive'])}")
    print(f"  Theorem confirmed: {tower_term['theorem_confirmed']}")
    for entry in tower_term["candidates_found"]:
        if "error" not in entry:
            print(f"    a={entry['conrey_index']:2d}: cond={entry['conductor']:3d}  "
                  f"real={entry['is_real']}  prim={entry['is_primitive']}")
    results["tower_termination_verification"] = tower_term

    # --- Find all real primitive conductor-8 characters ---
    print("\n[Finding real primitive characters of conductor 8]")
    chi8_candidates = []
    for a in range(1, 8):
        if math.gcd(a, 8) != 1:
            continue
        try:
            chi = flint.dirichlet_char(8, a)
            if (bool(chi.is_real()) and bool(chi.is_primitive())
                    and int(chi.conductor()) == 8):
                chi8_candidates.append((a, chi))
                vals = get_chi_at_primes(chi, PRIMES[:5])
                print(f"  dirichlet_char(8, {a}): "
                      f"chi at p=2,3,5,7,11 = {[vals[p] for p in PRIMES[:5]]}")
        except Exception as e:
            print(f"  dirichlet_char(8, {a}): error — {e}")

    if len(chi8_candidates) < 2:
        print(f"  WARNING: expected 2 real primitive characters of conductor 8, "
              f"found {len(chi8_candidates)}")

    # chi8a is the Phase 18A character (Conrey index 5)
    chi8a_index = 5
    chi8a = flint.dirichlet_char(8, chi8a_index)
    # chi8b is the companion: the other conductor-8 real primitive character
    chi8b_candidates = [(a, chi) for a, chi in chi8_candidates if a != chi8a_index]
    if not chi8b_candidates:
        raise RuntimeError("No chi8 companion found — only chi8a (index 5) detected.")
    chi8b_index, chi8b = chi8b_candidates[0]
    print(f"\n  chi8a = dirichlet_char(8, {chi8a_index})  [Phase 18A]")
    print(f"  chi8b = dirichlet_char(8, {chi8b_index})  [companion, this run]")

    # --- Define characters ---
    print("\n[Character definitions: chi4, chi8a, chi8b]")
    chi4  = flint.dirichlet_char(4, 3)

    char_configs = [
        ("chi4",  chi4,  "zeros_chi4_2k.json"),
        ("chi8a", chi8a, "zeros_chi8_phase18a.json"),
        (f"chi8b_{chi8b_index}", chi8b, f"zeros_chi8b_{chi8b_index}_phase18f.json"),
    ]

    char_props = {}
    for name, chi, _ in char_configs:
        props = check_character_properties(name, chi)
        char_props[name] = props
        print(f"  {name}: conductor={props['conductor']}  "
              f"order={props['order']}  "
              f"ramified={props['ramified_primes_in_survey']}")
        print(f"    chi at p=2..23: "
              f"{[props['chi_at_primes'][str(p)] for p in PRIMES]}")
        if not (props["is_real"] and props["is_primitive"] and props["conductor"] in [4, 8]):
            print(f"  WARNING: {name} does not have expected properties!")
    results["character_properties"] = char_props

    # --- Load zeta reference ---
    print("\n[Loading zeta zeros (rh_zeros_10k.json)]")
    with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
        zeta_zeros = json.load(f)
    zeta_gaps = gaps_from_zeros(zeta_zeros)
    print(f"  zeta: {len(zeta_zeros)} zeros, {len(zeta_gaps)} gaps, "
          f"mean gap = {sum(zeta_gaps)/len(zeta_gaps):.4f}")

    # --- Load or compute zeros ---
    print("\n[Loading/computing zeros]")
    zeros_data = {}
    for name, chi, cache_fname in char_configs:
        cache_path = os.path.join(script_dir, cache_fname)
        # chi4: also try Phase 16B file
        if name == "chi4":
            alt_path = os.path.join(script_dir, "zeros_chi4_2k.json")
            if os.path.exists(alt_path):
                with open(alt_path) as f:
                    zeros_data[name] = json.load(f)
                print(f"  {name}: {len(zeros_data[name])} zeros loaded from "
                      f"zeros_chi4_2k.json")
                continue
        zeros_data[name] = compute_zeros(
            chi, name, t_max=2500.0, dt_coarse=0.25, target_n=1500,
            cache_file=cache_path
        )

    # --- Trim to equal N ---
    chi_names = list(zeros_data.keys())
    min_chi_gaps = min(len(zeros_data[n]) - 1 for n in chi_names)
    min_chi_gaps = min(min_chi_gaps, 1500)
    print(f"\n[Using first {min_chi_gaps} gaps per L-function for chi comparisons]")
    print(f"  Zeta uses full {len(zeta_gaps)} gaps as SNR reference")

    gaps_trimmed  = {name: gaps_from_zeros(zeros_data[name])[:min_chi_gaps]
                     for name in chi_names}
    zeros_trimmed = {name: zeros_data[name][:min_chi_gaps + 1]
                     for name in chi_names}

    # --- SNR profiles ---
    print("\n[Computing log-prime DFT SNR profiles]")
    proj_vecs = [("Q2", Q2), ("Q4", Q4), ("P2", P2)]

    snr_zeta_ref = {}
    for proj_name, vec in proj_vecs:
        snr_ref, _, _ = snr_profile(zeta_gaps, zeta_zeros, vec)
        snr_zeta_ref[proj_name] = snr_ref

    snr_results = {}
    for proj_name, vec in proj_vecs:
        snr_results[proj_name] = {}
        snr_results[proj_name]["zeta"] = {str(p): round(snr_zeta_ref[proj_name][p], 2)
                                          for p in PRIMES}
        print(f"\n  --- Projection: {proj_name} ---")
        hdr = " ".join(f"p={p:>2}" for p in PRIMES)
        print(f"  {'L-func':>8}  {hdr}")
        print(f"  {'zeta':>8}: "
              + " ".join(f"{snr_zeta_ref[proj_name][p]:5.0f}" for p in PRIMES)
              + f"  (10k zeros)")

        for name in chi_names:
            g = gaps_trimmed[name]
            z = zeros_trimmed[name]
            snr, noise, n = snr_profile(g, z, vec)
            snr_results[proj_name][name] = {str(p): round(snr[p], 2) for p in PRIMES}
            ramified = char_props.get(name, {}).get("ramified_primes_in_survey", [])
            row = " ".join(
                f"{snr[p]:5.0f}" + ("*" if p in ramified else " ")
                for p in PRIMES
            )
            print(f"  {name:>8}: {row}  (n={n})")

    # --- chi/zeta ratios ---
    print("\n[chi/zeta SNR ratios (zeta reference = 10k)]")
    chi_zeta_ratios = {}
    for proj_name, vec in proj_vecs:
        chi_zeta_ratios[proj_name] = {}
        print(f"\n  Projection: {proj_name}")
        print(f"  {'L-func':>8}  " + "  ".join(f"p={p:>2}" for p in PRIMES))
        print("  " + "-" * 72)
        for name in chi_names:
            ratios = {}
            for p in PRIMES:
                z_snr = snr_zeta_ref[proj_name][p]
                c_snr = snr_results[proj_name][name].get(str(p), 0)
                ratios[p] = c_snr / z_snr if z_snr > 0 else 0
            chi_zeta_ratios[proj_name][name] = {str(p): round(ratios[p], 3) for p in PRIMES}
            ramified = char_props.get(name, {}).get("ramified_primes_in_survey", [])
            ratio_str = "  ".join(
                f"{ratios[p]:5.2f}" + ("*" if p in ramified else " ")
                for p in PRIMES
            )
            print(f"  {name:>8}: {ratio_str}")

    results["snr_profiles"] = snr_results
    results["chi_zeta_ratios"] = chi_zeta_ratios

    # --- Companion test summary ---
    print("\n" + "=" * 70)
    print("COMPANION TEST SUMMARY: Q2 chi/zeta ratios (unramified primes)")
    print("=" * 70)

    companion_summary = {}
    for name in chi_names:
        ramified = char_props.get(name, {}).get("ramified_primes_in_survey", [])
        unram_primes = [p for p in PRIMES if p not in ramified]

        q2_ratios = [chi_zeta_ratios["Q2"][name][str(p)] for p in unram_primes]
        mean_q2 = sum(q2_ratios) / len(q2_ratios) if q2_ratios else 0

        q4_ratios = [chi_zeta_ratios["Q4"][name][str(p)] for p in unram_primes]
        mean_q4 = sum(q4_ratios) / len(q4_ratios) if q4_ratios else 0

        sup_prime = ramified[0] if ramified else None
        sup_q2 = chi_zeta_ratios["Q2"][name].get(str(sup_prime), 0) if sup_prime else 0

        companion_summary[name] = {
            "conductor": char_props[name]["conductor"],
            "conrey_index": char_props[name].get("modulus"),   # placeholder
            "mean_Q2_ratio_unramified": round(mean_q2, 3),
            "mean_Q4_ratio_unramified": round(mean_q4, 3),
            "unramified_primes": unram_primes,
            "Q2_ratios_by_prime": {str(p): chi_zeta_ratios["Q2"][name][str(p)]
                                   for p in unram_primes},
            "suppressed_prime": sup_prime,
            "suppression_Q2_ratio": round(sup_q2, 4),
            "suppression_factor_Q2": round(1 / sup_q2, 0) if sup_q2 > 0 else None,
        }

    print(f"\n  {'L-func':>8}  {'Conductor':>10}  "
          f"{'Mean Q2 ratio':>14}  {'Mean Q4 ratio':>14}  {'p=2 supp (Q2)':>16}")
    print("  " + "-" * 74)

    # Include Phase 18A chi4 reference
    print(f"  {'chi4':>8}  {4:>10}  {0.158:>14.3f}  {'[Phase 18A]':>14}  {'[Phase 18A]':>16}")

    for name in chi_names:
        ts = companion_summary[name]
        if ts["suppression_factor_Q2"]:
            supp_str = (f"{ts['suppression_Q2_ratio']:.4f} "
                        f"({ts['suppression_factor_Q2']:.0f}x)")
        else:
            supp_str = "---"
        print(f"  {name:>8}  {ts['conductor']:>10}  "
              f"{ts['mean_Q2_ratio_unramified']:>14.3f}  "
              f"{ts['mean_Q4_ratio_unramified']:>14.3f}  "
              f"{supp_str:>16}")

    # Companion interpretation
    chi8a_key = "chi8a"
    chi8b_key = f"chi8b_{chi8b_index}"
    chi8a_q2 = companion_summary.get(chi8a_key, {}).get("mean_Q2_ratio_unramified", None)
    chi8b_q2 = companion_summary.get(chi8b_key, {}).get("mean_Q2_ratio_unramified", None)
    chi4_q2  = companion_summary.get("chi4", {}).get("mean_Q2_ratio_unramified", 0.158)

    print(f"\n  chi8a Q2 (Phase 18A): 0.298  [dirichlet_char(8,5)]")
    if chi8a_q2 is not None:
        print(f"  chi8a Q2 (this run):  {chi8a_q2:.3f}  [consistency check]")
    if chi8b_q2 is not None:
        print(f"  chi8b Q2 (this run):  {chi8b_q2:.3f}  [companion, dirichlet_char(8,7)]")

    if chi8a_q2 is not None and chi8b_q2 is not None:
        delta = abs(chi8a_q2 - chi8b_q2)
        chi8_mean = (chi8a_q2 + chi8b_q2) / 2
        if delta < 0.05 and chi8_mean > 0.22:
            conclusion = (
                "CONDUCTOR-8 PROPERTY: Both real primitive characters of conductor 8 "
                f"show elevated Q2 ratios (chi8a={chi8a_q2:.3f}, chi8b={chi8b_q2:.3f}, "
                f"delta={delta:.3f}). The Q2 elevation is a structural property of "
                "conductor 8, not specific to dirichlet_char(8,5). "
                "The 2-adic tower effect is real but terminates at chi8 (no chi16 exists)."
            )
        elif delta >= 0.05:
            conclusion = (
                "CHARACTER-SPECIFIC: The two real primitive characters of conductor 8 "
                f"show different Q2 ratios (chi8a={chi8a_q2:.3f}, chi8b={chi8b_q2:.3f}, "
                f"delta={delta:.3f}). The Q2 elevation is not a conductor-8 property — "
                "it depends on the specific chi-value pattern at primes."
            )
        else:
            conclusion = (
                f"BOTH SUPPRESSED: chi8a={chi8a_q2:.3f}, chi8b={chi8b_q2:.3f}. "
                "Neither companion shows significant Q2 elevation. "
                "The Phase 18A chi8a result (0.298) may need recheck at larger N."
            )
    else:
        conclusion = "Insufficient data for conclusion."

    print(f"\n  Conclusion: {conclusion}")
    companion_summary["conclusion"] = conclusion
    results["companion_summary"] = companion_summary

    # --- Route B verification ---
    print("\n" + "=" * 70)
    print("ROUTE B: p=2 suppression in chi4, chi8a, chi8b")
    print("=" * 70)
    for name in chi_names:
        ts = companion_summary[name]
        if ts["suppression_Q2_ratio"] and ts["suppression_Q2_ratio"] > 0:
            print(f"  {name}: Q2 chi/zeta at p=2 = {ts['suppression_Q2_ratio']:.4f}  "
                  f"({ts['suppression_factor_Q2']:.0f}x suppressed)  ✓")
        else:
            print(f"  {name}: p=2 suppression data unavailable or p=2 not ramified")

    # Save
    out_path = os.path.join(script_dir, "p18f_results.json")
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: p18f_results.json")
    print("Phase 18F complete.")

    return results


if __name__ == "__main__":
    main()
