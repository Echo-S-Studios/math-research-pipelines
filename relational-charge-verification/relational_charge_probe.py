"""Relational (pairwise) charge probe -- exact arithmetic only.

Object of study: for monic p in Z[x], the RATIO polynomial
    Rat_p(x) = Res_y( p(y), p(x*y) ),   roots = { a_i / a_j } (all n^2 ratios).
A pair (a_i, a_j) of EQUAL MODULUS has rational relative angle  <=>  a_i/a_j is a
root of unity  <=>  some cyclotomic Phi_m divides Rat_p.  Completeness certificate:
Phi_m | Rat_p forces phi(m) <= deg(Rat_p) = n^2, and phi(m) >= sqrt(m/2) for all m,
so scanning m <= 2*(n^2)^2 is a COMPLETE decision (no float, no truncation).
Scope: the probe certifies coherence within equal-modulus shells; for a Salem number
the shells are {tau}, {1/tau}, {circle}, so the probe decides the circle block fully.
"""
import time
import sympy as sp

x, y = sp.symbols('x y')

def ratio_poly(p_expr):
    R = sp.resultant(p_expr.subs(x, y), sp.expand(p_expr.subs(x, x*y)), y)
    return sp.Poly(sp.expand(R), x).primitive()[1]

def totients_upto(N):
    phi = list(range(N + 1))
    for i in range(2, N + 1):
        if phi[i] == i:                      # i prime
            for j in range(i, N + 1, i):
                phi[j] -= phi[j] // i
    return phi

def cyclotomic_contacts(P):
    d = P.degree()
    N = 2 * d * d
    phi = totients_upto(N)
    hits = {}
    for m in range(1, N + 1):
        if phi[m] > d:
            continue
        cm = sp.Poly(sp.cyclotomic_poly(m, x), x)
        if sp.rem(P, cm).is_zero:            # Phi_m irreducible: divides or no contact
            mult, T = 0, P
            while True:
                q, r = sp.div(T, cm)
                if r.is_zero:
                    mult, T = mult + 1, q
                else:
                    break
            hits[m] = mult
    return hits

def probe(name, p_expr):
    t0 = time.time()
    P = ratio_poly(p_expr)
    hits = cyclotomic_contacts(P)
    print(f"{name:34s} degRat={P.degree():4d}  contacts={hits}  ({time.time()-t0:.1f}s)")
    return P, hits

print("== controls (charge-admissible) ==")
P3, h3 = probe("A  x^3-2          (Z/3, M=2)", x**3 - 2)
assert P3 == sp.Poly(sp.expand((x**3 - 1)**3), x) and h3 == {1: 3, 3: 3}
P4, h4 = probe("B  x^4-2          (Z/4, M=2)", x**4 - 2)
assert h4 == {1: 4, 2: 4, 4: 4}          # relational recovery of n=4, no reference ray
Pq, hq = probe("C  x^4+x^2-1      (q_2, M=phi)", x**4 + x**2 - 1)
assert hq == {1: 4, 2: 4}                # shell-scoped: 2 antipodal pairs x 2 orderings

print("== inadmissible sector (Salem) ==")
Pb, hb = probe("D  beta4 = x^4-x^3-x^2-x+1", x**4 - x**3 - x**2 - x + 1)
PL, hL = probe("E  Lehmer degree-10",
               x**10 + x**9 - x**7 - x**6 - x**5 - x**4 - x**3 + x + 1)
print("   verdict D:", "circle block INERT" if hb == {1: 4} else f"nontrivial: {hb}")
print("   verdict E:", "all 8 circle roots mutually INERT" if hL == {1: 10} else f"nontrivial: {hL}")

print("== two-route corroboration (beta4): Rat == charpoly(C (x) C^-1) ==")
def companion(coeffs):                       # [1, c_{n-1}, ..., c0] monic high->low
    n = len(coeffs) - 1
    C = sp.zeros(n)
    for i in range(1, n):
        C[i, i - 1] = 1
    for i in range(n):
        C[i, n - 1] = -coeffs[n - i]
    return C
Cb = companion([1, -1, -1, -1, 1])
assert Cb.det() == 1                         # unit => integer inverse
Kron = sp.Matrix(sp.kronecker_product(Cb, Cb.inv()))
cp = sp.Poly(Kron.charpoly(x).as_expr(), x).primitive()[1]
assert cp == Pb
print("   beta4: resultant route == Kronecker route  [two-route OK]")

print("== the golden internal relation, and the group drop ==")
phi_ = (1 + sp.sqrt(5)) / 2
phip = (1 - sp.sqrt(5)) / 2
assert sp.simplify(phi_ / phip + phi_**2) == 0          # ratio = -phi^2 : angle pi, Delta = 1/2
print("   phi/phi' = -phi^2  ->  relative charge 1/2 (order 2)  [forced]")
g = sp.Poly(x**4 + 5*x**2 + 5, x)
assert g.is_irreducible                                  # Eisenstein at 5
y1, y2 = (-5 + sp.sqrt(5))/2, (-5 - sp.sqrt(5))/2        # x^2-roots
assert y1.is_negative and y2.is_negative                 # all four roots purely imaginary
assert sp.simplify((-y1)*(-y2) - 5) == 0 and (-y1 - 1).is_positive and (-y2 - 1).is_positive
print("   x^4+5x^2+5: absolute group Z/4 (angles 1/4,3/4), differences generate Z/2, M = 5")
print("ALL ASSERTIONS PASSED")
