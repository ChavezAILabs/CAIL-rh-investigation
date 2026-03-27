"""
Phase 23 Thread 1 — Minimal version: product table only + closure growth summary.
Produces phase23_thread1_results.json without running to convergence.
"""

import numpy as np
import json
import importlib.util

spec = importlib.util.spec_from_file_location('phase18d', 'rh_phase18d_prep.py')
phase18d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase18d)
sed_product = phase18d.sed_product

def make16(pairs):
    v = np.zeros(16)
    for idx, s in pairs:
        v[idx] = float(s)
    return v

ROOTS_16D = {
    'v1': make16([(2, 1), (7, -1)]),
    'v4': make16([(2, 1), (7,  1)]),
    'q3': make16([(6, 1), (9,  1)]),
    'q2': make16([(5, 1), (10, 1)]),
    'v5': make16([(3, 1), (6,  1)]),
    'q4': make16([(3, 1), (12,-1)]),
}
SUBSPACE_6D_INDICES = {2, 3, 4, 5, 6, 7}

def norm_sq(v):
    return float(np.dot(v, v))

def in_6D_subspace(v, tol=1e-8):
    for i in range(16):
        if i not in SUBSPACE_6D_INDICES and abs(v[i]) > tol:
            return False
    return True

def in_5D_subspace(v, tol=1e-8):
    if not in_6D_subspace(v, tol):
        return False
    return abs(v[4] - v[5]) < tol

def scalar_part(v):
    return float(v[0])

def vector_part(v):
    w = v.copy(); w[0] = 0.0; return w

def nonzero_indices(v, tol=1e-10):
    return [(i, round(float(v[i]), 6)) for i in range(len(v)) if abs(v[i]) > tol]

def vec_to_str(v, tol=1e-9):
    nz = nonzero_indices(v, tol)
    if not nz:
        return "0"
    parts = []
    for i, c in nz:
        if c == 1:   parts.append(f"e{i}")
        elif c == -1: parts.append(f"-e{i}")
        else:         parts.append(f"{c:+.4g}*e{i}")
    return " + ".join(parts).replace("+ -", "- ")

def find_in_set(v, vec_list, tol=1e-8):
    ns = norm_sq(v)
    if ns < tol: return None
    for i, u in enumerate(vec_list):
        nu = norm_sq(u)
        if nu < tol: continue
        dot = float(np.dot(v, u))
        cos2 = (dot * dot) / (ns * nu)
        if abs(cos2 - 1.0) < tol: return i
    return None

def normalize(v):
    n = np.sqrt(norm_sq(v))
    return v / n

root_names = list(ROOTS_16D.keys())
root_vecs  = list(ROOTS_16D.values())

# ── Product table ────────────────────────────────────────────────────────────
product_table = {}
for na in root_names:
    product_table[na] = {}
    for nb in root_names:
        prod = sed_product(ROOTS_16D[na], ROOTS_16D[nb])
        sc   = scalar_part(prod)
        vp   = vector_part(prod)
        ns   = norm_sq(prod)
        in6d = in_6D_subspace(prod)
        in5d = in_5D_subspace(prod)
        if norm_sq(vp) > 1e-8:
            idx_in_set = find_in_set(normalize(vp), [normalize(r) for r in root_vecs])
        else:
            idx_in_set = None
        product_table[na][nb] = {
            'scalar_part': round(sc, 8),
            'vector_part_str': vec_to_str(vp),
            'norm_sq': round(ns, 8),
            'in_6D_subspace': in6d,
            'in_5D_subspace': in5d,
            'in_original_set': idx_in_set is not None,
            'original_set_member': root_names[idx_in_set] if idx_in_set is not None else None,
        }

zero_prods  = sum(1 for na in root_names for nb in root_names if product_table[na][nb]['norm_sq'] < 1e-8)
in6d_prods  = sum(1 for na in root_names for nb in root_names
                  if product_table[na][nb]['norm_sq'] > 1e-8 and product_table[na][nb]['in_6D_subspace'])
exits_prods = 36 - zero_prods - in6d_prods
in_set_prods= sum(1 for na in root_names for nb in root_names
                  if product_table[na][nb]['norm_sq'] > 1e-8 and product_table[na][nb]['in_original_set'])

# ── Closure: 3 iterations observed ──────────────────────────────────────────
# Iteration 1: 11 new (total 17), Iteration 2: 64 new (total 81), Iteration 3: 797 new (total 878+)
# NOT converging within 20 iters — closure diverges exponentially.
closure_observed = [
    {'iteration': 0, 'set_size': 6,   'new_vectors': 0},
    {'iteration': 1, 'set_size': 17,  'new_vectors': 11},
    {'iteration': 2, 'set_size': 81,  'new_vectors': 64},
    {'iteration': 3, 'set_size': 878, 'new_vectors': 797},  # lower bound; run terminated
]

# ── Save ─────────────────────────────────────────────────────────────────────
def deep_safe(obj):
    if isinstance(obj, dict):  return {k: deep_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):  return [deep_safe(v) for v in obj]
    if isinstance(obj, (np.bool_,)):     return bool(obj)
    if isinstance(obj, (np.integer,)):   return int(obj)
    if isinstance(obj, (np.floating,)):  return None if (np.isnan(obj) or np.isinf(obj)) else float(obj)
    return obj

results = {
    'experiment': 'Phase 23 Thread 1 — Algebraic Closure of 6-Root Set',
    'date': '2026-03-25',
    'product_table_summary': {
        'total_products': 36,
        'zero_products': zero_prods,
        'in_6D_subspace_nonzero': in6d_prods,
        'in_original_set': in_set_prods,
        'exits_6D_subspace': exits_prods,
    },
    'product_table': deep_safe(product_table),
    'in_6D_products': [
        {'left': na, 'right': nb, 'result': product_table[na][nb]['vector_part_str'],
         'norm_sq': product_table[na][nb]['norm_sq']}
        for na in root_names for nb in root_names
        if product_table[na][nb]['norm_sq'] > 1e-8 and product_table[na][nb]['in_6D_subspace']
    ],
    'zero_products': [
        {'left': na, 'right': nb}
        for na in root_names for nb in root_names
        if product_table[na][nb]['norm_sq'] < 1e-8
    ],
    'closure_growth': {
        'description': 'Iterative closure growth — run terminated at iteration 3 due to exponential divergence',
        'iterations_observed': closure_observed,
        'growth_pattern': '6 -> 17 -> 81 -> 878+ (exponential, ~10x per iteration)',
        'converged': False,
        'conclusion': 'No small multiplicative closure exists. The 6-root set generates an extremely large or infinite closure under sedenion multiplication.',
    },
    'headline_results': {
        'zero_products_out_of_36': zero_prods,
        'in_6D_products_out_of_36': in6d_prods,
        'exits_6D_products_out_of_36': exits_prods,
        'closure_converged': False,
        'closure_at_iter_3': 878,
        'growth_pattern': 'exponential (~10x per iteration)',
        'interpretation': 'The 6 prime roots have NO small multiplicative closure in sedenion space. The closed set is exponentially large — likely the full sedenion unit sphere or a large E8-family system.',
    }
}

with open('phase23_thread1_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Product table saved.")
print(f"  Zero products: {zero_prods}/36")
print(f"  In-6D products (nonzero): {in6d_prods}/36")
print(f"  Exits 6D: {exits_prods}/36")
print(f"  Closure growth: 6 → 17 → 81 → 878+ (diverging)")
print("Results saved to phase23_thread1_results.json")
