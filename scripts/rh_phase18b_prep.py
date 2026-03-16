"""
RH Phase 18B ? Three-Gap Layer Structure: Vector Part & n-Gap Generalization
=============================================================================
Three sub-experiments extending the Phase 17 three-gap sedenion discovery.

Background:
  Phase 17 found that the scalar part (component 0) of the sedenion product
  x_n * x_{n+1} gives Act/GUE variance ratio = 1.02 (matches GUE), while
  the two-gap embed_pair P2 variance ratio = 0.65 (actual tighter than GUE).
  This layer structure is Phase 18B's focus.

Sub-experiments:
  18B-i  : All 16 sedenion product components ? Act/GUE for each
           + log-prime DFT SNR for each component
           + octonion-inherited (e1-e7) vs sedenion-only (e8-e15) boundary analysis
  18B-ii : n-gap generalization ? sweep k=1..8 to find the transition point
           Formula: s_n^(k) = g_{n+floor(k/2)} * sum(other k-1 gaps)
           NOTE: k=2 product formula (g_n*g_{n+1}) is NOT the same statistic as
           Phase 10C embed_pair P2 = -(g1^2+g2^2)/(2*(g1+g2)). The 0.65 result
           belongs to the P2 formula. Both are computed for comparison; they are
           different statistics from different families.
  18B-iii: Height window stability ? does Act/GUE=1.02 hold across zero heights?
           Phase 12A showed two-gap ratio is HEIGHT-DEPENDENT. If three-gap is
           height-STABLE, that is a qualitatively stronger result: matching GUE
           at three-gap scale is universal, not a window artifact.

Data required: rh_zeros_10k.json, rh_gaps_10k.json
"""

import json, math, random, os

script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# Shared infrastructure
# ============================================================================

def load_json(fname):
    with open(os.path.join(script_dir, fname)) as f:
        return json.load(f)

def var(seq):
    if len(seq) < 2:
        return 0.0
    mu = sum(seq) / len(seq)
    return sum((x - mu) ** 2 for x in seq) / len(seq)

def mean(seq):
    return sum(seq) / len(seq) if seq else 0.0

# Cayley-Dickson multiplication (recursive, works for any 2^n dimension)
def cd_conj(v):
    return [v[0]] + [-x for x in v[1:]]

def cd_mul(a, b):
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    c1 = [x + y for x, y in zip(cd_mul(a1, b1), [-x for x in cd_mul(cd_conj(b2), a2)])]
    c2 = [x + y for x, y in zip(cd_mul(b2, a1), cd_mul(a2, cd_conj(b1)))]
    return c1 + c2

def sed(indices_signs, n=16):
    v = [0.0] * n
    for idx, sign in indices_signs.items():
        v[idx] = float(sign)
    return v

# Pattern 1: P1 = e1+e14, Q1 = e3+e12  (sedenion basis 0-indexed)
P1 = sed({1: +1, 14: +1})
Q1 = sed({3: +1, 12: +1})

def gue_gaps(n, mean_gap, rng):
    """Generate GUE-distributed gaps (Wigner surmise approx)."""
    scale = mean_gap * math.sqrt(2.0 / math.pi)
    gaps = []
    while len(gaps) < n:
        u = rng.random()
        if u > 0:
            gaps.append(scale * math.sqrt(-2 * math.log(u)))
    return gaps[:n]

def poisson_gaps(n, mean_gap, rng):
    """Generate Poisson-distributed gaps (exponential)."""
    return [-mean_gap * math.log(rng.random() or 1e-300) for _ in range(n)]

# Load data
print("Loading zero and gap data...")
zeros = load_json('rh_zeros_10k.json')
gaps  = load_json('rh_gaps_10k.json')
mean_gap = mean(gaps)
print(f"  Zeros: {len(zeros)}, Gaps: {len(gaps)}, Mean gap: {mean_gap:.4f}")

# GUE and Poisson samples (3 seeds, averaged)
SEEDS = [42, 137, 271]
rng_pool = [random.Random(s) for s in SEEDS]
gue_samples = [gue_gaps(len(gaps), mean_gap, r) for r in rng_pool]
poi_samples = [poisson_gaps(len(gaps), mean_gap, random.Random(s + 1000)) for s in SEEDS]

# Log-prime DFT infrastructure
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]
prime_omegas = {p: math.log(p) for p in PRIMES}
log_vals = sorted(prime_omegas.values())
ctrl_omegas = [(log_vals[i] + log_vals[i+1]) / 2 for i in range(len(log_vals) - 1)]

def dft_snr(seq, zero_list):
    """Compute SNR at each prime frequency relative to interstitial noise."""
    n = len(seq)
    mu = mean(seq)
    hts = zero_list[1:n+1]

    def power(omega):
        re = sum((x - mu) * math.cos(omega * t) for x, t in zip(seq, hts)) / n
        im = sum((x - mu) * math.sin(omega * t) for x, t in zip(seq, hts)) / n
        return re**2 + im**2

    noise = mean([power(om) for om in ctrl_omegas]) or 1e-300
    return {p: power(prime_omegas[p]) / noise for p in PRIMES}


# ============================================================================
# 18B-i: All 16 sedenion product components
# ============================================================================

print(f"\n{'='*70}")
print("18B-i PREFLIGHT: Structural Zero Analysis for P1/Q1 Choice")
print(f"{'='*70}")
print("Expanding x_n * x_{n+1} = (g_n*P1 + g_{n+1}*Q1) * (g_{n+1}*P1 + g_{n+2}*Q1)")
print("  = g_n*g_{n+1}*(P1*P1) + g_n*g_{n+2}*(P1*Q1)")
print("  + g_{n+1}^2*(Q1*P1) + g_{n+1}*g_{n+2}*(Q1*Q1)")
print()

# Compute the four sedenion products that determine the component structure
P1P1 = cd_mul(P1, P1)
P1Q1 = cd_mul(P1, Q1)
Q1P1 = cd_mul(Q1, P1)
Q1Q1 = cd_mul(Q1, Q1)

def nonzero_components(v, tol=1e-12):
    return [i for i, x in enumerate(v) if abs(x) > tol]

nz_P1P1 = nonzero_components(P1P1)
nz_P1Q1 = nonzero_components(P1Q1)
nz_Q1P1 = nonzero_components(Q1P1)
nz_Q1Q1 = nonzero_components(Q1Q1)

print(f"  P1*P1 nonzero components: {nz_P1P1}  values: {[P1P1[i] for i in nz_P1P1]}")
print(f"  P1*Q1 nonzero components: {nz_P1Q1}  (bilateral ZD: expect [])")
print(f"  Q1*P1 nonzero components: {nz_Q1P1}  (bilateral ZD: expect [])")
print(f"  Q1*Q1 nonzero components: {nz_Q1Q1}  values: {[Q1Q1[i] for i in nz_Q1Q1]}")

# Structurally active components = union of all nonzero components across the four products
import functools, operator
all_nz = sorted(set(nz_P1P1) | set(nz_P1Q1) | set(nz_Q1P1) | set(nz_Q1Q1))
struct_zero = [c for c in range(16) if c not in all_nz]

print(f"\nStructurally active components (can be nonzero for ANY gap sequence): {all_nz}")
print(f"Structurally zero components (zero by algebra, independent of data):   {struct_zero}")

if nz_P1Q1 == [] and nz_Q1P1 == []:
    print()
    print("THEOREM CONFIRMED: P1*Q1 = Q1*P1 = 0 (bilateral zero divisor property).")
    print("Therefore x_n * x_{n+1} = -2*g_{n+1}*(g_n+g_{n+2}) * e0 exactly.")
    print("ALL 15 vector components are structurally zero ? not a statistical result,")
    print("but an algebraic consequence of the bilateral ZD structure of Pattern 1.")
    print("The product is FORCED into the scalar channel by the zero divisor property.")

# Empirical verification: confirm structurally-zero components are indeed all-zero
print(f"\nEmpirical verification (first 100 triplets of actual zeros):")
emp_components = [[] for _ in range(16)]
for i in range(min(100, len(gaps) - 2)):
    g1, g2, g3 = gaps[i], gaps[i+1], gaps[i+2]
    xn  = [g1 * P1[k] + g2 * Q1[k] for k in range(16)]
    xn1 = [g2 * P1[k] + g3 * Q1[k] for k in range(16)]
    prod = cd_mul(xn, xn1)
    for c in range(16):
        emp_components[c].append(prod[c])
empirically_zero = []
empirically_nonzero = []
for c in range(16):
    max_abs = max(abs(x) for x in emp_components[c]) if emp_components[c] else 0.0
    if max_abs < 1e-10:
        empirically_zero.append(c)
    else:
        empirically_nonzero.append(c)

print(f"  Empirically nonzero: {empirically_nonzero}")
print(f"  Empirically zero (max|val| < 1e-10): {empirically_zero}")
if set(empirically_zero) == set(struct_zero):
    print("  Structural prediction MATCHES empirical result. OK")
else:
    print(f"  WARNING: mismatch between structural prediction {struct_zero} and empirical {empirically_zero}")

ACTIVE_COMPONENTS = empirically_nonzero  # only these will be used in statistical analysis

print(f"\n{'='*70}")
print("18B-i: All 16 Sedenion Product Components ? Act/GUE Survey")
print(f"{'='*70}")
print(f"Only {len(ACTIVE_COMPONENTS)} structurally active component(s) will be analysed: {ACTIVE_COMPONENTS}")
print(f"Remaining {len(struct_zero)} components are algebraically zero and excluded from statistics.")
print(f"(Including them would artificially inflate 'Act/GUE ~= 1' counts.)")

def all_sed_components(gap_seq):
    """Return lists of all 16 component sequences from x_n * x_{n+1}."""
    components = [[] for _ in range(16)]
    for i in range(len(gap_seq) - 2):
        g1, g2, g3 = gap_seq[i], gap_seq[i+1], gap_seq[i+2]
        xn  = [g1 * P1[k] + g2 * Q1[k] for k in range(16)]
        xn1 = [g2 * P1[k] + g3 * Q1[k] for k in range(16)]
        prod = cd_mul(xn, xn1)
        for c in range(16):
            components[c].append(prod[c])
    return components

print("Computing sedenion product components for actual zeros...")
act_components = all_sed_components(gaps)

print("Computing for GUE samples...")
gue_components_list = [all_sed_components(g) for g in gue_samples]

print("Computing for Poisson samples...")
poi_components_list = [all_sed_components(p) for p in poi_samples]

# Average GUE and Poisson variance across seeds
gue_vars = [[var(gue_components_list[s][c]) for c in range(16)] for s in range(len(SEEDS))]
poi_vars = [[var(poi_components_list[s][c]) for c in range(16)] for s in range(len(SEEDS))]
gue_var_avg = [mean([gue_vars[s][c] for s in range(len(SEEDS))]) for c in range(16)]
poi_var_avg = [mean([poi_vars[s][c] for s in range(len(SEEDS))]) for c in range(16)]

act_vars = [var(act_components[c]) for c in range(16)]
act_means = [mean(act_components[c]) for c in range(16)]

# Act/GUE and Poi/GUE ratios
act_gue_ratios = [act_vars[c] / gue_var_avg[c] if gue_var_avg[c] > 0 else float('nan') for c in range(16)]
poi_gue_ratios = [poi_var_avg[c] / gue_var_avg[c] if gue_var_avg[c] > 0 else float('nan') for c in range(16)]

# Sedenion basis element labels (e0..e15)
basis_labels = [f"e{i}" for i in range(16)]

print(f"\n{'Comp':>5}  {'Basis':>5}  {'Act mean':>10}  {'Act var':>12}  "
      f"{'GUE var':>12}  {'Act/GUE':>8}  {'Poi/GUE':>8}")
print("-" * 75)
for c in range(16):
    marker = " <--" if c == 0 else ""
    print(f"{c:>5}  {basis_labels[c]:>5}  {act_means[c]:>10.4f}  {act_vars[c]:>12.4f}  "
          f"{gue_var_avg[c]:>12.4f}  {act_gue_ratios[c]:>8.4f}  {poi_gue_ratios[c]:>8.4f}{marker}")

# Summary counts ? only over structurally active components
n_lt_gue  = sum(1 for c in ACTIVE_COMPONENTS if not math.isnan(act_gue_ratios[c]) and act_gue_ratios[c] < 0.90)
n_approx  = sum(1 for c in ACTIVE_COMPONENTS if not math.isnan(act_gue_ratios[c]) and 0.90 <= act_gue_ratios[c] <= 1.10)
n_gt_gue  = sum(1 for c in ACTIVE_COMPONENTS if not math.isnan(act_gue_ratios[c]) and act_gue_ratios[c] > 1.10)
best_act_gue_comp = max(range(16), key=lambda c: act_gue_ratios[c] if not math.isnan(act_gue_ratios[c]) else -1)
best_poi_gue_comp = max(range(16), key=lambda c: poi_gue_ratios[c] if not math.isnan(poi_gue_ratios[c]) else -1)

print(f"\nSummary:")
print(f"  Act/GUE < 0.90 (actual tighter): {n_lt_gue} components")
print(f"  Act/GUE 0.90-1.10 (matches GUE): {n_approx} components")
print(f"  Act/GUE > 1.10 (actual broader):  {n_gt_gue} components")
print(f"  Highest Act/GUE ratio: component {best_act_gue_comp} ({basis_labels[best_act_gue_comp]}) = {act_gue_ratios[best_act_gue_comp]:.4f}")
print(f"  Highest Poi/GUE ratio: component {best_poi_gue_comp} ({basis_labels[best_poi_gue_comp]}) = {poi_gue_ratios[best_poi_gue_comp]:.4f}")

# Octonion-inherited (e1-e7) vs sedenion-only (e8-e15) boundary analysis
# e0 = scalar (separate); e1-e7 = octonion imaginary (inherited); e8-e15 = sedenion-only (pathological)
# IMPORTANT: only use structurally active components ? structurally zero components
# must be excluded or they will artificially dominate the group averages.
oct_comps_active = [c for c in range(1, 8)  if c in ACTIVE_COMPONENTS]
sed_comps_active = [c for c in range(8, 16) if c in ACTIVE_COMPONENTS]

oct_ratios = [act_gue_ratios[c] for c in oct_comps_active if not math.isnan(act_gue_ratios[c])]
sed_ratios = [act_gue_ratios[c] for c in sed_comps_active if not math.isnan(act_gue_ratios[c])]
oct_poi    = [poi_gue_ratios[c] for c in oct_comps_active if not math.isnan(poi_gue_ratios[c])]
sed_poi    = [poi_gue_ratios[c] for c in sed_comps_active if not math.isnan(poi_gue_ratios[c])]

print(f"\nOctonion/Sedenion Boundary Analysis (active components only):")
print(f"  e0  (scalar):                        Act/GUE = {act_gue_ratios[0]:.4f}  Poi/GUE = {poi_gue_ratios[0]:.4f}")
if oct_ratios:
    print(f"  e1-e7 active {oct_comps_active} (octonion):  Act/GUE = {mean(oct_ratios):.4f}  Poi/GUE = {mean(oct_poi):.4f}")
else:
    print(f"  e1-e7: NO active components for this P1/Q1 choice")
if sed_ratios:
    print(f"  e8-e15 active {sed_comps_active} (sedenion): Act/GUE = {mean(sed_ratios):.4f}  Poi/GUE = {mean(sed_poi):.4f}")
else:
    print(f"  e8-e15: NO active components for this P1/Q1 choice")

if not oct_ratios and not sed_ratios:
    print(f"\n  NOTE: Only the scalar component (e0) is structurally active for Pattern 1 P1/Q1.")
    print(f"  The bilateral ZD property (P1*Q1=Q1*P1=0) collapses ALL vector components to zero.")
    print(f"  Boundary hypothesis cannot be tested with Pattern 1 ? requires a different P/Q pair")
    print(f"  where at least one of P*Q or Q*P has nonzero vector components.")
    split = "N/A ? all vector components structurally zero for this P1/Q1 choice"
elif oct_ratios and sed_ratios:
    split = "YES ? octonion and sedenion groups differ" if abs(mean(oct_ratios) - mean(sed_ratios)) > 0.15 else "NO ? groups similar"
    print(f"  Boundary split detected: {split}")
else:
    split = "partial ? only one group has active components"
    print(f"  Boundary split: {split}")

# Log-prime DFT for all non-trivial components (skip components with ~0 variance)
print(f"\nLog-prime DFT SNR ? all components with Act var > 1e-6:")
print(f"{'Comp':>5}  {'Basis':>5}  {'p=2':>8}  {'p=3':>8}  {'p=5':>8}  {'p=7':>8}  {'p=11':>8}  max SNR")
print("-" * 65)
component_snr_results = {}
for c in range(16):
    if act_vars[c] < 1e-6:
        component_snr_results[c] = {str(p): 0.0 for p in PRIMES}
        continue
    snr = dft_snr(act_components[c], zeros)
    component_snr_results[c] = {str(p): snr[p] for p in PRIMES}
    max_snr = max(snr.values())
    best_p = max(snr, key=snr.get)
    print(f"{c:>5}  {basis_labels[c]:>5}  {snr[2]:>8.1f}  {snr[3]:>8.1f}  {snr[5]:>8.1f}  "
          f"{snr[7]:>8.1f}  {snr[11]:>8.1f}  {max_snr:.1f} @ p={best_p}")

best_snr_comp = max(range(16), key=lambda c: max(component_snr_results[c].values()) if component_snr_results[c] else 0)
best_snr_val  = max(component_snr_results[best_snr_comp].values())
print(f"\nBest log-prime SNR: component {best_snr_comp} ({basis_labels[best_snr_comp]}), max SNR = {best_snr_val:.1f}")


# ============================================================================
# 18B-ii: n-Gap Generalization
# ============================================================================

print(f"\n{'='*70}")
print("18B-ii: n-Gap Generalization ? k=1..8, s_n^(k) = central * sum(surrounding)")
print(f"{'='*70}")
print("Formula: s_n^(k) = g_{n+floor(k/2)} * sum of other k-1 gaps in window")
print("k=3 should reproduce Phase 17 Act/GUE = 1.02")
print()
print("DEFINITIONAL NOTE: k=2 in this family = g_n * g_{n+1} (product).")
print("Phase 10C 'two-gap' result (Act/GUE=0.65) used embed_pair P2 =")
print("  -(g1^2+g2^2)/(2*(g1+g2))  ? a different statistic (neg. harmonic mean).")
print("Both are computed below. They are NOT the same family; direct comparison")
print("of k=2 product to 0.65 is invalid without this flag.")

# Phase 10C P2 reference ? compute explicitly for comparison
def embed_p2(g1, g2):
    """Phase 10C embed_pair P2 projection: -(g1^2+g2^2)/(2*(g1+g2))"""
    s = g1 + g2
    return -(g1**2 + g2**2) / (2 * s) if s > 0 else 0.0

act_p2_seq = [embed_p2(gaps[i], gaps[i+1]) for i in range(len(gaps)-1)]
gue_p2_seqs = [[embed_p2(g[i], g[i+1]) for i in range(len(g)-1)] for g in gue_samples]
poi_p2_seqs = [[embed_p2(p[i], p[i+1]) for i in range(len(p)-1)] for p in poi_samples]
act_p2_var = var(act_p2_seq)
gue_p2_var = mean([var(s) for s in gue_p2_seqs])
poi_p2_var = mean([var(s) for s in poi_p2_seqs])
p2_agr = act_p2_var / gue_p2_var if gue_p2_var > 0 else float('nan')
p2_pgr = poi_p2_var / gue_p2_var if gue_p2_var > 0 else float('nan')
print(f"\nPhase 10C reference (embed_pair P2, k=2 equivalent):")
print(f"  Act var={act_p2_var:.4f}, GUE var={gue_p2_var:.4f}, Act/GUE={p2_agr:.4f} (expect ~0.65)")
print(f"  Poi/GUE={p2_pgr:.4f}")

def ngap_stat(gap_seq, k):
    """k-gap statistic: central gap times sum of surrounding gaps in k-window."""
    if k == 1:
        return list(gap_seq)
    mid = k // 2
    result = []
    for i in range(len(gap_seq) - k + 1):
        window = gap_seq[i:i+k]
        central = window[mid]
        surrounding = sum(window[:mid]) + sum(window[mid+1:])
        result.append(central * surrounding)
    return result

k_range = range(1, 9)
k_results = []

print(f"\n{'k':>4}  {'n_values':>9}  {'Act var':>12}  {'GUE var':>12}  "
      f"{'Poi var':>12}  {'Act/GUE':>8}  {'Poi/GUE':>8}")
print("-" * 75)

for k in k_range:
    act_seq = ngap_stat(gaps, k)
    gue_seqs = [ngap_stat(g, k) for g in gue_samples]
    poi_seqs = [ngap_stat(p, k) for p in poi_samples]

    act_v = var(act_seq)
    gue_v = mean([var(s) for s in gue_seqs])
    poi_v = mean([var(s) for s in poi_seqs])
    agr   = act_v / gue_v if gue_v > 0 else float('nan')
    pgr   = poi_v / gue_v if gue_v > 0 else float('nan')

    k_results.append({
        'k': k,
        'n_values': len(act_seq),
        'actual_var': act_v,
        'gue_var': gue_v,
        'poisson_var': poi_v,
        'act_gue_ratio': agr,
        'poi_gue_ratio': pgr
    })
    marker = " <- Phase 17" if k == 3 else ""
    print(f"{k:>4}  {len(act_seq):>9}  {act_v:>12.4f}  {gue_v:>12.4f}  "
          f"{poi_v:>12.4f}  {agr:>8.4f}  {pgr:>8.4f}{marker}")

# Find transition point
ratios = [r['act_gue_ratio'] for r in k_results]
transition_k = None
for i in range(len(ratios) - 1):
    if ratios[i] < 1.0 and ratios[i+1] >= 1.0:
        transition_k = k_results[i+1]['k']
        break

if transition_k:
    print(f"\nTransition from Act/GUE < 1 to Act/GUE >= 1: at k={transition_k}")
else:
    vals_str = ', '.join(f"k={r['k']}:{r['act_gue_ratio']:.3f}" for r in k_results)
    print(f"\nNo clean transition found. Ratios: {vals_str}")


# ============================================================================
# 18B-iii: Height Window Stability
# ============================================================================

print(f"\n{'='*70}")
print("18B-iii: Height Window Stability ? Three-Gap Statistic (k=3)")
print(f"{'='*70}")
print("Phase 12A established: two-gap Act/GUE is HEIGHT-DEPENDENT (not sample-size).")
print("Ratio ranged 0.65-0.75 depending on height window; always < 1.0.")
print("If three-gap Act/GUE ~= 1.02 is height-STABLE, that is qualitatively stronger:")
print("  GUE-matching at three-gap scale is a universal property of the zero spectrum,")
print("  not a window artifact. This distinction belongs in the write-up.")

window_size = len(gaps) // 4
windows = [
    (f"zeros {i*window_size}?{(i+1)*window_size - 1}", i*window_size, (i+1)*window_size)
    for i in range(4)
]

def three_gap_for_window(gap_seq, start, end):
    """Three-gap statistic for a sub-window of gaps."""
    sub = gap_seq[start:end]
    return ngap_stat(sub, 3)

print(f"\n{'Window':>25}  {'Heights':>18}  {'Act var':>10}  {'GUE var':>10}  {'Act/GUE':>8}")
print("-" * 80)

height_results = []
for label, start, end in windows:
    sub_gaps = gaps[start:end]
    sub_gue  = [gue_samples[0][start:end]]  # use seed 0 for window tests
    sub_poi  = [poi_samples[0][start:end]]

    act_tg = ngap_stat(sub_gaps, 3)
    gue_tg = ngap_stat(sub_gue[0], 3)

    act_v = var(act_tg)
    gue_v = var(gue_tg)
    agr   = act_v / gue_v if gue_v > 0 else float('nan')

    h_lo = zeros[start] if start < len(zeros) else 0
    h_hi = zeros[min(end, len(zeros)-1)]
    h_range = f"t={h_lo:.0f}?{h_hi:.0f}"

    print(f"{label:>25}  {h_range:>18}  {act_v:>10.4f}  {gue_v:>10.4f}  {agr:>8.4f}")
    height_results.append({
        'label': label, 'start': start, 'end': end,
        'height_lo': h_lo, 'height_hi': h_hi,
        'act_var': act_v, 'gue_var': gue_v, 'act_gue_ratio': agr
    })

all_agrs = [r['act_gue_ratio'] for r in height_results if not math.isnan(r['act_gue_ratio'])]
if all_agrs:
    print(f"\nAct/GUE range across windows: {min(all_agrs):.4f} ? {max(all_agrs):.4f}")
    stability = "stable" if max(all_agrs) - min(all_agrs) < 0.15 else "height-dependent"
    print(f"Height stability assessment: {stability}")


# ============================================================================
# Save results
# ============================================================================

results = {
    "phase": "18B",
    "date": "2026-03-16",
    "researcher": "Paul Chavez, Chavez AI Labs LLC",
    "data": {
        "n_zeros": len(zeros),
        "n_gaps": len(gaps),
        "mean_gap": mean_gap,
        "seeds": SEEDS
    },
    "18Bi_vector_part_survey": {
        "question": "What do all 16 sedenion product components reveal about Act/GUE structure?",
        "preflight": {
            "P1_sq_nonzero_components": nz_P1P1,
            "P1_Q1_nonzero_components": nz_P1Q1,
            "Q1_P1_nonzero_components": nz_Q1P1,
            "Q1_sq_nonzero_components": nz_Q1Q1,
            "structurally_active_components": ACTIVE_COMPONENTS,
            "structurally_zero_components": struct_zero,
            "bilateral_zd_forces_scalar_product": nz_P1Q1 == [] and nz_Q1P1 == [],
            "theorem": "If P*Q=Q*P=0 and P^2=Q^2=-2*e0, then x_n*x_{n+1} is purely scalar for all gap sequences. All 15 vector components are algebraically zero, not statistically zero."
        },
        "n_triplets": len(act_components[0]),
        "P1_pattern": {1: 1, 14: 1},
        "Q1_pattern": {3: 1, 12: 1},
        "components": [
            {
                "index": c,
                "basis_element": basis_labels[c],
                "actual_mean": act_means[c],
                "actual_var": act_vars[c],
                "gue_var": gue_var_avg[c],
                "poisson_var": poi_var_avg[c],
                "act_gue_ratio": act_gue_ratios[c],
                "poi_gue_ratio": poi_gue_ratios[c],
                "log_prime_snr": component_snr_results[c]
            }
            for c in range(16)
        ],
        "summary": {
            "n_components_act_lt_gue": n_lt_gue,
            "n_components_act_approx_gue": n_approx,
            "n_components_act_gt_gue": n_gt_gue,
            "max_act_gue_ratio_component": best_act_gue_comp,
            "max_act_gue_ratio_value": act_gue_ratios[best_act_gue_comp],
            "max_poi_gue_ratio_component": best_poi_gue_comp,
            "max_poi_gue_ratio_value": poi_gue_ratios[best_poi_gue_comp],
            "best_log_prime_snr_component": best_snr_comp,
            "best_log_prime_snr_value": best_snr_val
        },
        "octonion_sedenion_boundary": {
            "note": "e0=scalar, e1-e7=octonion-inherited, e8-e15=sedenion-only (pathological). Only structurally active components included.",
            "active_components_only": ACTIVE_COMPONENTS,
            "e0_scalar": {"act_gue_ratio": act_gue_ratios[0], "poi_gue_ratio": poi_gue_ratios[0]},
            "e1_e7_octonion": {
                "active_components": oct_comps_active,
                "act_gue_mean": mean(oct_ratios) if oct_ratios else None,
                "poi_gue_mean": mean(oct_poi) if oct_poi else None,
                "act_gue_values": {str(c): act_gue_ratios[c] for c in oct_comps_active}
            },
            "e8_e15_sedenion": {
                "active_components": sed_comps_active,
                "act_gue_mean": mean(sed_ratios) if sed_ratios else None,
                "poi_gue_mean": mean(sed_poi) if sed_poi else None,
                "act_gue_values": {str(c): act_gue_ratios[c] for c in sed_comps_active}
            },
            "boundary_split_detected": split,
            "boundary_testable": len(oct_comps_active) > 0 and len(sed_comps_active) > 0
        }
    },
    "18Bii_ngap_generalization": {
        "question": "At what k does Act/GUE variance ratio transition from <1 to ~=1?",
        "formula": "s_n^(k) = g_{n+floor(k/2)} * sum(other k-1 gaps in window)",
        "note_k3": "k=3 formula g_{n+1}*(g_n+g_{n+2}) = Phase 17 sedenion scalar (sign drop for variance)",
        "definitional_note": "k=2 product g_n*g_{n+1} is NOT embed_pair P2. Phase 10C 0.65 belongs to P2 = -(g1^2+g2^2)/(2*(g1+g2)). Not the same family.",
        "phase10c_p2_reference": {
            "formula": "-(g1^2+g2^2)/(2*(g1+g2))",
            "actual_var": act_p2_var,
            "gue_var": gue_p2_var,
            "poisson_var": poi_p2_var,
            "act_gue_ratio": p2_agr,
            "poi_gue_ratio": p2_pgr,
            "note": "This is the Phase 10C two-gap result; expect Act/GUE ~0.65"
        },
        "k_results": k_results,
        "transition_k": transition_k,
    },
    "18Biii_height_stability": {
        "question": "Does k=3 Act/GUE ~= 1.02 hold across height windows?",
        "phase12a_context": "Two-gap Act/GUE was HEIGHT-DEPENDENT (0.65 at low heights, 0.75 at high, always <1). If three-gap is stable, that is qualitatively stronger: GUE-matching at three-gap scale is universal.",
        "window_size": window_size,
        "windows": height_results,
        "act_gue_range": [min(all_agrs), max(all_agrs)] if all_agrs else None,
        "stability_assessment": stability if all_agrs else "unknown",
        "qualitative_significance": "height-stable three-gap > height-dependent two-gap: universality vs window artifact"
    }
}

out_path = os.path.join(script_dir, 'p18b_results.json')
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n{'='*70}")
print("PHASE 18B COMPLETE")
print(f"{'='*70}")
print(f"Results saved to: p18b_results.json")
print(f"\nQUICK SUMMARY:")
print(f"  18B-i  components Act/GUE < 0.90: {n_lt_gue}/16, ~=GUE: {n_approx}/16, > 1.10: {n_gt_gue}/16")
print(f"  18B-ii transition k: {transition_k if transition_k else 'see table'}")
print(f"  18B-iii height stability: {stability if all_agrs else 'unknown'}")
print(f"  Best log-prime SNR: component {best_snr_comp} ({basis_labels[best_snr_comp]}), SNR={best_snr_val:.1f}")
