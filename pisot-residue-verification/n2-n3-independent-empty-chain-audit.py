#!/usr/bin/env python3
"""Independent empty-chain audit for the N2 census over [-3,3]^5.

Replaces the absent n2_chain_audit.py. Claim under test:
  2602 candidates have an empty 4-path certificate chain; 8 of them are
  irreducible; 0 are Pisot; 0 unresolved.

Method (exact arithmetic only, no floats):
  * reproduce the 4-path chain partition of all 14406 candidates (c0 != 0);
  * for each empty-chain candidate, test irreducibility (sympy, exact);
  * for each irreducible one, prove no roots on |z| = 1 via
    gcd(P(x), x^5 P(1/x)) == const (an irreducible quintic sharing a root with
    its reciprocal would divide it, forcing |c0| = 1 and P = +-rev(P), i.e.
    P(1) = 0 or P(-1) = 0 -- reducible; the gcd makes this per-instance exact);
  * decide the interior-of-unit-disk count by a lambda-sandwich: Schur-Cohn on
    P(lambda x) with rational lambda straddling 1; non-degenerate equal counts
    at lambda < 1 and lambda > 1 pin #{|z| < 1} exactly (no unimodular roots);
  * Pisot <=> irreducible AND interior count 4 AND Sturm#(1, 5) == 1.
"""
import sys, time, types
from fractions import Fraction as F
from itertools import product

src = open("/home/claude/n1/stage_a_certify.py").read().replace(
    'if __name__ == "__main__":\n    main()', '')
sa = types.ModuleType("sa"); exec(src, sa.__dict__)

from sympy import Poly, Symbol, ZZ, gcd as sgcd
x = Symbol("x")

def cert_chain(coeffs, neg):
    out = []
    sc, st = sa.schur_cohn_interior(coeffs)
    if st == "ok": out.append(("SC", sc))
    rh, rst = sa.routh_lhp(coeffs)
    if rst.startswith("ok"): out.append(("RH", rh))
    if len(out) < 2 or len({v for _, v in out}) > 1:
        rh2, rst2 = sa.routh_lhp(neg)
        if rst2.startswith("ok"): out.append(("RHneg", rh2))
    if len(out) < 2:
        sc2, st2 = sa.schur_cohn_interior(neg)
        if st2 == "ok": out.append(("SCneg", sc2))
    return out

def interior_sandwich(coeffs):
    """Exact #{roots with |z| < 1} for P with no unimodular roots."""
    for k in (6, 10, 14, 20, 30, 44):
        lo, hi = F(2**k - 1, 2**k), F(2**k + 1, 2**k)
        counts = []
        for lam in (lo, hi):
            scaled = [c * lam**i for i, c in enumerate(coeffs)]
            cnt, st = sa.schur_cohn_interior(scaled)
            if st != "ok":
                counts = None; break
            counts.append(cnt)
        if counts and counts[0] == counts[1]:
            return counts[0], (lo, hi)
    return None, None

def main():
    t0 = time.time()
    accepted = empty = rejected_cert = 0
    empty_list = []
    for c in product(range(-3, 4), repeat=5):
        c0, c1, c2, c3, c4 = c
        if c0 == 0: continue
        coeffs = (c0, c1, c2, c3, c4, 1); neg = (-c0, c1, -c2, c3, -c4, 1)
        certs = cert_chain(coeffs, neg)
        vals = {v for _, v in certs}
        if not certs:
            empty += 1; empty_list.append(c); continue
        if vals != {4}:
            assert 4 not in vals, ("exact-path disagreement", c, certs)
            rejected_cert += 1; continue
        accepted += 1  # vals == {4}: candidate proceeds to Sturm/irreducibility gates
    print(f"partition: chain-4 candidates={accepted}  cert!=4 rejects={rejected_cert}  "
          f"empty-chain={empty}  (claim: empty=2602)")
    assert empty == 2602, empty

    irred = []
    for c in empty_list:
        c0, c1, c2, c3, c4 = c
        P = Poly([1, c4, c3, c2, c1, c0], x, domain=ZZ)
        if P.is_irreducible:
            irred.append((c, P))
    print(f"irreducible among empty-chain: {len(irred)}  (claim: 8)")
    assert len(irred) == 8, len(irred)

    pisot = 0; unresolved = 0
    for c, P in irred:
        c0, c1, c2, c3, c4 = c
        coeffs = (c0, c1, c2, c3, c4, 1)
        revP = Poly(list(reversed(P.all_coeffs())), x, domain=ZZ)
        g = sgcd(P, revP)
        assert Poly(g, x).degree() == 0, ("unimodular-root risk", c)
        cnt, window = interior_sandwich(coeffs)
        if cnt is None:
            unresolved += 1
            print(f"  UNRESOLVED {c}"); continue
        n_big = int(P.count_roots(1, 5))
        is_pisot = (cnt == 4 and n_big == 1)
        pisot += is_pisot
        print(f"  c={c} interior={cnt} (window {window[0]}..{window[1]}) "
              f"real>1: {n_big} -> {'PISOT (!!)' if is_pisot else 'not Pisot'}")
    print(f"AUDIT VERDICT: empty-chain=2602  irreducible=8  Pisot={pisot}  "
          f"unresolved={unresolved}  (claim: 0 Pisot, 0 unresolved)  "
          f"{time.time()-t0:.1f}s")
    assert pisot == 0 and unresolved == 0

if __name__ == "__main__":
    main()
