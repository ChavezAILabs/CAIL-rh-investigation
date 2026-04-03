
import json
import subprocess
import time

def run_zdtp(vector_16d):
    # As an agent, I should probably not try to call 'gemini-cli' inside a subprocess
    # because the environment might not be set up for it.
    # Instead, I will use the 'mcp_cailculator_zdtp_transmit' tool directly in my next turns.
    # I'll just save the vectors and process them in batches via my own tool calls.
    return {"error": "Subprocess tool calls are unreliable. Batching manually."}

print("Loading vectors...")
with open('phase56_density_scan_vectors.json', 'r') as f:
    vectors = json.load(f)

results = []
t0 = time.time()

print(f"Starting ZDTP cascade for {len(vectors)} vectors...")
for i, v in enumerate(vectors):
    print(f"[{i+1}/{len(vectors)}] Processing n={v['n']} (gamma={v['gamma']:.2f})...")
    z_res = run_zdtp(v['F_vector'])
    
    if "convergence" in z_res:
        conv = z_res["convergence"]["score"]
        results.append({
            "n": v["n"],
            "gamma": v["gamma"],
            "convergence": conv,
            "mean_magnitude": z_res["convergence"]["mean_magnitude"],
            "energy": v["energy"]
        })
        print(f"  Success: conv={conv:.4f}")
    else:
        print(f"  Error: {z_res.get('error', 'Unknown error')}")
        results.append({
            "n": v["n"],
            "gamma": v["gamma"],
            "error": z_res.get("error", "Unknown error")
        })
    
    # Save partial results
    if (i + 1) % 10 == 0:
        with open("phase56_density_scan_results_partial.json", "w") as f:
            json.dump(results, f, indent=2)

with open("phase56_density_scan_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Finished in {time.time()-t0:.1f}s. Results saved to phase56_density_scan_results.json")
