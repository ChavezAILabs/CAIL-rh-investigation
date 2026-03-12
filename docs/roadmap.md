# RH Investigation Roadmap
## Chavez Transform & ZDTP Applied to the Riemann Hypothesis

**Researcher:** Paul Chavez, Chavez AI Labs LLC
**Initiated:** March 4, 2026
**Last Updated:** March 12, 2026
**Status:** Active — Phases 1–17 complete; Phase 18 next

---

## Overview

This roadmap documents the systematic application of the Chavez Transform and ZDTP to the nontrivial zeros of the Riemann zeta function. The investigation began March 4, 2026 and has produced seventeen completed experimental phases. Each phase has refined the research question — from broad structural detection through precise GUE discrimination, L-function arithmetic comparison, and now into the E8 geometric structure underlying the bilateral zero divisor mechanism.

The long-range objective is a contribution at the level of the Riemann Hypothesis itself: not merely empirical confirmation of GUE statistics, but a proposed algebraic mechanism — grounded in the Canonical Six bilateral zero divisors of sedenion space — that may explain *why* the zeros are constrained to the critical line Re(s) = ½.

**Foundational algebraic asset**: The Canonical Six and their 24-element bilateral zero divisor family (Lean 4 verified, zero sorry stubs). The Canonical Six are framework-independent across Cayley-Dickson and Clifford algebras. Their P-vector images lie on the E8 lattice first shell and form a single Weyl orbit — formally proven.

---

## Sensitivity Map (Established Across Phases 1–10)

| Input to Chavez | What It Detects |
|---|---|
| Raw zero positions | Monotone growth artifact — not meaningful |
| Raw gap values | Lower-bound compactness (gap floor ~0.72), not GUE-specific |
| Gap ordering | Ordering-invariant — cannot detect sequential GUE correlations |
| Spacing ratios rₙ | GUE/Poisson separation; correct ordering; widens n=99→499 ✅ |
| Scale behavior | Separation 5.3 pt (n=99) → 7.2 pt (n=499); not at ceiling ✅ |
| Height behavior | Higher zeros exceed GUE synthetic; low-height regime explains shortfall ✅ |
| Band-resolution survey | Oscillatory delta = Berry-Keating R_c corrections at finite height ✅ |
| R(α) pair correlation | 13.2 pt GUE/Poisson separation (10k zeros, 750 bins); peaks at intermediate data density (Good Data Paradox) ✅ |
| P-vector projection via embed_pair (symmetry score) | Does NOT discriminate GUE from Poisson — all \|GUE−Poi\| < 6 pt across all four directions tested |
| P-vector projection via embed_pair (variance ratio) | Poi/GUE variance = 3.3–5.4× across all directions — consistent level-repulsion signal ✅ |
| P-vector projection — actual vs. GUE variance | Act/GUE variance ≈ 0.63 uniformly (preliminary, n=97; needs scale validation) ✅ |

**Key retractions**: ZDTP 98.7% at n=16 on raw positions is non-discriminating (monotone artifact, March 4, 2026). Phase 9A P5 26 pt separation (GUE~52%, Poi~78%) used direct projection — does not replicate under embed_pair (Phase 10C: −5.5 pt, inverted). Method-dependent, not a contradiction.

---

## Completed Phases

---

### Phase 1 — Initial Application (RH-1)
**Date:** March 4, 2026 | **Files:** `rh_experiment_results.json`, `RH_Experiment_Results_Summary.md`

**Dataset:** 1,000 Riemann zeros (mpmath, mp.dps=25). Also: 99 gaps, normalized gaps, random float baseline.

**Key Results:**

| Metric | Dataset | Result |
|---|---|---|
| Chavez conjugation symmetry | Raw zeros (100 pts) | 55.9% (monotone artifact) |
| Chavez conjugation symmetry | Gaps (99 pts) | **83.8%** |
| Chavez conjugation symmetry | Normalized gaps | 79.8% |
| Chavez conjugation symmetry | Random baseline | 0.0% (clean null) |
| ZDTP convergence | Zero positions (16D) | 98.7% → retracted |

**Findings:**
1. Zero gaps score 83.8% — GUE range, consistent with Montgomery-Dyson.
2. Normalization is destructive: drops symmetry 83.8% → 79.8%. Raw gaps carry more structure.
3. Clean random separation (0.0%) confirms the gap signal is structural.
4. ZDTP 98.7% retracted in Phase 2 — monotonicity artifact.

---

### Phase 2 — Control Test (RH-CTRL-1)
**Date:** March 4, 2026 | **Files:** `rh_ctrl_experiment_results.json`, `RH_Phase2_Control_Handoff.md`

**Purpose:** Discriminability test for Phase 1 ZDTP result. Three synthetic controls on first 16 zeros.

**Key Finding:** ZDTP convergence at n=16 is non-discriminating. All monotone sequences score 97–99%. Phase 1 ZDTP figure retracted. Chavez symmetry at n=16 is underpowered (minimum useful n: 50–100). The 83.8% on 99 gaps stands as the meaningful Phase 1 result.

---

### Phase 2b — Gap Discriminability (RH-GAP-1)
**Date:** March 4, 2026 | **Files:** `rh_gap_experiment_results.json`, `RH_Phase2b_Gap_Discriminability_Results.md`

**Purpose:** Does the 83.8% reflect gap ordering, gap distribution, or both? Is it scale-stable?

| Test | Symmetry | Verdict |
|---|---|---|
| Baseline: n=99 (unshuffled) | 83.8% | Reference |
| Shuffle mean (3 trials) | 83.9% | Ordering irrelevant |
| Synthetic Exp(mean=1.41) | 80.1% | Borderline, confounded |
| Scale n=249 gaps | 86.2% | Scale-stable ✅ |

**Key Finding:** Chavez conjugation symmetry is ordering-independent and scale-stable. It measures gap *size distribution*, not sequential arrangement. Cannot detect GUE long-range pair correlations.

---

### Phase 3 — GUE Fingerprint Test (RH-GUE-1)
**Date:** March 4, 2026 | **Files:** `rh_gue_experiment_results.json`, `RH_Phase3_GUE_Results.md`

**Purpose:** Does Chavez symmetry on raw zero gaps detect GUE level repulsion vs. Poisson?

| Sequence | Chavez Symmetry | Δ |
|---|---|---|
| Actual zero gaps (n=99) | 83.4% | baseline |
| Poisson Exp(mean=2.25) | 80.1% | −3.3 pts |
| GUE Wigner surmise (mean=2.25) | 79.4% | −4.0 pts |

**Key Finding:** GUE and Poisson are indistinguishable (0.7 pt separation). The 83.4% detects **lower-bound compactness** — the gap floor at ~0.72 — not GUE eigenvalue statistics. Reframe: apply Chavez to ordering-dependent GUE-specific statistics (spacing ratios, pair correlation).

---

### Phase 4 — Spacing Ratio GUE Test (RH-SR-1)
**Date:** March 4, 2026 | **Files:** `rh_spacing_ratio_results.json`, `RH_Phase4_SpacingRatio_Results.md`

**Purpose:** Apply Chavez to rₙ = min(gₙ, gₙ₊₁)/max(gₙ, gₙ₊₁) — ordering-dependent, GUE-sensitive.

| Sequence | Mean Ratio | Chavez Symmetry | Δ |
|---|---|---|---|
| Actual zero gaps (n=99) | 0.610 | 75.0% | baseline |
| GUE Wigner (mean=2.25) | 0.640 | 76.9% | +1.9 pts |
| Poisson Exp(mean=2.25) | 0.397 | 71.6% | −3.4 pts |

**Key Findings:**
1. Mean ratio 0.610 matches GUE theoretical expectation (~0.60) — direct arithmetic confirmation of Montgomery-Dyson before any transform is applied.
2. **Chavez achieves correct ordering for first time**: GUE > actual > Poisson. 5.3 pt GUE/Poisson separation clears the 5-pt significance threshold.
3. Actual zeros below GUE synthetic — expected in low-height regime.

---

### Phase 5 — Scale and Height Test (RH-SCALE-1)
**Date:** March 5, 2026 | **Files:** `rh_scale_experiment_results.json`, `RH_Phase5_Scale_and_Height_Results.md`

**Part A — Scale:** GUE/Poisson separation widens from 5.3 pts (n=99) to **7.2 pts (n=499)**. Mean ratio rock-stable at 0.610–0.618 across full dataset. Pipeline is not at ceiling.

**Part B — Higher Zeros (500–599):**

| Sequence | Chavez Symmetry |
|---|---|
| Actual zeros 500–599 | **78.3%** |
| GUE Wigner (mean-matched) | 76.8% |
| Poisson Exp (mean-matched) | 71.8% |

Actual zeros **exceed GUE by +1.5 pts** at higher height. Phase 4's −1.9 pt shortfall fully explained by low-height Berry-Keating corrections. Asymptotic GUE convergence confirmed.

---

### Phase 6 — Height Band Survey (RH-HB-1)
**Date:** March 6, 2026 | **Files:** `rh_height_band_results.json`

**Purpose:** Does actual-vs-GUE delta increase monotonically with height? 10 bands of 100 zeros, t~14–1419.

| Band | Height | Actual | GUE | Delta |
|---|---|---|---|---|
| 1 | 14–237 | 75.0% | 76.9% | −1.9 |
| 2 | 238–396 | 77.0% | 76.8% | +0.2 |
| 3 | 398–542 | 73.1% | 76.8% | −3.7 |
| 4 | 544–680 | 74.8% | 76.8% | −2.0 |
| 5 | 682–811 | 73.6% | 76.8% | −3.2 |
| 6 | 812–937 | 78.3% | 76.8% | +1.5 |
| 7 | 940–1063 | 71.4% | 76.8% | **−5.4** |
| 8 | 1064–1184 | 78.2% | 76.8% | +1.4 |
| 9 | 1185–1302 | 77.9% | 76.8% | +1.1 |
| 10 | 1303–1419 | 73.7% | 76.8% | −3.1 |

**Key Findings:**
1. **Monotone convergence hypothesis rejected.** Pattern is oscillatory.
2. GUE synthetic immovably stable at 76.8% across all bands — all variance is in actual zeros.
3. **Berry-Keating connection**: Oscillatory delta is the empirical signature of prime-orbit corrections R_c = Σ cos(log p × t). At t~1000, N_eff ≈ 1.1 — corrections are large and non-averaging. First band-resolution measurement of this regime.
4. Band 7 outlier (delta = −5.4) not documented in any published anomaly catalog.

---

## Phase 7 — Pair Correlation and 24-Element Zero Divisor Projection (RH-PC-1)

**Status:** Queued — next sprint
**Date Designed:** March 8, 2026

### Background: The 24-Element Connection

The Canonical Six generate a **24-element bilateral zero divisor family** (48 signed pairs) in 16D sedenion space — Lean 4 proven. This family is the minimal complete algebraic structure generated by the six framework-independent patterns.

A parallel: in a night session months before formal RH investigation began, Paul Chavez dreamed that the key to the Riemann Hypothesis was **24-dimensional — 24 distinct values of i**. The 24-element bilateral zero divisor family is not 24 dimensions in the conventional sense, but it is 24 algebraically independent annihilation events in 16D sedenion space, each carrying a distinct structural signature. The resonance between the dream and the formally verified algebra is the motivating intuition for Phase 7's second experiment.

The AIEX-001 conjecture (March 3, 2026) proposes that the Hilbert-Pólya operator H has a natural representation in sedenion space via this annihilation structure. Phase 7 pursues the first concrete test of that claim.

### Experiment 7A — Pair Correlation Function (Direct Montgomery-Dyson Test)

**Objective:** Apply Chavez Transform to R(α) — the pair correlation function of Riemann zeros — and compare to GUE theoretical prediction.

Montgomery (1973) proved that for the Riemann zeros, as T→∞:

> R(α) = 1 − (sin πα / πα)² + δ(α)

This is identical to the pair correlation of GUE eigenvalues. Odlyzko's numerical work confirmed it to extraordinary precision. No prior work has applied the Chavez Transform to R(α) itself.

**Protocol:**

1. Compute pair correlation R(α) for first 1,000 zeros at α = 0.1, 0.2, ..., 3.0 (30 values)
2. Apply Chavez Transform to the R(α) sequence
3. Generate GUE synthetic R(α) from Wigner surmise at same α values
4. Generate Poisson R(α) = 1 (no level repulsion) at same α values
5. Apply Chavez Transform to all three
6. Compare: CV, conjugation symmetry, dimensional persistence

**Key Question:** Does Chavez Transform applied to R(α) produce a sharper GUE/Poisson separation than spacing ratios achieved (7.2 pts at n=499)? If R(α) carries the full Montgomery-Dyson structure, the separation should be decisive.

**Expected Results:**
- Actual zeros R(α): high conjugation symmetry reflecting the sinc² oscillation
- GUE synthetic R(α): matches actual — should score near-identically
- Poisson R(α) = flat 1: distinctly lower symmetry (no oscillatory structure)
- GUE/Poisson separation: potentially >> 7.2 pts

**Significance threshold:** 10 pt separation would be compelling. 15+ pts would be definitive.

---

### Experiment 7B — Canonical Six Spectral Projection

**Objective:** Test whether the Canonical Six — the six framework-independent bilateral zero divisor patterns — project onto a 2D spectral structure consistent with known Riemann zero spacing statistics.

This is the AIEX-001 Step 4 — the first concrete attempt at the dimensional reduction:

> **16D sedenion space → Canonical Six (framework-independent) → 2D spectral data**

**Why the Canonical Six first, not the full 24-element family:**

The Canonical Six are the privileged set. They are the only bilateral zero divisors in 16D sedenion space that are framework-independent — working identically in both non-associative Cayley-Dickson and associative/geometric Clifford algebras. The 18 children they generate are Cayley-Dickson-specific and fail in Clifford (norm ≈ √8). If the Hilbert-Pólya operator H is a fundamental mathematical object, it should be built from the most algebraically universal pieces available. The Canonical Six are that.

The 24-element family remains available for Phase 8 if the Canonical Six projection produces a positive or partially positive result — escalating from the minimal sufficient set to the full generated family is the natural next step, not the first one.

**Protocol:**

1. **Enumerate the Canonical Six**: Record all six bilateral zero divisor pairs (P₁,Q₁)...(P₆,Q₆) in 16D basis coordinates. Note: Patterns 18 and 102 share a P-vector index set, yielding 5 distinct P-vector images on the E8 first shell.

2. **Construct the projection matrix**: For each of the six pairs, compute the 16D norm-squared of Pᵢ and Qᵢ. This yields a 6×2 real matrix M (one row per pattern, two columns: ‖Pᵢ‖², ‖Qᵢ‖²).

3. **Derive spectral sequences**: Extract a 1D sequence from M via each of these methods:
   - Row norms: {‖Mᵢ‖} for i = 1..6
   - Eigenvalues of M^T M (2×2 matrix — natural 2D projection)
   - E8 Weyl-orbit-ordered sequence using the 5 distinct P-vector images
   - Color-group-ordered sequence (Color Groups 1, 2, 3 per v1.3)

4. **Apply Chavez Transform** to each derived sequence and to the actual first 6 Riemann zero imaginary parts.

5. **Compare structural fingerprints**: CV, conjugation symmetry, dimensional persistence, and transform values dimension-by-dimension.

6. **Test the key question**: Does any natural projection of the Canonical Six produce Chavez metrics that match the metrics of the first 6 Riemann zeros?

**Secondary test — the 6 zeros directly:**
Apply Chavez Transform to exactly the first 6 Riemann zero imaginary parts. Does the 6-element cardinality — matching the Canonical Six count — produce a qualitatively distinct signal compared to adjacent window sizes (4, 8, 10)?

**What a positive result would mean:**

If a natural projection of the Canonical Six reproduces the spacing statistics of the Riemann zeros — even approximately — it would constitute the first concrete evidence for the AIEX-001 mechanism, built from the most algebraically fundamental pieces. It would establish that the dimensional reduction from 16D sedenion annihilation structure to 2D spectral data is not merely analogical but computational.

This would not be a proof. It would be the discovery of a mechanism worth proving — and worth escalating to the 24-element family in Phase 8.

**What a negative result would mean:**

A null result narrows the search: norm-based and eigenvalue-based projections of the 6-parent structure do not reproduce zero statistics. Next step would be the full 24-element family (Phase 8), or more sophisticated mappings — representation-theoretic, involving the E8 Weyl group action, or via the Color Group tripartite structure.

---

### Phase 7 Deliverables

| File | Purpose |
|---|---|
| `rh_phase7_results.json` | Complete Phase 7 results (7A and 7B) |
| `RH_Phase7_Results.md` | Human-readable results with decision matrix |
| `RH_Phase7_Handoff.md` | Analysis protocol for CAILculator MCP session |
| `rh_pair_correlation.json` | Computed R(α) values for actual zeros |
| `rh_canonical_six.json` | Canonical Six patterns in 16D basis coordinates |
| `rh_phase7_sequences.json` | All synthetic controls and derived sequences |

---

## Theoretical Thread: AIEX-001

The AIEX-001 conjecture (March 3, 2026) runs parallel to the empirical phases. Its formal statement:

> There exists a self-adjoint operator H on a Hilbert space whose spectral decomposition can be naturally represented using the bilateral zero divisor structure of sedenion space, such that the imaginary parts of the nontrivial Riemann zeros appear as eigenvalues of H. The Canonical Six, as the minimal generating set of the 24-element bilateral zero divisor family, provide the algebraic basis. The E8 Weyl orbit structure of their P-vector images supplies the geometric constraint that forces the eigenvalues onto the critical line Re(s) = ½.

**Three pillars:**
1. **Algebraic** — Canonical Six are Lean 4 verified, framework-independent
2. **Geometric** — E8 Weyl orbit is Lean 4 proven; E8 appears in Langlands/L-function research
3. **Empirical** — Montgomery-Dyson: the quantum-prime connection is established; AIEX-001 proposes *where* the quantum system lives

**Critical gap:** No mechanism yet connecting sedenion annihilation events to spectral theory. Experiment 7B is the first attempt to close this gap empirically.

**Why the Canonical Six are the right starting point:**
The Canonical Six are framework-independent — the only bilateral zero divisors that survive both Cayley-Dickson and Clifford algebra settings. Their 5 distinct P-vector images lie on the E8 lattice first shell and form a single Weyl orbit. They are the minimal sufficient algebraic structure. If H is a universal operator, it should emerge from universal pieces. The 24-element family they generate is the natural escalation if the 6-parent projection succeeds.

**On the "24 values of i" intuition (March 2026):**
A formative research dream suggested the key to RH was 24-dimensional. The 24-element bilateral zero divisor family is the algebraically natural candidate — but the Canonical Six, as the framework-independent generating set, are the more fundamental starting point. The 24-element family may still be the right space for the operator to act *on* or *through*, with the Canonical Six as the basis for constructing H. Investigation proceeds from the more privileged set first.

---

## Cumulative Findings Summary

| Phase | Key Result | Status |
|---|---|---|
| 1 | Zero gaps score 83.8% Chavez symmetry; ZDTP at n=16 non-discriminating | Complete |
| 2 | ZDTP 98.7% retracted; 83.8% on gaps confirmed as meaningful signal | Complete |
| 2b | Ordering-independent; scale-stable (86.2% at n=249); lower-bound compactness | Complete |
| 3 | GUE and Poisson indistinguishable on raw gaps; reframe to ordering-dependent statistics | Complete |
| 4 | **First correct GUE ordering**: spacing ratios give 5.3 pt separation; mean ratio 0.610 = GUE fingerprint | Complete |
| 5 | Separation widens to 7.2 pts at n=499; asymptotic GUE convergence confirmed | Complete |
| 6 | Oscillatory band pattern = Berry-Keating R_c corrections; Band 7 anomaly undocumented | Complete |
| 7 | GUE R(α) = 96.7% (Fibonacci-level); 1D invariance theorem: all 6 patterns identical; empirical zeros 93.1%; −5.1 pt delta consistent across all patterns | Complete |
| 8 | 1D invariance theorem confirmed encoding-independent; R(α) fine-grid 12.5 pt separation (new record); systematic negative delta (actual < GUE) confirmed across 3 experiments | Complete |
| 9 | P5 anomaly resolved (not Riemann-specific; bilateral zeros measure projection oscillation); R(α) n=300 = 14.7 pt record; n=750 spurious (sparse bins, needs 10k zeros); Berry-Keating r=0.35 p=0.325 (p=2 term only) | Complete |
| 10 | R(α) 10k zeros 750 bins 13.20 pt separation — Good Data Paradox. No P-vector discriminates via conjugation symmetry; variance ratio Poi/GUE = 3.3–5.4× all directions; Act/GUE variance ≈ 0.63 uniformly (preliminary). | Complete |
| 11 | Poi/GUE variance stable n=97→998; BK r=0.6569 SIGNIFICANT (9-prime model); P3 antipodal confirmed; actual P2 skewness=−1.42 (see Phase 15B for measurement clarification) | Complete |
| 12A | Act/GUE variance height-dependent (not asymptote): 0.651→0.756→0.665; remains <1.0 at all heights | Complete |
| 12B | Skewness −1.42 confirmed genuine (not transform artifact); root cause: P2 amplifies right-skewed gap distributions | Complete |
| 12C | BK r=0.5793 corrected (Phase 11B unweighted cosines error); peaks at p=23, declines for p≥29 | Complete |
| 13A | **Log-prime signal: SNR 7–245x at p=3..23; GUE/Poisson/shuffled flat (max SNR~2.2)** | Complete |
| 13B/C/D | Per-band BK tests: null. Frequency presence ≠ phase coherence | Complete |
| 14A | Actual > GUE all 20 bands, mean Δ=+2.59 pp, p<<0.001, height-independent | Complete |
| 14B | SR/P2 complementarity; p=11 crossover; antipodal isometry (⚠️ see 15A: this is a theorem, not empirical finding) | Complete |
| 14C | Color Group hypothesis violated; P1 = spectral bridge (⚠️ see 15D: revised to high-pass cluster) | Complete |
| 15C | Framework-independence is Q-vector property; embed_pair only probes P-vector geometry; E8 Weyl orbit is operative structure | Complete |
| 15D | **Weyl orbit = orthogonal frame** (all norms √2, all pairs 90° except antipodal 180°); spectral split: {v1,v2,v3,v4} high-pass cluster vs {v5} low-pass outlier; P1 bridge claim corrected | Complete |
| 15A | Antipodal isometry is a THEOREM (v3=−v2 → universal, not zero-specific); log-prime signal re-confirmed zero-specific; Route C eliminated, Route B favored | Complete |
| 15B | P2 projection skewness height-invariant (CV=0.096) but not zero-specific (GUE delta=−0.014, indistinguishable) | Complete |
| 16A | L-function sample size diagnosis (mpmath underpowered); python-flint 100× speed discovery | Complete |
| 16B | **Route B CONFIRMED:** p=2 chi4 suppressed 353×, p=3 chi3 suppressed 736×; Route C ELIMINATED | Complete |
| 17A-i | **q2 (e5+e10): 9/9 primes, SNR 418–1762×; p=2 first-ever detection at SNR=418.7** | Complete |
| 17A-ii | q4 (e3-e12): 8/9 primes, SNR up to 1995×; ultra-low-pass filter (p=23 below threshold) | Complete |
| 17A-iii | q3=−v1 isometry confirmed exact (max deviation 0.00e+00); machine-exact algebraic theorem | Complete |
| 17B-i | Q2: p=2 chi4 suppressed 4652×, p=3 chi3 suppressed 6723× (10–14× stronger than SR). chi3/zeta≈1.0 unexpected open thread | Complete |
| 17B-i | Q4: p=2 chi4 suppressed ~10,000× (strongest suppression observed). Q-vectors outperform P-vectors in Route B signal | Complete |
| 17B-ii | Sedenion bilateral verification: all 6 patterns P*Q=0.00e+00 exact; three-gap Act/GUE=1.020 (contrast: two-gap 0.65) | Complete |

---

## Open Questions Driving Future Phases

**Resolved through Phase 10:**
1. ✅ Pair correlation R(α) — 13.2 pt GUE/Poisson separation confirmed at 10k zeros, 750 bins.
2. ✅ 1D invariance theorem — encoding-independent; all 6 Canonical Six patterns identical for 1D real arrays.
3. ✅ Systematic negative delta — confirmed across multiple experiments; Berry-Keating R_c mechanism.
4. ✅ P-vector discrimination via conjugation symmetry — negative result: none of P1/P2/P4/P5 discriminate.
5. ✅ Variance as discrimination signal — Poi/GUE variance ratio 3.3–5.4× all embed_pair directions.

**Active open questions (driving Phases 11–20):**
1. **Act/GUE variance ≈ 0.63 at scale**: Preliminary finding from n=97 gap pairs. Does it hold at n=499, n=999? If stable, it's a quantitative refinement of Montgomery-Dyson.
2. **Act/GUE variance height dependence**: Does the 0.63 ratio oscillate with height like the symmetry score does (Berry-Keating signature), or is it height-independent?
3. **Berry-Keating significance threshold**: r=+0.543 at n=10 bands with 7-term model. Adding p=13,17 — can we reach r>0.632?
4. **P3 direction (antipodal to P2)**: v3 = (0,0,0,−1,1,0,0,0) untested. As the antipodal of P2, does it mirror P2's results exactly, or does the Weyl reflection produce a different discrimination geometry?
5. **Optimal R(α) density**: Good Data Paradox shows separation peaks at intermediate density. What is the optimal (N_zeros, n_bins) pair?
6. **AIEX-001 mechanism**: No constructive path established yet. 1D invariance is a hard constraint — scalar projection is insufficient. Vector-valued sedenion representation required. Is there a first concrete step?
7. **Annihilation topology AT-1**: Type I/II classification of all 84 zero divisor pairs. Required before ZDTP Chess Version B experiment (Experiment 2.3).

---

---

## Phase 11 — Scale Validation, Berry-Keating Extension, and P3 Direction (CONCRETE)

**Date designed:** March 9, 2026 | **Estimated duration:** 1–2 sessions

Three independent sub-experiments, all using existing data files (no new computation required).

---

### Phase 11A — Act/GUE Variance at Scale

**Question:** Does Act/GUE variance ≈ 0.63 hold at n=499 and n=999 gap pairs, or is it a small-sample feature of the low-height regime?

**Protocol:**
1. Take first 500 Riemann zero gaps from `rh_gaps.json` (zeros 1–500, t~14–811)
2. Generate 499 consecutive gap pairs; apply embed_pair transformation
3. Project onto P1, P2, P4, P5; compute variance for actual, GUE (3 seeds, mean-matched), Poisson (3 seeds, mean-matched)
4. Compute Act/GUE variance ratio for each direction
5. Repeat for n=999 gap pairs (zeros 1–1000)

**Decision criteria:**
- Ratio stable at 0.60–0.68 across both scales → preliminary finding confirmed; add to paper as established result
- Ratio drifts toward 1.0 at larger n → low-height artifact; retire the finding
- Ratio oscillates with height → Berry-Keating connection; design dedicated height-band study (Phase 12)

**Files:** `p11a_variance_scale.json`, `RH_Phase11A_Results.md`

---

### Phase 11B — Berry-Keating Extended to p=13, 17

**Question:** Does adding p=13 and p=17 to the 5-prime + prime-squares model push the Pearson r above the significance threshold r>0.632 at n=10 bands?

**Protocol:** Existing 10-band delta values from `rh_phase10a_definitive.json`. Extend R_c model:

R_c(t) = (1/√2)cos(log 2·t) + (1/√3)cos(log 3·t) + (1/√5)cos(log 5·t) + (1/√7)cos(log 7·t) + (1/√11)cos(log 11·t) + (1/√13)cos(log 13·t) + (1/√17)cos(log 17·t) + 0.5·cos(log 4·t) + (1/3)·cos(log 9·t)

Compute R_c at each band midpoint t̄; Pearson r against actual band deltas.

**Decision criteria:**
- r>0.632 → significant; Berry-Keating confirmed as the mechanism; update paper Section 7.4
- r<0.632 but trend continuing → extend to p=19,23 in Phase 12
- r declining → model is overfitting; investigate multi-prime interference

**Files:** `p11b_bk_extended.json`, `RH_Phase11B_Results.md`

---

### Phase 11C — P3 Direction (Missing Canonical Six Vector)

**Question:** What does the antipodal P-vector v3 = (0,0,0,−1,1,0,0,0) produce on the embed_pair projection? Does the Weyl antipodal relationship to v2 mirror P2's results?

**Context:** P3 is the only Canonical Six P-vector direction not yet tested. It is antipodal to P2 (v2+v3=0, connected by simple Weyl reflection α₄). Algebraically it belongs to Color Group 3 alone, while P2 and P5 share Color Group 2.

**Protocol:** Same as Phase 10C — 97 gap pairs, embed_pair, project onto P3, run detect_patterns for actual, GUE (3 seeds), Poisson (3 seeds). Compute symmetry score and variance.

**Decision criteria:**
- P3 mirrors P2 exactly → Weyl reflection produces symmetric result; confirms Color Group geometry
- P3 differs from P2 → antipodal relationship breaks the discrimination geometry; Color Group 3 has distinct behavior
- P3 mirrors P4 (same Weyl orbit but different color group) → orbit structure dominates over color group

**Files:** `p11c_p3_projection.json`, `RH_Phase11C_Results.md`

---

### Phase 11 Deliverables

| File | Purpose |
|---|---|
| `p11a_variance_scale.json` | Act/GUE variance ratio at n=499, n=999 |
| `p11b_bk_extended.json` | Berry-Keating r with p=13,17 added |
| `p11c_p3_projection.json` | P3 direction embed_pair results |
| `RH_Phase11_Results.md` | Combined Phase 11 results |

---

## Phases 12–20 — Sketch

These are directional, not fixed. Each phase will be fully designed after Phase 11 results are in hand.

**Standing antipodal tracking instruction (all phases through 18):** Each phase includes an antipodal component — measuring skewness, kurtosis, and distributional shape of P2/P3 projection values at each new scale, height, or dataset. The goal is to build a complete characterization of the P2/P3 antipodal axis across all experimental conditions heading into Phase 18's theoretical treatment.

---

**Phase 12 — Height Dependence of Act/GUE Variance Ratio and Antipodal Skewness**

*Depends on:* Phase 11A result. If Act/GUE ≈ 0.63 is stable at n=999, investigate whether it varies across height bands (using 10k zero dataset). Does the variance ratio oscillate like the spacing ratio delta does, or is it height-independent?

*Antipodal component:* At each height band, compute skewness of the P2/P3 projection values for actual zeros. Phase 11D established that at t~14–237 (n=97), actual P2 skew = −1.42 vs. GUE mean skew = −0.45. Does the skewness change with height? If it tracks the Berry-Keating oscillation, the antipodal axis is carrying oscillatory R_c information. If it's height-independent, it's a structural property of the zero distribution at all heights.

---

**Phase 13 — Optimal R(α) Bin Density**

*Depends on:* Good Data Paradox finding (Phase 10B). Systematic study: fix N=1,000 zeros, vary bin count from 50 to 500 to find the separation maximum. Then vary N at the optimal bin count. Map the (N, n_bins) surface.

*Antipodal component:* At the optimal density, compute R(α) separately for P2-projected and P3-projected zero pairs. Since proj_P3 = −proj_P2, R(α) on P3 is R(α) on the sign-reversed P2 sequence. Do the pair correlations differ? Any asymmetry between P2-R(α) and P3-R(α) would signal that the pair correlation function is sensitive to the sign structure of the projection — a finding with direct implications for the antipodal bilateral symmetry thread.

---

**Phase 14 — Berry-Keating Significance Push (if needed)**

*Depends on:* Phase 11B result. If r ≥ 0.632 confirmed with p=13,17,19,23 (pre-computation suggests yes), this phase records the definitive model, updates paper Section 7.4, and closes the BK arc. If r < 0.632, extend to p=29,31.

*Antipodal component:* For each height band in the BK study, record the P2/P3 skewness alongside the spacing ratio delta and R_c value. Test whether skewness correlates with R_c: if prime-orbit corrections drive both the spacing ratio oscillation AND the antipodal skewness, the correlation would link the two measurement axes.

---

**Phase 15 — Weyl Orbit Structure and Mechanistic Routes — COMPLETE (March 9, 2026)**

*15C: Framework-dependent pattern comparison*
- Framework-independence lives in Q-vector; embed_pair only probes P-vector. Every CD-specific pattern shares its P-vector with a Canonical Six pattern → numerically identical results. The operative algebraic structure is E8 P-vector geometry.
- Antipodal structure is a property of E8 geometry, independent of framework classification.
- To probe canonical vs non-canonical distinction: multi-channel embed or direct sedenion multiplication needed (Phase 17+).

*15D: P1 spectral bridge characterization*
- **Major geometric finding:** All five P-vectors have norm √2. All pairwise angles = 90° exactly, except v2/v3 = 180° (antipodal). The Weyl orbit P-vectors form a near-orthogonal frame (coordinate system) in 8D.
- **Spectral split:** {v1,v2,v3,v4} = high-pass dominant cluster (r≥0.95 pairwise; SNR peaks 114–351 at p=7..23). {v5} = low-pass outlier (r≈0.08 vs cluster; peaks at p=3,5,7). P5 is the genuine spectral complement, not P2.
- **Correction to Phase 14C:** P1 is not uniquely the spectral bridge — P1/P2/P3/P5 all detect 9/9 primes. P1 = highest-SNR member of high-pass cluster.
- r(P2,P3)=1.000 exactly: algebraic theorem, not empirical finding.

*15A: Antipodal isometry scope test*
- **Major correction to Phase 14B:** The isometry |DFT(P3)|²=|DFT(P2)|² is a mathematical theorem (v3=−v2 → proj_P3=−proj_P2 → DFT linearity → powers equal). Holds for ANY sequence. Deviation = exactly 0 for actual zeros, GUE, Poisson, and shuffled alike. Phase 14B's observation was correct; the zero-specific interpretation was wrong.
- **Route determination:** Log-prime signal re-confirmed zero-specific (actual SNR 7.6–245; GUE max 1.9; Poisson max 1.4). Route C (GUE as mechanism) effectively eliminated for log-prime signal. Route B (explicit formula/prime orbits) strongly favored.

*15B: Antipodal skewness at scale and height*
- P2 projection (embed_pair dot v2) skewness: grand mean = +0.557, CV=0.096 across 10 height bands — **height-invariant**. All 10 bands positive. Mean value locked at −0.322±0.001 across entire height range.
- **NOT zero-specific:** GUE grand mean = +0.571; delta = −0.014 (within 1 GUE std). Skewness is a level-repulsion property shared with GUE, not a Riemann-zero-specific signal.
- No BK oscillation in skewness (r=0.37, sub-threshold).
- Phase 11D skewness=−1.42 is a different measurement (distinct projection method); both valid. Paper must distinguish them.

*Phase 15 corrections required in paper:*
1. Phase 14B antipodal isometry → reframe as theorem, not empirical finding
2. Phase 14C P1 spectral bridge → reframe as high-pass cluster property
3. Phase 11D skewness=−1.42 → clarify which projection method vs Phase 15B's +0.557

Files: `p15c_framework_dependent.json`, `p15d_p1_bridge.json`, `p15b_skewness_height.json`

---

**Phase 16 — L-function Comparative Study — COMPLETE (March 10, 2026)**

*16A: Sample size diagnosis (underpowered baseline)*
- Initial computation (mpmath): 132 chi_4 zeros + 117 chi_3 zeros to t=200 (~10ms/eval). All SNRs at noise floor — underpowered. Minimum N identified: ~400 zeros per L-function. RH signal emergence threshold: N≥200.
- **Key discovery:** python-flint `acb.dirichlet_l()` evaluates at 0.1ms/call (100× faster than mpmath), enabling full-scale computation in ~80 seconds.

*16B: Definitive test*
- **Dataset:** 2,092 chi_4 zeros + 1,893 chi_3 zeros to t=2000 (Hardy Z-function sign-change + bisection via python-flint). Files: `zeros_chi4_2k.json`, `zeros_chi3_2k.json`.
- **Ramified prime suppression (core test):**
  - p=2 in chi_4 (chi_4(2)=0 → absent from Euler product): SNR=0.11, **353× suppressed** vs RH ✓
  - p=3 in chi_3 (chi_3(3)=0 → absent from Euler product): SNR=0.09, **736× suppressed** vs RH ✓
  - All unramified primes (p=3,7,11,13,17,19,23 in chi_4; p=2,5,7,11,13,17,19,23 in chi_3): elevated SNR, 7/8 each above threshold
- **Route B: CONFIRMED.** Detected primes = unramified primes of each L-function's Euler product. No free parameters.
- **Route C: ELIMINATED.** chi_3, chi_4, ζ all have unitary Katz-Sarnak symmetry class. Any difference in detected prime sets is arithmetic by construction. GUE synthetics show no log-prime signal (Phases 13A/15A).
- *Loose thread:* p=5 in chi_4: SNR=2.7, flat N=500–2092. chi_4(5)=+1, so p=5 IS in Euler product — likely needs N>3000. Does not affect route determination.
- Files: `p16_lfunction_comparison.json`, `zeros_chi4_2k.json`, `zeros_chi3_2k.json`

---

**Phase 17 — Q-Vector Access: Multi-Channel Embedding — COMPLETE (March 12, 2026)**

Files: `rh_phase17a_prep.py`, `rh_phase17b_prep.py`, `p17a_results.json`, `p17b_results.json`, `RH_Phase17_Results.md`, `RH_Phase17_Handoff.md`

*17A — Q-vector DFT survey (zeta zeros, 10k):*

**q2 projection** (e5+e10 → 8D image (0,0,−1,0,0,+1,0,0)):
- **9/9 primes detected, SNR 418–1762×** — first single projection to detect all 9 primes p=2..23
- **p=2 detected at SNR=418.7** — first p=2 detection in any projection (absent from all P-vector phases 13A, 14B, 15D)
- Mechanism: q2·embed_pair = g2−g1+g1/(g1+g2) (asymmetric). All P-vector projections were symmetric or high-pass filtered in ways that cancelled the p=2 contribution.
- Sequence: mean=0.499, range=[−2.27, 3.05], asymmetric (unlike all P-vectors)

**q4 projection** (e3−e12 → 8D image (0,0,0,+1,+1,0,0,0)):
- **8/9 primes detected (p=23 just below threshold), SNR up to 1995×**
- Ultra-low-pass filter: SNR decays exponentially from p=2 (SNR=1796.9) to p=19 (SNR=4.1)
- Algebraic identity: q4·embed_pair = H/2+A (positive complement of P2 = H/2−A); q4+P2 = H (harmonic mean)
- Sequence: mean=1.429, always positive

**q3 isometry** (q3=−v1):
- Max deviation |DFT(q3)|²−|DFT(v1)|²: 0.00e+00 (machine exact) — algebraic theorem confirmed

Q-vector SNR vs P-vector SNR: Best P-vector peak = 245× (Phase 13A, P2). Best Q-vector peak = 1995× (q4, p=3). Median SNR improvement: 5–7×.

*17B-i — L-function comparative Q-projection:*

| Direction | p=2 chi4/zeta | p=3 chi3/zeta | Interpretation |
|-----------|--------------|--------------|----------------|
| SR (Phase 16B) | 0.0029 (353×) | 0.0014 (736×) | baseline |
| q2 (Phase 17) | 0.0002 (4652×) | 0.0001 (6723×) | 10× stronger Route B |
| q4 (Phase 17) | 0.0001 (~10,000×) | 0.0004 (~2500×) | 14× stronger Route B |

Route B confirmed more decisively via Q-vectors. Q-vectors encode Euler product arithmetic with higher sensitivity than P-vectors.

**Unexpected: chi3/zeta ≈ 1.0 for Q2 unramified primes (p=5..23, ratio 0.90–1.05).** Chi4/zeta ≈ 0.23. Chi3 zeros carry nearly identical Q2 SNR as zeta zeros. Candidate: chi3 has conductor 3 (minimal odd prime), giving it a special relationship with the e5+e10 Q-vector direction. **Open thread → Phase 18.**

*17B-ii — Sedenion bilateral zero divisor verification:*
- All 6 patterns: ||P*Q|| = 0.00e+00 (exact machine zero) — re-verification of Lean 4 proof
- Three-gap formula derived analytically: scalar_part(x_n * x_{n+1}) = −2·g_{n+1}·(g_n+g_{n+2})
- Three-gap Act/GUE variance ratio = **1.020** (no discrimination); Poi/GUE = 4.472
- Contrast with two-gap Act/GUE ≈ 0.65. Layer structure revealed: zeros match GUE in three-gap correlations but are tighter in two-gap correlations. The bilateral product structure exposes this.

---

**Phase 18 — AIEX-001 Structural Exploration + Open Thread Resolution**

*Depends on:* Phases 15, 16, 17 complete. The Phase 17 picture sharpens the AIEX-001 target substantially. Q-vectors carry arithmetic structure with higher SNR than P-vectors; the full bilateral zero divisor pair (P,Q) — not just the P-projection — reads the Euler product. Three new open threads from Phase 17 drive the Phase 18 agenda.

**18A — chi3/zeta ≈ 1.0 for Q2: Character Structure in Q-Vector Projection**

Phase 17 showed chi3/zeta Q2 ratio ≈ 0.90–1.05 for all unramified primes, while chi4/zeta ≈ 0.23. This asymmetry is not predicted by Route B alone (Route B only predicts which primes are suppressed, not the ratio of unramified prime SNRs across L-functions). Candidate investigations:

1. **Conductor asymmetry test:** Compute Q2 and Q4 projections for chi_8 (conductor 8), chi_5 (conductor 5), chi_7 (conductor 7) zeros. If chi3's unique behavior traces to conductor=3 (minimal odd prime), other small-conductor L-functions should show intermediate behavior. Prediction: chi_5 and chi_7 will show chi/zeta ratios between 0.23 and 1.0 for Q2.

2. **Character table correlation:** For each character chi, tabulate chi(p) values at p=2,3,5,...,23. Check whether the chi/zeta SNR ratio at prime p correlates with |chi(p)|² across all computed L-functions. Route B predicts full suppression when chi(p)=0; Q2 asymmetry would imply the SNR ratio also encodes |chi(p)| for unramified primes.

3. **Q4 profile comparison:** chi3/zeta for Q4 is 0.235–0.290 (not ≈1.0 like Q2). The chi3/Q2 anomaly is projection-specific. This constrains the mechanism to something about q2=(0,0,-1,0,0,+1,0,0) in particular — the e5-e10 direction in 8D space.

**18B — Three-Gap Layer Structure: Why Does Act/GUE Shift from 0.65 to 1.02?**

Phase 17B-ii established a new empirical fact: the bilateral sedenion product naturally generates the three-gap statistic s_n = g_{n+1}(g_n+g_{n+2}), and for this statistic Act/GUE variance = 1.02 (matching GUE), whereas the two-gap variance ratio is consistently 0.65 (actual tighter than GUE). This is a multi-scale structure in the zero correlations that the bilateral product reveals.

Investigations:
1. **Analytic connection to GUE form factor:** The 3-point form factor of GUE is a known quantity in random matrix theory. Check whether Act/GUE = 1.02 for three-gap statistics is consistent with the theoretical 3-point form factor at the relevant scale. If yes, this is a direct RMT validation; if no, it constrains the mechanism.
2. **n-gap generalization:** Define s_n^(k) involving k consecutive gaps. At what k does the Act/GUE variance ratio transition from <1 to ≈1? The transition scale carries information about the correlation length in the zero sequence.
3. **Vector part of sedenion product:** The three-gap statistic came from the *scalar part* of x_n·x_{n+1}. The *vector part* is 15 unexplored components — each a bilinear function of consecutive gap triples, structure determined by the sedenion multiplication table. Extract and compute Act/GUE for each component against actual zeros vs GUE/Poisson. The sedenion product is already implemented in `rh_phase17b_prep.py`; this requires only indexing beyond component 0.

**18C — AIEX-001 Operator Construction: Q-Vector Component**

Phase 17 shows the full bilateral pair (P,Q) reads the Euler product — not just the P-projection. This updates the AIEX-001 target:
- Prior: H should be built from P-vector geometry (E8 Weyl orbit)
- Revised: H should incorporate both P and Q components of the bilateral zero divisor pairs

Structural questions:
1. Can the embed_pair kernel be understood as a discretization of a prime-orbit operator? The P-projection gives high-pass (p≥7) and Q-projection gives broadband (p=2..23) channels — this is a filter bank.
2. Does the P/Q split correspond to a known decomposition in the explicit formula? E.g., short vs long prime orbits, ramified vs unramified contributions?
3. The v2+v3=0 antipodal constraint: operator-theoretic interpretation connecting to self-adjointness of H? The functional equation pairs zeros ρ ↔ 1−ρ̄, which is also a bilateral pairing.
4. **NEW from Phase 17:** The chi3/zeta ≈ 1.0 anomaly in Q2 — could this encode L-function character structure in a way that gives a representation-theoretic interpretation of the bilateral zero divisor action? The Q2 direction seems to "know" about chi3 specifically.

**18E — E8 Geometry: Gram Matrix, Orthogonality, and Subspace Analysis**

New geometric observations from the E8 implications analysis (see `RH_Phase17_E8_Implications.md`) that require formal computation and Lean 4 verification:

1. **Gram matrix of the 8-root set:** Compute all 28 pairwise inner products of { ±(e2−e7), ±(e4−e5), e2+e7, ±(e3−e6), e4+e5 }. The full Gram matrix determines whether this is a named root subsystem of E8 (A₁⁴, D₄, or other). Several inner products are already known to be 0 or ±2 from inspection; the full matrix settles the sub-structure question. This is a half-hour calculation and Phase 18's first concrete deliverable.

2. **P⊥Q orthogonality:** Every bilateral pair (Pᵢ,Qᵢ) has orthogonal 8D projections (verified for all 6 patterns by direct inner product). This is independent of, and in addition to, the 16D algebraic annihilation P·Q=0. Whether these two zero conditions are connected by a theorem is the **second primary Lean 4 target** for Phase 18 (after the Weyl reflection conjecture).

3. **6D subspace expansion:** P-vectors span a 4D subspace (v3=−v2 reduces rank). Q-vectors q2 and q4 are provably outside this span, expanding coverage to 6D. Lean 4 target: rank computation from the coordinate matrix. Direct consequence for AIEX-001: H cannot be fully represented using P-vector geometry alone; the Q-vectors add two new independent dimensions of arithmetic coverage.

4. **Spectral filter rule analytic derivation:** Prove formally that difference roots (eᵢ−eⱼ) give high-pass filter character and sum roots (eᵢ+eⱼ) give low-pass filter character, by expanding the embed_pair projection for each root type and analyzing the resulting DFT frequency response. If successful, this unifies the Phase 15D P-vector spectral split and the Phase 17 Q-vector results into a single theorem about E8 root geometry and prime spectral content.

**18F — Framework-Independence Empirical Probe**

Phase 15C showed the canonical/non-canonical distinction is invisible to P-vector projections because all framework-dependent patterns share P-vectors with Canonical Six patterns. The conclusion: probing framework-independence requires Q-vector access. Phase 17 delivers that access.

Apply Q-vector projections to gap sequences using framework-dependent patterns' Q-vectors as projection directions. Compare log-prime DFT SNR profiles against Canonical Six Q-projections. A positive result — different SNR profiles for framework-dependent Q-vectors — would be the **first empirical probe of framework-independence itself**, directly measuring the canonical/non-canonical distinction experimentally.

The E8 geometry analysis (18E) should precede this: the Gram matrix and subspace structure will identify which framework-dependent Q-vectors are most geometrically distinct from Canonical Six Q-vectors, informing which directions to probe first.

**18D — Paper Integration**

Phase 17 results for paper (Section 8 extension or Section 9 new):
- Q-vector SNR superiority (5–7× over P-vectors)
- First p=2 detection in single projection (q2 broadband)
- Route B re-confirmed via Q-vectors with 10–14× stronger suppression ratios
- chi3/zeta ≈ 1.0 anomaly (flag as open question)
- Three-gap Act/GUE = 1.02 layer structure

**Seeded theoretical thread — Antipodal Bilateral Symmetry:** The isometry is universal/trivial (Phase 15A), but the geometric structure — orthogonal frame with one antipodal pair — is the non-trivial object. The question is whether the breaking of the orthogonal frame at the antipodal pair has an operator-theoretic meaning connected to the functional equation (which also pairs zeros via ρ ↔ 1−ρ̄). This thread now has a Q-vector complement: are any Q-vectors mutually antipodal?

---

**Phase 19 — Annihilation Topology AT-1**

*Depends on:* Review of Biss-Dugger-Isaksen. Classify all 84 sedenion zero divisor pairs as Type I (instant) or Type II (delayed). Test: Type I → 6 Canonical Six parents; Type II → 18 children.

---

**Phase 20+ — Paper Finalization and Beyond**

*Note: This roadmap is open-ended. Given the trajectory of the investigation — each phase consistently opening new threads — additional phases beyond 20 are expected. Phase 20 marks a natural paper consolidation point, not a terminus.*

*Depends on:* Phases 16–19 sufficiently resolved. Key decisions:
1. Incorporate Phase 15 corrections (antipodal isometry, P1 bridge, skewness clarification)
2. **Incorporate Phase 16 results:** Route B confirmed; ramified prime suppression (353× for p=2/chi_4, 736× for p=3/chi_3); log-prime signal encodes Euler product structure. Section 8 (new) or Section 7.6.
3. **Incorporate Phase 17 results:** Q-vector SNR superiority (5–7×); first p=2 detection in single projection; Route B re-confirmed with 10–14× stronger suppression; chi3/zeta≈1.0 anomaly; three-gap layer structure.
4. Update Section 7 with all Phase 11–17 findings
5. Write AIEX-001 status section based on Phase 18 theoretical work
6. Submit to *Experimental Mathematics*

**Phase 16 contribution to paper:** Ramified prime suppression (353–736×) is clean and publishable independent of broader sedenion/AIEX-001 story. Route B confirmed, Route C eliminated.

**Phase 17 contribution to paper:** Q-vector access is a new result at two levels: (1) practical — q2 is the first single projection to detect all 9 primes p=2..23 with SNR>100×; (2) structural — the chi3/zeta≈1.0 Q2 anomaly and three-gap Act/GUE=1.02 layer structure are new findings about the arithmetic of L-function zeros.

**Phase 17 E8 implications contribution to paper:** The geometric observations in `RH_Phase17_E8_Implications.md` extend the v1.3 E8 results: all Q-vector 8D images lie on the E8 first shell; the bilateral pairs are geometrically orthogonal; the P+Q set spans 6D vs P-only 4D; the root-type→spectral-character rule unifies Phases 15D and 17. These are paper-ready once Lean 4 verification is complete (Phase 18E).

---

## Connection to Chavez Transform Paper

The paper draft (`ChavezTransform_Paper_Draft.md`) is current through Phase 10. Sections added in subsequent sprints:
- **Section 6.5** — P-Vector Projection: variance ratio discriminates (3.3–5.4×); symmetry score does not
- **Section 7.5** — Preliminary finding: Act/GUE variance ≈ 0.65 across all four P-vector directions (n=97, marked preliminary)
- **Section 7.6** — Log-prime DFT signal (Phases 13A, 15A, 16B): SNR 7–245× for primes 3–23; GUE synthetics show no signal; signal encodes Euler product structure (Phase 16B confirmed)
- **Section 8** (new) — L-function comparative study: ramified prime suppression 353× (p=2/chi_4) and 736× (p=3/chi_3); Route B confirmed; Route C eliminated
- **Section 9.2** — Sensitivity table updated with P-vector rows and log-prime DFT row
- **Section 9.3** — Act/GUE scale validation added as open question

**Phase 16 is paper-ready.** The ramified prime test is a clean, self-contained result: no threshold sensitivity, no parameter tuning, 300–700× suppression at the predicted primes. Suitable for publication independent of the broader AIEX-001 story.

---

*This is a living document. Update after each completed phase.*

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
