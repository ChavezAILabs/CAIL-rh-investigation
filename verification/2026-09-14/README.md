# C-022 Fix — September 14, 2026

Reproducibility record for `CORRECTIONS.md` entry **C-022**: "bilateral in both
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
`Clifford✓` exactly — a check that this script's index-to-blade map is the right
one, since it reproduces a result the paper already independently verified by a
different implementation). Only pattern 59 additionally satisfies Q·P = 0. The
other five have Q·P with residual coefficients ±2 on two grade-1 blades each — norm
`sqrt(2²+2²) = 2√2` — matching a figure already on record in
`docs/handoffs/CLAUDE_CODE_HANDOFF_PHASE78_Q18.md` (August 2026): "S1, S3–S6
collapse in Clifford (one-sided residual ‖QP‖ = 2√2)". That prior record is why
this entry is a propagation-gap correction (the fact was already known, just not
in the headline docs), not a new computational discovery — see C-022's full text
for the provenance.

## The mechanism (grade-homogeneity ⟺ bilaterality)

Not re-derived independently here (the algebraic argument, not just its numeric
consequence, is taken from the Claude Desktop chat and recorded in C-022) but
consistent with the computed output: Clifford reversion's sign is
`(-1)^(g(g-1)/2)` — `+1` at grade 1, `-1` at grade 2, `-1` at grade 3, `+1` at
grade 4. `reverse(P) = -P` only when both of `P`'s blade components share one
grade. Pattern 59's `P=e3+e12` and `Q=e5+e10` are the only pair in the Canonical
Six built entirely from grade-2 blades (grade-2 indices under the identity map:
`{3,5,6,9,10,12}`); every other pattern's `P`-vector mixes grades 1 and 3
(e.g. index 1 is grade 1, index 14 is grade 3 — `popcount(1)=1`, `popcount(14)=
popcount(0b1110)=3`), breaking the forcing argument that gives bilaterality in
Cayley-Dickson unconditionally (there, conjugation of a pure-imaginary sum is
always `-1` regardless of index, with no grade dependence — see C-022's Cayley-
Dickson argument).

## Files in this directory

| File | Purpose |
|---|---|
| `verify_clifford_bilateral.py` | Independent Cl(4,0) implementation + the six-pattern bilaterality check above |

This script is a standalone scratch verification, not part of the canonical Lean
stack or the CAILculator MCP server. No canonical file was modified to produce
this result.
