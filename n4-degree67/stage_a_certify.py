#!/usr/bin/env python3
"""Stage A -- regenerate the quintic Pisot certification over the box [-2,2]^5.

Target endpoint (prior session, GP+sympy): 83 Pisot / 16 mixed / 67 two-pair.
Discipline: exact arithmetic only. Fraction/int everywhere a verdict depends on it.

Certification of P = x^5 + c4 x^4 + ... + c0, ci in {-2..2}:
  P Pisot  <=>  irreducible over Q  AND  exactly 4 roots in |z|<1  AND  1 real root in (1, oo).

Interior count, path 1 (primary): Schur-Cohn recursion.
  Tp = a0*p - an*rev(p);  delta = a0^2 - an^2.
  delta > 0: nu(p) = nu(Tp);  delta < 0: nu(p) = deg(p) - nu(Tp);  delta = 0: DEGENERATE.
  [FORCED] If every delta != 0 down to degree 0, the recursion itself certifies p has no
  roots on |z|=1 (a circle zero would propagate to the terminal nonzero constant), and
  every Rouche comparison is strict, so the count is exact.

Interior count, path 2 (independent): Routh-Hurwitz on q(w) = (1-w)^5 * P((1+w)/(1-w)).
  |z|<1 <-> Re(w)<0; interior count = 5 - (sign changes in the Routh first column).
  Zero pivot / zero row => DEGENERATE (flagged, not fudged).

Real-root counts: sympy Sturm (Poly.count_roots) with rational endpoints; Cauchy bound
  1 + max|ci| <= 3, so all real roots lie in (-4, 4) and P(+-4) != 0, P(1) != 0.

Classification: two-pair <=> total real roots == 1; mixed <=> total in {3,5}.
"""
from fractions import Fraction as F
from itertools import product
import hashlib, json, sys, time

from sympy import Poly, Symbol, ZZ

x = Symbol("x")

# ---------------------------------------------------------------- Schur-Cohn
def schur_cohn_interior(coeffs):
    """coeffs = (a0,...,an) ints/Fractions, an != 0. Return (count, 'ok') or (None, 'degenerate')."""
    p = [F(c) for c in coeffs]
    n = len(p) - 1
    if n == 0:
        return (0, "ok") if p[0] != 0 else (None, "degenerate")
    a0, an = p[0], p[-1]
    delta = a0 * a0 - an * an
    if delta == 0:
        return (None, "degenerate")
    Tp = [a0 * p[i] - an * p[n - i] for i in range(n + 1)]  # degree-n term cancels
    while Tp and Tp[-1] == 0:
        Tp.pop()
    if not Tp:
        return (None, "degenerate")
    sub, st = schur_cohn_interior(Tp)
    if st != "ok":
        return (None, "degenerate")
    return (sub, "ok") if delta > 0 else (n - sub, "ok")

# ------------------------------------------------------------- Routh-Hurwitz
def mobius_q(coeffs):
    """q(w) = (1-w)^5 * P((1+w)/(1-w)), exact integer coefficients, ascending in w."""
    n = len(coeffs) - 1
    q = [0] * (n + 1)
    for k, ck in enumerate(coeffs):            # ck * (1+w)^k * (1-w)^(n-k)
        term = [1]
        for _ in range(k):
            term = [ (term[i-1] if i > 0 else 0) + (term[i] if i < len(term) else 0)
                     for i in range(len(term) + 1) ]
        for _ in range(n - k):
            term = [ (term[i] if i < len(term) else 0) - (term[i-1] if i > 0 else 0)
                     for i in range(len(term) + 1) ]
        for i, t in enumerate(term):
            q[i] += ck * t
    return q

def _routh_desc(desc):
    n = len(desc) - 1
    row0 = desc[0::2]
    row1 = desc[1::2]
    first_col = [row0[0]]
    while len(row1) > 0:
        if row1[0] == 0:
            return (None, "degenerate")
        first_col.append(row1[0])
        w = len(row0) - 1
        nxt = []
        for i in range(w):
            a = row0[i + 1] if i + 1 < len(row0) else F(0)
            b = row1[i + 1] if i + 1 < len(row1) else F(0)
            nxt.append((row1[0] * a - row0[0] * b) / row1[0])
        row0, row1 = row1, nxt                 # widths follow 3,3,2,2,1,1; zero pivot caught above
    if len(first_col) != n + 1:
        return (None, "degenerate")
    changes = sum(1 for a, b in zip(first_col, first_col[1:]) if (a > 0) != (b > 0))
    return (n - changes, "ok")

def routh_lhp(coeffs):
    """Interior-of-unit-disk count via Routh on q(w) = (1-w)^5 P((1+w)/(1-w)).
    Zero pivot => retry on the reversed q: Re(1/w) has the sign of Re(w), so the
    reversal w -> 1/w preserves the LHP count [FORCED]; q(0) = P(1) != 0 keeps degree."""
    q = mobius_q(coeffs)
    if q[-1] == 0 or q[0] == 0:
        return (None, "degenerate")
    desc = [F(c) for c in reversed(q)]         # descending: w^n ... w^0
    cnt, st = _routh_desc(desc)
    if st == "ok":
        return (cnt, "ok")
    cnt, st = _routh_desc(list(reversed(desc)))
    return (cnt, "ok:rev") if st == "ok" else (None, "degenerate")

# -------------------------------------------------------------------- sweep
def main():
    t0 = time.time()
    tal = dict(candidates=0, c0_nonzero=0, sc_pass=0, sturm_pass=0, irreducible_pisot=0,
               sc_degenerate=0, dual_path_checked=0, dual_path_mismatch=0)
    pisot = []
    for c in product(range(-2, 3), repeat=5):
        c0, c1, c2, c3, c4 = c
        tal["candidates"] += 1
        if c0 == 0:
            continue
        tal["c0_nonzero"] += 1
        coeffs = (c0, c1, c2, c3, c4, 1)                       # ascending
        sc, st = schur_cohn_interior(coeffs)
        if st != "ok":
            tal["sc_degenerate"] += 1
            sc = None                                          # fall through on Routh alone
            r_only, rst = routh_lhp(coeffs)
            if not rst.startswith("ok") or r_only != 4:
                continue
        elif sc != 4:
            continue
        tal["sc_pass"] += 1
        P = Poly([1, c4, c3, c2, c1, c0], x, domain=ZZ)        # descending for sympy
        if P.count_roots(1, 4) != 1:
            continue
        tal["sturm_pass"] += 1
        if not P.is_irreducible:
            continue
        tal["irreducible_pisot"] += 1
        # dual path: Routh must agree with Schur-Cohn on every certified instance
        rh, rst = routh_lhp(coeffs)
        tal["dual_path_checked"] += 1
        if not rst.startswith("ok") or rh != 4 or (sc is not None and rh != sc):
            tal["dual_path_mismatch"] += 1
            print(f"MISMATCH {coeffs} SC={sc} RH={rh}/{rst}", file=sys.stderr)
            continue
        # invariant: nothing hides in (-4,-1]
        assert P.count_roots(-4, -1) == 0, coeffs
        r_total = int(P.count_roots(-4, 4))
        assert r_total in (1, 3, 5), (coeffs, r_total)
        pisot.append(dict(c=list(c), real_roots=r_total,
                          pattern="two-pair" if r_total == 1 else "mixed"))
    tp = [p for p in pisot if p["pattern"] == "two-pair"]
    mx = [p for p in pisot if p["pattern"] == "mixed"]
    with open("/home/claude/n1/pisot83.jsonl", "w") as f:
        for p in pisot:
            f.write(json.dumps(p) + "\n")
    sha = hashlib.sha256(open("/home/claude/n1/pisot83.jsonl", "rb").read()).hexdigest()
    print(json.dumps(tal, indent=2))
    print(f"PISOT {len(pisot)}  two-pair {len(tp)}  mixed {len(mx)}")
    print(f"TARGET  83        two-pair 67          mixed 16   ->",
          "MATCH" if (len(pisot), len(tp), len(mx)) == (83, 67, 16) else "MISMATCH")
    print(f"pisot83.jsonl sha256 {sha[:16]}...  elapsed {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
