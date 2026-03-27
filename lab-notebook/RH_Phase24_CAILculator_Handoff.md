# Phase 24 CAILculator Handoff
## Chavez AI Labs LLC · March 25, 2026

**Purpose:** Run CAILculator MCP analyses on Phase 24 Thread 1 windowed Weil sequences.
**Source file:** `phase24_thread1_results.json` → key `cailculator_sequences`
**Priority:** Thread 1 sequences only (Thread 2 produced no sequences requiring MCP analysis).

---

## Background

Phase 23T3 found 98.7% conjugation symmetry on the unwindowed residual ratio sequence — the investigation record. Phase 24T1 now has 4 windowed variants of that same sequence (T=50, 100, 200, 500) plus the unwindowed reference recomputed. The key question: does the bilateral symmetry of the Weil angle oscillations change with windowing?

**Thread 1 headline:** The 12% Weil angle is structural (constant for T=100..500). The residual does not converge to 0 with larger T.

---

## Priority Sequences

### Priority 1: Windowed residual ratio comparison

For each T ∈ {50, 100, 200, 500}, analyze `residual_ratio_T{T}_n100` (100 values, N=5..500).
Compare with `residual_ratio_unwindowed_n100`.

**Expected range per sequence:**
- T=50: [0.083, 0.184] — elevated and stabilized early (only 29 effective zeros)
- T=100: [0.065, 0.207]
- T=200: [0.074, 0.219]
- T=500: [0.077, 0.223]
- Unwindowed: [0.078, 0.224]

**What to look for:**
- Does conjugation symmetry stay near 98.7% across all T? (If yes: symmetry is structural)
- Does it drop for small T (T=50) where the sequence saturates early?
- Does the T=100/200/500 unwindowed quartet show nearly identical symmetry? (If yes: windowing has zero effect on the bilateral structure)

### Priority 2: Projection fraction sequences

For T ∈ {50, 100, 200}, analyze `projection_fraction_T{T}_n100` (100 values, N=5..500).
These measure the cosine of S_T(N) with the RHS direction — how tightly aligned the partial sum stays.

**Expected range:**
- T=50: [0.983, 0.997] — high floor (T=50 sum is small and consistently aligned)
- T=100: [0.978, 0.998]
- T=200: [0.976, 0.997]

**What to look for:**
- Conjugation symmetry of the projection fraction itself
- Whether the projection fraction shows the same bilateral symmetry as the residual ratio

### Priority 3: Convergence rate (secondary)

`convergence_rate_T100_n100` — how ‖S_T100(N) - S_T100(500)‖ / ‖S_T100(500)‖ decays with N.
This is a monotone decaying sequence (starts ~0.53, reaches 0 by N=200). Expected Chavez score: ~52-55% (null — monotone like the Phase 23T3 growth sequence).

---

## CAILculator Protocol

For each sequence:
1. Load values from `phase24_thread1_results.json` → `cailculator_sequences` → `{key}`
2. Run `analyze_dataset` with the 100-value sequence
3. Record: conjugation_symmetry, Chavez Transform value, bilateral zeros, mean, std
4. Compare to Phase 23T3 reference (residual ratio unwindowed = 98.7%)

---

## Expected CAILculator Summary Table

| Sequence | Expected score | Interpretation if confirmed |
|---|---|---|
| residual_ratio_unwindowed_n100 | ~98.7% (Phase 23T3 record) | Reference — same sequence recomputed |
| residual_ratio_T500_n100 | ~98.7% (should match unwindowed) | Windowing equivalent at T=500 |
| residual_ratio_T200_n100 | ~97-98% | Mild effect of T=200 window |
| residual_ratio_T100_n100 | ~96-98% | Moderate window effect |
| residual_ratio_T50_n100 | ~85-95% | T=50 uses only 29 zeros; expect lower symmetry |
| projection_fraction_T100_n100 | TBD | Alignment with RHS — new measurement |
| convergence_rate_T100_n100 | ~52-55% | Expected null (monotone decay) |

---

## Update Instructions for Results Files

After CAILculator runs, update `RH_Phase24_Thread1_Results.md` Section 7 with actual scores and add a CAILculator summary section. Update the headline if the symmetry comparison yields a significant new finding.

---

*Handoff prepared March 25, 2026*
*Chavez AI Labs LLC*
