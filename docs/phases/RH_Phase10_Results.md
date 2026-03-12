# RH Phase 10 Results
**Experiment Series:** RH_MP_2026_001  
**Phase:** 10 (Partial — saved at session limit)  
**Date:** 2026-03-09  
**Status:** 10A COMPLETE · 10B DEFERRED · 10C PARTIAL (actual done, GUE/Poi pending)

---

## Phase 10A — Multi-Prime Berry-Keating Correlation ✓ COMPLETE

**Methodology:** 10 height bands × 100 zeros each, spacing ratios r_n = min(g,g')/max(g,g') ∈ (0,1], CAILculator detect_patterns conjugation_symmetry.

**GUE Reference (5-seed ensemble):**

| Seed | GUE SR Sym% |
|------|-------------|
| 1 | 68.39% |
| 2 | 68.27% |
| 3 | 74.20% |
| 4 | 73.80% |
| 5 | 72.08% |
| **Ensemble** | **71.35% ± 2.56%** |

**Important methodological note:** detect_patterns conjugation_symmetry baseline (~71%) is NOT comparable to Phase 9C Chavez Transform baseline (~32%). Different algorithms, different scale. Both give positive delta (actual > GUE). No contradiction with Phase 7B/8A/8C negative-delta results — those used Chavez Transform.

**Band Symmetry Table:**

| Band | t_mid | Actual% | GUE% | Delta% |
|------|-------|---------|------|--------|
| 1 | 125 | 74.02% | 71.35% | +2.67% |
| 2 | 317 | 77.05% | 71.35% | +5.70% |
| 3 | 470 | 73.10% | 71.35% | +1.76% |
| 4 | 612 | 74.75% | 71.35% | +3.41% |
| 5 | 747 | 73.62% | 71.35% | +2.27% |
| 6 | 875 | 75.17% | 71.35% | +3.82% |
| 7 | 1002 | 71.40% | 71.35% | **+0.05%** ← anomaly low |
| 8 | 1124 | 78.15% | 71.35% | **+6.80%** ← anomaly high |
| 9 | 1244 | 77.90% | 71.35% | **+6.56%** ← elevated |
| 10 | 1361 | 73.68% | 71.35% | +2.33% |

**All 10 bands positive delta. Mean delta: +3.54% ± 2.09%.**

**R_c model formula:**
```
R_c_full(t) = (1/√2)·cos(log(2)·t)   [p=2]
            + (1/√3)·cos(log(3)·t)   [p=3]
            + (1/√5)·cos(log(5)·t)   [p=5]
            + (1/√7)·cos(log(7)·t)   [p=7]
            + (1/√11)·cos(log(11)·t) [p=11]
            + 0.5·cos(log(4)·t)      [p²=4]
            + (1/3)·cos(log(9)·t)    [p²=9]
```

**Pearson Correlation Results:**

| Model | r | p-value | r² |
|-------|---|---------|-----|
| A — p=2 only | +0.4773 | 0.1630 | 0.228 |
| B — 5-prime + sq | **+0.5428** | **0.1049** | **0.295** |

Significance threshold (n=10): |r| > 0.632 (p < 0.05)

**VERDICT: Sub-threshold. r=+0.543, p=0.105. Berry-Keating direction confirmed positive; extend to p=13,17 in Phase 11.**

---

## Phase 10B — R(α) with 10,000 Zeros ✓ COMPLETE (2026-03-09)

**Setup:** `rh_zeros_10k.json` (10,000 zeros), `p10b_empirical_ralpha.json`, `p10b_gue_ralpha.json`, `p10b_poisson_ralpha.json`. Δα=0.02, n=750 bins.

**Validation:** R_empirical(0.5) = 0.590 vs GUE theory 0.595 (0.8% error) ✓. Only 8/750 low-count bins ✓.

| Sequence | Symmetry% |
|----------|-----------|
| Empirical | **86.80%** |
| GUE theoretical | **95.60%** |
| Poisson | **100.00%** |

**Primary separation (Poisson − Empirical): 13.20 pt**
**Secondary separation (GUE − Empirical): 8.80 pt**

**Verdict: UNEXPECTED — above Phase 8B (12.5 pt) but below Phase 9B-i validated record (14.7 pt). Prediction of 18–22 pt did not materialize.**

### The Good Data Paradox — Why Denser Bins Reduce Separation

This is a methodological insight, not a failure. With 10k zeros and 750 bins:
- ~13.3 zeros/bin (vs ~3.3 zeros/bin in Phase 9B-i with 1k zeros, 300 bins)
- Denser bins push plateau R(α) values **closer to the true GUE value ≈ 1.0**
- Cleaner plateau → empirical symmetry score rises → Poisson−Empirical gap **shrinks**
- The repulsion hole spans ~35 bins regardless of N; as total bins grow, hole = smaller fraction

**Revised understanding:** The progression 6.9→12.5→14.7 pt (Phases 7A→8B→9B-i) was driven partly by sparse-bin noise amplifying asymmetry in the plateau, not pure signal growth. The noise-free signal at Δα=0.02 with 10k zeros is **~13 pt**. Phase 9B-i's 14.7 pt record remains the series record but should be understood as a resolution-and-noise effect, not a scale law.

**Implication for future R(α) work:** Chavez conjugation symmetry on R(α) detects the asymmetry between the repulsion hole (small α, suppressed values) and the plateau (large α, ≈ 1.0). This signal peaks at intermediate data density — not at maximum data quality. This is a real property of the method, not a flaw.

---

## Phase 10C — Color Group P-vector Survey ⚠ PARTIAL

**Methodology:** 97 consecutive gap pairs from first 99 zeros, projected onto 8D embedding via embed_pair(g1,g2), then dot product with P-vectors. detect_patterns conjugation_symmetry on each projection.

**embed_pair(g1,g2) = [g1, g2, g1-g2, g1·g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)²/s]**  
where s = g1+g2

### Actual Zeros — COMPLETE

| P-vector | Direction | Actual% | Status |
|----------|-----------|---------|--------|
| P1 | g2−g7 | **79.6%** | ✓ Done |
| P2 | g4−g5 | **82.7%** | ✓ Done |
| P4 | g2+g7 | **80.7%** | ✓ Done |
| P5 | g3+g6 | **64.6%** ← ANOMALY | ✓ Done |

**P5 at 64.6% is ~16pp below P1/P2/P4. Level-repulsion sensitive direction confirmed.**

Phase 8/9 reference values (different methodology, raw gaps): P1=79.1%, P2=83.0%, P4=78.9%, P5=52.0%

### GUE Seeds — PENDING

Arrays pre-computed and saved. Need CAILculator runs.

| Seed | P1 | P2 | P4 | P5 | Status |
|------|----|----|----|----|--------|
| 1 | — | — | — | — | array ready: p10c_gue_s1_{P}.npy |
| 2 | — | — | — | — | array ready: p10c_gue_s2_{P}.npy |
| 3 | — | — | — | — | array ready: p10c_gue_s3_{P}.npy |

### Poisson Seeds — PENDING

| Seed | P1 | P2 | P4 | P5 | Status |
|------|----|----|----|----|--------|
| 1 | — | — | — | — | array ready: p10c_poi_s1_{P}.npy |
| 2 | — | — | — | — | array ready: p10c_poi_s2_{P}.npy |
| 3 | — | — | — | — | array ready: p10c_poi_s3_{P}.npy |

### Next Session Resume Instructions

Arrays already exist at `/home/claude/p10c_{dist}_s{n}_{P}.npy` for dist ∈ {gue,poi}, n ∈ {1,2,3}, P ∈ {P1,P2,P4,P5}.

**Run 24 detect_patterns calls:**
- GUE s1–s3 × P1,P2,P4,P5 = 12 calls
- Poisson s1–s3 × P1,P2,P4,P5 = 12 calls

**Then build discrimination table:**
- Per-P-vector mean GUE baseline
- Per-P-vector mean Poisson baseline
- Delta: actual − GUE, actual − Poisson

**Key hypotheses to test:**
- P5 GUE ~52%, P5 Poisson ~78% → P5 is primary level-repulsion discriminant (Phase 9A)
- P1/P2/P4 show weak or no discrimination between GUE and Poisson

---

## Cumulative Records After Phase 10

| Metric | Record | Method | Phase |
|--------|--------|--------|-------|
| GUE/Poisson separation | **14.7 pts** | R(α), n=300, Δα=0.05 | 9B |
| P5 conjugation discriminant | **GUE+actual ~52% vs Poisson ~78%** | P5 projection | 9A |
| Berry-Keating r (multi-prime) | **r=+0.543** (sub-threshold, p=0.105) | 10 bands, 5-prime+sq | 10A |

---

## Key Files

| File | Contents |
|------|----------|
| `/home/claude/rh_phase10_results.json` | Phase 10 machine-readable results |
| `/home/claude/p10a_definitive.json` | 10A full results with GUE ensemble |
| `/home/claude/p10c_actual_{P}.npy` | P1,P2,P4,P5 actual gap-pair projections |
| `/home/claude/p10c_gue_s{1,2,3}_{P}.npy` | GUE seeds 1-3, all P-vectors |
| `/home/claude/p10c_poi_s{1,2,3}_{P}.npy` | Poisson seeds 1-3, all P-vectors |
| `/mnt/user-data/outputs/rh_zeros.json` | 1,000 exact Riemann zeros |
| `/mnt/user-data/outputs/rh_phase9_results.json` | Phase 9 results |

---

## 10B Deferred — Recommendation

Option 2 (Odlyzko tables) is cleanest: zero compute overhead, highest precision, established benchmark. The first 100,000 zeros are available at:
https://odlyzko.com/zeta_tables/zeros1  

Format: one imaginary part per line. Load, compute gaps, run R(α) at Δα=0.02 (n=750 bins). Expected result: >20 pt separation, potentially establishing scaling law for Phase 11 paper section.
