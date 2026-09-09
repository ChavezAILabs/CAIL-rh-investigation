# RH Investigation — Phase 78 Results v2: Q-18 Detector Ensemble & Run C
**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Date:** 2026-09-08 (v2, superseding `RH_PHASE_78_RESULTS.md`)
**Phase:** 78 (Q-18 empirical track + Run C)
**Tag:** #phase-78-detector-ensemble
**Execution:** Claude Sonnet 5 (Claude Code, in-shell), original run Aug 22–23, 2026; corrections and re-verification Sept 8, 2026
**Branch:** `phase-78-q18`, commit `4af1fa7`
**Status:** v1 contained four wrong or incomplete claims, including its headline finding. See [`CORRECTIONS.md`](../../CORRECTIONS.md) — entries C-001, C-007, C-009, C-010, C-011, C-012 all bear on this document. This version corrects the interpretation of every number v1 reported; **no number in v1 was wrong**, only what several of them were said to mean.

---

## Executive Summary

**Pre-flight verification: PASSED, and the provenance behind it is stronger than v1 stated.** `phase77_q17_signed_channel.py` reproduced the Phase 77 baseline exactly (z=8.42, AUC=0.8661, precision=0.831), and a live CAILculator v2.1.4 call at γ₁ matched the recorded `phase77_q17_live_validation.json` values to full double precision. v1 read this as "the instrument has not drifted since June 12," which a later review (C-012) initially challenged as circular — a script's output compared to a file the same script wrote in the same session. That challenge was itself wrong: SHA-256 verification against git history shows `phase77_q17_results.json` and `phase77_q17_live_validation.json` are byte-identical to commit `a96bc39`, dated 2026-06-12. The pre-flight was a genuine reproduction against a committed reference two months old, not a comparison of a script to itself. See §1.

**Q-18 asked: can a multi-gateway ensemble beat the Detector Encoding baseline (z=8.42, AUC 0.866)?** Three candidates were run under a held-out-data discipline (weights/parameters fit on a training slice, evaluated on a disjoint test slice) after Candidate 1 exposed how badly in-sample fitting overstates these ensembles:

- **Candidate 1 (per-gateway weighting): FAILS, badly.** Held-out z = **−7.26** vs an unfitted baseline of 5.12. Root cause: under the Detector Encoding, S3 is algebraically identical to S6 (§4.1), so a naive six-gateway sum double-counts one prime channel; and the handoff's `(z_g/Σz)²` weighting formula discards the sign of each gateway's z-score, giving the three anti-correlated Class B gateways (z ≈ −2.3 each) positive weight with the wrong orientation.
- **Candidate 2 (Class B hybrid, λ·(c_S1−c_S4)): FAILS, cleanly, and the finding is stronger than "marginally below baseline."** Best-fit λ on a 30-zero training slice is **−0.05** after a 121-point grid search — the optimizer found essentially nothing to adjust. Held-out z = 6.15 vs baseline 6.16: a gap of 0.0046, roughly thirteen times smaller than the ±0.09 seed-to-seed variation the null carries (C-008). The hybrid and the baseline are statistically indistinguishable; the real evidence for "no improvement" is the optimizer finding nothing, not the tiny ordering. See §3.
- **Candidate 3 (higher-prime truncation, k=1→k=2): SUCCEEDS, and on stronger grounds than v1 reported.** Extending the 6-prime detector to 8 primes (p=17, p=19) raises z from 8.42 to 9.84 at γ₁–γ₁₀₁, using only the standard explicit-formula weight `w_p = log p/√p` — no fitted parameter. v1 reported this on the T1 statistic alone; ROC AUC and peak-matching precision, computed after the fact (C-011), both improve too — AUC 0.8661 → **0.9059** at N=101, 0.8342 → **0.8704** at N=340. AUC is rank-based and invariant under monotone rescaling, so this cannot be an amplitude artifact of the eight-prime detector simply reading larger values. See §4 and §5.4.

**Run C** extended the grid to t ∈ [10,600] (340 zeros through γ₃₄₀ ≈ 598.5). v1's headline finding here was backwards:

1. **Both detectors' z keep rising through γ₃₄₀ — but this is not "genuine strengthening."** Per-zero detector strength *declines* with height on every metric measured (T1, AUC, peak precision-over-chance); z rises only because the Monte-Carlo null tightens as 1/√N. A candidate mechanism for the decay is offered as conjecture, explicitly labelled as untested. See §5.1.
2. **Candidate 3's AUC margin over baseline is real and roughly constant across scale** (+0.040 at N=101, +0.036 at N=340) — a uniform detection improvement, not one that extends the detector's reach as zero density rises. That distinction matters for Phase 79. See §5.4.
3. **The Run C "controls" are not controls.** `f6_control ≡ base6` and `f8_control ≡ ext8` to machine precision at every checkpoint, but this is forced by the Gateway Linear Law identity — the gateway reading and the explicit-formula sum are the same function by construction, so the match carries no information about architecture dilution at high zero density. That question remains open and untested. See §5.2.
4. **The k=1 and k=2 detectors are the same channel pair, not two different detectors.** Under the Detector Encoding, S3 ≡ S6 exactly (§4.1); Candidate 3's extension breaks that degeneracy by moving new primes into S3's otherwise-unused slots. §2.1 (Candidate 1's structural pre-check) and §4.1 (Candidate 3's slot correction) describe the same structural fact from two directions and are presented together here. See §4.1.

**Net Q-18 verdict, unchanged from v1:** ensembling across the existing six Canonical Six gateways under the Detector Encoding does not help (two independent negative results, both with identified mechanisms). The k=1→k=2 explicit-formula truncation is a real, scale-holding improvement, now supported by a rank-based metric in addition to T1.

Every z-score in this document should be read with its seed and resample count: `seed = 20260612`, `n_trials = 5000`, giving a minimum resolvable two-sided p of 2×10⁻⁴ and a run-to-run z variation of roughly ±0.09 (C-007, C-008). Achieved significance throughout is **p < 2×10⁻⁴**, not the p-value a z of this size would suggest under a continuous normal null — the Monte-Carlo null is discrete and floored. z is an effect size, not a significance level.

Nothing in this phase has been committed to KSJ. Per the project's standing workflow, KSJ `extract_insights` runs through Claude Desktop, not Claude Code. Git commits for this phase and its September 8 corrections are on branch `phase-78-q18`.

---

## 1. Pre-Flight Verification

| Check | Result |
|---|---|
| CAILculator version | v2.1.4, Engine v2.0 High-Precision, Production Stable |
| Local baseline reproduction (`phase77_q17_signed_channel.py`) | z=8.42, AUC(δ=0.5)=0.8661, precision(ε=0.5)=0.831 — exact match to `phase77_q17_results.json` |
| Live identity check, γ₁, pattern 2 | server 3.1204551984921403 = recorded 3.1204551984921403 (exact) |
| Live identity check, γ₁, pattern 6 | server 2.102194713548072 = recorded 2.102194713548072 (exact) |
| c_S2 + c_S6 vs recorded sum (5.222649912040213) | 5.222649912040212 (agreement to float precision) |
| **Provenance of the baseline file (added 2026-09-08)** | `phase77_q17_results.json` SHA-256-identical (after CRLF normalization) to commit `a96bc39`, 2026-06-12 14:42:22 -0700 |

**Verdict:** environment and instrument confirmed stable; the reference file being reproduced is a two-month-old committed artifact, not a same-session regeneration. Safe to proceed to Q-18.

---

## 2. Q-18 Candidate 1 — Per-Gateway Explicit-Formula Weighting

**Design (per handoff §3):** read all six gateways under the Detector Encoding, weight each by `(z_g/Σz)²` from its own T1 value-at-zeros z-score, sum.

### 2.1 Structural pre-check

Before running anything, the algebra of what each gateway reads under the Detector Encoding (pos2=0, signal only in u₂={3,5,10,12} and u₆={6,9} slots) was worked out and then confirmed numerically:

- **S3 ≡ S6 exactly** (`max|c_S3 − c_S6| = 0.0`) — S3's differentiating support indices {4,11} are zeroed by the encoding, leaving only the {6,9} slots shared with S6. **This is the same structural fact behind Candidate 3's slot correction in §4.1 — see there for the unified statement.**
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

**Mechanism:** squaring `(z_g/Σz)` discards sign. S1/S4/S5 have *negative* z (anti-correlated with zero proximity), but squaring makes their weights positive regardless, so they get summed in with the wrong orientation (C-014) — compounded by S3=S6 double-counting the {5,7} prime channel.

**Verdict: NO IMPROVEMENT. Candidate 1 fails, with an identified statistical bug in the weighting formula itself, not just noise dilution.**

---

## 3. Q-18 Candidate 2 — Class B Sign-Structure Hybrid

**Design (per handoff §3, refined per Claude Desktop's follow-up):** `detector_hybrid(t;λ) = c_S2 + c_S6 + λ·(c_S1 − c_S4)`. Under the Detector Encoding, `c_S1 − c_S4 = −4·w₁₃·cos(t·ln13)` exactly (confirmed, residual 5.68×10⁻¹⁴) — the shared −2t drift cancels between S1 and S4, leaving a clean, t-drift-free prime-13 channel. This does not add new prime information (p=13 is already inside c_S2) but lets λ retune the *relative weight* the detector gives cos(t·ln13) against the standard explicit-formula weighting.

**Protocol:** grid-search λ ∈ [−3,3] (step 0.05, 121 points) maximizing T1 z on the first 30 zeros; evaluate the fixed λ on the remaining 71, held out.

| | value |
|---|---|
| λ* (fit on train, 121-point grid) | **−0.05** |
| Train z at λ* | 6.0918 |
| Train z at λ=0 | 6.0902 |
| Held-out (71 zeros) hybrid z | **6.153** |
| Held-out (71 zeros) baseline z | **6.158** |

**Correction (2026-09-08, C-010).** v1 read the held-out gap as "hybrid marginally *below* baseline" and used that ordering as part of the verdict. That ordering is not evidence of anything: the gap is 0.0046, against a run-to-run seed variation of roughly ±0.09 in z (C-008) — about thirteen times smaller than the noise floor. The hybrid and the baseline are statistically indistinguishable, full stop; there is no defensible direction to the comparison. The actual finding is upstream of that noise: a 121-point grid search over λ moved the optimum only to −0.05, essentially zero, with train z at the optimum (6.0918) barely different from train z at λ=0 (6.0902). The optimizer had three full orders of magnitude of λ-range to search and found nothing worth taking.

**Verdict: NO IMPROVEMENT. The standard explicit-formula weight `w_p = log p/√p` is already near-optimal for p=13 — the grid search confirms this directly; the held-out z comparison is not the evidence and should not be cited as such.**

---

## 4. Q-18 Candidate 3 — Higher Prime Truncation (k=1 → k=2)

### 4.1 Slot-assignment correction, and its structural unification with §2.1

The original handoff doc suggested adding p=17/19 into "unused u₂ slots {4,7}." This is not quite right: **index 7 is not in the support of any of the six Canonical Six gateways** — a signal placed there is invisible to every reading, dead weight. **Index 4 is live, but it belongs to S3's support** {4,11,6,9}, not S2's or S6's. This was caught and corrected before any result was computed from the faulty assignment (C-013).

Once traced correctly, putting `w₁₇·cos(t·ln17)` in slot 4 makes

> c_S3 = −2·(w₁₇cos(t·ln17) + w₁₁·0 + w₅cos(t·ln5) + w₇cos(t·ln7)) = c_S6 − 2·w₁₇·cos(t·ln17)

so `detector_extended = c_S2 + c_S3 = c_S2 + c_S6 − 2·w₁₇·cos(t·ln17)` — the natural 7-prime explicit-formula detector, realized without disturbing S2 or S6 at all. A second prime (p=19) extends the same way via slot 11 (also in S3's support), giving an 8-prime detector via c_S2+c_S3 alone. Identity confirmed to residual 8.88×10⁻¹⁶ (p=17 alone) and 1.78×10⁻¹⁵ (p=17+p=19, in Run C, §5).

**This is the same fact §2.1 found from the other direction.** S3 ≡ S6 exactly under the k=1 Detector Encoding, because S3's differentiating slots {4,11} are zeroed and only its shared {6,9} slots (with S6) carry signal. Candidate 3's extension is not a different detector built from a different gateway — it is the *same* channel pair (c_S2 paired with what is, at k=1, a copy of S6) with the S3/S6 degeneracy broken by putting new primes exactly where S3 differs from S6. The k=1 detector `c_S2+c_S6` and the k=2 detector `c_S2+c_S3` are one structural object at two truncation orders, not two independent architectures.

No free parameter is fit here — both `w₁₇` and `w₁₉` use the standard explicit-formula recipe `log p/√p`, so this result does not carry Candidate 1/2's overfitting risk.

### 4.2 T1 results

| | z (20-zero quick check) | z (full 101 zeros) |
|---|---|---|
| Baseline (6 primes) | 5.61 | 8.42 |
| +p17 (7 primes) | 5.96 | 9.17 |
| +p17+p19 (8 primes) | — | **9.84** |

The 20-zero quick check cleared the handoff's own go/no-go bar, triggering the full-101 run.

### 4.3 ROC and peak-matching metrics (added 2026-09-08, C-011)

v1 reported Candidate 3 on T1 alone, against a baseline described with two additional metrics (ROC AUC, peak precision) — an incomplete comparison, and one that could not by itself distinguish "better detector" from "detector reads larger numbers." AUC and peak-matching precision, computed with the identical code paths used for the baseline, close that gap. See §5.4 for the N=340 figures and the full discussion.

| | AUC δ=0.5, N=101 | Peak P @ ε=0.5, N=101 |
|---|---|---|
| base6 | 0.8661 | 0.831 |
| ext8 | **0.9059** | **0.901** |

Because AUC and peak precision are rank statistics, invariant under any monotone rescaling of the detector's output, this rules out "the eight-prime detector just reads bigger numbers" as an explanation for the T1 gain.

**Verdict: IMPROVEMENT, on stronger grounds than v1 reported.** z rises from 8.42 to 9.84 (8-prime), and AUC and peak precision rise with it — a genuine gain from extending the explicit-formula truncation, corroborated by a metric that cannot be an amplitude artifact.

---

## 5. Run C — High-Zero Validation (executed immediately after Candidate 3, per Paul's instruction)

**Question (carried over from the July 11, 2026 opening handoff):** does the detector z-score keep growing sub-√N beyond γ₁₀₁, or plateau? Run together with Candidate 3 to check whether its margin holds at scale.

**Protocol:** t ∈ [10,600], Δt=0.005 (118,001 points), 340 zeros through γ₃₄₀ ≈ 598.5. Two detectors compared at four zero-count checkpoints, each against its own pure explicit-formula identity check (§5.2) to verify the architecture stays exact as the grid grows.

| N zeros | γ_N | base6 (k=1) z | ext8 (k=2) z | identity check (base6/ext8 vs pure sum) | √N-predicted from γ₁₀₁ (base6 / ext8) |
|---|---|---|---|---|---|
| 101 | 237.77 | 8.483 | 10.009 | match to 1.78×10⁻¹⁵ | 8.48 / 10.01 |
| 150 | 318.85 | 9.268 | 10.660 | match to 1.78×10⁻¹⁵ | 10.34 / 12.20 |
| 200 | 396.38 | 10.070 | 11.658 | match to 1.78×10⁻¹⁵ | 11.94 / 14.08 |
| 340 | 598.49 | 11.871 | 13.833 | match to 1.78×10⁻¹⁵ | 15.56 / 18.36 |

(N=101 z reads 8.483 here vs 8.42 in the Phase 77 §2A / §4.2 baseline. This is a real, code-level effect — this script's null samples query points over the full [10,600] range rather than [10,240] — but a three-arm test (C-008) found Arm C's scope-varied spread sits *inside* Arm B's seed-only spread at this N: [8.3818, 8.4831] vs [8.3789, 8.5540]. The gap is not distinguishable from ordinary Monte-Carlo noise here, so it should not be read as evidence of a scope-dependence bias, even though the mechanism is real.)

### 5.1 Finding 1 — per-zero signal decays; z rises only because the null tightens

**Correction (2026-09-08, C-001) — this finding was reported backwards in v1.** v1's text: "Both detectors keep growing in z through γ₃₄₀... genuine strengthening, not pure statistical scaling." The opposite is closer to true.

| N | γ_N | observed T1 (base6) | null_std | null_std·√(N/101) | z |
|---|---|---|---|---|---|
| 101 | 237.77 | 1.9662 | 0.2309 | 0.2309 | 8.483 |
| 150 | 318.85 | 1.7806 | 0.1919 | 0.2339 | 9.268 |
| 200 | 396.38 | 1.6838 | 0.1669 | 0.2348 | 10.070 |
| 340 | 598.49 | 1.5041 | 0.1265 | 0.2321 | 11.871 |

The null_std column, rescaled by √(N/101), is flat to under 2% — it tightens almost exactly as 1/√N, as a Monte-Carlo null over a fixed-width query set should. The observed T1 statistic — the numerator — falls monotonically, to 76.5% of its N=101 value by γ₃₄₀. **All of the z growth is the null shrinking; none of it is the detector reading stronger.** "Sub-√N growth" was read as evidence the signal was strengthening (just more slowly than statistical scaling alone would predict); it should have been read as the null tightening while the numerator quietly weakens — a decay, not a diminished growth.

**Candidate mechanism, offered as conjecture and explicitly not yet tested:** the six-prime detector's finest oscillation has period 2π/log 13 ≈ 2.45. The mean Riemann-zero gap 2π/log(t/2π) falls from ≈1.73 at γ₁₀₁ to ≈1.38 at γ₃₄₀ — zeros are packing tighter than a fixed-truncation detector can resolve. This is the prime-log commensurability limit raised in the July 11, 2026 opening handoff. It is a plausible story consistent with the direction of the decay; it has not been tested against an alternative.

**Note, unaffected by this correction:** the same structure was present in Phase 77 and mislabeled there first (see `RH_PHASE_77_RESULTS.md` §2A.1, corrected the same day): c_S2 observed 1.8464 at 31 zeros → 1.3735 at 101 (74%), null_std 0.5075 → 0.2783 (ratio 0.548 against √(31/101) = 0.554).

This correction strengthens rather than weakens the research programme. A measured decay law with a candidate mechanism is a better result than an unexplained growth claim.

### 5.2 Finding 2 — the identity checks are not controls, and dilution remains untested

**Correction (2026-09-08, C-009).** v1's finding 3 read: "Zero architecture dilution at high zero density. The gateway-realized detectors matched the pure explicit-formula controls to the same decimal at every checkpoint — the instrument stays exact as the grid and zero count grow, it does not degrade." The word "controls" (and the field names `f6_control`/`f8_control` in the results JSON) implied this was an independent check that could have failed.

It could not have. `f6_control ≡ base6` and `f8_control ≡ ext8` to 0.0 or 1.78×10⁻¹⁵ at every checkpoint because the Gateway Linear Law identity `c_S2 + c_S6 = −2Σ_p w_p cos(t log p)` forces the gateway reading and the pure explicit-formula sum to be the same function. This is a genuine, valuable identity verification across four sample sizes and two truncation orders — worth keeping as exactly that — but it carries no information about dilution at high zero density, because there is no way for it to have come out differently. Dilution, if present, would show up in the T1/AUC/peak statistics themselves, not in an identity that is exact by construction. That question, raised in the July 11, 2026 opening handoff, remains open and untested.

### 5.3 Finding 3 — Candidate 3's margin holds at scale, and is now measured on a rank statistic too

T1 margin, unchanged from v1: ext8 − base6 = +1.53 (γ₁₀₁), +1.39 (γ₁₅₀), +1.59 (γ₂₀₀), +1.96 (γ₃₄₀) z-points over baseline. The ext8/base6 *ratio* is flat across these four checkpoints (1.353, 1.322, 1.330, 1.333 in the observed statistic; 1.180, 1.150, 1.158, 1.165 in z) — v1 did not remark on this, but a flat ratio is exactly what a uniform amplitude gain looks like, and by itself cannot distinguish that from a genuine, scale-independent detection improvement. §5.4 resolves this with a rank-based metric.

### 5.4 AUC and peak-matching at N=101 and N=340 (added 2026-09-08, C-011)

Computed with the identical `roc_auc` / `local_maxima` / `peak_matching` code paths as the N=101 baseline (`phase77_q17_signed_channel.py`), reused verbatim; the N=101 base6 row reproduces AUC 0.8661 and peak precision 0.831 exactly, validating the method before trusting the N=340 numbers.

| | AUC δ=0.5 | Peak P @ ε=0.5 | Chance @ ε=0.5 | ratio |
|---|---|---|---|---|
| base6, N=101 | 0.8661 | 0.831 | 0.4334 | 1.92× |
| ext8, N=101 | **0.9059** | **0.901** | 0.4334 | 2.08× |
| base6, N=340 | 0.8342 | 0.817 | 0.5572 | 1.47× |
| ext8, N=340 | **0.8704** | **0.885** | 0.5572 | 1.59× |

Chance at ε=1.0 is 0.7607 (N=101) and 0.8765 (N=340) — every honest baseline must be stated at its own radius and its own zero count (C-007); chance rises with both.

**What this settles:** the k=2 extension improves AUC by +0.040 at N=101 and +0.036 at N=340 — real, and (being rank-based) not explainable as the eight-prime detector simply having larger amplitude. Candidate 3 is a genuine detection improvement, on firmer evidence than the T1 result alone provided.

**What this does not settle, and corrects from v1's framing:** the AUC gain is itself roughly flat across scale (+0.040 → +0.036), mirroring the flat T1 ratio noted in §5.3. This means the k=2 extension is a **uniform** improvement — it does not extend the detector's *reach* as zero density rises. Both detectors degrade with height on every metric (AUC 0.8661→0.8342 and 0.9059→0.8704; precision-over-chance 1.92×→1.47× and 2.08×→1.59×), consistent with and independently confirming the per-zero decay identified in §5.1, this time via a rank statistic rather than T1. This matters for Phase 79: whatever addresses the §5.1 decay mechanism is a separate problem from adding more primes, and the eight-prime detector should not be expected to hold up better at very high zero density than the six-prime one did.

**Verdict: Run C confirms z keeps rising through γ₃₄₀ with no plateau — but this is a null-tightening effect, not detector strengthening (§5.1). Candidate 3's improvement is real and rank-confirmed at both N=101 and N=340 (§5.4), but is a uniform gain, not one that grows with scale.**

---

## 6. Artifacts

| Artifact | Path |
|---|---|
| Candidate 1 script | `scripts/phase78_q18_candidate1_per_gateway.py` |
| Candidate 1 results JSON | `results/phase78_q18_candidate1_results.json` |
| Candidate 2 script | `scripts/phase78_q18_candidate2_classb.py` |
| Candidate 2 results JSON | `results/phase78_q18_candidate2_results.json` |
| Candidate 3 script | `scripts/phase78_q18_candidate3_higher_primes.py` |
| Candidate 3 results JSON | `results/phase78_q18_candidate3_results.json` |
| Candidate 3 ROC/peak metrics (added 2026-09-08) | `results/phase78_q18_candidate3_roc_results.json` |
| Run C script | `scripts/phase78_q18_runC_high_zeros.py` |
| Run C results JSON | `results/phase78_q18_runC_results.json` |
| Corrections register | `CORRECTIONS.md` |
| Sept 8 Lean verification record | `verification/2026-09-08/` |

All scripts reuse the Detector Encoding and T1 value-at-zeros statistic exactly as defined in `phase77_q17_signed_channel.py`; no changes to gateway definitions, encoding conventions, or the Gateway Linear Law were made. Phase 78 and its September 8 corrections are committed on branch `phase-78-q18` (commit `4af1fa7` and following).

---

## 7. Open Items

- **Lean track (undecided this phase).** The July 11, 2026 opening handoff's primary Lean targets — `SedenionProduct.lean` infrastructure and Q-16 `canonical_six_e0_transparency` — were not touched in the original Q-18 session, and are unaffected by the September 8 verification/corrections work, which used scratch copies only (`verification/2026-09-08/`) and modified no canonical `.lean` file. Paul is still deciding whether to pursue Lean work in Phase 78/79 or keep it empirical-only.
- **`detector_channel_identity` Lean lemma** (candidate, standard axioms, over `GatewayLinearLaw.lean`) — still Paul's call on stack growth, now with a natural follow-on question of whether to formalize the k=2 extension (§4.1) as well if the k=1 identity is ever added. The C-020 hypothesis audit found no decorative hypotheses anywhere in `GatewayLinearLaw.lean`'s four theorems, so this infrastructure is sound to build on whenever that call is made.
- **The §5.1 decay mechanism is untested.** The prime-log commensurability conjecture is offered as a candidate explanation, not a result. Testing it — e.g., checking whether the decay rate tracks the mean-gap/detector-period ratio more precisely, or whether a detector with a shorter finest period decays more slowly — is a natural Phase 79 question.
- **The §5.2 dilution question remains open and untested**, independent of the (uninformative) identity match.
- **KSJ extraction** — not run for the original Aug 22–23 results. Per standing workflow, `extract_insights` goes through Claude Desktop, not Claude Code. Any future extraction from this document should draw on v2's corrected findings, not v1's.
- **Candidate 4 (Clifford framework variant)** — still deferred, per the handoff's own gate.
- **v1.4 abstract** — unaffected by this session; still open from Phase 77.

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 78 v2 · September 8, 2026*
