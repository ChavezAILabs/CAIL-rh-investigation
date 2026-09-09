# CAIL-RH Investigation — Phase 78 Verification Batch: Claude Code Handoff

**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Date:** September 8, 2026
**From:** Claude Opus 5 (Claude.ai session) — corrections review of Phase 77/78 artifacts
**To:** Claude Code (in-shell)
**Branch:** none yet — Task 1 opens `phase-78-q18`
**Status:** Six tasks. Five are verification checks that resolve open entries in the
Corrections Register; one is a commit. No new research. No claims to be made.

**This document is public.** It is published alongside `CORRECTIONS.md` as part of
the investigation's open-science record.

---

## Context

The CAIL-RH Investigation is a formal Lean 4 + empirical study of the Riemann
Hypothesis using 16D sedenion zero-divisor algebra (the Canonical Six), the Chavez
Transform, and the Zero Divisor Transmission Protocol. Phase 78 completed the Q-18
detector-ensemble question empirically.

A September 8 review of the Phase 77/78 artifacts, READMEs, and Lean sources opened
a standing **Corrections Register** (`CORRECTIONS.md`, 21 entries). Several entries
assert specific defects that have **not yet been verified against a live build or a
re-run**. Publishing unverified corrections in a corrections document would defeat
its purpose.

Your job is to run those verifications and report exactly what comes back —
including results that contradict the register. **A withdrawn entry is a good
outcome, not a failure.**

---

## What's Already Done

- Phase 78 Q-18 empirical track complete: Candidates 1–3 and Run C executed
  Aug 22–23, 2026. Results in four JSONs (see Key Files).
- Candidate 3 (k=1 → k=2, eight primes) is the positive result: T1 z 8.42 → 9.84
  at γ₁–γ₁₀₁, holding to γ₃₄₀.
- Candidates 1 and 2 are negative results with identified mechanisms.
- Corrections Register opened Sept 8, 2026, 21 entries, in the working folder.
- **Nothing from Phase 78 is in version control.** No branch, no commits. All
  artifacts exist in a single working tree on one machine.

---

## Task 1 — Commit Phase 78 to a local branch

**Do this first, before any other task.** Everything below modifies or adds files.

```bash
git checkout -b phase-78-q18
git add scripts/phase78_q18_*.py results/phase78_q18_*.json \
        docs/phases/RH_PHASE_78_RESULTS.md CORRECTIONS.md
git status          # review before committing
git commit -m "Phase 78: Q-18 detector ensemble + Run C; corrections register opened"
```

Include `phase77_q17_signed_channel.py` and `phase77_q17_results.json` if they are
not already tracked — see Task 6.

**Do NOT push.** Standing order 4: no push without Paul's explicit review. Local
commits only. Report the commit hash.

---

## Task 2 — C-019: axiom footprint of `eigenvalue_zero_mapping`

**Register claim:** both READMEs give `eigenvalue_zero_mapping` the footprint
`[propext, riemann_critical_line, Classical.choice, Quot.sound]`, but it is built
from `spectral_implies_zeta_zero`, which contains a `sorry` at
`SpectralIdentification.lean` line 139. The footprint should therefore include
`sorryAx`.

**Run:**

```lean
-- axiom_check_c019.lean, project root
import SpectralIdentification
#print axioms eigenvalue_zero_mapping
#print axioms zeta_zero_implies_spectral
#print axioms spectral_implies_zeta_zero
#print axioms spectral_implies_critical_line
```

```bash
lake env lean axiom_check_c019.lean
```

**Report all four footprints verbatim.** Do not paraphrase, do not summarize as
"standard only," do not reformat. Copy the exact output.

**Expected if the register is right:** `eigenvalue_zero_mapping` and
`spectral_implies_zeta_zero` include `sorryAx`; the other two do not.
**If `eigenvalue_zero_mapping` comes back without `sorryAx`,** say so plainly —
C-019 is then withdrawn and the READMEs were correct.

---

## Task 3 — C-020: hypothesis-use audit

**Register claim:** `Fbase_nondegeneracy` in `SpectralIdentification.lean` takes
`hs : 0 < s.re ∧ s.re < 1` and never uses it.

**Method — standing check item 1.** Copy the file to a scratch location, delete the
hypothesis from the signature, re-elaborate. If it still compiles, the hypothesis is
decorative.

Apply the same audit to the four theorems in `GatewayLinearLaw.lean`
(`gateway_magSq_sub`, `gateway_pairing_iff`, `pairing_sigma_independent`,
`ba_asymptote_sq`) — these are the infrastructure the RH paper's Lean targets sit
on, so their hypotheses matter more than most.

**Report:** for each theorem, which hypotheses are load-bearing and which are not.
**Do not modify the canonical files.** Scratch copies only; report findings and let
Paul decide.

Also flag: `SpectralIdentification.lean` lines 99–101 say Path B "relies on the
hwitness sorry in `Fbase_nondegeneracy`," while line 28 of the same file says
hwitness was CLOSED. Confirm which is current.

---

## Task 4 — C-008: is the null Monte-Carlo variation or scope dependence?

**The problem.** `phase77_q17_results.json` and `phase78_q18_runC_results.json`
evaluate the identical configuration at N=101. The observed statistic is
bit-identical in both — `1.9661573443371425` — but the nulls differ:

| | null_mean | null_std | z |
|---|---|---|---|
| `phase77_q17_results.json` | −0.0104500995552135 | 0.23461305292875698 | 8.4250 |
| `phase78_q18_runC_results.json` (N=101) | 0.007087079361809704 | 0.23093736963401 | 8.4831 |

`RH_PHASE_78_RESULTS.md` §4 attributes this to the null sampling over [10,600]
rather than [10,240]. That is untested. **If the scope explanation is correct it is
the more serious finding**, because reported significance would then depend on how
much grid was swept beyond the zeros being tested.

**Three-arm test.** Same detector (k=1, six primes), same 101 zeros throughout.

- **Arm A — determinism.** t ∈ [10,240], fixed seed `20260612`, run twice. Expect
  bit-identical z. If not, there is unseeded randomness and everything below is
  moot — stop and report.
- **Arm B — Monte-Carlo spread.** t ∈ [10,240], five different seeds. Report all
  five z values, their mean and standard deviation.
- **Arm C — scope dependence.** t ∈ [10,600], the same five seeds as Arm B, still
  evaluating only the 101 zeros with γ < 240. Report all five z values.

**Interpretation:** if Arm C's spread overlaps Arm B's, the 8.42/8.48 gap is
Monte-Carlo noise and the Phase 78 explanation is wrong (harmlessly). If Arm C is
systematically shifted beyond Arm B's spread, scope dependence is real and must be
characterized before any z is published.

**Also report, for every arm:** the permutation/resample count `N_perm`, and the
smallest non-zero p-value the null can resolve. Across all five existing JSONs
`p_two_sided` is 0.0 except for two values (0.0004 and 0.0576), which suggests a
floor near 2×10⁻⁴. Confirm the actual `N_perm` in the source. This resolves C-007.

---

## Task 5 — C-011: ROC and peak metrics for the k=2 detector

**The gap.** `phase78_q18_candidate3_results.json` contains no `roc` and no `peaks`
keys. `phase77_q17_results.json` contains both. The winning candidate is currently
evaluated on one statistic against a baseline described with two.

This matters because T1 is a value-at-zeros statistic and the eight-prime detector
has larger amplitude by construction, so T1 alone cannot separate improved detection
from a larger number. Supporting concern: across all four Run C checkpoints the
ext8/base6 observed ratio is flat (1.353, 1.322, 1.330, 1.333), which is what a
uniform amplitude gain looks like rather than a resolution improvement.

**Compute, for ext8 (c_S2 + c_S3, eight primes) at N=101 and N=340:**
- ROC AUC at δ = 0.25 and δ = 0.5
- Peak precision, recall, F1 at ε = 0.5 and ε = 1.0, with `n_maxima` and
  `n_predictions`
- The same metrics for base6 at N=340 (the baseline currently has them at N=101
  only), so the comparison is like-for-like at both scales

Use the identical ROC and peak-finding code paths as `phase77_q17_signed_channel.py`
— do not reimplement. Write to `results/phase78_q18_candidate3_roc_results.json`.

**Report the honest baseline alongside every precision figure.** Random-prediction
precision differs between ε = 0.5 and ε = 1.0; the existing documents quote 0.433
for both, which cannot be right. Compute both and state which radius each belongs
to. This resolves part of C-011 and all of the honest-baseline half of C-007.

---

## Task 6 — C-012: locate any June-dated Q-17 artifact

**The problem.** All five result JSONs share a file origination date, and
`phase77_q17_results.json` is 3,557 bytes where `DATA_MANIFEST_CLAUDE_CODE.md`
describes a ~15 KB June 12 file. The Phase 78 pre-flight "reproduced the baseline
exactly" by comparing a script's output to a file the same script wrote in the same
session.

**Search the machine and any backups** for any copy of `phase77_q17_results.json`,
`phase77_q17_live_validation.json`, or `phase77_q15_results.json` with a June 2026
timestamp. Check git history in case an earlier version was ever committed.

**If found:** record path, size, timestamp, SHA-256, and diff against the current
file.
**If not found:** say so. The provenance claim then gets restated as "regenerated
on [date] from `phase77_q17_signed_channel.py`," and AIEX-741/742's citation chain
is annotated accordingly.

---

## Encoding Reference — use this, not the older handoff

The Phase 78 handoff (`CLAUDE_CODE_HANDOFF_PHASE78_Q18.md`) contains two errors
that are corrected here. Prefer this section over that document.

### Weights

**Always compute `w_p = log(p) / sqrt(p)` from the formula. Never hardcode a
table.** The §11 table in the older handoff is wrong for p = 5, 7, 11, 13 — it is
monotonically increasing, while the true sequence peaks at p = 7 (log p/√p is
maximized at p = e² ≈ 7.39).

Correct values, **for verifying your computation only**:

```
w2  = 0.4901291    w3  = 0.6342841    w5  = 0.7197625
w7  = 0.7354849    w11 = 0.7229926    w13 = 0.7113890
w17 = log(17)/sqrt(17)                w19 = log(19)/sqrt(19)
```

### Slot map (16D Detector Encoding, σ = 0.5, pos2 = 0)

| slot | contents |
|---|---|
| 0 | σ |
| 1 | t |
| 2 | **0** — zeroed, non-negotiable (breaks c_S6 purity otherwise) |
| 3 | w₂·cos(t·ln 2) |
| 4 | w₁₇·cos(t·ln 17) — k=2 only, S3 support |
| 5 | w₃·cos(t·ln 3) |
| 6 | w₅·cos(t·ln 5) |
| 9 | w₇·cos(t·ln 7) |
| 10 | w₁₁·cos(t·ln 11) |
| 11 | w₁₉·cos(t·ln 19) — k=2 only, S3 support |
| 12 | w₁₃·cos(t·ln 13) |
| 7, 8, 13, 14, 15 | 0 |

u₂ support = {3, 5, 10, 12} ← p ∈ {2, 3, 11, 13}.
u₆ support = {6, 9} ← p ∈ {5, 7}.
**Index 7 is in the support of no gateway.** A signal placed there is invisible to
every reading. The older handoff's "unused u₂ slots {4,7}" is wrong on both counts.

### Detector channels

- **k=1 (six primes):** `c_S2 + c_S6`. Identity residual 1.78×10⁻¹⁵.
- **k=2 (eight primes):** `c_S2 + c_S3`. Residuals 8.88×10⁻¹⁶ (7 primes),
  1.78×10⁻¹⁵ (8 primes).
- Under the k=1 encoding, **S3 ≡ S6 exactly** (`max|c_S3 − c_S6| = 0.0`) because
  slots {4, 11} are zeroed. The k=2 extension works by breaking that degeneracy —
  it is the same channel pair, not a different detector.

### Do not use

The `(z_g/Σz)²` per-gateway weighting from the older handoff §3 Step 3. It squares
away the sign, so the three Class B gateways (z ≈ −2.3, anti-correlated with zero
locations) get positive weight, and the weights sum to 1.1008 rather than 1. That
formula is a documented defect (C-014), not a method.

---

## Key Files

| File | Purpose |
|---|---|
| `CORRECTIONS.md` | Standing corrections register — read entries C-007, C-008, C-011, C-012, C-019, C-020 before starting |
| `scripts/phase77_q17_signed_channel.py` | k=1 baseline; source of the ROC/peak code paths to reuse |
| `results/phase77_q17_results.json` | Baseline results (provenance under review, Task 6) |
| `results/phase78_q18_runC_results.json` | Run C, four checkpoints, both detectors |
| `results/phase78_q18_candidate3_results.json` | k=2 result, T1 only — Task 5 fills the gap |
| `lean/SpectralIdentification.lean` | Tasks 2 and 3 |
| `lean/GatewayLinearLaw.lean` | Task 3 hypothesis audit |
| `docs/phases/RH_PHASE_78_RESULTS.md` | Phase 78 narrative (contains the C-001 misreading) |

**Build directory convention:** edit canonical files in `lean/`, copy to
`AsymptoticRigidity_aristotle/` before building.

**Build-log encoding:** PowerShell `tee` produces UTF-16 LE and corrupts warning
line numbers. Use `Out-File -Encoding utf8`, or treat `lake env lean` axiom checks
as the definitive sorry audit rather than `lake build` warnings.

---

## Reporting Format

For each task, report:

1. **Task number and register entry.**
2. **Command(s) run**, verbatim.
3. **Output**, verbatim for anything involving `#print axioms`, z-scores, or file
   hashes. No paraphrase, no rounding, no "matches expected."
4. **Verdict:** register entry CONFIRMED / WITHDRAWN / MODIFIED — and if modified,
   what the entry should say instead.
5. **Anything unexpected**, including things not asked about.

State what you did not do and why. If a task cannot be completed, say so rather
than working around it.

---

## Safety / Gotchas

1. **Axiom discipline.** `riemann_critical_line` is the sole non-standard axiom.
   Never discharge it — no tactic, no `sorry`, no `native_decide`. No new axioms.
2. **Sorry count is exactly 1** (`spectral_implies_zeta_zero`, by design — the
   pointwise converse is mathematically false). Never close it.
3. **Files 1–16 do not get modified.** Task 3 uses scratch copies only.
4. **No push.** Local commits fine; pushing needs Paul's explicit review.
5. **No KSJ commits.** `extract_insights` runs through Claude Desktop, and
   `commit_aiex` needs Paul's explicit approval. Never auto-commit — there is a
   violation precedent (AIEX-627, May 5).
6. **CAILculator server state.** The input-validation hardening from the Aug 21–22
   audit is in the editable install but the server process may not have restarted.
   Restart before any live MCP call and say whether you did.
7. **Report contradictions rather than resolving them.** If a check disagrees with
   the register, the register is what changes.

---

## Out of Scope

Do not, this session:

- Propagate corrections into the READMEs, phase docs, or handoff docs. The register
  is the record; the edits are a separate pass, and doing both at once is how a
  correction becomes a rewrite.
- Push anything to GitHub.
- Start Phase 79 (32D/64D dimensional hierarchy) or any feasibility work.
- Add Lean files or attempt `detector_channel_identity` /
  `extended_detector_channel_identity`. Stack growth is Paul's call.
- Attempt Candidate 4 (Clifford variant) — still gated.
- Re-run Candidates 1 or 2. Their negative verdicts stand; only C-010's wording
  changes.
- Rewrite `RH_PHASE_78_RESULTS.md`. Task 5's output will change what it should say.

---

## Why This Batch Exists

Four entries in the register — C-002, C-016, C-017, C-021 — are the same defect:
**a theorem true for reasons unrelated to the mathematics it claims to establish.**
One had a degenerate definition, one a degenerate statement, one a definition that
unfolds into its neighbour, one a construction engineered to have the property it
then verifies.

`#print axioms` catches none of them. It detects `sorryAx` and non-standard axioms;
a vacuous theorem is fully proved from standard axioms and reports a clean
footprint. The investigation's headline verification metric is structurally blind
to its most common failure mode.

Tasks 2 and 3 are the first application of the standing check that follows from
that. Tasks 4, 5 and 6 do the same for the empirical side, where the analogous
blindness is a Monte-Carlo p-value floor reported as significance.

The point is not to find more errors. It is to make sure that what gets published
next — corrections included — has been checked rather than asserted.

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 78 Verification Batch · September 8, 2026*
