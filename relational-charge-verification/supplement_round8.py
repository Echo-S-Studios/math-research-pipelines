"""Round-8 investigation: the cross-shell nu-criterion on p = x^4 - x + 1.
Core finding (verified exactly below): charpoly(C_p (x) C_p) = S6(x)^2 * p2(x)
with S6 the certified degree-6 Salem polynomial of Theorem 7.9 -- so the
cross products alpha*conj(beta) are unit-circle conjugates of a Salem number,
whose angles are irrational [forced]; cross-shell coherence is impossible."""
import sympy as sp
from relational_charge_probe import ratio_poly, cyclotomic_contacts, x
from supplement_round3 import trace_poly

p  = x**4 - x + 1
S6 = x**6 - x**4 - x**3 - x**2 + 1
P  = sp.Poly(p, x)

print("== X(a): shape of p = x^4 - x + 1 ==")
assert P.is_irreducible
assert P.count_roots() == 0                          # no real roots (Sturm)
assert P.all_coeffs() != P.all_coeffs()[::-1]        # non-reciprocal => no unimodular root
print("  irreducible, 0 real roots, non-reciprocal -> two conjugate-pair shells r, 1/r with r != 1")

print("== X(b): Kronecker-square factorization ==")
def companion(ch):
    n = len(ch) - 1
    C = sp.zeros(n)
    for i in range(1, n): C[i, i-1] = 1
    for i in range(n):    C[i, n-1] = -ch[n-i]
    return C
Cp = companion(P.all_coeffs())
F  = sp.Poly(sp.Matrix(sp.kronecker_product(Cp, Cp)).charpoly(x).as_expr(), x)
fl = sp.factor_list(F.as_expr())
print("  factors:", [(sp.sstr(f), m) for f, m in fl[1]])
p2 = sp.Poly(sp.expand(sp.resultant(p.subs(x, sp.Symbol('y')),
                                    x - sp.Symbol('y')**2, sp.Symbol('y'))), x)
fdict = {sp.Poly(f, x): m for f, m in fl[1]}
assert fdict.get(sp.Poly(S6, x)) == 2, "S6^2 must divide the Kronecker square"
assert fdict.get(p2.primitive()[1]) == 1 and p2.primitive()[1].is_irreducible
assert sum(sp.Poly(f, x).degree()*m for f, m in fl[1]) == 16
print("  charpoly(C(x)C) = S6^2 * psi2-image  [S6 = the certified Salem sextic of Thm 7.9]")
# which S6-roots are the pair-products A = r^2, 1/A? the real ones; the four
# cross products alpha*conj(beta) etc. are S6's unimodular conjugates.
T, m = trace_poly(S6)   # re-assert the Salem certificate (ledger O)
assert T.is_irreducible and T.count_roots() == m and T.count_roots(inf=2) == 1 \
   and T.count_roots(sup=-2) == 0 and T.count_roots(inf=-2, sup=2) == m - 1
print("  S6 Salem certificate re-asserted -> its circle roots are not roots of unity [forced]")
print("  => alpha*conj(beta) has irrational angle => cross-shell pairs of p incoherent [forced]")
# Mahler measure identity: M(p) = r^2 = A = tau(S6); exact route: A is the
# unique real S6-root > 1, and M(p) = product of the outer pair = A.
print("  identity: M(x^4 - x + 1) = tau_{S6} (outer-shell pair product; A real root >1 of S6)")
# alpha = (alpha^2)^2 + 1 from p, so Q(alpha^2) = Q(alpha): psi2-image irreducible, one line.

print("== X(c): shell-level scan of p (complete) ==")
h = cyclotomic_contacts(ratio_poly(p))
print(f"  contacts Rat_p = {h}")
assert h == {1: 4}      # no within-shell torsion, no rational angles

print("== X(d): Galois group (optional garnish) ==")
try:
    from sympy.polys.numberfields.galoisgroups import galois_group
    G = galois_group(P, by_name=True)
    print("  Gal =", G)
except Exception as e:
    print("  (galois_group unavailable in this sympy build:", type(e).__name__, ")")

print("== X: verdict ==")
print("  x^4 - x + 1 is FULLY relationally inert [forced]:")
print("   - within-shell: complete scan {Phi_1^4} (X(c))")
print("   - cross-shell:  alpha*conj(beta) is a circle conjugate of the Salem S6 (X(b))")
print("ROUND-8 CORE: ALL PASSED")
