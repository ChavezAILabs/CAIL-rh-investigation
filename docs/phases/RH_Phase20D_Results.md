# Phase 20D Results — Near-Miss Pair Diophantine Analysis
## Chavez AI Labs LLC · March 24, 2026

**Status:** COMPLETE
**Script:** `rh_phase20d.py`
**Output:** `phase20d_results.json`

---

## Headline

The near-miss pair (ρ₅₄, ρ₉₈) with |cos θ| = 0.9928 has a ratio spread **125× tighter** than a generic pair — but the ratios are NOT near a common constant. The near-proportionality is driven by **Block B and Block C** (primes 2, 3, 5) being roughly proportional, while **Block A** (primes 7, 11, 13) exhibits wild per-prime variation. The Diophantine structure shows no prime with a near-integer Δt/log p — the near-miss is a multi-prime amplitude coincidence, not a single-prime resonance.

---

## Pair Zero Values

| Zero | t value |
|---|---|
| ρ₅₄ | 150.925257612241467 |
| ρ₉₈ | 231.987235253180245 |
| **Δt** | **−81.061977640939** |

---

## Analysis 1: Ratio Table

For each prime p, the ratio λ_p = cos(t₅₄ · log p) / cos(t₉₈ · log p):

| Prime | Block | cos(t₅₄·log p) | cos(t₉₈·log p) | λ_p |
|---|---|---|---|---|
| 2 | C | −0.58909394 | −0.83642280 | **+0.70430** |
| 3 | B | −0.76736936 | −0.92298790 | **+0.83140** |
| 5 | B | −0.53845211 | −0.88677587 | **+0.60720** |
| 7 | A | −0.05189925 | +0.57103801 | **−0.09089** |
| 11 | A | −0.81399081 | −0.97607279 | **+0.83394** |
| 13 | A | −0.76500570 | −0.29198139 | **+2.62005** |

**Mean ratio (λ):** 0.918
**Spread (max − min):** 2.711 — driven entirely by p=7 (−0.091) and p=13 (+2.620)

**Comparison to reference pair (ρ₅, ρ₁₀), |cos θ| = 0.486:**

| Metric | Near-miss pair | Reference pair | Factor |
|---|---|---|---|
| |cos θ| | 0.9928 | 0.4863 | — |
| Ratio spread | 2.711 | 339.559 | **125× tighter** |

The near-miss pair has dramatically compressed ratio spread, but it is NOT zero — the ratios are not near a common constant λ. Exact proportionality (|cos θ| = 1) would require spread = 0.

---

## Analysis 2: Block Failure Mode

| Block | Primes | Per-prime spread | Mean ratio |
|---|---|---|---|
| C | {2} | 0.000 (trivial — 1 prime) | 0.704 |
| B | {3, 5} | **0.224** | 0.719 |
| **A** | **{7, 11, 13}** | **2.711** | **1.121** |

**Block A is the failure mode.** The wild variation (p=7: λ=−0.091, p=13: λ=+2.620) within Block A prevents exact proportionality.

**Why is |cos θ| still 0.9928 despite Block A wildness?**

The f₅D vectors reveal the answer:

| Component | f₅D(ρ₅₄) | f₅D(ρ₉₈) | Ratio |
|---|---|---|---|
| e₂ | −0.05831 | −0.05515 | 1.057 (small) |
| e₇ | −0.77397 | −0.94285 | **0.821** |
| e₃ | +0.07013 | −0.03736 | −1.877 (tiny, sign flip) |
| e₆ | −0.61821 | −0.86529 | **0.714** |
| e₄ | −0.20416 | −0.28988 | **0.704** |
| e₅ | −0.20416 | −0.28988 | **0.704** |

The **large components** (e₇, e₆, e₄, e₅) all have ratios in [0.70, 0.82] — roughly proportional with λ ≈ 0.73. The two problematic ratios (e₃ sign flip, e₂ outlier) live in **small-magnitude components** that barely contribute to the dot product:

- dot product dominated by e₇ (contributes 0.730) and e₆ (contributes 0.535)
- e₃ sign flip contributes only −0.003 (< 0.2% of dot product)

**Geometric explanation:** Within Block A, the wild per-prime ratios (p=7 and p=13 cancel constructively/destructively) produce a moderate net e₇ value that is roughly proportional across both zeros. The small e₂ component absorbs the Block A inconsistency. The high |cos θ| = 0.9928 is driven by Block B (e₆) and Block C (e₄, e₅) being the dominant large-amplitude contributions, both with ratios near 0.71.

---

## Analysis 3: Diophantine Structure

Δt = −81.062. For near-proportionality via a pure Diophantine resonance, we'd need Δt · log p / (2π) near an integer — so cos(t₅₄·log p) ≈ ±cos(t₉₈·log p) for that prime.

| Prime | |Δt| / log p | Frac. part | Near integer? | Best approx |
|---|---|---|---|---|---|
| 2 | 116.948 | **+0.052** | borderline (5%) | 17893/153 (err 1.1×10⁻⁴) |
| 3 | 73.786 | +0.214 | No | 1033/14 |
| 5 | 50.367 | −0.367 | No | 1511/30 |
| 7 | 41.658 | +0.342 | No | 7665/184 |
| 11 | 33.805 | +0.195 | No | 1217/36 |
| 13 | 31.604 | +0.396 | No | 1675/53 |

**No prime shows a clear near-integer fractional part.** The closest is p=2 with frac = +0.052 (i.e., |Δt|/log 2 ≈ 117 with 5% error). This mild resonance at p=2 is consistent with Block C (p=2) having the tightest ratio (λ=0.704, a genuine proportionality rather than near-zero). But p=2 resonance alone does not explain |cos θ| = 0.9928.

**Interpretation:** This is a genuine multi-prime amplitude coincidence — not attributable to a single Diophantine near-miss. The pair (t₅₄, t₉₈) happens to oscillate with similar amplitudes across the dominant directions (e₆, e₇, e₄, e₅), purely by numerical coincidence. There is no recognizable number-theoretic structure (e.g., rational combination of log-primes) forcing this near-proportionality.

This is precisely what the Linear Independence Conjecture predicts: near-proportionalities occur as multi-prime amplitude coincidences, not as Diophantine near-misses. The absence of a single-prime explanation *strengthens* the conjecture — no "shortcut" path to exact proportionality is available.

---

## Analysis 4: Secondary Pair (ρ₄₂ & ρ₉₅) — 6-prime Formula

| Zero | t value |
|---|---|
| ρ₄₂ | 127.516683879596 |
| ρ₉₅ | 227.421444279679 |
| **Δt** | **−99.904760400083** |

**|cos θ| (6-prime) = 0.878** — this pair is only the headline near-miss under the 9-prime formula (|cos θ| = 0.9964). Under the 6-prime formula it is a moderate pair.

| Prime | Block | λ_p |
|---|---|---|
| 2 | C | +1.074 |
| 3 | B | −3.139 |
| 5 | B | **+20.585** |
| 7 | A | +1.095 |
| 11 | A | −1.932 |
| 13 | A | +1.772 |

**Ratio spread: 23.725** (vs 2.711 for headline pair). The near-miss for (ρ₄₂, ρ₉₅) in the 9-prime formula is driven by the cross-block directions (p=17, 19, 23) rather than the (A₁)⁶ primes. The 6-prime Block B completely fails (p=5 ratio = 20.6 — near-zero denominator: cos(t₉₅ · log 5) ≈ −0.025).

| Block | Spread | Role |
|---|---|---|
| C | 0.000 | tightest (trivially, 1 prime) |
| A | 3.704 | moderate |
| **B** | **23.725** | **failure mode** |

Block B is the failure mode for this pair — the opposite of (ρ₅₄, ρ₉₈). The two near-miss pairs have **different block failure modes**:

| Pair | Failure block | Driving blocks |
|---|---|---|
| ρ₅₄ & ρ₉₈ (6-prime) | **A** (p=7,11,13) | B + C |
| ρ₄₂ & ρ₉₅ (6-prime) | **B** (p=3,5) | A + C |

No single block is the universal "weak point." The near-proportionalities occur in different geometric directions, consistent with pseudo-random oscillation across all blocks.

---

## Summary of Key Findings

1. **125× ratio compression** — near-miss pair has dramatically tighter ratio spread than a generic pair, but spread is still 2.711 (not near 0). Exact proportionality requires spread = 0.

2. **Block A is the failure mode for (ρ₅₄, ρ₉₈)** — per-prime ratios spread from −0.091 (p=7) to +2.620 (p=13). Block B and C ratios are tightly clustered at λ ≈ 0.70–0.83.

3. **Large components dominate** — the high |cos θ| = 0.9928 is geometrically explained by the large-magnitude components (e₇, e₆, e₄, e₅) being roughly proportional at λ ≈ 0.71–0.82. Small components (e₃, e₂) absorb the Block A inconsistency.

4. **No single-prime Diophantine structure** — no prime has |Δt|/log p near an integer (threshold 5%). This is a multi-prime amplitude coincidence, not a Diophantine near-miss.

5. **Different blocks fail for different near-miss pairs** — (ρ₅₄, ρ₉₈) fails in Block A; (ρ₄₂, ρ₉₅) fails in Block B. No systematic weak point. The embedding distributes near-proportionalities across all blocks.

6. **Linear Independence Conjecture status unchanged** — the absence of a Diophantine shortcut is itself evidence for the conjecture. The near-miss arises from numerical coincidence, not from a rational relation among the tₙ · log p values.

---

## Implication for the Paper

Section (AIEX-001, strong injectivity) should state:

> The empirically near-proportional pairs (Phase 20C, 20D) do not exhibit Diophantine resonances — no prime p shows |Δt/log p| near an integer. Near-proportionalities arise as multi-prime amplitude coincidences across the (A₁)⁶ block decomposition, with different blocks driving each near-miss. This is precisely the expected signature of pseudo-random oscillation in an arithmetic sequence, consistent with the Linear Independence Conjecture and inconsistent with any low-complexity Diophantine explanation.

---

## Open Questions

1. **What is the probability distribution of ratio spread for random pairs at n=100?** Analytically, under independence, the ratio λ_p = cos(tᵢ·log p)/cos(tⱼ·log p) has a Cauchy-like distribution (ratio of two sinusoids). The 125× compression may be typical for the top-0.02% quantile of pairs.

2. **Does the failure block rotate as n grows?** At n=200 or n=500, are the near-miss pairs still alternately failing in Block A vs Block B? If Block A consistently fails (low-pass Block C compensates), that would indicate a structural imbalance.

3. **Can the block structure bound max |cos θ| analytically?** If Block A and Block B are guaranteed to have at least one near-zero cos value in any pair, the 5D embedding is structurally protected. This is the path toward an analytic bound on max |cos θ| from the block decomposition.

---

*Phase 20D completed March 24, 2026*
*Chavez AI Labs LLC · Applied Pathological Mathematics*
