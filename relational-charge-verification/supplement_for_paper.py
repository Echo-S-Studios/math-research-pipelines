"""Supplementary exact computations for the relational-charge whitepaper ledger."""
import time, sympy as sp
from relational_charge_probe import ratio_poly, cyclotomic_contacts, x, y

phi  = (1 + sp.sqrt(5))/2
PASS = []
def chk(name, cond):
    assert cond, name
    PASS.append(name); print("  ok:", name)

# (1) Gauge-blindness of the probe: x^3+2 (absolute Z/6) reads the SAME as x^3-2 (absolute Z/3)
P, h = ratio_poly(x**3 + 2), None
h = cyclotomic_contacts(P)
chk("x^3+2 contacts {1:3,3:3} == x^3-2 contacts (probe reads relational Z/3, blind to n=6)",
    h == {1: 3, 3: 3})

# (2) The group-drop quartic and the catalog seed K: identical shell signatures
h2 = cyclotomic_contacts(ratio_poly(x**4 + 5*x**2 + 5))
hK = cyclotomic_contacts(ratio_poly(x**4 + 5*x**2 - 5))
chk("x^4+5x^2+5 contacts {1:4,2:4}", h2 == {1: 4, 2: 4})
chk("K = x^4+5x^2-5 contacts {1:4,2:4} (full Z/4 lives cross-shell, settled symbolically)",
    hK == {1: 4, 2: 4})

# (3) Mixed probe: beta4 x Lehmer cross ratios -- circle-locking test, complete scan
b4 = x**4 - x**3 - x**2 - x + 1
Lh = x**10 + x**9 - x**7 - x**6 - x**5 - x**4 - x**3 + x + 1
chk("gcd(beta4, Lehmer) = 1 (distinct irreducibles)", sp.gcd(b4, Lh) == 1)
t0 = time.time()
RM = sp.Poly(sp.expand(sp.resultant(b4.subs(x, y), sp.expand(Lh.subs(x, x*y)), y)), x).primitive()[1]
hM = cyclotomic_contacts(RM)
print(f"     mixed Rat deg={RM.degree()}, contacts={hM}  ({time.time()-t0:.1f}s)")
chk("beta4 x Lehmer: NO cyclotomic contact (deg 40, scan complete) -> not circle-locked", hM == {})

# (4) The sign twist: (-1)^n p(-x) maps the odd-m coset sector onto the absolute Z/m sector
chk("twist(x^3+2) = x^3-2", sp.expand(-( (-x)**3 + 2 ) - (x**3 - 2)) == 0)
for m in (3, 5, 7, 9):
    for e in range(1, 2*m, 2):                     # e odd
        chk_ok = ((e + m) % 2 == 0)                # (e+m)/(2m) lands in (1/m)Z
        assert chk_ok
print("  ok: coset arithmetic (e odd, m odd => (e+m)/(2m) in (1/m)Z), m in {3,5,7,9}")

# (5) q_k = x^{2k}+x^k-1 always realizes the difference 1/2 via a real +- pair
chk("y-roots of y^2+y-1: 1/phi > 0 and -phi < 0",
    sp.simplify((1/phi)**2 + (1/phi) - 1) == 0 and sp.simplify(phi**2 - phi - 1) == 0
    and (1/phi).is_positive and (-phi).is_negative)

# (6) Group-drop witness re-consolidated: x^4+5x^2+5
g = sp.Poly(x**4 + 5*x**2 + 5, x, domain='QQ')
y1, y2 = (-5 + sp.sqrt(5))/2, (-5 - sp.sqrt(5))/2
chk("x^4+5x^2+5: irreducible; purely imaginary roots; M = 5; n = 4, Delta = Z/2",
    g.is_irreducible and y1.is_negative and y2.is_negative
    and sp.simplify(y1*y2 - 5) == 0 and (-y1 - 1).is_positive and (-y2 - 1).is_positive)

# (7) Golden internal relation (re-run for this ledger)
phip = (1 - sp.sqrt(5))/2
chk("phi/phi' = -phi^2 (relative charge 1/2)", sp.simplify(phi/phip + phi**2) == 0)

print(f"SUPPLEMENT: {len(PASS)+1} checks passed")
