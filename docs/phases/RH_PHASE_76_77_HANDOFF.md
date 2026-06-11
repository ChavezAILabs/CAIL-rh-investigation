# RH Investigation — Phase 76 Close / Phase 77 Handoff
**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Prepared:** June 11, 2026 (Claude Fable 5, Claude Code session — on instruction from Paul Chavez)
**For:** The next Claude Fable 5 session (Claude Code)
**Mandate:** Phase 77 is handed to Fable in full, with permission to continue into subsequent phases on promising leads (Paul, June 11, 2026). See §6 for the guardrails that bound this mandate.

---

## 0. Read-First State Summary

- **Phase 76 Parts A+B are COMPLETE** (June 10, 2026, Fable-led in Claude Desktop): the **Gateway Linear Law** — c_g(x) = −2⟪x, P_g+Q_g⟫, |M_g|² = ‖x‖² + 4(c_g² + 4(2σ)²) — validated 22/22 against CAILculator v2.1.4 to 10⁻¹⁵ and proved symbolically in exact arithmetic. Q-5 CLOSED (negative), Q-3 closed for the magnitude channel, Q-6/γ₄ RESOLVED (no zero lock), Q-8 CLOSED (asymptote = √17 exactly; 4.0 superseded).
- **The verified Lean stack is unchanged from Phase 75:** 16 files · 8,059 jobs · 0 errors · 1 sorry (`spectral_implies_zeta_zero`, by design) · 1 non-standard axiom (`riemann_critical_line` = RH). `GatewayLinearLaw.lean` (17th file) is written but **UNVERIFIED** — verifying it is your first task.
- **Canonical status document:** `C:\dev\projects\Experiments_January_2026\Primes_2026\PROJECT_STATUS-v13.md` (June 11, 2026). Read it before starting. CLAUDE.md has had its workflow rules patched (June 11) but its quick-state content is stale (Phase 75-era) — updating it is Task 3c below.
- **Workflow changes you must honor (June 11, 2026):**
  1. **You verify Lean locally in the shell.** Aristotle is fallback only (escalate on genuine blockage, not first failure).
  2. **No GitHub push without Paul's explicit review — ever.** Local commits are fine, including multiple closed phases accumulating locally.
- **Tooling:** `cailculator` and `ksj` MCP servers are registered in Claude Code (user scope) and were live as of June 11. If `mcp__cailculator__*` / `mcp__ksj__*` tools are not visible, restart the session.

---

## 1. Directory and File Map

| What | Path |
|---|---|
| Project root | `C:\dev\projects\Experiments_January_2026\Primes_2026\` |
| Repo (git) | `C:\dev\projects\Experiments_January_2026\Primes_2026\CAIL-rh-investigation\` |
| Canonical Lean source (files 1–16) | `CAIL-rh-investigation\lean\` |
| Active build project | `C:\dev\projects\Experiments_January_2026\Primes_2026\AsymptoticRigidity_aristotle\` |
| Phase docs | `CAIL-rh-investigation\docs\phases\` |
| Scripts | `CAIL-rh-investigation\scripts\` |
| Results data | `CAIL-rh-investigation\results\` |
| Project instructions | `C:\dev\projects\Experiments_January_2026\Primes_2026\CLAUDE.md` |
| Status document (current) | `C:\dev\projects\Experiments_January_2026\Primes_2026\PROJECT_STATUS-v13.md` |
| Persistent memory | `C:\Users\chave\.claude\projects\C--dev-projects-Experiments-January-2026-Primes-2026\memory\` |
| Legacy (IGNORE) | `rh_investigation\` — superseded |

**Phase 76 artifacts — all recovered and currently at PROJECT ROOT, not yet in the repo** (destination on staging):

| File (at `C:\dev\projects\Experiments_January_2026\Primes_2026\`) | Destination |
|---|---|
| `RH_PHASE_76_RESULTS.md` — canonical phase results | `CAIL-rh-investigation\docs\phases\` |
| `RH_PHASE_76_PART_A_RESULTS.md` — Part A full tables | `CAIL-rh-investigation\docs\phases\` |
| `RH_PHASE_76_HANDOFF_PART_A.md` | `CAIL-rh-investigation\docs\phases\` |
| `RH_PHASE_76_HANDOFF_PART_B.md` | `CAIL-rh-investigation\docs\phases\` |
| `GatewayLinearLaw.lean` — 17th stack file, UNVERIFIED | `CAIL-rh-investigation\lean\` (canonical) + copy to `AsymptoticRigidity_aristotle\` (build) |
| `LEAN4_HANDOFF_PHASE76_LINEARLAW.md` — verification handoff (renamed from ARISTOTLE_HANDOFF by Paul, June 11 — you execute it locally) | `CAIL-rh-investigation\lean\` |
| `phase76_partA_vectors.py` — documented-encoding vector generator | `CAIL-rh-investigation\scripts\` |
| `phase76_zdtp_replica.py` — exact validated ZDTP replica | `CAIL-rh-investigation\scripts\` |
| `phase76_partA_run.py` — Part A campaign execution | `CAIL-rh-investigation\scripts\` |
| `phase76_partB_symbolic.py` — exact symbolic proofs (sympy) | `CAIL-rh-investigation\scripts\` |
| `phase76_partA_results.json` — full numeric record | `CAIL-rh-investigation\results\` |
| `RH_PHASE_76_77_HANDOFF.md` — this document | `CAIL-rh-investigation\docs\phases\` |

(Artifact recovery note: the replica/run scripts and results JSON originated in the Claude Desktop session and were exported to the project root by Paul on June 11 — the artifact list in `RH_PHASE_76_PART_A_RESULTS.md` §6 is now fully satisfied. Raw server transcripts remain in the Desktop chat; archive on staging if Paul exports them, otherwise note their location in the commit message.)

---

## 2. Task 1 — Lean 4 Verification of `GatewayLinearLaw.lean` (local, in-shell)

The full verification protocol, robust proof alternates, and constraints are in `LEAN4_HANDOFF_PHASE76_LINEARLAW.md`. Execute it yourself in the shell. Condensed sequence:

```powershell
# 0. Place files
#    Copy GatewayLinearLaw.lean from project root → CAIL-rh-investigation\lean\ (canonical)
#    and → AsymptoticRigidity_aristotle\ (build copy)

# 1. Register the new target in AsymptoticRigidity_aristotle\lakefile.toml:
#    - add "GatewayLinearLaw" to defaultTargets
#    - add a [[lean_lib]] entry: name = "GatewayLinearLaw", globs = ["GatewayLinearLaw"]

# 2. Add to AsymptoticRigidity_aristotle\axiom_check.lean:
#    import GatewayLinearLaw
#    #print axioms gateway_pairing_iff
#    #print axioms gateway_magSq_sub
#    #print axioms pairing_sigma_independent

# 3. Build (project-local .lake on C:; D: drive removed from workflow — unreliable)
cd 'C:\dev\projects\Experiments_January_2026\Primes_2026\AsymptoticRigidity_aristotle'
lake exe cache get
lake build

# 4. Axiom audit
lake env lean axiom_check.lean
```

**Acceptance criteria:** 0 errors · sorry count unchanged at 1 (`spectral_implies_zeta_zero` only) · all three new theorems print exactly `[propext, Classical.choice, Quot.sound]` · `riemann_hypothesis` footprint unchanged at `[propext, riemann_critical_line, Classical.choice, Quot.sound]`. Record job count, error count, sorry count, and `#print axioms` output **verbatim**.

**If proofs resist** (in order):
- `gateway_pairing_iff`: the file's `nlinarith` proof may stall — use the robust route in the handoff: `rw [← sub_eq_zero, gateway_magSq_sub, mul_eq_zero]` then `simp [(by norm_num : (16:ℝ) ≠ 0)]` (requires `gateway_magSq_sub` placed before it in the file). `set_option maxHeartbeats 800000` if needed.
- Inner-product rewrites: try `real_inner_sub_right` / `real_inner_add_right` variants if `inner_sub_right`/`inner_add_right` resist elaboration.
- `ba_asymptote_sq` (stretch goal): attempt only after the three core theorems pass; if it does not close cleanly, defer to Phase 77 — **do NOT introduce a sorry**.
- Escalate to Aristotle only if genuinely blocked after exhausting the alternates. When uploading to Aristotle, ALWAYS include the full 138-line `UniversalPerimeter.lean` from `CAIL-rh-investigation\lean\` (their cached copy is a stub).

**Standing Mathlib v4.28.0 traps** (history says you will hit some of these):
- `EuclideanSpace.norm_sq_eq_inner` and `EuclideanSpace.inner_def` are ABSENT — banned. Canonical pattern: `real_inner_smul_left` → `real_inner_self_eq_norm_sq` → `ring`.
- `starRingEnd ℂ 2 = 2` does not close by plain `simp` — prove via `apply Complex.ext <;> simp [Complex.conj_re, Complex.conj_im]` then `rw`.
- `Nat.cast_pos.mpr` leaves `Nontrivial ?m` stuck — pin the type with `exact_mod_cast` first.
- `EulerAudit.lean` has 6 commented-out `#check` lines for absent identifiers — they must STAY commented if cache invalidation recompiles `EulerProductBridge.lean`.
- `isSpectralPoint` is a `def`, not `abbrev` — explicit `unfold` needed in `refine` goal positions.
- PowerShell `tee` writes UTF-16 LE and corrupts build logs — use `Out-File -Encoding utf8`, or rely on `lake env lean axiom_check.lean` as the definitive audit.
- Lean 4 `↔` is right-associative — never chain `↔` for 3+ propositions; use `∧` of biconditionals.

---

## 3. Task 2 — Update `RH_PHASE_76_RESULTS.md` with Lean status

File: `C:\dev\projects\Experiments_January_2026\Primes_2026\RH_PHASE_76_RESULTS.md`

After verification succeeds, update (keep the honest-status-line discipline — state exactly what was verified, by whom, when):

1. **Executive summary (end of ¶4):** replace the "ships UNVERIFIED-PENDING-ARISTOTLE … does not claim a verified build count" sentence with the actual outcome: verified locally by Claude Fable 5 in-shell on [date], new build baseline [N jobs · 0 errors · 1 sorry · 1 non-standard axiom].
2. **§4 table:** change each "written, pending Aristotle" → "✅ proved (verified locally, [date])"; record the `ba_asymptote_sq` outcome honestly (proved / deferred to Phase 77).
3. **§4 "Honest status line":** update to the new verified baseline (17 files) with the verbatim `#print axioms` results.
4. **§1 Workflow Record:** append a row: local Lean verification (Fable, in-shell — June 11 workflow revision; Aristotle not needed / needed because X).
5. **§5 table:** mark the "Aristotle verification" row done and reword to "local verification" (the row predates the June 11 local-first revision).
6. Fix the handoff filename reference: the results doc cites `ARISTOTLE_HANDOFF_PHASE76_LINEARLAW.md`; the actual file is `LEAN4_HANDOFF_PHASE76_LINEARLAW.md` (renamed by Paul, June 11, intentionally — reflects local-first verification).

If verification FAILS and cannot be repaired in-session: do NOT update the doc to claim success; record the failure mode in the doc's honest status line, escalate per Task 1, and leave the verified baseline at Phase 75.

Then mirror the outcome into `PROJECT_STATUS-v13.md` (Quick State row 76, Technical Baseline, stack table row 17, action items) — or write v14 if Phase 77 work has also landed by then.

---

## 4. Task 3 — Remaining Phase 76 Close-Out Items

a. **Stage for GitHub (commit locally — DO NOT PUSH):** move the root artifacts to their destinations per the §1 table, create a phase branch following the established naming (`phase-76-linear-law`), commit with an accurate message. **The push itself requires Paul's explicit review — hard gate, no exceptions, regardless of how many phases accumulate.** Prepare a push-ready summary for Paul instead.
b. **Update CLAUDE.md** quick-state to Phase 76: phase table row, key findings (Gateway Linear Law; Q-5 negative; Q-8 = √17 supersedes 4.0; E₈/Fano explains partition not ratio; new build baseline once verified), action items, 17-file stack table. The workflow rules were already patched June 11 — don't regress them.
c. **KSJ extraction approval:** Phase 76 `extract_insights` output and AIEX-646/647 (Phase 75) are still pending Paul's explicit approval. If Paul is present in-session, surface them; NEVER call `commit_aiex` without his explicit approval.
d. **Memory:** update `project_phase76_status.md` and the `MEMORY.md` index (paths in §1) when verification lands.

---

## 5. Task 4 — Phase 77 (proceed as documented; you have the lead)

Open questions, from `RH_PHASE_76_RESULTS.md` §5 and `PROJECT_STATUS-v13.md`:

| ID | Question | Suggested path |
|---|---|---|
| **Q-14** | Reconcile the Phase 73–75 baseline encoding constants with the Phase 76 documented encoding; re-derive the Phase 75 pairing (S1=S2, S3=S6, S4=S5) and the t=20 collapse as explicit functional conditions | Recover the original generator from the pipeline archive (check `CAIL-rh-investigation\scripts\` and Phase 73–75 docs in `docs\phases\`); apply the pairing criterion ⟪x,u_g−u_h⟫⟪x,u_g+u_h⟫ = 0 |
| **Q-15** | Does the *convergence/bilateral-annihilation* channel (vs. the now-understood magnitude channel) carry a genuine γₙ signature? | Design a CAILculator protocol isolating the verification layer; you have `mcp__cailculator__zdtp_transmit` + `verify_bilateral_oracle` directly in-session. RHI profile. Phase 76 Documented Encoding (`phase76_partA_vectors.py`) or explicitly document deviations |
| **Q-16** | Lean formalization of the sedenion orthogonality theorem (e₀-transparency of the Canonical Six: e₀((x·P_g)·Q_g) = e₀((P_g·x)·Q_g) = ⟪x·P_g, Q_g⟫ = 0 for generic x) | Requires formalizing the sedenion product (stack currently works at EuclideanSpace level) — natural companion to `canonical_six_fano_correspondence` (motivation revised: explains the Class A/B partition, i.e. which u_g contain e₁ — not the ratio value) |
| Q-12 | Gateway ↔ eigenvalue functional-calculus bridge | Exploratory; sedenion non-associativity makes this genuinely hard. Low priority |

**Also live, not CAILculator/Lean:** the **v1.4 paper abstract** — gate long cleared, and it blocks the Berry/Keating and Tao outreach emails. Structure per CLAUDE.md: (1) APM introduction ("Discovery, verification and deployment as the APM way of life"); (2) version record v1.0→v1.4; (3) Chavez Transform; (4) CAILculator; (5) RH Investigation with `critical_line_convergence` as centerpiece. The Gateway Linear Law strengthens the narrative: the 2σ Gateway Integer Law (Phase 74, RH-independent Lean theorem) is now visibly the live mechanism inside the instrument (Phase 76). Drafting the abstract is in scope for autonomous work; **sending outreach emails is not — outward-facing communications go through Paul.**

**Sequencing recommendation:** Task 1 (verification) → Task 2 (results update) → Task 3a–b (staging + CLAUDE.md) in one sitting — they're coupled. Then Phase 77 proper: Q-14 first (archaeology that de-risks every future CAILculator claim), Q-15 second (the most promising empirical lead — if the convergence channel DOES carry a γₙ signature, that's the Phase 77 headline), Q-16 + v1.4 abstract as the formal/writing track in parallel. You have continue-phases permission: if Q-15 returns something real, follow it.

**Conventions:** one results doc per phase (`RH_PHASE_NN_RESULTS.md`), handoffs as needed, all eventually in `docs\phases\`. KSJ consultation (`mcp__ksj__get_stats`, `search_captures`) at phase open is standing practice. Phase 76 tags were `#phase-76-pairing` / `#phase-76-linear-law`; continue the pattern for 77.

---

## 6. Guardrails (bound the autonomy mandate — non-negotiable)

1. **No GitHub push without Paul's explicit review.** Local commits fine, multiple phases accumulating locally fine. Present push-ready summaries; never run `git push`.
2. **KSJ:** `extract_insights` → route to Paul for explicit approval → only then `commit_aiex`. Never auto-commit. (Violation precedent: AIEX-627, May 5.)
3. **Axiom discipline:** zero new axioms. Never discharge `riemann_critical_line` — it IS the Riemann Hypothesis; no tactic, no `sorry`, no `native_decide`. Never close the by-design sorry in `spectral_implies_zeta_zero` (the pointwise converse is mathematically false).
4. **Files 1–9 of the stack: DO NOT MODIFY.** Files 10–12: only for critical-error correction. Files 13–17: active zone.
5. **Honest status lines:** never claim a verified build count before a clean local build; state exactly what is verified and what is pending, every document, every time.
6. **Key definitions are frozen** (Sed, u_antisym, F, F_base, sedenion_Hamiltonian, ROOT_16D prime roots) — see CLAUDE.md "Key Definitions (DO NOT CHANGE)".
7. **Encoding discipline:** Phase 76 Documented F(s) Encoding for all CAILculator work, or explicitly document deviations. Cross-phase absolute magnitudes are not comparable until Q-14 closes.
8. **`mirror_op` is NOT an algebra automorphism; `n20k_calibration` was a false axiom** — never re-introduce either (CLAUDE.md Critical Non-Obvious Facts #6–7).
9. **Outward-facing actions** (emails, X posts, Zenodo, anything public) go through Paul.
10. **Approved closing line for results documents, only:** *Better math, less suffering.*

---

## 7. Quick Reference — Numbers You'll Need

- Verified baseline (Phase 75): **8,059 jobs · 0 errors · 1 sorry · 1 non-standard axiom** — commit `884f6a1`, branch `phase-75-convergence`; repo `main` is at `6053cd4`.
- Expected post-verification: ~8,061 jobs (each new file historically adds ~2), same sorry/axiom counts.
- Gateway Linear Law: c_g(x) = −2⟪x, u_g⟫ · |M_g|² = ‖x‖² + 4(c_g² + 4(2σ)²) · pairing ⟺ ⟪x,u_g−u_h⟫⟪x,u_g+u_h⟫ = 0 · B/A → √17 = 4.123105625…
- Canonical Six pair sums (`gatewaySum` in the Lean file): S1: e₁+e₁₄+e₃+e₁₂ · S2: e₃+e₁₂+e₅+e₁₀ · S3: e₄+e₁₁+e₆+e₉ · S4: e₁−e₁₄+e₃−e₁₂ · S5: e₁−e₁₄+e₅+e₁₀ · S6: e₂−e₁₃+e₆+e₉
- Class partition: B = {S1, S4, S5} (u_g contains e₁, the t-slot) · A = {S2, S3, S6}
- KSJ stood at 734 captures at Phase 76 open; AIEX-646/647 + Phase 76 extraction pending approval.
- CAILculator v2.1.4 · ZDTP v2.0 · profile RHI (spectral) / Quant (algebraic identity only) · γ₄ = 21.022040 · Odlyzko γ₂₁–γ₂₆: 79.337375, 82.910381, 84.735493, 87.425275, 88.809111, 92.491899.

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering.*
*Phase 76/77 Handoff · June 11, 2026*
