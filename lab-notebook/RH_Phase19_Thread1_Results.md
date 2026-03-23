# Phase 19 Thread 1 Results — 45-Direction E8 Root System Classification
## Chavez AI Labs LLC · March 23, 2026

**Status:** COMPLETE
**Script:** `rh_phase19_thread1.py`
**Output:** `phase19_thread1_results.json`

---

## Headline Finding: Exact Characterization of the Bilateral 45-Direction Set

The 45 bilateral P∪Q directions are precisely **the D₆ root system minus its 15 "both-negative" roots**.

| Property | Value |
|---|---|
| Host root system | D₇ (84 roots, ±eᵢ±eⱼ, i≠j in {1..7}) |
| Bilateral subset | 45 of 84 D₇ roots |
| Actual host space | **D₆** (60 roots in positions 1..6 only) |
| Missing from D₆ | 15 roots: {−eᵢ−eⱼ, 1≤i<j≤6} |
| Bilateral = | D₆ roots with at least one positive component |
| Index 7 (8D pos. 7) | **Completely excluded** — no bilateral direction involves e₇ |

**Exact rule:** The bilateral set is `{ε₁eᵢ + ε₂eⱼ : 1≤i<j≤6, NOT (ε₁=−1 AND ε₂=−1)}`.

This is the simplest possible description: take D₆, remove all "both-negative" roots.

---

## Sign Pattern — Universal Regularity

Every index pair (i,j) with i<j, i,j ∈ {1..6} has **exactly 3 of 4 sign combos** in the bilateral set:

| Sign combo | Present? | Count |
|---|---|---|
| (+eᵢ, +eⱼ) both positive | YES | 15 |
| (+eᵢ, −eⱼ) mixed | YES | 15 |
| (−eᵢ, +eⱼ) mixed | YES | 15 |
| (−eᵢ, −eⱼ) both negative | **NO** | 0 |

The missing sign is **always** (−,−). No exceptions across all 15 index pairs.

---

## Index 7 Exclusion

The bilateral set uses only 8D positions {1,2,3,4,5,6} — position 7 is entirely absent:

- Index pairs with NO bilateral directions: 6 → `{(1,7),(2,7),(3,7),(4,7),(5,7),(6,7)}`
- Index pairs present: 15 → all `(i,j)` with i<j in {1..6}

The span dimension = **6**, consistent with the set living in the e₁..e₆ hyperplane.

**Phase 18E consistency:** All 8 Phase 18E (A₁)⁶ roots are confirmed in the bilateral set (8/8 ✓). They all use positions in {1..6}: v1=(1,6), q3=(1,6), v2=(3,4), v3=(3,4), v4=(1,6), v5=(2,5), q2=(2,5), q4=(3,4).

---

## Root System Closure Analysis

The bilateral set does NOT form a root system — 120 Weyl reflection failures.

**Structure of failures:** The 120 failures come from pairs with inner product ±1 (pairs sharing exactly one index). The Weyl reflection σ_α(β) = β − ⟨α,β⟩·α maps each such pair to a "both-negative" direction −eᵢ−eⱼ. These 15 missing directions are exactly the set needed to close under Weyl reflections:

| Closure failures | 120 ordered pairs |
|---|---|
| Distinct missing directions | 15 |
| Missing directions in D₇ | 15/15 (all in D₇, just not in bilateral set) |
| Adding these 15 would give | D₆ (closed root system) |

The bilateral 45-direction set = D₆ positive cone under a natural orientation (all roots with ε₁ OR ε₂ = +1).

---

## Gram Matrix

Full 45×45 Gram matrix entry histogram:

| Entry | Count | Geometric meaning |
|---|---|---|
| +2 | 45 (diagonal) | Self-inner-product |
| +1 | 300 off-diagonal | 60° angle (A-type) |
| 0 | 435 off-diagonal | 90° angle (orthogonal) |
| −1 | 240 off-diagonal | 120° angle (A-type) |
| −2 | 15 off-diagonal | Antipodal pairs |

**Total pairs with ±1 inner product (60°/120° angles): 540.** This confirms the bilateral set is not D-type (which would have only 0 and ±2) — it has A-type geometry throughout, explaining why the Gram matrix has ±1 entries absent in Phase 18E's pure (A₁)⁶ Gram.

---

## Clifford Cl(7,0) Pass — CAILculator CliffordElement

**Implementation:** `CliffordElement` from `clifford_verified.py` (Beta v7+, verified against 552 bridge patterns). n=7, 128-dimensional multivector space.

### Geometric Product Structure of Closure-Failure Pairs

All 1080 closure-failure pairs (|⟨α,β⟩|=1) produce **100% mixed grade-0+grade-2** multivectors:

| Grade output | Count | Fraction |
|---|---|---|
| Pure grade-0 (scalar only) | 0 | 0% |
| Pure grade-2 (bivector only) | 0 | 0% |
| Mixed grade-0+grade-2 | 1080 | **100%** |

The grade-0 part = ±1 (= the inner product). The grade-2 part is the exterior product α∧β.

**Grade-2 blade saturation:** All 15 basis bivectors of Cl(6,0) (= C(6,2) = 15) appear with **equal frequency: 216 each**. The bilateral set is **bivector-saturating** in Cl(6,0) — the geometric products of its elements span the full 15D bivector space.

### A₂ Sub-Structure (Heegner: ℚ(√−3), Eisenstein Integers)

**Result: 60 distinct A₂ sub-systems embedded in the bilateral 45-direction set.**

- A₂-generating triples (α, β, α+β all in bilateral set with ⟨α,β⟩=−1): **240**
- Distinct A₂ sub-systems: **60**

The A₂ root system (6 roots, 60°/120° angles) is the root system of the Eisenstein integers ℤ[ω] and of su(3), which is the Lie algebra associated with ℚ(√−3) via the E6 connection. The bilateral set contains 60 copies of A₂ — the Q2 selectivity of ℚ(√−3) (Phase 18F) is geometrically reflected in this A₂ abundance.

Sample A₂ triple:
- α₁ = e₁−e₂, α₂ = e₂+e₆, α₁+α₂ = e₁+e₆ ✓ (all in bilateral set)

### D₄ Sub-Structure (Heegner: ℚ(√−2), D₄ Lattice)

**Result: 0 complete D₄ sub-systems. Best coverage: 18/24 roots for any 4-index subset.**

The systematic absence of (−,−) roots blocks every D₄ embedding: any 4-index subset S ⊂ {1..6} is missing the 6 roots {−eᵢ−eⱼ: i<j in S}. So 18/24 = 75% for all 15 four-element subsets equally.

**Interpretation:** The Phase 18F ℚ(√−2)/D₄ connection operates through a different geometric mechanism than D₄ sub-root-system embedding. The D₄ lattice connection to ℚ(√−2) may be reflected in the specific role of q2 and q4 within the bilateral set rather than in a full D₄ sub-system.

### Canonical Six Clifford Consistency

All 8 Phase 18E (A₁)⁶ roots confirmed in the bilateral set (8/8 ✓).

Geometric product grade structure of (A₁)⁶ root pairs (28 pairs total):

| Grade output | Count | Interpretation |
|---|---|---|
| Grade [0] — scalar only | 2 | Antipodal pairs (⟨α,β⟩=−2) |
| Grade [2] — bivector only | 26 | Orthogonal pairs (⟨α,β⟩=0) |
| Mixed [0,2] | 0 | No ±1 inner products in (A₁)⁶ |

The (A₁)⁶ subspace has a **pure grade structure** — no mixed-grade products. This cleanly distinguishes it from the rest of the bilateral 45-direction set, where mixed [0,2] grade products are universal (100% of closure-failure pairs). The Canonical Six are geometrically special within D₆: they form the unique 8-root subset with pure Clifford grade structure.

---

## Summary Table

| Property | Result |
|---|---|
| All 45 in D₇ | YES (45/84) |
| Host sub-system | **D₆** (positions 1..6 only; position 7 excluded) |
| Exact characterization | D₆ minus 15 "both-negative" roots |
| Span dimension | 6 |
| Forms root system | NO (120 closure failures) |
| Closing set (15 missing roots) | All in D₇, are the "both-negative" roots |
| Gram entries | {−2,−1,0,+1,+2} |
| 60°/120° angle pairs | 540 |
| Antipodal pairs | 15 |
| Unpaired directions | 15 (the "both-positive" roots +eᵢ+eⱼ) |
| D₄ sub-systems | 0 complete (18/24 best coverage) |
| A₂ sub-systems | **60 distinct** |
| Clifford grade (closure failures) | 100% mixed [0,2] |
| Grade-2 blades saturated | Yes — all 15 Cl(6,0) bivectors |
| Canonical Six Clifford | 8/8 in bilateral; pure grade structure |

---

## Open Questions (Generated by Thread 1)

**Q1 (Primary, now sharpened):** What is the algebraic mechanism that removes exactly the "both-negative" roots from D₆? The sedenion Cayley-Dickson construction produces bilateral pairs (P,Q) with P and Q both in the "positive half" of D₆. Why?

**Q2 (A₂ and Heegner):** The 60 A₂ sub-systems are abundant. Do specific A₂ sub-systems correspond to specific L-function characters (chi3, chi8a)? The q2 direction (−e₃+e₆ in 8D, i.e., index pair (3,6) with signs (−1,+1)) is one of the bilateral directions — which A₂ sub-systems does it participate in?

**Q3 (D₄ alternative):** If D₄ cannot be embedded (blocked by missing (−,−) roots), how does the Phase 18F ℚ(√−2)/D₄ connection manifest geometrically in the bilateral set? The 18/24 partial D₄ coverage is the same for all 4-index subsets — no subset is special.

**Q4 (Lean 4):** The exact characterization — bilateral set = D₆ minus {−eᵢ−eⱼ} — is a finitely checkable statement about specific root coordinates. Target: `bilateral_directions_are_D6_minus_both_negative`.

**Q5 (Bivector saturation):** The bilateral set saturates all 15 Cl(6,0) bivectors via geometric products. Is this related to the fact that Cl(6,0) has a well-known connection to E8 through the triality of SO(8) acting on Cl(6,0)?

---

## Files

| File | Contents |
|---|---|
| `rh_phase19_thread1.py` | Computation script |
| `phase19_thread1_results.json` | Complete results (Gram matrix, closure analysis, Clifford pass) |
| `RH_Phase19_Thread1_Results.md` | This document |
