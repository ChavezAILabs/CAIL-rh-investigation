# RH Investigation — Phase 79 Run D Results: Commensurability Knee Sweep
**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Date:** 2026-09-11
**Phase:** 79 (Run D)
**Tag:** #phase-79-rund-knee-sweep
**Execution:** Claude Sonnet 5 (Claude Code, in-shell)
**Branch:** `phase-79-runD` (local commit only — no GitHub push per the standing gate)
**Status:** Complete. **The tested prediction (γ_knee ≈ 2π·p_max) is not supported.**

---

## Executive Summary

C-001 (2026-09-08) found that the Detector Encoding's per-zero discriminating power
declines monotonically with height, and offered — explicitly as untested conjecture —
a mechanism: a detector truncated at prime p_max has a finest oscillation period of
2π/log(p_max), while the mean zero spacing at height t is 2π/log(t/2π); when zeros
pack tighter than the truncation can resolve, discrimination should degrade. Setting
the two periods equal gives a one-parameter, no-free-constants prediction:
**γ_knee ≈ 2π·p_max.**

Run D tested this directly: seven prime truncations (p_max = 7, 11, 13, 17, 19, 23,
29), each measured for local ROC AUC in sliding windows of zeros across t ∈ [10,600],
with a two-segment (broken-stick) regression locating the height at which each arm's
AUC-vs-height curve breaks from a shallow to a steep decline, and a 2,000-resample
bootstrap giving a CI on that breakpoint.

**Result: the fitted breakpoints do not track p_max.** They cluster tightly between
132.8 and 156.0 (five of seven arms land on the *identical* value, 148.27) against a
predicted range of 43.98 to 182.21 — better than a 4× span. A flat, no-p_max-dependence
model fits the seven (p_max, breakpoint) points with RSS = 289.3; the literal
prediction bp = 2π·p_max (zero free parameters) has RSS = 26,697.0, **92× worse**; the
freely-fit OLS line has a **negative** point-estimate slope (−0.41, vs. the predicted
+6.28) and only trivially improves on the flat model (RSS = 231.8, R² = 0.199 against
the flat-model baseline). The nested-bootstrap 95% CI on the slope, [−9.72, 14.93],
technically contains 2π — but it contains almost anything, including zero and the
observed negative point estimate, which is a statement about this design's very low
power, not about support for the prediction. See §4.

**Mechanism.** The seven arms' AUC-vs-height curves are strongly correlated with each
other (pairwise r = 0.56–0.96, §3) rather than independent per-arm signals. C-006
established that w_p = log(p)/√p peaks at p = 7 and *decreases* for larger p, so each
arm's newly added high-p_max term carries progressively less amplitude than the
shared low-order core {2,3,5,7} already present in arm A. The aggregate local-AUC
curve is dominated by that shared, large-amplitude, low-frequency core; the fine
oscillation whose period sets the C-001 mechanism is a comparatively small
perturbation riding on top of it, and does not visibly relocate where the aggregate
rank statistic breaks from a shallow to a steep decline. What each arm shows instead
is close to one smooth, common-shaped decay (matching the aggregate decay C-001/C-011
already reported), and the two-segment fit's "breakpoint" reads as a generic feature
of fitting two lines to a mildly concave curve, not a location tied to that arm's own
p_max.

**Controls point the same direction.** The term-count control (arm C minus p=3, same
max frequency) was predicted to leave the knee unmoved — instead it shifted from
148.27 to 101.96, a bigger move than most of the p_max arms show relative to each
other. The non-prime control (p=13 → q=15, predicted knee ≈ 94.2) landed on the exact
same breakpoint as arm C (148.27) — no movement, the opposite of what a
frequency-driven mechanism predicts. Neither behaves as the commensurability
mechanism requires; both are consistent with "this statistic is dominated by which
low-order terms are present, not by the truncation's maximum frequency." See §5.

**The secondary channel (amplitude-normalized T1) shows the same qualitative
pattern independently** — clustered breakpoints (102–133), no clean p_max tracking,
and three of seven arms (A, C, D) fail to reach even an interior, non-boundary fit.
See §6.

**What this does and does not settle.** This refutes the specific numeric claim —
γ_knee ≈ 2π·p_max, tested via local-AUC segmented regression on the explicit-formula
detector family — as tested by this design. It does not re-open C-001's separate,
independently-established finding that per-zero detector strength declines with
height (§3 reconfirms that decay is present and shared across all seven arms); it
only refutes the specific commensurability mechanism offered to explain it. A null
result is a result, and this is the empirical spine question Phase 79 was opened to
answer plainly (see `CORRECTIONS.md` C-001). §8 records what a better-powered test of
the same idea would need.

Every quantity in this document is a bootstrap CI or an F-test p-value on directly
measured data — **no Monte-Carlo permutation null is used anywhere in Run D**, and it
must not be conflated with the permutation-null p-values elsewhere in the corpus
(C-007/C-008). The `seed = 20260612` recorded throughout is the bootstrap-resampling
RNG seed, not a null-distribution seed. See §8 for the important caveat on the F-test
p-values (the Davies 1987 problem).

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
control (per the instruction to fix one width across all series). Local AUC per
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

## 2. Per-Arm Results

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
model, p < 0.05) — but see §8: this p-value is uncorrected for the breakpoint
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

---

## 4. Slope Fit: Breakpoint vs. p_max

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
variance in fitted breakpoint across arms. **The honest reading is: this design finds
no detectable p_max-dependence in the breakpoint location, and what dependence the
free fit does show points the wrong way.**

---

## 5. Control Arms

| Control | Predicted knee | Fitted breakpoint | 95% CI | vs. arm C (148.27) |
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
commensurability mechanism as the driver of what this design measures.

---

## 6. Secondary Channel: Amplitude-Normalized T1

Reported alongside AUC per the handoff (raw T1 is not used for cross-arm comparison,
per its own amplitude-scale caveat; this is the RMS-normalized form):

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
the noisier of the two channels, as the handoff anticipated in naming AUC primary;
it does not rescue the prediction.

---

## 7. What Is Confirmed, Separately From the Refuted Mechanism

C-001's underlying observation — that per-zero detector discrimination declines with
height — is not reopened by this result and is visible directly in every arm's raw
window series (monotone-ish decline from the low-γ end to the high-γ end, all seven
arms, both channels). What Run D refutes is specifically the *mechanism offered to
explain that decline* (a p_max-tracking commensurability knee), not the decline
itself.

---

## 8. Methodological Caveats

- **The F-test p-values in §2 are uncorrected for the Davies (1987) problem.** The
  breakpoint is chosen by grid search over 60 candidates before the F-test is run
  against it, which is equivalent to an unadjusted multiple comparison; the reported
  p-values are a liberal (too-easily-significant) indicator, not a corrected
  significance test. This document treats the bootstrap CI, not the p-value, as the
  primary evidence for "is there a locatable interior break" — and even by that more
  conservative standard, the *location* is what fails to track p_max.
- **No Monte-Carlo permutation null is used anywhere in Run D.** AUC is a rank
  statistic computed directly from the deterministic detector and zero data; the
  segmented regression, F-test, and bootstrap CI are all computed directly from data
  with no randomized null distribution involved. `seed = 20260612` is recorded
  throughout as the bootstrap-resampling RNG seed only, and must not be read as (or
  conflated with) the permutation-null seed used elsewhere in the corpus for T1
  z-scores (C-007/C-008's `n_trials = 5000` machinery is not invoked here at all).
- **Window design deviates from the handoff's suggested default** (§1.1), for a
  documented, data-driven reason (the zero-density argument above), not a
  post-hoc search for a result. The same width (20/5) is applied uniformly to all
  nine series.
- **Arm A was not the outlier this design anticipated.** The handoff flagged arm A
  specifically as likely measurement-limited (predicted knee near γ₈). With the
  retuned window width, arm A converges to a non-boundary fit like every other arm —
  it is not distinguished from the rest of the family; all seven behave alike.

---

## 9. Recommendations for a Better-Powered Test

Not executed here (out of scope for this run; recorded for a future Phase 79/80
follow-on):

1. **Isolate the marginal contribution of the newly added term directly**, e.g. fit
   the segmented model to `AUC(arm_k) − AUC(arm_{k-1})` or to a per-arm residual
   after regressing out the shared low-order core, rather than to each arm's raw
   aggregate AUC — this should suppress the shared-shape effect identified in §3 and
   give the added term's own frequency a chance to show up in the breakpoint.
2. **Extend the zero range** beyond γ₃₄₀ (Run C's grid already reaches t=600; more
   zeros could be pulled from the existing 1,000-zero dataset without a new grid) to
   thicken the post-knee segment and narrow the very wide bootstrap CIs (all ≥ 300
   units in §2).
3. **A finer or adaptive breakpoint search** (continuous optimization rather than a
   60-point grid) would remove the Davies-problem caveat from the p-values, though it
   would not by itself fix the power problem identified in §3–§4.

---

## 10. Artifacts

| Artifact | Path |
|---|---|
| Sweep script | `scripts/phase79_runD_knee_sweep.py` |
| Per-arm/per-window results | `results/phase79_runD_results.json` |
| Slope fit + controls comparison | `results/phase79_runD_slope_fit.json` |
| Corrections register (C-001 background) | `CORRECTIONS.md` |
| Handoff | `../rh-phase79-runD-claude-code-handoff.md` |

`roc_auc`, `local_maxima`, `peak_matching`, `t1_value_at_zeros` are copied verbatim
from `phase78_q18_candidate1_per_gateway.py` into the Run D script, per the handoff's
explicit instruction not to reimplement them; only `roc_auc` is used in the primary
analysis (the other three are carried for fidelity and available for any follow-on
that needs them, per §9).

---

## 11. Open Items

- **§9's three follow-on designs** are not run. Whether to pursue one is Paul's call —
  none is required by this phase's mandate, which was to test the prediction as
  stated.
- **Lean, `detector_channel_identity`, and k=3 slot saturation** — untouched, per the
  handoff's explicit out-of-scope list.
- **RH paper draft** — not edited in this task, per the handoff. This document is the
  input Run D was commissioned to produce for that draft; the paper itself is a
  separate, later task.
- **KSJ extraction** — not run. Per standing workflow, `extract_insights` goes
  through Claude Desktop, not Claude Code.
- **GitHub push** — not performed. Work is committed locally on `phase-79-runD` only,
  per the standing push gate (Paul's explicit review required).

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 79 Run D · September 11, 2026*
