# Canonical Six — Corrections Register

**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Companion paper:** "The Canonical Six" (v1.3, Zenodo DOI
[10.5281/zenodo.17402495](https://doi.org/10.5281/zenodo.17402495))
**Opened:** September 15, 2026
**Maintainer:** Paul Chavez
**Status:** ACTIVE — 1 entry · 1 corrected · 0 open

---

## What This Document Is

A permanent, public, append-only record of every error found in the Canonical Six
companion paper and the repository documentation that describes it — in results,
in documentation, in formal proofs, and in the interpretation of data. This
register follows the same discipline and format as
[`CORRECTIONS.md`](CORRECTIONS.md), the CAIL-RH Investigation's own errata
register, but is kept separate because the two cover different published claims
with different DOIs: the Canonical Six paper is its own Zenodo record, not a
section of the RH investigation, even though both live in this repository and
share its Lean stack.

**Why a separate file, opened this late.** The first entry below (C-001) was
drafted against `CORRECTIONS.md`'s numbering before this file existed, on
2026-09-14, then moved here on merge the following day when it collided with an
independently-numbered RH-investigation entry (`CORRECTIONS.md` C-022, Phase 79
Run D) that had been assigned the same slot on a divergent branch. Moving it
here, rather than renumbering either entry, follows the principle that the
register should track the claim's own paper, not the repository's commit graph.

**Placement:** repository root, `CORRECTIONS_CANONICALSIX.md`, linked from
[`CORRECTIONS.md`](CORRECTIONS.md) and from the top of `README.md`.

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

Any of: a published number that cannot be reproduced; a claim whose stated
meaning does not follow from its evidence; a formal proof that is vacuous,
circular, or weaker than advertised; a retraction not propagated to every place
the claim appears; a provenance chain that cannot be traced to an artifact.

---

## Index

| ID | Title | Sev | Status |
|---|---|---|---|
| C-001 | "Bilateral in both frameworks" overstates 5 of 6 Canonical Six patterns | 2 | **Corrected** |

---

## Entries

### C-001 — "Bilateral in both frameworks" overstates 5 of 6 Canonical Six patterns
**Found:** 2026-09-14 · **By:** Claude (Desktop chat, independent Clifford derivation), verified from scratch by Claude Sonnet 5 (Claude Code) · **Severity:** 2 · **Status:** **Corrected**
**Affects:** `README.md` (Overview/Algebraic Foundations); `docs/roadmap.md`; `docs/RH_Investigation_Roadmap.md`; `supplemental/annihilation_topology.md`; `docs/aiex_001_hilbert_polya.md`

**The claim as published (README.md, and equivalently in the other affected files):**
"The algebraic foundation is the **Canonical Six** — six framework-independent
bilateral zero divisor patterns in 16D sedenion space, verified across both
Cayley-Dickson and Clifford algebras from 16D through 256D."

**Why it is wrong.** "Bilateral" (P·Q = 0 **and** Q·P = 0) was verified across both
frameworks for the Canonical Six as a group only in the sense that all six satisfy
P·Q = 0 in both — the published paper's own Table 1 states exactly this, one
direction only, matching its own one-sided zero-divisor definition (§2.2). It never
claims Clifford-side bilaterality, and neither does any Lean file — the sole
bilateral-zero-divisor formalization
(`lean/canonical_six_bilateral_zero_divisors_cd4_cd5_cd6.lean`) covers the
Cayley-Dickson side (CD4/CD5/CD6) only. **The published Zenodo v1.3 PDF is correct
as written and needs no correction** — every "bilateral" claim in it (Table 1's
one-directional formulas, Addendum C's 24-element family) is explicitly CD-scoped.

The overclaim is specific to the five affected repository documents, which state or
imply bilaterality itself was cross-framework-verified. It was not, for five of the
six patterns. Independently re-derived from scratch (Cl(4,0) geometric product,
implemented and sanity-checked against known identities, not the chat's own
arithmetic) and confirmed exactly: **only pattern 59 (S2: P=e₃+e₁₂, Q=e₅+e₁₀)
satisfies Q·P = 0 in Cl(4,0); the other five (patterns 18, 84, 102, 104, 124) have
Q·P ≠ 0 there**, with residual norm 2√2 in every case (a grade-1 blade and a
grade-3 blade in every case, not two grade-1 blades — checked directly against the
verification script's output, see the Reproducibility record below) — matching a
figure already on record in `docs/handoffs/CLAUDE_CODE_HANDOFF_PHASE78_Q18.md`
line 294–295 ("S2 = (e₃+e₁₂, e₅+e₁₀) is proven bilateral in both frameworks —
S1, S3–S6 collapse in Clifford (one-sided residual ‖QP‖ = 2√2)") and repeated as
established fact in `docs/handoffs/PHASE_78_Q18_BASELINE_CONFIRMED.md` line 117.
**This fact was already correctly recorded in the corpus, in an August 2026
Phase 78 handoff, and never propagated to the headline documents** — a finding
correct in one place, stale everywhere else it's cited, not a new computational
error.

**What is true instead.** All six Canonical Six patterns are bilateral zero
divisors in the Cayley-Dickson framework (CD4/CD5/CD6), formally proved in Lean with
zero sorries. Under the Clifford framework Cl(4,0)/Cl(5,0), only pattern 59 (S2) is
additionally bilateral; the other five satisfy the annihilation formula in one
direction only (matching Table 1 exactly), with a nonzero, norm-2√2 residual in the
reverse direction.

**The mechanism, newly derived and independently confirmed.** Conjugation
(Cayley-Dickson) and reversion (Clifford) are both anti-automorphisms:
conj(xy) = conj(y)·conj(x). In Cayley-Dickson, P and Q (sums of two imaginary basis
elements, no e₀ component) always satisfy conj(P) = −P, conj(Q) = −Q, so
P·Q = 0 ⟹ conj(P·Q) = 0 ⟹ conj(Q)·conj(P) = (−Q)(−P) = Q·P = 0 unconditionally —
bilaterality in Cayley-Dickson is forced, not observed, matching the "one-sided
two-term zero divisors cannot exist in the sedenions" result. In Clifford, reversion's
sign depends on grade, (−1)^(g(g−1)/2) — +1 at grade 1, −1 at grade 2, −1 at grade 3,
+1 at grade 4 — so reverse(P) = −P only when P's two blade components share a single
grade. Under the "identity" index-to-blade map (sedenion basis index i ↔ Clifford
blade with bitmask i over 4 generators, all squaring to +1 — confirmed to reproduce
the published Table 1/Table 2 classification exactly, and this is consistent with,
not proof of, that map being the one the paper's own Clifford verification used),
pattern 59's P = e₃+e₁₂ and Q = e₅+e₁₀ are the only pair built entirely from
grade-2 blades ({3,5,6,9,10,12} are exactly the grade-2 indices); every other
pattern's P-vector mixes grades 1 and 3 (e.g. index 1 is grade 1, index 14 is
grade 3), breaking the forcing argument. This also explains why, in the 24-element
framework-independent census, exactly 12 of the 24 ordered pairs are bilateral in
Clifford: grade-homogeneity and bilaterality coincide exactly on that set.

**Corrected:** 2026-09-14, in `README.md`, `docs/roadmap.md`,
`docs/RH_Investigation_Roadmap.md`, `supplemental/annihilation_topology.md`, and
`docs/aiex_001_hilbert_polya.md` — each now names pattern 59/S2 as the sole
Clifford-bilateral exception rather than describing all six as bilateral in both
frameworks. Historical dated phase/lab-notebook documents that carry the older
language (e.g. `lab-notebook/RH_Phase7_Handoff.md`, `RH_Phase19_Handoff.md`,
`RH_Phase23_Handoff.md`) are left as-is, consistent with how the RH register
treats history (see `CORRECTIONS.md` C-002). The published Zenodo v1.3 PDF is
unaffected and not corrected — it never made the overstated claim.

**Tested and narrowed, 2026-09-14 (same day, on request).** The grade-homogeneity
mechanism above was checked against more than the six patterns: the same
construction (`e_i ± e_{15-i}`), completed to all 8 index-mirror-pairs instead of
the 6 the Canonical Six happen to use, gives 16 candidate vectors and 112
Cl(4,0)-annihilating ordered pairs. **Grade-homogeneity ⟹ bilaterality holds with
zero exceptions across all 112** — a real, general, Lean-formalizable theorem, not
an artifact of the six-pattern census. **Grade-homogeneity ⟺ bilaterality does
not hold**: 48 of the 112 annihilating pairs are bilateral, but only 12 are
grade-homogeneous — 36 are bilateral without being grade-homogeneous. A refinement
(testing *reversion-sign* homogeneity — `(-1)^(g(g-1)/2)` groups grades {0,1,4}
together and {2,3} together, coarser than raw grade) explains 12 of those 36 (the
cases touching the scalar/pseudoscalar indices 0 and 15, which the six-pattern
census never used); 24 remain unexplained. Full breakdown and the extended script
in `verification/2026-09-14/`.

**What this means for a paper Addendum:** the provable general claim is the ⟹
direction (grade-homogeneous ⟹ bilateral), not the ⟺ the six-pattern census
suggested — that ⟺ was real on that census but not a general fact. An Addendum
built on ⟹ is solid; one claiming a full classification of Cl(4,0) bilateral pairs
is not yet supported and would need the remaining 24-pair mechanism identified
first. Formalizing the ⟹ direction in Lean, and identifying the missing mechanism,
are both separate, larger work, not undertaken as part of this correction.

**Reproducibility record:** `verification/2026-09-14/` — independent, from-scratch
Cl(4,0) geometric-product implementation, sanity-checked against known identities
before use, confirming all six patterns' P·Q = 0 (matching the published Table 1)
and exactly one (pattern 59) additionally satisfying Q·P = 0, plus the 112-pair
generalization test above.

---

## Log

| Date | Change |
|---|---|
| 2026-09-14 | C-001 found and corrected same day, on the RH investigation's `CORRECTIONS.md` (as a draft C-022) — see that register's 2026-09-14 log entries for the same-day history, including the same-day generalization test and two small factual fixes (residual blade grade, map-assumption overclaim) to the verification README caught on a follow-up review. |
| 2026-09-15 | This register opened. C-001 moved here from `CORRECTIONS.md`, where it had been drafted against that register's next open slot before this file existed — it collided with an independently-numbered entry (Phase 79 Run D) assigned the same slot on a divergent branch, and moving it here rather than renumbering either entry keeps each register tracking its own paper. Content, severity, and status carried over unchanged; only the entry number changed (C-022 → C-001) and cross-references in the five affected repository documents were updated to point here. |

---

*Chavez AI Labs LLC — Applied Pathological Mathematics*
*Corrections are the method, not the exception.*
