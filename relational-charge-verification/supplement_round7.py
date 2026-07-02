"""Round-7: (W) plastic-number inertness, exact; census rejection tally;
nu-criterion symbolic execution on the group-drop quartic. All exact."""
import itertools, sympy as sp
from relational_charge_probe import ratio_poly, cyclotomic_contacts, x

print("== W(i): plastic number x^3 - x - 1 ==")
p = x**3 - x - 1
P = sp.Poly(p, x)
assert P.is_irreducible and P.count_roots() == 1 and P.count_roots(inf=1) == 1
h = cyclotomic_contacts(ratio_poly(p))
print(f"  contacts = {h}  -> {'INERT' if h == {1:3} else 'NONTRIVIAL'}")
assert h == {1: 3}

print("== W(ii): census rejection tally (exact certificates, 378 classes) ==")
z = sp.symbols('z')
def trace_fast(low, m):
    Pk = [sp.Integer(2), z]
    for k in range(2, m + 1): Pk.append(sp.expand(z*Pk[k-1] - Pk[k-2]))
    return sp.Poly(low[m] + sum(low[m+k]*Pk[k] for k in range(1, m+1)), z)
tally = {"pm1": 0, "sturm": 0, "reducible": 0, "Tred": 0, "salem": 0}
seen = set()
for c in itertools.product((-1,0,1), repeat=6):
    tw = tuple((-1)**i*v for i,v in enumerate(c, start=1))
    if min(c, tw) in seen: continue
    seen.add(min(c, tw))
    low = [1,c[0],c[1],c[2],c[3],c[4],c[5],c[4],c[3],c[2],c[1],c[0],1][::-1]
    if sum(low) == 0 or sum(v*(-1)**i for i,v in enumerate(low)) == 0:
        tally["pm1"] += 1; continue
    T = trace_fast(low, 6)
    if not (T.count_roots()==6 and T.count_roots(inf=2)==1
            and T.count_roots(sup=-2)==0 and T.count_roots(inf=-2,sup=2)==5):
        tally["sturm"] += 1; continue
    if not sp.Poly(sum(co*x**i for i,co in enumerate(low)), x).is_irreducible:
        tally["reducible"] += 1; continue
    if not T.is_irreducible: tally["Tred"] += 1; continue
    tally["salem"] += 1
assert tally == {"pm1": 39, "sturm": 257, "reducible": 45, "Tred": 0, "salem": 37}
assert sum(tally.values()) == len(seen) == 378
print(f"  {tally}  sum={sum(tally.values())}")

print("== W(iii): nu-criterion, symbolic, on x^4+5x^2+5 cross-shell pair ==")
a = sp.sqrt((5 + sp.sqrt(5))/2); b = sp.sqrt((5 - sp.sqrt(5))/2)
mu = a/b
assert sp.im(mu) == 0 and mu.is_positive           # cross-shell ratio real > 0
assert sp.simplify(mu/sp.conjugate(mu) - 1) == 0   # nu = 1: torsion of order 1
print("  mu = a/b real positive; nu = mu/conj(mu) = 1 -> coherent, t_rel = 0")
print("ROUND-7: ALL PASSED")
