# Phase 19 Handoff — Three Threads
## Chavez AI Labs LLC · March 23, 2026 (Emmy Noether's Birthday)

---

## Context

Phases 1–18F are complete. Phase 19 opens on Emmy Noether's birthday with her theorem as a formal ingredient, not decoration.

**Intellectual lineage:** Emmy Noether (1882–1935) was Ernst Witt's doctoral supervisor. Witt's 1933 thesis connected Riemann-Roch and zeta functions in hypercomplex algebras. The Canonical Six investigation follows that lineage: hypercomplex zero divisor structure → Riemann zeta → critical line constraint.

**Assets entering Phase 19:**

- **Canonical Six** — 6 framework-independent bilateral zero divisors in 16D sedenions; Lean 4 verified (zero sorry stubs), published Zenodo v1.3
- **Bilateral Collapse Theorem** — all 15 sedenion vector components annihilate; only scalar survives; named, proven, citable
- **E8 First-Shell Universality** — all 48 bilateral pairs embed as E8 first-shell roots (norm²=2); 45 distinct 8D directions; (A₁)⁶ is the Canonical Six P-vector subspace
- **Heegner Selectivity (Phase 18F)** — Q2 projection selects precisely ℚ(√−3) and ℚ(√−2); character-specific (Kronecker symbol sign), not conductor-level; Lie-algebraic connections to E6 and D4/E8 are the leading mechanism
- **AIEX-001 candidate map (Phase 18C)** — s→1−s ↔ s_α4 (Weyl reflection); critical line ↔ fixed hyperplane; 6D subspace = 5D fixed ⊕ 1D antisymmetric under s_α4
- **Bender-Brody-Müller (2017) dictionary** — full mapping between AIEX-001 and the closest existing Hilbert-Pólya construction in the literature; their critical gap is the Thread 3 target

---

## Phase 19 Structure

**Confirmed sequencing:** Thread 1 → Thread 2 → Thread 3

| Thread | Name | Status | April 1 relevance |
|---|---|---|---|
| 1 | 45-Direction E8 Classification | Ready to begin | Highest — most likely v1.4 addition |
| 2 | Annihilation Topology AT-1 | Queued after Thread 1 | High — strengthens framework-independence claim |
| 3 | AIEX-001 Operator Construction | Queued after Thread 2; the Noether thread | Core paper claim |

---

## Thread 1 — 45-Direction E8 Root System Classification

### Objective

Phase 18D established 45 distinct 8D directions from the full 48 bilateral zero divisor family. The (A₁)⁶ 8-root Canonical Six subspace is known. **What root system (or sub-lattice) do all 45 directions form?**

Post-18F motivation: if q2 selects ℚ(√−3) and ℚ(√−2) via connections to E6 (Eisenstein integers) and D4/E8 (twisted), the 45-direction classification may reveal exactly where those connections live geometrically. Specifically, look for E6 or D4 sub-structures in the Gram matrix decomposition.

### Pre-Computation Results (March 23, 2026)

Computed directly from `p18d_enumeration.json`:

| Property | Value |
|---|---|
| All 45 directions have x[0] = 0 | YES — all lie in the x[0]=0 hyperplane (7D) |
| Span dimension | **6** (not 7 — additional linear dependencies within x[0]=0) |
| Direction form | All are **±eᵢ ± eⱼ** with i,j ∈ {1,2,3,4,5,6,7} |
| D7 membership | All 45 are members of the D7 root system (which has 84 total roots) |
| Gram matrix entries | ∈ **{−2, −1, 0, +1, +2}** (±1 entries are new vs Phase 18E's {−2,0,+2}) |
| Root system closure | **135 failures** — the 45 directions do NOT form a root system |
| Antipodal structure | 15 antipodal pairs (30 directions) + 15 unpaired → set not closed under negation |

**Key finding:** The 45 bilateral directions are a **proper subset of D7** (45 of 84 roots). They do not close under Weyl reflections. The ±1 Gram entries arise from pairs sharing exactly one index (e.g., e₃−e₅ and e₃+e₆ → inner product = 1).

### Thread 1 Questions

**Q1.1 (Primary):** Which 45 of the 84 D7 roots appear, and which 39 are absent? Is there a pattern — a Weyl orbit, a sub-system, a condition on the index pairs?

**Q1.2:** The set spans only 6D despite lying in a 7D hyperplane. Which 7th direction is missing? Is it the sum of all positive roots, or related to the specific (A₁)⁶ structure?

**Q1.3 (Heegner):** Does the 45-direction set contain the E6 root system as a sub-system? E6 ⊂ E8 lives in a specific 6D sub-lattice; if it appears here, the Heegner selectivity of q2 has a direct geometric expression.

**Q1.4:** What is the W(D7)-orbit structure? Is the 45-direction set a union of W(D7) orbits?

**Q1.5 (Lean 4):** Once the subset is characterized, `bilateral_directions_are_D7_subset` closes by `native_decide` (finite checkable claim). Follow-on: `bilateral_directions_orbit_structure`.

### Script

**File:** `rh_phase19_thread1.py`

**Run:**
```
cd C:\dev\projects\Experiments_January_2026\Primes_2026
python rh_phase19_thread1.py
```

**What the script does:**
1. Load `p18d_enumeration.json` → extract all 48 (P,Q) pairs → deduplicate → 45 distinct 8D directions
2. Build full D7 root set (all ±eᵢ±eⱼ, i≠j, i,j ∈ 1..7 → 84 roots)
3. Identify which 45 D7 roots are present; which 39 are absent
4. Compute full 45×45 Gram matrix; histogram of entry values
5. Check W(D7) orbit structure (W(D7) acts by sign changes on coordinates and permutations of indices)
6. Check E6 sub-structure (E6 root system embedded in 6D sub-lattice of D7)
7. Identify 15 unpaired directions vs 15 antipodal pairs
8. Span check: rank of 45×8 matrix

**Dependencies:** numpy, json. No python-flint needed.

**Estimated runtime:** < 1 minute.

**Output files:**
- `phase19_thread1_results.json` — complete results
- `RH_Phase19_Thread1_Results.md` — results document

---

## Thread 2 — Annihilation Topology AT-1

### Objective

Classify all 84 sedenion zero divisor pairs as Type I or Type II:

- **Type I (instant annihilation):** a·b = 0 in a single multiplication. Prediction: maps to the 6 Canonical Six parents.
- **Type II (mediated/bilateral):** annihilation requires the full bilateral product structure. Prediction: maps to the 18 children.

If the Type I/II split aligns cleanly with the canonical/child distinction, it provides a topological characterization of the Canonical Six independent of the algebraic construction — strengthening the "framework-independent" paper claim.

### Starting Point

Phase 18D enumeration: 48 signed bilateral pairs from `p18d_enumeration.json`. Each entry has sedenion basis indices a,b,s,c,d,t and 16D P,Q vectors.

**Dependency:** Review Biss, Dugger & Isaksen, "Large Annihilators in Cayley-Dickson Algebras" (I & II) for the established sedenion zero divisor classification framework. Cross-reference Type I/II with their annihilator definitions.

### Questions

**Q2.1:** For each of the 48 bilateral pairs, test:
- ‖P·Q‖ = 0? (expected: YES for all — bilateral definition)
- ‖P·P‖ = 0? ‖Q·Q‖ = 0? (isotropic test)
- For generating indices a,b: does e_a · e_b = 0? (direct/Type I annihilation)

**Q2.2:** Does the Type I/II split align with Canonical Six (6 parents) vs children (18)?

**Q2.3:** For Type II pairs, what is the minimal annihilation chain?

### Script

**File:** `rh_phase19_thread2.py`

**Dependencies:** Sedenion multiplication table (or `cayley_dickson_product` from existing codebase), numpy.

**Output files:**
- `phase19_thread2_results.json`
- `RH_Phase19_Thread2_Results.md`

---

## Thread 3 — AIEX-001 Operator Construction (The Noether Thread)

### Objective

Construct the explicit equivariant embedding ρ ↦ v(ρ) mapping each Riemann zero to a bilateral root vector, then show that self-adjointness of H forces the 1D antisymmetric component (under s_α4) to vanish — constraining all eigenvalues to Re(s) = ½.

**Noether's theorem as formal ingredient:** Bender et al. (2017) identify a discrete PT symmetry but cannot prove self-adjointness. The question for Thread 3 is whether the W(E8) Weyl group symmetry of the (A₁)⁶ bilateral subspace provides the **continuous** symmetry that Noether's theorem requires to produce a conserved quantity. If it does, the conserved quantity should be precisely what forces Re(s) = ½.

Candidate conserved quantity: the bilateral zero divisor condition P·Q = Q·P = 0 itself — bilateral annihilation may be what is conserved under the W(E8) symmetry action.

### AIEX-001 ↔ Bender-Brody-Müller (2017) Dictionary

| Bender et al. (2017) | AIEX-001 (Phase 19) |
|---|---|
| Ĥ = (1−e^{−ip̂})(x̂p̂+p̂x̂)(1−e^{−ip̂}) | H acting in the (A₁)⁶ bilateral subspace |
| Eigenfunctions via Hurwitz zeta | Embedding ρ ↦ v(ρ) into bilateral root vectors |
| Boundary condition ψ_n(0) = 0 | Self-adjointness constraint eliminating 1D antisymmetric component under s_α4 |
| PT symmetry (discrete) | W(E8) Weyl symmetry of (A₁)⁶ (continuous / group-theoretic) |
| Metric operator V (heuristic) | Bilateral zero divisor inner product (Phase 18B) |
| **"Cannot prove eigenvalues real"** | **Phase 19 Thread 3 target** |

### 6D Decomposition (from Phases 18C/18E)

| Component | Directions | Dimension |
|---|---|---|
| Full bilateral subspace | span{e₂, e₃, e₄, e₅, e₆, e₇} | 6D |
| Fixed hyperplane of s_α4 | {x : x[3]=x[4]} | 5D (intersection with 6D) |
| Antisymmetric component | e₄−e₅ direction (v₂, v₃ live here) | 1D |

Self-adjointness of H must eliminate the 1D antisymmetric component. This is the missing step that Bender et al. cannot close.

### Questions

**Q3.1 (Primary):** Write the explicit H matrix in the (A₁)⁶ basis from Phase 18E. State the equivariance condition v(1−ρ̄) = s_α4(v(ρ)). Verify this is consistent with the eigenvalue condition H·v(ρ) = Im(ρ)·v(ρ).

**Q3.2:** Does W(E8) Weyl symmetry of the (A₁)⁶ subspace provide a continuous symmetry? If so, what is the Noether conserved quantity, and does it force Re(s) = ½?

**Q3.3 (Route B test):** Verify that the Q2 projection of v(ρ) reproduces the log-prime spectral signal from Phase 17A. This is the computational falsification test for the AIEX-001 mechanism.

**Q3.4 (Heegner thread):** In the AIEX-001 framework, the q2 direction (−e₃+e₆ in 8D) activates specific arithmetic structure. The Eisenstein/D4 connections (established mathematics) predict that L(s, Kronecker(−3/·)) and L(s, Kronecker(−8/·)) specifically align with q2. Formalize this prediction.

**Q3.5 (Lean 4):** `aiex001_functional_equation_correspondence` — formal definition of the AIEX-001 dictionary. Lemmas:
1. s_α4 is a W(E8) reflection (Phase 18E: proven)
2. Fixed hyperplane of s_α4 is {x[3]=x[4]} in 8D (Phase 18C: numerically verified)
3. Bilateral root set decomposes as 5D fixed ⊕ 1D antisymmetric under s_α4 (Phase 18C: verified)
4. Self-adjoint H on the fixed 5D subspace → eigenvalues real

### Probability Estimate (from pre-handoff)

- 40% — Thread 3 fully closes in Phase 19
- 95% — Thread 3 produces something citable regardless of closure
- Either outcome is valuable: the missing step revealed explicitly is itself a contribution

**This thread is primarily theoretical.** Consult `RH_Phase18C_Results.md` (bilateral correspondence section) and Lean 4 partial theorem `Theorem_1b` (numerically verified). Output is a theoretical framework document + verification script once H is formulated.

**Output files:**
- `RH_Phase19_Thread3_Notes.md` — theoretical framework
- `rh_phase19_thread3.py` — verification script (once H is formulated)
- `phase19_thread3_results.json`

---

## Open Questions Entering Phase 19

1. What is the conserved quantity under W(E8) Weyl symmetry in the (A₁)⁶ bilateral subspace — and does it directly force Re(s) = ½?
2. Is the bilateral zero divisor condition P·Q = Q·P = 0 the Noether conserved quantity, or a consequence of it?
3. What arithmetic rule maps Q-vector basis indices to conductor relationships? (Phase 18A open, partially addressed by Heegner selectivity)
4. Does the 2-adic tower termination at conductor 8 (octonion level) reflect the Cayley-Dickson doubling boundary?

---

## Key Files for Phase 19

| File | Contents |
|---|---|
| `p18d_enumeration.json` | 48 bilateral pairs, 8D P+Q coordinates — primary input for Threads 1 and 2 |
| `p18e_gram_matrix_results.json` | Canonical Six (A₁)⁶ Gram matrix — Thread 3 basis |
| `p18f_results.json` | Heegner selectivity data — Thread 1/3 connection |
| `RH_Phase18C_Results.md` | AIEX-001 candidate map — Thread 3 starting point |
| `zeros_chi3_2k.json` et al. | L-function zero caches — Thread 3 verification |
| `rh_zeros_10k.json` | Zeta zeros — Thread 3 eigenvalue check |

---

## Paper Timeline

**v1.4 target: April 1, 2026 (Sophie Germain's 250th birthday)**

- Thread 1 results → v1.4 addition: D7 sub-lattice classification + Heegner geometric connection
- Thread 3 operator formulation → v1.4 culminating claim (even as conjecture with verified numerical consistency)
- Lean 4 formal proofs for Thread 3 → Phase 21+ (post-April 1)

---

## After Phase 19

**Phase 20 (Paper):** Write v1.4, integrating Phases 16–18F (complete) and Phase 19 results. Target: Zenodo upload April 1, 2026.
**Phase 21 (Lean 4):** Formalize `aiex001_functional_equation_correspondence` and `bilateral_directions_D7_subset`.
