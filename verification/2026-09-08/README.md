# Verification Batch — September 8, 2026

Reproducibility record for the Lean checks behind `CORRECTIONS.md` entries
**C-019** and **C-020**. Run against a clean Mathlib cache fetched the same day
(the environment that produced the June 2026 build figures had been lost from
the local machine and was re-established from scratch — see `CORRECTIONS.md`
"Second Failure Mode" for what that cost).

Build baseline reproduced first, to confirm the environment matches
`CLAUDE.md`:

```
lake build
```

Result: **8,061 jobs, 0 errors**, matching the `CLAUDE.md` Phase 76 baseline
exactly. One sorry (`spectral_implies_zeta_zero`, by design, unchanged).

---

## C-019 — `axiom_check_c019.lean`

```
lake env lean axiom_check_c019.lean
```

Verbatim output:

```
'eigenvalue_zero_mapping' depends on axioms: [propext, riemann_critical_line, sorryAx, Classical.choice, Quot.sound]
'zeta_zero_implies_spectral' depends on axioms: [propext, riemann_critical_line, Classical.choice, Quot.sound]
'spectral_implies_zeta_zero' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
'spectral_implies_critical_line' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`eigenvalue_zero_mapping` carries `sorryAx`. Both READMEs' published footprint
for it (which omits `sorryAx`) was wrong. Confirms C-019.

---

## C-020 — `audit_c020_Fbase_nondegeneracy.lean` and `audit_c020_ba_asymptote_sq.lean`

Standing check item 1 (hypothesis-use audit): delete a hypothesis, re-elaborate,
see if it still compiles. Two of the four candidate theorems had a Prop
hypothesis to test; the other two (`gateway_pairing_iff`, `gateway_magSq_sub`)
take no Prop hypotheses at all, so there was nothing to delete for them.

**`Fbase_nondegeneracy`** (`SpectralIdentification.lean`), with
`hs : 0 < s.re ∧ s.re < 1` removed from the signature:

```
lake env lean audit_c020_Fbase_nondegeneracy.lean
```

Result: **compiles clean, exit 0.** `hs` is decorative — the result is pure
sedenion algebra and holds for any `s`.

Independently confirmed by the Lean linter itself, present in every full build
since Phase 73:

```
warning: SpectralIdentification.lean:66:35: unused variable `hs`
```

**`ba_asymptote_sq`** (`GatewayLinearLaw.lean`), with `hK : 0 ≤ K` removed from
the signature (proof body otherwise identical):

```
lake env lean audit_c020_ba_asymptote_sq.lean
```

Result: **fails.**

```
audit_c020_ba_asymptote_sq.lean:46:32: error: failed to prove positivity/nonnegativity/nonzeroness
```

`hK` is load-bearing: `positivity` needs `K ≥ 0` to establish `t² + K ≠ 0` for
*all* `t > 0` (the `filter_upwards [Filter.eventually_gt_atTop 0]` step is not
restricted to eventually-large `t`, so a negative `K` could make `t² + K = 0`
at some small positive `t`). Without it the proof does not go through.

Docstring staleness in the same file, confirmed by grep rather than by a Lean
run: `SpectralIdentification.lean` line 28 records hwitness as CLOSED; lines
99–101 still say Path B "relies on the hwitness sorry." `grep sorry` on the
file finds exactly one real `sorry` keyword (line 139, in
`spectral_implies_zeta_zero`, unrelated to hwitness) — lines 99–101 are stale
against the file's own header.

---

## Files in this directory

| File | Purpose |
|---|---|
| `axiom_check_c019.lean` | C-019 axiom-footprint check |
| `audit_c020_Fbase_nondegeneracy.lean` | C-020 deletion test, `hs` (negative result — decorative) |
| `audit_c020_ba_asymptote_sq.lean` | C-020 deletion test, `hK` (positive result — load-bearing) |
| `build2.log` | Full `lake build` output for this session's run (8,061 jobs, includes the `hs` linter warning) |

None of these files are part of the canonical stack (files 1–17 in `lean/`)
and none were imported into it. They are standalone scratch copies against the
project's Mathlib environment, kept here rather than in
`AsymptoticRigidity_aristotle/` because that directory gets rebuilt and would
lose them.
