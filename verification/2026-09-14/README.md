# C-001 Fix — September 14, 2026 (CORRECTIONS_CANONICALSIX.md)

Reproducibility record for `CORRECTIONS_CANONICALSIX.md` entry **C-001**: "bilateral in both
Cayley-Dickson and Clifford frameworks" overstates five of the six Canonical Six
patterns. A Claude Desktop chat derived that only pattern 59 (S2) is a genuine
bilateral (two-sided) zero divisor in Cl(4,0) — the other five satisfy P·Q = 0
but not Q·P = 0 there — via a grade-homogeneity argument on Clifford reversion.
This directory is an independent, from-scratch re-derivation, not a transcription
of that chat's own arithmetic.

## What this verifies

`verify_clifford_bilateral.py` implements the Cl(4,0) geometric product directly
(bitmask blades over 4 generators, all squaring to +1; standard sign-tracking
algorithm for reordering blade products), with its own sanity checks against known
identities (`e1*e2=e12`, `e2*e1=-e12`, `e1*e1=1`, `e12*e12=-1`) run before anything
else, then computes P·Q and Q·P directly for all six Canonical Six patterns under
the "identity" index-to-blade map (sedenion basis index *i* ↔ Clifford blade with
bitmask *i*).

```
python verify_clifford_bilateral.py
```

Result:

```
Bilateral (P*Q=0 AND Q*P=0) in Cl(4,0): [59]
One-sided (P*Q=0 only) in Cl(4,0): [18, 84, 102, 104, 124]
```

All six patterns satisfy P·Q = 0 (matching the published paper's Table 1
`Clifford✓` exactly — this is consistent with the "identity" index-to-blade map
being the one the paper's own Clifford verification used, since it reproduces
that verification's result under a fully independent implementation; it does not
rule out some other map also reproducing Table 1, and the map is not stated
explicitly anywhere in the paper — see the caveat in C-001's own text). Only
pattern 59 additionally satisfies Q·P = 0. The other five have Q·P with residual
coefficients ±2 on one grade-1 blade and one grade-3 blade each (e.g. pattern 18:
`{2: -2, 13: 2}` — index 2 is grade 1, index 13 is grade 3) — norm
`sqrt(2²+2²) = 2√2` — matching a figure already on record in
`docs/handoffs/CLAUDE_CODE_HANDOFF_PHASE78_Q18.md` (August 2026): "S1, S3–S6
collapse in Clifford (one-sided residual ‖QP‖ = 2√2)". That prior record is why
this entry is a propagation-gap correction (the fact was already known, just not
in the headline docs), not a new computational discovery — see C-001's full text
for the provenance.

## The mechanism on the six patterns (grade-homogeneity ⟹ bilaterality)

Not re-derived independently here (the algebraic argument, not just its numeric
consequence, is taken from the Claude Desktop chat and recorded in C-001) but
consistent with the computed output: Clifford reversion's sign is
`(-1)^(g(g-1)/2)` — `+1` at grade 1, `-1` at grade 2, `-1` at grade 3, `+1` at
grade 4. `reverse(P) = -P` only when both of `P`'s blade components share one
grade. Pattern 59's `P=e3+e12` and `Q=e5+e10` are the only pair in the Canonical
Six built entirely from grade-2 blades (grade-2 indices under the identity map:
`{3,5,6,9,10,12}`); every other pattern's `P`-vector mixes grades 1 and 3
(e.g. index 1 is grade 1, index 14 is grade 3 — `popcount(1)=1`, `popcount(14)=
popcount(0b1110)=3`), breaking the forcing argument that gives bilaterality in
Cayley-Dickson unconditionally (there, conjugation of a pure-imaginary sum is
always `-1` regardless of index, with no grade dependence — see C-001's Cayley-
Dickson argument).

## Generalization test: does the criterion extend beyond these six pairs?

The six patterns are one specific census (the Cayley-Dickson zero-divisor
discovery), not an exhaustive search of Cl(4,0). The script's final section tests
the same construction (`e_i ± e_{15-i}`, the "mirror pair" form all six patterns
already use) completed to all 8 index-mirror-pairs `(0,15)` through `(7,8)` instead
of just the 6 that happen to appear in the Canonical Six — 16 candidate vectors,
240 ordered pairs, 112 of which annihilate (`P·Q=0`) in Cl(4,0).

**Result: the criterion does not generalize to a clean if-and-only-if.**

- **Sufficiency holds with zero exceptions.** Every one of the 12 grade-homogeneous
  annihilating pairs is bilateral. This direction is the one the reversion
  argument actually proves, and it generalizes cleanly — this is a real,
  Lean-formalizable theorem: *grade-homogeneous annihilating pairs in Cl(4,0) are
  always bilateral*, not just the six.
- **Necessity fails.** 48 of the 112 annihilating pairs are bilateral — four times
  the 12 that are grade-homogeneous. 36 pairs are bilateral *without* being
  grade-homogeneous. The six-pattern census never surfaced this because none of
  the six uses index 0 (scalar) or 15 (pseudoscalar), and it happened to be exactly
  narrow enough that "same grade" and "same reversion sign" looked identical.
- **A refinement closes 12 of the 36.** Reversion's sign, `(-1)^(g(g-1)/2)`, is
  `+1` at grades {0,1,4} and `-1` at grades {2,3} — a coarser equivalence than raw
  grade. Testing *reversion-sign*-homogeneity instead of grade-homogeneity
  correctly resolves every mismatch involving index 0/15 (scalar+pseudoscalar
  vectors, which mix grade 0 and grade 4 but share reversion sign `+1`) — down to
  24 unexplained mismatches.
- **24 remain unexplained.** Pairs like `(e1+e14)·(e2−e13) = 0` are bilateral
  despite neither vector being homogeneous by grade *or* by reversion sign. Some
  other mechanism, not identified here, produces bilaterality in these cases.
  Not chased further — recording the open question rather than forcing a
  narrative.

**What this means for a paper Addendum:** the provable, general claim is
*grade-homogeneity ⟹ bilaterality* in Cl(4,0) (or the slightly stronger
*reversion-sign-homogeneity ⟹ bilaterality*), not the ⟺ the six-pattern census
suggested. That six-case ⟺ was real but coincidental to a census that never
touched the scalar/pseudoscalar case and apparently never touched whatever
produces the remaining 24. An Addendum built on the ⟹ direction is solid; one
claiming a full classification is not yet supported.

## Files in this directory

| File | Purpose |
|---|---|
| `verify_clifford_bilateral.py` | Independent Cl(4,0) implementation, the six-pattern check, and the generalization test above |

This script is a standalone scratch verification, not part of the canonical Lean
stack or the CAILculator MCP server. No canonical file was modified to produce
this result.
