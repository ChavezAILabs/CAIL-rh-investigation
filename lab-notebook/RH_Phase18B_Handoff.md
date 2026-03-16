# RH Phase 18B Handoff — Three-Gap Layer Structure: Vector Part & n-Gap Generalization

**Researcher:** Paul Chavez, Chavez AI Labs LLC
**Date:** March 16, 2026
**Status:** Ready to execute
**Depends on:** Phases 17, 18E (complete)

---

## Background

Phase 17 discovered that the sedenion product of consecutive gap-encoded sedenions naturally produces the **three-gap statistic**:

> s_n = scalar_part(x_n · x_{n+1}) = −2 · g_{n+1} · (g_n + g_{n+2})

where x_n = g_n · P1 + g_{n+1} · Q1, and P1, Q1 are the Pattern 1 bilateral zero divisors.

This revealed a **layer structure** in the Riemann zero correlations:

| Statistic | Act/GUE variance ratio | Interpretation |
|---|---|---|
| Two-gap (embed_pair P2, Phase 10C) | **0.65** | Actual zeros are *tighter* than GUE |
| Three-gap sedenion scalar (Phase 17) | **1.02** | Actual zeros *match* GUE |

Phase 18B investigates the full structure of this transition.

---

## Research Questions

### 18B-i — Vector Part Survey (with Preflight)

The sedenion product x_n · x_{n+1} has **16 components** (one scalar + 15 vector). Phase 17 used only component 0 (the scalar). The script first runs a **preflight** to determine which components are structurally active for the chosen P1/Q1 pair, before any statistics are computed.

**Preflight theorem (derived analytically):** Expanding the product:

> x_n · x_{n+1} = g_n·g_{n+1}·(P1²) + g_n·g_{n+2}·(P1·Q1) + g_{n+1}²·(Q1·P1) + g_{n+1}·g_{n+2}·(Q1²)

Since P1·Q1 = Q1·P1 = 0 (bilateral zero divisor property, Lean 4 verified) and P1² = Q1² = −2·e0, this collapses to:

> x_n · x_{n+1} = −2·g_{n+1}·(g_n + g_{n+2})·e0

**All 15 vector components are structurally zero for any gap sequence** — an algebraic consequence of the bilateral ZD property, not a statistical observation. The product is forced entirely into the scalar channel by the zero divisor structure.

The script verifies this analytically (computing P1², P1·Q1, Q1·P1, Q1²) and empirically (checking that all 15 vector component sequences are identically zero), then proceeds with statistics only on structurally active components.

**Octonion/sedenion boundary hypothesis:** Cannot be tested with Pattern 1 — no vector components survive the preflight. Testing requires a P/Q pair where at least one of P·Q or Q·P has nonzero vector components. This is a natural target for **Phase 18F** (framework-independence probe), where framework-dependent patterns use different Q-vectors that may not have total scalar collapse.

### 18B-ii — n-Gap Generalization
Define a coherent k-gap family:

> s_n^(k) = g_{n + ⌊k/2⌋} × (sum of all other k−1 gaps in the window)

**Definitional note — k=2 vs Phase 10C:** The k=2 entry in this family is `g_n × g_{n+1}` (a pure product). The Phase 10C two-gap result (Act/GUE = 0.65) used a different statistic: embed_pair P2 = `−(g1²+g2²)/(2(g1+g2))` (a negative rescaled harmonic mean). These are not the same family. The script computes both and reports Phase 10C P2 as an explicit reference point. Do not compare k=2 product directly to 0.65 without flagging this distinction.

- k=1: just g_n (single gap baseline)
- k=2: g_n × g_{n+1} (pairwise product)
- k=3: g_{n+1} × (g_n + g_{n+2}) ← **matches Phase 17 sedenion scalar exactly**
- k=4: g_{n+2} × (g_n + g_{n+1} + g_{n+3})
- k=5: g_{n+2} × (g_n + g_{n+1} + g_{n+3} + g_{n+4})
- k=6, 7, 8: similarly extended

At what k does Act/GUE transition from <1 to ≈1? Is the transition sharp (step) or gradual?

### 18B-iii — Height Window Stability
Does Act/GUE ≈ 1.02 hold across different height windows, or is it window-dependent?

**Phase 12A context (critical):** The two-gap Act/GUE ratio was found to be HEIGHT-DEPENDENT — it ranged from 0.65 at low heights to 0.75 at high heights, always < 1.0, and was never a sample-size effect. If the three-gap ratio is height-STABLE, that is a qualitatively stronger result: GUE-matching at three-gap scale would be a universal property of the Riemann zero spectrum, not a window artifact. This distinction must be stated explicitly in the write-up if it holds.

---

## Data Files Required

| File | Contents | Used for |
|---|---|---|
| `rh_zeros_10k.json` | 10,000 Riemann zeros | actual zero dataset |
| `rh_gaps_10k.json` | 9,999 gaps | actual gap sequences |

No new zero computation needed. All analysis uses existing cached data.

---

## Step-by-Step Protocol (Claude Desktop + CAILculator)

### Step 0 — Run the preparation script
```
python rh_phase18b_prep.py
```
This generates `p18b_results.json` with all numerical results. Check the console output for warnings.

### Step 1 — Record vector part results (18B-i)

First check the **preflight output**:
- Confirm P1·Q1 = Q1·P1 = 0 (expected from Lean 4 proof)
- Confirm structurally active components = [0] only
- Confirm empirically zero components match structural prediction

Then record for the scalar component (e0):
- Mean, variance (actual, GUE, Poisson)
- Act/GUE variance ratio (expect ≈1.02 — Phase 17 replication)
- Log-prime DFT SNR profile

**Key questions to answer:**
1. Does the preflight confirm the bilateral ZD theorem holds computationally?
2. Does Act/GUE for e0 replicate Phase 17's 1.02?
3. Are all 15 vector components confirmed zero to machine precision?

### Step 2 — Record n-gap generalization results (18B-ii)

From the script output, record the Act/GUE variance ratio for k = 1, 2, 3, 4, 5, 6, 7, 8.

**Key questions to answer:**
1. Does k=2 give Act/GUE < 1? (Expected yes, confirming Phase 17 vs Phase 10C pattern)
2. Does k=3 give Act/GUE ≈ 1.02? (Replication of Phase 17 result)
3. Is there a sharp transition between specific k values, or gradual drift?
4. Does the ratio overshoot >1 at any k? If so, at what k does it peak and then drop?

### Step 3 — Height window stability (18B-iii)

Run the three-gap statistic on height sub-windows to check stability:
- Zeros 0–2499 (heights ~14–227)
- Zeros 2500–4999 (heights ~227–495)
- Zeros 5000–7499 (heights ~495–768)
- Zeros 7500–9999 (heights ~768–9878)

Does Act/GUE ≈ 1.02 hold across all windows, or is it height-dependent (like the two-gap 0.65 result was in Phase 12A)?

### Step 4 — Apply Chavez Transform (CAILculator)

Apply the Chavez Transform to the **three-gap scalar sequence** (the only structurally active component): s_n = −2·g_{n+1}·(g_n + g_{n+2}). Compare symmetry scores for actual vs GUE vs Poisson.

Use standard parameters:
- Alpha: 1.0
- Dimension parameter: 2
- Pattern ID: 1
- Dimensions tested: 1, 2, 3, 4, 5

### Step 5 — Save results

Save all results to `p18b_results.json` (schema below) and write `RH_Phase18B_Results.md` with findings.

---

## Expected Outcomes

| Sub-experiment | Likely result | Would be surprising |
|---|---|---|
| 18B-i preflight | All 15 vector components structurally zero; only e0 active | Any nonzero vector component |
| 18B-i component 0 (scalar) | Act/GUE ≈ 1.02 (Phase 17 replication) | Major deviation |
| 18B-i boundary hypothesis | Untestable with Pattern 1; deferred to Phase 18F | — |
| 18B-ii k=2 (product) | Act/GUE unknown for product family (not the P2 stat) | — |
| 18B-ii k=2 (P2 reference) | Act/GUE ≈ 0.65 (Phase 10C replication) | Major deviation |
| 18B-ii k=3 | Act/GUE ≈ 1.02 (Phase 17 replication) | Major deviation |
| 18B-ii k≥4 | Act/GUE ≥ 1.0 (or gradual drift) | Return below 1.0 |
| Height stability (18B-iii) | More stable than two-gap; ≈1.02 across windows | Strong height dependence |

---

## Results Schema

```json
{
  "phase": "18B",
  "date": "2026-03-16",
  "researcher": "Paul Chavez, Chavez AI Labs LLC",
  "18Bi_vector_part_survey": {
    "question": "What do all 16 sedenion product components reveal about Act/GUE structure?",
    "n_gaps_used": 9999,
    "n_triplets": 9997,
    "components": [
      {
        "index": 0,
        "basis_element": "e0 (scalar)",
        "actual_mean": 0.0,
        "actual_var": 0.0,
        "gue_var": 0.0,
        "poisson_var": 0.0,
        "act_gue_ratio": 0.0,
        "poi_gue_ratio": 0.0,
        "top_prime_snr": {"p": 0, "snr": 0.0}
      }
    ],
    "summary": {
      "n_components_act_lt_gue": 0,
      "n_components_act_approx_gue": 0,
      "n_components_act_gt_gue": 0,
      "max_act_gue_ratio_component": 0,
      "max_poi_gue_ratio_component": 0,
      "best_log_prime_snr_component": 0
    }
  },
  "18Bii_ngap_generalization": {
    "question": "At what k does Act/GUE variance ratio transition from <1 to ≈1?",
    "formula": "s_n^(k) = g_{n+floor(k/2)} * sum(other k-1 gaps in window)",
    "k_results": [
      {"k": 1, "n_values": 0, "actual_var": 0.0, "gue_var": 0.0, "act_gue_ratio": 0.0, "poi_gue_ratio": 0.0}
    ],
    "transition_k": null,
    "transition_type": "sharp/gradual/unknown"
  },
  "18Biii_height_stability": {
    "question": "Does Act/GUE ≈ 1.02 hold across height windows?",
    "windows": [
      {"label": "zeros 0-2499", "height_range": [0, 0], "act_gue_ratio": 0.0}
    ]
  },
  "key_findings": {
    "vector_part_new_discriminator": "YES/NO — description",
    "transition_k": "k=N or gradual",
    "height_stability": "stable/height-dependent",
    "best_component_for_SNR": "component index and SNR"
  }
}
```

---

## Files

| File | Type | Purpose |
|---|---|---|
| `rh_phase18b_prep.py` | Python script | All numerical computation |
| `p18b_results.json` | JSON | Structured results |
| `RH_Phase18B_Results.md` | Markdown | Human-readable findings |

---

*Chavez AI Labs LLC · Applied Pathological Mathematics*
*"Better math, less suffering"*
