"""Exhaustive degree-12 census: all monic reciprocal p = x^12 + c1 x^11 + ... with
c1..c6 in {-1,0,1} (c_{12-i} = c_i). Certify Salem exactly (trace-poly Sturm);
dedupe under the sign twist p(x) -> p(-x) (which fixes Rat_p: ratios are
invariant under a global sign); scan every certified Salem for cyclotomic
contact. All exact; no floats."""
import time, itertools, sympy as sp
from relational_charge_probe import ratio_poly, cyclotomic_contacts, x
from supplement_round3 import trace_poly   # exact reciprocal->trace reduction

def poly_from(c):                # c = (c1..c6)
    # coeffs high->low: 1, c1..c5, c6, c5..c1, 1
    full = [1, c[0], c[1], c[2], c[3], c[4], c[5], c[4], c[3], c[2], c[1], c[0], 1]
    return sum(co * x**(12 - i) for i, co in enumerate(full))

def twist_key(c):                # coefficients of p(-x) in the same parametrization
    # p(-x): coefficient of x^{12-i} picks (-1)^{12-i} = (-1)^i sign on c_i
    tc = tuple((-1)**i * ci for i, ci in enumerate(c, start=1))
    return min(c, tc)

def is_salem(p):
    P = sp.Poly(p, x)
    if P(1) == 0 or P(-1) == 0 or not P.is_irreducible:
        return False
    T, m = trace_poly(p)
    if not T.is_irreducible:
        return False
    return (T.count_roots() == m and T.count_roots(inf=2) == 1
            and T.count_roots(sup=-2) == 0
            and T.count_roots(inf=-2, sup=2) == m - 1)

t0 = time.time()
seen, salems = set(), []
for c in itertools.product((-1, 0, 1), repeat=6):
    k = twist_key(c)
    if k in seen:
        continue
    seen.add(k)
    p = sp.expand(poly_from(c))
    if is_salem(p):
        salems.append((c, p))
print(f"family: 3^6 = 729 polynomials; {len(seen)} twist-classes; "
      f"certified Salem twist-classes: {len(salems)}  ({time.time()-t0:.0f}s)")
for c, p in salems:
    print("  Salem:", c, "  p =", sp.sstr(p))

print("-- contact scans (Rat degree 144, complete bound 41472 each) --")
all_inert = True
for c, p in salems:
    t1 = time.time()
    R = ratio_poly(p)
    h = cyclotomic_contacts(R)
    inert = (h == {1: 12})
    all_inert &= inert
    print(f"  {c}: contacts={h}  {'INERT' if inert else '*** NON-TRIVIAL ***'}  ({time.time()-t1:.0f}s)")
print("CENSUS VERDICT:", "every certified Salem in the family is relationally inert"
      if all_inert else "NON-INERT INSTANCE FOUND")
print(f"total {time.time()-t0:.0f}s")
