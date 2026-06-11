#!/usr/bin/env python3
"""
phase76_partB_symbolic.py — CAIL-RH Investigation, Phase 76 Part B
Chavez AI Labs LLC — Applied Pathological Mathematics

Exact symbolic verification (sympy, rational/symbolic arithmetic) of:
  B-1.2  Canonical Six product orthogonality on generic sedenion x
  B-1.3  Pairing criterion identity
  B-1.4  B/A asymptote sqrt(17) in the encoding family
plus bilateral annihilation P*Q = Q*P = 0 in exact integers.
"""
import sympy as sp


def cd_mult(a, b):
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    conj = lambda v: [v[0]] + [-x for x in v[1:]]
    p1 = [sp.expand(x - y) for x, y in zip(cd_mult(a1, b1), cd_mult(conj(b2), a2))]
    p2 = [sp.expand(x + y) for x, y in zip(cd_mult(b2, a1), cd_mult(a2, conj(b1)))]
    return p1 + p2


def vec(*pairs, n=16):
    v = [sp.Integer(0)] * n
    for i, val in pairs:
        v[i] = sp.Integer(val)
    return v


PATTERNS = {
    1: (vec((1, 1), (14, 1)),  vec((3, 1), (12, 1))),
    2: (vec((3, 1), (12, 1)),  vec((5, 1), (10, 1))),
    3: (vec((4, 1), (11, 1)),  vec((6, 1), (9, 1))),
    4: (vec((1, 1), (14, -1)), vec((3, 1), (12, -1))),
    5: (vec((1, 1), (14, -1)), vec((5, 1), (10, 1))),
    6: (vec((2, 1), (13, -1)), vec((6, 1), (9, 1))),
}

x = [sp.Symbol(f"x{i}", real=True) for i in range(16)]
dot = lambda a, b: sp.expand(sum(p * q for p, q in zip(a, b)))

print("=== B-1.2a Bilateral annihilation (exact integers) ===")
for g, (P, Q) in PATTERNS.items():
    PQ, QP = cd_mult(P, Q), cd_mult(Q, P)
    ok = all(c == 0 for c in PQ) and all(c == 0 for c in QP)
    print(f"  S{g}: P*Q = Q*P = 0 : {'PROVED' if ok else 'FAIL'}")

print("\n=== B-1.2b Product orthogonality on GENERIC x (16 free symbols) ===")
for g, (P, Q) in PATTERNS.items():
    r1 = sp.simplify(cd_mult(cd_mult(x, P), Q)[0])
    r2 = sp.simplify(cd_mult(cd_mult(P, x), Q)[0])
    r3 = sp.simplify(dot(cd_mult(x, P), Q))
    ok = r1 == 0 and r2 == 0 and r3 == 0
    print(f"  S{g}: e0((xP)Q)={r1}  e0((Px)Q)={r2}  <xP,Q>={r3}  : "
          f"{'PROVED identically zero' if ok else 'NONZERO'}")

print("\n=== B-1.3 Pairing criterion identity ===")
sigma = sp.Symbol("sigma", real=True)
U = {g: [p + q for p, q in zip(P, Q)] for g, (P, Q) in PATTERNS.items()}
c = {g: -2 * dot(x, U[g]) for g in PATTERNS}
magsq = {g: dot(x, x) + 4 * (c[g] ** 2 + 4 * (2 * sigma) ** 2) for g in PATTERNS}
all_ok = True
for g in PATTERNS:
    for h in PATTERNS:
        if g < h:
            lhs = sp.expand(magsq[g] - magsq[h])
            rhs = sp.expand(16 * dot(x, [a - b for a, b in zip(U[g], U[h])])
                            * dot(x, [a + b for a, b in zip(U[g], U[h])]))
            if sp.simplify(lhs - rhs) != 0:
                all_ok = False
                print(f"  S{g}/S{h}: FAIL")
print("  |M_g|^2 - |M_h|^2 = 16 <x,u_g-u_h><x,u_g+u_h> for all 15 pairs:",
      "PROVED identically" if all_ok else "FAIL")

print("\n=== B-1.4 B/A asymptote in the encoding family ===")
t = sp.Symbol("t", real=True, positive=True)
# encoding family: x1 = t, all other coordinates bounded (treat as symbols b_i)
b = [sp.Symbol(f"b{i}", real=True) for i in range(16)]
xe = list(b)
xe[1] = t
CLASS_B, CLASS_A = (1, 4, 5), (2, 3, 6)
for g in CLASS_B:
    m2 = sp.expand(sum(xi ** 2 for xi in xe) + 4 * ((-2 * dot(xe, U[g])) ** 2)
                   + 16 * (2 * sigma) ** 2)
    lead = sp.LT(sp.Poly(m2, t).as_expr(), gens=(t,))
    print(f"  S{g} (Class B): |M|^2 leading term in t = {lead}")
for g in CLASS_A:
    m2 = sp.expand(sum(xi ** 2 for xi in xe) + 4 * ((-2 * dot(xe, U[g])) ** 2)
                   + 16 * (2 * sigma) ** 2)
    deg = sp.Poly(m2, t).degree()
    lead = sp.LT(sp.Poly(m2, t).as_expr(), gens=(t,)) if deg > 0 else m2
    print(f"  S{g} (Class A): degree in t = {deg}, leading = {lead if deg>0 else 'O(1)'}")
print("  => |M_B|/t -> sqrt(17), |M_A|/t -> 1, B/A -> sqrt(17) =",
      sp.sqrt(17).evalf(12))
