# RH Investigation — Phase 78 Opening Handoff

> ⚠ **Correction pending.** §4A's prediction frames the Run C outcome as a
> binary — "growth past ~13 → the truncated signal genuinely strengthens;
> plateau → structural limit" — that omits what actually happened: z kept
> rising with no plateau, but the *per-zero* signal declined throughout
> (to 76.5% of its N=101 value by γ₃₄₀); all the z growth was the
> Monte-Carlo null tightening as 1/√N. See
> [`CORRECTIONS.md`](../../CORRECTIONS.md) C-001 and
> `docs/phases/RH_PHASE_78_RESULTS_v2.md` §5.1 for the corrected account.
> Moved into the repository 2026-09-08 (was previously outside version
> control) so this citation is verifiable. The Lean track this handoff
> opened (§3, sedenion product infrastructure, Q-16) was not started in
> Phase 78 and remains open.

**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Date:** July 11, 2026
**Prepared by:** Claude Fable 5 (Claude.ai session), from the Phase 77 record (results + continuation handoff, June 12/17, 2026) and the KSJ knowledge base (900 captures through July 7, 2026)
**For:** The next Claude session (Claude Code preferred for Lean toolchain work)
**Mission:** Open Phase 78. Primary Lean target: the sedenion product infrastructure and the Q-16 e₀-transparency theorem. Empirical targets: Run C and the newly opened Q-18 ensemble question. Paper target: v1.4 abstract.

---

## 0. What This Investigation Is

A dual-purpose open science project:

1. **A pure-mathematics assault on the Riemann Hypothesis** conducted in the Applied Pathological Mathematics framework — 16D sedenion zero-divisor algebra (the Canonical Six), the Chavez Transform, and ZDTP — formally verified in Lean 4.
2. **A showcase of CAILculator's abilities** as a high-precision (10⁻¹⁵) production MCP server. Phase 76–77 completed the arc from *empirical oracle* to *proved instrument*: every gateway output is now a machine-verified closed-form inner product, and the instrument's first genuine zero detector (Signed Gateway Channel / Detector Encoding, z = 8.42, AUC 0.87) was discovered, characterized, and live-validated against the analytical law to 10⁻¹⁵.

Principal formal result to date: **`critical_line_convergence`** — three independent standard-axiom characterizations of Re(s) = ½ (Hamiltonian vanishing, spectral containment, gateway arithmetic integrality) proved co-extensive in one machine-verified conjunction. `#print axioms` → `[propext, Classical.choice, Quot.sound]`.

---

## 1. Verified Baseline at Phase 78 Open

```
Build:          8,061 jobs · 0 errors · 1 sorry (spectral_implies_zeta_zero — by design)
Files:          17 verified Lean files (GatewayLinearLaw.lean now holds 4 theorems incl. ba_asymptote_sq)
Non-std axiom:  1 (riemann_critical_line = RH itself; appears only in riemann_hypothesis
                and eigenvalue_zero_mapping)
Branches:       phase-76-linear-law @ e1f170e   — push pending Paul's review (hard gate)
                phase-77-archaeology @ 4e740af  — push pending Paul's review (hard gate)
                (status as of June 17 record; confirm with git before assuming)
Last pushed:    phase-75-convergence @ 884f6a1 (May 12, 2026); main @ 6053cd4
CAILculator:    v2.1.4 · Engine v2.0 High-Precision · 10⁻¹⁵ · Production Stable
KSJ:            900 captures · 896 AIEX · AIEX-731–743 committed June 12 ·
                AIEX-744–749 committed June 17 · date range through July 7, 2026
Toolchain:      Lean 4 / Mathlib v4.28.0 · build project AsymptoticRigidity_aristotle/
```

**Do NOT push to GitHub without Paul's explicit review and approval.**

---

## 2. Phase 77 Final Ledger (all items confirmed in KSJ)

| Item | Verdict | Key Finding | KSJ |
|---|---|---|---|
| Q-14 encoding reconciliation | CLOSED | Gateway Linear Law reproduces every recorded Phase 73 observable on the recovered baseline vector (mean mag 35.3833, conv 0.4274, B/A 3.6591); live continuity confirmed across server versions v2.0.3→v2.1.4. Q-9/Q-10 upgraded empirical→derived. Phase 75 Q-2/Q-4 magnitude tables **quarantined** via infeasibility certificate (\|M\| ≥ 4.0311 at σ=½ for any input). | AIEX-731, 732 |
| Q-15 γₙ probe | CLOSED (negative as posed) | No γₙ signature in convergence or bilateral sandwich channels; explicit-formula control z = 6.36 proves the signal exists in the encoding and is destroyed by the even-in-c magnitude law. Architectural, not information-theoretic. | AIEX-736, 738 |
| Q-17 Signed Gateway Channel | CLOSED | c_S2 carries Bonferroni-surviving γₙ signature (z = 3.72 → 4.92 over γ₁–γ₁₀₁, sub-√N growth). Detector Encoding realizes the 6-prime explicit-formula detector exactly as c_S2 + c_S6 (residual 1.8×10⁻¹⁵). Detector: z = 8.42, AUC 0.866 (δ=0.5), precision 0.831 vs 0.433 chance. | AIEX-737, 739–742 |
| Q-8 / `ba_asymptote_sq` | CLOSED (PROVED) | B/A² → 17 as t → ∞, machine-verified limit theorem in `GatewayLinearLaw.lean` (4th theorem). Axioms: standard only. √17 = 4.1231… is the exact architectural constant; "4.0 hypothesis" superseded. | AIEX-745 |
| Run A σ-sweep | COMPLETE | `pairing_sigma_independent` confirmed live to 10⁻¹⁵: c_S2 exactly σ-blind (range 0.0 across 9 σ values), c_S6 exactly −2σ per unit step. Two structurally disjoint instruments in one server call. **This opens Q-18** (see §4). | AIEX-744 |
| Run B bilateral scan | COMPLETE (refutation) | Bilateral magnitude equality \|M(½+iγ)\| = \|M(½−iγ)\| does **NOT** hold per-gateway under the Documented F(s) Encoding (all 6 gateways, γ₁/γ₂/γ₃, nonzero at σ=½). Sedenion norm ‖F(+t)‖ = ‖F(−t)‖ IS symmetric. Bilateral difference is driven by c_g time-reversal asymmetry: \|M(+t)\|²−\|M(−t)\|² = 16·a_g·b_g. Not a critical-line probe. | AIEX-746 |
| Q-4 discrepancy | RESOLVED | Prior "proved" bilateral-equality claim was a theorem misapplication: `pairing_sigma_independent` governs *cross-gateway* differences at fixed input, not ±t pairs at one gateway. Phase 75 tables were a quarantined v2.0.4 pipeline. | AIEX-747 |
| S6 σ-sensitivity | CHARACTERIZED | S6 is the only gateway with pos2 = σ−½+0.0019 in support; σ-slope of its bilateral diff is γ-dependent; extrapolated zero-crossings all outside the critical strip. | AIEX-748 |
| Double-blind protocol | VALIDATED | Sonnet 4.6 (live MCP) and Claude Code (analytical law) executed Run B independently with consistent results — a working methodology for instrument-vs-theory cross-checks. | AIEX-749 |

**Honest accounting — what Phase 77 did NOT do:** Run C (detector at high zeros) was never executed — no script, no results JSON, no KSJ capture. The full Q-16 theorem was not attempted (infrastructure absent). `detector_channel_identity` was not implemented (awaiting Paul's call). The v1.4 abstract was not drafted.

---

## 3. Phase 78 Primary Track — Lean

### 3A. Sedenion product infrastructure (opening task, 18th file)

The entire 17-file stack operates at `EuclideanSpace ℝ (Fin 16)` level — inner products and scalar contractions only. Q-16 requires the actual sedenion product. Build `SedenionProduct.lean`:

- The 16×16×16 Cayley-Dickson structure tensor (≈50–80 lines of definitions + compatibility lemmas per the Phase 77 estimate).
- Compatibility with the existing frozen definitions (Sed, u_antisym, F, F_base — DO NOT redefine; extend).
- Ground truth for validation: `phase77_q15_convergence_probe.py` computes the sandwich residuals via the same tensor, replica-validated against the live server at 10⁻⁹ (Phase 76) and re-validated live June 12. `BilateralCollapse.lean` (companion file, Phase 18B) already encodes bilateral products for the Canonical Six — mine it for conventions before writing anything new.
- Sanity theorem before Q-16: re-derive one Canonical Six annihilation (e.g., S1: (e₁+e₁₄)·(e₃+e₁₂) = 0) from the tensor as a `decide`/`norm_num`-class check.

### 3B. Q-16 — e₀-transparency of the Canonical Six (Phase 78 headline target)

For every Canonical Six pair (P_g, Q_g) and generic x ∈ Sed:

```
e₀((x·P_g)·Q_g) = 0     e₀((P_g·x)·Q_g) = 0     ⟪x·P_g, Q_g⟫ = 0
```

This is the algebraic explanation of the Q-15 negative: the nonlinear sandwich channel contracts to zero at the e₀ slot for ALL inputs, not just at zeros. Proving it converts Phase 77's empirical null into a structural theorem — the strongest kind of negative result. Target name: `canonical_six_e0_transparency`. Standard axioms expected (pure algebra).

### 3C. `u_antisym` orthogonality companion (quick win — do first if warming up)

`u_antisym ∈ (span{P_i, Q_i : i = 1..6})⊥` — AIEX-558 flagged this as a direct inner-product computation in the current EuclideanSpace framework, no product tensor needed. AIEX-553 records the numerical fact (zero inner product with all 12 generators); AIEX-581 records why it matters (the orthogonality is the formal mechanism isolating the bilateral collapse to the critical line). Reachable in a single session.

### 3D. `detector_channel_identity` (Paul's call — surface it, don't decide it)

```lean
theorem detector_channel_identity (t : ℝ) :
    gatewayScalar (D t) 2 + gatewayScalar (D t) 6
      = -2 * ∑ p ∈ ({2,3,5,7,11,13} : Finset ℕ),
            (Real.log p / Real.sqrt p) * Real.cos (t * Real.log p)
```

Pure inner-product algebra over `GatewayLinearLaw.lean`; AIEX-743 calls it clean. Options: 5th theorem in `GatewayLinearLaw.lean` (requires defining `D t` there), a standalone `DetectorEncoding.lean`, or continued deferral. **Stack-growth decision belongs to Paul.** If the 18th file is `SedenionProduct.lean` (3A), a 19th file for this is the tidier separation. The zero-detection *statistics* remain out of Lean scope (number-theoretic).

---

## 4. Phase 78 Empirical Track — CAILculator

### 4A. Run C — Detector Encoding at high zeros (carried over, ready to execute)

- **Question:** Does the detector z-score keep growing sub-√N beyond γ₁₀₁ or plateau?
- **Protocol:** Detector Encoding (w_p·cos(t·ln p) in u₂/u₆ slots, pos2 = 0); sweep t ∈ [10, 600], Δt = 0.005 (118,001 points, ≈250 zeros); channel c_S2 + c_S6; test T1 with corrected null (fixed-minima methodology, AIEX-742).
- **Prediction:** sub-√N law gives z ≈ 8.42 × √(251/101) = 13.3 at 251 zeros. Growth past ~13 → the truncated signal genuinely strengthens; plateau → structural limit (possibly prime-log commensurability). Either result is informative.
- **Control:** run the explicit-formula scalar in parallel over the same range to check for dilution by rising zero density.
- KSJ: extract insights after the run; **never `commit_aiex` without Paul's explicit approval.**

### 4B. Q-18 — OPEN (new, unlocked by Run A)

The Phase 77 continuation handoff made Q-18 conditional on Run A confirming c_S2 σ-independence live. **Run A succeeded (AIEX-744), so Q-18 is now formally open:**

> **Q-18: Can a multi-gateway signed-channel ensemble outperform the 6-prime Detector Encoding (z = 8.42, AUC 0.866)?**

This is the first investigation-driven CAILculator run with a quantitative improvement target — the purest possible showcase framing: the instrument's proved formula (c_g = −2⟪x, u_g⟫) is used to *design* a better detector, then the live server validates the design. Candidate directions: per-gateway explicit-formula weighting across all six u_g supports; exploiting the S4/S5 sign structure (u₄, u₅ contain e₁ with mixed signs); higher prime truncations if the encoding admits them. Honest-baseline discipline (AIEX-742) applies to every performance claim.

### 4C. Fano plane visualization (carried over, ungated)

`fano_plane` illustrate type via CAILculator: Canonical Six → PG(2,2), all 4 styles, publication target for v1.4 / outreach materials.

---

## 5. Paper & Outreach Track

- **v1.4 abstract** — ungated, still the blocking item for Berry/Keating and Tao outreach. Structure (standing, per CLAUDE.md + Phase 77 doc): (1) APM introduction; (2) version record v1.0→v1.4; (3) Chavez Transform; (4) CAILculator; (5) RH Investigation with `critical_line_convergence` as centerpiece, `ba_asymptote_sq` as the Q-8 algebraic closure, and the Signed Gateway Channel / Detector Encoding as the instrument highlight. The Phase 76–77 arc gives the abstract its strongest new line: *the instrument's outputs are proved formulas, and reading them correctly (signed, not squared) turns the calculator into a zero detector.*
- Submit as a **new Zenodo record** (separate from v1.3, DOI 10.5281/zenodo.17402495).
- Drafting is in scope for autonomous work; **sending anything outward is not — all outward-facing actions go through Paul.**

---

## 6. Cross-Project Intelligence (KSJ, June 24 – July 7)

Two IGP24-era captures are directly relevant to Phase 78 framing and should be considered when writing the v1.4 narrative:

- **AIEX-857 (July 5) — the spinor inversion, Paul's intuition, cross-project:** RH Phase 43 promoted σ = ½ from boundary condition to the fixed scalar of a double-valued object; IGP24 v33 performed the identical inversion on its own problem. The same APM move working in two unrelated domains is evidence the move is methodological, not coincidental — a v1.4 introduction theme.
- **AIEX-810 (June 24):** the IGP24 r=20/22 barren strip read as geometric forcing — a "sideways critical strip" echoing the Riemann strip. Speculative; log it as color, not as a claim.
- **AIEX-754 (June 19):** ZDTP ramification-filter hypothesis (bilateral scores vs discriminant complexity in degree-24 polynomials) — untested; a possible future CAILculator-showcase experiment bridging the two projects. Not Phase 78 scope.

---

## 7. Standing Orders (unchanged — non-negotiable)

1. **Axiom discipline:** `riemann_critical_line` is the sole non-standard axiom. Never discharge it — no tactic, no `sorry`, no `native_decide`. Zero new axioms without Paul's explicit approval.
2. **Sorry count:** exactly 1 (`spectral_implies_zeta_zero`, boundary condition, by design — the pointwise converse is mathematically false). Never close it.
3. **Files 1–16: DO NOT MODIFY.** File 17 (`GatewayLinearLaw.lean`) and new files 18+ are the active zone.
4. **GitHub:** local commits fine, phases may accumulate; **no push without Paul's explicit review.** Prepare push-ready summaries instead.
5. **KSJ:** `extract_insights` → Paul approves → `commit_aiex`. Never auto-commit (violation precedent: AIEX-627, May 5).
6. **Lean verification:** local build first, in-shell (Claude Code); Aristotle is fallback for genuine blockage only. Gemini CLI is not used for Lean (documented Mathlib v4.28.0 lemma-name drift).
7. **Encoding discipline:** Phase 76 Documented F(s) Encoding for all comparable CAILculator work; the Detector Encoding is a documented purpose-built deviation. Cross-phase magnitude comparisons cite Phase 76+ runs only (Phase ≤75 magnitude tables quarantined).
8. **Honest status lines:** state exactly what is verified, by whom, when — never claim a build count before a clean local build.
9. Frozen definitions (Sed, u_antisym, F, F_base, sedenion_Hamiltonian, ROOT_16D) stay frozen; `mirror_op` is NOT an automorphism; `n20k_calibration` was a false axiom — never reintroduce either.
10. **Outward-facing actions go through Paul.** Approved closing line for results documents only: *Better math, less suffering.*

---

## 8. Quick Reference

**Gateway Linear Law (all proved, standard axioms):**
```
gatewayScalar x g = −2⟪x, P_g + Q_g⟫
gatewayMagSq x σ g = ‖x‖² + 4·c_g² + 16·(2σ)²
gateway_magSq_sub · gateway_pairing_iff · pairing_sigma_independent · ba_asymptote_sq (→17)
```

**Scope warning (Run B lesson):** `pairing_sigma_independent` is about *cross-gateway* magnitude differences at a fixed input. It does NOT imply bilateral (±t) equality at a single gateway — that claim was refuted June 17. The time-reversal-symmetric quantity is the sedenion norm ‖F(+t)‖ = ‖F(−t)‖.

**Canonical Six pair sums:** S1: e₁+e₁₄+e₃+e₁₂ · S2: e₃+e₁₂+e₅+e₁₀ · S3: e₄+e₁₁+e₆+e₉ · S4: e₁−e₁₄+e₃−e₁₂ · S5: e₁−e₁₄+e₅+e₁₀ · S6: e₂−e₁₃+e₆+e₉
Class B = {S1, S4, S5} (contain e₁, the t-slot) · Class A = {S2, S3, S6}

**Documented F(s) Encoding (comparability standard):** pos0 = σ · pos1 = t · pos2 = σ−½+0.0019 (load-bearing) · pos3–13 = prime oscillators (2,3,5,7,11,13) · pos14 = pos15 = 0.

**Detector Encoding (purpose-built):** pos2 = 0; u₂ slots (3,5,10,12) ← w_p·cos(t·ln p), p ∈ {2,3,11,13}; u₆ slots (6,9,13; pos2 zeroed) ← p ∈ {5,7}; w_p = log p/√p. Identity: c_S2 + c_S6 = −2·Σₚ(log p/√p)cos(t·log p), residual 1.8×10⁻¹⁵.

**Detector performance baseline to beat (Q-18):** z = 8.42 · AUC 0.866 (δ=0.5) · precision 0.831 vs 0.433 chance, over γ₁–γ₁₀₁.

**Key constants:** γ₁ = 14.134725141734695 · γ₂ = 21.022039638771555 · γ₃ = 25.010857580145688 · B/A → √17 = 4.123105625… · mean-magnitude growth (3√17+3)/6 = 2.5616·γₙ · conv asymptote 0.3904 · \|M\| floor at σ=½: 4.0311.

---

## 9. Suggested Sequencing

1. **§3C** `u_antisym` orthogonality companion — one-session Lean win, closes AIEX-558's open question, warms up the toolchain.
2. **§3A** `SedenionProduct.lean` infrastructure + annihilation sanity theorem — the Phase 78 foundation.
3. **§3B** Q-16 `canonical_six_e0_transparency` — the headline.
4. **§4A** Run C in parallel (empirical track, independent of Lean work).
5. **§5** v1.4 abstract draft alongside — it unblocks outreach and nothing gates it.
6. Surface **§3D** (detector lemma placement) and the pending GitHub pushes to Paul at first opportunity.

---

*Chavez AI Labs LLC — Applied Pathological Mathematics*
*Phase 78 Opening Handoff · July 11, 2026*
