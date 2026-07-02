"""Round-3 computations: exact Salem certification (trace-poly Sturm counts),
inertness scans for degree-6/8 instances, pairwise circle-locking batch,
quadratic-(EG) identities. All exact; no floats anywhere."""
import time, sympy as sp
from relational_charge_probe import ratio_poly, cyclotomic_contacts, x, y

phi = (1 + sp.sqrt(5))/2

def trace_poly(p_expr):
    """For reciprocal p of degree 2m, the T with p(x) = x^m T(x+1/x). Exact."""
    P = sp.Poly(p_expr, x)
    c = P.all_coeffs()[::-1]                      # low -> high
    deg = P.degree(); assert deg % 2 == 0
    m = deg // 2
    assert c == c[::-1], "not reciprocal"
    z = sp.symbols('z')
    Pk = [sp.Integer(2), z]                        # P_0=2, P_1=z
    for k in range(2, m + 1):
        Pk.append(sp.expand(z*Pk[k-1] - Pk[k-2]))
    T = c[m] + sum(c[m + k]*Pk[k] for k in range(1, m + 1))
    assert sp.simplify(sp.expand(x**m * T.subs(z, x + 1/x)) - p_expr) == 0
    return sp.Poly(sp.expand(T), z), m

def salem_cert(name, p_expr):
    P = sp.Poly(p_expr, x)
    assert P.is_irreducible and P(1) != 0 and P(-1) != 0
    T, m = trace_poly(p_expr)
    assert T.is_irreducible
    total, above2 = T.count_roots(), T.count_roots(inf=2)
    below, inside = T.count_roots(sup=-2), T.count_roots(inf=-2, sup=2)
    ok = (total == m and above2 == 1 and below == 0 and inside == m - 1)
    print(f"  {name:28s} deg={2*m}  Sturm: total={total} (>2)={above2} "
          f"(<-2)={below} in(-2,2)={inside}  SALEM={'YES' if ok else 'NO'}")
    return ok

b4 = x**4 - x**3 - x**2 - x + 1
L  = x**10 + x**9 - x**7 - x**6 - x**5 - x**4 - x**3 + x + 1
S6 = x**6 - x**4 - x**3 - x**2 + 1
S8 = x**8 - x**5 - x**4 - x**3 + 1

print("== O: exact Salem certification ==")
for nm, p in [("beta4", b4), ("S6", S6), ("S8", S8), ("Lehmer L", L)]:
    assert salem_cert(nm, p)

def mixed_rat(p, q):
    R = sp.resultant(q.subs(x, y), sp.expand(p.subs(x, x*y)), y)
    return sp.Poly(sp.expand(R), x).primitive()[1]

print("== P: internal coherence, S6 and S8 ==")
for nm, p, expect in [("S6", S6, {1: 6}), ("S8", S8, {1: 8})]:
    t0 = time.time(); R = ratio_poly(p); h = cyclotomic_contacts(R)
    print(f"  {nm}: degRat={R.degree()} bound={2*R.degree()**2} contacts={h} ({time.time()-t0:.1f}s)")
    assert h == expect

print("== Q: pairwise circle-locking batch ==")
for nm, p, q in [("b4xS6", S6, b4), ("b4xS8", S8, b4), ("S6xS8", S8, S6),
                 ("LxS6", L, S6), ("LxS8", L, S8)]:
    assert sp.gcd(p, q) == 1
    R = mixed_rat(p, q); h = cyclotomic_contacts(R)
    print(f"  {nm}: deg={R.degree()} bound={2*R.degree()**2} contacts={h}")
    assert h == {}

print("== R: quadratic-(EG) identities ==")
assert sp.simplify((1 + sp.sqrt(5))/2 - phi) == 0
assert sp.simplify((3 + sp.sqrt(5))/2 - phi**2) == 0
print("ROUND-3: ALL PASSED")

print("== S: worked non-inert example, beta4 (x) beta4 ==")
def companion(coeffs_high_to_low):
    n = len(coeffs_high_to_low) - 1
    C = sp.zeros(n)
    for i in range(1, n):
        C[i, i-1] = 1
    for i in range(n):
        C[i, n-1] = -coeffs_high_to_low[n-i]
    return C
Cb = companion([1, -1, -1, -1, 1])
K  = sp.Matrix(sp.kronecker_product(Cb, Cb))          # 16x16 integer
F  = sp.Poly(K.charpoly(x).as_expr(), x)
mult, T = 0, F                                        # (x-1)-multiplicity
while True:
    qq, rr = sp.div(T, sp.Poly(x - 1, x))
    if rr.is_zero: mult, T = mult + 1, qq
    else: break
G   = sp.gcd(F, sp.Poly(F.diff(x), x))                # squarefree defect
Fsq = sp.Poly(sp.quo(F, G), x)                        # distinct-eigenvalue poly
assert mult == 4                                      # {tau/tau, 1/tau*tau (x2), lam*conj (x2)} -> 1^4
assert G.degree() == 7                                # 3 from (x-1)^4 + 4 doubles
assert Fsq.degree() == 9                              # 9 distinct eigenvalues
assert Fsq.count_roots() == 3                         # distinct reals: 1, tau^2, tau^-2
assert Fsq.count_roots(inf=0) == 3                    # all positive
print(f"  charpoly(C(x)C): (x-1)-mult={mult}, deg gcd(F,F')={G.degree()}, "
      f"distinct={Fsq.degree()}, distinct-real={Fsq.count_roots()} (all>0)")
print("  -> rational block {1^4, tau^2, tau^-2}; two size-4 classes at +-theta; "
      "singletons at +-2theta: NOT inert")
