# C-017 Fix — September 9, 2026

Reproducibility record for the fix to `CORRECTIONS.md` entry **C-017**:
`chavez_transform_convergence` in `ChavezTransform_genuine.lean` was vacuous
(`∃ C, |C[f]| ≤ C` holds for any real number, using none of its four
hypotheses — confirmed independently by the Lean linter, which flagged all
four as unused on every build). Replaced with `chavez_transform_integrable`,
proving the transform's integrand is genuinely `IntegrableOn (a, b]`.

Build baseline reproduced first:

```
lake build ChavezTransformGenuine
```

Result: **8,028 jobs, 0 errors**, standalone target (not in `defaultTargets`
in `lakefile.toml`, so a plain `lake build` does not compile it — build it
explicitly by this target name, or import it from a file that does).

## The new theorem

```
'chavez_transform_integrable' depends on axioms: [propext, Classical.choice, Quot.sound]
'chavez_transform_stability' depends on axioms: [propext, Classical.choice, Quot.sound]
'K_realToSed_continuous' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Standard axioms only, no `sorryAx`. `chavez_transform_stability` (already a
genuine theorem, unaffected by this change) is reconfirmed unchanged.

## Hypothesis-use audit (standing check item 1)

The old theorem's `h_bounded` (a sup-norm bound on `f`) is **not** in the new
signature — it was checked and found unnecessary: integrability of the
integrand needs `f` to be integrable (not bounded) and `K(...)` to be bounded
(which follows from `h_alpha`, `h_d` alone via `K_bound`). Dropping a
hypothesis found unnecessary is the correct standing-check outcome, same as
`hs` in `SpectralIdentification.lean`'s `Fbase_nondegeneracy` (see
`verification/2026-09-08/`) — the difference here is the hypothesis was
dropped from the theorem signature rather than left in place decoratively.

The three hypotheses that remain were each tested by deletion:

| File | Hypothesis deleted | Result |
|---|---|---|
| `audit_no_h_alpha.lean` | `h_alpha` | **FAILS** — `unknown identifier 'h_alpha'` at the `K_bound` call |
| `audit_no_h_d.lean` | `h_d` | **FAILS** — `unknown identifier 'h_d'` at the `K_bound` call |
| `audit_no_h_integrable.lean` | `h_integrable` | **FAILS** — `unknown identifier 'h_integrable.norm'` / `'h_integrable'` at the majorant-integrability and measurability steps |

All three load-bearing. No decorative hypotheses in the new theorem.

## Proof sketch

`f(x) * K(P,Q,realToSed x,α,d)` is dominated a.e. on `(a,b]` by the
integrable majorant `stability_constant P Q α * |f x|` — the same
expression `chavez_transform_stability`'s own proof uses for its dominating
function (`(h_integrable.norm.1).const_mul _`) — and is itself
a.e.-strongly-measurable: `f` from `h_integrable`, and
`fun x => K P Q (realToSed x) α d` from a new helper lemma,
`K_realToSed_continuous`, which substitutes the exact 1D formulas
(`K_Z_realToSed`, `norm_realToSed_sq`) to reduce continuity to elementary
real analysis (polynomial × `exp` × `rpow` with strictly positive base, so
the `rpow`'s continuity holds regardless of the sign of its exponent
`-d/2`). `MeasureTheory.Integrable.mono'` then closes the goal.

## Files in this directory

| File | Purpose |
|---|---|
| `audit_no_h_alpha.lean`, `audit_no_h_d.lean`, `audit_no_h_integrable.lean` | Hypothesis-deletion tests above |

`K_realToSed_continuous` and `chavez_transform_integrable` themselves are
canonical — they live in `lean/ChavezTransform_genuine.lean`, not here. The
audit files are standalone scratch copies kept for the reproducibility
record; none were imported into the canonical stack.
