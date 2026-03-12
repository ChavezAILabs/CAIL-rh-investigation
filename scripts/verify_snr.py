import json
import math
import cmath

def get_snr(zeros, primes):
    def get_power(omega):
        sum_val = complex(0, 0)
        for gamma in zeros:
            sum_val += cmath.exp(complex(0, omega * gamma))
        return abs(sum_val)**2

    # Get power at prime frequencies
    powers = {p: get_power(math.log(p)) for p in primes}

    # Get noise: average power at midpoints between prime frequencies
    # log(2) to log(23) range: 0.69 to 3.13
    # Use 8 control points spread out
    control_omegas = [0.8, 1.2, 1.5, 1.8, 2.2, 2.5, 2.8, 3.0]
    control_powers = [get_power(o) for o in control_omegas]
    noise = sum(control_powers) / len(control_powers)

    snr = {p: powers[p] / noise for p in primes}
    return snr

def main():
    with open('C:\\dev\\projects\\Experiments_January_2026\\Primes_2026\\zeros_chi4_2k.json', 'r') as f:
        chi4_zeros = json.load(f)
    with open('C:\\dev\\projects\\Experiments_January_2026\\Primes_2026\\zeros_chi3_2k.json', 'r') as f:
        chi3_zeros = json.load(f)

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    print("Computing SNR for chi4 (ramified at 2)...")
    chi4_snr = get_snr(chi4_zeros, primes)
    
    print("Computing SNR for chi3 (ramified at 3)...")
    chi3_snr = get_snr(chi3_zeros, primes)

    print("\nSNR Results (omega = log(p)):")
    print(f"{'p':>2} | {'chi4 SNR':>10} | {'chi3 SNR':>10}")
    print("-" * 30)
    for p in primes:
        print(f"{p:>2} | {chi4_snr[p]:>10.4f} | {chi3_snr[p]:>10.4f}")

    print("\nRoute B Verification:")
    print(f"chi4 p=2 SNR: {chi4_snr[2]:.4f} (Expected: < 1.0)")
    print(f"chi3 p=3 SNR: {chi3_snr[3]:.4f} (Expected: < 1.0)")
    
    chi4_unramified = [p for p in primes if p != 2]
    chi3_unramified = [p for p in primes if p != 3]
    
    avg_chi4_un = sum(chi4_snr[p] for p in chi4_unramified) / len(chi4_unramified)
    avg_chi3_un = sum(chi3_snr[p] for p in chi3_unramified) / len(chi3_unramified)
    
    print(f"chi4 Avg Unramified SNR: {avg_chi4_un:.4f}")
    print(f"chi3 Avg Unramified SNR: {avg_chi3_un:.4f}")

if __name__ == "__main__":
    main()
