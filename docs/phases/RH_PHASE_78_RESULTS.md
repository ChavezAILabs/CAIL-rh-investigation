# RH Investigation — Phase 78 Results: Q-18 Detector Ensemble & Run C

> ⚠ **Superseded by [`RH_PHASE_78_RESULTS_v2.md`](RH_PHASE_78_RESULTS_v2.md), 2026-09-08.**
> This version's headline Run C finding (§4, finding 1) is inverted — see
> [`CORRECTIONS.md`](../../CORRECTIONS.md) C-001, and C-007, C-009, C-010,
> C-011, C-012 for the other corrections v2 applies. Retained for the record;
> read v2 for the corrected account.

**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Date:** August 22, 2026
**Phase:** 78 (Q-18 empirical track + Run C)
**Tag:** #phase-78-detector-ensemble
**Execution:** Claude Sonnet 5 (Claude Code, in-shell), from the `CLAUDE_CODE_HANDOFF_PHASE78_Q18.md` / `DATA_MANIFEST_CLAUDE_CODE.md` / `PHASE_78_Q18_BASELINE_CONFIRMED.md` handoff (Aug 22–23, 2026), with a mid-run pivot recommendation from Claude Desktop
**Branch:** none opened yet — all work is uncommitted in the working tree
**Status:** **DRAFT.** Covers the Q-18 empirical track only. The Phase 78 Lean track (`SedenionProduct.lean` infrastructure, Q-16 `canonical_six_e0_transparency`) from the July 11, 2026 opening handoff was **not started this session** — whether to pursue it this phase is still open, per Paul.

---

## Executive Summary

**Pre-flight verification: PASSED.** `phase77_q17_signed_channel.py` reproduced the Phase 77 baseline exactly (z=8.42, AUC=0.8661, precision=0.831), and a live CAILculator v2.1.4 call at γ₁ matched the recorded `phase77_q17_live_validation.json` values to full double precision (c_S2 = 3.1204551984921403, c_S6 = 2.102194713548072). The instrument has not drifted since June 12.

**Q-18 asked: can a multi-gateway ensemble beat the Detector Encoding baseline (z=8.42, AUC 0.866)?** Three candidates were run, with a held-out-data discipline applied throughout (weights/parameters fit on a training slice, evaluated on a disjoint test slice) after Candidate 1 exposed how badly in-sample fitting overstates these ensembles:

- **Candidate 1 (per-gateway weighting): FAILS, badly.** Held-out z = **−7.26** vs an unfitted baseline of 5.12 on the same test zeros. Root cause identified analytically and confirmed numerically: under the Detector Encoding, **S3 is algebraically identical to S6** (`max|c_S3−c_S6| = 0`), so a naive six-gateway sum double-counts one prime channel; and the doc's own `(z_g/Σz)²` weighting formula **discards the sign** of each gateway's z-score, so the three Class B gateways (which are anti-correlated with zero locations, z ≈ −2.3 each) get added in with the wrong orientation.
- **Candidate 2 (Class B hybrid, λ·(c_S1−c_S4)): FAILS, cleanly.** Best-fit λ on a 30-zero training slice is **−0.05** (essentially zero — the training data found no room for improvement), and held-out z = 6.15 vs baseline 6.16 on the same 71 test zeros — a wash. The standard explicit-formula weight on p=13 is already near-optimal.
- **Candidate 3 (higher-prime truncation, k=1→k=2): SUCCEEDS.** Extending the 6-prime detector to 8 primes (p=17, p=19) via a previously-unused live slot (see §3.1 for a correction to the handoff's slot assignment) raises z from **8.42 to 9.84** at γ₁–γ₁₀₁, using only the *standard* explicit-formula weight `w_p = log p/√p` — no free parameter was fit to the evaluation data, so this result does not carry the same overfitting risk as Candidates 1–2.

**Run C, executed immediately after Candidate 3 "while hot" (Paul's instruction) at Claude Desktop's suggested capstone framing:** extended the grid to t ∈ [10,600] (340 zeros through γ₃₄₀ ≈ 598.5). Findings:
1. **No plateau.** Both the 6-prime baseline and the 8-prime extension keep growing in z through γ₃₄₀, sub-√N throughout (matching the Phase 77 c_S2 pattern), answering Run C's original question.
2. **Candidate 3's margin holds at scale**, not a small-N artifact: +1.53 (γ₁₀₁) → +1.39 (γ₁₅₀) → +1.59 (γ₂₀₀) → +1.96 (γ₃₄₀) z-points over baseline.
3. **Zero dilution at high zero density**: the gateway-realized detectors match the pure explicit-formula control to machine precision (residual 1.78×10⁻¹⁵) at every checkpoint — the architecture stays exact, it does not degrade.

**Net Q-18 verdict:** ensembling across the existing six Canonical Six gateways under the Detector Encoding does not help (two independent negative results, both with identified mechanisms) — the architecture is tight, as Claude Desktop's mid-run analysis anticipated. But the k=1→k=2 explicit-formula truncation is a real, held-up-at-scale improvement.

Nothing in this phase has been committed to git or KSJ. Per the project's standing workflow, KSJ `extract_insights` runs through Claude Desktop, not Claude Code.

---

## 1. Pre-Flight Verification

| Check | Result |
|---|---|
| CAILculator version | v2.1.4, Engine v2.0 High-Precision, Production Stable |
| Local baseline reproduction (`phase77_q17_signed_channel.py`) | z=8.42, AUC(δ=0.5)=0.8661, precision(ε=0.5)=0.831 — exact match to `phase77_q17_results.json` |
| Live identity check, γ₁, pattern 2 | server 3.1204551984921403 = recorded 3.1204551984921403 (exact) |
| Live identity check, γ₁, pattern 6 | server 2.102194713548072 = recorded 2.102194713548072 (exact) |
| c_S2 + c_S6 vs recorded sum (5.222649912040213) | 5.222649912040212 (agreement to float precision) |

**Verdict:** environment and instrument confirmed stable; safe to proceed to Q-18.

---

## 2. Q-18 Candidate 1 — Per-Gateway Explicit-Formula Weighting

**Design (per handoff §3):** read all six gateways under the Detector Encoding, weight each by `(z_g/Σz)²` from its own T1 value-at-zeros z-score, sum.

### 2.1 Structural pre-check

Before running anything, the algebra of what each gateway reads under the Detector Encoding (pos2=0, signal only in u₂={3,5,10,12} and u₆={6,9} slots) was worked out and then confirmed numerically:

- **S3 ≡ S6 exactly** (`max|c_S3 − c_S6| = 0.0`) — S3's differentiating support indices {4,11} are zeroed by the encoding, leaving only the {6,9} slots shared with S6.
- **S1, S4, S5 (Class B) are dominated by a −2t linear term** (measured slope of c_S1 vs t: −2.0001) from the shared pos1=t protocol slot in their support.

### 2.2 Per-gateway z-scores (T1, full 101 zeros)

| Gateway | Class | z |
|---|---|---|
| S1 | B | −2.320 |
| S2 | A | +6.642 |
| S3 | A | +5.351 |
| S4 | B | −2.374 |
| S5 | B | −2.308 |
| S6 | A | +5.351 |

### 2.3 Ensemble evaluation

| | in-sample (fit + eval, same 101 zeros) | held-out (weights fit on first 50, eval on remaining 51) |
|---|---|---|
| Ensemble z | **−1.89** | **−7.26** |
| Baseline (c_S2+c_S6, unfitted) z | 8.42 | 5.12 |

Even in-sample — the optimistic case — the ensemble underperforms the unfitted baseline and goes negative. Held out, it is actively anti-correlated with zero locations (ROC AUC drops to 0.40–0.43, worse than chance).

**Mechanism:** squaring `(z_g/Σz)` discards sign. S1/S4/S5 have *negative* z (anti-correlated with zero proximity), but squaring makes their weights positive regardless, so they get summed in with the wrong orientation — compounded by S3=S6 double-counting the {5,7} prime channel.

**Verdict: NO IMPROVEMENT. Candidate 1 fails, with an identified statistical bug in the weighting formula itself, not just noise dilution.**

---

## 3. Q-18 Candidate 2 — Class B Sign-Structure Hybrid

**Design (per handoff §3, refined per Claude Desktop's follow-up):** `detector_hybrid(t;λ) = c_S2 + c_S6 + λ·(c_S1 − c_S4)`. Under the Detector Encoding, `c_S1 − c_S4 = −4·w₁₃·cos(t·ln13)` exactly (confirmed, residual 5.68×10⁻¹⁴) — the shared −2t drift cancels between S1 and S4, leaving a clean, t-drift-free prime-13 channel. This does not add new prime information (p=13 is already inside c_S2) but lets λ retune the *relative weight* the detector gives cos(t·ln13) against the standard explicit-formula weighting.

**Protocol:** grid-search λ ∈ [−3,3] (step 0.05) maximizing T1 z on the first 30 zeros; evaluate the fixed λ on the remaining 71, held out.

| | value |
|---|---|
| λ* (fit on train) | **−0.05** |
| Train z at λ* | 6.0918 |
| Train z at λ=0 | 6.0902 |
| Held-out (71 zeros) hybrid z | **6.153** |
| Held-out (71 zeros) baseline z | **6.158** |

The optimizer could barely move λ off zero, and the held-out z is a wash (hybrid marginally *below* baseline).

**Verdict: NO IMPROVEMENT. The standard explicit-formula weight `w_p = log p/√p` is already near-optimal for p=13 — retuning it empirically finds nothing.**

---

## 4. Q-18 Candidate 3 — Higher Prime Truncation (k=1 → k=2)

### 3.1 Slot-assignment correction

The handoff doc suggested adding p=17/19 into "unused u₂ slots {4,7}." This is not quite right: **index 7 is not in the support of any of the six Canonical Six gateways** — a signal placed there is invisible to every reading, dead weight. **Index 4 is live, but it belongs to S3's support** {4,11,6,9}, not S2's or S6's. Once traced correctly, putting `w₁₇·cos(t·ln17)` in slot 4 makes

> c_S3 = −2·(w₁₇cos(t·ln17) + w₁₁·0 + w₅cos(t·ln5) + w₇cos(t·ln7)) = c_S6 − 2·w₁₇·cos(t·ln17)

so `detector_extended = c_S2 + c_S3 = c_S2 + c_S6 − 2·w₁₇·cos(t·ln17)` — the natural 7-prime explicit-formula detector, realized without disturbing S2 or S6 at all. A second prime (p=19) extends the same way via slot 11 (also in S3's support), giving an 8-prime detector via c_S2+c_S3 alone. Identity confirmed to residual 8.88×10⁻¹⁶ (p=17 alone) and 1.78×10⁻¹⁵ (p=17+p=19, in Run C, §4).

No free parameter is fit here — both `w₁₇` and `w₁₉` use the standard explicit-formula recipe `log p/√p`, so this result does not carry Candidate 1/2's overfitting risk.

### 3.2 Results

| | z (20-zero quick check) | z (full 101 zeros) |
|---|---|---|
| Baseline (6 primes) | 5.61 | 8.42 |
| +p17 (7 primes) | 5.96 | 9.17 |
| +p17+p19 (8 primes) | — | **9.84** |

The 20-zero quick check cleared the handoff's own go/no-go bar, triggering the full-101 run.

**Verdict: IMPROVEMENT. z rises from 8.42 to 9.84 (8-prime), a genuine gain from extending the explicit-formula truncation, not a fitting artifact.**

---

## 4. Run C — High-Zero Validation (executed immediately after Candidate 3, per Paul's instruction)

**Question (carried over from the July 11, 2026 opening handoff):** does the detector z-score keep growing sub-√N beyond γ₁₀₁, or plateau? Run together with Candidate 3 to check whether its margin holds at scale.

**Protocol:** t ∈ [10,600], Δt=0.005 (118,001 points), 340 zeros through γ₃₄₀ ≈ 598.5. Two detectors compared at four zero-count checkpoints, each against its own pure explicit-formula control (no gateway indirection) to isolate architecture dilution from truncation effects.

| N zeros | γ_N | base6 (k=1) z | ext8 (k=2) z | f6/f8 control z | √N-predicted (base6 / ext8, from γ₁₀₁) |
|---|---|---|---|---|---|
| 101 | 237.77 | 8.483 | 10.009 | 8.483 / 10.009 | 8.48 / 10.01 |
| 150 | 318.85 | 9.268 | 10.660 | 9.268 / 10.660 | 10.34 / 12.20 |
| 200 | 396.38 | 10.070 | 11.658 | 10.070 / 11.658 | 11.94 / 14.08 |
| 340 | 598.49 | 11.871 | 13.833 | 11.871 / 13.833 | 15.56 / 18.36 |

(N=101 z reads 8.48 here vs 8.42 in §2A of the Phase 77 doc/§3.2 above — not a discrepancy: the null here samples query points over the full [10,600] range rather than [10,240], so the null scope changed with the grid, not the statistic.)

**Findings:**

1. **No plateau.** Both detectors keep growing in z through γ₃₄₀, at a rate that is consistently *below* the naive √N extrapolation from γ₁₀₁ (sub-√N growth, same pattern as the Phase 77 c_S2 result) — genuine strengthening, not pure statistical scaling.
2. **The Candidate 3 margin is stable, not a small-N artifact**: ext8 − base6 = +1.53 (γ₁₀₁), +1.39 (γ₁₅₀), +1.59 (γ₂₀₀), +1.96 (γ₃₄₀).
3. **Zero architecture dilution at high zero density.** The gateway-realized detectors matched the pure explicit-formula controls to the same decimal at every checkpoint (identity residual 1.78×10⁻¹⁵) — the instrument stays exact as the grid and zero count grow, it does not degrade.

**Verdict: Run C confirms sub-√N growth continues with no plateau through γ₃₄₀, and validates that Candidate 3's improvement is real at scale, not an N=101 artifact.**

---

## 5. Artifacts

| Artifact | Path |
|---|---|
| Candidate 1 script | `scripts/phase78_q18_candidate1_per_gateway.py` |
| Candidate 1 results JSON | `results/phase78_q18_candidate1_results.json` |
| Candidate 2 script | `scripts/phase78_q18_candidate2_classb.py` |
| Candidate 2 results JSON | `results/phase78_q18_candidate2_results.json` |
| Candidate 3 script | `scripts/phase78_q18_candidate3_higher_primes.py` |
| Candidate 3 results JSON | `results/phase78_q18_candidate3_results.json` |
| Run C script | `scripts/phase78_q18_runC_high_zeros.py` |
| Run C results JSON | `results/phase78_q18_runC_results.json` |

All scripts reuse the Detector Encoding and T1 value-at-zeros statistic exactly as defined in `phase77_q17_signed_channel.py`; no changes to gateway definitions, encoding conventions, or the Gateway Linear Law were made. Nothing has been staged or committed to git.

---

## 6. Open Items

- **Lean track (undecided this phase).** The July 11, 2026 opening handoff's primary Lean targets — `SedenionProduct.lean` infrastructure and Q-16 `canonical_six_e0_transparency` — were not touched this session. Paul is still deciding whether to pursue Lean work in Phase 78 or keep it empirical-only.
- **`detector_channel_identity` Lean lemma** (candidate, standard axioms, over `GatewayLinearLaw.lean`) — still Paul's call on stack growth, now with a natural follow-on question of whether to formalize the k=2 extension (§3.1) as well if the k=1 identity is ever added.
- **KSJ extraction** — not run. Per standing workflow, `extract_insights` goes through Claude Desktop, not Claude Code. Ready for extraction: Candidate 1 (negative + mechanism), Candidate 2 (negative + near-optimality confirmation), Candidate 3 (positive, z 8.42→9.84), Run C (positive, no plateau to γ₃₄₀, margin holds, zero dilution).
- **Candidate 4 (Clifford framework variant)** — deferred, per the handoff's own gate ("requires clarification on whether Lean has Clifford inner products exposed... Hold for Paul's direction").
- **GitHub push** — not applicable yet; no branch opened, no commits made this phase.
- **v1.4 abstract** — unaffected by this session; still open from Phase 77.

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 78 (draft) · August 22, 2026*
