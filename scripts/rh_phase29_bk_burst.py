"""
Phase 29 — Claude Code computation script
Produces phase29_results.json for Claude Desktop/CAILculator analysis.

Claude Code's job: pure math, pure Python, no MCP.
Claude Desktop's job: CAILculator on the output sequences.

Run from: C:\dev\projects\Experiments_January_2026\Primes_2026\rh_investigation
Save output to: phase29_results.json
"""
import numpy as np
from mpmath import mp, zetazero
from scipy.stats import linregress, binomtest
import json, time
mp.dps = 25

# ============================================================
# SEDENION ENGINE (from rh_phase21b.py)
# ============================================================
def cd_conj(v):
    c = list(v); c[0] = v[0]
    for i in range(1, len(v)): c[i] = -v[i]
    return c

def cd_mul(a, b):
    n = len(a)
    if n == 1: return [a[0]*b[0]]
    h = n // 2
    a1,a2,b1,b2 = a[:h],a[h:],b[:h],b[h:]
    c1 = [x-y for x,y in zip(cd_mul(a1,b1), cd_mul(cd_conj(b2),a2))]
    c2 = [x+y for x,y in zip(cd_mul(b2,a1), cd_mul(a2,cd_conj(b1)))]
    return c1+c2

def norm_sq(v): return sum(x*x for x in v)

def make16(pairs):
    v=[0.0]*16
    for i,val in pairs: v[i]=float(val)
    return v

sqrt2 = np.sqrt(2.0)

# Root vectors for primes 2–31 in 16D sedenion space
# Core 6 (AIEX-001a embedding primes): positions verified against E8 shell
ROOT_16D_BASE = {
    2:  make16([(3, 1.0),(12,-1.0)]),
    3:  make16([(5, 1.0),(10, 1.0)]),
    5:  make16([(3, 1.0),(6,  1.0)]),
    7:  make16([(2, 1.0),(7, -1.0)]),
    11: make16([(2, 1.0),(7,  1.0)]),
    13: make16([(6, 1.0),(9,  1.0)]),
    # Extended primes: next available E8-adjacent positions
    17: make16([(1, 1.0),(14, 1.0)]),
    19: make16([(1, 1.0),(14,-1.0)]),
    23: make16([(4, 1.0),(11, 1.0)]),
    29: make16([(4, 1.0),(11,-1.0)]),
    31: make16([(8, 1.0),(15, 1.0)]),
}

def F_16d(t, sigma=0.5, primes=None):
    if primes is None: primes = [2,3,5,7,11,13]
    r = make16([(0,1.0)])
    for p in primes:
        theta = t*np.log(p)
        rp = ROOT_16D_BASE[p]; rn = np.sqrt(norm_sq(rp))
        f = [0.0]*16; f[0] = np.cos(theta)
        for i in range(16): f[i] += np.sin(theta)*rp[i]/rn
        r = cd_mul(r, f)
    r[4] += (sigma-0.5)/sqrt2
    r[5] -= (sigma-0.5)/sqrt2
    return r

def H_BK(t, sigma=0.5, eps=1e-6):
    """BK Hamiltonian = numerical derivative dF/dt"""
    Fp = F_16d(t+eps, sigma)
    Fm = F_16d(t-eps, sigma)
    return [(Fp[i]-Fm[i])/(2*eps) for i in range(16)]

def commutator_norm(t, sigma=0.5):
    F = F_16d(t, sigma)
    H = H_BK(t, sigma)
    FH = cd_mul(F, H); HF = cd_mul(H, F)
    return float(np.sqrt(sum((FH[i]-HF[i])**2 for i in range(16))))

def Tr_BK(t, primes=None):
    if primes is None: primes = [2,3,5,7,11,13]
    return float(sum((np.log(p)/np.sqrt(p))*np.cos(t*np.log(p)) for p in primes))

def Weil_RHS(primes=None):
    if primes is None: primes = [2,3,5,7,11,13]
    return -sum(np.log(p)/np.sqrt(p) for p in primes)

def V_BK(t, sigma=0.5):
    F = F_16d(t, sigma); ns = norm_sq(F)
    if ns < 1e-20: return 0.0
    gn = []
    for p in [2, 13]:
        rp = ROOT_16D_BASE[p]; rn = np.sqrt(norm_sq(rp))
        probe = [x/rn for x in rp]
        prod = cd_mul(F, probe)
        gn.append(norm_sq(prod)/ns)
    return float(np.var(gn))

# ============================================================
# DATA FETCH
# ============================================================
print("="*60)
print("PHASE 29 — Berry-Keating Sedenion Burst")
print("="*60)
import os as _os
_CACHE = 'rh_zeros.json'
if _os.path.exists(_CACHE):
    import json as _json
    print(f"Loading zeros from cache: {_CACHE}", flush=True)
    t0 = time.time()
    zeros = _json.load(open(_CACHE))[:500]
    print(f"Done in {time.time()-t0:.1f}s. t_1={zeros[0]:.4f} .. t_500={zeros[499]:.4f}")
else:
    print(f"Fetching 500 zeros...", flush=True)
    t0 = time.time()
    zeros = [float(zetazero(n).imag) for n in range(1, 501)]
    print(f"Done in {time.time()-t0:.1f}s. t_1={zeros[0]:.4f} .. t_500={zeros[499]:.4f}")
midpoints = [0.5*(zeros[i]+zeros[i+1]) for i in range(499)]

# ============================================================
# THREAD 1: Weil Convergence
# ============================================================
print("\n" + "="*60)
print("THREAD 1: Weil Explicit Formula Convergence")
print("="*60)

PRIME_SETS = {
    6:  [2,3,5,7,11,13],
    7:  [2,3,5,7,11,13,17],
    8:  [2,3,5,7,11,13,17,19],
    9:  [2,3,5,7,11,13,17,19,23],
    10: [2,3,5,7,11,13,17,19,23,29],
    11: [2,3,5,7,11,13,17,19,23,29,31],
}

thread1 = {}
for n_primes, pset in PRIME_SETS.items():
    rhs = Weil_RHS(pset)
    tr_zeros = [Tr_BK(t, pset) for t in zeros[:100]]
    tr_mids  = [Tr_BK(t, pset) for t in midpoints[:100]]
    mean_z = float(np.mean(tr_zeros))
    mean_m = float(np.mean(tr_mids))
    ratio  = mean_z / rhs if abs(rhs) > 1e-10 else 0.0
    neg_frac = sum(1 for x in tr_zeros if x < 0) / 100
    thread1[str(n_primes)] = {
        'primes': pset,
        'weil_rhs': float(rhs),
        'mean_zeros': mean_z,
        'mean_mids': mean_m,
        'ratio': float(ratio),
        'fraction_negative': neg_frac,
        'Tr_zeros_n100': tr_zeros,
        'Tr_mids_n100': tr_mids,
    }
    print(f"  {n_primes:2d} primes: Weil_RHS={rhs:.4f}  mean_z={mean_z:.4f}  "
          f"ratio={ratio:.4f}  neg={neg_frac:.2f}")

# ============================================================
# THREAD 2: Uncertainty Principle Scaling
# ============================================================
print("\n" + "="*60)
print("THREAD 2: Sedenion Uncertainty Principle")
print("="*60)

print("  Computing commutator norms for 100 zeros...", flush=True)
CN_100 = [commutator_norm(t) for t in zeros[:100]]
print(f"  Done. mean={np.mean(CN_100):.4f} ± {np.std(CN_100):.4f}")

# Linear regression: CN ~ a*t + b
slope, intercept, r, p_val, se = linregress(zeros[:100], CN_100)
hbar_sed = slope
print(f"  Fit: CN = {slope:.4f}*t + {intercept:.4f}")
print(f"  R2={r**2:.4f}  p={p_val:.4f}  hbar_sed={hbar_sed:.4f}")

thread2 = {
    'CN_100': CN_100,
    'zero_heights_100': zeros[:100],
    'linear_fit': {
        'slope': float(slope),
        'intercept': float(intercept),
        'R2': float(r**2),
        'p_value': float(p_val),
        'std_err': float(se),
        'hbar_sed': float(hbar_sed),
    }
}

# ============================================================
# THREAD 3: 500-Zero BK Signature
# ============================================================
print("\n" + "="*60)
print("THREAD 3: 500-Zero BK Signature")
print("="*60)

print("  Computing Tr_BK for 500 zeros + 499 midpoints...", flush=True)
Tr_500_z = [Tr_BK(t) for t in zeros]
Tr_499_m = [Tr_BK(t) for t in midpoints]
neg_500   = sum(1 for x in Tr_500_z if x < 0)
print(f"  Tr_BK < 0 at {neg_500}/500 zeros ({neg_500/5:.1f}%)")

# Binomial test: is 90% negativity significant?
btest = binomtest(neg_500, 500, 0.5, alternative='greater')
print(f"  Binomial test (H0: p=0.5): p-value = {btest.pvalue:.2e}")

print("  Computing V_BK for 500 zeros + 499 midpoints...", flush=True)
VBK_500_z = [V_BK(t) for t in zeros]
VBK_499_m = [V_BK(t) for t in midpoints]
vbk_count = sum(1 for i in range(499) if VBK_500_z[i] > VBK_499_m[i])
print(f"  V_BK zeros > midpoints: {vbk_count}/499")

# Mean and std
print(f"  Tr_BK zeros:  mean={np.mean(Tr_500_z):.4f} ± {np.std(Tr_500_z):.4f}")
print(f"  Tr_BK mids:   mean={np.mean(Tr_499_m):.4f} ± {np.std(Tr_499_m):.4f}")
print(f"  V_BK zeros:   mean={np.mean(VBK_500_z):.6f} ± {np.std(VBK_500_z):.6f}")
print(f"  V_BK mids:    mean={np.mean(VBK_499_m):.6f} ± {np.std(VBK_499_m):.6f}")

# The algebraic identity check: p=5,7,11 gateway norms
print("\n  Algebraic identity check: ||F×r_p||/||F|| for p=5,7,11 vs p=2,13")
for p in [2,5,7,11,13]:
    vals = []
    for t in zeros[:50]:
        F = F_16d(t); ns = norm_sq(F)
        rp = ROOT_16D_BASE[p]; rn = np.sqrt(norm_sq(rp))
        probe = [x/rn for x in rp]
        prod = cd_mul(F, probe)
        vals.append(np.sqrt(norm_sq(prod)/ns))
    print(f"    p={p:2d}: mean={np.mean(vals):.8f} ± {np.std(vals):.8f}")

thread3 = {
    'Tr_zeros_500': Tr_500_z,
    'Tr_mids_499': Tr_499_m,
    'VBK_zeros_500': VBK_500_z,
    'VBK_mids_499': VBK_499_m,
    'fraction_Tr_negative_500': float(neg_500/500),
    'binomial_pvalue': float(btest.pvalue),
    'VBK_count_zeros_gt_mids': int(vbk_count),
    'VBK_fraction_zeros_gt_mids': float(vbk_count/499),
    'stats': {
        'Tr_zeros_mean': float(np.mean(Tr_500_z)),
        'Tr_zeros_std': float(np.std(Tr_500_z)),
        'Tr_mids_mean': float(np.mean(Tr_499_m)),
        'Tr_mids_std': float(np.std(Tr_499_m)),
        'VBK_zeros_mean': float(np.mean(VBK_500_z)),
        'VBK_zeros_std': float(np.std(VBK_500_z)),
        'VBK_mids_mean': float(np.mean(VBK_499_m)),
        'VBK_mids_std': float(np.std(VBK_499_m)),
    }
}

# ============================================================
# SAVE OUTPUT
# ============================================================
results = {
    'metadata': {
        'phase': 29,
        'date': '2026-03-25',
        'zeros_computed': 500,
        'script': 'rh_phase29_bk_burst.py',
    },
    'thread1_weil': thread1,
    'thread2_uncertainty': thread2,
    'thread3_500zero': thread3,
}

with open('phase29_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\n" + "="*60)
print("Saved: phase29_results.json")
print("="*60)
print("\nHANDOFF TO CLAUDE DESKTOP:")
print("  Load phase29_results.json")
print("  Run CAILculator on the following keys:")
print("  - thread1_weil[*].Tr_zeros_n100  (analyze_dataset)")
print("  - thread2_uncertainty.CN_100     (analyze_dataset + detect_patterns)")
print("  - thread3_500zero.Tr_zeros_500   (analyze_dataset — 500 points)")
print("  - thread3_500zero.VBK_zeros_500  (detect_patterns)")
print("  - zdtp_transmit on F(rho_1) for each prime set")
