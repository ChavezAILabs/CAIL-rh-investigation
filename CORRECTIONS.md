# CAIL-RH Investigation — Corrections Register

**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Opened:** September 8, 2026
**Maintainer:** Paul Chavez
**Status:** ACTIVE — 21 entries · 2 corrected · 3 confirmed against source ·
3 modified by verification · 13 open
**Last verification batch:** September 8, 2026 (six tasks, Claude Code)

---

## What This Document Is

A permanent, public, append-only record of every error found in the CAIL-RH
Investigation: in results, in documentation, in formal proofs, and in the
interpretation of data.

Entries are never deleted. A corrected entry keeps its original text and gains a
`Corrected` block underneath. Superseded claims elsewhere in the corpus are struck
through and cross-referenced here rather than silently rewritten.

The register exists because this investigation is conducted by a single
independent researcher working with AI assistance across multiple models and
sessions, at a volume no one person can re-verify by hand. That method produces
results faster than traditional review and it produces errors faster too. The only
defensible response is to find them, publish them, and keep the count visible.

**Placement:** repository root, `CORRECTIONS.md`, linked from the top of
`README.md` and from every Zenodo record's description.

---

## Entry Format

```
### C-NNN — [short title]
**Found:** YYYY-MM-DD · **By:** [who/what] · **Severity:** [1–4] · **Status:** [Open | Corrected | Withdrawn | Disputed]
**Affects:** [documents, files, phases, DOIs]

**The claim as published:** [verbatim or close paraphrase]
**Why it is wrong:** [evidence — numbers, not assertions]
**What is true instead:** [the corrected statement, or "under investigation"]
**Corrected:** [date, where, how — added when resolved]
```

### Severity scale

| | Meaning |
|---|---|
| **1** | Cosmetic. Typo, stale count, broken cross-reference. No claim affected. |
| **2** | Documentation error. A reader is misled; no result changes. |
| **3** | Interpretation error. The number is right, what it was said to mean is wrong. |
| **4** | Result error. A published claim is unsupported or false. |

### What triggers an entry

Any of: a published number that cannot be reproduced; a claim whose stated meaning
does not follow from its evidence; a formal proof that is vacuous, circular, or
weaker than advertised; a retraction not propagated to every place the claim
appears; a provenance chain that cannot be traced to an artifact.

---

## Index

| ID | Title | Sev | Status |
|---|---|---|---|
| C-001 | Sub-√N growth misread as signal strengthening | 3 | Open |
| C-002 | "Three independent characterizations" — routes 1 and 2 are not independent | 4 | Open — **confirmed** |
| C-003 | `riemann_critical_line` axiom count stated as one; it is two | 2 | Open |
| C-004 | Retracted Q-2 / Q-4 results still published as CLOSED | 4 | Open |
| C-005 | B/A → 4.0 hypothesis superseded by √17, not withdrawn | 2 | Open |
| C-006 | Explicit-formula weight table wrong for p = 5, 7, 11, 13 | 2 | Open |
| C-007 | Monte-Carlo p-value floor reported as significance | 4 | Open — **partly verified** |
| C-008 | z = 8.42 quoted as a fixed constant | 3 | **Modified** |
| C-009 | Run C "controls" are the detector by identity | 3 | Open |
| C-010 | Candidate 2 ordering claim below measurement resolution | 3 | Open |
| C-011 | Candidate 3 evaluated on one metric, baseline on two | 3 | **Modified** |
| C-012 | Phase 77 baseline artifact provenance broken | 3 | **Modified — central claim refuted** |
| C-013 | Handoff slot assignment {4,7} — index 7 is in no gateway support | 2 | **Corrected** |
| C-014 | `(z_g/Σz)²` weighting formula discards sign and does not normalize | 2 | Open |
| C-015 | Repository tree omits four `.lean` files, including axiom-bearing ones | 1 | Open |
| C-016 | `CD4_mul` defined as the zero function — all Chavez Transform theorems vacuous | 4 | **Corrected** |
| C-017 | `chavez_transform_convergence` is vacuous in the replacement file | 4 | Open |
| C-018 | Chavez Transform verification scope overstated — 1D scalar channel only | 4 | Open |
| C-019 | `eigenvalue_zero_mapping` axiom footprint omits `sorryAx` in both READMEs | 4 | Open — **confirmed verbatim** |
| C-020 | Decorative hypothesis in `Fbase_nondegeneracy`; stale Path B docstring | 2 | Open — **confirmed** |
| C-021 | Critical-line "characterizations" are definitionally engineered | 3 | Open |

---

## Entries

### C-001 — Sub-√N growth misread as signal strengthening
**Found:** 2026-09-08 · **By:** Claude (Opus 5), reviewing Run C JSON · **Severity:** 3 · **Status:** Open
**Affects:** `RH_PHASE_78_RESULTS.md` §4 finding 1 and Executive Summary; `RH_PHASE_77_RESULTS.md` §2A; `rh-phase78-opening-handoff.md` §4A; `README.md` Phase 76–77 narrative; KSJ AIEX-737, 739–742

**The claim as published:** Detector z grows through γ₃₄₀ "at a rate that is
consistently *below* the naive √N extrapolation (sub-√N growth) — genuine
strengthening, not pure statistical scaling."

**Why it is wrong:** The observed T1 statistic declines monotonically with height,
and the null tightens as 1/√N almost exactly. All of the z growth comes from the
shrinking null.

| N | γ_N | observed T1 | null_std | null_std·√(N/101) | z |
|---|---|---|---|---|---|
| 101 | 237.77 | 1.9662 | 0.2309 | 0.2309 | 8.483 |
| 150 | 318.85 | 1.7806 | 0.1919 | 0.2339 | 9.268 |
| 200 | 396.38 | 1.6838 | 0.1669 | 0.2348 | 10.070 |
| 340 | 598.49 | 1.5041 | 0.1265 | 0.2321 | 11.871 |

The rescaled null column is flat to under 2%. Observed falls to 76.5% of its N=101
value. Sub-√N growth means the signal grows *more slowly* than statistical scaling
alone would give; the documents read it as evidence of more.

The same structure is present in Phase 77 and was mislabeled there first: c_S2
observed 1.8464 at 31 zeros → 1.3735 at 101 (74%), null_std 0.5075 → 0.2783
(ratio 0.548 against √(31/101) = 0.554).

**What is true instead:** Per-zero detector strength decays with height. The z
increase is a sample-size effect of the null, not detector improvement. Candidate
mechanism, offered as conjecture and not yet tested: the six-prime detector's
finest oscillation has period 2π/log 13 ≈ 2.45, while mean zero gap
2π/log(t/2π) falls from ≈1.73 at γ₁₀₁ to ≈1.38 at γ₃₄₀ — zeros pack tighter than
the truncation can resolve. This is the prime-log commensurability limit
hypothesized in the July 11 opening handoff.

**Note:** this correction strengthens rather than weakens the research programme.
A measured decay law with a candidate mechanism is a better result than an
unexplained growth claim.

---

### C-002 — "Three independent characterizations" — routes 1 and 2 are not independent
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 4 · **Status:** Open — **confirmed against source 2026-09-08**
**Affects:** `README.md` Principal Result; `lean/README.md` Phase 75 section; planned v1.4 paper; RH paper framing; all milestone claims citing "three routes"

**The claim as published:** "Three independent standard-axiom characterizations of
the critical line Re(s) = ½, formally verified in Lean 4."

**Why it is wrong — confirmed.** `SpectralIdentification.lean` line 47:

```lean
def isSpectralPoint (s : ℂ) : Prop :=
  sedenion_Hamiltonian s = 0
```

`isSpectralPoint s` is not equivalent to H(s) = 0; it *is* H(s) = 0, by definition.
Therefore conjunct 2 of `critical_line_convergence` —
`isSpectralPoint s ↔ s.re = 1/2` — delta-reduces to conjunct 1,
`sedenion_Hamiltonian s = 0 ↔ s.re = 1/2`. The two conjuncts are the same
proposition written twice, which is why `unfold isSpectralPoint` discharges the
step.

Route 2's theorem is correspondingly thin (line 117):

```lean
theorem spectral_implies_critical_line (s : ℂ) (hsp : isSpectralPoint s) :
    s.re = 1 / 2 :=
  (Hamiltonian_vanishing_iff_critical_line s).mp hsp
```

It is the forward projection of route 1, one `.mp` deep. It is not an independent
characterization; it is a corollary with a different name.

**What is true instead:** Two independent mechanisms — the Hamiltonian route and
gateway integrality — expressed as three formulations. `critical_line_convergence`
remains correctly proved under standard axioms and is still worth having as a
formal assembly. Only the independence count is false, and it appears in the
headline sentence of both READMEs.

**Recommended restatement:** "Two independent standard-axiom mechanisms
characterizing Re(s) = ½, assembled with a third equivalent formulation into one
machine-verified conjunction." This costs nothing that was real and removes the
claim a referee would open with.

---

### C-003 — `riemann_critical_line` axiom count stated as one; it is two
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 2 · **Status:** Open
**Affects:** `lean/README.md`, Phase 75 section and Conditional Proof Structure section

**The claim as published:** "`riemann_critical_line` appears in exactly **one**
theorem (`riemann_hypothesis`) across the full 8,059-job stack."

**Why it is wrong:** The Complete Axiom Footprint Table on the same page lists
`eigenvalue_zero_mapping` with footprint
`[propext, riemann_critical_line, Classical.choice, Quot.sound]`. The document's
own Conditional Proof Structure section then says "one named theorem
(`riemann_hypothesis`) and its downstream `eigenvalue_zero_mapping`," which is two.
`README.md` states it correctly as two.

**What is true instead:** `riemann_critical_line` appears in exactly two theorems:
`riemann_hypothesis` and `eigenvalue_zero_mapping`. Axiom localization remains the
strongest structural property of the stack; the count was simply stated wrong in
one of two places.

---

### C-004 — Retracted Q-2 / Q-4 results still published as CLOSED
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 4 · **Status:** Open
**Affects:** `README.md` Phase 75 row; `lean/README.md` Phase 75 section

**The claim as published:** "CAILculator Q-2 CLOSED: |M(σ)|² − |M(1−σ)|² = 0
exactly for all σ" and "Q-4 CLOSED: |M(½+it)| = |M(½−it)| exactly."

**Why it is wrong:** Phase 77 Run B refuted per-gateway bilateral magnitude
equality under the Documented F(s) Encoding across all six gateways at γ₁, γ₂, γ₃.
Phase 77 further recorded (AIEX-747) that the prior "proved" bilateral-equality
claim was a theorem misapplication — `pairing_sigma_independent` governs
cross-gateway differences at fixed input, not ±t pairs at one gateway — and
quarantined the Phase 75 magnitude tables via infeasibility certificate as a
v2.0.4 pipeline artifact. Standing order 7 requires exactly this quarantine. The
public README currently violates it.

Related: `README.md` describes Run B as having "established the precise structural
boundaries of bilateral symmetry," which reads as consolidation. It was a
refutation and should say so.

**What is true instead:** Bilateral magnitude equality does not hold per-gateway.
The time-reversal-symmetric quantity is the sedenion norm ‖F(+t)‖ = ‖F(−t)‖. The
bilateral difference is driven by c_g time-reversal asymmetry:
|M(+t)|² − |M(−t)|² = 16·a_g·b_g.

---

### C-005 — B/A → 4.0 hypothesis superseded by √17, not withdrawn
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 2 · **Status:** Open
**Affects:** `lean/README.md` Phase 74 section

**The claim as published:** "Q-8 DEVELOPING: B/A magnitude ratio local minima
tightening toward 4.0 (γ₁₂: 4.067 · γ₁₄: 4.057 · γ₁₆: 4.044)."

**Why it is wrong:** Phase 77 proved `ba_asymptote_sq` — B/A² → 17, so
B/A → √17 = 4.1231… — as a machine-verified limit theorem under standard axioms.
The 4.0 hypothesis is superseded.

**What is true instead:** √17 is the exact architectural constant. The observed
values were approaching it from below and were misread as approaching 4.0.
`README.md` carries this correctly; `lean/README.md` does not.

---

### C-006 — Explicit-formula weight table wrong for p = 5, 7, 11, 13
**Found:** 2026-09-08 · **By:** Claude (Opus 5), recomputation · **Severity:** 2 · **Status:** Open
**Affects:** `CLAUDE_CODE_HANDOFF_PHASE78_Q18.md` §11 Weighting Constants

**The claim as published:**

| p | published | true w_p = log p/√p | error |
|---|---|---|---|
| 2 | 0.4903 | 0.4901291 | +0.0002 |
| 3 | 0.6365 | 0.6342841 | +0.0022 |
| 5 | 0.7171 | 0.7197625 | −0.0027 |
| 7 | 0.7619 | 0.7354849 | +0.0264 |
| 11 | 0.7852 | 0.7229926 | +0.0622 |
| 13 | 0.7974 | 0.7113890 | +0.0860 |

**Why it is wrong:** The published sequence increases monotonically. The true
sequence peaks at p = 7 and decreases — log p/√p is maximized at p = e² ≈ 7.39.
The error is qualitative, not just numerical.

**Contamination check — negative.** The recorded live-validation vector and all
Phase 77/78 scripts compute w_p from the formula rather than the table. All six
nonzero slots of the γ₁ validation vector match w_p·cos(γ₁ ln p) to residual
0.00e+00, and the detector sum reproduces 5.222649912040212 as recorded. No result
is affected. The risk was to any future agent hardcoding the table.

---

### C-007 — Monte-Carlo p-value floor reported as significance
**Found:** 2026-09-08 · **By:** Claude (Opus 5), across all five result JSONs · **Severity:** 4 · **Status:** Open
**Affects:** `PHASE_78_Q18_BASELINE_CONFIRMED.md`; `RH_PHASE_78_RESULTS.md`; `RH_PHASE_77_RESULTS.md`; all result JSONs; planned RH paper

**The claim as published:** "z-score (T1) 8.42 | p < 2e-4" and "z = 8.42
significance (5-sigma equivalent)"; z = 13.83 reported at γ₃₄₀.

**Why it is wrong:** Across all five result JSONs, `p_two_sided` takes exactly three
distinct values: 0.0004 once (c_S2 at 31 zeros), 0.0576 once (Candidate 1 in-sample
ensemble), and 0.0 in every other case. That is the signature of a permutation null
of roughly 5,000 draws with a minimum resolvable p of about 2×10⁻⁴. The p-values
are censored at a floor, not measured.

Reporting z = 8.42 as "5-sigma equivalent" understates it as a z and overstates it
as a significance. Reporting z = 13.83 as a significance claims p ≈ 10⁻⁴³ from a
5,000-draw null.

**What is true instead:** z is a standardized effect size under a Monte-Carlo null,
and the achieved significance is p < 2×10⁻⁴ throughout. Both must be reported, with
the permutation count stated. Publishing z alone as a significance claim is not
defensible.

**Partly verified 2026-09-08.** `n_trials = 5000` confirmed directly from source in
`t1_value_at_zeros`, giving a minimum resolvable two-sided p of 2×10⁻⁴ — exactly the
0.0004 floor observed. The p-value censoring is established.

**Honest-baseline half — correction to this entry's own reasoning.** The published
"0.433 chance" is the ROC base rate n_pos/(n_pos+n_neg) at ε=0.5, verified exactly
as 19939/46001 = 0.43345. My original filing asserted that the 1.92× ratio divided
an ε=0.5 precision by an ε=1.0 baseline. **That was wrong** — 0.831/0.4334 = 1.92
uses matching radii, and the ratio is correct as published.

What is genuinely wrong is narrower and still needs fixing: the prose describing
0.433 as the chance rate at ε=1.0, and the baseline row quoting it against both
radii. True chance at ε=1.0 is 0.7607 at N=101, so the ε=1.0 precision of 0.974 is
1.28× above random, not the 2.25× that pairing it with 0.433 would suggest.
Chance also rises with height — 0.5572 at ε=0.5 by N=340 — so every honest baseline
must be stated at its own radius *and* its own zero count.

---

### C-008 — z = 8.42 quoted as a fixed constant
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 3 · **Status:** **Modified** — verified 2026-09-08
**Affects:** every document in the corpus; the RH paper's headline number

**The claim as published:** The Detector Encoding baseline is z = 8.42.

**Verified.** Both scripts hardcode `seed = 20260612` and `n_trials = 5000` inside
`t1_value_at_zeros`. A three-arm test was run:

| Arm | Configuration | Result |
|---|---|---|
| A | t ∈ [10,240], fixed seed, twice | bit-identical, z = 8.424967917247878 both times — reproduces the published number exactly |
| B | t ∈ [10,240], five seeds | z ∈ [8.3789, 8.5540], range 0.175 |
| C | t ∈ [10,600], same five seeds, same 101 zeros | z ∈ [8.3818, 8.4831], mean 8.4364, sd 0.0457 |

**What is true instead:** The core claim stands — z is not a fixed constant. Across
seeds it varies by roughly ±0.09, an order of magnitude larger than the second
decimal the corpus quotes. Any published z needs a stated seed and resample count,
or an error bar.

**What is retracted from this entry's original text:** the suggestion that the
Phase 78 doc's null-scope explanation was probably wrong, and the framing of scope
dependence as "the more serious finding." The scope difference is real at code
level — the two scripts do sample the null over different t-ranges — but Arm C's
spread sits inside Arm B's, so the effect is not separable from seed variation at
this N. The 8.425 → 8.483 gap is fully accounted for by ordinary variability with a
known mechanism, and does not indicate a bias in which sweeping more empty grid
inflates significance.

**Outstanding, low priority:** the five paired differences z_C(seedᵢ) − z_B(seedᵢ)
were not reported. With a fixed seed the published gap is deterministic, so pairing
would show whether the scope shift is systematic or a reshuffle. This is a
re-analysis of numbers already computed and would settle the residue.

---

### C-009 — Run C "controls" are the detector by identity
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 3 · **Status:** Open
**Affects:** `RH_PHASE_78_RESULTS.md` §4 finding 3; `phase78_q18_runC_results.json` field names `f6_control`, `f8_control`

**The claim as published:** "Zero architecture dilution at high zero density. The
gateway-realized detectors matched the pure explicit-formula controls to the same
decimal at every checkpoint — the instrument stays exact as the grid and zero count
grow, it does not degrade."

**Why it is wrong:** `f6_control` equals `base6` and `f8_control` equals `ext8` to
0.0 or 1.78×10⁻¹⁵ at every checkpoint, which is forced by the Gateway Linear Law
identity c_S2 + c_S6 = −2Σ_p w_p cos(t log p). The gateway reading and the
explicit-formula sum are the same function. The comparison could not have come out
any other way, so it carries no information about dilution. Dilution, if present,
would appear in the T1 statistic, not in the identity residual.

**What is true instead:** This is a valid identity verification across four sample
sizes and two truncation orders, and worth keeping as such. It is not a control and
the field names should change. The dilution question raised in the July 11 handoff
remains open and untested.

---

### C-010 — Candidate 2 ordering claim below measurement resolution
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 3 · **Status:** Open
**Affects:** `RH_PHASE_78_RESULTS.md` §3; `phase78_q18_candidate2_results.json` verdict field

**The claim as published:** "held-out z = 6.15 vs baseline 6.16 … hybrid marginally
*below* baseline"; verdict "NO IMPROVEMENT: held-out hybrid z (6.15) does not beat
baseline (6.16)."

**Why it is wrong:** The held-out gap is 0.0046 and the full-101 gap is 0.0045,
against run-to-run null variation of ±0.058 (see C-008). The ordering is a factor
of thirteen below the resolution of the measurement.

**What is true instead:** The hybrid and the baseline are statistically
indistinguishable. The negative result stands on stronger evidence anyway: λ\*
came out at −0.05 after a 121-point grid search, with train z of 6.0918 at λ\*
versus 6.0902 at λ = 0. The optimizer found nothing, which is the finding.

---

### C-011 — Candidate 3 evaluated on one metric, baseline on two
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 3 · **Status:** **Modified** — measured 2026-09-08, resolves in Candidate 3's favour
**Affects:** `RH_PHASE_78_RESULTS.md` §3.2 and Executive Summary; `PHASE_78_Q18_BASELINE_CONFIRMED.md` honest-baseline section

**The gap as filed:** `phase78_q18_candidate3_results.json` contained no `roc` and
no `peaks` keys, so the winning candidate was judged on T1 alone against a baseline
described with two metrics.

**Measured** (`results/phase78_q18_candidate3_roc_results.json`, reusing the
`roc_auc` / `local_maxima` / `peak_matching` code paths verbatim; base6 at N=101
reproduced AUC 0.8661 and precision 0.831, validating the method):

| | AUC δ=0.5 | Peak P @ ε=0.5 | Chance @ ε=0.5 | ratio |
|---|---|---|---|---|
| base6, N=101 | 0.8661 | 0.831 | 0.4334 | 1.92× |
| ext8, N=101 | **0.9059** | **0.901** | 0.4334 | 2.08× |
| base6, N=340 | 0.8342 | 0.817 | 0.5572 | 1.47× |
| ext8, N=340 | **0.8704** | **0.885** | 0.5572 | 1.59× |

**What is true instead:** the k=2 extension improves AUC by +0.040 at N=101 and
+0.036 at N=340. AUC is rank-based and therefore invariant under any monotone
amplitude scaling, so this cannot be an artifact of the eight-prime detector having
larger values. Candidate 3 is a genuine detection improvement, and this is stronger
evidence for it than the T1 result originally published.

**Withdrawn from this entry's original text:** the inference that a flat
ext8/base6 T1 ratio indicated an amplitude gain rather than better detection. AUC
refutes it. What survives is the narrower observation that the AUC gain is also
roughly flat across scale (+0.040, +0.036), so the extension is a uniform detection
improvement and does not extend the detector's reach as zero density rises. That
distinction matters for Phase 79 (see C-001).

**Corroborates C-001.** Both detectors degrade with height on every metric: AUC
0.8661 → 0.8342 and 0.9059 → 0.8704; precision-over-chance 1.92× → 1.47× and
2.08× → 1.59×. Independent confirmation, by a rank-based statistic, of the per-zero
signal decay that C-001 identified in the T1 values.

---

### C-012 — Phase 77 baseline artifact provenance broken
**Found:** 2026-09-08 · **By:** Paul Chavez · **Severity:** 3 · **Status:** **Modified — central claim refuted 2026-09-08**
**Affects:** `DATA_MANIFEST_CLAUDE_CODE.md` file-size figure

**The claim as filed:** All five result JSONs share a file origination date and
`phase77_q17_results.json` is 3,557 bytes against a manifest description of ~15 KB,
therefore the file is a regeneration rather than a preserved June 12 artifact, and
the Phase 78 pre-flight "reproduction" was circular.

**Refuted.** Git history plus SHA-256 verification shows
`phase77_q17_results.json` and `phase77_q17_live_validation.json` byte-identical
(after CRLF normalization) to commit **a96bc39**, dated **2026-06-12 14:42:22
-0700**; `phase77_q15_results.json` byte-identical to commit **312e541**, same date.
A search of all reachable drives found no other or older copies.

**What is true instead:** the provenance chain to June 12 is intact and verified.
The identical on-disk origination dates are explained innocently — a checkout
rewrites mtimes — and with `seed = 20260612` hardcoded (see C-008 Arm A, which
reproduced the published value bit-for-bit), a later re-run would be byte-identical
to the committed artifact anyway. The Phase 78 pre-flight was therefore a genuine
reproduction against a committed reference, not a comparison of a script to its own
output.

**What survives:** the manifest's "~15 KB" figure is wrong; the file is ~3.5 KB.
Severity of the surviving claim is 1, not 3.

**Retracted:** the circularity charge against `RH_PHASE_78_RESULTS.md` §1, and the
recommendation to restate AIEX-741/742's provenance. Both were unfounded.

---

### C-013 — Handoff slot assignment {4,7}: index 7 is in no gateway support
**Found:** 2026-08-22 · **By:** Claude Sonnet 5 (Claude Code), Phase 78 execution · **Severity:** 2 · **Status:** **Corrected**
**Affects:** `CLAUDE_CODE_HANDOFF_PHASE78_Q18.md` §3 Candidate 3 design

**The claim as published:** Add p = 17 and p = 19 "to u₂ (slots 4, 7)."

**Why it was wrong:** Index 7 is in the support of none of the six Canonical Six
gateways; a signal placed there is invisible to every reading. Index 4 is live but
belongs to S3's support {4, 11, 6, 9}, not to u₂.

**What is true instead:** p = 17 goes in slot 4 and p = 19 in slot 11, both in S3's
support, giving detector_extended = c_S2 + c_S3. Identity confirmed to residual
8.88×10⁻¹⁶ (p=17) and 1.78×10⁻¹⁵ (p=17 + p=19).

**Corrected:** 2026-08-22, in `RH_PHASE_78_RESULTS.md` §3.1, before any result was
computed from the faulty assignment.

**Follow-on worth recording:** because S3 ≡ S6 exactly under the k=1 Detector
Encoding (`max|c_S3 − c_S6| = 0.0`, slots {4,11} zeroed), the k=1 detector
c_S2 + c_S6 and the k=2 detector c_S2 + c_S3 are the same channel pair. The
extension is not a different detector with more primes added — it is the same
detector with the S3/S6 degeneracy broken. This unifies two separately-reported
Phase 78 observations into one structural result.

---

### C-014 — `(z_g/Σz)²` weighting formula discards sign and does not normalize
**Found:** 2026-08-22 · **By:** Claude Sonnet 5 (Claude Code) · **Severity:** 2 · **Status:** Open — doc fix outstanding
**Affects:** `CLAUDE_CODE_HANDOFF_PHASE78_Q18.md` §3 Candidate 1, Step 3

**The claim as published:** weight each gateway by `(z_g/Σz)²`.

**Why it is wrong:** Gateways S1, S4, S5 have negative z under the Detector
Encoding (−2.320, −2.374, −2.308) — they are anti-correlated with zero locations.
Squaring discards the sign and gives them positive weight, summing them in with the
wrong orientation. The resulting weights also sum to 1.1008 rather than 1.

Claude Code applied the formula literally, flagged the lookahead bias, and reported
the failure honestly. The defect is in the handoff document, not the execution.

**What is true instead:** Candidate 1's failure is partly a real negative result
(ensembling across the existing gateways does not help) and partly an artifact of a
broken weighting rule. The two should be separated before the negative result is
cited. The handoff document must be corrected before it is reused.

---

### C-015 — Repository tree omits four `.lean` files, including axiom-bearing ones
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 1 · **Status:** Open
**Affects:** `README.md` Repository Structure; `README.md` Gateway Linear Law section

**The claim as published:** The Repository Structure tree lists 13 `.lean` files
plus one companion. The Formal Proof Stack table lists 17.

**Why it is wrong:** Missing from the tree: `PrimeEmbedding.lean`,
`ZetaIdentification.lean`, `RiemannHypothesisProof.lean`, `EulerProductBridge.lean`
— precisely the four carrying the RH axiom and the zeta bridge. A reader working
from the tree concludes the axiom-bearing files do not exist.

Also in the same document: "Three theorems in `GatewayLinearLaw.lean` follow:" is
immediately followed by four bullets. The prose count was not updated when
`ba_asymptote_sq` was added in Phase 77.

---

### C-016 — `CD4_mul` defined as the zero function; all Chavez Transform theorems vacuous
**Found:** 2026-04 (on or before Apr 16) · **By:** Paul Chavez / Claude Code · **Severity:** 4 · **Status:** **Corrected**
**Affects:** `ChavezTransform_Specification_aristotle.lean` (Aristotle UUID 0bfec79d, January 2026)

**The claim as published:** The January 2026 Aristotle file formalized the Chavez
Transform with sedenion multiplication and proved its theorems.

**Why it was wrong:** `CD4_mul` was defined as the zero function. With the product
identically zero, every theorem depending on it was trivially satisfied. The
formalization proved nothing about the Chavez Transform.

**What is true instead:** The file was superseded on April 16, 2026 by
`ChavezTransform_genuine.lean`, which uses `instMulSed` — the genuine 16×16
Cayley-Dickson table — with e₀ proved as a two-sided identity from the table via
`decide` on universally-quantified propositions (§2–§3).

**Corrected:** 2026-04-16. The supersession is recorded in the replacement file's
own header (lines 7–8), which names the superseded UUID and states the reason.
That is the correct handling and is the model this register generalizes.

**Related:** see C-017. The replacement file carries a vacuous theorem of its own,
of a different kind.

---

### C-017 — `chavez_transform_convergence` is vacuous in the replacement file
**Found:** 2026-09-08 · **By:** Claude (Opus 5), reading `ChavezTransform_genuine.lean` · **Severity:** 4 · **Status:** Open
**Affects:** `ChavezTransform_genuine.lean` §10 and header Key Results; `README.md` Overview ("convergence and stability theorems"); `CHAVEZ_TRANSFORM_GEMINI_HANDOFF.md` §File Architecture

**The claim as published:** "**Theorem 1: Convergence.** The Chavez Transform of
any bounded integrable function is finite."

```lean
theorem chavez_transform_convergence
    (f : ℝ → ℝ) (P Q : Sed) (α d a b : ℝ)
    (h_bounded    : ∃ M, ∀ x ∈ Set.Ioc a b, |f x| ≤ M)
    (h_integrable : IntervalIntegrable f MeasureTheory.volume a b)
    (h_alpha      : 0 < α)
    (h_d          : 0 < d) :
    ∃ C : ℝ, |chavez_transform_1d f P Q α d a b| ≤ C :=
  ⟨_, le_refl _⟩
```

**Why it is wrong:** `∃ C : ℝ, |X| ≤ C` holds for every real X — instantiate C
with |X|. The proof term `⟨_, le_refl _⟩` does exactly that and closes by
reflexivity. None of the four hypotheses are used; the theorem is provable with all
of them deleted, for unbounded f, non-integrable f, α ≤ 0 and d ≤ 0.

It cannot be repaired in this form. `chavez_transform_1d` is a Bochner integral,
and Mathlib's `∫` evaluates to 0 for non-integrable integrands, so the expression
is a real number unconditionally and convergence is not expressible as a bound on
it.

The defect was visible before the file shipped: the April 16 handoff's File
Architecture section lists "§10 Main theorems — chavez_transform_convergence
(trivial ⟨_, le_refl _⟩)". It was recorded as a description rather than treated as
a blocker.

**What is true instead:** No convergence theorem has been proved. To state one,
the target must be `IntegrableOn (fun x => f x * K P Q (realToSed x) α d)
(Set.Ioc a b) volume` — integrability of the integrand — which is where the
boundedness and decay hypotheses would actually do work. Until that exists,
`chavez_transform_convergence` should be deleted or renamed to something that does
not assert convergence, and every document claiming a proved convergence theorem
must be corrected.

**Not affected:** `chavez_transform_stability` is a genuine theorem with real
content (see Verified Sound). This entry concerns Theorem 1 only.

**Attribution note, recorded to prevent a wrong lesson:** the trivial proof term is
present in the Claude Code handoff document written *before* the Gemini CLI relay,
so it originated in the proof architecture, not in the build completion. The
subsequent standing order restricting Gemini from Lean work rests on Mathlib
lemma-name drift and is not evidenced by this entry.

---

### C-018 — Chavez Transform verification scope overstated
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 4 · **Status:** Open
**Affects:** `README.md` Overview; `lean/README.md` §Chavez Transform; `ChavezTransform_genuine.lean` header Key Results; Canonical Six companion paper claims

**The claim as published:** "**Chavez Transform** — Applies zero divisor structure
from Cayley-Dickson algebras (sedenions, 16D and above) to analyze numerical
sequences across hypercomplex dimensions. Formally verified in Lean 4 with
convergence and stability theorems proved under standard axioms."

**Why it is wrong:** What is formalized is `chavez_transform_1d`, whose integration
variable enters only through `realToSed x = x • sedBasis 0` — the e₀ scalar
channel. Because e₀ is the multiplicative identity (proved in §3), P * (x·e₀) = x·P
for every P, so on this subspace sedenion multiplication reduces to scalar
multiplication and the kernel collapses exactly:

    K_Z P Q (realToSed x) = 2·x²·(‖P‖² + ‖Q‖²)          (§6, exact)

The zero-divisor structure — the entire subject of the transform — is invisible on
the embedded line. The file header states this as a feature: "Both theorems
unconditional on P*Q=0 (zero divisor property not required)." It is better read as
a diagnostic: the 1D embedding is precisely the subspace where the non-associative
structure does nothing.

The header's further claim that this is "pattern invariance formally proved as
theorem" does not follow. The formula is pattern-independent because the
multiplication degenerated, not because distinct Canonical Six patterns were shown
equivalent.

**What is true instead:** `chavez_transform_stability` is a correct and non-trivial
bound on a scalar-channel restriction of the transform, with a sharp constant
2(‖P‖²+‖Q‖²)/(αe) derived from the exact maximum of x²e^(−αx²). That is a real
result and should be stated as what it is. The claim that the Chavez Transform —
the object in the papers, defined over a domain D in Sed — has been formally
verified is not supported by this file.

**Follow-on:** a genuine formalization requires the integral over a sedenion domain
where P·x and x·P differ, which needs `sed_norm_mul_le` or an equivalent bound.
The April 16 design note records that `realToSed` was chosen specifically to avoid
needing it. That trade should be documented as a scope limitation rather than
presented as an architectural advantage.

---

### C-019 — `eigenvalue_zero_mapping` axiom footprint omits `sorryAx`
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 4 · **Status:** Open — **confirmed verbatim 2026-09-08**
**Affects:** `lean/README.md` Complete Axiom Footprint Table; `README.md` Build Status and Formal Proof Stack table

**The claim as published:** Both READMEs give `eigenvalue_zero_mapping` the
footprint `[propext, riemann_critical_line, Classical.choice, Quot.sound]`.

**Confirmed.** `lake env lean axiom_check_c019.lean`, against a clean build of
8,061 jobs matching the `CLAUDE.md` baseline, returns verbatim:

```
'eigenvalue_zero_mapping' depends on axioms: [propext, riemann_critical_line, sorryAx, Classical.choice, Quot.sound]
'zeta_zero_implies_spectral' depends on axioms: [propext, riemann_critical_line, Classical.choice, Quot.sound]
'spectral_implies_zeta_zero' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
'spectral_implies_critical_line' depends on axioms: [propext, Classical.choice, Quot.sound]
```

**What is true instead:** `eigenvalue_zero_mapping` carries `sorryAx` and is not a
proved biconditional. The published footprint is that of
`zeta_zero_implies_spectral`, the forward direction, recorded against the
biconditional. Every footprint table and milestone claim citing the biconditional
requires correction, and the "1 intentional sorry" framing must name which
downstream theorems inherit it — `eigenvalue_zero_mapping` at minimum.

**Note:** `riemann_critical_line` localization is *narrower* than published, not
wider — it does not appear in `spectral_implies_zeta_zero` at all. The axiom
discipline holds; the sorry propagation is what went unrecorded.

---

### C-020 — Decorative hypothesis in `Fbase_nondegeneracy`; stale Path B docstring
**Found:** 2026-09-08 · **By:** Claude (Opus 5), applying standing check item 1 · **Severity:** 2 · **Status:** Open — **confirmed 2026-09-08**
**Affects:** `SpectralIdentification.lean` §Fbase Non-Degeneracy

**Confirmed by two independent mechanisms.**

1. **Deletion test.** `Fbase_nondegeneracy` with `hs : 0 < s.re ∧ s.re < 1` removed
   from the signature compiles clean, exit 0. The hypothesis is decorative; the
   result is pure sedenion algebra and holds for any s.
2. **The Lean linter.** The full build emits
   `SpectralIdentification.lean:66:35: unused variable 'hs'`. Lean has been
   reporting this on every build since Phase 73.

Docstring staleness also confirmed: grep finds exactly one `sorry` in the file, at
line 139, unrelated to hwitness. Lines 99–101 claiming Path B "relies on the
hwitness sorry" are stale against line 28, which records it CLOSED.

**Narrowed from this entry's original text.** The `GatewayLinearLaw.lean` audit
came back **negative, which is the good outcome**: `gateway_pairing_iff`,
`gateway_magSq_sub` and `pairing_sigma_independent` take no Prop hypotheses at all,
and `ba_asymptote_sq` with `hK` deleted **fails to compile** — positivity cannot
discharge t² + K ≠ 0 without it. `hK` is load-bearing.

**Consequence for the RH paper:** the four theorems that `detector_channel_identity`
and `extended_detector_channel_identity` would sit on carry no decorative
hypotheses. That infrastructure is sound.

---

### C-021 — Critical-line "characterizations" are definitionally engineered
**Found:** 2026-09-08 · **By:** Claude (Opus 5) · **Severity:** 3 · **Status:** Open
**Affects:** `README.md` Principal Result and Overview; `lean/README.md` Core Proof Architecture; v1.4 framing; RH paper introduction

**The claim as published:** The stack establishes characterizations of the critical
line via distinct algebraic mechanisms, and Phase 73 achieves a "spectral
identification" linking ζ zeros to spectral theory.

**Why the scope is overstated:** The Sedenionic Hamiltonian is *defined* as
H(s) = (Re(s) − ½)·u_antisym. That it vanishes exactly when Re(s) = ½ is
`smul_eq_zero` together with u_antisym ≠ 0 — the theorem restates the definition.
The construction was built to vanish on the critical line, so its vanishing there
is not evidence about the critical line.

The identification with ζ then runs (line 107):

```lean
theorem zeta_zero_implies_spectral (s : ℂ) (hs : ...) (hζ : riemannZeta s = 0) :
    isSpectralPoint s :=
  (Hamiltonian_vanishing_iff_critical_line s).mpr (riemann_critical_line s hζ hs)
```

`riemann_critical_line` is RH itself, taken as axiom. So the chain is: assume every
ζ zero has Re(s) = ½; conclude that an object constructed to vanish at Re(s) = ½
vanishes at ζ zeros. Logically valid, correctly labeled conditional in the repo,
and empty as evidence about where ζ's zeros lie.

**What is true instead:** The stack is a formalized framework in which the critical
line admits several equivalent algebraic descriptions, machine-verified and
axiom-localized. Route 3 (gateway integrality) is the strongest of them, being
genuinely RH-independent. None of the routes constrains the location of ζ's zeros,
and none is offered as doing so — but the phrase "characterizations of the critical
line," repeated across the READMEs, invites a reader to think otherwise.

**Recommended:** state the conditional structure in the same sentence as the
result, everywhere the result appears, rather than in a separate section further
down.

---

## Recurring Failure Mode: Vacuity

Four entries in this register — C-002, C-016, C-017, C-021 — are the same class of
defect: **a theorem that is true for reasons unrelated to the mathematics it claims
to establish.** They arrived by four different routes, and C-002 was confirmed
against source on 2026-09-08.

| Entry | Route to vacuity |
|---|---|
| C-016 | A *definition* was degenerate (`CD4_mul = 0`), so every downstream theorem held trivially |
| C-017 | A *statement* was degenerate (`∃ C, \|X\| ≤ C`), so no hypothesis did any work |
| C-002 | A *definition unfolds* to one already proved, so a conjunct restates its neighbour |
| C-021 | A *construction is engineered* to have the property the theorem then verifies |

`#print axioms` catches none of these. It detects `sorryAx` and non-standard
axioms; a vacuous theorem is fully proved from standard axioms and reports a clean
footprint. **The stack's headline verification metric is structurally blind to its
most common failure mode.** Every clean-footprint claim in the corpus should be
read with that in mind.

### Proposed standing check

Before any theorem is cited in a paper, README, or KSJ capture, it must pass:

1. **Hypothesis-use audit.** Delete each hypothesis in turn and re-elaborate. If the
   proof still compiles, that hypothesis is decorative — either the statement is too
   weak or the hypothesis is unnecessary. Both need explaining.
2. **Degenerate-instance test.** Ask whether the statement holds when the central
   definitions are replaced by trivial ones (product ≡ 0, function ≡ constant,
   predicate ≡ True). If yes, the theorem is not about its subject.
3. **Definitional-collapse check.** For any conjunction or multi-route claim,
   confirm no conjunct reduces to another by `unfold`, `simp`, or `rfl`.
4. **Scope statement.** Record the domain the theorem actually quantifies over, not
   the domain the informal object lives on (see C-018).

Adopting this is the substantive response to C-016 through C-018. Correcting the
three entries without it leaves the generating mechanism in place.

---

## Second Failure Mode: Unread Signal

C-020 was reported by the Lean linter on every build since Phase 73:
`SpectralIdentification.lean:66:35: unused variable 'hs'`. It was in the build
output for five phases and went unread.

This is a different defect from the vacuity pattern above. Vacuity is invisible to
the tooling — `#print axioms` cannot see it. This was fully visible and simply not
looked at. The two need different remedies, and the second one is cheaper.

A plausible contributing cause is already documented in the project's tooling
notes: PowerShell `tee` writes build logs as UTF-16 LE, which corrupts warning line
numbers. A warning stream that renders as garbage is a warning stream nobody reads.
The same class of problem cost this verification batch several hours — `wmic` piped
through git-bash returned corrupted digit strings, reporting 5.14 GiB free as
46–60 GB and a 115 GB volume as 11.5 TB, until `Get-Volume` gave a clean reading.

**Added to the standing check:** treat linter warnings as part of the audit, not as
noise. Capture build logs with `Out-File -Encoding utf8`, never `tee`. Prefer
PowerShell-native cmdlets over `wmic` for any number a decision depends on. Standing
check item 1 asks you to delete a hypothesis and re-elaborate; often Lean has
already told you the answer.

---

## Verified Sound

Recorded so the register reflects the state of the work rather than only its
defects. Each item below was checked in the course of opening this document and
held up.

- **Detector Encoding identity.** All six nonzero slots of the recorded γ₁
  validation vector match w_p·cos(γ₁ ln p) to residual 0.00e+00; the detector sum
  reproduces 5.222649912040212. The mislabeled inline comments in
  `CLAUDE_CODE_HANDOFF_PHASE78_Q18.md` §0 do not affect the vector itself, though
  they should be fixed (see C-006 rationale).
- **k=2 extension identity.** Residuals 8.88×10⁻¹⁶ (7 primes) and 1.78×10⁻¹⁵
  (8 primes), holding across all four Run C checkpoints.
- **S3 ≡ S6 under the k=1 encoding.** `max|c_S3 − c_S6| = 0.0`, derived
  analytically before being confirmed numerically. This is a genuine structural
  result and the mechanism behind C-013's follow-on.
- **Held-out discipline.** Introduced mid-session in Phase 78 in direct response to
  Candidate 1's in-sample inflation, and applied to Candidates 2 and 3 thereafter.
  The in-sample/held-out gap (−1.89 vs −7.26) is itself a useful record of how
  badly in-sample fitting overstates these ensembles.
- **Class B structure.** c_S1 slope vs t measured at −2.0001 against a predicted
  −2t; c_S1 − c_S4 = −4·w₁₃·cos(t·ln 13) confirmed to residual 5.68×10⁻¹⁴.
- **`chavez_transform_stability`.** Genuine theorem, real content, all hypotheses
  load-bearing. The chain — `norm_integral_le_integral_norm`, then
  `integral_mono_of_nonneg` against the pointwise `K_bound` — is sound, and the
  constant is sharp: `sq_mul_exp_neg` derives x²e^(−αx²) ≤ 1/(αe) from
  `Real.add_one_le_exp`, which is the exact maximum at x² = 1/α. Subject to the
  scope limitation in C-018.
- **e₀ two-sided identity (§3).** `sed_mul_sedBasis0` and `sedBasis0_mul_sed`
  proved from the actual `sedMulTarget`/`sedMulSign` table, not assumed. This is
  the substantive repair C-016 called for and it was done properly.
- **Supersession hygiene.** `ChavezTransform_genuine.lean` names the file it
  replaces and the reason, in its own header. Two of the newer errors in this
  register (C-004, C-005) exist because that practice was not followed elsewhere.
- **`GatewayLinearLaw.lean` hypothesis audit — clean.** Three of the four theorems
  take no Prop hypotheses; `ba_asymptote_sq` fails to compile without `hK`. No
  decorative hypotheses in the infrastructure the RH paper's Lean targets depend on.
- **Build baseline reproduced.** 8,061 jobs, matching `CLAUDE.md`, from a cold
  Mathlib cache on 2026-09-08. The environment that produced the June figures had
  been lost from the machine; it is re-established.
- **Provenance chain to June 12.** Verified by SHA-256 against commits a96bc39 and
  312e541 (see C-012).
- **Detector reproducibility.** `seed = 20260612`, `n_trials = 5000`; the published
  z = 8.424967917247878 reproduces bit-for-bit.

---

## Log

| Date | Change |
|---|---|
| 2026-09-08 | Register opened. C-001 through C-015 entered; C-013 entered as already corrected. C-016 reserved pending specification. |
| 2026-09-08 | C-016 specified from `CHAVEZ_TRANSFORM_GEMINI_HANDOFF.md` and closed as Corrected. C-017 and C-018 opened from review of `ChavezTransform_genuine.lean`. Recurring Failure Mode section added. |
| 2026-09-08 | C-002 confirmed against `SpectralIdentification.lean` line 47. C-019, C-020, C-021 opened from the same file. C-020 was produced by applying standing check item 1. |
| 2026-09-08 | **First verification batch (six tasks, Claude Code).** C-019 confirmed verbatim; C-020 confirmed by deletion test and independently by the Lean linter; C-008, C-011, C-012 modified. **The batch corrected this register three times: C-012's central claim was refuted outright, C-011 resolved in the investigation's favour, and C-008's causal explanation was retracted. A fourth correction was internal — C-007's assertion about the 1.92× ratio was wrong on its own arithmetic.** Second Failure Mode section added. |

---

*Chavez AI Labs LLC — Applied Pathological Mathematics*
*Corrections are the method, not the exception.*
