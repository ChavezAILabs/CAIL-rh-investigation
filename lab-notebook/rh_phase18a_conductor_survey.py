"""
Phase 18A — chi3/zeta Q2 Anomaly: Conductor Survey
====================================================
Chavez AI Labs LLC · Applied Pathological Mathematics
Researcher: Paul Chavez
Date: March 13, 2026

Open Science: This script and its results are shared publicly on GitHub.

Background
----------
Phase 17 found an unexpected result for the Q2 projection (q2 = e6-e3, direction
(0,0,-1,0,0,+1,0,0) in 8D E8 space):

  chi3 / zeta SNR ratio (Q2, unramified primes p=5..23): 0.90 - 1.05  (anomalous ≈ 1)
  chi4 / zeta SNR ratio (Q2, unramified primes p=5..23): 0.23          (expected by Route B)

Route B predicts WHICH primes are suppressed (those where chi(p) = 0), but does
NOT predict the chi/zeta SNR ratio for unramified primes. The chi3/Q2 ≈ 1.0 anomaly
is outside Route B's scope.

Candidate: chi3 has conductor 3 (the minimal odd prime). In 8D E8 coordinates,
q2 = (0,0,-1,0,0,+1,0,0) has nonzero components at positions 3 and 6. The
coordinate positions in the E8 embedding may encode the prime 3 directly, giving
chi3 a special relationship with q2.

This phase tests the conductor specificity hypothesis by computing Q2 and Q4
log-prime DFT SNR profiles for L-functions with conductors 5, 7, and 8.

Character definitions (real primitive characters)
--------------------------------------------------
  chi3 = dirichlet_char(3, 2):  chi(1)=+1, chi(2)=-1              conductor 3
  chi4 = dirichlet_char(4, 3):  chi(1)=+1, chi(3)=-1              conductor 4
  chi5 = dirichlet_char(5, 4):  chi(1)=+1, chi(2)=-1, chi(3)=-1, chi(4)=+1  conductor 5
  chi7 = dirichlet_char(7, 6):  chi(1)=+1, chi(2)=+1, chi(3)=-1, chi(4)=+1,
                                 chi(5)=-1, chi(6)=-1              conductor 7
  chi8 = dirichlet_char(8, 5):  chi(1)=+1, chi(3)=-1, chi(5)=-1, chi(7)=+1  conductor 8

Chi values at primes p = 2, 3, 5, 7, 11, 13, 17, 19, 23
---------------------------------------------------------
  prime:  2    3    5    7   11   13   17   19   23
  chi3:  -1    0   -1   +1   -1   +1   +1   -1   +1   (ramified: p=3)
  chi4:   0   -1   +1   -1   -1   +1   +1   -1   -1   (ramified: p=2)
  chi5:  -1   -1    0   -1   +1   -1   -1   +1   -1   (ramified: p=5)
  chi7:  +1   -1   -1    0   +1   -1   -1   +1   +1   (ramified: p=7)
  chi8:   0   -1   -1   +1   -1   +1   -1   -1   +1   (ramified: p=2; note chi8(2)=0)

Route B predictions
-------------------
  Suppressed primes (chi(p) = 0, ramified):
    chi3: p=3 suppressed  (previously confirmed 736x via SR, 6723x via Q2)
    chi4: p=2 suppressed  (previously confirmed 353x via SR, 4652x-10000x via Q2)
    chi5: p=5 should be suppressed (NEW — testing)
    chi7: p=7 should be suppressed (NEW — testing)
    chi8: p=2 should be suppressed (NEW — testing; same ramified prime as chi4)

Anomaly test
------------
  If chi3/Q2 ≈ 1.0 is conductor-specific (conductor 3 special):
    chi5/zeta Q2 ratio should be ≈ 0.23 (like chi4) for unramified primes
    chi7/zeta Q2 ratio should be ≈ 0.23 (like chi4) for unramified primes
    chi8/zeta Q2 ratio should be ≈ 0.23 (like chi4) for unramified primes

  If chi3/Q2 ≈ 1.0 is a general phenomenon (not conductor-specific):
    All L-functions show chi/zeta Q2 ≈ 1.0 for unramified primes

  If the ratio tracks |chi(p)|²:
    chi(p) ∈ {0, ±1} for real characters → ratio is either ≈ 0 (suppressed) or ≈ χ²
    For all real primitive characters, |chi(p)|² = 1 for unramified primes,
    so this would give all chi/zeta ≈ 1.0 — and the chi4 ≈ 0.23 would be the outlier.

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


# ---------------------------------------------------------------------------
# Character definitions
# ---------------------------------------------------------------------------

CHARACTERS = {
    "chi3": flint.dirichlet_char(3, 2),   # conductor 3, p=3 ramified
    "chi4": flint.dirichlet_char(4, 3),   # conductor 4, p=2 ramified
    "chi5": flint.dirichlet_char(5, 4),   # conductor 5, p=5 ramified
    "chi7": flint.dirichlet_char(7, 6),   # conductor 7, p=7 ramified
    "chi8": flint.dirichlet_char(8, 5),   # conductor 8, p=2 ramified
}

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]

# Reference SNR values from Phase 17B (zeta, Q2, Q4)
PHASE17_ZETA_Q2 = {2: 418.7, 3: None, 5: None, 7: None, 11: None, 13: None,
                   17: None, 19: None, 23: None}  # will be recomputed from rh_zeros_10k


def get_chi_at_primes(chi, primes):
    """Return chi(p) for each prime p, as rounded integer (0, ±1) or float for complex."""
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
    """Report basic properties of a character."""
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
# Zero computation via Hardy Z function + sign-change bisection
# ---------------------------------------------------------------------------

def hardy_z_real(chi, t):
    """Return the real value of chi's Hardy Z-function at height t."""
    z = chi.hardy_z(t)
    return float(z.real)


def find_sign_changes(chi, t_start, t_end, dt=0.25):
    """
    Scan [t_start, t_end] with step dt and record (t_lo, t_hi) brackets
    where the Hardy Z-function changes sign. Each bracket contains exactly
    one zero (assuming dt is small enough relative to the zero spacing).
    """
    brackets = []
    t = t_start
    z_prev = hardy_z_real(chi, t)
    t_prev = t

    while t + dt <= t_end:
        t += dt
        z_curr = hardy_z_real(chi, t)
        if z_prev * z_curr < 0:  # sign change
            brackets.append((t_prev, t))
        z_prev = z_curr
        t_prev = t

    return brackets


def bisect_zero(chi, t_lo, t_hi, tol=1e-6):
    """
    Bisection refinement of a zero in [t_lo, t_hi].
    Returns the zero height to tolerance tol.
    """
    z_lo = hardy_z_real(chi, t_lo)
    for _ in range(50):  # max iterations
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
    """
    Compute nontrivial zeros of L(chi, s) on the critical line to t_max.

    Uses coarse grid scan (step dt_coarse) to find sign changes,
    then bisection refinement to 1e-6 precision.

    If cache_file exists, load from cache instead of recomputing.
    """
    if cache_file and os.path.exists(cache_file):
        print(f"  Loading {name} zeros from cache: {cache_file}")
        with open(cache_file) as f:
            return json.load(f)

    print(f"  Computing {name} zeros to t={t_max:.0f} (dt={dt_coarse})...", flush=True)

    # Hardy Z function is not defined at t=0, start from small positive t
    t_start = 1.0

    zeros = []
    t = t_start
    chunk = 100.0  # process in chunks for progress reporting
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
        print(f"  Saved to {cache_file}")

    return zeros


# ---------------------------------------------------------------------------
# Log-prime DFT SNR (identical pipeline to Phases 17A/B)
# ---------------------------------------------------------------------------

def embed_pair(g1, g2):
    """embed_pair(g1, g2): 8D kernel for bilateral zero divisor projection."""
    s = g1 + g2
    return (g1, g2, g1 - g2, g1 * g2 / s, (g1 + g2) / 2, g1 / s, g2 / s,
            (g1 - g2) ** 2 / s)


# Q-vector projections from Phase 17
Q2 = (0, 0, -1, 0, 0,  1, 0, 0)   # q2 = e6-e3: broadband, 9/9 primes
Q4 = (0, 0,  0, 1, 1,  0, 0, 0)   # q4 = e4+e5: ultra-low-pass

# P-vector for reference (Phase 13A/14B)
P2 = (0, 0,  0, 1, -1,  0, 0, 0)  # v2 = e4-e5: high-pass


def build_sequence(gaps, vec):
    """Project gap pairs onto an 8D direction vector via embed_pair."""
    return [
        sum(embed_pair(gaps[i], gaps[i + 1])[k] * vec[k] for k in range(8))
        for i in range(len(gaps) - 1)
    ]


def dft_power(seq, heights, omega):
    """DFT power at angular frequency omega, using zero heights as timestamps."""
    mu = sum(seq) / len(seq)
    n = len(seq)
    re = sum((x - mu) * math.cos(omega * t) for x, t in zip(seq, heights)) / n
    im = sum((x - mu) * math.sin(omega * t) for x, t in zip(seq, heights)) / n
    return re ** 2 + im ** 2


prime_omegas = {p: math.log(p) for p in PRIMES}
log_vals = sorted(prime_omegas.values())
ctrl_omegas = [(log_vals[i] + log_vals[i + 1]) / 2 for i in range(len(log_vals) - 1)]


def snr_profile(gaps, zeros_list, vec):
    """
    Compute SNR at each prime log-frequency for given gap sequence and projection.
    Returns {prime: SNR} dict, noise floor, and n_pairs used.
    """
    n_pairs = len(gaps) - 1
    seq = build_sequence(gaps, vec)
    hts = [zeros_list[i + 1] for i in range(n_pairs)]
    noise = sum(dft_power(seq, hts, om) for om in ctrl_omegas) / len(ctrl_omegas)
    return (
        {p: dft_power(seq, hts, prime_omegas[p]) / (noise or 1e-300) for p in PRIMES},
        noise,
        len(seq),
    )


def gaps_from_zeros(zeros):
    return [zeros[i + 1] - zeros[i] for i in range(len(zeros) - 1)]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Phase 18A — chi3/zeta Q2 Anomaly: Conductor Survey")
    print("Chavez AI Labs LLC")
    print("=" * 70)

    results = {
        "experiment": "Phase 18A",
        "date": "2026-03-13",
        "researcher": "Paul Chavez, Chavez AI Labs LLC",
        "question": (
            "Is the chi3/zeta Q2 ratio ~1.0 (Phase 17) specific to conductor=3, "
            "or general across all small-conductor L-functions?"
        ),
    }

    # --- Character properties ---
    print("\n[Character properties]")
    char_props = {}
    for name, chi in CHARACTERS.items():
        props = check_character_properties(name, chi)
        char_props[name] = props
        print(f"  {name}: conductor={props['conductor']}  order={props['order']}  "
              f"real={props['is_real']}  primitive={props['is_primitive']}")
        print(f"    chi at primes: {props['chi_at_primes']}")
        print(f"    ramified primes in survey: {props['ramified_primes_in_survey']}")
    results["character_properties"] = char_props

    # --- Load existing zeta zeros ---
    print("\n[Loading zeta zeros (rh_zeros_10k.json)]")
    with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
        zeta_zeros = json.load(f)
    zeta_gaps = gaps_from_zeros(zeta_zeros)
    print(f"  zeta: {len(zeta_zeros)} zeros, {len(zeta_gaps)} gaps, "
          f"mean gap = {sum(zeta_gaps)/len(zeta_gaps):.4f}")

    # --- Load or reuse Phase 16B chi3/chi4 zeros ---
    print("\n[Loading chi3/chi4 zeros from Phase 16B]")
    zeros_data = {}
    for name, fname in [("chi3", "zeros_chi3_2k.json"), ("chi4", "zeros_chi4_2k.json")]:
        path = os.path.join(script_dir, fname)
        if os.path.exists(path):
            with open(path) as f:
                zeros_data[name] = json.load(f)
            print(f"  {name}: {len(zeros_data[name])} zeros loaded from {fname}")
        else:
            print(f"  {name}: {fname} not found — will recompute")
            zeros_data[name] = None

    # Recompute chi3/chi4 if cache files are missing
    for name in ["chi3", "chi4"]:
        if zeros_data[name] is None:
            cache = os.path.join(script_dir,
                                 f"zeros_{name}_2k.json" if "2k" in name else
                                 f"zeros_{name}_phase18a.json")
            zeros_data[name] = compute_zeros(
                CHARACTERS[name], name,
                t_max=2500.0, dt_coarse=0.25, target_n=1500,
                cache_file=os.path.join(script_dir, f"zeros_{name}_phase18a.json")
            )

    # --- Compute new zeros: chi5, chi7, chi8 ---
    print("\n[Computing zeros for new L-functions (chi5, chi7, chi8)]")
    for name in ["chi5", "chi7", "chi8"]:
        cache_file = os.path.join(script_dir, f"zeros_{name}_phase18a.json")
        zeros_data[name] = compute_zeros(
            CHARACTERS[name], name,
            t_max=2500.0, dt_coarse=0.25, target_n=1500,
            cache_file=cache_file
        )

    # Build gap sequences for all L-functions
    gaps_data = {name: gaps_from_zeros(z) for name, z in zeros_data.items()}
    gaps_data["zeta"] = zeta_gaps

    # Trim chi-function datasets to 1500 gaps for fair comparison among themselves.
    # Zeta uses the full 10k dataset as the SNR reference denominator (matching Phase 17).
    chi_names = ["chi3", "chi4", "chi5", "chi7", "chi8"]
    min_chi_gaps = min(len(gaps_data[n]) for n in chi_names)
    min_chi_gaps = min(min_chi_gaps, 1500)
    print(f"\n[Using first {min_chi_gaps} gaps for chi-function comparisons]")
    print(f"  Zeta uses full {len(zeta_gaps)} gaps as SNR reference (matching Phase 17)")

    gaps_trimmed = {name: gaps_data[name][:min_chi_gaps] for name in chi_names}
    zeros_trimmed = {name: zeros_data[name][:min_chi_gaps + 1] for name in chi_names}

    # --- Compute SNR profiles for Q2, Q4, P2 ---
    print("\n[Computing log-prime DFT SNR profiles]")
    snr_results = {}
    # Zeta reference SNR: full 10k zeros
    snr_zeta_ref = {}
    for proj_name, vec in [("Q2", Q2), ("Q4", Q4), ("P2", P2)]:
        snr_ref, _, n_ref = snr_profile(zeta_gaps, zeta_zeros, vec)
        snr_zeta_ref[proj_name] = snr_ref
        snr_results.setdefault(proj_name, {})
        snr_results[proj_name]["zeta"] = {str(p): round(snr_ref[p], 2) for p in PRIMES}

    for proj_name, vec in [("Q2", Q2), ("Q4", Q4), ("P2", P2)]:
        print(f"\n  Projection: {proj_name}")
        print(f"    {'zeta (10k)':>10}: " + " ".join(
            f"{snr_zeta_ref[proj_name][p]:6.1f} " for p in PRIMES
        ) + f"  (n={len(zeta_gaps)})")
        for name in chi_names:
            g = gaps_trimmed[name]
            z = zeros_trimmed[name]
            snr, noise, n = snr_profile(g, z, vec)
            snr_results[proj_name][name] = {
                str(p): round(snr[p], 2) for p in PRIMES
            }
            ramified = char_props.get(name, {}).get("ramified_primes_in_survey", [])
            prime_str = " ".join(
                f"{snr[p]:6.1f}" + ("*" if p in ramified else " ")
                for p in PRIMES
            )
            print(f"    {name:>10}: {prime_str}  (n={n})")

    # --- Compute chi/zeta ratios (denominator = full 10k zeta SNR) ---
    print("\n[chi/zeta SNR ratios  (zeta reference = 10k zeros)]")
    chi_zeta_ratios = {}
    for proj_name in ["Q2", "Q4", "P2"]:
        chi_zeta_ratios[proj_name] = {}
        print(f"\n  Projection: {proj_name}")
        print(f"  {'L-func':>8}  " +
              "  ".join(f"p={p:>2}" for p in PRIMES))
        print("  " + "-" * 70)
        for name in chi_names:
            ratios = {}
            for p in PRIMES:
                z_snr = snr_zeta_ref[proj_name][p]
                c_snr = snr_results[proj_name][name].get(str(p), 0)
                ratios[p] = c_snr / z_snr if z_snr > 0 else 0
            chi_zeta_ratios[proj_name][name] = {str(p): round(ratios[p], 3)
                                                for p in PRIMES}
            ramified = char_props.get(name, {}).get("ramified_primes_in_survey", [])
            ratio_str = "  ".join(
                f"{ratios[p]:5.2f}" + ("*" if p in ramified else " ")
                for p in PRIMES
            )
            print(f"  {name:>8}: {ratio_str}")

    # --- Anomaly test: is chi3/Q2 ≈ 1.0 unique? ---
    print("\n" + "=" * 70)
    print("ANOMALY TEST: chi3/Q2 ≈ 1.0 — is it conductor-specific?")
    print("=" * 70)

    anomaly_results = {}
    for name in ["chi3", "chi4", "chi5", "chi7", "chi8"]:
        ramified = char_props.get(name, {}).get("ramified_primes_in_survey", [])
        unramified_ratios = [
            chi_zeta_ratios["Q2"][name][str(p)]
            for p in PRIMES if p not in ramified
        ]
        mean_ratio = sum(unramified_ratios) / len(unramified_ratios) if unramified_ratios else 0
        unramified_primes = [p for p in PRIMES if p not in ramified]

        anomaly_results[name] = {
            "unramified_primes": unramified_primes,
            "Q2_chi_zeta_ratios_unramified": {
                str(p): chi_zeta_ratios["Q2"][name][str(p)]
                for p in unramified_primes
            },
            "mean_Q2_ratio_unramified": round(mean_ratio, 3),
            "shows_anomaly_near_1": bool(0.7 < mean_ratio < 1.3),
            "suppressed_prime": ramified[0] if ramified else None,
            "suppression_ratio": chi_zeta_ratios["Q2"][name].get(
                str(ramified[0]), 0) if ramified else None,
        }

        print(f"\n  {name} (conductor {char_props[name]['conductor']}):")
        print(f"    Mean Q2 chi/zeta (unramified): {mean_ratio:.3f}  "
              f"{'<< ANOMALOUS near 1.0' if 0.7 < mean_ratio < 1.3 else 'normal range ~0.23'}")
        if ramified:
            sup = chi_zeta_ratios["Q2"][name].get(str(ramified[0]), 0)
            print(f"    Suppression at p={ramified[0]}: "
                  f"chi/zeta = {sup:.4f}  "
                  f"({1/sup:.0f}x suppressed)" if sup > 0 else
                  f"    Suppression at p={ramified[0]}: ratio = {sup}")

    results["snr_profiles"] = snr_results
    results["chi_zeta_ratios"] = chi_zeta_ratios
    results["anomaly_test"] = anomaly_results
    results["zero_counts"] = {name: len(zeros_data[name]) for name in zeros_data}

    # --- Summary interpretation ---
    print("\n" + "=" * 70)
    print("PHASE 18A SUMMARY")
    print("=" * 70)

    shows_anomaly = [name for name, r in anomaly_results.items()
                     if r["shows_anomaly_near_1"]]
    does_not = [name for name, r in anomaly_results.items()
                if not r["shows_anomaly_near_1"]]

    print(f"  L-functions with Q2 chi/zeta ≈ 1.0 (anomaly): {shows_anomaly}")
    print(f"  L-functions with Q2 chi/zeta < 0.5 (normal):  {does_not}")

    if set(shows_anomaly) == {"chi3"}:
        interpretation = (
            "CONDUCTOR-SPECIFIC: chi3/Q2 ≈ 1.0 is unique to conductor 3. "
            "The q2 = e6-e3 direction has a special relationship with the prime 3 "
            "in the E8 coordinate system. The nonzero components of q2 are at "
            "positions 3 and 6 — matching the prime 3 in the sedenion basis."
        )
    elif len(shows_anomaly) > 1:
        names_str = ", ".join(shows_anomaly)
        interpretation = (
            f"NOT CONDUCTOR-SPECIFIC: {names_str} all show Q2 chi/zeta ≈ 1.0. "
            "The anomaly is either universal for real primitive characters, "
            "or shared by a broader class than conductor=3 alone."
        )
    else:
        interpretation = (
            "ANOMALY ABSENT: No L-function shows chi/zeta Q2 ≈ 1.0. "
            "The Phase 17 result may have been a statistical fluctuation at N=1893."
        )

    print(f"\n  Interpretation: {interpretation}")
    results["interpretation"] = interpretation

    # Save results
    out_path = os.path.join(script_dir, "p18a_conductor_results.json")
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: p18a_conductor_results.json")

    return results


if __name__ == "__main__":
    main()
