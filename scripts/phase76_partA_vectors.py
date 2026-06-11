#!/usr/bin/env python3
"""
phase76_partA_vectors.py — CAIL-RH Investigation, Phase 76 Part A
Chavez AI Labs LLC — Applied Pathological Mathematics

Generates the 16D F(s) input vectors for all Phase 76 Part A ZDTP runs
(Q-5 pairing collapse probe, Q-6 gamma_4 approach curve, Q-8 B/A extension)
under the Phase 76 Documented Encoding (see RH_PHASE_76_HANDOFF_PART_A.md §4).

Output: phase76_partA_vectors.json — one record per planned zdtp_transmit call.
"""
import json
import math

SQRT2 = math.sqrt(2.0)
PRIMES = [2, 3, 5, 7, 11, 13]


def f_encoding(sigma: float, t: float) -> list:
    """Phase 76 Documented F(s) encoding (deterministic)."""
    v = [0.0] * 16
    v[0] = sigma
    v[1] = t
    v[2] = sigma - 0.5 + 0.0019          # Hamiltonian shift (standing)
    v[3] = math.cos(t * math.log(2))
    v[4] = math.sin(t * math.log(3)) / SQRT2
    v[5] = math.sin(t * math.log(3))
    v[6] = math.cos(t * math.log(5))
    v[7] = math.sin(t * math.log(5)) / SQRT2
    v[8] = math.cos(t * math.log(7))
    v[9] = math.sin(t * math.log(7)) / SQRT2
    v[10] = math.cos(t * math.log(11))
    v[11] = math.sin(t * math.log(11)) / SQRT2
    v[12] = math.cos(t * math.log(13))
    v[13] = math.sin(t * math.log(13)) / SQRT2
    # v[14] = v[15] = 0.0
    return [round(x, 15) for x in v]


GAMMA = {  # Odlyzko, first 26 nontrivial zeros (subset used)
    4: 21.022040,
    21: 79.337375, 22: 82.910381, 23: 84.735493,
    24: 87.425275, 25: 88.809111, 26: 92.491899,
}

runs = []

# Q-5 — pairing collapse probe: sigma x t grid, off-zero t
for sigma in (0.4, 0.5, 0.6):
    for t in (1.0, 10.0):
        runs.append({
            "run_id": f"Q5_s{sigma}_t{t}",
            "question": "Q-5",
            "sigma": sigma, "t": t,
            "vector": f_encoding(sigma, t),
        })

# Q-6 — gamma_4 approach curve on the critical line
for t in (18.0, 19.0, 20.0, 21.0, 21.022040, 22.0):
    runs.append({
        "run_id": f"Q6_t{t}",
        "question": "Q-6",
        "sigma": 0.5, "t": t,
        "vector": f_encoding(0.5, t),
    })

# Q-8 — B/A ratio extension, gamma_21..gamma_26
for n in range(21, 27):
    runs.append({
        "run_id": f"Q8_gamma{n}",
        "question": "Q-8",
        "sigma": 0.5, "t": GAMMA[n], "gamma_index": n,
        "vector": f_encoding(0.5, GAMMA[n]),
    })

if __name__ == "__main__":
    out = {
        "phase": "76A",
        "encoding": "Phase 76 Documented F(s) Encoding (handoff §4)",
        "tool": "CAILculator v2.1.4 / ZDTP v2.0 / profile=RHI / gateway=all",
        "n_runs": len(runs),
        "runs": runs,
    }
    with open("phase76_partA_vectors.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"wrote {len(runs)} run vectors")
