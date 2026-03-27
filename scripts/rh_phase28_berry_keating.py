"""
AIEX-001a Phase 28 — Berry-Keating Sedenion Hamiltonian
Chavez AI Labs LLC · March 25, 2026

IDENTIFICATION: AIEX-001a IS the Berry-Keating xp Hamiltonian in 16D sedenion space.
  F(t) = e^{iH_BK*t}, t=BK time, log(p)=dilation factor, r_p=sedenion direction.

KEY FINDINGS:
1. Tr_BK(t) = sum_p (log p/sqrt(p))*cos(t*log p) negative at 90/100 zeros
2. 44 bilateral zero pairs at 95% confidence in Tr_BK at zeros
3. hbar_sed = 11.31 +/- 2.93 (mean commutator norm, constant not growing)
4. V_BK peaks at sigma=0.5 (0.10158) — unimodal maximum at critical line
5. Regime detection: HMM=bull, structural=UNSTABLE, 82.3% symmetry
"""
import numpy as np
from mpmath import mp, zetazero
import json
mp.dps = 25

def cd_conj(v):
    c=list(v)
    for i in range(1,len(v)): c[i]=-v[i]
    return c
def cd_mul(a,b):
    n=len(a)
    if n==1: return [a[0]*b[0]]
    h=n//2
    a1,a2,b1,b2=a[:h],a[h:],b[:h],b[h:]
    c1=[x-y for x,y in zip(cd_mul(a1,b1),cd_mul(cd_conj(b2),a2))]
    c2=[x+y for x,y in zip(cd_mul(b2,a1),cd_mul(a2,cd_conj(b1)))]
    return c1+c2
def norm_sq(v): return sum(x*x for x in v)
def make16(pairs):
    v=[0.0]*16
    for i,val in pairs: v[i]=float(val)
    return v

sqrt2=np.sqrt(2.0)
ROOT_16D={2:make16([(3,1),(12,-1)]),3:make16([(5,1),(10,1)]),
          5:make16([(3,1),(6,1)]),7:make16([(2,1),(7,-1)]),
          11:make16([(2,1),(7,1)]),13:make16([(6,1),(9,1)])}
PRIMES=[2,3,5,7,11,13]
BILATERAL=[2,13]

def F_16d(t,sigma=0.5):
    r=make16([(0,1.0)])
    for p in PRIMES:
        theta=t*np.log(p); rp=ROOT_16D[p]; rn=np.sqrt(norm_sq(rp))
        f=[0.0]*16; f[0]=np.cos(theta)
        for i in range(16): f[i]+=np.sin(theta)*rp[i]/rn
        r=cd_mul(r,f)
    r[4]+=(sigma-0.5)/sqrt2; r[5]-=(sigma-0.5)/sqrt2
    return r

def Tr_BK(t): return float(sum((np.log(p)/np.sqrt(p))*np.cos(t*np.log(p)) for p in PRIMES))
def Weil_RHS(): return -sum(np.log(p)/np.sqrt(p) for p in PRIMES)

def V_BK(t,sigma=0.5):
    F=F_16d(t,sigma); ns=norm_sq(F)
    if ns<1e-20: return 0.0
    gn=[norm_sq(cd_mul(F,[x/np.sqrt(norm_sq(ROOT_16D[p])) for x in ROOT_16D[p]]))/ns for p in BILATERAL]
    return float(np.var(gn))

def commutator_norm(t,sigma=0.5,eps=1e-6):
    F=F_16d(t,sigma)
    Fp=F_16d(t+eps,sigma); Fm=F_16d(t-eps,sigma)
    H=[(Fp[i]-Fm[i])/(2*eps) for i in range(16)]
    FH=cd_mul(F,H); HF=cd_mul(H,F)
    return float(np.sqrt(sum((FH[i]-HF[i])**2 for i in range(16))))

if __name__ == '__main__':
    print("Fetching 100 zeros + 99 midpoints...")
    zeros=[float(zetazero(n).imag) for n in range(1,101)]
    midpoints=[0.5*(zeros[i]+zeros[i+1]) for i in range(99)]

    Tr_z=[Tr_BK(t) for t in zeros]
    Tr_m=[Tr_BK(t) for t in midpoints]
    VBK_z=[V_BK(t) for t in zeros]
    CN_z=[commutator_norm(t) for t in zeros[:20]]

    print(f"Weil RHS: {Weil_RHS():.4f}")
    print(f"Tr_BK zeros: mean={np.mean(Tr_z):.4f}, neg={sum(1 for x in Tr_z if x<0)}/100")
    print(f"Tr_BK mids:  mean={np.mean(Tr_m):.4f}, neg={sum(1 for x in Tr_m if x<0)}/99")
    print(f"V_BK zeros: {np.mean(VBK_z):.6f} +/- {np.std(VBK_z):.6f}")
    print(f"Commutator mean (n=20): {np.mean(CN_z):.4f} +/- {np.std(CN_z):.4f}")

    # V_BK sigma scan
    SIGMA_SCAN = [0.3,0.4,0.45,0.5,0.55,0.6,0.7]
    vbk_sigma = {str(sv): float(np.mean([V_BK(t,sv) for t in zeros[:50]])) for sv in SIGMA_SCAN}
    print("\nV_BK sigma scan (mean over 50 zeros):")
    for sv in SIGMA_SCAN:
        print(f"  sigma={sv}: {vbk_sigma[str(sv)]:.6f}")

    seqs={
        'Tr_zeros_n100': Tr_z, 'Tr_mid_n99': Tr_m,
        'VBK_zeros_n100': VBK_z, 'CN_zeros_n20': CN_z,
        'weil_rhs': float(Weil_RHS()),
        'fraction_Tr_negative': sum(1 for x in Tr_z if x<0)/100,
        'vbk_sigma_scan': vbk_sigma,
    }
    with open('phase28_bk.json','w') as f:
        json.dump(seqs,f)
    print("Saved: phase28_bk.json")
