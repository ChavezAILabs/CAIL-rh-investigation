# CAIL-RH Investigation — Corrections Propagation & Publication: Claude Code Handoff

**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Date:** September 8, 2026
**From:** Claude Opus 5 (Claude.ai session)
**To:** Claude Code (in-shell)
**Branch:** `phase-78-q18` (commit 4af1fa7 is the current head)
**Ends in:** one comprehensive commit and a **push** — see Task 9

**This document is public.** It is published alongside `CORRECTIONS.md`.

---

## Context

The September 8 verification batch resolved six tasks against a live Lean build
(8,061 jobs, matching `CLAUDE.md`). Results are recorded in `CORRECTIONS.md`, which
now holds 21 entries: 2 corrected, 3 confirmed against source, 3 modified by
verification, 13 open.

The register is in the repo. The documents it describes are not yet corrected. This
session closes that gap so the repository is internally consistent at the moment it
becomes public.

**Division of labour.** This handoff covers **factual corrections only** — claims
that are wrong about what happened or what a number is. Four entries (C-002, C-017,
C-018, C-021) concern what the work *establishes* rather than what it *did*; those
are Paul's decision and are handled in Task 8 with inline markers, not rewrites.
Do not reframe them.

---

## Verified Reference Numbers

Use these. Do not recompute, do not round differently, do not soften.

**Detector metrics** (`results/phase78_q18_candidate3_roc_results.json`):

| | AUC δ=0.5 | Peak P @ ε=0.5 | Chance @ ε=0.5 | ratio |
|---|---|---|---|---|
| base6, N=101 | 0.8661 | 0.831 | 0.4334 | 1.92× |
| ext8, N=101 | 0.9059 | 0.901 | 0.4334 | 2.08× |
| base6, N=340 | 0.8342 | 0.817 | 0.5572 | 1.47× |
| ext8, N=340 | 0.8704 | 0.885 | 0.5572 | 1.59× |

Chance @ ε=1.0: **0.7607** at N=101, **0.8765** at N=340.
Chance is the ROC base rate n_pos/(n_pos+n_neg) at that radius — 19939/46001 =
0.43345 at ε=0.5, N=101. It is radius-dependent *and* zero-count-dependent.

**Run C T1 values** (the C-001 correction rests on these):

| N | γ_N | observed T1 | null_std | null_std·√(N/101) | z |
|---|---|---|---|---|---|
| 101 | 237.77 | 1.9662 | 0.2309 | 0.2309 | 8.483 |
| 150 | 318.85 | 1.7806 | 0.1919 | 0.2339 | 9.268 |
| 200 | 396.38 | 1.6838 | 0.1669 | 0.2348 | 10.070 |
| 340 | 598.49 | 1.5041 | 0.1265 | 0.2321 | 11.871 |

**Null:** `seed = 20260612`, `n_trials = 5000`, minimum resolvable two-sided
p = 2×10⁻⁴. Across seeds z varies by ≈ ±0.09.

**Axiom check** (verbatim, do not paraphrase when quoting):

```
'eigenvalue_zero_mapping' depends on axioms: [propext, riemann_critical_line, sorryAx, Classical.choice, Quot.sound]
'zeta_zero_implies_spectral' depends on axioms: [propext, riemann_critical_line, Classical.choice, Quot.sound]
'spectral_implies_zeta_zero' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
'spectral_implies_critical_line' depends on axioms: [propext, Classical.choice, Quot.sound]
```

**Weights** — compute from `w_p = log(p)/sqrt(p)`, never tabulate:
w₂ 0.4901291 · w₃ 0.6342841 · w₅ 0.7197625 · w₇ 0.7354849 · w₁₁ 0.7229926 ·
w₁₃ 0.7113890. The sequence peaks at p=7; any monotone-increasing table is wrong.

---

## Task 1 — Stage the loose verification artifacts

1. `results/phase78_q18_candidate3_roc_results.json` is untracked and is now the
   evidence behind C-011. Track it.
2. Move the two scratch files out of the build directory into
   `verification/2026-09-08/`:
   - `axiom_check_c019.lean`
   - `audit_c020_*.lean`
   Add a short `verification/2026-09-08/README.md` stating what each file checks,
   the command that runs it, and the verbatim output obtained. These are the
   reproducibility record for C-019 and C-020.

Do not leave verification artifacts in `AsymptoticRigidity_aristotle/` — that
directory gets rebuilt.

---

## Task 2 — `lean/README.md`

This file is two phases stale (pinned at Phase 75, May 11) and carries three
confirmed errors.

1. **C-003.** It states twice that `riemann_critical_line` appears in "exactly
   **one** theorem (`riemann_hypothesis`)". Its own Complete Axiom Footprint Table
   lists `eigenvalue_zero_mapping` carrying it too. Correct to **two**, consistently.
2. **C-019.** Add `sorryAx` to `eigenvalue_zero_mapping`'s row in the footprint
   table, and add a line stating which theorems inherit the sorry from
   `spectral_implies_zeta_zero`. Use the verbatim block above.
3. **C-005.** The Phase 74 section still reads "Q-8 DEVELOPING: B/A ratio local
   minima tightening toward 4.0". Phase 77 proved `ba_asymptote_sq`: B/A² → 17, so
   B/A → √17 = 4.1231…. Mark the 4.0 hypothesis **superseded** — strike it through
   and cross-reference C-005 rather than deleting it.
4. **C-004.** The Phase 75 section carries "Q-2 CLOSED" and "Q-4 CLOSED". Both were
   refuted by Phase 77 Run B and the Phase 75 magnitude tables were quarantined per
   standing order 7. Strike through, mark retracted, cross-reference C-004.
5. **Staleness.** Header still says CAILculator v2.0.4 — the version whose pipeline
   Phase 77 quarantined. Update to v2.1.4. Add `GatewayLinearLaw.lean` to the File
   Directory; it is currently absent entirely.

**Do not** rewrite the Phase 75 "three characterizations" claim — that is C-002 and
belongs to Task 8.

---

## Task 3 — `README.md`

1. **C-004.** The Phase 75 row still reads "Q-2 CLOSED (bilateral magnitude
   symmetry identically zero). Q-4 CLOSED (±t symmetry structural)." Strike and mark
   retracted. Separately, the Phase 77 paragraph describes Run B as having
   "established the precise structural boundaries of bilateral symmetry" — it was a
   refutation; say so.
2. **C-019.** Correct `eigenvalue_zero_mapping`'s footprint wherever it appears, and
   revise the "1 intentional sorry" framing to name which theorems inherit it.
   Note in the same place that `riemann_critical_line` localization is *narrower*
   than published — it does not appear in `spectral_implies_zeta_zero` at all.
3. **C-015.** The Repository Structure tree lists 13 `.lean` files; the Formal Proof
   Stack table lists 17. Add the four missing: `PrimeEmbedding.lean`,
   `ZetaIdentification.lean`, `RiemannHypothesisProof.lean`, `EulerProductBridge.lean`.
4. **C-015 (second).** "Three theorems in `GatewayLinearLaw.lean` follow:" is
   followed by four bullets. Fix the count.
5. **Link the register.** Add a prominent link to `CORRECTIONS.md` near the top —
   above the fold, not in a footer.

---

## Task 4 — `CLAUDE_CODE_HANDOFF_PHASE78_Q18.md`

This document is still reachable and still wrong. It has already caused one
near-miss.

1. **C-006.** Replace the §11 Weighting Constants table. The published values for
   p = 5, 7, 11, 13 are wrong and the sequence shape is wrong. Better: delete the
   table and state the formula, with a note that any hardcoded table is a defect.
2. **C-014.** Remove or clearly mark the `(z_g/Σz)²` weighting formula. It discards
   sign — three Class B gateways have z ≈ −2.3 and receive positive weight — and the
   weights sum to 1.1008 rather than 1.
3. **Slot comments.** The §0 live-validation vector has correct values with
   mislabeled inline comments from index 6 onward. Slots 3, 5, 6, 9, 10, 12 carry
   p = 2, 3, 5, 7, 11, 13 respectively. Fix the labels.
4. **Index 7.** Correct the "unused u₂ slots {4,7}" instruction. Index 7 is in the
   support of no gateway; index 4 belongs to S3. Cross-reference C-013.

Add a header banner: superseded for the Q-18 work, retained for the record, see
`CORRECTIONS.md`.

---

## Task 5 — `RH_PHASE_77_RESULTS.md`

**C-001 originates here.** §2A describes the c_S2 result as sub-√N growth
indicating genuine strengthening. The same structure as Phase 78: observed 1.8464
at 31 zeros → 1.3735 at 101 (74% of value), null_std 0.5075 → 0.2783 (ratio 0.548
against √(31/101) = 0.554).

Correct the interpretation: per-zero signal decays; the z increase comes from the
null tightening as 1/√N. Cross-reference C-001. Leave the numbers alone — they are
correct — and change only what they are said to mean.

---

## Task 6 — `RH_PHASE_78_RESULTS.md`: write v2

Four of this document's claims are wrong and they include its headline. Patching in
place will produce something incoherent. **Write `RH_PHASE_78_RESULTS_v2.md`** and
keep v1 in place with a superseded banner pointing to v2 and to `CORRECTIONS.md`.

What changes:

1. **C-001 — Run C finding 1 is inverted.** "Both detectors keep growing in z…
   genuine strengthening, not pure statistical scaling" is backwards. Use the T1
   table above. State: per-zero detector strength decays with height (76.5% of its
   N=101 value by γ₃₄₀); z rises only because the null tightens as 1/√N. Offer the
   commensurability mechanism as **conjecture, explicitly labelled**: six-prime
   finest oscillation 2π/log 13 ≈ 2.45 against mean zero gap 2π/log(t/2π) falling
   from ≈1.73 to ≈1.38.
2. **C-009 — Run C finding 3 is vacuous.** `f6_control` ≡ `base6` and
   `f8_control` ≡ `ext8` to 0.0 or 1.78×10⁻¹⁵, forced by the Gateway Linear Law
   identity. It could not have come out otherwise, so it says nothing about
   dilution. Relabel as an identity verification across four sample sizes and two
   truncation orders — which is genuinely valuable — and state that the dilution
   question remains untested.
3. **C-010 — Candidate 2's ordering claim.** Drop "hybrid marginally below
   baseline"; the 0.0046 gap is far under the ±0.09 seed variation. The real
   evidence is λ\* = −0.05 after a 121-point grid search, train z 6.0918 at λ\*
   versus 6.0902 at λ=0. The optimizer found nothing. That is the finding.
4. **C-011 — Candidate 3 gets better evidence.** Add the full ROC/peak table above.
   The k=2 AUC gain (+0.040 at N=101, +0.036 at N=340) is rank-based and therefore
   cannot be an amplitude artifact. State also that the gain is roughly flat across
   scale, so the extension is a uniform detection improvement and does **not**
   extend reach as zero density rises — this matters for Phase 79.
5. **C-007 — significance reporting.** Every z gets its seed and `n_trials = 5000`
   stated, with achieved significance p < 2×10⁻⁴. Do not report z as a significance
   level. Honest baselines must be quoted at their own radius and their own zero
   count.
6. **C-012 — pre-flight.** The provenance claim is now *stronger*, not weaker:
   byte-identity with commit a96bc39 (2026-06-12) verified by SHA-256. Say so.
7. **§2.1 and §3.1 unify.** S3 ≡ S6 under the k=1 encoding, so the k=1 detector
   c_S2+c_S6 and the k=2 detector c_S2+c_S3 are the same channel pair. The extension
   breaks the degeneracy rather than adding a different detector. Present as one
   structural result.

Keep everything v1 got right: the slot-7 catch, the sign diagnosis, the held-out
discipline, and the plain statements that the Lean track was not started and nothing
was committed.

---

## Task 7 — `DATA_MANIFEST_CLAUDE_CODE.md`

Small. `phase77_q17_results.json` is ~3.5 KB, not ~15 KB (C-012). Also reconcile
`riemann_zeros.json` versus `rh_zeros.json` — the document uses both names for the
same file.

---

## Task 8 — Inline markers for the four reframing entries

C-002, C-017, C-018 and C-021 concern what the work claims to establish. **Do not
rewrite these claims.** Instead, insert a short marker adjacent to each affected
statement:

> ⚠ **Correction pending** — see `CORRECTIONS.md` C-0NN.

Locations:

| Entry | Where |
|---|---|
| C-002 | `README.md` Principal Result; `lean/README.md` Phase 75 — the "three independent characterizations" claim |
| C-017 | `ChavezTransform_genuine.lean` header Key Results and the `chavez_transform_convergence` docstring; `README.md` "convergence and stability theorems" |
| C-018 | `README.md` Chavez Transform overview; `lean/README.md` Chavez Transform section |
| C-021 | `README.md` Principal Result and Overview |

This keeps the repository honest without pre-empting Paul's decisions on framing.

---

## Task 9 — One comprehensive commit and push

**Paul has explicitly authorized this push**, exercising standing order 4 for this
commit. This is the only push authorized by this document.

Before committing:

- [ ] `lake build` still succeeds — 8,061 jobs, 0 errors, 1 sorry
- [ ] No `.lean` file in the main stack modified (Task 3's audit used scratch copies)
- [ ] `CORRECTIONS.md` is at repo root and tracked
- [ ] Every cross-reference in the corrected docs points to an entry that exists
- [ ] `git status` reviewed and reported before the commit runs

```bash
git add -A
git status                     # report this output before committing
git commit -m "Phase 78: corrections propagation, verification batch results, ROC metrics

Propagates CORRECTIONS.md entries C-001, C-003, C-004, C-005, C-006, C-007,
C-009, C-010, C-011, C-012, C-014, C-015, C-019, C-020 into the affected
documents. Adds verification artifacts for the Sept 8 batch. RH_PHASE_78_RESULTS
superseded by v2. C-002, C-017, C-018, C-021 marked pending, not reframed."
git push -u origin phase-78-q18
```

Report the commit hash and the push result. **Push the branch only — do not merge
to `main`.**

---

## Out of Scope

- Reframing C-002, C-017, C-018, C-021. Markers only.
- Merging to `main`.
- Any Lean stack growth — `detector_channel_identity` remains Paul's call.
- Phase 79 feasibility work.
- KSJ commits. `extract_insights` runs through Claude Desktop; `commit_aiex` needs
  Paul's explicit approval. There is a violation precedent (AIEX-627).
- Editing `CORRECTIONS.md` entry text. If a correction reveals a register entry is
  wrong, **report it** — do not fix the register yourself.

---

## Reporting

For each task: files touched, a diff summary, and anything that didn't match what
this document predicted. The READMEs have already proven to describe a repository
layout that differs from what is on disk (C-015), so expect mismatches and report
them rather than working around them.

If any correction turns out to be unsupported by what you find in the files, say so.
The register has already been corrected three times by verification; a fourth would
be unremarkable.

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Corrections propagation · September 8, 2026*
