# Phase 31 Pre-Handoff Document
**RH Investigation — Chavez AI Labs LLC**
*Prepared: 2026-03-27 | Claude Desktop + KSJ-MCP*
*Handoff to: Claude Code (Phase 31 script generation)*

---

## Status Going In

| Item | Status |
|------|--------|
| KSJ captures | 100 (AIEX-001 through AIEX-099 + RC-001) |
| Phase 30 closed | Track 2 (ZDTP leakage) ✓ · Track 3 (asymptote) open |
| Open questions logged | 17 |
| Key insights logged | 68 |
| Canonical Six v1.4 target | April 1 (Sophie Germain's 250th birthday) |

---

## What Phase 30 Established

### Confirmed (carry forward as foundations)

**1. Isometry pinning — prime-by-prime, zero leakage**
ZDTP full-cascade and individual S1 transmission confirmed that p∈{5,7,11} each preserves its norm exactly through 32D and 64D expansion. Input norms [0.9984, 0.9974, 0.9962] are preserved to full double precision, no cross-slot contamination. Convergence score 0.9762 across all 6 Canonical Six gateways. *(AIEX-086, AIEX-087)*

**2. {2,3,13} is structurally distinct**
The decay sub-vector occupies a 4× lower-magnitude basin in 64D vs the {5,7,11} isometry sub-vector (0.495 vs 1.997 at leading component). Both transmit losslessly, but they are not in the same geometric home. *(AIEX-088)*

**3. c₁ beats 1/2π as asymptote**
Fixed-c curve fitting: SSE_A (c₁=0.118) = 0.000642, SSE_B (1/2π=0.159) = 0.000929. Ratio 1.45×. c₁ is the preferred floor within the current dataset. *(AIEX-093)*

**4. GUE overlap is ruled out as the origin of c₁**
Zero-based overlap converges to 1.0 (not c₁). Grid-based diverges. c₁ is a discrete residual property of the zeros, not a spectral density effect. *(AIEX-089)*

**5. c₁² + c₃² = 1.0 exactly**
Verified to 16 decimal places. Suggests a unitarity constraint in the Weil explicit formula — candidate for a structural theorem. *(AIEX-091)*

**6. Weil ratio is monotone decreasing, does not converge to 1/4**
Sequence from p_max=13 to p_max=151: 0.2479 → 0.1736. Best analytic fit: vs log(p_max), R²=0.936, slope −0.0326. The 1/log(p_max) limit estimate ~0.110 is close to c₁=0.118. *(AIEX-090)*

### Open / Underdetermined (Phase 31 must resolve)

- **Asymptote floor:** SSE landscape is monotonically decreasing — 9 data points spanning n_primes 6→36 cannot distinguish c₁ from 0.10 or 0.14. Dataset underdetermined. Free-fit collapses to degenerate solution. *(AIEX-094, AIEX-095)*
- **Decay exponent:** b = 0.42 at c₁ floor. Not a square-root law. b = 0.5 implies c ≈ 0.140 — a value between both candidates with no known identity. *(AIEX-096)*
- **p=11 sign asymmetry:** Slots 50/61 ±paired in 64D vs purely positive for p=5 and p=7. Single observation. Not yet a structural claim. *(AIEX-099)*
- **Sedenion Horizon Conjecture:** Four component claims at different evidential levels. Cannot be called a theorem until Phase 31 extends the prime set. *(AIEX-097)*

---

## Phase 31 Objectives

### Primary — Floor Determination (Track A)

**The single most important task.** Extend the Weil ratio sequence to large prime sets and rerun curve-fitting. The current 9-point dataset is statistically underdetermined. A minimum in the SSE landscape — if it appears — will identify the true floor.

**Target prime sets:**

| Run | p_max | Estimated N_primes | Purpose |
|-----|-------|--------------------|---------|
| 31A | 200 | ~46 | Near-term extension |
| 31B | 300 | ~62 | Mid-range |
| 31C | 500 | ~95 | Primary target |
| 31D | 700 | ~125 | Confirmation |

**Script requirement:** Extend `thread2_weil_ratio()` from `rh_phase30.py` to these cutoffs. Same model: y = a·x^(−b) + c. Three runs per dataset — c fixed at c₁, c fixed at 1/2π, c free with constrained bounds. Report SSE landscape at each p_max. Flag if the landscape develops a minimum or inflection point.

**Decision criteria:**
- If SSE minimum appears near c₁ = 0.118 → Conjecture 29.3 promoted to Strong
- If SSE minimum appears near 0.140 → square-root law hypothesis gains traction, new constant to identify
- If landscape remains monotone through p_max=700 → dataset still underdetermined, Phase 32 needed

### Secondary — p=11 Hinge Verification (Track B)

**The p=11 sign asymmetry is a single observation.** It needs a reproducibility test at larger prime boundaries before it can be called a structural claim.

**ZDTP batch run (Claude Desktop):** After Claude Code delivers Phase 31 data, run isolated S1 transmissions for the next prime boundaries: p=13, p=17, p=19, p=23. Check whether the ±sign pair in 64D recurs, and if so, whether it is unique to certain primes or a general property of primes above a threshold.

**Hypothesis to test:** p=11 is special because it sits at the boundary between the {5,7,11} invariant anchor set and the {13,...} extended prime range. If the ±pattern appears only at boundary primes (the largest member of the isometry set), that is structural. If it appears at all primes above p=7, it is a general ZDTP property, not a sedenion-specific one.

### Tertiary — D₆ Partition Check (Track C)

From Phase 19 Thread 1 (AIEX-053): the 45 bilateral P∪Q directions are exactly D₆ minus its 15 both-negative roots. The prime split {5,7,11} vs {2,3,13} may correspond to a subset selection within this D₆ cone.

**Task:** Map each prime's bilateral direction assignment (from the Phase 19 Gram matrix data) onto the 45 D₆ directions. Check whether {5,7,11} and {2,3,13} fall in geometrically distinct subregions of the cone. If so, the isometry pinning has a Lie-algebraic explanation. *(AIEX-092)*

**This is a Claude Code / Lean 4 task**, not a CAILculator run.

### Quaternary — c₁² + c₃² = 1 Analytic Proof Attempt (Track D)

The exact unit norm identity (AIEX-091) is a candidate theorem. The Phase 31 script should attempt to verify it analytically from the Weil explicit formula, not just numerically.

**Approach:** Express c₁ and c₃ as the sine and cosine of the Weil angle θ_W = arctan(c₁/c₃) = 6.775°. The unit norm follows trivially from trigonometry *if* θ_W is a true angle — but the question is whether θ_W has an analytic definition in terms of the explicit formula independent of the numerical fit. If it does, the identity is a theorem. If it only holds numerically, it remains an empirical observation.

---

## Connections from KSJ — What Phase 31 Inherits

The following prior results from the KSJ bear directly on Phase 31 interpretation:

**From Phase 17 (AIEX-001):** Q-vector q2 detects p=2 at SNR=418. P-vectors span a 4D subspace where p=2 is invisible. The {5,7,11} isometry set are all unramified primes — p=2 is not in the anchor set, consistent with its unique Q2 role.

**From Phase 18E (AIEX-035, AIEX-036):** The full 48-member bilateral family universally embeds as E8 first-shell roots (norm²=2), spanning 45 distinct 8D directions. The Canonical Six (A₁)⁶ subspace is the unique subset with pure Clifford grade structure. The {5,7,11} anchor primes may preferentially align with the Canonical Six subspace — this should be checked.

**From Phase 18F (AIEX-046, AIEX-054):** Q2 selectivity is Heegner-specific: ℚ(√−3) and ℚ(√−2) are elevated; the chi8 tower terminates. The 60 A₂ sub-systems in the bilateral set reflect the Eisenstein integer structure. The {2,3,13} decay set contains p=2 (dominant Weil misalignment driver, AIEX-066) and p=13 (conductor-13 L-function territory, related to chi3 anomaly, AIEX-016).

**From Phase 19 Thread 1 (AIEX-053, AIEX-055):** The 45 bilateral directions = D₆ minus 15 both-negative roots. The Canonical Six have unique pure Clifford grade structure within the bilateral set (0 mixed [0,2] products vs 100% for closure-failure pairs). Index 7 excluded.

**From Phases 24–29 (session memory):** AIEX-001a multiplicative sedenion exponential product identified as Berry-Keating xp Hamiltonian in 16D sedenion space. Weil negativity confirmed (ratio ~0.248 stable). ℏ_sed = 11.19 ± 1.71 as a constant. Bilateral prime isometry confirmed for p∈{5,7,11} to machine precision across those phases.

**From Phase 30 methodology note (AIEX-095):** Free-fit degeneration is a diagnostic of dataset underdetermination, not a negative result about the asymptote. Phase 31 scripts should always report the degenerate/constrained status of Run C explicitly.

---

## Abstract Revision Requirements (Before April 1)

Per AIEX-097 and AIEX-098, the draft abstract requires these changes before the Canonical Six v1.4 submission:

| Current phrasing | Corrected phrasing |
|-----------------|-------------------|
| "Sedenion Horizon Theorem" | "Sedenion Horizon Conjecture" |
| "We demonstrate" | "We present evidence for" |
| "undergoes 1/√N decay toward c₁" | "undergoes power-law decay (b≈0.42) with c₁ as preferred floor over the Circle Method limit" |
| (missing) | "Verification with p_max extending to 500+ is underway (Phase 31)" |
| "p=11 functions as a Symmetry Hinge" | "p=11 exhibits a preliminary sign asymmetry in 64D ZDTP transmission, requiring verification" |

---

## Phase 31 Script Specification for Claude Code

**File:** `rh_phase31.py`
**Inherits:** `rh_phase30.py` structure — extend, do not rewrite

**Required tracks:**

```
Track A: thread2_weil_ratio() extended to p_max ∈ {200, 300, 500, 700}
         - Same bilateral trace and Weil RHS formulas as Phase 30
         - Full SSE landscape sweep (c from 0.05 to 0.22, 35 points)
         - Run A (c=c1), Run B (c=1/2pi), Run C (constrained free)
         - Report: does landscape develop minimum? Where?

Track B: D6 direction map
         - Load Phase 19 Gram matrix data (bilateral 8D directions)
         - Assign each prime p ≤ 151 to its bilateral D6 direction
         - Flag which D6 directions are occupied by {5,7,11} vs {2,3,13}
         - Output: direction partition table as JSON

Track C: c1^2 + c3^2 = 1 analytic check
         - Express c1, c3 as cos/sin of Weil angle theta_W
         - Verify: does theta_W have an analytic expression in terms
           of the Weil explicit formula parameters?
         - Report: theorem candidate or empirical observation

Track D: Extended bilateral zero pair count (from Phase 29 baseline)
         - Phase 29 found 6,290 bilateral zero pairs at 500 zeros
         - Phase 31: extend to 750 and 1000 zeros
         - Verify superlinear growth continues
         - Fit growth model: pairs ~ N^alpha, report alpha
```

**Output files:**
- `phase31_results.json`
- `phase31_summary.txt`

**Dependencies:** numpy, scipy, mpmath

---

## CAILculator Runs Queued for Claude Desktop (Phase 31)

Once Claude Code delivers the Phase 31 script and results JSON, the following CAILculator runs are pre-planned:

1. **ZDTP batch — p=13, 17, 19, 23 isolated (S1):** p=11 hinge reproducibility test
2. **ZDTP full cascade — extended state vector (p_max=500 data):** convergence score at the larger prime set
3. **analyze_dataset on extended Weil ratio sequence:** check for structural shift in decay character as p_max crosses 200, 300, 500

---

## Open Questions Entering Phase 31

From KSJ (?question tags, filtered to Phase 31-relevant):

1. Does the SSE landscape develop a minimum as p_max → 500+? Where does it land? *(AIEX-094)*
2. Is there a theoretical reason for b = 0.5 (square-root law)? What mechanism produces it? *(AIEX-096)*
3. Does the p=11 ±sign asymmetry recur at p=23, p=47, or other prime boundaries? *(AIEX-099)*
4. Does the D₆ decomposition segregate {5,7,11} from {2,3,13}? *(AIEX-092)*
5. What is the correct mathematical definition of c₁ in terms of zeta zero statistics? *(AIEX-089)*
6. Can c₁² + c₃² = 1 be proven analytically? *(AIEX-091)*
7. Does the Weil ratio limit as p_max → ∞ equal c₁ = 0.11798? *(AIEX-090)*
8. Is the 45-direction bilateral cone a sub-lattice of E8 with Weyl group description? *(AIEX-040)*

---

## Decision Gate

Phase 31 has a single binary outcome that determines the trajectory:

**If the SSE landscape develops a minimum near c₁ (0.118):**
→ Sedenion Horizon Conjecture is promoted from Developing to Strong
→ The April 1 abstract claim becomes defensible with the Phase 31 caveat removed
→ Phase 32 focuses on the analytic proof of the c₁ floor

**If the SSE landscape minimum lands elsewhere (0.140, or remains monotone):**
→ The asymptote question is re-opened
→ If near 0.140: investigate theoretical basis for b=0.5 and identity of 0.140
→ If monotone through p_max=700: the dataset may be fundamentally underdetermined at this precision level; pivot to analytic methods

---

*Phase 30 closed (Track 2). Phase 31 opens.*
*KSJ: 100 captures | 17 open questions | 68 key insights*
*Chavez AI Labs LLC — Applied Pathological Mathematics: Better math, less suffering.*
