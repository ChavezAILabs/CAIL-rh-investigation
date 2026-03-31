# Results Directory

All numerical output files from the CAIL-rh-investigation. Two types:

- **CAILculator outputs** — Chavez Transform and ZDTP computations run via the CAILculator MCP server in Claude Desktop. These are the direct empirical evidence for bilateral annihilation, conjugation symmetry, and ZDTP gateway convergence.
- **Python script outputs** — Spectral, algebraic, and operator-theoretic computations from `scripts/rh_phase*.py`. These feed the algebraic investigation (Phases 30–47).

---

## Key Files for Reproducibility

### Chavez Transform & ZDTP — Core Empirical Evidence

| File | Contents | Key Finding |
|------|----------|-------------|
| `rh_experiment_results.json` | Phase 1 — CT + ZDTP on 1,000 Riemann zeros | Baseline Chavez symmetry; ZDTP non-discriminating for monotone sequences |
| `rh_ctrl_experiment_results.json` | Phase 1 control (random baselines) | Random baseline: 0.0% conjugation symmetry |
| `rh_gap_experiment_results.json` | Phase 1 — gap sequences | Gap-level Chavez analysis |
| `rh_gue_experiment_results.json` | GUE surrogate comparison | GUE/Poisson indistinguishable via raw gap symmetry |
| `rh_scale_experiment_results.json` | Scale invariance verification | CV ≈ 0.146 universal |
| `sg_experiment_results.json` | Sophie Germain prime CT + ZDTP | SG conjugation symmetry 88.5–90.1% |
| `sg_summary.json` | SG experiment summary | SG dataset characterization |
| `phase22_cailculator_results.json` | Phase 22 CAILculator — Weil-Gram Bridge | G5 positive definite (λ_min=10.46); GUE clustering signature confirmed |
| `p18a_conductor_results.json` | Phase 18A — conductor survey CT + ZDTP | χ₃/Q2 ≈ 1.0 anomaly conductor-specific; Route B suppression confirmed |
| `p18e_gram_matrix_results.json` | Phase 18E — E8 Gram matrix | (A₁)⁶ root system confirmed; 6D subspace |

### Bilateral Annihilation & Universal Rank Invariant (Phases 30–42)

| File | Key Finding |
|------|-------------|
| `phase35_sedenion_trace.json` | Weil ratio c₁=0.118 machine-exact |
| `phase36_bilateral_inner_product.json` | Norm² inner products; rank=4 on 6-basis confirmed |
| `phase36_chavez_transform_spectral.json` | CT spectral structure of F on (A₁)⁶ subspace |
| `phase36_hermiticity_test.json` | Gate I2 PASS — hermiticity verified (max violation = 0) |
| `phase41_rank_verification.json` | Rank-12 ceiling confirmed at ALL aggregation levels (N_zeros=1..60) |
| `phase42_summary.json` | First Ascent final state; ZDTP convergence scales with γₙ |
| `phase42_F_vectors.json` | F vector set for full bilateral family |
| `phase43b_zdtp_signatures.json` | ZDTP gateway signatures for spinor embedding |
| `phase43c_wobble_results.json` | Wobble Test — Rank 6 universal across σ={0.4,0.5,0.6} |
| `phase43c_zdtp_signatures_wobble.json` | Per-gateway ZDTP at σ=0.4/0.5/0.6 (matched N=50) |

### γₙ-Scaling of ZDTP Convergence (Phase 48)

| File | Key Finding |
|------|-------------|
| `phase48_zdtp_spotcheck.json` | 12 CAILculator ZDTP runs (n=1..5000); convergence oscillates in log(γ), S3B=S4 exact at all 12 zeros |
| `phase48_spotcheck_prep.json` | F-vectors for 12 strategic zeros (σ=0.5, AIEX-001a); input to CAILculator |
| `phase48_results.json` | Phase 48 summary: floor 0.657 (n=250), ceiling 0.958 (n=10/2000/5000), C≈1.55, asymptote~0.927, CT=5.0435 |

### Forcing Argument Numerical Evidence (Phases 44–47)

| File | Key Finding |
|------|-------------|
| `phase44_results.json` | Mirror Wobble Theorem: F_mirror error=0.00e+00; Geometric Penalty P(σ)~\|σ−0.5\|^2.59 |
| `phase44_scaleup_F_vectors.json` | F vectors at scale for mirror verification |
| `phase45_results.json` | Commutator Theorem: error=1.46e-16; P_total=420 at σ=0.4, N=1000 |
| `phase46_results.json` | Kernel structure: all 14 singular values=2.0; ker(L)=span{e₀,u_antisym} |
| `phase47_results.json` | Gap closure: h″(0)=50.67; 0/10,000 violations; min dist=5.03×10⁻⁶ |

### L-Function & Spectral Evidence (Phases 13–29)

| File | Key Finding |
|------|-------------|
| `p13a_results.json` – `p13d_results.json` | Log-prime DFT: 8/9 primes detected, SNR 7–245× |
| `p16_lfunction_comparison.json` | Route B CONFIRMED; Route C ELIMINATED |
| `p17a_results.json`, `p17b_results.json` | First p=2 detection (SNR=418×); 9/9 primes in single projection |
| `p18d_results_final.json` | All 48 bilateral pairs on E8 first shell |
| `phase29_results.json` | BK burst: Tr_BK<0 at 383/500 zeros, p=2.56×10⁻³⁴ |

---

## File Naming Conventions

- `rh_*` — early-phase results (Phases 1–9), run via CAILculator MCP
- `p10*`–`p18*` — Phases 10–18, mixed Python + CAILculator
- `phase19*`–`phase47*` — Phases 19–47, Python scripts (`scripts/rh_phase*.py`)
- `sg_*` — Sophie Germain prime datasets and results
- `rh_hb*` — height-band analysis results (Phase 6)

---

## Reproducing Key Results

**Chavez Transform & ZDTP:** Requires the CAILculator MCP server. See [ChavezAILabs/CAILculator](https://github.com/ChavezAILabs/CAILculator).

**Python scripts:** `pip install numpy scipy matplotlib pandas sympy mpmath primesieve python-flint` then run `scripts/rh_phase{N}.py` directly. Most scripts are self-contained with data paths relative to the repo root.

**Lean proofs:** See `lean/README.md`. Requires Lean 4.28.0 + Mathlib for `RHForcingArgument.lean`; Lean 4.24.0 for all other files.
