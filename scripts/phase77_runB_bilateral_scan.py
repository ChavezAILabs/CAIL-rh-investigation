"""
phase77_runB_bilateral_scan.py
Phase 77 Run B: Dense sigma-scan of bilateral magnitude symmetry
Date: June 17, 2026 — Claude Sonnet 4.6

Protocol: Documented F(s) Encoding. For each of 17 sigma values in [0.10, 0.90]
and each of 3 Riemann zeros (gamma1, gamma2, gamma3), compute the ZDTP gateway
magnitudes at t=+gamma and t=-gamma, then take the bilateral difference.

The Gateway Linear Law gives:
  |M_g(sigma, +t)|^2 - |M_g(sigma, -t)|^2 = 4*(c_g(+t)^2 - c_g(-t)^2)
                                            = 16 * a_g * b_g
where a_g = inner(x_even, u_g) and b_g = inner(x_odd, u_g) and x = x_even + x_odd
is the decomposition by even/odd time components.

Key finding: ALL gateways show nonzero bilateral differences at sigma=0.5. The
handoff prediction of zero at sigma=1/2 (citing Q-4) does NOT hold for the
Documented F(s) Encoding — the ZDTP gateway magnitude is NOT time-reversal
symmetric because gateway sums have support on odd-indexed components (t-slot,
sin components). The sedenion NORM ||F(+t)|| = ||F(-t)|| IS symmetric, but
individual gateway magnitudes are not.
"""

import math
import json

SQRT2 = math.sqrt(2.0)
LN = {p: math.log(p) for p in [2, 3, 5, 7, 11, 13]}

GAMMAS = [14.134725141734695, 21.022039638771555, 25.010857580145688]
SIGMAS = [round(0.10 + 0.05 * i, 2) for i in range(17)]

# Gateway pair-sum vectors u_g = P_g + Q_g (Canonical Six, with signs)
# Format: [(position, sign), ...]
GATEWAY_SUMS = {
    1: [(1, 1), (14, 1), (3, 1), (12, 1)],   # S1: e1+e14+e3+e12
    2: [(3, 1), (12, 1), (5, 1), (10, 1)],   # S2: e3+e12+e5+e10
    3: [(4, 1), (11, 1), (6, 1), (9, 1)],    # S3: e4+e11+e6+e9
    4: [(1, 1), (14, -1), (3, 1), (12, -1)], # S4: e1-e14+e3-e12
    5: [(1, 1), (14, -1), (5, 1), (10, 1)],  # S5: e1-e14+e5+e10
    6: [(2, 1), (13, -1), (6, 1), (9, 1)],   # S6: e2-e13+e6+e9
}


def f_encoding(sigma: float, t: float) -> list:
    """Documented F(s) Encoding — Phase 76 standard (reproducibility baseline).
    pos2 = sigma - 0.5 + 0.0019 is the Hamiltonian shift; load-bearing."""
    v = [0.0] * 16
    v[0] = sigma
    v[1] = t
    v[2] = sigma - 0.5 + 0.0019
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


def gateway_scalar(x: list, g: int) -> float:
    """c_g = -2 * inner(x, u_g) (Gateway Linear Law, proved GatewayLinearLaw.lean)."""
    return -2.0 * sum(sign * x[pos] for pos, sign in GATEWAY_SUMS[g])


def gateway_magnitude(x: list, g: int) -> float:
    """ZDTP 256D gateway magnitude: |M_g|^2 = ||x||^2 + 4*(c_g^2 + 4*(2*sigma)^2)."""
    sigma = x[0]
    c = gateway_scalar(x, g)
    norm_sq = sum(xi * xi for xi in x)
    return math.sqrt(norm_sq + 4.0 * (c * c + 4.0 * (2.0 * sigma) ** 2))


def run_scan():
    results = {}
    for gidx, gamma in enumerate(GAMMAS, 1):
        rows = []
        for sigma in SIGMAS:
            xp = f_encoding(sigma, +gamma)
            xm = f_encoding(sigma, -gamma)
            row = {
                "sigma": sigma,
                "norm_sq": sum(xi * xi for xi in xp),  # == norm_sq(xm) by symmetry
                "mags_pos": {},
                "mags_neg": {},
                "bilateral_diff": {},
                "cvals_pos": {},
                "cvals_neg": {},
            }
            for g in range(1, 7):
                mp = gateway_magnitude(xp, g)
                mm = gateway_magnitude(xm, g)
                row["mags_pos"][g] = mp
                row["mags_neg"][g] = mm
                row["bilateral_diff"][g] = mp - mm
                row["cvals_pos"][g] = gateway_scalar(xp, g)
                row["cvals_neg"][g] = gateway_scalar(xm, g)
            rows.append(row)
        results[gidx] = {"gamma": gamma, "rows": rows}
    return results


def print_tables(results):
    for gidx in [1, 2, 3]:
        gamma = results[gidx]["gamma"]
        print(f"=== RUN B-{gidx}: gamma{gidx} = {gamma:.15g} ===")
        print("sigma  |   S1        S2        S3        S4        S5        S6")
        print("-" * 75)
        for row in results[gidx]["rows"]:
            s = row["sigma"]
            d = row["bilateral_diff"]
            print(
                f'{s:.2f}  | {d[1]:+8.4f}  {d[2]:+8.4f}  {d[3]:+8.4f}'
                f'  {d[4]:+8.4f}  {d[5]:+8.4f}  {d[6]:+8.4f}'
            )
        print()

    print("=== BILATERAL DIFF AT sigma=0.50 ACROSS GAMMAS ===")
    print("Gateway |  gamma1       gamma2       gamma3")
    print("-" * 52)
    GW = {1: "S1", 2: "S2", 3: "S3", 4: "S4", 5: "S5", 6: "S6"}
    for g in range(1, 7):
        vals = [
            next(r["bilateral_diff"][g] for r in results[gi]["rows"]
                 if abs(r["sigma"] - 0.5) < 0.001)
            for gi in [1, 2, 3]
        ]
        print(f"  {GW[g]:<4}  |  {vals[0]:+9.4f}   {vals[1]:+9.4f}   {vals[2]:+9.4f}")

    print()
    print("=== S6 SLOPE per unit sigma ===")
    for gidx in [1, 2, 3]:
        rows = results[gidx]["rows"]
        s6 = [r["bilateral_diff"][6] for r in rows]
        sigs = [r["sigma"] for r in rows]
        slope = (s6[-1] - s6[0]) / (sigs[-1] - sigs[0])
        print(f"  gamma{gidx}: slope = {slope:.6f}")

    print()
    print("=== NORM SYMMETRY VERIFICATION ===")
    for gidx in [1, 2, 3]:
        gamma = results[gidx]["gamma"]
        # Recompute to verify ||x(+t)||^2 == ||x(-t)||^2
        xp = f_encoding(0.5, +gamma)
        xm = f_encoding(0.5, -gamma)
        ns_p = sum(xi * xi for xi in xp)
        ns_m = sum(xi * xi for xi in xm)
        print(f"  gamma{gidx}: ||x(+t)||^2 = {ns_p:.15g}, ||x(-t)||^2 = {ns_m:.15g}, diff = {abs(ns_p-ns_m):.2e}")


if __name__ == "__main__":
    print("Phase 77 Run B — Bilateral Magnitude Sigma-Scan")
    print("Date: 2026-06-17  |  Encoding: Documented F(s)  |  Method: Gateway Linear Law (analytical)")
    print()
    results = run_scan()
    print_tables(results)

    out_path = (
        r"C:\dev\projects\Experiments_January_2026\Primes_2026"
        r"\CAIL-rh-investigation\results\phase77_runB_results.json"
    )
    serializable = {
        str(gi): {
            "gamma": results[gi]["gamma"],
            "rows": [
                {**row, "mags_pos": {str(k): v for k, v in row["mags_pos"].items()},
                 "mags_neg": {str(k): v for k, v in row["mags_neg"].items()},
                 "bilateral_diff": {str(k): v for k, v in row["bilateral_diff"].items()},
                 "cvals_pos": {str(k): v for k, v in row["cvals_pos"].items()},
                 "cvals_neg": {str(k): v for k, v in row["cvals_neg"].items()}}
                for row in results[gi]["rows"]
            ]
        }
        for gi in [1, 2, 3]
    }
    with open(out_path, "w") as f:
        json.dump({"run": "B", "date": "2026-06-17", "encoding": "DocumentedF(s)", "data": serializable}, f, indent=2)
    print(f"Results saved: {out_path}")
