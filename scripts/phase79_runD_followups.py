#!/usr/bin/env python3
"""
phase79_runD_followups.py -- CAIL-RH Investigation, Phase 79 Run D follow-ups
Chavez AI Labs LLC -- Applied Pathological Mathematics

Two follow-ups requested (Claude Desktop review, 2026-09-11/14) before Run D is
treated as closed, both noted as not-yet-done in RH_PHASE_79_RUND_RESULTS.md:

1. Run D's two control arms (term_count, nonprime) through Channel 2 (model-free
   threshold-crossing), not just Channel 1 (segmented regression). §7 of the
   results doc explicitly flagged this as skipped.
2. A frequency-swap robustness check on the `nonprime` control's surprising
   result (its Channel-1 breakpoint did not move at all when p=13 was replaced
   by q=15, contradicting the prediction that it should move to ~94.2). Is "no
   movement" specific to q=15, or does it hold across a range of substitute
   frequencies? Sweeps q in {12,14,15,16,18,20} in arm C's slot.

Reuses every function from phase79_runD_knee_sweep.py verbatim (grid, zero data,
detector, windowing, Channel 1 segmented fit, Channel 2 threshold-crossing sweep)
-- no reimplementation, same methodology and thresholds as the main run.

Outputs: ../results/phase79_runD_followups.json
"""
import json

import numpy as np

import phase79_runD_knee_sweep as m

if __name__ == "__main__":
    zeros_all = json.load(open("../data/riemann/rh_zeros.json"))
    T_LO, T_HI, DT = 10.0, 600.0, 0.005
    T = np.arange(T_LO, T_HI + DT / 2, DT)
    zin = [z for z in zeros_all if T_LO + 1 < z < T_HI - 1]
    WIDTH, STEP = 20, 5  # matches the chosen width/step from the main Run D sweep
    THRESHOLDS = [0.78, 0.80, 0.82, 0.84, 0.85, 0.86, 0.88, 0.90, 0.92, 0.94]

    out = {"grid": {"t_lo": T_LO, "t_hi": T_HI, "dt": DT}, "width": WIDTH, "step": STEP}

    # ---- 1. Controls through Channel 2 -------------------------------------
    print("=== 1. CONTROLS THROUGH CHANNEL 2 (threshold-crossing sweep) ===")
    controls_ch2 = {}
    for name, spec in m.CONTROLS.items():
        Y = m.explicit_detector(T, spec["freqs"])
        windows = m.measure_arm(T, Y, zin, width=WIDTH, step=STEP)
        gamma_arr = np.array([w["gamma_center"] for w in windows])
        auc_arr = np.array([w["auc_delta0.5"] for w in windows])
        print(f"  control {name} (p_max={spec['p_max']}, predicted knee="
              f"{m.TWO_PI * spec['p_max']:.2f}):")
        by_thresh = {}
        for th in THRESHOLDS:
            point = m.threshold_crossing(gamma_arr, auc_arr, th, 3)
            boot = m.bootstrap_threshold_crossing(gamma_arr, auc_arr, th, n_boot=2000, min_run=3)
            by_thresh[str(th)] = {
                "crossing_point": point,
                "boot_n_success": boot.get("n_success"),
                "boot_ci95": boot.get("ci95"),
            }
            print(f"    thresh={th:.2f}: crossing={point}  "
                  f"boot_n_success={boot.get('n_success')}/2000  ci95={boot.get('ci95')}")
        controls_ch2[name] = {"p_max": spec["p_max"], "predicted_knee": m.TWO_PI * spec["p_max"],
                               "by_threshold": by_thresh}
    out["controls_channel2"] = controls_ch2

    # ---- 2. Frequency-swap robustness on the nonprime control --------------
    print("\n=== 2. FREQUENCY-SWAP ROBUSTNESS (Channel 1, arm-C slot swapped) ===")
    print("  base freqs {2,3,5,7,11}; swapped value in the 6th slot varies:")
    SWAP_VALUES = [12, 13, 14, 15, 16, 18, 20]  # 13 = arm C itself (prime, reference)
    swap_results = {}
    for q in SWAP_VALUES:
        freqs = (2, 3, 5, 7, 11, q)
        Y = m.explicit_detector(T, freqs)
        windows = m.measure_arm(T, Y, zin, width=WIDTH, step=STEP)
        gamma_arr = np.array([w["gamma_center"] for w in windows])
        auc_arr = np.array([w["auc_delta0.5"] for w in windows])
        seg = m.segmented_test(gamma_arr, auc_arr)
        boot = m.bootstrap_breakpoint(gamma_arr, auc_arr, n_boot=2000, n_grid=60)
        bp = seg.get("two_segment", {}).get("breakpoint")
        is_prime = q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
        predicted = m.TWO_PI * q
        swap_results[str(q)] = {
            "freqs": list(freqs), "is_prime": is_prime, "predicted_knee": predicted,
            "fitted_breakpoint": bp, "boot_ci95": boot.get("breakpoint_ci95"),
            "boundary_hit": seg.get("boundary_hit"), "knee_detected": seg.get("knee_detected"),
        }
        tag = "prime, = arm C" if q == 13 else ("prime" if is_prime else "non-prime")
        print(f"  q={q:2d} ({tag:14s}): predicted={predicted:7.2f}  fitted_bp={bp}  "
              f"ci95={boot.get('breakpoint_ci95')}  boundary_hit={seg.get('boundary_hit')}")
    out["frequency_swap_robustness"] = swap_results

    with open("../results/phase79_runD_followups.json", "w") as fh:
        json.dump(out, fh, indent=2, default=float)
    print("\nwrote ../results/phase79_runD_followups.json")
