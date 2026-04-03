
import numpy as np
import json

def detect_bilateral_pairs(v, threshold=0.01):
    pairs = 0
    n = len(v)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(v[i] + v[j]) < threshold or abs(v[i] - v[j]) < threshold:
                pairs += 1
    return pairs

def compute_variance(v):
    return float(np.var(v))

def compute_symmetry(v):
    mid = len(v) // 2
    left = np.array(v[:mid])
    right = np.array(v[mid:])[::-1]
    return float(np.mean(np.abs(left - right)))

print("Loading vectors...")
with open('phase56_density_scan_vectors.json', 'r') as f:
    vectors = json.load(f)

results = []
for v in vectors:
    var = compute_variance(v['F_vector'])
    pairs = detect_bilateral_pairs(v['F_vector'])
    symm = compute_symmetry(v['F_vector'])
    results.append({
        "n": v['n'],
        "gamma": v['gamma'],
        "variance": var,
        "bilateral_pairs": pairs,
        "symmetry_residual": symm,
        "energy": v['energy']
    })

with open("phase56_structural_scan_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Processed {len(results)} vectors for structural profile.")
