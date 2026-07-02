#!/usr/bin/env python3
"""p_census.py -- box-parametrized Pisot census (P-series runs).

Same discipline as n4_lib.census (unconditional four-path chain, exact in-run
adjudication of degenerate chains, zero unadjudicated candidates), but over
the box [lo,hi]^n with the Cauchy bound generalized: all roots lie in
(-B, B) for B = 1 + max(|lo|,|hi|) < B+1, so the real gates use (1, B+1) and
(-B-1, -1). n4_lib itself is MANIFEST-pinned and is imported, not modified.
"""
import json
import sys
import time
from itertools import product

sys.path.insert(0, "/home/claude/n4")
from n4_lib import sa, four_paths, interior_sandwich  # noqa: E402
from sympy import Poly, Symbol, ZZ, gcd as sgcd  # noqa: E402

x = Symbol("x")


def census_box(n, lo, hi, out_path, log=print):
    t0 = time.time()
    B = 1 + max(abs(lo), abs(hi))
    tal = dict(candidates=0, c0_zero=0, chain_target=0, chain_reject=0,
               empty=0, empty_reciprocal=0, empty_reducible=0,
               empty_interior=0, empty_pisot=0,
               sturm_reject=0, reducible=0, pisot=0)
    rows = []
    target = n - 1
    for c in product(range(lo, hi + 1), repeat=n):
        tal["candidates"] += 1
        if c[0] == 0:
            tal["c0_zero"] += 1
            continue
        coeffs = c + (1,)
        vals = four_paths(coeffs)
        desc = [1] + [c[i] for i in range(n - 1, -1, -1)]
        if not vals:
            tal["empty"] += 1
            P = Poly(desc, x, domain=ZZ)
            rev = Poly(list(reversed(desc)), x, domain=ZZ)
            if P == rev or P == -rev:
                tal["empty_reciprocal"] += 1
                continue
            if not P.is_irreducible:
                tal["empty_reducible"] += 1
                continue
            assert Poly(sgcd(P, rev), x).degree() == 0, ("unimodular risk", c)
            inside = interior_sandwich(coeffs)
            if inside == target and int(P.count_roots(1, B + 1)) == 1:
                tal["empty_pisot"] += 1
                log(f"*** ADJUDICATED PISOT (degenerate chain): {c} ***")
                rows.append(_row(c, P, n, B, "adjudicated"))
            else:
                tal["empty_interior"] += 1
            continue
        assert len(set(vals.values())) == 1, ("cross-path disagreement", c, vals)
        if next(iter(vals.values())) != target:
            tal["chain_reject"] += 1
            continue
        tal["chain_target"] += 1
        P = Poly(desc, x, domain=ZZ)
        if int(P.count_roots(1, B + 1)) != 1:
            tal["sturm_reject"] += 1
            continue
        if not P.is_irreducible:
            tal["reducible"] += 1
            continue
        rows.append(_row(c, P, n, B, sorted(vals)))
        tal["pisot"] += 1
    tal["pisot"] += tal["empty_pisot"]
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    pat = {}
    for r in rows:
        pat[r["pattern"]] = pat.get(r["pattern"], 0) + 1
    log(f"deg {n} box [{lo},{hi}]: {json.dumps(tal)}")
    log(f"deg {n} box [{lo},{hi}]: {len(rows)} Pisot, patterns "
        f"{dict(sorted(pat.items()))}  {time.time()-t0:.1f}s")
    return rows, tal


def _row(c, P, n, B, certs):
    assert int(P.count_roots(-B - 1, -1)) == 0, c
    r_total = int(P.count_roots(-B - 1, B + 1))
    pairs = (n - r_total) // 2
    assert r_total >= 1 and (n - r_total) % 2 == 0, (c, r_total)
    return dict(c=list(c), real_roots=r_total, pairs=pairs,
                pattern=f"{r_total}r{pairs}p", certs=certs)
