# Phase 24 Pre-Handoff — Claude Code Briefing
## RH Investigation · Chavez AI Labs LLC · March 25, 2026

**Prepared by:** Claude (claude.ai session)
**For:** Claude Code
**Working directory:** `C:\dev\projects\Experiments_January_2026\Primes_2026\`
**Status:** Phase 23 complete. Phase 24 is the windowed Weil identity + bilateral triple module action.

---

## Why Phase 24 Is Different

Phases 21–23 closed algebraic avenues. Phase 24 attacks from two directions that are structurally richer:

1. **Windowed Weil identity** — the first time the investigation uses a *proven theorem* (the Weil explicit formula) as primary tool. Phase 23T3 showed S(N) is 99.3% aligned with the Euler product RHS direction, with a 12% residual that oscillates at 98.7% bilateral symmetry. The residual doesn't shrink because f₅D is not Schwartz-class. A Gaussian window fixes this. If the windowed residual shrinks to zero, AIEX-001 satisfies a proven theorem.

2. **Bilateral triple module action** — the 12-vector finite closure of {q2, q3, q4} (Phase 23T1) is the first algebraic structure that emerged without being put in by hand. Phase 21C ruled out the module map for the full 6-root set (products escape 5D). The 12-vector closure is finite and self-contained — it may admit a well-defined module action. If yes, this reopens the eigenvalue constraint question Phase 21A closed.

---

## Canonical Embedding (Phase 20B — use exactly this)

```python
import numpy as np
from mpmath import mp, zetazero
mp.dps = 25

sqrt2 = np.sqrt(2.0)
ROOT_DIRS = {
    2:  np.array([0, 0, 0, 0, 1, 1]) / sqrt2,   # q4 — Block C
    3:  np.array([0, 0,-1, 1, 0, 0]) / sqrt2,   # q2 — Block B (Heegner)
    5:  np.array([0, 0, 1, 1, 0, 0]) / sqrt2,   # v5 — Block B
    7:  np.array([1,-1, 0, 0, 0, 0]) / sqrt2,   # v1 — Block A
    11: np.array([1, 1, 0, 0, 0, 0]) / sqrt2,   # v4 — Block A
    13: np.array([-1,1, 0, 0, 0, 0]) / sqrt2,   # q3 — Block A (bilateral hub)
}
U_ANTISYM = np.array([0, 0, 0, 0, 1, -1]) / sqrt2  # (e4-e5)/sqrt2

def f5D(t):
    result = np.zeros(6)
    for p, r in ROOT_DIRS.items():
        result += (np.log(p) / np.sqrt(p)) * np.cos(t * np.log(p)) * r
    return result

def v_rho(sigma, t):
    return f5D(t) + (sigma - 0.5) * U_ANTISYM
```

**Structural facts (do not re-investigate):**
- v1 = −q3 → G5 (5×5) is the correct Gram matrix object
- Block C is structurally rank 1 (single prime p=2)
- v2 = u_antisym — antisymmetric direction reserved for functional equation
- q3 (p=13) bilateral hub: q3×q2=0, q3×q4=0 in both orders
- G5 positive definite to N=500 (λ_min ∝ N, R²=0.9999)

---

## Sedenion Multiplication (Thread 2 needs this)

```python
def cd_conj(v):
    return [v[0]] + [-x for x in v[1:]]

def cd_mul(a, b):
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    c1 = [x - y for x, y in zip(cd_mul(a1, b1), cd_mul(cd_conj(b2), a2))]
    c2 = [x + y for x, y in zip(cd_mul(b2, a1), cd_mul(a2, cd_conj(b1)))]
    return c1 + c2

# 16D representations of bilateral triple {q2, q3, q4} (0-indexed, unnormalized norm=sqrt(2)):
#   q2 = e5 + e10   → positions 5(+1), 10(+1)
#   q3 = e6 + e9    → positions 6(+1), 9(+1)
#   q4 = e3 - e12   → positions 3(+1), 12(-1)
```

**The 12-vector closure of {q2, q3, q4} (from Phase 23T1):**

| # | Positions | Identification |
|---|---|---|
| v1 | e0 = −1 | Scalar (negative identity) |
| v2 | (−e3−e12)/√2 | = −q4 antipodal |
| v3 | (−e5+e10)/√2 | = −q2 antipodal |
| v4 | (−e6+e9)/√2 | = sign partner of q3 |
| v5,v6 | ±e15 | New direction |
| v7 | (e6−e9)/√2 | = sign partner of q3 |
| v8 | (e6+e9)/√2 | = q3 |
| v9 | (e5−e10)/√2 | = sign partner of q2 |
| v10 | (e5+e10)/√2 | = q2 |
| v11 | (e3−e12)/√2 | = q4 |
| v12 | (e3+e12)/√2 | = new direction |

**Inner product structure:** 6 antipodal pairs; all other 62 pairings orthogonal.

**CAILculator scores (Phase 23T1):**
- Gram inner products: 84.8% conjugation symmetry
- 12×12 product zero pattern: 95% bilateral zero confidence, 94.4% conjugation symmetry

---

## Phase 23 Key Results (What Phase 24 Builds On)

| Result | Value | Source |
|---|---|---|
| S(N) alignment with Weil RHS | 99.3% at N=500 | Phase 23T3 |
| Residual ratio | 12.1% ± 0.6% (stable) | Phase 23T3 |
| Residual ratio Chavez | **98.7%** — investigation record | Phase 23T3 CAILculator |
| P(N)/N → | 1.270 (7% below random 1.365) | Phase 23T3 |
| P(N)/N Chavez | **97.8%** | Phase 23T3 CAILculator |
| Bilateral triple closure | 12 vectors, 4 generations | Phase 23T1 |
| 12-vec Gram Chavez | 84.8% | Phase 23T1 CAILculator |
| 12-vec product zero pattern | 95% bilateral, 94.4% Chavez | Phase 23T1 CAILculator |
| λ_min(G5) growth | Linear R²=0.9999 (Marchenko-Pastur) | Phase 23T2 |
| GUE norm signature | GUE ≈ zeros ≠ uniform random | Phase 23T2 |

---

## Phase 24 — Two Threads

**Run order: Thread 1 first (Weil), then Thread 2 (bilateral triple).**

---

### Thread 1: Windowed Weil Identity

**File:** `rh_phase24_thread1.py`
**Output:** `phase24_thread1_results.json`, `RH_Phase24_Thread1_Results.md`

**The test:** Apply a Gaussian window w_T(t) = exp(−t²/T²) to f₅D to obtain a Schwartz-class test function h_T(t) = w_T(t)·f₅D(t). The windowed partial sum S_T(N) = Σ_{n=1}^N h_T(tₙ) should converge to a finite vector as N→∞ (for fixed T). Check whether the residual ratio shrinks to zero.

**Why this matters:** f₅D is not Schwartz-class — it oscillates without decay. The Weil explicit formula requires rapid decay. The window fixes this. If the windowed residual converges to zero, the AIEX-001 embedding satisfies the Weil explicit formula — connecting it to a proven theorem in analytic number theory.

**Computations:**

**1. Window construction**
For T = 50, 100, 200 (three window widths):
```python
def h_T(t, T):
    return np.exp(-t**2 / T**2) * f5D(t)
```
Note: zeros go up to t₅₀₀ ≈ 236.5. Window T=50 suppresses t>150 heavily; T=200 is near-flat across the zero range.

**2. Windowed partial sums**
Compute S_T(N) = Σ_{n=1}^N h_T(tₙ) for N = 10, 50, 100, 200, 300, 500 and each T.

**3. Residual ratio vs T**
For each (T, N), compute:
- Projection fraction: |⟨S_T(N), RHS_dir⟩| / ‖S_T(N)‖
- Residual ratio: ‖S_T(N) − projection‖ / ‖S_T(N)‖

**Key question:** Does the residual ratio → 0 as T → ∞ (for fixed large N)? If yes, the Weil identity is satisfied in the limit.

**4. Convergence rate**
For each T, fit the residual ratio vs N to the models:
- Decaying: a·N^b with b < 0
- Stable: constant c
- Oscillating: a·cos(b·N) + c

If the windowed residual is decaying, report the decay rate b and the extrapolated N at which it reaches 1%.

**5. Comparison table: unwindowed vs windowed**

| N | Unwindowed residual | T=50 residual | T=100 residual | T=200 residual |
|---|---|---|---|---|
| 100 | 12.6% | ? | ? | ? |
| 300 | 11.7% | ? | ? | ? |
| 500 | 12.0% | ? | ? | ? |

**6. RHS direction check**
The RHS direction for the windowed formula changes with T:
- Unwindowed: RHS_dir = −f₅D(0)/‖f₅D(0)‖
- Windowed: RHS_T_dir = −Σ_p r_p · (log p/√p) · ĥ_T(log p) where ĥ_T is the Fourier transform of w_T(t)·cos(t·log p)

For Gaussian window: ĥ_T(ω) = (T√π/2)·[exp(−T²(ω−log p)²/4) + exp(−T²(ω+log p)²/4)]

Compute the windowed RHS direction for each T and report how much it differs from the unwindowed direction.

**7. Block-wise windowed residuals**
Decompose residual by Block A, B, C. Does any block drive the residual? If Block C (p=2, weakest channel) is responsible for a disproportionate share, that connects to both Thread 2 and the Thread 1 algebraic closure findings.

**Key result to look for:**
- If residual ratio shrinks with T → **Weil identity confirmed in windowed sense, connect AIEX-001 to proven theorem**
- If residual ratio stays ~12% regardless of T → 12% is structural, not a test-function artifact; the AIEX-001 embedding has a stable 6.8° offset from the Weil RHS
- If residual ratio grows with T → the window is not the right regularization; try a different approach

---

### Thread 2: Bilateral Triple Module Action

**File:** `rh_phase24_thread2.py`
**Output:** `phase24_thread2_results.json`, `RH_Phase24_Thread2_Results.md`

**The test:** Phase 21C showed the module map H₅(q·v) = q·H₅(v) is ill-defined for the full 6-root set because sedenion products escape the 5D fixed subspace (32/36 products escape). The 12-vector closure of {q2, q3, q4} is finite and self-contained. Test whether multiplication by q3 (the bilateral hub) defines a well-defined action *within* the 12-vector closure.

**Why this matters:** If the 12-vector set is closed under left-multiplication by q3, then L_q3 defines an endomorphism of the 12-vector space. An H₅ commuting with L_q3 on this space would be constrained. Phase 21A found no constraint from the full 6-root set — but the 12-vector closure is a different, smaller object.

**Computations:**

**1. Multiplication table within the 12-vector closure**
For each pair (v_i, v_j) from the 12-vector closure, compute the sedenion product and check:
- Does the result lie in the span of the 12 closure vectors?
- If yes: which linear combination?
- If no: what is the "escape" — where does it land?

Build the full 12×12 multiplication table. Report: how many products stay within the closure vs escape.

**2. L_q3 action on the 12-vector closure**
q3 is the bilateral hub. Compute q3 · v_i for each of the 12 closure vectors.
- Which products are zero? (Known: q3·q2=0, q3·q4=0)
- Which products stay in the 12-vector closure?
- Which escape?

Build the 12×1 action table for left-multiplication by q3.

**3. Sub-module identification**
The bilateral zeros q3·q2=0 and q3·q4=0 define a kernel. What is the kernel of L_q3 acting on the 12-vector closure? Is the kernel a sub-module?

Candidate kernel: {q2, q4, sign_partner(q3), scalar, ±e15} — the vectors that q3 annihilates within the closure.

**4. Eigenspace structure**
For vectors v_i where q3·v_i ≠ 0, compute the eigenvalue: does q3·v_i = λ·v_i for some scalar λ? If yes, report λ. If not (mixed output), report the decomposition.

**5. Commutator test**
Define H₅ on the 12-vector closure as the restriction of the AIEX-001 operator. The Phase 21C blocker was [H₅, L_q3] not being well-defined because L_q3 escapes the domain. Within the 12-vector closure, is [H₅, L_q3] well-defined? Does it impose constraints on H₅'s eigenvalues restricted to the closure?

**6. Comparison with Phase 21A**
Phase 21A tested whether the Gram matrix commutativity [H₅, G]=0 forces simple spectrum. Report: does the 12-vector structure impose any eigenvalue constraint that the full 6-root Gram matrix did not?

**Key result to look for:**
- If L_q3 maps the 12-vector closure to itself → well-defined module action found; test for eigenvalue constraints
- If L_q3 escapes the 12-vector closure → smaller finite algebra doesn't help; close this avenue
- If the kernel of L_q3 on the closure is a proper sub-module → new algebraic structure worth investigating

---

## Output Standards

**JSON:** All numpy types → Python native (float/int/bool); replace inf/NaN with None. Use `safe()` helper:
```python
def safe(x):
    import math
    if x is None: return None
    if isinstance(x, (list, tuple)): return [safe(i) for i in x]
    try:
        if math.isnan(x) or math.isinf(x): return None
        return float(x)
    except: return x
```

**Sequences ≥50 elements:** Save in `cailculator_sequences` JSON key for CAILculator MCP handoff. Do NOT compute Chavez locally for these — defer to MCP.

**MD format (match prior phases exactly):**
```
# Phase 24 Thread N Results — [Title]
## Chavez AI Labs LLC · [Date]
**Status:** COMPLETE
**Script:** `rh_phase24_threadN.py`
**Output:** `phase24_threadN_results.json`
---
## Headline
[bold key finding]
---
## Section 1...
---
## Summary Table
| Result | Finding | Significance |
---
## Open Questions for Phase 25
---
*Phase 24 Thread N completed [date]*
*Chavez AI Labs LLC · Applied Pathological Mathematics · "Better math, less suffering"*
```

---

## Closed Avenues (Do NOT Re-investigate)

| Avenue | Phase | Reason |
|---|---|---|
| Simple spectrum from bilateral algebra | 21A | Degenerate H₅=I₅ satisfies all constraints |
| Linear independence from block structure | 21C | Module map ill-defined (32/36 products escape 5D) |
| Full 6-root algebraic closure | 23T1 | Diverges exponentially (6→17→81→878+) |
| Weil identity (non-Schwartz f₅D) | 23T3 | Formally diverges; direction correct, convergence requires window |
| Chavez on sorted pairwise inner products | 22 | Null — sorted pairwise ≠ sequential GUE |

---

## Key File Inventory

| File | What to reuse |
|---|---|
| `rh_phase20b.py` | f5D embedding — canonical reference |
| `rh_phase21b.py` | cd_mul, cd_conj; sedenion products |
| `rh_phase23_thread1_minimal.py` | 12-vector closure generation code |
| `rh_phase23_thread3.py` | S(N) partial sum, RHS direction, residual computation |
| `rh_phase22.py` | gram_G5, P5 projection, safe() JSON helper |
| `phase23_thread1_results.json` | 12-vector closure vectors (exact positions) |
| `phase23_thread3_results.json` | S(N) norms, residual ratios, cailculator_sequences |

---

## What Success Looks Like

**Thread 1 success (strong):** Residual ratio shrinks toward zero as T → ∞. The windowed AIEX-001 embedding satisfies the Weil explicit formula. AIEX-001 connects to a proven theorem.

**Thread 1 success (partial):** Residual ratio decreases with T but doesn't reach zero in the computed range. Provides a decay rate and an extrapolated convergence N.

**Thread 1 null result:** Residual ratio stays ~12% regardless of T. The 6.8° offset is structural — the AIEX-001 embedding has a fundamental geometric relationship with the Weil RHS that a window cannot remove. This is itself a new result: it characterizes the embedding's relationship to the Weil formula precisely.

**Thread 2 success:** L_q3 maps the 12-vector closure to itself and the commutator [H₅, L_q3] imposes an eigenvalue constraint. This reopens the simple spectrum question from a new algebraic angle.

**Thread 2 null result:** L_q3 escapes the 12-vector closure on at least some vectors. The finite closure doesn't help more than the full 6-root set. Close this avenue cleanly.

**All null results are valued.** Each closed avenue tightens the characterization of what the AIEX-001 framework can and cannot prove from within its current structure.

---

## Broader Context

- **Researcher:** Paul Chavez, Chavez AI Labs LLC
- **CAILculator MCP** — available in Claude Desktop only. Scripts prepare `cailculator_sequences` JSON keys for MCP handoff.
- **Chavez conjugation symmetry formula:** `1 − mean(|x[i]−x[n−1−i]|) for i in range(n//2)` on sequence normalized to [0,1]
- **Investigation record scores:** Residual ratio 98.7%, P(N)/N convergence 97.8%, bilateral triple product zero pattern 94.4% / 95% confidence — all from Phase 23
- **The open gap:** Simple spectrum + linear independence of {tₙ·log p} over ℚ. Both confirmed undefeatable from algebra alone. Analytic approaches (Weil, windowed) are the remaining paths.
- **Paper target:** April 1, 2026 — Sophie Germain's 250th birthday. Phase 20 (consolidation) still queued. The investigation is the priority.
- Null results are as valued as positive ones.

---

*Phase 24 Pre-Handoff prepared March 25, 2026*
*Chavez AI Labs LLC · Applied Pathological Mathematics · "Better math, less suffering"*
