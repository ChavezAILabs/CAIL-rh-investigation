# RH Phase 18 — CAILculator Handoff
## AIEX-001 Structural Exploration: E8 Geometry, Layer Structure, and Open Thread Resolution
**Date:** March 13, 2026
**Researcher:** Paul Chavez, Chavez AI Labs LLC
**Status:** Prep scripts pending; awaiting CAILculator MCP analysis
**Open Science:** Scripts and results will be shared on GitHub and social media

---

## Background

Phase 17 opened Q-vector access for the first time and produced three new findings that drive Phase 18:

1. **chi3/zeta ≈ 1.0 for Q2 projections** — unexpected and not predicted by Route B alone. Chi3 zeros carry nearly identical Q2 log-prime SNR as zeta zeros for all unramified primes (ratio 0.90–1.05), while chi4/zeta ≈ 0.23 for the same projection. The mechanism is unknown.

2. **Three-gap layer structure** — the bilateral sedenion product generates a three-gap statistic s_n = g_{n+1}(g_n + g_{n+2}) whose Act/GUE variance ratio is **1.02** (actual zeros match GUE), contrasting sharply with the two-gap Act/GUE = **0.65** (actual zeros tighter than GUE). The bilateral product reveals a multi-scale correlation structure invisible to single projections.

3. **E8 subspace expansion** — Phase 17 Q-vectors q2 and q4 lie on the E8 first shell and are provably outside the 4D subspace spanned by the P-vectors, expanding arithmetic coverage to 6 dimensions. The bilateral annihilation condition P·Q = 0 now has a candidate geometric interpretation: each (P,Q) pair is related by a single Weyl reflection in W(E8).

**Phase 18 resolves these threads in order:**
- **18E** — E8 Gram matrix + geometric substructure (first deliverable; pure computation)
- **18A** — chi3/zeta Q2 anomaly: conductor survey
- **18B** — Three-gap layer structure: vector part of sedenion product + n-gap generalization
- **18C** — AIEX-001 operator construction with Q-vector component (theoretical)
- **18F** — Framework-independence empirical probe

**Algebraic foundation (Canonical Six v1.3):**

The 8D images of the bilateral pairs (P,Q) form a combined 8-root set:

| Root | 8D coordinates | Form | Type |
|------|---------------|------|------|
| v1 | (0, +1, 0, 0, 0, 0, −1, 0) | e2−e7 | difference |
| q3 = −v1 | (0, −1, 0, 0, 0, 0, +1, 0) | e7−e2 | difference |
| v2 | (0, 0, 0, +1, −1, 0, 0, 0) | e4−e5 | difference |
| v3 = −v2 | (0, 0, 0, −1, +1, 0, 0, 0) | e5−e4 | difference |
| v4 | (0, +1, 0, 0, 0, 0, +1, 0) | e2+e7 | sum |
| v5 | (0, 0, +1, 0, 0, +1, 0, 0) | e3+e6 | sum |
| q2 | (0, 0, −1, 0, 0, +1, 0, 0) | e6−e3 | difference |
| q4 | (0, 0, 0, +1, +1, 0, 0, 0) | e4+e5 | sum |

All 8 roots have ‖v‖² = 2 — they all lie on the E8 first shell (lattice radius √2).

**Empirically established spectral rule (from Phases 15D and 17):**
- Difference roots (eᵢ−eⱼ) → high-pass or broadband filter character
- Sum roots (eᵢ+eⱼ) → low-pass or ultra-low-pass filter character

---

## Phase 18E — E8 Gram Matrix and Geometric Substructure

*This is Phase 18's first concrete deliverable. It requires only Python/NumPy — no CAILculator. Complete before 18A or 18B.*

### Script: `rh_phase18e_gram_matrix.py`

### What the script computes:

**18E-i: Full Gram matrix of the 8-root set**

Compute all 28 pairwise inner products of the 8 roots listed above. The Gram matrix determines whether this set contains a named root subsystem of E8. Several entries are already known by inspection (antipodal pairs give −2; orthogonal pairs give 0), but the full 8×8 matrix is needed to classify the structure.

Candidates for the root subsystem type: A₁ × A₁ × A₁ × A₁, D₄, or other. The asymmetry (v4 = e2+e7 and q4 = e4+e5 have no antipodal partners in the set) rules out any root system requiring antipodal closure — investigate what named structure fits.

**18E-ii: Subspace rank verification**

Confirm via rank computation that:
- The 5 P-vectors span a 4D subspace (v3 = −v2 creates a linear dependency)
- Adding q2 and q4 expands this to a 6D subspace (q2 and q4 are outside span of P-vectors)
- The full 8-root set spans at most 6D (since many roots are ±pairs)

Report the coordinate matrix rank and the two independent directions q2 and q4 add.

**18E-iii: Weyl reflection structure**

For each bilateral pair (Pᵢ, Qᵢ), verify that the Q-vector 8D image is the image of the P-vector 8D image under a specific simple Weyl reflection:

| Pattern | P_8D | Q_8D | Proposed Weyl reflection |
|---------|------|------|--------------------------|
| 1 | v2 | q1=v2 | identity |
| 2 | v2 | q2 | reflection through e3 (flip sign on component 3) |
| 3 | v3=−v2 | q3=−v1 | global sign followed by swap? (verify) |
| 4 | v2 | q4 | reflection through e5 (flip sign on component 5) |
| 5 | v5 | q2 | reflection through e3 (flip sign on component 3) |
| 6 | v1 variant | q3 | (verify) |

For each case: compute σ_α(P_8D) where σ_α is the Weyl reflection through root α, and confirm it equals Q_8D. The Weyl reflection formula is: σ_α(v) = v − 2(v·α/α·α)α.

**18E-iv: P⊥Q orthogonality table**

For all 6 bilateral pairs, compute the 8D inner product P_8D · Q_8D. Expected: all zero (verified by inspection for patterns 1–4 in `RH_Phase17_E8_Implications.md`). Confirm for patterns 5 and 6.

**18E-v: Spectral filter rule analytic derivation (partial)**

Expand the embed_pair projection for a general difference root (eᵢ−eⱼ) and a general sum root (eᵢ+eⱼ):

- embed_pair(g1, g2) = [g1, g2, g1−g2, g1g2/s, (g1+g2)/2, g1/s, g2/s, (g1−g2)²/s] where s = g1+g2
- Projection of difference root eᵢ−eⱼ: component_i − component_j
- Projection of sum root eᵢ+eⱼ: component_i + component_j

For each of the 6 (P,Q) pairs, write out the symbolic projection function explicitly (as a function of g1 and g2). Then compute the discrete Fourier transform of the resulting sequence analytically — at minimum, determine the DC component (α=0) and compute the sign/parity of the function to predict high-pass vs low-pass behavior. Full DFT derivation is a Lean 4 target; the Python script should produce the symbolic expansions and numerical spectral envelopes as verification.

### Output file: `p18e_gram_matrix_results.json`

```json
{
  "experiment": "Phase 18E",
  "gram_matrix": [[...8x8...]],
  "gram_matrix_labels": ["v1", "q3", "v2", "v3", "v4", "v5", "q2", "q4"],
  "subspace_rank_p_only": 4,
  "subspace_rank_p_plus_q": 6,
  "weyl_reflection_verification": {
    "pattern_1": {"reflection": "identity", "error": 0.0},
    "pattern_2": {"reflection": "sigma_e3", "error": 0.0},
    ...
  },
  "bilateral_orthogonality": {
    "pattern_1": 0.0, "pattern_2": 0.0, ...
  },
  "root_subsystem_candidate": "TBD",
  "spectral_filter_expansions": {
    "v1": "g1 - g2·(1/s)",
    "q2": "...",
    ...
  }
}
```

### Key questions:

1. What named root subsystem do the 8 roots form (or do they form no standard subsystem)?
2. Is the bilateral annihilation (P·Q = 0 in 16D sedenion) exactly equivalent to geometric orthogonality (P_8D · Q_8D = 0)? If both are zero for all 6 patterns, the correspondence is exact — but it may be coincidental or it may be a theorem.
3. Does the Weyl reflection conjecture hold for all 6 patterns?
4. Does the symbolic spectral expansion confirm difference roots → high-pass and sum roots → low-pass?

---

## Phase 18A — chi3/zeta ≈ 1.0 for Q2: Conductor Survey

*Depends on: 18E complete (for geometric context). Requires python-flint.*

### Script: `rh_phase18a_conductor_survey.py`

### Background:

Phase 17 found that chi3/zeta Q2 ratio ≈ 0.90–1.05 for all unramified primes (p=5..23), while chi4/zeta Q2 ≈ 0.23. This asymmetry is projection-specific: chi3/zeta for Q4 is ≈ 0.24 (not ≈ 1.0). The chi3 anomaly must be caused by something specific to the q2 = e6−e3 = (0,0,−1,0,0,+1,0,0) direction.

**Candidate mechanism:** chi3 has conductor 3, the minimal odd prime. In the E8 root coordinate system, the nonzero components of q2 are at positions 3 and 6. The connection may be that coordinate positions 3 and 6 in the E8 embedding have a special relationship with the prime 3 — encoding it at the level of individual lattice coordinates, not just globally.

**Route B prediction:** All unramified primes should appear for any L-function sharing the same root conductor structure. Route B does NOT predict the chi/zeta ratio for unramified primes — only that ramified primes are suppressed. The chi3/zeta ≈ 1.0 finding is outside Route B's scope and requires a new mechanism.

### What the script computes:

**18A-i: Compute zeros for small-conductor Dirichlet L-functions**

Using python-flint (Hardy Z-function + sign change + bisection, as in Phase 16B):
- chi_5 zeros (conductor 5): compute ~1,500 zeros to t ≈ 1500
- chi_7 zeros (conductor 7): compute ~1,500 zeros to t ≈ 1500
- chi_8 (the non-principal character mod 8, conductor 8): compute ~1,500 zeros to t ≈ 1500

For each: extract the imaginary parts, sort, compute gaps.

**18A-ii: Q2 and Q4 log-prime DFT SNR profiles**

Apply the same log-prime DFT pipeline as Phase 17 to all three new L-function zero sets, using both q2 and q4 projections. Also apply spacing ratio (SR) projection for comparison.

**18A-iii: chi/zeta ratio table**

For each prime p = 2, 3, 5, 7, 11, 13, 17, 19, 23 and each L-function (chi3, chi4, chi5, chi7, chi8, zeta), compute SNR and the ratio chi/zeta. Build a complete table.

**Prediction / decision criteria:**

| Outcome | Interpretation |
|---------|---------------|
| chi5/zeta Q2 ≈ 1.0 (similar to chi3) | Anomaly is conductor-independent — chi3 is not special |
| chi5/zeta Q2 ≈ 0.23 (similar to chi4) | chi3's ≈ 1.0 is conductor-specific — something about conductor 3 vs others |
| chi/zeta Q2 ratio tracks conductor size | E8 coordinate-prime correspondence hypothesis supported |
| chi/zeta Q2 ratio tracks character table chi(3) | Route B extension: Q2 encodes |chi(p)|², not just zero/nonzero |

**Character table values for context:**

| chi | mod | chi(2) | chi(3) | chi(5) | conductor |
|-----|-----|--------|--------|--------|-----------|
| chi4 | 4 | 0 | −1 | +1 | 4 |
| chi3 | 3 | +1 | 0 | +1 | 3 |
| chi5a | 5 | +1 | −1 | 0 | 5 |
| chi7a | 7 | +1 | +1 | −1 | 7 |
| chi8 | 8 | 0 | +1 | −1 | 8 |

If the Q2 chi/zeta ratio correlates with |chi(conductor prime)|², that would be a new Route B consequence: the Q2 projection encodes not just the Euler product structure but the specific character values at the root prime.

### Output file: `p18a_conductor_results.json`

```json
{
  "experiment": "Phase 18A",
  "l_functions": {
    "chi5": {"zero_count": 1500, "gaps_count": 1499},
    "chi7": {...},
    "chi8": {...}
  },
  "snr_table": {
    "q2": {
      "zeta": {"p2": 418.7, "p3": ..., "p5": ..., ...},
      "chi3": {"p2": "suppressed", "p5": ..., ...},
      "chi5": {...},
      ...
    },
    "q4": {...}
  },
  "chi_zeta_ratios": {
    "q2": {
      "chi3": {"p5": 0.95, "p7": 1.02, ...},
      "chi4": {"p5": 0.23, ...},
      "chi5": {...},
      ...
    }
  },
  "interpretation": "..."
}
```

### Key questions:

1. Is chi3's Q2 anomaly unique among small-conductor L-functions, or do others share it?
2. Does the chi/zeta ratio for Q2 track the character value at the conductor prime (|chi(p_0)|²)?
3. Does the chi3/Q2 anomaly persist for Q4 at larger scale? (Phase 17 showed it does not — verify at N≈1500.)

---

## Phase 18B — Three-Gap Layer Structure: Vector Part and n-Gap Generalization

*Depends on: Phase 17B code (`rh_phase17b_prep.py`) available. No new data required — uses rh_zeros_10k.json.*

### Script: `rh_phase18b_vector_part.py`

### Background:

Phase 17B-ii established that the scalar part of the sedenion product x_n · x_{n+1} (where x_n = g_n·P1 + g_{n+1}·Q1) gives the three-gap statistic s_n = g_{n+1}(g_n + g_{n+2}), with Act/GUE variance ratio = **1.02** — actual zeros match GUE exactly in this statistic, unlike the two-gap ratio of 0.65.

The full sedenion product has 16 components (1 scalar + 15 vector). Only the scalar part was analyzed. The vector part is **15 unexplored bilinear functions of consecutive gap triples** whose structure is determined by the sedenion multiplication table.

### What the script computes:

**18B-i: All 15 vector components of the sedenion product**

For each n, compute the full sedenion product x_n · x_{n+1} where x_n = g_n·P1 + g_{n+1}·Q1. Extract components 1–15 (the imaginary/vector part). For each component k, define the sequence {w_n^(k)} = Im_k(x_n · x_{n+1}).

For each of the 15 sequences, compute:
- Mean, variance, skewness, kurtosis
- Act/GUE variance ratio (compare to 1,000 GUE realizations)
- Act/Poisson variance ratio
- Chavez conjugation symmetry (CAILculator)

**18B-ii: n-gap generalization**

The two-gap statistic is a projection of a gap pair; the three-gap statistic is the scalar sedenion product of consecutive states. Generalize:

Define x_n^(k) = g_n·P1 + g_{n+1}·P2 + ... involving k consecutive gaps embedded using the bilateral zero divisor structure. For k=2 (two-gap): Act/GUE = 0.65. For k=3 (three-gap, scalar part): Act/GUE = 1.02. The transition point and rate carry information about the correlation length in the zero sequence.

Compute Act/GUE variance ratio for:
- k=2: two-gap linear projection (confirmed 0.65)
- k=3: three-gap scalar sedenion product (confirmed 1.02)
- k=3: three-gap, each of the 15 vector components (new)
- k=4: four-gap, using the natural sedenion extension (new): x_n · x_{n+1} · x_{n+2} scalar part

**18B-iii: Chavez Transform on three-gap + vector sequences (CAILculator)**

For the most discriminating vector components from 18B-i (highest |Act/GUE − 1| or highest |Act/Poi − 1|), extract 500-element samples and run the full Chavez Transform:
- alpha=1.0, dimension_param=2, pattern_id=1
- dimensions_tested=[1,2,3,4,5]

Compare CV and conjugation symmetry to the two-gap P2 reference (CV ≈ 0.146, sym ≈ 82–84%).

### Output file: `p18b_vector_part_results.json`

```json
{
  "experiment": "Phase 18B",
  "vector_components": {
    "component_1": {"act_gue_var_ratio": ..., "act_poi_var_ratio": ..., "skewness": ...},
    ...
    "component_15": {...}
  },
  "ngap_act_gue_ratios": {
    "k2_two_gap": 0.65,
    "k3_scalar": 1.02,
    "k3_vector_components": {...},
    "k4_scalar": "..."
  },
  "chavez_transform": {
    "most_discriminating_component": {...},
    "cv": 0.146,
    "conjugation_symmetry": ...
  }
}
```

### Key questions:

1. Which (if any) vector components show Act/GUE ≠ 1.0? Does the layer structure vary across the 15 imaginary directions of the sedenion product?
2. At what k does Act/GUE transition from <1 (actual tighter than GUE) to ≈1 (actual matches GUE)? Is k=3 the crossover, or does it continue rising above 1 for k≥4?
3. Do any vector components give Chavez CV ≈ 0.146 (the universal CV)? Or does the vector part break the universality seen in scalar projections?
4. Is there a sedenion imaginary direction that distinguishes actual zeros from GUE more sharply than any scalar projection?

---

## Phase 18C — AIEX-001 Operator Construction: Theoretical Summary

*No new scripts. This is the theoretical synthesis following 18E, 18A, 18B.*

### Questions to resolve after 18E and 18B are complete:

**From 18E:**
- Does the bilateral annihilation condition P·Q = 0 (16D algebraic) follow from or imply geometric orthogonality P_8D · Q_8D = 0 (8D Euclidean)? If this is a theorem, the AIEX-001 operator's self-adjointness has a purely geometric characterization in E8.
- If each (P,Q) bilateral pair is a Weyl reflection pair, then the operator H decomposes into contributions from each Weyl orbit of simple reflections — a known structure in representation theory.

**From 18A:**
- Does the chi3/Q2 anomaly encode character values at the conductor prime? If yes, the Q2 projection is reading something about the representation theory of the L-function, not just its Euler product zeros. This would constrain the AIEX-001 mechanism to include character structure, not just prime orbit phases.

**From 18B:**
- The bilateral sedenion product naturally generates multi-scale statistics (different Act/GUE at different k). This means the operator's natural eigenstates may correlate gaps at a specific scale — the scale where Act/GUE transitions from 0.65 to 1.02 may be a physically meaningful correlation length.

**Operator structure question (open):**
The P/Q split corresponds to a high-pass (P, p≥7) vs broadband (Q2, p=2..23) spectral decomposition of prime orbit content. Does this correspond to a short-range / long-range decomposition in the explicit formula for ζ(s)?

---

## Phase 18F — Framework-Independence Empirical Probe

*Depends on: 18E complete (geometry identifies which framework-dependent Q-vectors to probe first).*

### Background:

Phase 15C established that framework-dependent patterns (CD-only, failing Clifford) share P-vectors with Canonical Six patterns, making P-vector projections blind to the canonical/non-canonical distinction. Phase 17 delivered Q-vector access. 18F is the first test of whether framework-independence is empirically measurable.

The 6 framework-dependent patterns have Q-vectors in 16D sedenion space. Once 18E identifies their 8D projections and positions in the E8 root structure, we can apply them as projection directions to zeta gap sequences and compare log-prime DFT SNR profiles to Canonical Six Q-projections.

**Predicted outcomes:**

| Outcome | Interpretation |
|---------|---------------|
| Framework-dependent Q projections give identical SNR profiles to Canonical Six Q projections | The canonical/non-canonical distinction has no measurable spectral consequence via embed_pair |
| Framework-dependent Q projections give different SNR profiles (different primes detected, or different ratios) | Framework-independence is geometrically encoded in the Q-vector and experimentally measurable |
| Framework-dependent Q projections give null (no log-prime signal) | The canonical distinction is required for the arithmetic connection — framework dependence destroys the signal |

A null result here would be a strong statement: only Canonical Six Q-vectors connect to the Euler product. A positive result would be the first empirical probe of framework-independence outside of Lean 4 verification.

### Script: `rh_phase18f_framework_probe.py` *(pending 18E completion)*

---

## Theoretical Significance

### E8 Geometry (18E)

The 8-root set {v1, q3, v2, v3, v4, v5, q2, q4} may be the first explicit identification of a named E8 sub-geometric structure arising naturally from sedenion zero divisor algebra. The bilateral pairs (P,Q) satisfy both 16D algebraic annihilation and 8D geometric orthogonality — connecting the sedenion multiplication structure to E8 root geometry at two independent levels.

### Chi3/Zeta Anomaly (18A)

If chi3/zeta Q2 ≈ 1.0 is confirmed to be conductor-specific (chi3 unique; other L-functions do not replicate it), this is evidence that the Q2 projection direction (e6−e3 in E8 coordinates) encodes the prime 3 at the level of individual lattice coordinates. This would be a new mechanism beyond Route B: not just Euler product structure, but the specific arithmetic of each L-function's conductor is encoded geometrically in the E8 embedding.

### Multi-Scale Structure (18B)

The transition of Act/GUE variance ratio from 0.65 (k=2) to 1.02 (k=3) via the sedenion product is a new empirical fact about the GUE-like zero correlations. If vector components show additional Act/GUE values at k=3, the sedenion product is providing a 16-component decomposition of zero correlation structure — a spectral analysis tool that does not exist in standard RMT.

---

## Connection to AIEX-001

The Phase 18 results collectively constrain the AIEX-001 operator H as follows:

- **H must be built from (P,Q) bilateral pairs, not P-vectors alone** (established Phase 17; 18E provides the geometric reason)
- **H operates in a 6D subspace of the 8D E8 embedding space** (18E-ii will confirm this via rank)
- **H must encode character structure beyond raw Euler product** if the chi3/Q2 anomaly traces to conductor-prime correspondence (18A)
- **H's natural eigenstates correlate zeros at multiple scales** — the k=2 to k=3 Act/GUE transition defines the correlation length relevant to H's spectral structure (18B)
- **H's self-adjointness** may be derivable purely from E8 Weyl reflection geometry — the bilateral annihilation condition as a geometric orthogonality constraint (18E, Lean 4 target)

The functional equation ζ(s) = ζ(1−s̄) enforces a bilateral zero pairing ρ ↔ 1−ρ̄ — the same bilateral cancellation structure present in the Canonical Six annihilation P·Q = 0 and in the antipodal pair v2+v3 = 0. Phase 18E will determine whether these three bilateral conditions (functional equation, algebraic annihilation, geometric antipodality) are geometrically unified within the E8 root structure.

---

## Files

| File | Description |
|------|-------------|
| `rh_phase18e_gram_matrix.py` | E8 Gram matrix, rank, Weyl reflections, P⊥Q orthogonality, spectral filter expansions |
| `rh_phase18a_conductor_survey.py` | chi_5/chi_7/chi_8 zeros + Q2/Q4 conductor survey |
| `rh_phase18b_vector_part.py` | Vector part of sedenion product + n-gap Act/GUE generalization |
| `rh_phase18f_framework_probe.py` | Framework-dependent Q-vector probe (pending 18E) |
| `p18e_gram_matrix_results.json` | 18E outputs |
| `p18a_conductor_results.json` | 18A outputs |
| `p18b_vector_part_results.json` | 18B outputs |
| `RH_Phase18_Results.md` | Combined results document (post-analysis) |
| `RH_Phase18_Handoff.md` | This document |
| `RH_Phase17_E8_Implications.md` | Phase 17 E8 geometry analysis (prerequisite reading) |
| `rh_zeros_10k.json` | 10,000 zeta zeros (Phases 17–18 primary dataset) |
| `zeros_chi4_2k.json` | 2,092 chi_4 zeros (Phase 16B) |
| `zeros_chi3_2k.json` | 1,893 chi_3 zeros (Phase 16B) |

---

## Execution Order

```
1. rh_phase18e_gram_matrix.py     → p18e_gram_matrix_results.json
   (Pure computation, no CAILculator needed)

2. rh_phase18a_conductor_survey.py → p18a_conductor_results.json
   (Requires python-flint; ~5–10 min for ~1500 zeros per L-function)

3. rh_phase18b_vector_part.py     → p18b_vector_part_results.json
   (Uses rh_zeros_10k.json; CAILculator for Chavez Transform on selected sequences)

4. CAILculator: Run Chavez Transform on sequences flagged in p18b_vector_part_results.json

5. rh_phase18f_framework_probe.py → p18f_framework_results.json
   (After 18E geometry identifies framework-dependent Q-vector 8D projections)

6. Write RH_Phase18_Results.md combining all outputs
```

---

*Chavez AI Labs LLC · Applied Pathological Mathematics*
*"Better math, less suffering"*
