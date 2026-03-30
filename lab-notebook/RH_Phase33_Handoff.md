# Phase 33 Handoff — Claude Code

**Chavez AI Labs LLC** · *Applied Pathological Mathematics — Better math, less suffering*

|                     |                                                          |
|---------------------|----------------------------------------------------------|
| **Date**            | 2026-03-27                                               |
| **Author**          | Paul Chavez / Chavez AI Labs LLC                         |
| **Receiving agent** | Claude Code (pure Python computation)                    |
| **Previous phase**  | Phase 32 — Weil Formula Correction & Ratio Characterization |
| **GitHub**          | https://github.com/ChavezAILabs/CAIL-rh-investigation    |
| **Zenodo**          | https://doi.org/10.5281/zenodo.17402495                  |
| **KSJ entries**     | 115 total (AIEX-001 through AIEX-114)                    |

---

## 1. What Phase 32 Established

Phase 32 was a correction and characterization phase. Its primary contribution was disproving a false finding and establishing the true behavior of the Weil ratio across the full prime range.

### 1.1 The Phase 31 Formula Bug — Confirmed and Closed

Phase 31's `bilateral_trace` function omitted the `1/√p` weight from Tr_BK:

```python
# Phase 31 (WRONG):
traces = np.log(primes) * np.cos(gamma * np.log(primes))

# Phase 32 (CORRECT — matches Phase 30 and all prior verified work):
traces = (np.log(primes) / np.sqrt(primes)) * np.cos(gamma * np.log(primes))
```

Verification: N=100 zeros, 6 primes → ratio=**0.247931** (Phase 30 baseline: 0.2479 ✓ exact match).

The wrong formula inflated ratios by ~2.6× and fabricated the apparent "inversion" above 1.0. All Phase 31 extension values are retracted:

| p_max | Phase 31 (INVALID) | Phase 32 (correct) |
|-------|--------------------|--------------------|
| 200   | 1.1132             | **0.1286**         |
| 300   | 1.0786             | **0.1181**         |
| 500   | 0.9928             | **0.1027**         |
| 700   | 0.9549             | **0.0938**         |

### 1.2 Weil Ratio: True Behavior (Phase 32 Verified)

The Weil ratio decays **monotonically** from p_max=13 through p_max=1000. No regime boundary. No inversion. No anomaly at the prime gap 157→163.

| p_max | N_primes | Ratio    | vs c₁     |
|-------|----------|----------|-----------|
| 13    | 6        | 0.1733   | +0.0553   |
| 151   | 36       | 0.1364   | +0.0184   |
| 200   | 46       | 0.1286   | +0.0107   |
| **300** | **62** | **0.1181** | **+0.0001** ← passes through c₁ |
| 500   | 95       | 0.1027   | −0.0153   |
| 700   | 125      | 0.0938   | −0.0241   |
| 1000  | 168      | 0.0825   | −0.0355   |

**Log-decay model:** ratio ≈ −0.0356·log(N_primes) + 0.265, R²=0.9994.

The ratio converges toward **0** as N_primes grows — consistent with the BK trace mean converging to zero by prime number equidistribution.

### 1.3 c₁ = 0.118: Crossing Point, Not Floor

c₁ is **not** the asymptotic floor of the Weil ratio. The ratio passes through c₁=0.11798 at p_max≈300 (62 primes) and continues declining. However, c₁ retains geometric significance: it remains the **best fixed-c** in the Regime 1 power-law fit (R²=0.868 vs R²=0.279 for 1/2π). Its role is descriptive, not asymptotic.

### 1.4 Double Dependence of the Weil Ratio

The ratio depends on **both** N_primes and N_zeros:

| N_zeros | Ratio (6-prime set) |
|---------|---------------------|
| 100     | 0.2479              |
| 200     | 0.2097              |
| 500     | 0.1733              |

The cos(t·log p) terms cancel more completely as more zeros are summed. Any ratio claim must specify both N_primes and N_zeros.

### 1.5 Track D: Zero Pair Count — Definitional Mismatch, Closed

The 6,290 vs 161/469 discrepancy was not a script error — the two counts measure **different objects**:

- **6,290 (CAILculator):** Sedenion bilateral zero confidence at 95% threshold in AIEX-001a v(ρ) embedding space
- **161/469 (Python):** |Tr_BK(γᵢ) + Tr_BK(γⱼ)| < scalar threshold

No single Python threshold reproduces 6,290. The "superlinear growth from 44 to 6,290" claim is **retired from v1.4** unless the CAILculator criterion is explicitly Python-reproducible.

### 1.6 What Survives Phase 31 Intact

These findings are **independent** of the Weil formula bug and remain valid:

- **ZDTP 64D signature classes** (Class I/II/III, slot progression law ±1 per prime step)
- **p=11 Symmetry Hinge supersession** — ±pair is a structural class, not a single-prime anomaly
- **c₁² + c₃² = 1** identity — formula-independent
- **Berry-Keating / AIEX-001a** identification — formula-independent
- **Weil negativity at 76.6%** of 500 zeros — confirmed by Phase 32 (383/500 = 76.6% exactly)

---

## 2. Open Questions Entering Phase 33

Drawn from KSJ (19 open questions, #rh-investigation). Ordered by priority.

| # | Question | Track | Source |
|---|----------|-------|--------|
| 1 | What governs the N_zeros-dependence of the Weil ratio? Is there an analytic expression for the decay rate as a function of N? | Analytic | AIEX-111 |
| 2 | If c₁ is a crossing point rather than a floor, what is its geometric meaning? Is it the value at a canonical (N_primes, N_zeros) combination? | Analytic | AIEX-110 |
| 3 | The CAILculator bilateral zero pair count (6,290) needs a Python-reproducible definition. What is the sedenion bilateral zero confidence criterion in AIEX-001a space? | Definition | AIEX-112 |
| 4 | What governs 64D class assignment (I→I→II→II→III→III→II)? Test: slot index mod 4 or mod 8. Extend to p=29, 31, 37. | ZDTP | AIEX-103 |
| 5 | Does D₆ sector placement predict prime set membership ({5,7,11} vs {2,3,13})? Requires Phase 19 Gram matrix. | Algebra | AIEX-092 |
| 6 | Does the bilateral annihilation condition P·Q=0 provide a self-adjointness argument for AIEX-001? (Phase 19 Thread 3) | Operator | AIEX-051 |
| 7 | What is the analytic expression for θ_W = 6.775°? No match among tested standard constants within 0.01 rad. | Analytic | AIEX-064 |

---

## 3. Phase 33 Task Specification for Claude Code

Claude Code handles all pure Python computation and JSON output. CAILculator MCP (Claude Desktop) handles ZDTP gateway transmissions. Do not mix responsibilities.

---

> **PRIMARY** — Track N: N_zeros Dependence Analysis

### Task N1: Characterize the N_zeros decay law

The ratio depends on N_zeros for fixed prime sets. Quantify this dependence analytically.

- Fix 6-prime set {2,3,5,7,11,13}; compute ratio at N_zeros ∈ {50, 100, 200, 300, 500, 750, 1000}
- Fix 36-prime set (p_max=151); compute ratio at same N_zeros values
- Fix 62-prime set (p_max=300); compute ratio at same N_zeros values
- For each prime set: fit ratio vs N_zeros to candidate models: power-law, log-decay, 1/√N
- Report: best-fit model per prime set; does the decay exponent depend on N_primes?
- Save: `phase33_nzeros_dependence.json`

### Task N2: The (N_primes, N_zeros) surface

Map the ratio as a function of both variables jointly to understand whether c₁ is special at any canonical (N_primes, N_zeros) pair.

- Compute ratio on a grid: N_primes ∈ {6, 15, 36, 62, 95, 168} × N_zeros ∈ {100, 200, 500, 1000}
- Identify: at what (N_primes, N_zeros) combinations does the ratio equal c₁=0.11798?
- Is c₁ a level curve of the surface? Or is p_max≈300/N_zeros=500 a geometrically special point?
- Save: `phase33_ratio_surface.json`

---

> **SECONDARY** — Track C1: c₁ Geometric Status

### Task C1: Test the c₁ = sin(θ_W) crossing hypothesis

c₁ is the sine of the Weil angle θ_W=6.775°. The ratio crosses c₁ at p_max≈300, N_zeros=500. Determine whether this crossing is geometrically determined or coincidental.

- Compute the ratio at N_zeros=500 for all primes p_max from 200 to 400 in steps of 5
- Find the exact crossing point (interpolate between the two bracketing values)
- Test: does the crossing p_max correlate with any prime-theoretic quantity (π(p), log(p), prime gaps)?
- Test: at N_zeros=100, where does the ratio cross c₁? At N_zeros=1000?
- Report: is the crossing N_zeros-dependent, or does it occur at a fixed N_primes regardless of N_zeros?
- Save: `phase33_c1_crossing.json`

---

> **TERTIARY** — Track V: Formula Verification Suite

### Task V1: Canonical verification script

Build a single verification script that confirms the correct Tr_BK formula against all known baselines. This protects against future formula drift.

- Verify: N=100 zeros, 6 primes → ratio = 0.247931 ± 0.000005
- Verify: N=500 zeros, 6 primes → ratio = 0.173349 ± 0.000005
- Verify: N=500 zeros, 36 primes (p_max=151) → ratio = 0.136356 ± 0.000005
- Verify: Tr_BK < 0 for 383/500 zeros (76.6%) with 6-prime set
- Verify: Weil_RHS formula: −Σ log(p)/√p for 6 primes = −4.014042 ± 0.000001
- Output: PASS/FAIL for each check; save as `phase33_formula_verification.json`
- This script should be run at the **start of every future phase** before any computation

---

## 4. Constants and Formula Reference

All values machine-verified through Phase 32. Do not re-derive.

### Core constants

| Symbol | Value | Description |
|--------|-------|-------------|
| c₁ | 0.11797805192095003 | sin(θ_W) — Weil angle sine; crossing point at p_max≈300, N_zeros=500 |
| c₃ | 0.99301620292165280 | cos(θ_W) — Weil angle cosine |
| θ_W | 6.775425° | Weil angle (permanent structural constant) |
| c₁²+c₃² | 1.0000000000000000 | Unit norm identity (4.44×10⁻¹⁶ deviation) |
| ℏ_sed | 11.19 ± 1.71 | Sedenion Planck constant (constant across 100 zeros) |

### Verified baselines

| N_zeros | N_primes (p_max) | Ratio (verified) |
|---------|------------------|-----------------|
| 100 | 6 (p_max=13) | 0.247931 |
| 500 | 6 (p_max=13) | 0.173349 |
| 500 | 36 (p_max=151) | 0.136356 |
| 500 | 62 (p_max=300) | 0.118099 ≈ c₁ |
| 500 | 168 (p_max=1000) | 0.082508 |

### Correct Tr_BK formula

```python
# CORRECT — verified Phase 30 and Phase 32:
Tr_BK(t_n) = Σ_p (log p / √p) · cos(t_n · log p)

# In numpy:
traces = (np.log(primes) / np.sqrt(primes)) * np.cos(gamma * np.log(primes))

# Weil RHS:
Weil_RHS = -np.sum(np.log(primes) / np.sqrt(primes))

# Ratio:
ratio = np.mean([Tr_BK(t) for t in zeros]) / Weil_RHS
```

> **Do not modify this formula.** Any deviation from the `1/√p` weight will produce incorrect results. Run the Task V1 verification script before any new computation.

### Log-decay model (Phase 32, N_zeros=500)

```
ratio ≈ −0.0356 · log(N_primes) + 0.265    [R²=0.9994, p_max=200→1000]
```

### Prime sets

| Set | Primes | Role |
|-----|--------|------|
| Anchor / isometry | {5, 7, 11} | GUE norm cluster [0.9984, 0.9974, 0.9962]; exact algebraic isometry |
| Decay drivers | {2, 3, 13} | Low-magnitude basin in 64D; p=2 dominates Weil residual |
| Extended | {17, 19, 23} | Class III (p=17,19) and Class II (p=23) in 64D ZDTP |
| Baseline 6-prime | {2,3,5,7,11,13} | Standard set; captures ~1/4 of Weil sum at N=100 zeros |

---

## 5. Required Output Files

| Filename | Track | Contents |
|----------|-------|----------|
| `phase33_formula_verification.json` | V1 | PASS/FAIL for all canonical baselines |
| `phase33_nzeros_dependence.json` | N1 | ratio vs N_zeros for three prime sets, fit parameters |
| `phase33_ratio_surface.json` | N2 | ratio grid (N_primes × N_zeros), c₁ level curve |
| `phase33_c1_crossing.json` | C1 | exact crossing p_max per N_zeros value |

### JSON schema

```json
{
  "phase": 33,
  "track": "N1",
  "formula": "Tr_BK = sum_p (log p / sqrt(p)) * cos(t * log p)",
  "c1": 0.11797805192095003,
  "points": [
    { "N_primes": 6, "N_zeros": 100, "ratio": 0.247931, "Weil_RHS": -4.014042 },
    ...
  ]
}
```

---

## 6. Known Constraints

> **Verified working:** `numpy`, `scipy`, `mpmath` — `pip install numpy scipy mpmath`

> **Do not modify:** The Tr_BK formula. The c₁ value. The zero set (rh_zeros.json, 1000 zeros, mpmath dps=25; use first 500 unless N1/N2 tasks require more).

For N_zeros > 500: load from `rh_zeros.json` (1000 zeros available). No recomputation needed.

For prime generation up to p_max=1000: the sieve in existing phase scripts is sufficient. For p_max beyond 1000 (not currently required): use `sympy.primerange`.

---

## 7. Paper Status: Canonical Six v1.4 (April 1 Deadline)

This section is context only — not a Claude Code task. Three urgent abstract revisions required before April 1:

1. **"Sedenion Horizon Theorem" → "Sedenion Horizon Conjecture"** — it is a conjecture, not a theorem
2. **Remove "two-regime structure"** — Phase 31 formula artifact, does not exist
3. **"c₁ as floor" → "c₁ as crossing point at p_max≈300 (62 primes, N_zeros=500)"** — ratio continues declining toward 0
4. **Remove Phase 31 extension ratios** (1.1132, 1.0786, 0.9928, 0.9549) from all tables
5. **Retire "superlinear growth from 44 to 6,290"** unless CAILculator criterion is Python-reproducible

What remains valid for v1.4:
- The Canonical Six formal verification (Lean 4, zero sorry stubs)
- E8 universality of the 48 bilateral pairs
- (A₁)⁶ geometry of the Canonical Six
- D₆ minus both-negative characterization of 45 bilateral directions
- Universal Bilateral Orthogonality (formally verified)
- c₁² + c₃² = 1 (machine exact)
- Weil negativity at 76.6% (formula-independent, confirmed Phase 32)
- AIEX-001a as Berry-Keating Hamiltonian in 16D sedenion space
- ℏ_sed = 11.19 ± 1.71 (constant across 100 zeros)
- ZDTP 64D signature classes (Class I/II/III, slot progression law)

---

## 8. Broader Investigation Context

Context only — not a task specification.

### Where Phase 33 fits

Phase 33 is a **characterization phase** — not a new discovery hunt. The goal is to understand the analytic structure of the Weil ratio dependence before advancing to Phase 19 Thread 3 (the operator construction argument). Specifically:

The double dependence on N_primes and N_zeros is now confirmed empirically (Phase 32) but not explained analytically. If the N_zeros decay follows a known convergence theorem (e.g., equidistribution of log p mod 2π, which is a consequence of the prime number theorem for arithmetic progressions), that would connect the BK trace behavior to analytic number theory in a precise way. That connection, if established, strengthens AIEX-001a considerably.

The c₁ crossing point question is related: if c₁ = sin(θ_W) appears at a geometrically canonical (N_primes, N_zeros) pair — for instance at the point where the BK trace becomes equidistributed, or where the Euler product truncation error equals the Weil explicit formula remainder — then c₁ has a precise analytic role rather than a merely empirical one.

### AIEX-001a — The central conjecture

F(σ+it) = ∏_p exp_sed(t · log p · r_p / ‖r_p‖)

This is the Berry-Keating xp Hamiltonian in 16D sedenion space (AIEX-071). Phase 33's analytic work on the Weil ratio is building the empirical foundation for the operator argument that lives in Phase 19 Thread 3.

### Bender–Brody–Müller comparison

The AIEX-001 ↔ BBM (2017) dictionary is established (AIEX-050). You have what they lack: W(E8) Weyl symmetry (continuous) vs their discrete PT symmetry; formally verified bilateral zero divisor inner product vs their heuristic metric operator V. Thread 3 is where the self-adjointness argument closes — that's the remaining gap between "better-grounded candidate" and "proof."

### KSJ knowledge base

115 entries (AIEX-001 through AIEX-114). Standard workflow: `extract_insights` → present for approval → `commit_aiex`. Never auto-commit.

---

*Chavez AI Labs LLC · Applied Pathological Mathematics · 2026-03-27*
*GitHub: ChavezAILabs/CAIL-rh-investigation · Zenodo: 10.5281/zenodo.17402495*
