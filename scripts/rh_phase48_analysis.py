"""
rh_phase48_analysis.py
======================
Phase 48 -- gamma_n-Scaling of ZDTP Convergence
The Asymptotic Structure of Sedenion Transmission

FULL ANALYSIS -- Python native implementation.

Key findings from Claude Desktop calibration (2026-03-30):
  - Raw F-vector ZDTP gives convergence ~0.698 at n=1 -- matches Phase 42 AIEX-175 exactly.
  - Phase 43's higher values (0.843) were a second-pass protocol (gateway sigs as ZDTP input).
  - Formula verified: convergence = 1 - std(mags) / mean(mags).
  - S3B = S4 exact pairing confirmed universal on raw vectors.
  - For zero-padded F_64 with gateways at indices < 16: cd_mul(F_64, G_64) reduces to
    cd_mul(F_16, G_16). 64D computation is equivalent to 16D. Engine runs natively.
  - Convergence is NOT monotone per individual zero (n=1: 0.6977, n=2: 0.6202).
    The Phase 42 trend is aggregate/range, not per-zero.

Division of labor:
  Python (this script): all 1,700 vectors across Bands 1-4 + sigma04
  CAILculator:          strategic spot-checks + Chavez Transform on convergence series

TRACK A: 16D gateway engine + calibration vs CAILculator n=1 ground truth
TRACK B: Dense convergence scan (Bands 1-4)
TRACK C: Functional form fitting
TRACK D: Gateway structure analysis
TRACK E: sigma-comparative scan (Band 1 at sigma=0.4 vs sigma=0.5)
TRACK F: CAILculator spot-check prep (strategic sample for Desktop verification)

Jackie Robinson Standard:
  1. Calibration gate FIRST -- scan does not proceed without verified engine
  2. GUE/Poisson controls on Band 1 -- honest null if not RH-specific
  3. No over-fitting -- prefer simpler models; report R-squared honestly
  4. sigma-comparative genuinely predictive -- run before interpreting results
  5. Report all anomalies, including non-monotone behavior

Inputs:  rh_zeros_10k.json
Outputs: phase48_calibration.json, phase48_scan.json, phase48_fit.json,
         phase48_gateway_structure.json, phase48_sigma_comparative.json,
         phase48_spotcheck_prep.json, phase48_results.json

Date: 2026-03-30
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.special import erf as scipy_erf
import json, time

# ============================================================
# SEDENION ENGINE (unchanged from Phase 42)
# ============================================================

def cd_conj(v):
    c = list(v)
    for i in range(1, len(v)): c[i] = -v[i]
    return c

def cd_mul(a, b):
    n = len(a)
    if n == 1: return [a[0] * b[0]]
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    c1 = [x - y for x, y in zip(cd_mul(a1, b1), cd_mul(cd_conj(b2), a2))]
    c2 = [x + y for x, y in zip(cd_mul(b2, a1), cd_mul(a2, cd_conj(b1)))]
    return c1 + c2

def norm_sq(v): return sum(x * x for x in v)

def make16(pairs):
    v = [0.0] * 16
    for i, val in pairs: v[i] = float(val)
    return v

sqrt2 = np.sqrt(2.0)

ROOT_16D_BASE = {
    2:  make16([(3,  1.0), (12, -1.0)]),
    3:  make16([(5,  1.0), (10,  1.0)]),
    5:  make16([(3,  1.0), (6,   1.0)]),
    7:  make16([(2,  1.0), (7,  -1.0)]),
    11: make16([(2,  1.0), (7,   1.0)]),
    13: make16([(6,  1.0), (9,   1.0)]),
}
PRIMES_6 = [2, 3, 5, 7, 11, 13]

def F_16d(t, sigma=0.5):
    r = make16([(0, 1.0)])
    for p in PRIMES_6:
        theta = t * np.log(p)
        rp = ROOT_16D_BASE[p]
        rn = np.sqrt(norm_sq(rp))
        f = [0.0] * 16
        f[0] = np.cos(theta)
        for i in range(16): f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

# ============================================================
# TRACK A: 16D GATEWAY ENGINE
# Notes:
#   For zero-padded F_64 with gateway indices < 16:
#   cd_mul(F_64, G_64) = [cd_mul(F_16, G_16), 0^48]
#   so norm is identical. Run in 16D natively.
# ============================================================

GATEWAY_ORDER = ['S1', 'S2', 'S3A', 'S3B', 'S4', 'S5']
GATEWAYS_16D = {
    'S1':  make16([(3,  1.0)]),   # e3  -- Master
    'S2':  make16([(5,  1.0)]),   # e5  -- Multi-modal
    'S3A': make16([(10, 1.0)]),   # e10 -- Discontinuous
    'S3B': make16([(6,  1.0)]),   # e6  -- Diagonal A
    'S4':  make16([(9,  1.0)]),   # e9  -- Diagonal B
    'S5':  make16([(12, 1.0)]),   # e12 -- Orthogonal
}

def zdtp_convergence(F_16):
    """
    Compute ZDTP convergence on raw 16D F-vector.
    Equivalent to 64D computation for zero-padded inputs (verified by CAILculator).
    Returns: (convergence, mags, mu, sigma_mag)
    """
    mags = [float(np.sqrt(norm_sq(cd_mul(F_16, GATEWAYS_16D[g])))) for g in GATEWAY_ORDER]
    mu        = float(np.mean(mags))
    sigma_mag = float(np.std(mags))
    return 1.0 - sigma_mag / mu, mags, mu, sigma_mag

# CAILculator ground truth for raw F-vector at n=1 (gamma_1 ~ 14.134725)
# Confirmed by Claude Desktop 2026-03-30
CALIB_REF_CONVERGENCE = 0.6977
CALIB_REF_S3B         = 4.154982
CALIB_REF_S4          = 4.154982
CALIB_TOL_CONV        = 1e-3   # convergence within 0.001
CALIB_TOL_PAIR        = 1e-6   # S3B=S4 pairing

# ============================================================
# LOAD DATA
# ============================================================
print("Loading Riemann zeros...")
gammas_all = json.load(open("rh_zeros_10k.json"))
print(f"  Loaded {len(gammas_all)} zeros")
print(f"  gamma_1={gammas_all[0]:.6f}  gamma_5000={gammas_all[4999]:.3f}")

t0_total = time.time()
results  = {}

# ============================================================
# TRACK A: CALIBRATION
# ============================================================
print("\n" + "="*60)
print("TRACK A -- Calibration vs CAILculator ground truth")
print("="*60)

gamma1 = gammas_all[0]
F1     = F_16d(gamma1, sigma=0.5)
conv1, mags1, mu1, sig1 = zdtp_convergence(F1)

s3b_dev  = abs(mags1[3] - CALIB_REF_S3B)
s4_dev   = abs(mags1[4] - CALIB_REF_S4)
conv_dev = abs(conv1 - CALIB_REF_CONVERGENCE)

print(f"  n=1  gamma={gamma1:.6f}")
print(f"  S3B: {mags1[3]:.6f}  ref={CALIB_REF_S3B}  dev={s3b_dev:.2e}")
print(f"  S4:  {mags1[4]:.6f}  ref={CALIB_REF_S4}  dev={s4_dev:.2e}")
print(f"  convergence: {conv1:.6f}  ref={CALIB_REF_CONVERGENCE}  dev={conv_dev:.2e}")
print(f"  S3B=S4 exact: {abs(mags1[3] - mags1[4]) < CALIB_TOL_PAIR}")

calib_pass = (s3b_dev < CALIB_TOL_PAIR and
              s4_dev  < CALIB_TOL_PAIR and
              conv_dev < CALIB_TOL_CONV)

calib_result = {
    'gamma': float(gamma1), 'sigma': 0.5,
    'pass': calib_pass,
    'computed': {g: mags1[k] for k, g in enumerate(GATEWAY_ORDER)},
    'convergence_computed':  float(conv1),
    'convergence_reference': CALIB_REF_CONVERGENCE,
    'convergence_deviation': float(conv_dev),
    'S3B_deviation': float(s3b_dev),
    'S4_deviation':  float(s4_dev),
    'S3B_S4_exact':  bool(abs(mags1[3] - mags1[4]) < CALIB_TOL_PAIR),
    'source': 'CAILculator raw F-vector ZDTP, Claude Desktop 2026-03-30',
}
json.dump(calib_result, open("phase48_calibration.json", "w"), indent=2)

if not calib_pass:
    print("\n*** CALIBRATION FAILED -- halting per Jackie Robinson Standard ***")
    raise SystemExit(1)
print("  CALIBRATION PASSED -- proceeding")

# ============================================================
# SURROGATE GENERATORS (Jackie Robinson Standard)
# ============================================================

def generate_gue_zeros(n_zeros, gamma_start, seed=42):
    """GUE via Wigner surmise: CDF F(s) = 1 - exp(-pi*s^2/4)."""
    rng = np.random.RandomState(seed)
    zeros = [gamma_start]
    g = gamma_start
    for _ in range(n_zeros - 1):
        mean_sp = 2.0 * np.pi / np.log(max(g, 10.0) / (2.0 * np.pi))
        u = rng.uniform(0.0, 1.0 - 1e-10)
        s = np.sqrt(-4.0 / np.pi * np.log(1.0 - u))
        g += s * mean_sp
        zeros.append(g)
    return zeros

def generate_poisson_zeros(n_zeros, gamma_start, seed=42):
    """Poisson via exponential spacings."""
    rng = np.random.RandomState(seed)
    zeros = [gamma_start]
    g = gamma_start
    for _ in range(n_zeros - 1):
        mean_sp = 2.0 * np.pi / np.log(max(g, 10.0) / (2.0 * np.pi))
        g += rng.exponential(1.0) * mean_sp
        zeros.append(g)
    return zeros

# ============================================================
# TRACK B: DENSE CONVERGENCE SCAN
# ============================================================
print("\n" + "="*60)
print("TRACK B -- Dense Convergence Scan")
print("="*60)

BANDS = [
    ('Band1', 0,    100,  1),
    ('Band2', 100,  500,  1),
    ('Band3', 500,  2000, 3),
    ('Band4', 2000, 5000, 5),
]

scan_records = []
t_scan = time.time()

for band_label, idx_start, idx_end, step in BANDS:
    indices  = list(range(idx_start, idx_end, step))
    t_band   = time.time()
    print(f"\n  {band_label}: n={idx_start+1}..{idx_end} step={step} ({len(indices)} pts)")

    for count, idx in enumerate(indices):
        gamma     = gammas_all[idx]
        Fv        = F_16d(gamma, sigma=0.5)
        conv, mags, mu, sig = zdtp_convergence(Fv)
        scan_records.append({
            'n':           idx + 1,
            'band':        band_label,
            'gamma':       float(gamma),
            'convergence': float(conv),
            'mags':        [float(m) for m in mags],
            'mu':          float(mu),
            'sigma_mag':   float(sig),
        })
        if (count + 1) % 100 == 0 or count == len(indices) - 1:
            print(f"    n={idx+1:5d}  gamma={gamma:8.2f}  "
                  f"conv={conv:.6f}  mu={mu:.4f}  [{time.time()-t_band:.1f}s]")

# GUE and Poisson controls -- Band 1 range
print("\n  Surrogate controls (Band 1, n=100)...")
gue_gammas     = generate_gue_zeros(100, gammas_all[0])
poisson_gammas = generate_poisson_zeros(100, gammas_all[0])

gue_records = []
for i, g in enumerate(gue_gammas):
    conv, mags, mu, sig = zdtp_convergence(F_16d(g, sigma=0.5))
    gue_records.append({'n': i+1, 'gamma': float(g),
                        'convergence': float(conv), 'mu': float(mu)})

poisson_records = []
for i, g in enumerate(poisson_gammas):
    conv, mags, mu, sig = zdtp_convergence(F_16d(g, sigma=0.5))
    poisson_records.append({'n': i+1, 'gamma': float(g),
                             'convergence': float(conv), 'mu': float(mu)})

rh_b1  = [r['convergence'] for r in scan_records if r['band'] == 'Band1']
gue_b1 = [r['convergence'] for r in gue_records]
poi_b1 = [r['convergence'] for r in poisson_records]

print(f"  RH   Band1: mean={np.mean(rh_b1):.4f}  "
      f"min={np.min(rh_b1):.4f}  max={np.max(rh_b1):.4f}")
print(f"  GUE  Band1: mean={np.mean(gue_b1):.4f}  "
      f"min={np.min(gue_b1):.4f}  max={np.max(gue_b1):.4f}")
print(f"  POI  Band1: mean={np.mean(poi_b1):.4f}  "
      f"min={np.min(poi_b1):.4f}  max={np.max(poi_b1):.4f}")

json.dump({'rh': scan_records, 'gue': gue_records, 'poisson': poisson_records,
           'elapsed_s': time.time() - t_scan},
          open("phase48_scan.json", "w"), indent=2)
print(f"\n  Scan complete: {len(scan_records)} RH pts in {time.time()-t_scan:.1f}s")

# ============================================================
# TRACK C: FUNCTIONAL FORM FITTING
# ============================================================
print("\n" + "="*60)
print("TRACK C -- Functional Form Fitting")
print("="*60)

gammas_fit = np.array([r['gamma'] for r in scan_records])
convs_fit  = np.array([r['convergence'] for r in scan_records])

def r_sq(y, yp):
    ss_res = np.sum((y - yp)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    return float(1.0 - ss_res / ss_tot)

models = [
    ('power_law',    lambda g, c, a:       1.0 - c * g**(-a),          [1.0, 0.3]),
    ('log_decay',    lambda g, c:           1.0 - c / np.log(g),        [2.0]),
    ('exp_approach', lambda g, a, b, g0:    a - b * np.exp(-g / g0),    [1.0, 0.5, 50.0]),
    ('sigmoid_erf',  lambda g, A, g0:       A * scipy_erf(g / g0),      [1.0, 50.0]),
    ('log_power',    lambda g, c, a, b:     1.0 - c*(np.log(g))**b/g**a,[5.0, 0.4, 1.0]),
]

fit_results = {}
for name, func, p0 in models:
    try:
        popt, _ = curve_fit(func, gammas_fit, convs_fit, p0=p0, maxfev=10000)
        yp      = func(gammas_fit, *popt)
        r2      = r_sq(convs_fit, yp)
        asymp   = float(func(np.array([1e6]), *popt)[0])
        fit_results[name] = {
            'params': [float(p) for p in popt],
            'r_squared': r2,
            'asymptote_at_1e6': asymp,
            'converges_to_1': bool(abs(asymp - 1.0) < 0.01),
            'status': 'ok',
        }
        print(f"  {name:16s}: R2={r2:.6f}  asymptote={asymp:.6f}  "
              f"->1={abs(asymp-1.0)<0.01}  params={[f'{p:.4f}' for p in popt]}")
    except Exception as e:
        fit_results[name] = {'status': f'failed: {e}', 'r_squared': None}
        print(f"  {name:16s}: FAILED -- {e}")

ok_fits = [(k, v) for k, v in fit_results.items() if v.get('r_squared') is not None]
if ok_fits:
    best_name, best_val = max(ok_fits, key=lambda x: x[1]['r_squared'])
    fit_results['best_model']     = best_name
    fit_results['best_r_squared'] = best_val['r_squared']
    print(f"\n  Best fit: {best_name} (R2={best_val['r_squared']:.6f}  "
          f"asymptote={best_val['asymptote_at_1e6']:.6f})")

json.dump(fit_results, open("phase48_fit.json", "w"), indent=2)

# ============================================================
# TRACK D: GATEWAY STRUCTURE ANALYSIS
# ============================================================
print("\n" + "="*60)
print("TRACK D -- Gateway Structure Analysis")
print("="*60)

s3b = np.array([r['mags'][3] for r in scan_records])
s4  = np.array([r['mags'][4] for r in scan_records])
s1  = np.array([r['mags'][0] for r in scan_records])
s5  = np.array([r['mags'][5] for r in scan_records])
mus = np.array([r['mu']    for r in scan_records])
gs  = np.array([r['gamma'] for r in scan_records])

# S3B = S4 pairing
pair_devs      = np.abs(s3b - s4)
max_pair_dev   = float(np.max(pair_devs))
pairing_exact  = bool(max_pair_dev < 1e-10)
print(f"  S3B=S4 max dev over {len(scan_records)} zeros: {max_pair_dev:.2e}  "
      f"({'EXACT' if pairing_exact else 'BROKEN'})")

# S1/S5 ratio stability
ratios = s1 / s5
print(f"  S1/S5 ratio: n=1={ratios[0]:.6f}  "
      f"mean={np.mean(ratios):.6f}  std={np.std(ratios):.6f}  "
      f"range=[{np.min(ratios):.4f},{np.max(ratios):.4f}]")

# Mean magnitude scaling: mu vs gamma
try:
    popt_mu, _ = curve_fit(lambda g, a, b: a * g**b, gs, mus,
                           p0=[1.0, 0.3], maxfev=5000)
    mu_r2 = r_sq(mus, popt_mu[0] * gs**popt_mu[1])
    mu_fit = {'model': 'power_law', 'a': float(popt_mu[0]),
              'b': float(popt_mu[1]), 'r_squared': mu_r2}
    print(f"  mu(gamma) ~ {popt_mu[0]:.4f} * gamma^{popt_mu[1]:.4f}  R2={mu_r2:.6f}")
except Exception as e:
    mu_fit = {'status': f'failed: {e}'}
    print(f"  mu(gamma) fit failed: {e}")

# First ordering break (S1 > S2 > S3A not guaranteed per zero)
ordering_breaks = []
for r in scan_records:
    m = r['mags']
    if not (m[0] > m[1] and m[1] > m[2]):
        ordering_breaks.append({'n': r['n'], 'gamma': r['gamma'], 'mags': m})

print(f"  S1>S2>S3A ordering breaks: {len(ordering_breaks)} / {len(scan_records)}")
if ordering_breaks:
    ob = ordering_breaks[0]
    print(f"    First at n={ob['n']} gamma={ob['gamma']:.2f}")

gw_structure = {
    'S3B_S4_max_dev': max_pair_dev, 'S3B_S4_pairing_exact': pairing_exact,
    'S3B_S4_n_tested': len(scan_records),
    'S1_S5_ratio': {'at_n1': float(ratios[0]), 'mean': float(np.mean(ratios)),
                    'std': float(np.std(ratios)),
                    'min': float(np.min(ratios)), 'max': float(np.max(ratios))},
    'mu_scaling': mu_fit,
    'mu_at_n1':   float(mus[0]),
    'mu_at_n100': float(mus[min(99,  len(mus)-1)]),
    'mu_at_n500': float(mus[min(399, len(mus)-1)]),
    'ordering_breaks_count': len(ordering_breaks),
    'ordering_breaks_first': ordering_breaks[0] if ordering_breaks else None,
}
json.dump(gw_structure, open("phase48_gateway_structure.json", "w"), indent=2)

# ============================================================
# TRACK E: sigma-COMPARATIVE SCAN
# ============================================================
print("\n" + "="*60)
print("TRACK E -- sigma-Comparative (Band 1: sigma=0.4 vs sigma=0.5)")
print("="*60)

sig_records = {}
for sigma_val, label in [(0.5, 'sigma_0p5'), (0.4, 'sigma_0p4')]:
    recs = []
    for idx in range(100):
        g    = gammas_all[idx]
        conv, mags, mu, sig = zdtp_convergence(F_16d(g, sigma=sigma_val))
        recs.append({'n': idx+1, 'gamma': float(g), 'convergence': float(conv),
                     'mu': float(mu), 'sigma_mag': float(sig)})
    sig_records[label] = recs
    cs = [r['convergence'] for r in recs]
    print(f"  sigma={sigma_val}: mean={np.mean(cs):.6f}  "
          f"min={np.min(cs):.6f}  max={np.max(cs):.6f}  std={np.std(cs):.6f}")

c05 = np.array([r['convergence'] for r in sig_records['sigma_0p5']])
c04 = np.array([r['convergence'] for r in sig_records['sigma_0p4']])
mean_diff     = float(np.mean(c05 - c04))
max_abs_diff  = float(np.max(np.abs(c05 - c04)))
discriminable = bool(abs(mean_diff) > 0.001)
print(f"  Discriminability: mean diff={mean_diff:.6f}  "
      f"max|diff|={max_abs_diff:.6f}  discriminable={discriminable}")

json.dump({
    'sigma_0p5': sig_records['sigma_0p5'],
    'sigma_0p4': sig_records['sigma_0p4'],
    'mean_diff_0p5_minus_0p4': mean_diff,
    'max_abs_diff': max_abs_diff,
    'discriminable': discriminable,
    'note': 'Band 1 only (n=1..100). Positive mean_diff = sigma=0.5 has higher convergence.',
}, open("phase48_sigma_comparative.json", "w"), indent=2)

# ============================================================
# TRACK F: CAILculator SPOT-CHECK PREP
# ============================================================
print("\n" + "="*60)
print("TRACK F -- CAILculator Spot-Check Prep")
print("="*60)

# Strategic sample for Desktop verification and Chavez Transform
spot_n = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2000, 3000, 5000]
spot_vectors = []
for n in spot_n:
    idx   = n - 1
    gamma = gammas_all[idx]
    Fv    = F_16d(gamma, sigma=0.5)
    conv, mags, mu, sig = zdtp_convergence(Fv)
    spot_vectors.append({
        'n': n, 'gamma': float(gamma), 'sigma': 0.5,
        'F_vector': [float(x) for x in Fv],
        'python_convergence': float(conv),
        'python_mags': [float(m) for m in mags],
        'python_mu': float(mu),
    })
    print(f"  n={n:5d}  gamma={gamma:8.2f}  conv={conv:.6f}  mu={mu:.4f}")

# Also prep the convergence series itself for Chavez Transform
conv_series = [r['convergence'] for r in scan_records]
gamma_series = [r['gamma'] for r in scan_records]

json.dump({
    'description': 'Strategic spot-check vectors for CAILculator ZDTP verification + Chavez Transform',
    'spot_vectors': spot_vectors,
    'convergence_series': {
        'values': conv_series,
        'gammas': gamma_series,
        'n_points': len(conv_series),
        'note': 'Full scan convergence values -- run Chavez Transform on this series',
    },
    'instructions': (
        'For each spot_vector: run ZDTP and compare python_convergence to CAILculator result. '
        'Then run Chavez Transform (pattern_id=1, alpha=1.0) on convergence_series values '
        'to characterize the global symmetry structure of the gamma_n-scaling signal.'
    ),
}, open("phase48_spotcheck_prep.json", "w"), indent=2)

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*60)
print("Phase 48 Summary -- Jackie Robinson Standard")
print("="*60)

best_model = fit_results.get('best_model', 'N/A')
best_r2    = fit_results.get('best_r_squared')
asymptote  = fit_results.get(best_model, {}).get('asymptote_at_1e6')

def conv_near_n(n):
    closest = min(scan_records, key=lambda r: abs(r['n'] - n))
    return closest['convergence'], closest['gamma']

c1,   g1   = conv_near_n(1)
c100, g100 = conv_near_n(100)
c500, g500 = conv_near_n(500)
c2k,  g2k  = conv_near_n(2000)
c5k,  g5k  = conv_near_n(5000)

print(f"\n  Convergence trajectory:")
print(f"    n=1     gamma={g1:.1f}:    {c1:.6f}")
print(f"    n=100   gamma={g100:.1f}:  {c100:.6f}")
print(f"    n=500   gamma={g500:.1f}:  {c500:.6f}")
print(f"    n=2000  gamma={g2k:.1f}: {c2k:.6f}")
print(f"    n=5000  gamma={g5k:.1f}: {c5k:.6f}")
print(f"\n  Best fit: {best_model}  R2={best_r2:.6f}  asymptote={asymptote:.6f}")
print(f"  S3B=S4 exact pairing: {'YES (all tested)' if pairing_exact else 'BROKEN'}")
print(f"  sigma discriminable:  {discriminable}  (mean diff={mean_diff:.6f})")
print(f"\n  JRS Controls (Band 1):")
print(f"    RH mean conv:      {np.mean(rh_b1):.6f}")
print(f"    GUE mean conv:     {np.mean(gue_b1):.6f}")
print(f"    Poisson mean conv: {np.mean(poi_b1):.6f}")

summary = {
    'phase': 48, 'date': '2026-03-30',
    'convergence_trajectory': {
        'n1':   {'gamma': g1,   'conv': c1},
        'n100': {'gamma': g100, 'conv': c100},
        'n500': {'gamma': g500, 'conv': c500},
        'n2000':{'gamma': g2k,  'conv': c2k},
        'n5000':{'gamma': g5k,  'conv': c5k},
    },
    'best_fit': {
        'model': best_model, 'r_squared': best_r2,
        'asymptote_at_1e6': asymptote,
        'converges_to_1': bool(abs(asymptote - 1.0) < 0.01) if asymptote else None,
        'params': fit_results.get(best_model, {}).get('params'),
    },
    'gateway_structure': {
        'S3B_S4_exact': pairing_exact, 'S3B_S4_max_dev': max_pair_dev,
        'ordering_breaks': len(ordering_breaks),
        'S1_S5_ratio_n1': float(ratios[0]),
        'mu_scaling_exponent': mu_fit.get('b') if isinstance(mu_fit, dict) else None,
    },
    'sigma_comparative': {
        'discriminable': discriminable,
        'mean_diff_0p5_minus_0p4': mean_diff, 'max_abs_diff': max_abs_diff,
    },
    'jrs_controls': {
        'rh_band1_mean':      float(np.mean(rh_b1)),
        'gue_band1_mean':     float(np.mean(gue_b1)),
        'poisson_band1_mean': float(np.mean(poi_b1)),
        'rh_vs_gue':          float(np.mean(rh_b1) - np.mean(gue_b1)),
        'rh_vs_poisson':      float(np.mean(rh_b1) - np.mean(poi_b1)),
    },
    'n_zeros_scanned': len(scan_records),
    'total_elapsed_s':  time.time() - t0_total,
}
json.dump(summary, open("phase48_results.json", "w"), indent=2)

print(f"\n  Total elapsed: {time.time()-t0_total:.1f}s")
print("\nOutput files:")
for f in ["phase48_calibration.json", "phase48_scan.json", "phase48_fit.json",
          "phase48_gateway_structure.json", "phase48_sigma_comparative.json",
          "phase48_spotcheck_prep.json", "phase48_results.json"]:
    print(f"  {f}")
print("\nNext: send phase48_spotcheck_prep.json to Claude Desktop for")
print("CAILculator verification + Chavez Transform on convergence series.")
