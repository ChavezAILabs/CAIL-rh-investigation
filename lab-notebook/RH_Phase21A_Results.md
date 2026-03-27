# Phase 21A Results — Simple Spectrum Investigation
## Chavez AI Labs LLC · March 24, 2026

**Status:** COMPLETE — Null result confirmed; surprise in Target 3
**Script:** `rh_phase21a.py`
**Output:** `phase21a_results.json`

---

## Headline

**Simple spectrum is NOT forced by the AIEX-001 algebra.** A degenerate H₅ (repeated eigenvalues) satisfying all known constraints — self-adjointness, block-diagonal structure, and equivariance — can be explicitly constructed. Simple spectrum must remain an explicit assumption in the AIEX-001 argument.

**Surprise in Target 3:** Two inter-block sedenion products are zero (q₃×q₂ = 0 and q₃×q₄ = 0), confirming bilateral zero divisor structure within the fixed-subspace root set. Two inter-block products have nonzero scalar parts (−1), revealing shared sedenion basis indices across blocks. Neither imposes eigenvalue constraints on H₅.

---

## Target 1: Gram Matrix Spectrum

The 6×6 Gram matrix of the fixed-subspace roots (normalized inner products):

```
        v₁    v₄    q₃    q₂    v₅    q₄
v₁  [  1,    0,   -1,    0,    0,    0  ]
v₄  [  0,    1,    0,    0,    0,    0  ]
q₃  [ -1,    0,    1,    0,    0,    0  ]
q₂  [  0,    0,    0,    1,    0,    0  ]
v₅  [  0,    0,    0,    0,    1,    0  ]
q₄  [  0,    0,    0,    0,    0,    1  ]
```

**Eigenvalues:** {0, 1, 1, 1, 1, 2}

| Eigenvalue | Multiplicity | Geometric meaning |
|---|---|---|
| 0 | 1 | Null eigenvector = (v₁+q₃)/√2 = 0 (antipodal pair) |
| 1 | 4 | {v₄, q₂, v₅, q₄} — mutually orthogonal, independent |
| 2 | 1 | (v₁−q₃)/√2 = v₁√2 — the "symmetric sum" direction |

**Structural explanation:** v₁ = −q₃ (antipodal roots). They contribute the same direction twice, creating the null eigenvalue. The Block A submatrix is rank 2, not 3, because q₃ is redundant given v₁.

The 5×5 Gram operator (sum of outer products, acting on the 5D fixed subspace) has eigenvalues {1, 1, 1, 1, 2}. All eigenvalues nonzero — the 6 roots span the full 5D space (with one redundancy from the antipodal pair).

---

## Target 2: Commutator Constraint [H₅, G] = 0

If H₅ commutes with the Gram matrix G (treated as an operator), then H₅ must preserve each eigenspace of G:

| G eigenspace | Dimension | Constraint on H₅ |
|---|---|---|
| Eigenvalue 0 | 1 | H₅ maps null eigenvector to scalar × itself |
| **Eigenvalue 1** | **4** | **H₅ can be ANY 4×4 symmetric matrix on this subspace** |
| Eigenvalue 2 | 1 | H₅ maps dominant eigenvector to scalar × itself |

**Conclusion:** [H₅, G] = 0 does NOT force H₅ diagonal. The 4D eigenvalue-1 subspace is a large space where H₅ is unconstrained — it can have any symmetric structure, including repeated eigenvalues. The commutator condition cannot derive simple spectrum.

---

## Target 3: Inter-Block Sedenion Products

Computed all inter-block products r_A × r_B in the 16D sedenion algebra, using the 16D representations:

| Product | Block pair | Scalar part | \|prod\|² | Note |
|---|---|---|---|---|
| v₁ × v₄ | A×A | 0 | 4 | orthogonal |
| q₃ × v₁ | A×A | 0 | 4 | orthogonal |
| q₃ × v₄ | A×A | 0 | 4 | orthogonal |
| q₂ × v₅ | B×B | 0 | 4 | orthogonal |
| v₁ × q₂ | A×B | 0 | 4 | inter-block |
| v₁ × v₅ | A×B | 0 | 4 | inter-block |
| v₄ × q₂ | A×B | 0 | 4 | inter-block |
| v₄ × v₅ | A×B | 0 | 4 | inter-block |
| **q₃ × q₂** | **A×B** | **0** | **0** | **zero divisor pair!** |
| **q₃ × v₅** | **A×B** | **−1** | 4 | shared index e₇ |
| v₁ × q₄ | A×C | 0 | 4 | inter-block |
| v₄ × q₄ | A×C | 0 | 4 | inter-block |
| **q₃ × q₄** | **A×C** | **0** | **0** | **zero divisor pair!** |
| q₂ × q₄ | B×C | 0 | 8 | ∥prod∥²=8 — large |
| **v₅ × q₄** | **B×C** | **−1** | 4 | shared index e₄ |

### Surprise Finding: Two Unexpected Zero Divisor Pairs

**q₃ × q₂ = 0** (p=13 root × p=3 root, Block A × Block B)
- q₃ = e₆+e₉ (16D), q₂ = e₅+e₁₀ (16D)
- These have no shared indices, so their scalar part is 0 — but the full product vanishes!
- q₃ and q₂ are Q-vectors of different canonical patterns; their annihilation is a bilateral zero divisor identity within the root set.

**q₃ × q₄ = 0** (p=13 root × p=2 root, Block A × Block C)
- q₃ = e₆+e₉ (16D), q₄ = e₃−e₁₂ (16D)
- Again no shared indices, full product = 0
- Cross-block bilateral zero divisor: Block A × Block C annihilate.

### Nonzero Scalar Parts: Shared Sedenion Indices

**q₃ × v₅: scalar = −1** (p=13 × p=5, Block A × Block B)
- q₃ = e₆+e₉ and v₅ = e₃+e₆ share sedenion index 6 (= e₇ in 1-indexed notation)
- Scalar part = −⟨q₃, v₅⟩ = −1 (one shared unit)

**v₅ × q₄: scalar = −1** (p=5 × p=2, Block B × Block C)
- v₅ = e₃+e₆ and q₄ = e₃−e₁₂ share sedenion index 3 (= e₄ in 1-indexed notation)
- Scalar part = −⟨v₅, q₄⟩ = −1

**Do these impose eigenvalue constraints on H₅?** No. The scalar part of a sedenion product is a structural fact about the algebra, not an equation involving H₅ eigenvalues. There is no AIEX-001 identity of the form "λ_A − λ_B = scalar(r_A × r_B)."

**Overall conclusion:** The inter-block product table confirms no algebraic coupling between block eigenvalues. The zero divisor pairs and nonzero scalar parts reveal sedenion structure of the root set but do not constrain H₅.

---

## Target 4: Null Result — Degenerate H₅ Constructions

The constraints on H₅ are:
- **(a)** Self-adjoint: H₅ = H₅ᵀ
- **(b)** Block-diagonal: H₅ = H_A ⊕ H_B ⊕ H_C (from Phase 19 Thread 3)
- **(c)** Equivariance: satisfied by construction in the embedding formula

**All four test H₅ matrices are valid and degenerate:**

| Test | H₅ eigenvalues | Structure |
|---|---|---|
| H₅ = I₅ | {1, 1, 1, 1, 1} | All eigenvalues equal |
| H_A=H_B=1.5I, H_C=2 | {1.5, 1.5, 1.5, 1.5, 2} | 4-fold repeated |
| H_A=H_B=2I, H_C=3 | {2, 2, 2, 2, 3} | 4-fold repeated |
| H_A=H_C=3, H_B=5I | {3, 3, 3, 5, 5} | Cross-block degeneracy |

**Structural note:** Off-diagonal entries within a block (e.g., H_A = [[1, ε], [ε, 1]]) split eigenvalues to {1+ε, 1−ε} — this breaks degeneracy within the block. Block-diagonal degeneracy requires the block to be a scalar multiple of identity.

**Target 1 is closed:** Simple spectrum cannot be derived from the AIEX-001 algebra.

---

## Summary: Status of Simple Spectrum Assumption

| Source | Forces simple spectrum? | Reason |
|---|---|---|
| Self-adjointness | No | Degenerate self-adjoint operators exist |
| Block-diagonal structure | No | Each block can be λI (degenerate) |
| Equivariance constraint | No | Built into embedding, independent of H₅ eigenvalues |
| Gram matrix commutativity | No | 4D degenerate eigenspace allows any H₅ on it |
| Sedenion inter-block products | No | No eigenvalue coupling in product scalar parts |
| Grand Simplicity Hypothesis (GSH) | Partial | GSH ⟹ distinct eigenvectors, NOT necessarily distinct eigenvalues |
| Hilbert-Pólya identification | Yes (tautological) | If spectrum(H₅) = {tₙ}, distinct zeros ⟹ simple spectrum — but this is the claim, not a proof |

---

## Paper Statement

For the AIEX-001 paper, the simple spectrum assumption should be stated as:

> **Assumption (Simple Spectrum).** The operator H₅ on the 5D fixed subspace has simple spectrum — all eigenvalues occur with multiplicity 1. This is a standard assumption in Hilbert-Pólya theory: a self-adjoint operator whose spectrum is identified with the Riemann zeros is expected to have simple spectrum because the zeros are believed to be distinct. We verify numerically that the first 200 zeros are distinct (Phase 19 Thread 3); the algebraic constraints from the (A₁)⁶ block structure do not enforce this independently (Phase 21A).

**What Phase 21A rules out:** The search for an algebraic mechanism forcing simple spectrum is complete at the level of: (1) Gram matrix commutativity, (2) sedenion inter-block scalar products, and (3) block-diagonal structure. None of these force simple spectrum. The assumption is necessary and well-motivated, not provable from the current framework.

---

## Open Questions

1. **Zero divisor pairs q₃×q₂ = 0 and q₃×q₄ = 0** — are these instances of the bilateral zero divisor family from Phase 19 Thread 2, or new pairings? Specifically: is q₃ a bilateral zero divisor partner with q₂ and q₄ simultaneously? This would connect to Phase 18B (Bilateral Collapse Theorem).

2. **q₂ × q₄: |prod|² = 8** — this product has norm² = 8, not 4. This is anomalously large for two unit-norm-squared sedenion elements. What is the geometric meaning of this amplification? (Normal products of E8 first-shell roots have |prod|² = 2 or 4 or 0.)

3. **The v₅ "shared index" pattern** — v₅ = e₃+e₆ appears in two nonzero scalar products (as the "B block element" coupling to both A and C blocks via shared sedenion indices). Is v₅ (corresponding to prime p=5) algebraically special within Block B? This could connect to the Heegner channel structure.

---

*Phase 21A completed March 24, 2026*
*Chavez AI Labs LLC · Applied Pathological Mathematics*
