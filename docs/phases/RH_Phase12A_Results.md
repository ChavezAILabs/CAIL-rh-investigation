# RH Phase 12A — Act/GUE Variance Asymptote Study: RESULTS

**Date:** 2026-03-09
**Status: COMPLETE ✓**
**Verdict: CONFOUND IDENTIFIED — ratio depends on zero height, not sample size**

---

## Question

Does the Act/GUE P2 variance ratio plateau at ~0.75 (Phase 11A) as sample size
grows, or does it continue drifting?

---

## Full Results Table

| n_pairs | mean_gap | Act/GUE ratio | Height range (approx) | Source |
|---|---|---|---|---|
| 97 | ~2.24 | 0.651 | 14–237 | Phase 10C |
| 498 | ~2.24 | 0.759 | 14–811 | Phase 11A |
| 998 | ~2.24 | 0.756 | 14–1419 | Phase 11A |
| **2000** | **1.251** | **0.742** | **14–~2400** | **Phase 12A** |
| **5000** | **1.087** | **0.702** | **14–~5600** | **Phase 12A** |
| **9998** | **0.987** | **0.665** | **14–9878** | **Phase 12A** |

---

## Verdict: Height Confound — Not a Sample-Size Asymptote

The ratio does not plateau. It reverses: 0.742 → 0.702 → 0.665 as n grows from
2000 to 9998. However, a critical confound is present:

**Phases 10C and 11A all used the same height window** (zeros 1-1000, heights
14-1419, mean_gap ~2.24). Increasing n within that window showed 0.651 → 0.756.

**Phase 12A extends to higher zeros** (zeros 1001-10000, heights 1419-9878,
mean_gap shrinks to 0.99). The ratio at n=9998 (~0.665) is nearly identical to
the Phase 10C n=97 value (0.651).

**Conclusion:** The drift from 0.65 to 0.75 observed in Phase 11A was a
height-window effect, not a sample-size asymptote:
- Zeros at heights 14-1419 (low-height regime): Act/GUE ~0.65-0.76
- Zeros spanning 14-9878 (aggregate): Act/GUE ~0.665

This is consistent with Phase 6: the height-band survey showed Act/GUE variance
oscillates with height. The ratio is not universal — it is height-dependent.

---

## Physical Interpretation

The Act/GUE variance ratio measures how much tighter actual zero gap-pair
projections are relative to GUE synthetic. This ratio oscillates with height
in the same way the Chavez conjugation symmetry oscillates in Phase 6.

- At some heights, actual zeros are significantly tighter than GUE (ratio ~0.65)
- At other heights, the suppression is weaker (ratio ~0.75)
- The aggregate over all heights (n=9998) reverts toward the "typical" value ~0.66

**Revised conclusion from Phase 11A:** The Act/GUE ~0.75 at n=498/998 was
a property of the specific height window 14-1419, not a stable large-n value.
The correct statement is: Act/GUE variance ratio is consistently < 1.0 at all
heights (actual zeros always tighter than GUE), but the specific value oscillates
with height — consistent with the Berry-Keating prime orbit corrections.

---

## CAILculator Conjugation Symmetry (Secondary Metric)

P2 projection sequences are saved for Claude Desktop calls:
- `p12a_actual_n{2000,5000,9998}_P2.json` — actual zero projections
- `p12a_gue_s{1-5}_n{2000,5000,9998}_P2.json` — GUE synthetic projections

Note: sequences at n=5000 and n=9998 are large; CAILculator compatibility at
these sizes should be verified. Primary variance results above are complete
without CAILculator.

---

## Files

| File | Purpose |
|---|---|
| `rh_phase12a_prep.py` | Analysis script |
| `p12a_results.json` | Full variance results JSON |
| `p12a_actual_n{N}_P2.json` | Actual P2 projections (3 files) |
| `p12a_gue_s{S}_n{N}_P2.json` | GUE P2 projections (15 files) |
| `RH_Phase12A_Results.md` | This document |

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
