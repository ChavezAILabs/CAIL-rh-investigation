"""
RH Phase 14C -- Color Group Spectral Survey
============================================
Tests whether the five Canonical Six P-vector projections differ in their
log-prime DFT spectral signatures, and whether Color Group membership
predicts spectral similarity.

Canonical Six P-vectors (8D, acting on embed_pair output):
  v1 = (0, 1, 0, 0, 0, 0,-1, 0)  --> P1(g1,g2) = g1*g2/(g1+g2)  [harmonic mean / 2... actually g1*g2/s not /2]
  v2 = (0, 0, 0, 1,-1, 0, 0, 0)  --> P2(g1,g2) = -(g1^2+g2^2)/(2*s)
  v3 = (0, 0, 0,-1, 1, 0, 0, 0)  --> P3(g1,g2) = (g1^2+g2^2)/(2*s) = -P2
  v4 = (0, 1, 0, 0, 0, 0, 1, 0)  --> P4(g1,g2) = g2 + g2/s = g2*(s+1)/s
  v5 = (0, 0, 1, 0, 0, 1, 0, 0)  --> P5(g1,g2) = (g1-g2) + g1/s

embed_pair(g1,g2) = [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)^2/s]
  where s = g1+g2

Color Group structure (E6xA2 decomposition):
  CG1: v1, v4  (Patterns 1, 4)
  CG2: v2, v5  (Patterns 2, 5)
  CG3: v3      (Pattern 3, antipodal to v2)

Hypothesis: P-vectors in the same Color Group share more spectral similarity
(log-prime SNR profile correlation) than P-vectors across groups.

Notes on scale-dependence:
  P1 = g1*g2/(g1+g2): scale-dependent (units of gap size)
  P2 = -(g1^2+g2^2)/(2*s): scale-dependent (units of gap^2/gap = gap)
  P3 = -P2: scale-dependent, antipodal to P2
  P4 = g2 + g2/s: scale-dependent (dominated by raw g2)
  P5 = (g1-g2) + g1/s: scale-dependent (dominated by gap difference)

For DFT, subtract global mean to remove DC. The DFT then measures oscillatory
content, but P4/P5 will be dominated by the secular height-dependent trend.
All are tested; results interpreted with scale-dependence in mind.
"""

import json, math, random, os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
    zeros = json.load(f)
with open(os.path.join(script_dir, 'rh_gaps_10k.json')) as f:
    gaps_all = json.load(f)

N_ZEROS  = len(zeros)
mean_gap = sum(gaps_all) / len(gaps_all)

# -- P-vector projections -----------------------------------------------------
def embed_pair(g1, g2):
    s = g1 + g2
    return [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)**2/s]

P_VECTORS = {
    'P1': (0, 1, 0, 0, 0, 0,-1, 0),
    'P2': (0, 0, 0, 1,-1, 0, 0, 0),
    'P3': (0, 0, 0,-1, 1, 0, 0, 0),
    'P4': (0, 1, 0, 0, 0, 0, 1, 0),
    'P5': (0, 0, 1, 0, 0, 1, 0, 0),
}

COLOR_GROUPS = {
    'CG1': ['P1', 'P4'],
    'CG2': ['P2', 'P5'],
    'CG3': ['P3'],
}

def proj(g1, g2, v):
    ep = embed_pair(g1, g2)
    return sum(ep[i]*v[i] for i in range(8))

def proj_sequence(gaps, v):
    return [proj(gaps[i], gaps[i+1], v) for i in range(len(gaps)-1)]

# -- DFT power ----------------------------------------------------------------
def dft_power(seq, heights, omega):
    mu = sum(seq)/len(seq)
    re = sum((x-mu)*math.cos(omega*t) for x,t in zip(seq,heights))
    im = sum((x-mu)*math.sin(omega*t) for x,t in zip(seq,heights))
    n  = len(seq)
    return (re/n)**2 + (im/n)**2

# -- Samplers -----------------------------------------------------------------
def sample_wigner(n, mean, seed):
    rng = random.Random(seed)
    scale = math.sqrt(2.0/math.pi)
    samples = []
    while len(samples) < n:
        u = rng.random()
        if u == 0: continue
        samples.append(scale * math.sqrt(-2.0*math.log(u)) * mean)
    return samples

def shuffle_seq(seq, seed):
    rng = random.Random(seed)
    s = seq[:]
    rng.shuffle(s)
    return s

# -- Frequency grid -----------------------------------------------------------
PRIMES      = [2, 3, 5, 7, 11, 13, 17, 19, 23]
prime_omegas = {p: math.log(p) for p in PRIMES}
log_vals    = sorted(prime_omegas.values())
ctrl_omegas = [(log_vals[i]+log_vals[i+1])/2 for i in range(len(log_vals)-1)]
all_omegas  = list(prime_omegas.values()) + ctrl_omegas
SEEDS       = [1, 2, 3]
heights     = [zeros[i+1] for i in range(len(gaps_all)-1)]  # 9,998 heights

# Phase 13A spacing ratio SNR (for comparison baseline)
sr_snr_ref = {2:0.84, 3:7.6, 5:76.1, 7:139.7, 11:231.2, 13:245.4,
              17:205.9, 19:211.5, 23:185.1}

print("="*72)
print("PHASE 14C -- COLOR GROUP SPECTRAL SURVEY")
print("="*72)
print(f"P-vectors: {list(P_VECTORS.keys())}")
print(f"Color groups: CG1={COLOR_GROUPS['CG1']}  CG2={COLOR_GROUPS['CG2']}  CG3={COLOR_GROUPS['CG3']}")
print(f"Antipodal pair: P2 (CG2) <-> P3 (CG3)")

# -- Compute SNR for each P-vector -------------------------------------------
all_snr = {}   # {pname: {prime: snr}}

for pname, v in P_VECTORS.items():
    print(f"\nComputing {pname}...")
    act_seq  = proj_sequence(gaps_all, v)

    # Noise floor from controls
    gue_profs = []
    for seed in SEEDS:
        g_gaps = sample_wigner(len(gaps_all), mean_gap, seed)
        g_seq  = proj_sequence(g_gaps, v)
        gue_profs.append({om: dft_power(g_seq, heights, om) for om in all_omegas})
    gue_avg = {om: sum(d[om] for d in gue_profs)/len(SEEDS) for om in all_omegas}

    shuf_profs = []
    for seed in SEEDS:
        s_seq = shuffle_seq(act_seq, seed)
        shuf_profs.append({om: dft_power(s_seq, heights, om) for om in all_omegas})
    shuf_avg = {om: sum(d[om] for d in shuf_profs)/len(SEEDS) for om in all_omegas}

    act_prof  = {om: dft_power(act_seq, heights, om) for om in all_omegas}

    noise_act  = sum(act_prof[om]  for om in ctrl_omegas) / len(ctrl_omegas)
    noise_gue  = sum(gue_avg[om]   for om in ctrl_omegas) / len(ctrl_omegas)
    noise_shuf = sum(shuf_avg[om]  for om in ctrl_omegas) / len(ctrl_omegas)

    snr_dict = {}
    for p in PRIMES:
        om       = prime_omegas[p]
        snr_act  = act_prof[om]  / noise_act  if noise_act  > 0 else 0
        snr_gue  = gue_avg[om]   / noise_gue  if noise_gue  > 0 else 0
        snr_shuf = shuf_avg[om]  / noise_shuf if noise_shuf > 0 else 0
        snr_dict[p] = {'act': snr_act, 'gue': snr_gue, 'shuf': snr_shuf,
                       'signal': snr_act>2.0 and snr_act>1.5*max(snr_gue,snr_shuf)}
    all_snr[pname] = snr_dict

# -- Print full SNR table -----------------------------------------------------
print(f"\n{'='*72}")
print(f"SNR at log-prime frequencies: all P-vectors vs spacing ratio (13A)")
print(f"{'='*72}")
print(f"{'Prime':>6}  {'log(p)':>7}  {'P1':>8}  {'P2':>8}  {'P3':>8}  "
      f"{'P4':>8}  {'P5':>8}  {'SR(13A)':>9}")
print(f"{'-'*72}")

for p in PRIMES:
    om = prime_omegas[p]
    row = f"{p:>6}  {om:>7.4f}"
    for pname in ['P1','P2','P3','P4','P5']:
        row += f"  {all_snr[pname][p]['act']:>8.2f}"
    row += f"  {sr_snr_ref.get(p,'--'):>9}"
    print(row)

# -- Signal detection per P-vector --------------------------------------------
print(f"\nSignal primes per P-vector (SNR>2 AND >1.5x controls):")
for pname in P_VECTORS:
    sigs = [p for p in PRIMES if all_snr[pname][p]['signal']]
    print(f"  {pname}: {sigs if sigs else 'None'}")

# -- Color Group spectral similarity -----------------------------------------
print(f"\n{'='*72}")
print(f"Color Group spectral similarity (Pearson r of SNR profiles)")
print(f"{'='*72}")
print(f"Hypothesis: within-group r > cross-group r")

def snr_profile(pname):
    return [all_snr[pname][p]['act'] for p in PRIMES]

def pearson_r(x, y):
    n  = len(x)
    mx, my = sum(x)/n, sum(y)/n
    num = sum((x[i]-mx)*(y[i]-my) for i in range(n))
    dx  = math.sqrt(sum((x[i]-mx)**2 for i in range(n)))
    dy  = math.sqrt(sum((y[i]-my)**2 for i in range(n)))
    return num/(dx*dy) if dx*dy else 0.0

pnames = list(P_VECTORS.keys())
print(f"\nPairwise SNR profile correlations:")
print(f"{'':>5}", end="")
for q in pnames:
    print(f"  {q:>8}", end="")
print()
for p in pnames:
    print(f"{p:>5}", end="")
    for q in pnames:
        r = pearson_r(snr_profile(p), snr_profile(q))
        # Label within-group pairs
        same_group = any(p in g and q in g for g in COLOR_GROUPS.values())
        marker = '*' if same_group and p != q else ' '
        print(f"  {r:>7.4f}{marker}", end="")
    print()

print(f"\n* = within same Color Group")
print(f"\nWithin-group pairs and their r values:")
for gname, members in COLOR_GROUPS.items():
    for i in range(len(members)):
        for j in range(i+1, len(members)):
            p, q = members[i], members[j]
            r = pearson_r(snr_profile(p), snr_profile(q))
            print(f"  {gname}: r({p},{q}) = {r:.4f}")

print(f"\nCross-group pairs (sample):")
cross_pairs = [('P1','P2'), ('P1','P3'), ('P2','P4'), ('P3','P5'), ('P1','P5')]
for p, q in cross_pairs:
    r = pearson_r(snr_profile(p), snr_profile(q))
    print(f"  r({p},{q}) = {r:.4f}")

# -- The P2/P3 antipodal: confirm identical SNR profile ----------------------
print(f"\n{'='*72}")
print(f"P2/P3 Antipodal Pair: SNR profile comparison")
print(f"{'='*72}")
print(f"{'Prime':>6}  {'P2 SNR':>10}  {'P3 SNR':>10}  {'Ratio P3/P2':>12}  {'Equal?':>8}")
all_equal = True
for p in PRIMES:
    s2 = all_snr['P2'][p]['act']
    s3 = all_snr['P3'][p]['act']
    ratio = s3/s2 if s2 > 0 else float('inf')
    equal = abs(ratio - 1.0) < 1e-6
    if not equal: all_equal = False
    print(f"{p:>6}  {s2:>10.4f}  {s3:>10.4f}  {ratio:>12.8f}  {'YES' if equal else 'NO'}")
print(f"\nP2/P3 spectral isometry confirmed: {'YES' if all_equal else 'NO'}")

# -- Save results -------------------------------------------------------------
out = os.path.join(script_dir, 'p14c_results.json')
with open(out, 'w') as f:
    json.dump({
        'phase': '14C',
        'p_vectors': {k: list(v) for k,v in P_VECTORS.items()},
        'color_groups': COLOR_GROUPS,
        'primes': PRIMES,
        'snr': {pn: {str(p): all_snr[pn][p] for p in PRIMES}
                for pn in P_VECTORS},
        'snr_profiles': {pn: snr_profile(pn) for pn in P_VECTORS},
        'pairwise_r': {
            f'{p}_{q}': pearson_r(snr_profile(p), snr_profile(q))
            for p in pnames for q in pnames
        },
        'phase13a_sr_snr': sr_snr_ref,
    }, f, indent=2)
print(f"\nResults saved to p14c_results.json")
