# Canonical Six — Corrections Register

**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Companion paper:** "The Canonical Six" (v1.3, Zenodo DOI
[10.5281/zenodo.17402495](https://doi.org/10.5281/zenodo.17402495))
**Opened:** September 15, 2026
**Maintainer:** Paul Chavez
**Status:** ACTIVE — 3 entries · 1 corrected · 2 open

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
| C-001 | "Bilateral in both frameworks" overstates 5 of 6 Canonical Six patterns | 2 | **Corrected** (paper repository README: applied 2026-10-13, see addendum) |
| C-002 | "Dimensional persistence" is guaranteed by subalgebra embedding | 3 | Open |
| C-003 | "100% formal verification" headline omits that key theorems use `native_decide` | 2 | Open |

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

**Addendum, 2026-10-13: propagation to the paper repository's README, and the Lean
coverage of the Clifford side.** The paper's own repository
(`pchavez2029/framework-independent-zero-divisors`) was not among the five documents
corrected on 2026-09-14. Its README marks all six patterns "CD ✓ Clifford ✓" in the
Canonical Six table, says in Key Findings that the six "work identically in both
Cayley-Dickson and Clifford algebras" and that they persist through "Both associative
(Clifford) and non-associative (Cayley-Dickson) frameworks", without stating that the
Clifford-side result is P·Q = 0 in one direction only, with pattern 59 (S2) the sole
Clifford-bilateral pattern.

That one-directional Clifford result *is* formally verified in Lean, contrary to how
this entry's account above could be read. `dc08bbac-primary.lean`, a v1.2 file in the
paper repository (Lean v4.24.0, listed there under "v1.2 Files (Preserved for
Reproducibility)"), defines Cl(4,0) and Cl(5,0) over ℚ with Mathlib's `CliffordAlgebra`
and proves P·Q = 0 in Cl(4,0) for all six patterns
(`pattern_{18,59,84,102,104,124}_cl4_verified`), P·Q = 0 in Cl(5,0) for patterns 18,
59 and 84, and P·Q ≠ 0 in Cl(4,0) for four non-Canonical patterns
(`pattern_{58,101,103,19}_cl4_fails`), with zero sorries (two of its declarations,
`pattern_18_cl5` and `e_cl5_1`, use `native_decide`; see C-003). The statement above
that no Lean file claims Clifford-side *bilaterality* stands: none proves Q·P = 0 in
Clifford. The README's coverage bullet "Framework independence (Clifford vs.
Cayley-Dickson) mathematically verified" is therefore supported in the paper's own
one-directional sense, but it doesn't say "one direction" and doesn't name the file,
which is not in the v1.3 list.

**Paper repository README, 2026-10-13 (applied locally, not yet pushed, pending
Paul's review):** the table's Clifford column and the Key Findings lines annotated
with the one-direction scope and the pattern 59 exception; the coverage bullet
reworded to "P·Q = 0 in Cl(4,0) for all six patterns (one direction; Q·P = 0 only for
pattern 59), in `dc08bbac-primary.lean`"; and a link to this register added near the
top.

---

### C-002 — "Dimensional persistence" is guaranteed by subalgebra embedding
**Found:** 2026-10-13 · **By:** Claude Desktop (structural argument), checked against the paper's methodology by Claude Code · **Severity:** 3 · **Status:** Open
**Affects:** v1.0–v1.3 abstract and §§ on dimensional persistence ("exact preservation of zero divisor properties through successive dimensional doublings"; "superlinear dimensional stability … suggesting they occupy mathematically distinguished positions"); paper repository README (Key Findings: "12 patterns with dimensional persistence (16D → 256D)"; "256-fold complexity increase with perfect structural preservation"; coverage bullet "Dimensional persistence through CD6 (256D)"); RH repository `README.md` (Canonical Six "Dimension-stable … (Block Replication Theorem)")

**The claim as published:** The patterns persist exactly from 16D through 256D in
Cayley-Dickson and from 16D to 32D in Clifford, and this persistence, "maintaining
exact structure through 256-fold complexity increase," indicates distinguished
structure.

**Why it is wrong:** Each Cayley-Dickson doubling contains the previous algebra as a
subalgebra: with (a, b)(c, d) = (ac − d̄b, da + bc̄), the map a ↦ (a, 0) gives
(a, 0)(c, 0) = (ac, 0). Likewise Cl(4,0) is a subalgebra of Cl(5,0). The paper's
method is exactly this embedding: `main_v1.0.tex` (line 164) describes testing
"whether patterns discovered at lower dimensions maintained zero divisor properties
when embedded in higher-dimensional algebras, preserving their index structure", and
the Lean files do the same (`lift`, then `e5 1 + e5 14` and so on in
`dc08bbac-primary.lean`). Under that embedding, every sedenion zero divisor pair
remains a zero divisor pair in every higher Cayley-Dickson algebra, necessarily, not
only these six. The paper's table (12/12 at every Cayley-Dickson dimension) records
that guarantee, not a property that distinguishes the patterns. The original Python
verification scripts are not in the repository, so the check rests on the paper's own
description of its method.

**What is true instead:** Persistence under doubling holds for every sedenion zero
divisor and follows from the Cayley-Dickson construction. The evidence that the six
are distinguished rests on the framework comparison (C-001) and the E₈ results, not
on persistence.

**Recommended:** state the subalgebra argument wherever persistence is cited, and
drop "persistence" from the list of properties that distinguish the six.

---

### C-003 — "100% formal verification" headline omits that key theorems use `native_decide`
**Found:** 2026-10-13 · **By:** Claude Desktop (README read), Claude Code (source read) · **Severity:** 2 · **Status:** Open
**Affects:** paper repository README ("100% formal verification in Lean 4, zero sorry stubs"; "Full formal verification in Lean 4 (zero sorry stubs)"; Verification Coverage list); Zenodo v1.3 record description ("Full formal verification in Lean 4 confirms all core structural claims with zero sorry stubs"); v1.3 abstract's equivalent sentence

**The claim as published:** "100% formal verification in Lean 4, zero sorry stubs."

**Why it is misleading:** The sorry count is right (zero in code in every file), but
several headline results are proved with `native_decide`, which trusts the compiled
evaluator rather than the kernel and adds the axiom `Lean.ofReduceBool` to each
theorem's footprint. The README reports no axiom footprint. Per file (theorems using
`native_decide`):

- `e8_weyl_orbit_unification.lean`: `Theorem_1a`, `Theorem_1b` — the E₈ first-shell
  and Weyl-orbit results themselves.
- `canonical_six_parents_of_24_phase4.lean`: 7, including `All_ZDs_Generated` and
  `Count_Unique_ZDs_Is_24` — the 24-family results.
- `g2_family_24_investigation.lean`: 37.
- `master_theorem_scaffold_phase5.lean`: `Theorem_1a`, `Theorem_1b`,
  `CanonicalSix_G2Invariant_Combinatorial`.
- `dc08bbac-primary.lean`: `pattern_18_cl5`, `e_cl5_1`.
- `canonical_six_bilateral_zero_divisors_cd4_cd5_cd6.lean` and
  `c038a2e4-alternative.lean`: none. **The CD4–CD6 bilateral zero-divisor proofs are
  fully kernel-checked.**

The paper's own `LEAN_README.md` names `native_decide` as a proof tactic, so the
omission is in the summary, not hidden. Already flagged internally as F-10 in the
v1.4 organizing document.

**What is true instead:** The bilateral zero-divisor results are formally verified
with kernel-checked proofs; the E₈ and 24-family headline results are verified with
`native_decide`, i.e. relying on the compiler as well as the kernel.

**Recommended:** state per file: sorry count, whether `native_decide` is used, and the
`#print axioms` footprint of each headline theorem (to be run on a v4.24.0 build).
README now; paper text in v1.4.

---

## Log

| Date | Change |
|---|---|
| 2026-09-14 | C-001 found and corrected same day, on the RH investigation's `CORRECTIONS.md` (as a draft C-022) — see that register's 2026-09-14 log entries for the same-day history, including the same-day generalization test and two small factual fixes (residual blade grade, map-assumption overclaim) to the verification README caught on a follow-up review. |
| 2026-09-15 | This register opened. C-001 moved here from `CORRECTIONS.md`, where it had been drafted against that register's next open slot before this file existed — it collided with an independently-numbered entry (Phase 79 Run D) assigned the same slot on a divergent branch, and moving it here rather than renumbering either entry keeps each register tracking its own paper. Content, severity, and status carried over unchanged; only the entry number changed (C-022 → C-001) and cross-references in the five affected repository documents were updated to point here. |
| 2026-10-13 | C-001 addendum: the paper repository's own README (not among the five documents corrected on 2026-09-14) still described all six patterns as working identically in both frameworks; annotated there with the one-direction scope and the pattern 59 exception, and linked to this register (applied locally, pending push). The addendum also records that the one-directional Clifford result is formally verified in Lean, in the v1.2 file `dc08bbac-primary.lean`. C-002 (persistence under doubling is guaranteed by subalgebra embedding) and C-003 (verification headline omits `native_decide` in the E₈ and 24-family theorems; the CD4–CD6 bilateral proofs are fully kernel-checked) opened. A further draft entry, "framework independence listed as Lean-verified", was withdrawn before filing: `dc08bbac-primary.lean` does verify it in the one-directional sense; the remaining wording issue was folded into the C-001 addendum. Drafts by Claude Desktop, checked against the sources by Claude Code. |

---

*Chavez AI Labs LLC — Applied Pathological Mathematics*
*Corrections are the method, not the exception.*
