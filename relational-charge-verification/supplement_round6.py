"""Round-6: (W1-W2) the q(x^k) non-inert irreducible witness x^4+x^2+2;
(W3) five larger-coefficient degree-12 Salem spot-checks (F5). All exact."""
import itertools, time, sympy as sp
from relational_charge_probe import ratio_poly, cyclotomic_contacts, x
from supplement_round3 import trace_poly   # full version (with identity assert)

z = sp.symbols('z')

def trace_fast(coeffs_low_high, m):
    """Trace polynomial via the Chebyshev-like recursion; no identity check."""
    Pk = [sp.Integer(2), z]
    for k in range(2, m + 1):
        Pk.append(sp.expand(z*Pk[k-1] - Pk[k-2]))
    T = coeffs_low_high[m] + sum(coeffs_low_high[m + k]*Pk[k] for k in range(1, m + 1))
    return sp.Poly(sp.expand(T), z)

print("== W1/W2: witness p = x^4 + x^2 + 2 = q(x^2), q = x^2 + x + 2 ==")
q, p = x**2 + x + 2, x**4 + x**2 + 2
assert sp.Poly(q, x).is_irreducible and sp.Poly(p, x).is_irreducible
hq = cyclotomic_contacts(ratio_poly(q)); hp = cyclotomic_contacts(ratio_poly(p))
print(f"  Rat_q contacts = {hq}  (== {{1:2}}: q's angle irrational, complete)")
print(f"  Rat_p contacts = {hp}  (Phi_2 contact: irreducible, inadmissible, NON-INERT)")
assert hq == {1: 2} and hp == {1: 4, 2: 4}
print("  M(p) = |p(0)| = 2 (all moduli 2^{1/4} > 1 since |rho|^2 = q(0) = 2)")

print("== W3: five deg-12 Salem spot checks with a coefficient outside {-1,0,1} ==")
found, seen = [], set()
t0 = time.time()
for c in itertools.product((-2, -1, 0, 1, 2), repeat=6):
    if all(abs(v) <= 1 for v in c): continue
    tw = tuple((-1)**i * v for i, v in enumerate(c, start=1))
    key = min(c, tw)
    if key in seen: continue
    seen.add(key)
    low = [1, c[0], c[1], c[2], c[3], c[4], c[5], c[4], c[3], c[2], c[1], c[0], 1][::-1]
    if sum(low) == 0 or sum(v*(-1)**i for i, v in enumerate(low)) == 0: continue  # p(1), p(-1)
    T = trace_fast(low, 6)
    if not (T.count_roots() == 6 and T.count_roots(inf=2) == 1
            and T.count_roots(sup=-2) == 0 and T.count_roots(inf=-2, sup=2) == 5):
        continue
    pp = sum(co * x**i for i, co in enumerate(low))
    if not (sp.Poly(pp, x).is_irreducible and T.is_irreducible): continue
    Tchk, m = trace_poly(pp)                 # full identity re-assert for finalists
    assert Tchk == T and m == 6
    found.append((c, sp.expand(pp)))
    if len(found) == 5: break
print(f"  search: {time.time()-t0:.0f}s, {len(seen)} twist-classes examined")
for c, pp in found:
    t1 = time.time()
    h = cyclotomic_contacts(ratio_poly(pp))
    print(f"  {c}: contacts={h}  {'INERT' if h == {1:12} else '*** NON-TRIVIAL ***'}  ({time.time()-t1:.0f}s)")
    assert h == {1: 12}
print("W3: 5/5 inert -- corroborating the pinning theorem outside the census family")

with open('cross_round6.gp', 'w') as f:
    f.write(open('cross_check.gp').read().split('S6 =')[0])
    f.write('print("U1 ", contacts(rat(x^2+x+2)));\n')
    f.write('print("U2 ", contacts(rat(x^4+x^2+2)));\n')
    for i, (c, pp) in enumerate(found, 1):
        f.write(f'print("V{i} ", contacts(rat({sp.sstr(pp)})));\n')
print("gp snippet written")
