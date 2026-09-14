#!/usr/bin/env python3
"""
Independent, from-scratch verification of the Clifford Cl(4,0) bilaterality
claim relayed from a Claude Desktop chat: that only the Canonical Six pattern
59 (S2: P2=e3+e12, Q2=e5+e10) is a truly BILATERAL zero divisor under Cl(4,0)
(both P*Q=0 and Q*P=0), while the other five are one-sided there (P*Q=0 only),
because P2 and Q2 are the only pair built entirely from grade-2 blades under
the "identity" index-to-blade map (sedenion basis index i <-> Clifford blade
with bitmask i over 4 generators e1..e4, all squaring to +1).

Does not trust the chat summary -- implements Cl(4,0) geometric product from
scratch, tests it against known small cases, then computes all twelve
products (P_i*Q_i and Q_i*P_i) directly.
"""
import itertools

N = 4  # Cl(4,0): 4 generators, all squaring to +1
METRIC = [1, 1, 1, 1]


def geo_mult_blades(a, b):
    """Geometric product of two basis blades (bitmasks over N generators).
    Returns (result_bitmask, sign)."""
    sign = 1
    result = a
    for i in range(N):
        if (b >> i) & 1:
            higher = bin(result >> (i + 1)).count("1")
            if higher % 2 == 1:
                sign = -sign
            if (result >> i) & 1:
                sign *= METRIC[i]
                result &= ~(1 << i)
            else:
                result |= (1 << i)
    return result, sign


def mv_mult(mv_a, mv_b):
    """Multivector product. mv_a, mv_b: dict {blade_bitmask: coeff}."""
    out = {}
    for ba, ca in mv_a.items():
        if ca == 0:
            continue
        for bb, cb in mv_b.items():
            if cb == 0:
                continue
            r, s = geo_mult_blades(ba, bb)
            out[r] = out.get(r, 0) + s * ca * cb
    return {k: v for k, v in out.items() if v != 0}


def grade(bitmask):
    return bin(bitmask).count("1")


# ---- sanity checks against known Cl(4,0) / geometric algebra facts --------
def blade_str(b):
    if b == 0:
        return "1"
    return "e" + "".join(str(i + 1) for i in range(N) if (b >> i) & 1)


tests = [
    ((1, 2), {3: 1}),    # e1*e2 = +e12
    ((2, 1), {3: -1}),   # e2*e1 = -e12
    ((1, 1), {0: 1}),    # e1*e1 = +1  (Cl(4,0): square = +1)
    ((3, 3), {0: -1}),   # e12*e12 = e1e2e1e2 = -e1e1e2e2 = -1
]
print("=== sanity checks ===")
all_ok = True
for (a, b), expected in tests:
    r, s = geo_mult_blades(a, b)
    got = {r: s}
    ok = got == expected
    all_ok &= ok
    print(f"  {blade_str(a)} * {blade_str(b)} = {s:+d}*{blade_str(r)}  "
          f"(expected {expected})  {'OK' if ok else 'MISMATCH'}")
assert all_ok, "sanity checks failed -- do not trust results below"

# ---- the six Canonical Six patterns, exactly as in the Lean file and the --
# ---- published paper's Table 1 (indices literal, 0-indexed as in the repo)
PATTERNS = {
    18:  ("P1", [1, 14], "Q1", [3, 12]),
    59:  ("P2", [3, 12], "Q2", [5, 10]),
    84:  ("P3", [4, 11], "Q3", [6, 9]),
    102: ("P4", [1, -14], "Q4", [3, -12]),   # negative index encodes a minus sign
    104: ("P5", [1, -14], "Q5", [5, 10]),
    124: ("P6", [2, -13], "Q6", [6, 9]),
}


def vec_from_signed_indices(signed_indices):
    mv = {}
    for si in signed_indices:
        idx = abs(si)
        sign = -1 if si < 0 else 1
        mv[idx] = mv.get(idx, 0) + sign
    return mv


def homogeneous(mv):
    grades = {grade(b) for b in mv}
    return len(grades) == 1, grades


print("\n=== index -> blade grade (identity bitmask map) ===")
for i in range(16):
    print(f"  index {i:2d} -> {blade_str(i):>6s}  grade {grade(i)}")

print("\n=== per-pattern bilaterality in Cl(4,0) ===")
results = {}
for pid, (pname, pidx, qname, qidx) in PATTERNS.items():
    P = vec_from_signed_indices(pidx)
    Q = vec_from_signed_indices(qidx)
    PQ = mv_mult(P, Q)
    QP = mv_mult(Q, P)
    p_homog, p_grades = homogeneous(P)
    q_homog, q_grades = homogeneous(Q)
    bilateral = (len(PQ) == 0) and (len(QP) == 0)
    results[pid] = {
        "PQ_zero": len(PQ) == 0, "QP_zero": len(QP) == 0, "bilateral": bilateral,
        "P_homog": p_homog, "P_grades": p_grades, "Q_homog": q_homog, "Q_grades": q_grades,
    }
    print(f"  pattern {pid:3d} ({pname}={pidx}, {qname}={qidx}): "
          f"P*Q=0: {len(PQ)==0}  Q*P=0: {len(QP)==0}  BILATERAL: {bilateral}   "
          f"P grades={p_grades}({'homog' if p_homog else 'mixed'})  "
          f"Q grades={q_grades}({'homog' if q_homog else 'mixed'})")
    if len(QP) > 0:
        print(f"      Q*P (nonzero) = {QP}")

print("\n=== verdict ===")
bilateral_patterns = [pid for pid, r in results.items() if r["bilateral"]]
print(f"  Bilateral (P*Q=0 AND Q*P=0) in Cl(4,0): {bilateral_patterns}")
print(f"  One-sided (P*Q=0 only) in Cl(4,0): "
      f"{[pid for pid, r in results.items() if r['PQ_zero'] and not r['bilateral']]}")
