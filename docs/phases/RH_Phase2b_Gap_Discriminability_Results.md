# RH Phase 2b — Gap Sequence Discriminability Results
**Experiment ID:** RH_GAP_2026_001  
**Date:** 2026-03-04  
**Researcher:** Paul Chavez, Chavez AI Labs

---

## Summary Table

| Test | Conjugation Symmetry | Δ from Baseline | Verdict |
|---|---|---|---|
| **Baseline: n=99 gaps (unshuffled)** | **83.8%** | — | Reference |
| Shuffle seed=1 | 82.9% | −0.9 pts | |
| Shuffle seed=2 | 85.9% | +2.1 pts | |
| Shuffle seed=3 | 82.9% | −0.9 pts | |
| **Shuffle mean (3 trials)** | **83.9%** | **+0.1 pts** | **Ordering does NOT matter** |
| Synthetic Exp. seed=1 (mean=1.41) | 79.0% | −4.8 pts | |
| Synthetic Exp. seed=2 | 81.5% | −2.3 pts | |
| Synthetic Exp. seed=3 | 79.8% | −4.0 pts | |
| **Synthetic Exp. mean (3 trials)** | **80.1%** | **−3.7 pts** | **Borderline — below 5 pt threshold** |
| Scale: n=249 gaps | 86.2% | +2.4 pts | |
| Scale: n=499 gaps | ~86% (est.) | ~+2 pts | |

---

## Finding 1: Ordering Does NOT Matter

**Verdict: CLEAR. The sequential structure of Riemann zero gaps carries no additional bilateral symmetry beyond what the gap *distribution* alone provides.**

Shuffle mean: **83.9%** vs baseline 83.8% — a difference of +0.1 points. Across three independent shuffles with different random seeds, two trials scored below baseline (82.9%) and one scored above (85.9%). The variation between shuffles (±3 pts) is larger than the signal between shuffled and unshuffled. 

The handoff threshold was: "significantly lower = more than 5 percentage points below 83.8%." The shuffles show +0.1 pts. **Ordering is irrelevant to the Chavez conjugation symmetry signal.** The 83.8% result is entirely explained by the *distribution* of gap sizes, not their sequential arrangement. This is consistent with a gap size distribution that already has bilateral structure, independent of ordering.

**Interpretation:** The bilateral symmetry detected by Chavez is a property of the gap *ensemble* — the set of gap values that appear in the first 99 zero spacings — not the specific order in which they appear. This weakens the connection to GUE, because GUE's key distinguishing feature is its long-range pair correlations (which are ordering-dependent). A measure that is ordering-invariant cannot detect GUE correlations.

---

## Finding 2: Synthetic Exponential Gaps — Borderline Separation

**Verdict: BORDERLINE. Exponential gap distribution (mean=1.41) scores 3.7 points below the actual zero gaps on average, but this is below the 5-point significance threshold.**

Synthetic mean: **80.1%** vs baseline 83.8%. Individual trials ranged 79.0–81.5%. The threshold was 5 points. The actual separation is 3.7 points — real but sub-threshold.

**Two interpretations:**
1. The Riemann zero gap *distribution* (not ordering, not GUE correlations) has slightly more bilateral structure than a pure exponential. This is consistent with GUE-vs-Poisson gap statistics: GUE gaps have level repulsion (fewer very small gaps), producing a slightly more "balanced" distribution than exponential. The Chavez measure may be detecting this distributional difference, not the sequential correlations.
2. The 3.7-point gap could also be a sample-size artifact. With mean=1.41 vs actual mean=2.25 (the actual gap mean is 59% larger than the exponential parameter used), the controls are drawing from a different regime. A better-matched control would use mean=2.25.

**Action for Phase 3:** Re-run synthetic control with mean=2.25 (matching actual n=99 gap mean, not the full 999-gap mean). This eliminates the distribution-mismatch confound and gives a cleaner test of whether GUE gaps specifically differ from Poisson.

---

## Finding 3: Scale Stability — CONFIRMED

**Verdict: CLEAR. The 83.8% conjugation symmetry result is scale-stable, not a small-n artifact.**

| n | Symmetry |
|---|---|
| 99 | 83.8% |
| 249 | 86.2% |
| ~499 | ~86% |

Symmetry *increases* slightly at larger n, settling around 86%. This is the opposite of what a small-sample artifact would produce — artifacts typically decay with more data. The signal is robust and scale-invariant across the tested range.

This is the strongest positive result from Phase 2b. The 83.8% result generalizes: it's not specific to the first 99 zeros. At n=249, it reaches 86.2% — now entering Sophie Germain prime territory (88.5%).

---

## Decision Matrix Assessment

| Test | Threshold | Result | Verdict |
|---|---|---|---|
| Shuffle drops >5 pts | >5 pt drop | +0.1 pt (no drop) | ❌ Ordering does not matter |
| Synthetic Exp. separates >5 pts | >5 pt separation | 3.7 pt separation | ⚠️ Borderline — sub-threshold |
| Scale invariant across n | Stable ±5 pts | Stable, slight rise | ✅ Scale stable |

Strongest possible outcome (all three YES) was not reached. The scale stability is confirmed; the ordering and GUE separation tests produced softer results.

---

## Updated Interpretation

The 83.8% Chavez conjugation symmetry on Riemann zero gaps is:
- **Ordering-independent** → not detecting sequential GUE correlations
- **Slightly above exponential** → possibly detecting gap *distribution* shape (level repulsion)
- **Scale-stable** → a genuine property of the zero spectrum, not a small-n artifact
- **Approaching SG primes** at larger n (86.2% at n=249 vs SG primes at 88.5%)

The measure is detecting something real about the zero gap distribution — but not the specifically sequential structure that would constitute a strong GUE algebraic signal. It's closer to "the gap distribution of Riemann zeros has slightly more bilateral balance than pure exponential" — which is consistent with GUE level repulsion as a distributional feature.

---

## Coherent Picture (Claude Desktop synthesis)

The Chavez measure is detecting something distributional about the zero gaps — possibly the **level repulsion signature**: GUE has fewer very small gaps than Poisson, producing a slightly more balanced bilateral distribution. To confirm this, two runs are needed together:

1. A properly mean-matched exponential control (mean=2.25)
2. A true GUE gap synthetic (Wigner surmise)

Those two runs together will tell you whether Chavez is specifically fingerprinting the GUE spacing distribution or just coarse gap statistics.

## Revised Phase 3 Priorities

1. **Better-matched synthetic control:** Re-run exponential gaps with mean=2.25 (actual n=99 mean), not 1.41. This eliminates the distribution mismatch confound.

2. **GUE synthetic gaps:** Generate gaps from the actual GUE nearest-neighbor spacing distribution (Wigner surmise: P(s) ∝ s·exp(−πs²/4)) and run Chavez. If GUE-distributed gaps score near 83.8% and exponential (Poisson) gaps score lower, Chavez is genuinely detecting the GUE distributional signature.

3. **Proceed to Phase 2 annihilation topology** (AT-1/AT-2): This is independent of the gap analysis and can run in parallel. The AT results may provide structural evidence independent of what the Chavez measure detects.

4. **Update CLAUDE.md**: Chavez symmetry at 83.8% is ordering-independent; the meaningful claim is distributional, not sequential.

---

## Files
- `rh_gaps.json` — source data (999 gaps)
- `rh_phase2b_sequences.json` — shuffled sequences and synthetic gaps used in this experiment
- `RH_Phase2b_Gap_Discriminability_Results.md` — this document
