# Phase 18E Results — E8 Gram Matrix and Geometric Substructure
**Date:** March 13, 2026
**Researcher:** Paul Chavez, Chavez AI Labs LLC
**Script:** `rh_phase18e_gram_matrix.py`
**Output:** `p18e_gram_matrix_results.json`
**Open Science:** Results shared publicly on GitHub and social media.

---

## Summary

Phase 18E establishes the full E8 geometric picture for the combined P+Q bilateral zero divisor root set. Five computational experiments were run: Gram matrix, subspace rank, Weyl reflections, bilateral P⊥Q orthogonality, and the spectral filter rule.

| Result | Finding |
|--------|---------|
| All 8 roots on E8 first shell | ✓ confirmed (all norm² = 2) |
| Gram matrix structure | Block-diagonal: 2×antipodal + 4×isolated; all cross entries ∈ {0, −2} |
| Root subsystem (completed) | **(A1)^6** in a 6D subspace of the 8D E8 embedding |
| P-vector subspace rank | 4 (v3 = −v2 creates dependency) |
| P+Q subspace rank | **6** (q2 and q4 add 2 independent dimensions) |
| Bilateral orthogonality | 4 genuinely orthogonal pairs; 1 degenerate (P=Q); 1 antipodal (P=−Q) |
| Weyl reflections in W(E8) | 1 genuine W(E8) reflection (Pattern 6); 4 are O(8) only (irrational beta) |
| Spectral filter rule | Holds for 7/8 roots; **v4 is anomalous** (sum root, but high-pass) |

---

## 18E-i: Gram Matrix

The full 8×8 Gram matrix G[i,j] = rᵢ · rⱼ of the combined bilateral root set:

```
         v1    q3    v2    v3    v4    v5    q2    q4
    v1: [ 2,  -2,   0,   0,   0,   0,   0,   0 ]
    q3: [-2,   2,   0,   0,   0,   0,   0,   0 ]
    v2: [ 0,   0,   2,  -2,   0,   0,   0,   0 ]
    v3: [ 0,   0,  -2,   2,   0,   0,   0,   0 ]
    v4: [ 0,   0,   0,   0,   2,   0,   0,   0 ]
    v5: [ 0,   0,   0,   0,   0,   2,   0,   0 ]
    q2: [ 0,   0,   0,   0,   0,   0,   2,   0 ]
    q4: [ 0,   0,   0,   0,   0,   0,   0,   2 ]
```

**Key properties:**
- All diagonal entries = 2: all roots lie on the E8 first shell (‖r‖² = 2) ✓
- All off-diagonal entries ∈ {0, −2}: every pair of distinct roots is either **orthogonal** or **antipodal**
- No entry of 1 or −1: no roots are at 60° or 120° angles — the set has no root-system-internal coupling other than antipodal pairs

**Antipodal pairs:** {v1, q3} and {v2, v3}. These are the only pairs with inner product −2 (the roots are negatives of each other).

**This Gram matrix structure is maximally simple.** It means the 8 bilateral roots span 6 independent 1D subspaces in E8 space, with zero cross-coupling between any two non-antipodal directions.

---

## 18E-ii: Subspace Rank

| Root set | Rank | Interpretation |
|----------|------|---------------|
| P-vectors only {v1, v2, v3, v4, v5} | **4** | v3 = −v2 creates a linear dependency |
| Full P+Q set {v1, q3, v2, v3, v4, v5, q2, q4} | **6** | q2 and q4 add 2 independent dimensions |

**q2 outside P-span:** confirmed (residual norm = √2 ≈ 1.414 — q2 is at distance √2 from the P-vector subspace).

**q4 outside P-span:** confirmed (same residual).

**AIEX-001 consequence:** The operator H built from P-vectors alone operates in a 4D subspace of the 8D E8 embedding. Incorporating Q-vectors expands coverage to 6D. H cannot be fully represented by P-vector geometry — the Q-components are geometrically independent and carry arithmetic information (p=2 detection, ultra-low-pass prime spectrum) unreachable from the P-subspace.

---

## 18E-iii: Weyl Reflection Analysis

For each bilateral pair (P_8D, Q_8D), we asked: is there a single Weyl group element in W(E8) that maps P_8D to Q_8D?

| Pattern | P_8D | Q_8D | Relationship | W(E8) single reflection? |
|---------|------|------|-------------|--------------------------|
| 1 | v2 | v2 | P_8D = Q_8D (identity) | ✓ trivially |
| 2 | v2 | q2 | orthogonal, different roots | ✗ — O(8) only |
| 3 | v3 | q3 | orthogonal, different roots | ✗ — O(8) only |
| 4 | v2 | q4 | orthogonal, different roots | ✗ — O(8) only |
| 5 | v5 | q2 | orthogonal, different roots | ✗ — O(8) only |
| 6 | v1 | q3 = −v1 | antipodal (P = −Q) | ✓ σ_{v1}(v1) = −v1 |

**Key finding — W(E8) single reflection:**
- **Pattern 6 only:** The Weyl reflection σ_{v1} maps v1 to −v1 = q3. Beta = v1 is an integer E8 root (norm² = 2, integer coordinates). This is a genuine W(E8) reflection. ✓
- **Patterns 2, 3, 4, 5:** A reflection in O(8) maps P_8D → Q_8D, but the reflecting root beta = (P−Q)/√(P·(P−Q)) has **irrational coordinates** (of the form integers/√2). Such a root is NOT in the E8 lattice. These maps require **at least 2 Weyl reflections** in W(E8).

**Revision to E8 Implications doc:** The claim in `RH_Phase17_E8_Implications.md` that each bilateral pair is related by "a single simple Weyl reflection" is correct only for Pattern 6 in the strict W(E8) sense. Patterns 2–5 are related by O(8) reflections that are NOT single Weyl group elements. The E8 Implications doc should be updated.

**The W(E8) characterization still holds** — since W(E8) acts transitively on all 240 roots, every pair can be connected by *some* Weyl group element. For patterns 2–5, that element has word length ≥ 2.

---

## 18E-iv: Bilateral P⊥Q Orthogonality

| Pattern | P_8D | Q_8D | P_8D · Q_8D | Relationship |
|---------|------|------|-------------|-------------|
| 1 | v2 | q1 = v2 | **+2** | degenerate: P_8D = Q_8D (same E8 root) |
| 2 | v2 | q2 | **0** | orthogonal ✓ |
| 3 | v3 | q3 | **0** | orthogonal ✓ |
| 4 | v2 | q4 | **0** | orthogonal ✓ |
| 5 | v5 | q2 | **0** | orthogonal ✓ |
| 6 | v1 | q3 = −v1 | **−2** | antipodal: P_8D = −Q_8D |

**Three distinct relationship types:**
1. **Degenerate (Pattern 1):** P and Q project to the same E8 root. The sedenion patterns P1 and Q1 collapse to the same 8D direction.
2. **Genuinely orthogonal (Patterns 2, 3, 4, 5):** P and Q project to distinct, perpendicular E8 roots. These are the non-trivial bilateral pairs.
3. **Antipodal (Pattern 6):** P and Q project to opposite E8 roots. The 8D projection of Q is the negation of the 8D projection of P.

**Primary Lean 4 target:** For the 4 genuinely orthogonal pairs (patterns 2–5), the 8D geometric orthogonality P_8D · Q_8D = 0 holds. The 16D algebraic annihilation P·Q = 0 (sedenion bilateral zero divisor condition) also holds — proven in Lean 4 (Canonical Six v1.3, zero sorry stubs). The question is whether these two conditions are equivalent — i.e., whether geometric orthogonality of the 8D projections is *equivalent to* sedenion algebraic annihilation. If yes, this is a theorem that characterizes bilateral zero divisors purely via E8 root geometry, bypassing the sedenion multiplication table entirely.

---

## 18E-v: Spectral Filter Rule Analysis

Empirical spectral characters (from Phases 15D and 17) vs. root-form prediction:

| Root | Form | Prediction | Empirical | Match |
|------|------|-----------|-----------|-------|
| v1 = e2−e7 | difference | high-pass | high-pass (Phase 15D) | ✓ |
| q3 = e7−e2 | difference | high-pass | high-pass (isometry = v1) | ✓ |
| v2 = e4−e5 | difference | high-pass | high-pass (Phase 15D) | ✓ |
| v3 = e5−e4 | difference | high-pass | high-pass (isometry = v2) | ✓ |
| **v4 = e2+e7** | **sum** | **low-pass** | **high-pass (Phase 15D)** | **✗** |
| v5 = e3+e6 | sum | low-pass | low-pass (Phase 15D) | ✓ |
| q2 = e6−e3 | difference | high-pass | broadband (Phase 17A) | ✓ |
| q4 = e4+e5 | sum | low-pass | ultra-low-pass (Phase 17A) | ✓ |

**7/8 match. The single counterexample: v4 = e2+e7 is a sum root but is empirically high-pass.**

**Why does the naive rule fail for v4?**

The spectral character is determined by the specific functional form of proj_{v4}(embed_pair(g1, g2)), not just whether the root is a sum or difference type. For v4 = (0,1,0,0,0,0,1,0):

```
proj_{v4}(embed_pair) = component_1 + component_6
                      = g2 + g2/(g1+g2)
                      = g2 · (g1 + g2 + 1) / (g1 + g2)
```

This projection is dominated by `g2` — the **second gap** in each pair. It's asymmetric (treats g1 and g2 differently), not a simple sum. The g2 dominance makes v4 sensitive to the ordering of gaps, giving it high-pass character despite being a sum root.

Compare v5 = (0,0,1,0,0,1,0,0):
```
proj_{v5}(embed_pair) = component_2 + component_5
                      = (g1 - g2) + g1/(g1+g2)
```
This involves `g1−g2` (difference → high-pass tendency) plus `g1/s` (ratio). v5's low-pass character emerges from specific cancellation between these terms at high frequencies.

**Revised rule:** The spectral character is determined by **which embed_pair components are accessed**, not just the root form (sum vs difference). A full analytic derivation (Phase 18E Lean 4 target: spectral filter theorem) requires expanding each root's projection as a function of g1, g2 and computing its DFT frequency response.

**The counterexample v4 is itself informative:** v4 = e2+e7 uses components {g2, g2/s} — both involve g2 — creating a purely second-gap projection that is asymmetric. v5 = e3+e6 uses components {g1−g2, g1/s} — involving both g1 and g2 in a balanced way. The asymmetry of v4's projection, not its sum-root form, drives its high-pass behavior.

---

## 18E-vi: Root Subsystem Classification

**The 8-root set is an asymmetric subset of the (A1)^6 root system.**

The completed root system (adding the 4 missing negatives {−v4, −v5, −q2, −q4}) would be:
```
{ ±v1, ±v2, ±v4, ±v5, ±q2, ±q4 }  =  12 roots in 6 mutually orthogonal directions
```
This is the direct sum of 6 copies of A1 = {+r, −r}: the root system **(A1)⁶** embedded in a 6D subspace of the 8D E8 embedding.

**The actual 8-root set** contains both roots from 2 of the 6 A1 factors but only one root from each of the remaining 4:
- Both signs present: {v1, q3=−v1} and {v2, v3=−v2}
- One sign only: v4, v5, q2, q4 (missing −v4, −v5, −q2, −q4)

**This asymmetry is intrinsic to the sedenion bilateral zero divisor structure.** The Canonical Six patterns give rise to Q-vector images {q2, q4} but not their negatives {−q2, −q4}. Similarly, v4 and v5 appear as P-vector images but their negatives do not arise from any Canonical Six P-vector.

**Open question for Phase 18F:** The 4 missing negatives {−v4=−e2−e7, −v5=−e3−e6, −q2=e3−e6, −q4=−e4−e5} are all E8 roots. They may be the 8D images of the 6 framework-dependent (CD-only, non-Canonical) sedenion zero divisors. If confirmed, the full (A1)^6 root system would partition as:
- Canonical Six: 8-root asymmetric subset (half the system)
- Framework-dependent patterns: the complementary 4 roots (the missing negatives)

This would be a precise geometric characterization of what framework-independence means in E8 coordinates.

---

## New Findings vs. Prior State

| Finding | Prior state | Phase 18E |
|---------|------------|----------|
| Gram matrix off-diagonal structure | Conjectured (selected entries computed) | **All 28 pairs verified: {0,−2} only** |
| Root subsystem type | Open | **(A1)^6 confirmed** |
| P+Q subspace rank | Conjectured 6 from two independent vectors | **Rank 6 confirmed numerically** |
| Bilateral P⊥Q relationships | P·Q=0 claimed for all | **3 types: degenerate, orthogonal (×4), antipodal** |
| Weyl reflection claim (E8 Implications doc) | "Single Weyl reflection" for all patterns | **Only Pattern 6 is a W(E8) reflection; Patterns 2–5 require ≥2 Weyl steps** |
| Spectral filter rule | "difference→high-pass, sum→low-pass" (heuristic) | **7/8 match; v4 is anomalous; rule depends on embed_pair component access pattern** |

---

## Lean 4 Targets (Updated)

| Target | Complexity | Status |
|--------|-----------|--------|
| All 8 roots have norm² = 2 (E8 first shell) | Integer arithmetic | Queued |
| All Gram matrix off-diagonal entries ∈ {0, −2} | Integer inner products | Queued |
| P+Q matrix has rank 6 (q2, q4 are independent of P-span) | Integer linear algebra | Queued |
| **P_8D ⊥ Q_8D ↔ P*Q = 0 (16D sedenion)** | Algebraic equivalence | **Primary target** |
| Pattern 6: σ_{v1}(v1) = −v1 = q3 (W(E8) reflection) | One-line proof | Immediate |
| Patterns 2–5: minimum Weyl word length = 2 (not 1) | Combinatorial | Queued |
| Spectral filter theorem (derive DFT frequency response from embed_pair form) | Analysis | Long-term |

---

## Implications for AIEX-001

The Phase 18E results sharpen the AIEX-001 operator picture:

1. **H operates in a 6D subspace of 8D E8 space**, not 4D (P-only) and not the full 8D. The 6D is the exact span of all Canonical Six bilateral root images.

2. **H's bilateral structure** corresponds to the 4 genuinely orthogonal (P,Q) pairs plus 1 degenerate and 1 antipodal. The orthogonal pairs are the structurally interesting ones — they place P and Q in perpendicular E8 directions, covering 2 independent dimensions per pattern (rather than redundant information from the same or antipodal directions).

3. **Self-adjointness candidate:** If P_8D ⊥ Q_8D ↔ P*Q = 0 is a theorem, then H's self-adjointness has a purely geometric characterization: the operator is self-adjoint exactly because its bilateral components (P,Q) project to orthogonal E8 roots. This would connect H's spectral properties directly to E8 root geometry without requiring knowledge of the sedenion multiplication table.

4. **The (A1)^6 structure** means H decomposes as a sum of 6 independent 1D projections (one per A1 factor) with no coupling between factors. This is a strong constraint on H's structure and suggests it may have a product form.

---

## Files

| File | Description |
|------|-------------|
| `rh_phase18e_gram_matrix.py` | This phase's computation script |
| `p18e_gram_matrix_results.json` | Full numerical results |
| `RH_Phase18E_Results.md` | This document |
| `RH_Phase18_Handoff.md` | Phase 18 master handoff |
| `RH_Phase17_E8_Implications.md` | Prior E8 analysis (partially revised by this phase) |

---

*Chavez AI Labs LLC · Applied Pathological Mathematics*
*"Better math, less suffering"*
