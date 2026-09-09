# Claude Code Handoff — Phase 78 Q-18 Detector Ensemble
**Chavez AI Labs LLC — Applied Pathological Mathematics**  
**Mission:** Design and test multi-gateway Riemann zero detectors that beat z=8.42 baseline  
**Date:** August 23, 2026  
**Prerequisites:** CAILculator v2.1.4+, Python 3.10+, numpy, scipy  

> ⚠ **Superseded for the Q-18 work.** This document is retained for the
> record. Corrections applied 2026-09-08 (C-006, C-012, C-013, C-014) are
> marked inline where they occur; see [`CORRECTIONS.md`](../../CORRECTIONS.md)
> for the full register, including entries not yet propagated here. Moved
> into the repository 2026-09-08 (was previously outside version control at
> the top of `Primes_2026`) so the corrections citing it are verifiable.

---

## 0. Pre-Flight Checklist (First 5 Minutes)

### Verify CAILculator Setup

```bash
# 1. Check version and build
cailculator-mcp --version
# Expected: v2.1.4+ · Engine v2.0 High-Precision · Build clean (0 errors)

# 2. Upgrade to latest
pip install --upgrade cailculator-mcp

# 3. CRITICAL: Restart the MCP server
# If Claude Desktop: Restart the entire application
# If terminal: Kill the running process and restart:
#   cailculator-mcp --transport stdio
# (or http if that's your mode)
```

### Verify Input Validation (Post-Restart)

```python
import json
from cailculator_mcp import ChavezTransform

# Test that invalid input is caught, not passed silently
try:
    ct = ChavezTransform()
    result = ct.chavez_transform([float('nan'), 1.0, 2.0])  # Should raise ValueError
    print("ERROR: NaN was not rejected!")
except ValueError as e:
    print(f"✓ Input validation working: {e}")
```

### Verify Detector Encoding Identity (Live Server)

Run this Python snippet **after confirming CAILculator is running:**

```python
import json
import math
import numpy as np

# Ground truth: phase77_q17_live_validation.json at gamma_1
gamma1 = 14.134725141734695
detector_input_16d = [
    0.5,                         # pos0: sigma
    gamma1,                      # pos1: t
    0.0,                         # pos2: ZEROED (detector encoding rule)
    -0.4564864319016121,         # u2 support: p=2 weighted
    0.0,                         # padding (unused at k=1; k=2 slot for p=17)
    -0.6241066363311436,         # u2 support: p=3 weighted
    -0.5227925174928422,         # u6 support: p=5 weighted [corrected label, C-006]
    0.0,                         # padding (index 7 is in no gateway's support -- see C-013)
    0.0,                         # padding [corrected label, C-006 -- was mislabeled "p=7"]
    -0.5283048392811939,         # u6 support: p=7 weighted [corrected label, C-006]
    -0.5694126951199865,         # u2 support: p=11 weighted [corrected label, C-006]
    0.0,                         # padding (unused at k=1; k=2 slot for p=19)
    0.08977816410667207,         # u2 support: p=13 weighted [corrected label, C-006]
    0.0,                         # padding
    0.0, 0.0
]
# Slot labels corrected 2026-09-08 (C-006): the *values* above were always
# correct (residual 0.00e+00 against w_p*cos(gamma1*ln p)); only the inline
# comments from index 6 onward were mislabeled. See CORRECTIONS.md.

# Call CAILculator for pattern 2 (S2) and pattern 6 (S6)
# Pseudocode (actual implementation depends on your Python MCP client):
cS2_live = call_cailculator(detector_input_16d, pattern=2)  # Should return ~3.120
cS6_live = call_cailculator(detector_input_16d, pattern=6)  # Should return ~2.103
detector_live = cS2_live + cS6_live  # Should return ~5.223

# Theoretical value (explicit formula)
w = {2: math.log(2)/math.sqrt(2), 3: math.log(3)/math.sqrt(3),
     5: math.log(5)/math.sqrt(5), 7: math.log(7)/math.sqrt(7),
     11: math.log(11)/math.sqrt(11), 13: math.log(13)/math.sqrt(13)}
detector_theory = -2.0 * sum(w[p] * math.cos(gamma1 * math.log(p)) for p in [2,3,5,7,11,13])

residual = abs(detector_live - detector_theory)
print(f"Live:    {detector_live:.16f}")
print(f"Theory:  {detector_theory:.16f}")
print(f"Residual: {residual:.3e}")
assert residual < 1e-13, f"Identity check failed: residual {residual}"
print("✓ Detector Encoding identity confirmed")
```

---

## 1. Data Files & Baseline

### Input Data
All files available in the execution environment:

| File | Purpose | Size |
|------|---------|------|
| `phase77_q15_convergence_probe.py` | Q-15 investigation script | ~8KB |
| `phase77_q17_signed_channel.py` | Q-17 baseline (z=8.42) script | ~7KB |
| `phase77_q17_results.json` | Baseline results + metadata | ~3.5KB (corrected 2026-09-08, was ~15KB — C-012) |
| `phase77_q17_live_validation.json` | Live CAILculator confirmation | ~3KB |
| `phase77_q15_results.json` | Q-15 channel investigation | ~45KB |
| `RH_PHASE_77_RESULTS.md` | Full narrative (Q-14/Q-15/Q-17) | ~30KB |
| `riemann_zeros.json` | First 1000 Riemann zeros (γ₁–γ₁₀₀₀) | Provided separately |

### Baseline Summary
```
Detector Encoding (June 12, 2026):
  Grid:      t ∈ [10, 240], 46,001 points, Δt = 0.005
  Zeros:     γ₁–γ₁₀₁ (101 Riemann zeros)
  z-score:   8.42 (p < 2e-4)
  ROC AUC:   0.8661 (δ=0.5)
  Precision: 0.831 vs 0.433 random baseline
  Identity:  c_S2 + c_S6 = -2·Σ(log p/√p)cos(t·log p)  [residual 1.776e-15]
```

**You must beat:** z ≥ 8.42 OR AUC ≥ 0.8661 (choose one metric)

---

## 2. Detector Encoding Specification (Locked)

### Input Format
16D vector encoding for the live CAILculator server:

```python
def detector_encoding(sigma, t):
    """
    Detector Encoding: purpose-built for Riemann zero detection.
    Deviates from Phase 76 Documented F(s) by design.
    """
    X = np.zeros(16)
    X[0] = sigma                              # pos0: σ (protocol slot)
    X[1] = t                                  # pos1: t (protocol slot)
    X[2] = 0.0                                # pos2: ZEROED (purity)
    
    # u_2 support {3,5,10,12} ← w_p cos(t ln p), p ∈ {2,3,11,13}
    w2 = math.log(2) / math.sqrt(2)
    w3 = math.log(3) / math.sqrt(3)
    w11 = math.log(11) / math.sqrt(11)
    w13 = math.log(13) / math.sqrt(13)
    
    X[3] = w2 * np.cos(t * math.log(2))
    X[5] = w3 * np.cos(t * math.log(3))
    X[10] = w11 * np.cos(t * math.log(11))
    X[12] = w13 * np.cos(t * math.log(13))
    
    # u_6 support {6,9} ← w_p cos(t ln p), p ∈ {5,7}
    w5 = math.log(5) / math.sqrt(5)
    w7 = math.log(7) / math.sqrt(7)
    
    X[6] = w5 * np.cos(t * math.log(5))
    X[9] = w7 * np.cos(t * math.log(7))
    
    # All other slots remain zero
    return X
```

### Critical Rules
1. **pos2 = 0 always** (non-negotiable; breaks c_S6 purity otherwise)
2. **Weighting:** w_p = log p / √p (standard explicit-formula weight)
3. **σ = 0.5 only** (all Q-18 work on critical line)
4. **t range:** [10, 240] or [10, 600] depending on zero count target

---

## 3. Four Q-18 Candidate Directions

### Candidate 1: Per-Gateway Explicit-Formula Weighting
**Hypothesis:** Different gateways have different γₙ sensitivity; weighted ensemble amplifies the signal.

**Design:**
```
Step 1: Read all six gateways at standard Detector Encoding
        c_S1, c_S2, c_S3, c_S4, c_S5, c_S6
        
Step 2: For each gateway, compute its per-zero z-score
        (from Phase 77 or new sweep)
        
Step 3: **DEFECT (C-014, fixed 2026-09-08) — do not use this formula:**
        ~~detector_weighted = Σ_g (z_g / Σz)² · c_S_g~~
        Gateways S1, S4, S5 have negative z under the Detector Encoding
        (≈ -2.3 each) -- they are anti-correlated with zero locations.
        Squaring discards the sign and gives them positive weight with the
        wrong orientation; the resulting weights also sum to 1.1008, not 1.
        Any weighting scheme here must preserve sign and normalize to 1.
        
Step 4: Evaluate: Does z_weighted > 8.42?
```

**Why it might work:**
- Phase 77 shows c_S2 is strongest (z=3.72→4.92 scale)
- c_S3, c_S6 also carry significant signal (z=1.87, z=2.05)
- Unweighted (1/6 each) may be suboptimal aggregation

**Fail criterion:** If z_weighted ≤ 8.42, the noise mixing overwhelms any benefit.

---

### Candidate 2: Class B Sign Structure Exploitation
**Hypothesis:** Class B gateways (S1, S4, S5) are t-dominated and contain odd-indexed components; their sign structure encodes additional zero information.

**Background:**
- Class A (S2, S3, S6): bounded oscillators, phase-sensitive
- Class B (S1, S4, S5): t-dominated, time-reversal asymmetric (from Phase 77 Run B)
- S1/S4/S5 support {1,3,12,14}, {1,3,12,14}, {1,5,10,14} — all contain pos1=t (odd index)

**Design:**
```
Step 1: Construct Class B combined scalar:
        detector_classB = α·c_S1 + β·c_S4 + γ·c_S5
        where α, β, γ chosen by:
        (a) Equal weighting (baseline)
        (b) Inverse-variance weighting (per Phase 77)
        (c) Optimization over a subsample of zeros
        
Step 2: Construct hybrid:
        detector_hybrid = c_S2 + c_S6 + λ·detector_classB
        (λ chosen to maximize z on validation set)
        
Step 3: Evaluate hybrid on held-out zeros
```

**Why it might work:**
- Class B has large |c| values (|c_S1| ~26 at γ₁ vs |c_S2| ~2)
- Time-reversal asymmetry is a distinct architectural feature not captured in baseline
- Hybrid exploits both phase coherence (A) and amplitude/timing (B)

**Fail criterion:** If adding Class B degrades z (noise dominates).

---

### Candidate 3: Higher Prime Truncations
**Hypothesis:** The k=1 explicit-formula truncation (6 primes) is suboptimal; k=2 or selective higher primes improve detection.

**Background:**
- Current Detector Encoding uses only {2,3,5,7,11,13}
- von Mangoldt explicit formula: Λ(t) = Σ_n Λ(ρₙ)·k_s(t−ρₙ)
- k=1 truncation omits primes p > 13 (17, 19, 23, ...)
- Constraint: 16D sedenion; u₂, u₆ supports must remain disjoint

**Design (corrected 2026-09-08 — see C-013; the original instruction below this
line was wrong and was fixed before any result was computed from it):**
```
Step 1: Identify unused slots in u_2, u_6 supports
        Current: u_2={3,5,10,12}, u_6={6,9}
        Index 7 is in the support of NONE of the six gateways -- a signal
        placed there is invisible to every reading, dead weight.
        Index 4 IS live but belongs to S3's support {4,11,6,9}, not to u_2.
        
Step 2: Test extension via S3 (not u_2):
        (a) Add p=17 to slot 4, p=19 to slot 11 -- both in S3's support
            w17 = log(17) / √17
            w19 = log(19) / √19
            detector_extended = c_S2 + c_S3
                               = c_S2 + c_S6 - 2*w17*cos(t*ln17) - 2*w19*cos(t*ln19)
            (since S3 shares slots {6,9} with S6, and slots {4,11} carry the
            new primes; S3 ≡ S6 exactly under the k=1 encoding before this
            extension, so this breaks that degeneracy rather than adding an
            unrelated channel)
            
Step 3: For each extension, compute detector_extended
        and evaluate z-score on first 20-50 zeros
        
Step 4: If improvement is meaningful, validate on full 101 zeros
```

**Why it might work:**
- Explicit formula truncation artifacts may suppress higher-frequency signals
- 16D → 256D ZDTP transmission may preserve information from higher primes

**Fail criterion:** If added primes introduce 16D crosstalk (slot collision) or numerical instability.

---

### Candidate 4: Clifford Framework Variant
**Hypothesis:** S2 is unique among the Canonical Six: it's bilateral in **both** Cayley-Dickson and Clifford algebras. Reading it via Clifford structure may bypass non-associative noise.

**Background:**
- Phase 77 used Cayley-Dickson (non-associative)
- S2 = (e₃+e₁₂, e₅+e₁₀) is proven bilateral in both frameworks
- S1, S3–S6 collapse in Clifford (one-sided residual ‖QP‖ = 2√2)
- Hypothesis: Clifford S2 reading has lower noise floor

**Design:**
```
Step 1: Replicate phase77_q17_signed_channel.py in Clifford algebra
        Use Clifford(7, 0) or Clifford(3, 4) representation
        (Paul's preference; check CAIL-RH Lean stack for conventions)
        
Step 2: Compute c_S2_clifford via the Clifford inner product
        c_S2_clifford = -2 ⟨x, P_S2 + Q_S2⟩_clifford
        
Step 3: Combine with c_S6 (Cayley-Dickson, no alternative)
        detector_hybrid_framework = c_S2_clifford + c_S6
        
Step 4: Compare z-score to baseline z=8.42
```

**Why it might work:**
- Associativity of Clifford may suppress non-associative scrambling at scale
- S2's bilateral status in both frameworks is a marker of structural importance

**Why it might fail:**
- Dimension mismatch (Clifford 8D vs sedenion 16D)
- Gateway scalars are defined in Cayley-Dickson; Clifford versions need explicit derivation

**Dependency:** Requires CAILculator to expose Clifford inner products (check schema).

---

## 4. Implementation Roadmap

### Phase 1: Verification (Day 1, ~1 hour)
1. Run pre-flight checklist (CAILculator version, input validation, identity check)
2. Reproduce `phase77_q17_results.json` exactly
   - Load `phase77_q17_signed_channel.py`
   - Run on first 31 zeros (quick validation)
   - Confirm z≈3.62 for c_S2, z≈8.42 for detector
3. Document any discrepancies in KSJ (will inform Paul)

### Phase 2: Candidate 1 Implementation (Day 1–2, ~3 hours)
1. Per-gateway weighting ensemble
2. Test on first 50 zeros
3. If z > 8.5, validate on full 101
4. Record all intermediate z-scores, ROC curves to JSON

### Phase 3: Candidate 2 Implementation (Day 2–3, ~3 hours)
1. Class B extraction + weighting
2. Hybrid design (t ∈ [10, 240] grid)
3. Validation on held-out zero subset
4. Compare z, AUC, precision to baseline

### Phase 4: Candidate 3 or 4 (Day 3–4, ~2 hours each, pick one)
- Higher primes: Quick sanity check first (test on 20 zeros, stop if no improvement)
- Clifford variant: Requires schema check + Lean reference; defer if infrastructure unavailable

### Phase 5: KSJ Extraction & Report (Day 4, ~1 hour)
1. For each candidate, run `extract_insights` from KSJ
2. Compile results JSON (z, AUC, precision, grid, notes)
3. Wait for Paul's approval before `commit_aiex`

---

## 5. Success Criteria & Honest Baselines

### Primary Metric: z-score
- **Baseline (beat this):** z = 8.42 (p < 2e-4)
- **Strong improvement:** z ≥ 9.5 (√N + 5% bonus)
- **Weak improvement:** 8.42 < z < 9.5 (keep, iterate)
- **No improvement:** z ≤ 8.42 (discard candidate)

### Secondary Metric: ROC AUC
- **Baseline:** AUC = 0.8661 (δ=0.5)
- **Success:** AUC > 0.875 (clear improvement)

### Honest-Baseline Discipline (AIEX-742)
At γ₁–γ₁₀₁, mean zero gap ≈ 2.28:
- Random prediction within ε=0.5 lands near a zero ~54% of the time
- Random prediction within ε=1.0 lands near a zero ~88% of the time
- **Baseline precision @ ε=0.5:** 0.433 (random)
- **Baseline precision @ ε=1.0:** 0.433 (random)

**Any claimed precision must cite the honest baseline and report ratio (detector_precision / random_baseline).**

---

## 6. Output Artifacts

### For Each Candidate
Create a results JSON with this structure:

```json
{
  "phase": "78",
  "question": "Q-18",
  "candidate": "1_per_gateway_weighting",
  "date": "2026-08-23",
  "grid": {
    "t_lo": 10.0, "t_hi": 240.0, "dt": 0.005, "n": 46001
  },
  "zeros_tested": 101,
  "detector_spec": "Detector Encoding per Q-17 specification",
  "modifications": "Added per-gateway inverse-variance weighting",
  "results": {
    "z_score": 8.42,
    "z_pvalue": 0.0,
    "roc_auc_delta05": 0.8661,
    "roc_auc_delta025": 0.8095,
    "peak_precision_eps05": 0.831,
    "peak_precision_eps10": 0.974,
    "honest_baseline_ratio": 1.92
  },
  "interpretation": "Per-gateway weighting did NOT improve z-score beyond baseline...",
  "code_location": "phase78_q18_candidate1_per_gateway.py",
  "commit_status": "awaiting_paul_review"
}
```

### Master Results Table
Maintain a CSV across all candidates:

```
Candidate | z_score | z_vs_baseline | AUC(δ=0.5) | Precision(ε=1) | Status
Per-Gateway | 8.42 | 0.00 | 0.8661 | 0.974 | No improvement
ClassB | ? | ? | ? | ? | Running
Higher Primes | ? | ? | ? | ? | Pending
Clifford | ? | ? | ? | ? | Pending
```

---

## 7. CAILculator MCP Interaction

### API Calls Needed

**Pattern-based reading:**
```python
# Pseudocode (adapt to your MCP client)
cS2 = cailculator.gateway_scalar(16d_input, gateway=2)
cS6 = cailculator.gateway_scalar(16d_input, gateway=6)
```

Or use the `zdtp_transmit` tool directly:
```python
result = cailculator.zdtp_transmit(16d_input, restrict_to_pattern=[2, 6])
# Extract c_S2, c_S6 from lift slot 0 at different dimensions
```

**Precision check:**
- All results should maintain 10⁻¹⁵ machine precision
- Any coefficient > ±1e8 indicates numerical instability (stop and debug)

**Validation:** Before declaring success on a candidate, validate a subset of inputs with the live server to ensure replica calculations match.

---

## 8. Known Constraints & Gotchas

### Dimensionality
- Detector Encoding is 16D input only
- ZDTP transmits to 32D, 64D, ..., 256D
- Gateway scalars (c_g) are read from 32D lift (slot 0)
- Do NOT use the 256D transmission length; 32D has the interpreted basis

### Time Grid
- Phase 77 used Δt = 0.005 (46,001 points for t ∈ [10,240])
- For Run C (high zeros), may need Δt = 0.001 or 0.002 for finer resolution
- **Memory:** 46K points × 6 gateways × 8 bytes = ~2.2 MB (fine)

### Gateway Ordering
```
Pattern 1: S1 (e₁+e₁₄, e₃+e₁₂)  — Class B
Pattern 2: S2 (e₃+e₁₂, e₅+e₁₀)  — Class A [Detector primary]
Pattern 3: S3 (e₄+e₁₁, e₆+e₉)   — Class A
Pattern 4: S4 (e₁−e₁₄, e₃−e₁₂)  — Class B
Pattern 5: S5 (e₁−e₁₄, e₅+e₁₀)  — Class B
Pattern 6: S6 (e₂−e₁₃, e₆+e₉)   — Class A [Detector secondary]
```

Confirmed via `phase77_q17_signed_channel.py`.

### RNG Seed
Phase 77 used `seed=20260612` (June 12, 2026) for null hypotheses. Keep for reproducibility if regenerating baselines.

---

## 9. Escalation & Paul Handoff

### When to Escalate
1. **z < 7.5 on Candidate 1** → Stop; re-evaluate strategy with Paul
2. **Numerical instability** (|c| > 1e8) → Debug + report
3. **CAILculator schema mismatch** → Pause; clarify API contract
4. **Clifford variant requires new Lean lemma** → Pause for Paul's direction

### KSJ Commit Protocol
**Before every `commit_aiex`:**
1. Run `extract_insights` on the candidate results
2. Wait for Paul's explicit approval
3. Only then `commit_aiex` with the approved summary

**Never auto-commit.**

---

## 10. Timeline & Checkpoints

| Checkpoint | Deadline | Owner | Deliverable |
|------------|----------|-------|-------------|
| Pre-flight verification | EOD today | Claude Code | Identity check passes ✓ |
| Candidate 1 z-score | Day 2 AM | Claude Code | z > 8.0 or fail reason |
| Candidate 2 prototype | Day 3 AM | Claude Code | Hybrid design, 50-zero test |
| Results JSON (all candidates) | Day 4 PM | Claude Code | Master table + artifacts |
| KSJ extracts (Paul review) | Day 5 AM | Paul | Approval on top candidates |
| Commit to KSJ | Day 5 PM | Claude Code | AIEX-XXX records live |

---

## 11. Reference Data

### Riemann Zeros (γ₁–γ₁₀₁)
Load from `riemann_zeros.json` (provided separately). First 5:
```
γ₁ = 14.134725141734695
γ₂ = 21.022039638771555
γ₃ = 25.010857580145688
γ₄ = 30.424876125859513
γ₅ = 32.935062301763590
```

### Canonical Six Patterns (Locked)
```python
PATTERNS = {
    1: (vec((1, 1), (14, 1)),  vec((3, 1), (12, 1))),
    2: (vec((3, 1), (12, 1)),  vec((5, 1), (10, 1))),
    3: (vec((4, 1), (11, 1)),  vec((6, 1), (9, 1))),
    4: (vec((1, 1), (14, -1)), vec((3, 1), (12, -1))),
    5: (vec((1, 1), (14, -1)), vec((5, 1), (10, 1))),
    6: (vec((2, 1), (13, -1)), vec((6, 1), (9, 1))),
}
```

### Weighting Constants
**(C-006, fixed 2026-09-08): always compute from the formula below. Never
hardcode a table of values — a previous version of this table had numbers
wrong for p = 5, 7, 11, 13, and the error was qualitative, not just
numerical: the true sequence peaks at p = 7 (log p/√p is maximized at
p = e² ≈ 7.39) and decreases after, while the wrong table increased
monotonically. The scripts that actually ran always used the formula, so no
result was affected — the risk was to any future agent hardcoding the wrong
table instead of computing it. See `CORRECTIONS.md` C-006.**
```python
PRIMES = (2, 3, 5, 7, 11, 13)
W = {p: math.log(p) / math.sqrt(p) for p in PRIMES}
```

---

## 12. Quick Start Script

```bash
# 1. Verify setup
python3 << 'EOF'
import math, json, numpy as np
print("✓ Imports OK")
# Load baseline
with open("phase77_q17_results.json") as f:
    baseline = json.load(f)
print(f"✓ Baseline z = {baseline['scale']['detector_gamma100']['z']:.2f}")
# Quick encoding check
W = {p: math.log(p)/math.sqrt(p) for p in [2,3,5,7,11,13]}
print(f"✓ Weighting loaded: w2={W[2]:.4f}, w13={W[13]:.4f}")
EOF

# 2. Run Candidate 1
python3 phase78_q18_candidate1_per_gateway.py

# 3. Check results
python3 << 'EOF'
import json
with open("phase78_q18_candidate1_results.json") as f:
    results = json.load(f)
print(f"Candidate 1 z-score: {results['results']['z_score']:.2f}")
print(f"Improvement: {results['results']['z_vs_baseline']:+.2f}")
EOF
```

---

## Summary

**You have:**
- ✅ Phase 77 baseline (z=8.42) confirmed reproducible
- ✅ Detector Encoding specification (locked, exact identity)
- ✅ Four candidate directions (ranked by risk/effort)
- ✅ CAILculator v2.1.4+ (just verify + restart)
- ✅ Honest-baseline discipline (AIEX-742 methodology)

**Your job:**
1. Pre-flight checks (15 min)
2. Reproduce baseline (30 min)
3. Run Candidates 1 & 2 (6 hours, maybe parallel)
4. KSJ extractions for Paul (1 hour)

**Success bar:** z ≥ 8.42 on at least one candidate, with honest baselines cited.

---

**Better math, less suffering.**  
*Phase 78 Q-18 — Claude Code Execution Handoff*
