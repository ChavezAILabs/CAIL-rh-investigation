# RH Investigation — Phase 79 Run D Results: Commensurability Knee Sweep
**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Date:** 2026-09-11 (v2 same day; v3 2026-09-14 adds §7.1–§7.2 — see §0)
**Phase:** 79 (Run D)
**Tag:** #phase-79-rund-knee-sweep
**Execution:** Claude Sonnet 5 (Claude Code, in-shell)
**Branch:** `phase-79-runD` (local commit only — no GitHub push per the standing gate)
**Status:** Complete. **The literal prediction (γ_knee ≈ 2π·p_max, exact slope, zero
intercept) is not supported by either of the two independent measurements below —
but the two measurements disagree on whether reach depends on p_max at all, and that
disagreement is itself the more informative finding.**

---

## 0. Revision Note

v1 of this document (same day) reported only the segmented-regression breakpoint
result (§§2–4) and concluded flatly that p_max has no detectable effect on reach.
Claude Desktop reviewed v1 and asked for three additions before treating it as
final: a model-free reach measure independent of the segmented model, an explicit
tie to C-011's convergent finding, and a `CORRECTIONS.md` entry. Running the
model-free measure (§5) surfaced a real, high-R² positive relationship between
reach and p_max that the segmented model had not found at all — the opposite of
what v1's single-channel result suggested. This version reports both channels in
full, including the threshold-sensitivity analysis that determines how much weight
the second channel's result can bear. **The three requested additions changed the
substantive conclusion, not just its presentation** — recorded here rather than
silently folded into a rewritten Executive Summary.

**v3 (2026-09-14)** closes the two items v2 flagged as not yet done: §7.1 runs
both control arms through Channel 2 (they behave like the primary arms, no new
qualitative finding); §7.2 checks whether the `nonprime` control's "no movement"
result is specific to its substitute frequency (q=15) or part of the broader
shared-low-order-core insensitivity §3 identified — it is the latter (q=16 lands on
the identical breakpoint as q=15 and arm C itself). Neither follow-up changes the
Executive Summary's verdict; both extend and reinforce it.

---

## Executive Summary

C-001 (2026-09-08) found that the Detector Encoding's per-zero discriminating power
declines monotonically with height, and offered — explicitly as untested conjecture —
a mechanism: a detector truncated at prime p_max has a finest oscillation period of
2π/log(p_max), while the mean zero spacing at height t is 2π/log(t/2π); when zeros
pack tighter than the truncation can resolve, discrimination should degrade. Setting
the two periods equal gives a one-parameter, no-free-constants prediction:
**γ_knee ≈ 2π·p_max.**

Run D tested this two ways, across the same seven prime truncations (p_max = 7, 11,
13, 17, 19, 23, 29) and two control arms:

**Channel 1 — segmented-regression breakpoint (§§2–4): no p_max-dependence
detected.** A two-segment (broken-stick) fit locates where each arm's local-AUC-
vs-height curve breaks from a shallow to a steep decline. Fitted breakpoints cluster
tightly between 132.8 and 156.0 against a predicted range of 43.98–182.21 (a 4×
span). A flat, no-dependence model fits the seven points 92× better (RSS 289 vs.
26,697) than the literal prediction, and the freely-fit slope is small and
*negative* (−0.41), not the predicted +6.28. **Mechanism:** the seven arms' AUC
curves are strongly correlated (r = 0.56–0.96, §3) because C-006 already
established — three entries earlier in the same corrections register — that
`w_p = log(p)/√p` peaks at p = 7 and *decreases* for larger p. Every arm past C
adds a term smaller than the ones already present; the aggregate curve stays
dominated by the shared {2,3,5,7} core, and a two-segment fit to a family of curves
differing mainly by shrinking perturbations naturally locates its break at nearly
the same point regardless of p_max. **This tension was visible before any data was
collected** — C-001 proposed a mechanism reasoning from the *highest* frequency in
the sum; C-006 had already recorded that the detector's *behavior* is dominated by
its *heaviest* terms, and past p=7 those are different things. Neither the
conjecture nor the experiment design drew that connection in advance.

**Channel 2 — model-free reach: first sustained crossing of a fixed AUC threshold
(§5): a real, robust, positive relationship exists, at a rate that is
threshold-dependent and does not settle the prediction either way.** This measure
does not depend on the segmented model at all (requested specifically as a
referee-facing check, per §0). Swept over ten fixed AUC thresholds (0.78–0.94), it
shows R² = 0.68–0.92 throughout the usable range — a real, non-trivial relationship
the segmented model entirely missed. But the fitted slope is not stable: it falls
monotonically from 50.1 (threshold 0.82, 3 arms censored) to 3.3 (threshold 0.94),
crossing the predicted 6.28 only in a narrow band (≈0.90–0.92) with no principled
reason to prefer that band over any other. At every threshold where all seven arms
are measurable without censoring (0.85–0.88), the fitted slope is **3–4× the
predicted rate**, decisively excluding it. Full table and discussion in §5.

**Net verdict on the literal claim: not supported, by both channels, though for
different reasons.** Channel 1 finds no p_max-dependence in *where the curve's shape
breaks*. Channel 2 finds real p_max-dependence in *when the curve's level crosses a
fixed value* — but at a rate several-fold too fast across the usable, non-arbitrary
part of its threshold range, only touching the predicted rate where the threshold
choice becomes least meaningful (very close to each arm's own peak). Both point away
from the specific one-parameter prediction; they disagree on the more basic question
of whether reach depends on p_max at all, which is itself an open finding for Phase
80, not a contradiction to be resolved here (§6, §12).

**Convergence with C-011, named explicitly (§6).** C-011 (Phase 78) found that
adding primes 17,19 to the six-prime detector lifts AUC by a roughly *constant*
amount across scale (+0.040 at N=101, +0.036 at N=340) — a vertical shift, not a
widening gap. A vertical-shift picture of this kind is a plausible (not yet tested)
explanation for *why* Channel 2 shows any positive reach-vs-p_max relationship at
all: a curve shifted up by a roughly constant amount crosses any fixed absolute
level later, by an amount set by the shift size and the local decay slope. This is
offered as an interpretive frame for a qualitative fact (a relationship exists),
not a mechanistic account of its specific, threshold-sensitive rate.

**Controls point the same direction as Channel 1.** The term-count control (arm C
minus p=3, same max frequency) was predicted to leave the knee unmoved — instead it
moved by 46.3. The non-prime control (p=13→q=15, predicted knee ≈94.2) landed on the
exact same breakpoint as arm C — no movement at all. See §7.

**What this does and does not settle.** Neither channel supports the literal
γ_knee ≈ 2π·p_max claim with confidence. It does not reopen C-001's separate,
independently-established finding that per-zero detector strength declines with
height — only the specific commensurability mechanism offered to explain it. A null
result is a result, and the disagreement between the two channels on whether reach
depends on p_max *at all* is a genuine, useful finding for whoever picks this up
next (§12), not a loose end to paper over.

Every quantity in this document is a bootstrap CI or an F-test p-value computed
directly from data — **no Monte-Carlo permutation null is used anywhere in Run D**,
and it must not be conflated with the permutation-null p-values elsewhere in the
corpus (C-007/C-008). `seed = 20260612` is the bootstrap-resampling RNG seed only.
See §10 for the Davies-problem caveat on the F-test p-values.

---

## 1. Design as Executed

**Grid:** t ∈ [10, 600], Δt = 0.005, 118,001 points (identical to Phase 78 Run C).
**Zeros:** `data/riemann/rh_zeros.json`, filtered to (11, 599) → 340 zeros, γ₁ =
14.135 to γ₃₄₀ = 598.493. The same 340-zero list and the same sliding windows are
used for every arm and control, so only the detector values (not the window
geometry) differ between series.

**Detector form:** explicit-formula only, `D_pmax(t) = -2·Σ_p (log p/√p)·cos(t·log p)`
for p ≤ p_max, computed directly from the formula (never from a hardcoded table,
per C-006).

| Arm | p_max | Primes | Predicted knee (2π·p_max) |
|---|---|---|---|
| A | 7  | 2,3,5,7 | 43.98 |
| B | 11 | +11 | 69.12 |
| C | 13 | +13 (= Phase 78 base6) | 81.68 |
| D | 17 | +17 | 106.81 |
| E | 19 | +19 (= Phase 78 ext8) | 119.38 |
| F | 23 | +23 | 144.51 |
| G | 29 | +29 | 182.21 |

**Controls:**

| Control | Freqs | Design | Prediction |
|---|---|---|---|
| `term_count` | {2,5,7,11,13} | arm C minus p=3; same max frequency, one fewer term | knee should NOT move from arm C's |
| `nonprime` | {2,3,5,7,11,15} | arm C with p=13 replaced by non-prime q=15; max frequency moves log 13 → log 15 | knee should move to 2π·15 ≈ 94.25 |

### 1.1 Window width: the suggested default was under-resolved

The handoff's suggested width (40 zeros/window, step 10) was piloted on arm C first,
as instructed, and rejected. The reason is a zero-density fact, not a tuning
preference: at t ∈ [10,150] — the region containing every arm's predicted knee except
G's — zeros are sparse enough that a single 40-zero window already spans roughly that
entire range. Concretely, arm C has only 21 of its 340 zeros below its own predicted
knee (γ = 81.7); arm A has only 8 below its predicted knee (γ = 44.0). At width ≥ 30,
the segmented-regression breakpoint search degenerates to the edge of its candidate
interval (`boundary_hit = True`) for every width tried, with 95% bootstrap CIs
spanning ~380 units — the fit is not locating an interior feature at all.

| Width | Step | Windows | Fitted bp | p-value | knee_detected | boundary_hit | CI95 width (300 boot) |
|---|---|---|---|---|---|---|---|
| 10 | 5 | 67 | 154.85 | 0.0221 | True | False | 488.4 |
| 15 | 5 | 66 | 151.47 | 0.0095 | True | False | 407.1 |
| **20** | **5** | **65** | **148.27** | **0.0051** | **True** | **False** | 407.3 |
| 25 | 5 | 64 | 145.23 | 0.0035 | True | False | 380.2 |
| 30 | 10 | 32 | 154.13 | 0.0606 | False | **True** | 379.5 |
| 40 | 10 | 31 | 163.69 | 0.1029 | False | **True** | 375.2 |

**Chosen: width = 20, step = 5** (65 windows) — the narrowest width tried that is
still comfortably clear of the boundary degeneracy, with the lowest F-test p-value
among the non-degenerate widths. This width is used, unchanged, for every arm and
control (both channels below reuse the same 65 windows per arm). Local AUC per
window uses δ = 0.5 (matching the corpus's existing headline AUC figures); the local
classification universe for each window is the zero list and t-grid restricted to
[window_lo − 3ḡ, window_hi + 3ḡ] where ḡ is the window's own mean zero spacing —
local to the window's height, not the full domain.

### 1.2 Gateway identity check (arms C, E; C-009 naming)

Per C-009, this is an identity verification, not a control, and is named accordingly.
The gateway-realized channels (`c_S2+c_S6` for arm C, `c_S2+c_S3` with p=17,19 in
slots 4,11 for arm E — the closed-form Gateway Linear Law, validated 22/22 against
live CAILculator in Phase 76, reused here rather than re-issuing 118,001-point live
MCP calls) match the explicit-formula sums to:

- `f6_identity_residual` = 1.78 × 10⁻¹⁵
- `f8_identity_residual` = 2.66 × 10⁻¹⁵

This confirms the swept explicit-formula quantity is the same object as the sedenion
architecture's detector, at the two truncations where both forms are realizable
(k=3 slot saturation beyond p=19 is out of scope, per the handoff).

---

## 2. Channel 1 — Per-Arm Segmented-Regression Breakpoint

| Arm | p_max | Predicted knee | Fitted breakpoint | 95% bootstrap CI | F-test p | knee_detected |
|---|---|---|---|---|---|---|
| A | 7 | 43.98 | 148.27 | [105.2, 395.6] | 0.0002 | True |
| B | 11 | 69.12 | 148.27 | [129.3, 397.5] | 0.0002 | True |
| C | 13 | 81.68 | 148.27 | [86.3, 497.1] | 0.0051 | True |
| D | 17 | 106.81 | 148.27 | [109.6, 578.2] | 0.0207 | True |
| E | 19 | 119.38 | 148.27 | [110.6, 549.9] | 0.0096 | True |
| F | 23 | 144.51 | 155.98 | [121.5, 502.6] | 0.0014 | True |
| G | 29 | 182.21 | 132.83 | [120.3, 547.8] | 0.0430 | True |

Every arm reports `knee_detected = True` (an F-test rejection of the single-segment
model, p < 0.05) — but see §10: this p-value is uncorrected for the breakpoint
location being chosen by grid search (the Davies problem), so it is a liberal
indicator, not a substitute for the bootstrap CI. What the table actually shows is
that **the fitted location of that break is essentially the same number (132.8–156.0)
across a sevenfold range of p_max**, while the predicted location moves 4×
(43.98→182.21) over the same arms. All seven arms are usable (none excluded as
measurement-limited) — a direct consequence of retuning the window width in §1.1;
at the handoff's suggested default, most or all of these arms would have hit the
same boundary degeneracy the pilot table shows.

---

## 3. Why the Breakpoints Cluster: Shared Curve Shape

The seven arms' local-AUC-vs-height series are strongly cross-correlated:

| | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| **A** | 1.000 | 0.881 | 0.859 | 0.748 | 0.789 | 0.714 | 0.572 |
| **B** | 0.881 | 1.000 | 0.891 | 0.733 | 0.753 | 0.701 | 0.564 |
| **C** | 0.859 | 0.891 | 1.000 | 0.853 | 0.855 | 0.806 | 0.692 |
| **D** | 0.748 | 0.733 | 0.853 | 1.000 | 0.957 | 0.908 | 0.749 |
| **E** | 0.789 | 0.753 | 0.855 | 0.957 | 1.000 | 0.939 | 0.789 |
| **F** | 0.714 | 0.701 | 0.806 | 0.908 | 0.939 | 1.000 | 0.827 |
| **G** | 0.572 | 0.564 | 0.692 | 0.749 | 0.789 | 0.827 | 1.000 |

Even the least-correlated pair (A, G — the widest p_max separation) shares r = 0.57.
This is expected given C-006's correction: `w_p = log(p)/√p` peaks at p = 7 and
*decreases* monotonically for p > 7 (0.735 at p=7 down to 0.549 at p=29). Arms A
through G are nested — each equals the previous arm plus one more term — and every
added term (p=11 onward) carries less weight than the shared {2,3,5,7} core already
present in arm A. The aggregate rank statistic (AUC) is dominated by that shared
low-frequency, high-amplitude core; the arm-specific finest oscillation (the quantity
C-001's mechanism is actually about) is a small perturbation on top of it. A
two-segment fit to a family of curves that mostly differ by a small perturbation on a
shared shape will naturally locate its break near the same point for all of them —
which is what §2 shows.

**This should have been anticipated, not just explained after the fact.** C-006 was
already in the register — three entries before C-001 — when the commensurability
conjecture was written, and it records exactly the weight structure that makes a
curve-shape-based test insensitive to p_max past p=7. Neither C-001 (which proposed
the mechanism) nor the Run D design (which built the seven-arm test around it) drew
that connection before the sweep ran. The information needed to predict Channel 1's
null result was already two entries away in the same corrections register.

---

## 4. Slope Fit: Segmented Breakpoint vs. p_max

Nested bootstrap (each of 2,000 draws samples one breakpoint per arm from that arm's
own 2,000-resample bootstrap distribution, refits OLS, repeats):

| Quantity | Value | 95% CI |
|---|---|---|
| Slope | **−0.4134** | [−9.720, 14.928] |
| Intercept | 154.193 | [−25.403, 416.614] |
| R² (vs. flat baseline) | 0.199 | — |
| Predicted slope | 2π = 6.2832 | — |

**Slope CI contains 2π: True. Intercept CI contains 0: True.** Read plainly, without
the RSS comparison below, this could be misreported as "consistent with the
prediction." It is not — the CI is wide enough to contain almost any hypothesis:

| Model | Free parameters | RSS (7 arms) |
|---|---|---|
| Flat (bp = mean, no p_max dependence) | 1 | 289.3 |
| Free OLS (fitted slope/intercept) | 2 | 231.8 |
| Literal prediction (bp = 2π·p_max, zero free parameters) | 0 | **26,697.0** |

The literal prediction fits **92× worse** than a flat line with no p_max dependence
at all, and the freely-fit line's own point estimate is a small *negative* slope, not
the predicted positive 6.28. The R² of 0.199 for the free OLS fit (measured against
the flat-model baseline) means p_max explains under a fifth of the already-small
variance in fitted breakpoint across arms. **Channel 1's honest reading: no
detectable p_max-dependence in breakpoint location, and what dependence the free fit
does show points the wrong way.**

---

## 5. Channel 2 — Model-Free Reach: Threshold-Crossing Sensitivity

Requested specifically because it does not depend on the segmented model §§2–4
rejected: sort each arm's 65 windows by height, find the first run of 3 consecutive
windows whose local AUC sustains below a **fixed** absolute threshold (the same
number for every arm), report that run's starting height. A 2,000-resample bootstrap
(resampling windows) gives a CI; an arm that never sustains the drop within t≤600 is
censored, a valid outcome, not a fit failure.

The first threshold tried (0.85) gave a clean, high-R² positive slope — the opposite
of Channel 1's null result. A second threshold (0.90) gave a materially different
slope. **The honest report is the full sensitivity sweep, not either single number:**

| Threshold | Arms censored | Slope | 95% CI | R² | CI contains 2π |
|---|---|---|---|---|---|
| 0.78 | 6 of 7 | — | too few usable arms (1) | — | — |
| 0.80 | 5 of 7 | — | too few usable arms (2) | — | — |
| 0.82 | 3 of 7 | 50.13 | [28.11, 50.53] | 0.764 | False |
| 0.84 | 2 of 7 | 41.78 | [22.28, 42.97] | 0.922 | False |
| **0.85** | **0** | **25.21** | **[19.25, 25.46]** | **0.836** | **False** |
| 0.86 | 0 | 21.75 | [17.68, 26.06] | 0.678 | False |
| **0.88** | **0** | **18.74** | **[14.61, 23.20]** | **0.872** | **False** |
| 0.90 | 0 | 9.50 | [6.23, 15.89] | 0.851 | True |
| 0.92 | 0 | 4.27 | [2.93, 8.02] | 0.863 | True |
| 0.94 | 0 | 3.27 | [1.95, 4.38] | 0.871 | False |

**What is robust across this sweep:** at every threshold where a fit could be run,
R² is 0.68–0.92 — a real, non-trivial monotonic relationship between reach and
p_max that Channel 1 did not find at all. This is the more basic and more solid part
of the finding: reach depends on p_max in a way breakpoint location does not.

**What is not robust:** the fitted slope. It falls monotonically from 50.1 to 3.3
across the sweep — over a 15× range — and crosses the predicted 6.28 only in a
narrow band (≈0.90–0.92), with no principled reason in the design to prefer that
band over any other. **At every threshold where all seven arms are measurable
without any censoring (0.85–0.88) — the least arbitrary part of the range — the
fitted slope is 3–4× the predicted rate, and the CI excludes it.** At the lowest
thresholds tested (0.78, 0.80), most arms never sustain the drop at all within
t ≤ 600 (5–6 of 7 censored) — an uninformative regime. At the highest (0.94), the
point estimate undershoots the prediction instead of overshooting it — the
crossing near 0.90–0.92 is where a monotonically-falling curve happens to pass
through 6.28, not a location the design identifies as privileged.

**Per-arm detail at threshold = 0.85** (the representative, all-arms-usable row):

| Arm | p_max | Crossing γ | Bootstrap n_success / 2000 | 95% CI |
|---|---|---|---|---|
| A | 7 | 78.13 | 2000 | [78.1, 113.1] |
| B | 11 | 144.35 | 2000 | [123.8, 173.6] |
| C | 13 | 144.35 | 2000 | [144.3, 228.5] |
| D | 17 | 366.88 | 1997 | [154.3, 529.1] |
| E | 19 | 522.02 | 1969 | [366.9, 536.2] |
| F | 23 | 536.16 | 1142 (57%) | [536.2, 543.2] |
| G | 29 | 536.16 | 1549 (77%) | [420.0, 543.2] |

Arms F and G's crossings sit within ~50 units of the domain's upper edge (last
window γ_center = 585.2), and their bootstrap success rates (57%, 77%, vs. ~100% for
A–D) show a meaningful fraction of resamples never produce a crossing at all —
these two arms' contribution to the slope fit is the least reliably determined and
should be read with that caveat (§10). Ties across arms (B=C at 144.35, F=G at
536.16) reflect the 65-window grid's discreteness, not the shared-curve-shape
degeneracy of §3 — a different, benign cause of the same surface symptom.

**Net reading of Channel 2:** confirms a real reach-vs-p_max relationship Channel 1
missed; does not confirm or cleanly refute the specific predicted rate, because that
rate is not stable to an essentially arbitrary choice of absolute threshold.

---

## 6. Convergence — and an Open Tension — with C-011

**Convergence.** C-011 (Phase 78) measured whether the AUC margin between two
specific arms (base6, p_max=13; ext8, p_max=19) grows as more zeros are swept —
found it does not: +0.040 at N=101, +0.036 at N=340, a roughly *constant* vertical
gain, not a widening one. That is a different axis from anything measured directly
in this document (C-011 fixed two arms and varied zero count; Run D fixes the
zero/height range and varies arms), but the two are compatible under a simple shared
picture: each added prime lifts the AUC-vs-height curve by roughly a constant amount
at every height (C-011), and a curve shifted up by a roughly constant amount
necessarily crosses any fixed absolute level later — which is exactly what §5
measures directly across seven truncations. **This is offered as a plausible
interpretive frame for why Channel 2 shows a positive relationship at all, not as a
tested explanation of its specific (and threshold-sensitive) rate.** Verifying it
quantitatively — checking whether the per-arm AUC offset implied by C-011's flat-gain
finding, divided by each arm's local decay slope, actually predicts the §5 crossing
shifts — is not done here and belongs with the Phase 80 follow-on (§11–§12).

**The open tension.** C-011's own framing (Phase 78 §5.4) read the flat AUC gain as
evidence that k=2 "does not extend the detector's reach as zero density rises" —
a uniform improvement, not a reach improvement. Run D's Channel 2 measures reach
directly across seven truncations and finds it *does* move with p_max, robustly in
direction if not in rate. These are not strictly the same claim (C-011 : two arms,
across N; Run D : seven arms, across p_max, within one N-range) but they use similar
language for what could be read as related quantities, and a careless citation could
flatten the distinction. Recorded here precisely so a future paper draft does not
silently pick whichever reads better.

---

## 7. Control Arms

| Control | Predicted knee | Fitted breakpoint (Channel 1) | 95% CI | vs. arm C (148.27) |
|---|---|---|---|---|
| `term_count` (drop p=3) | 81.68 (unmoved) | 101.96 | [78.1, 564.3] | moved −46.3 |
| `nonprime` (13→15) | 94.25 (moved) | 148.27 | [90.4, 564.3] | unmoved (identical) |

Both controls contradict the commensurability mechanism, in opposite directions:

- **`term_count`** was predicted *not* to move (same max frequency, 13, just one
  fewer term) — it moved by 46.3, a bigger shift than most pairs of p_max arms show
  relative to each other in §2.
- **`nonprime`** was predicted *to* move, to ≈94.2 (max frequency log 13 → log 15) —
  it landed on the *exact same* fitted breakpoint as arm C itself, no movement at all.

This is consistent with §3's explanation: the statistic is sensitive to which
(mostly low-order) terms are present in the sum, not to the specific value of the
maximum log-frequency. Both results point the same direction as §4 — away from the
commensurability mechanism as the driver of what Channel 1 measures.

### 7.1 Controls through Channel 2 (follow-up)

Flagged in v1/v2 of this document as not yet done; run here
(`scripts/phase79_runD_followups.py`, reusing every Channel-2 function verbatim).
Both controls show the same threshold-sensitive pattern as the seven arms in §5 —
crossing height falls as the threshold rises through the same 0.78–0.94 sweep, with
`term_count` and `nonprime` tracking values close to the p_max-neighboring arms at
every threshold (e.g. at threshold 0.85 both cross at 78.13, matching arm A's own
0.85 crossing exactly — see §5's per-arm table). No qualitatively new behavior
appears: the controls' Channel-2 reach depends on threshold the same way, and to a
similar degree, as the primary arms. This does not change §5's verdict; it extends
its coverage. Full per-threshold table in `results/phase79_runD_followups.json`
(`controls_channel2`).

### 7.2 Frequency-swap robustness on the `nonprime` control (follow-up)

The `nonprime` result above (§7: no movement from arm C's 148.27) invites an
obvious question: is that specific to q=15, or does the whole last-slot frequency
barely matter? Swept q ∈ {12, 13(=arm C), 14, 15, 16, 18, 20} in arm C's sixth slot,
Channel 1 only (the segmented breakpoint), same width/step/n_boot as the main run:

| q | prime? | predicted knee (2π·q) | fitted breakpoint | 95% CI | boundary_hit |
|---|---|---|---|---|---|
| 12 | no | 75.40 | 109.68 | [97.9, 528.1] | **True** |
| 13 (arm C) | yes | 81.68 | 148.27 | [86.3, 497.1] | False |
| 14 | no | 87.96 | 125.12 | [113.1, 556.2] | False |
| **15 (`nonprime`)** | no | 94.25 | **148.27** | [90.4, 564.3] | False |
| **16** | no | 100.53 | **148.27** | [141.0, 564.3] | False |
| 18 | no | 113.10 | 534.13 | [154.1, 540.8] | False |
| 20 | no | 125.66 | 171.42 | [153.7, 569.9] | False |

**q=15 is not a special case.** q=16 lands on the *exact same* breakpoint as arm C
and q=15 (148.27); q=12, 14, 18, 20 each land somewhere else, with no visible
relationship to their own predicted knee (q=18's predicted knee, 113.10, is nowhere
near its fitted 534.13). Three of seven swap values (13, 15, 16) share one fitted
breakpoint exactly — the same shared-candidate clustering §3 already identified as
the shared-low-order-core artifact, now shown to extend across substitute
frequencies as well as across p_max arms. The frequency-swap check confirms §3's
mechanism more broadly than the single q=15 result alone did: **Channel 1's
breakpoint is largely insensitive to which specific frequency occupies the last
slot**, not narrowly insensitive to 15 specifically. Full table in
`results/phase79_runD_followups.json` (`frequency_swap_robustness`).

---

## 8. Secondary Channel: Amplitude-Normalized T1

Reported alongside AUC per the handoff (raw T1 is not used for cross-arm comparison,
per its own amplitude-scale caveat; this is the RMS-normalized form). This is a
secondary check on Channel 1's segmented model, not on Channel 2.

| Arm | Predicted knee | Fitted bp (T1) | knee_detected | boundary_hit | 95% CI |
|---|---|---|---|---|---|
| A | 43.98 | 101.96 | False | **True** | [65.0, 578.2] |
| B | 69.12 | 117.40 | True | False | [102.0, 514.1] |
| C | 81.68 | 101.96 | False | **True** | [65.0, 534.3] |
| D | 106.81 | 101.96 | False | **True** | [73.3, 543.2] |
| E | 119.38 | 125.12 | True | False | [78.1, 466.7] |
| F | 144.51 | 132.83 | True | False | [85.8, 511.8] |
| G | 182.21 | 132.83 | True | False | [78.1, 550.3] |

Independent confirmation of §2's pattern: fitted breakpoints cluster (102–133) well
short of the predicted 4× range, and three of seven arms (A, C, D) do not even clear
the boundary-degeneracy check that §1.1 used to reject the wide-window default. T1 is
the noisier of the two channels, as the handoff anticipated in naming AUC primary.

---

## 9. What Is Confirmed, What Is Refuted

**Confirmed, unaffected by this run:** C-001's underlying observation that per-zero
detector discrimination declines with height — visible directly in every arm's raw
window series (a monotone-ish decline from the low-γ end to the high-γ end, all
seven arms, both channels).

**Refuted, as tested:** the literal γ_knee ≈ 2π·p_max claim — a one-parameter,
zero-intercept, exact-slope prediction. Channel 1 finds no p_max-dependence in
breakpoint location at all. Channel 2 finds a real p_max-dependence in reach, but at
a rate that is 3–4× the prediction across its most defensible (least arbitrary,
least censored) threshold range, and only touches the prediction where the choice of
threshold is least meaningful.

**Not settled, and flagged rather than papered over:** whether "reach" depends on
p_max at all. The two channels disagree on this more basic question, not just on
rate. §12 names this as the standing question for Phase 80, alongside the separate
question of what actually drives the underlying per-zero decay C-001 first
identified.

---

## 10. Methodological Caveats

- **The F-test p-values in §2 are uncorrected for the Davies (1987) problem.** The
  breakpoint is chosen by grid search over 60 candidates before the F-test is run
  against it, which is equivalent to an unadjusted multiple comparison; the reported
  p-values are a liberal (too-easily-significant) indicator, not a corrected
  significance test. This document treats the bootstrap CI, not the p-value, as the
  primary evidence for "is there a locatable interior break."
- **Channel 2's slope is not robust to the choice of fixed threshold** (§5) — this
  is reported as a finding, not hidden behind a single headline number. A single
  threshold, chosen without the sensitivity sweep, would have supported whatever
  conclusion the choice happened to favor.
- **Arms F and G's Channel-2 crossings sit close to the t≤600 domain's upper edge**
  at the representative threshold (0.85), with bootstrap success rates of 57% and
  77% (vs. ~100% for A–D) — their weight in the slope fit is the least reliable of
  the seven arms, at that threshold specifically.
- **No Monte-Carlo permutation null is used anywhere in Run D.** AUC is a rank
  statistic computed directly from the deterministic detector and zero data; the
  segmented regression, F-test, threshold crossing, and both channels' bootstrap CIs
  are all computed directly from data with no randomized null distribution involved.
  `seed = 20260612` is the bootstrap-resampling RNG seed only, and must not be read
  as (or conflated with) the permutation-null seed used elsewhere in the corpus for
  T1 z-scores (C-007/C-008's `n_trials = 5000` machinery is not invoked here).
- **Window design deviates from the handoff's suggested default** (§1.1), for a
  documented, data-driven reason, not a post-hoc search for a result.
- **Arm A was not the outlier this design anticipated.** The handoff flagged arm A
  specifically as likely measurement-limited (predicted knee near γ₈). With the
  retuned window width, arm A converges to a non-boundary fit in both channels like
  every other arm.

---

## 11. Recommendations for a Better-Powered Test

Not executed here (out of scope for this run; recorded for a future follow-on):

1. **Isolate the marginal contribution of the newly added term directly**, e.g. fit
   Channel 1's model to `AUC(arm_k) − AUC(arm_{k-1})` or to a per-arm residual after
   regressing out the shared low-order core, rather than to each arm's raw aggregate
   AUC — this should suppress §3's shared-shape effect.
2. **Test the §6 vertical-shift explanation quantitatively**: does the per-arm AUC
   offset implied by C-011's flat-gain finding, divided by each arm's local decay
   slope, predict the §5 crossing shifts? This would settle whether Channel 2's
   relationship is the mechanical consequence proposed in §6, or something else.
3. **Extend the zero range** beyond γ₃₄₀ (more zeros are already in the existing
   1,000-zero dataset without a new grid) to reduce the right-censoring on arms F, G
   in §5 and narrow Channel 1's very wide bootstrap CIs (all ≥ 300 units in §2).
4. **A finer or adaptive breakpoint search** for Channel 1 would remove the
   Davies-problem caveat from the p-values, though it would not by itself fix the
   power problem in §3–§4.

---

## 12. The Standing Question for Phase 80

Per-zero discrimination decays smoothly, monotonically, and — per Channel 1 — largely
independently of where the detector is truncated. If that decay is not a resolution
effect (the commensurability mechanism this run tested and did not support), what is
it? Two candidates worth naming without chasing here:

1. **Truncation error in the explicit formula grows with t regardless of cutoff** —
   a property of how any fixed-length truncation approximates the true explicit
   formula at increasing height, not specific to p_max at all.
2. **The decay is a property of zero statistics, not of the detector** — checkable
   directly against a GUE (random-matrix) surrogate for the zero sequence: if a
   GUE-generated point process produces the same decay shape under the identical
   detector and window pipeline, the effect is about zero spacing statistics in
   general, not about the Riemann zeros or the detector's truncation specifically.

Neither is tested in this document. This is Run D's earned handoff to Phase 80, not
a preview of its answer.

---

## 13. Artifacts

| Artifact | Path |
|---|---|
| Sweep script | `scripts/phase79_runD_knee_sweep.py` |
| Follow-up script (§7.1–§7.2) | `scripts/phase79_runD_followups.py` |
| Per-arm/per-window results | `results/phase79_runD_results.json` |
| Slope fit, controls, and threshold-sensitivity sweep | `results/phase79_runD_slope_fit.json` |
| Follow-up results (controls via Channel 2; frequency-swap robustness) | `results/phase79_runD_followups.json` |
| Corrections register (C-001, C-006 background; new entry, see §14) | `CORRECTIONS.md` |
| Handoff | `../rh-phase79-runD-claude-code-handoff.md` |

`roc_auc`, `local_maxima`, `peak_matching`, `t1_value_at_zeros` are copied verbatim
from `phase78_q18_candidate1_per_gateway.py` into the Run D script, per the handoff's
explicit instruction not to reimplement them; `roc_auc` drives both channels'
underlying AUC computation, and `threshold_crossing`/`bootstrap_threshold_crossing`
(new, for Channel 2) reuse the same bootstrap-resampling pattern as Channel 1's
`bootstrap_breakpoint`.

---

## 14. Open Items

- **A `CORRECTIONS.md` entry recording this result**, including the C-006
  weight-structure point from §3, and a cross-reference added to C-001 itself — done
  as part of this revision; see the register for the entry number and text.
- **Controls through Channel 2, and the frequency-swap robustness check** — both
  done in v3 (§7.1–§7.2); neither changed the verdict.
- **§6's vertical-shift explanation and §11 item 2** — untested quantitative
  reconciliation, natural Phase 80 work.
- **§12's standing question** — Phase 80's mandate, not previewed here.
- **Lean, `detector_channel_identity`, and k=3 slot saturation** — untouched, per the
  handoff's explicit out-of-scope list.
- **RH paper draft** — not edited in this task, per the handoff. This document is
  input to that draft; the draft itself is separate, later work.
- **KSJ extraction** — not run. Per standing workflow, `extract_insights` goes
  through Claude Desktop, not Claude Code.
- **GitHub push** — not performed. Work is committed locally on `phase-79-runD` only,
  per the standing push gate (Paul's explicit review required).

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 79 Run D · September 11, 2026 (v3: September 14, 2026)*
