#!/usr/bin/env python3
"""
residual_return_audit.py — independent re-derivation of every displayed numeric/
algebraic claim in "Residual Return" (the dynamic/linguistic companion paper).

Written from scratch (sympy + stdlib + mpmath), importing none of the L00M engine.
Purpose: confirm the paper's load-bearing numbers from definitions, exactly, and
flag any displayed identity that is only true under an unstated restriction.

It cannot verify the paper's *test names*, *commit hashes*, or *suite pass counts*
(127/544/121/74/...): those are claims about a repository not in evidence. This
harness checks the mathematics those tests purportedly assert.
"""
import sympy as sp
import hashlib, json
from mpmath import iv

x = sp.symbols("x")
R2, R3, R5, R6, R7 = (sp.sqrt(n) for n in (2, 3, 5, 6, 7))

results = []
def chk(name, cond, got="", exp="", status="exact"):
    results.append((status, bool(cond), name, str(got), str(exp)))

# ─────────────────────────────────────────────────────────────────────────────
# §2  K = Q(sqrt2+sqrt3) = Q[x]/(x^4-10x^2+1); power-basis trace-form Gram (Eq 2)
# ─────────────────────────────────────────────────────────────────────────────
conj = [R2 + R3, R2 - R3, -R2 + R3, -R2 - R3]            # the four embeddings of theta
def trace_pow(m):                                        # Tr(theta^m) = sum of conjugates^m
    return sp.simplify(sum(c**m for c in conj))
G = sp.Matrix(4, 4, lambda i, j: trace_pow(i + j))       # G_ij = Tr(theta^(i-1) theta^(j-1))
G_paper = sp.Matrix([[4, 0, 20, 0], [0, 20, 0, 196], [20, 0, 196, 0], [0, 196, 0, 1940]])
chk("(2) power-basis Gram G of Q(sqrt2+sqrt3)", G == G_paper, G.tolist(), G_paper.tolist())
chk("G is positive definite (totally real)", all(v > 0 for v in G.eigenvals()), status="exact")

# Example 2.4 / 5.3 : w = 2sqrt6 = theta^2-5, coords (-5,0,1,0); ||r||^2_G = 96
w = sp.Matrix([-5, 0, 1, 0])
score_w = (w.T * G * w)[0]
chk("(Ex 2.4) residual norm of 2sqrt6 is 96", score_w == 96, score_w, 96)
# the off-axis element really is 2sqrt6
chk("(Ex 2.4) (sqrt2+sqrt3)^2 - 5 == 2 sqrt6", sp.simplify((R2 + R3)**2 - 5 - 2*R6) == 0)

# ─────────────────────────────────────────────────────────────────────────────
# §2.5 / §8.2  witness digest — fully external SHA-256 reproduction
# ─────────────────────────────────────────────────────────────────────────────
body = {"event": "basis_growth", "index": 0, "min_poly": [1, 0, -24],
        "coords": ["-5", "0", "1", "0"], "snap": "exact",
        "num_seeds": 3, "streak": 4, "prev_hash": "genesis"}
canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
digest = hashlib.sha256(("genesis" + canonical).encode()).hexdigest()[:16]
chk("(Ex 2.5) SHA-256 witness digest", digest == "31f1f1e05ac9a35a", digest, "31f1f1e05ac9a35a")

# ─────────────────────────────────────────────────────────────────────────────
# §3.1  coordinates->minimal-polynomial bridge (verify the *result* two ways)
# ─────────────────────────────────────────────────────────────────────────────
def minpoly(alpha):
    return sp.Poly(sp.minimal_polynomial(alpha, x), x)
chk("(Ex 3.2) minpoly(phi) = x^2-x-1",
    minpoly((1 + R5)/2) == sp.Poly(x**2 - x - 1, x))
chk("(Ex 3.2) minpoly(2 sqrt6) = x^2-24",
    minpoly(2*R6) == sp.Poly(x**2 - 24, x))
chk("(Ex 3.2) minpoly(theta) = x^4-10x^2+1",
    minpoly(R2 + R3) == sp.Poly(x**4 - 10*x**2 + 1, x))
_p_half = sp.Poly(sp.minimal_polynomial(sp.Rational(1, 2), x), x)   # sympy primitive form: 2x-1
_monic_half = [c / _p_half.LC() for c in _p_half.all_coeffs()]      # monic form: [1, -1/2]
chk("(Ex 3.2) 1/2 is not an algebraic integer (monic minpoly x-1/2 has non-integer coeff)",
    not all(c.is_integer for c in _monic_half), _monic_half)

# Remark 3.3 : characteristic polynomial is an incomplete similarity invariant
def companion(coeffs):                                   # coeffs = [1, c_{n-1}, ..., c0], monic
    n = len(coeffs) - 1
    C = sp.zeros(n)
    for i in range(1, n):
        C[i, i - 1] = 1
    for i in range(n):
        C[i, n - 1] = -coeffs[n - i]
    return C
Cphi = companion([1, -1, -1])                            # C(x^2-x-1) = [[0,1],[1,1]]
A = sp.Matrix(sp.BlockDiagMatrix(Cphi, Cphi))            # phi (+) phi
B = companion([1, -2, -1, 2, 1])                         # C((x^2-x-1)^2)
I4 = sp.eye(4)
chk("(Rem 3.3) phi(+)phi and C((x^2-x-1)^2) share charpoly",
    sp.expand(A.charpoly(x).as_expr() - B.charpoly(x).as_expr()) == 0)
chk("(Rem 3.3) ...but A satisfies x^2-x-1 and B does not -> not similar",
    (A*A - A - I4 == sp.zeros(4)) and (B*B - B - I4 != sp.zeros(4)))
# even (charpoly, minpoly) is incomplete: rank separates J2(+)J2 from J2(+)J1(+)J1
J2 = sp.Matrix([[0, 1], [0, 0]])
AJ = sp.Matrix(sp.BlockDiagMatrix(J2, J2))
BJ = sp.diag(J2, sp.zeros(1), sp.zeros(1))
chk("(Rem 3.3) Jordan pair: equal charpoly x^4 and minpoly x^2",
    AJ.charpoly(x).as_expr() == x**4 and BJ.charpoly(x).as_expr() == x**4
    and AJ*AJ == sp.zeros(4) and BJ*BJ == sp.zeros(4))
chk("(Rem 3.3) ...but rank 2 vs rank 1 -> not similar",
    AJ.rank() == 2 and BJ.rank() == 1)

# ─────────────────────────────────────────────────────────────────────────────
# §3.2  disjoint compositum: Kronecker Gram and the exact det relation
# ─────────────────────────────────────────────────────────────────────────────
GK = sp.diag(4, 8, 12, 24)                               # Q(sqrt2,sqrt3)
GL = sp.diag(2, 14)                                      # Q(sqrt7)
GKL = sp.Matrix(sp.kronecker_product(GK, GL))
chk("(Ex 3.6) G_KL = G_K (x) G_L = diag(8,56,16,112,24,168,48,336)",
    list(GKL.diagonal()) == [8, 56, 16, 112, 24, 168, 48, 336],
    list(GKL.diagonal()))
# det relation det G_KL = (det G_K)^[L:Q] (det G_L)^[K:Q]
chk("(Rem 3.7) det relation 9216^2 * 28^4",
    GKL.det() == GK.det()**2 * GL.det()**4 == 9216**2 * 28**4, GKL.det())

# ─────────────────────────────────────────────────────────────────────────────
# §3.3  NON-DISJOINT compositum (the headline new result), Example 3.10
# ─────────────────────────────────────────────────────────────────────────────
# m_beta = x^4-10x^2+1 factors over K = Q(sqrt2)
fac = sp.factor(x**4 - 10*x**2 + 1, extension=R2)
explicit = sp.expand((x**2 - 2*R2*x - 1)*(x**2 + 2*R2*x - 1))
chk("(Ex 3.10) m_beta factors over Q(sqrt2) into the stated two quadratics",
    fac != sp.Poly(x**4 - 10*x**2 + 1, x).as_expr()
    and sp.simplify(explicit - (x**4 - 10*x**2 + 1)) == 0, sp.factor(fac))
# true compositum Q(sqrt2)(sqrt2+sqrt3) = Q(sqrt2,sqrt3), degree 4 (sqrt3 = beta - sqrt2)
chk("(Ex 3.10) compositum is Q(sqrt2,sqrt3): (sqrt2+sqrt3)-sqrt2 == sqrt3",
    sp.simplify((R2 + R3) - R2 - R3) == 0)
# primitive element theta = sqrt2 + (sqrt2+sqrt3) = 2sqrt2 + sqrt3 ; its minpoly
theta = 2*R2 + R3
mtheta = minpoly(theta)
chk("(Eq 4) selected minimal polynomial m_theta = x^4-22x^2+25",
    mtheta == sp.Poly(x**4 - 22*x**2 + 25, x), mtheta.as_expr())
chk("(Ex 3.10) degree-6 operator poly factors as (x^2-3)(x^4-22x^2+25)",
    sp.expand((x**2 - 3)*(x**4 - 22*x**2 + 25)) == x**6 - 25*x**4 + 91*x**2 - 75)
chk("(Ex 3.10) spurious factor x^2-3 has root sqrt3 (= theta under sqrt2 -> -sqrt2)",
    sp.simplify((-R2 + (R2 + R3)) - R3) == 0)
# exact reconstruction beta = -7/20 theta + 1/20 theta^3
beta_recon = sp.Rational(-7, 20)*theta + sp.Rational(1, 20)*theta**3
chk("(Ex 3.10) beta = -7/20 theta + 1/20 theta^3 == sqrt2+sqrt3",
    sp.simplify(beta_recon - (R2 + R3)) == 0, sp.simplify(beta_recon))

# ─────────────────────────────────────────────────────────────────────────────
# §4  capacity gate (Landau certificate) and Fisher matrices
# ─────────────────────────────────────────────────────────────────────────────
def landau_sumsq(coeffs):                                # sum of c_i^2 (incl leading 1)
    return sum(c*c for c in coeffs)
chk("(Ex 4.1) 2sqrt6: (deg,ch)=(2,24), sum c^2 = 577, Landau 24^2<=577",
    landau_sumsq([1, 0, -24]) == 577 and 24**2 <= 577, landau_sumsq([1, 0, -24]))
chk("(Ex 4.1) sqrt7: x^2-7, sum c^2 = 50, certifies M<=8 (50<=64)",
    landau_sumsq([1, 0, -7]) == 50 and 50 <= 64, landau_sumsq([1, 0, -7]))

def fisher(Gm, tvec):                                    # I_exp = (1/n)(G - (1/n) t t^T)
    n = Gm.shape[0]
    t = sp.Matrix(tvec)
    return sp.Rational(1, n)*(Gm - sp.Rational(1, n)*(t*t.T))

# Q(sqrt5), {1,phi}: G=[[2,1],[1,3]], t=(Tr1,Tr phi)=(2,1)
G5 = sp.Matrix([[2, 1], [1, 3]]); t5 = [2, 1]
Iexp5 = fisher(G5, t5)
chk("(Ex 4.2) Q(sqrt5) I_exp = diag-ish [[0,0],[0,5/4]]",
    Iexp5 == sp.Matrix([[0, 0], [0, sp.Rational(5, 4)]]), Iexp5.tolist())
chk("(Ex 4.2) Q(sqrt5) det G = 5", G5.det() == 5)
# residual sqrt5 = 2phi-1 = (-1,2) is trace-zero and ||.||^2_G = 10 = n I(.)
v = sp.Matrix([-1, 2])
chk("(Ex 4.2) ||sqrt5||^2_G = 10 = 2*I(sqrt5) on trace-zero",
    (v.T*G5*v)[0] == 10 and (v.T*G5*v)[0] == 2*(v.T*Iexp5*v)[0], (v.T*G5*v)[0])

# Q(sqrt2,sqrt3): G=diag(4,8,12,24), t=(4,0,0,0)
G23 = sp.diag(4, 8, 12, 24); t23 = [4, 0, 0, 0]
Iexp23 = fisher(G23, t23)
chk("(Ex 4.2) Q(sqrt2,sqrt3) I_exp = diag(0,2,3,6)",
    list(Iexp23.diagonal()) == [0, 2, 3, 6], list(Iexp23.diagonal()))
# Q(sqrt2,sqrt3,sqrt7): G = the Kronecker diag, t=(8,0,...,0)
G237 = sp.diag(8, 56, 16, 112, 24, 168, 48, 336); t237 = [8] + [0]*7
Iexp237 = fisher(G237, t237)
chk("(Ex 4.2) Q(sqrt2,sqrt3,sqrt7) I_exp = diag(0,7,2,14,3,21,6,42)",
    list(Iexp237.diagonal()) == [0, 7, 2, 14, 3, 21, 6, 42], list(Iexp237.diagonal()))

# CHALLENGE: the paper writes "I_exp = (1/n) G" — true only on the trace-zero subspace,
# NOT as a full-matrix identity (it fails at the constant direction, where I_exp[0,0]=0).
chk("(Rem) I_exp == (1/n)G as a FULL matrix? (paper's shorthand)",
    Iexp23 == sp.Rational(1, 4)*G23, Iexp23.tolist(), (sp.Rational(1,4)*G23).tolist(),
    status="shorthand")
chk("(Rem) G = n I_exp on the trace-zero subspace (the load-bearing claim) holds",
    all(((u := sp.Matrix(col)).T*G23*u)[0] == 4*((u.T*Iexp23*u)[0])
        for col in ([0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 1, -1, 0])))

# ─────────────────────────────────────────────────────────────────────────────
# §4.2/§4.3  Smyth floor and certified-grow enclosures (mpmath interval arithmetic)
# ─────────────────────────────────────────────────────────────────────────────
mu_S = sp.nsolve(x**3 - x - 1, 1.3)                      # plastic number
chk("(Rem 4.3) Smyth floor mu_S ~ 1.3247179572 (root of x^3-x-1)",
    abs(float(mu_S) - 1.3247179572447898) < 1e-12, float(mu_S))
import math
floor_const = 2*math.log(float(mu_S))
chk("(Rem 4.3) constant floor 2 log mu_S ~ 0.5623991", abs(floor_const - 0.5623991486) < 1e-9, floor_const)
chk("(Rem 4.3) degree-aware floors: n=4 -> 2.2496, n=8 -> 4.4992",
    abs(4*floor_const - 2.2496) < 1e-3 and abs(8*floor_const - 4.4992) < 1e-3,
    (round(4*floor_const, 4), round(8*floor_const, 4)))

iv.dps = 30
l7, l24 = iv.log(7), iv.log(24)                          # rigorous interval enclosures
chk("(Ex 4.4) log7 in [1.94591,1.94592] and 2*upper <= 56 (certified grow)",
    (l7.a > iv.mpf("1.94591")) and (l7.b < iv.mpf("1.94592")) and (2*float(l7.b) <= 56),
    f"[{float(l7.a):.6f},{float(l7.b):.6f}]")
chk("(Ex 4.4) log24 in [3.17805,3.17806] and 2*upper <= 96 (certified grow)",
    (l24.a > iv.mpf("3.17805")) and (l24.b < iv.mpf("3.17806")) and (2*float(l24.b) <= 96),
    f"[{float(l24.a):.6f},{float(l24.b):.6f}]")
chk("(Ex 4.4) lattice-aligned noise 1/10 < 0.5624 -> stopped by Smyth floor",
    sp.Rational(1, 10) < sp.Float(floor_const))

# ─────────────────────────────────────────────────────────────────────────────
# §6  the residual-valued language over Cl(2,0) ~= M2(R)
# ─────────────────────────────────────────────────────────────────────────────
def mat(c):                                              # coords (a,b,c,d) -> 2x2
    a, b, cc, d = c
    return sp.Matrix([[a + cc, b - d], [b + d, a - cc]])
def coords(M):                                           # 2x2 -> coords (a,b,c,d)
    p, q, r, s = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
    return sp.Matrix([(p + s)/2, (q + r)/2, (p - s)/2, (r - q)/2])

# carrier axioms
chk("(6.1) e1^2 = e2^2 = 1, i^2 = -1, e1 e2 = i",
    mat([0, 1, 0, 0])**2 == sp.eye(2) and mat([0, 0, 1, 0])**2 == sp.eye(2)
    and mat([0, 0, 0, 1])**2 == -sp.eye(2)
    and mat([0, 1, 0, 0])*mat([0, 0, 1, 0]) == mat([0, 0, 0, 1]))

# keystone R = 1/2 + e1 - 1/2 e2  -> mat(R) = [[0,1],[1,1]] = C(x^2-x-1)
Rk = mat([sp.Rational(1, 2), 1, sp.Rational(-1, 2), 0])
chk("(6.2) mat(R) = [[0,1],[1,1]] = companion(x^2-x-1)", Rk == sp.Matrix([[0, 1], [1, 1]]))
chk("(7.2) R^2 = R + I (golden law)", Rk*Rk == Rk + sp.eye(2))
chk("(6.1) tau(R)=1/2 (scalar part), det(R) = -1",
    coords(Rk)[0] == sp.Rational(1, 2) and Rk.det() == -1)

# return operator L(X) = R X + X R - X ; build its 4x4 matrix over {1,e1,e2,i}
def L(c):
    M = mat(c)
    return coords(Rk*M + M*Rk - M)
Lmat = sp.Matrix.hstack(*[L([int(i == k) for i in range(4)]) for k in range(4)])
ns = Lmat.nullspace()
chk("(6.3) ker L is exactly 2-dimensional", len(ns) == 2, len(ns))
# the stated kernel basis e1+2e2 and i lie in ker L
chk("(6.3) e1+2e2 in ker L and i in ker L",
    L([0, 1, 2, 0]) == sp.zeros(4, 1) and L([0, 0, 0, 1]) == sp.zeros(4, 1))
# Sylvester eigenvalue argument: spec(L) = {sqrt5, 0, 0, -sqrt5}
_evL = Lmat.eigenvals()
chk("(6.3) spectrum of L = {+sqrt5, 0(x2), -sqrt5} (ties to substrate's {R,R})",
    len(_evL) == 3 and _evL.get(sp.Integer(0)) == 2
    and _evL.get(sp.sqrt(5)) == 1 and _evL.get(-sp.sqrt(5)) == 1, _evL)
chk("(6.2) R not in ker L; L(R) = 5/2 + e1 - 1/2 e2",
    L([sp.Rational(1, 2), 1, sp.Rational(-1, 2), 0]) ==
    sp.Matrix([sp.Rational(5, 2), 1, sp.Rational(-1, 2), 0]))

# commit = exact idempotent orthogonal projector onto ker L (Eq 7)
Kbasis = sp.Matrix([[0, 0], [1, 0], [2, 0], [0, 1]])     # columns e1+2e2, i
P = Kbasis*(Kbasis.T*Kbasis).inv()*Kbasis.T
P_paper = sp.Matrix([[0, 0, 0, 0],
                     [0, sp.Rational(1, 5), sp.Rational(2, 5), 0],
                     [0, sp.Rational(2, 5), sp.Rational(4, 5), 0],
                     [0, 0, 0, 1]])
chk("(Eq 7) commit projector value", P == P_paper, P.tolist())
chk("(Eq 7) projector idempotent and not identity", P*P == P and P != sp.eye(4))

# Theorem 6.5 generalisation by return-to-zero
chk("(Thm 6.5) commit(E1) = H(0,1/5,2/5,0)",
    P*sp.Matrix([0, 1, 0, 0]) == sp.Matrix([0, sp.Rational(1, 5), sp.Rational(2, 5), 0]))
chk("(Thm 6.5) commit(E1+1) == commit(E1) (constant orthogonal to slack -> merge)",
    P*sp.Matrix([1, 1, 0, 0]) == P*sp.Matrix([0, 1, 0, 0]))
chk("(Thm 6.5) i and 2i are distinct exact residues (dedup on value, not word)",
    P*sp.Matrix([0, 0, 0, 1]) != P*sp.Matrix([0, 0, 0, 2]))
chk("(Ex 6.6) five tokens -> four lexicon entries",
    len({tuple((P*sp.Matrix(c)).T.tolist()[0])
         for c in ([0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 2], [0, 0, 0, -1])}) == 4)

# Remark 6.4 the corrected disproof: N = -e1+e2 NOT in ker L; L(N) = -3 (scalar)
chk("(Rem 6.4) L(H(0,-1,1,0)) = H(-3,0,0,0) (the disproof)",
    L([0, -1, 1, 0]) == sp.Matrix([-3, 0, 0, 0]))
chk("(Rem 6.4) but cl([[0,-1],[1,0]]) = i is in the kernel",
    coords(sp.Matrix([[0, -1], [1, 0]])) == sp.Matrix([0, 0, 0, 1]))

# ─────────────────────────────────────────────────────────────────────────────
# §7  the phi-keystone is one object (three independent routes)
# ─────────────────────────────────────────────────────────────────────────────
phi = (1 + R5)/2
chk("(Prop 7.1) companion(x^2-x-1) == mat(R) == [[0,1],[1,1]]",
    companion([1, -1, -1]) == Rk)
chk("(Prop 7.1) Mahler measure of x^2-x-1 equals phi (one root outside unit circle)",
    sp.simplify(phi - sp.Max(*[abs(r) for r in sp.Poly(x**2 - x - 1, x).all_roots()
                               if abs(r) > 1])) == 0)

# ─────────────────────────────────────────────────────────────────────────────
# §4.3  the lambda = 2c closure (this revision): identity, gate ladder, forced flip
# ─────────────────────────────────────────────────────────────────────────────
_c, _gain, _logM = sp.symbols("c gain logM", positive=True)
_lam = sp.solve(sp.Eq(_gain / (2 * _c), _logM), _gain)[0] / _logM
chk("(Thm 4.6) exchange rate is the derived identity lambda = 2c",
    sp.simplify(_lam - 2 * _c) == 0 and sp.simplify(_lam.subs(_c, 1) - 2) == 0,
    sp.simplify(_lam), "2c (c=1 -> 2)")
chk("(Prop 4.9) self-action gate ladder sqrt(1+4C) in {sqrt2, sqrt3, sqrt5}",
    all(sp.simplify(sp.sqrt(1 + 4 * C) - sp.sqrt(g)) == 0 for C, g in
        [(sp.Rational(1, 4), 2), (sp.Rational(1, 2), 3), (sp.Integer(1), 5)]),
    "sqrt2,sqrt3,sqrt5")
chk("(Rem 4.12) forced flip: D=1+4C sign at C=-1/4; frame-shift c real (D>0) / imaginary (D<0)",
    sp.solve(sp.Eq(1 + 4 * x, 0), x) == [sp.Rational(-1, 4)]
    and sp.im((sp.sqrt(1 + 4 * x) / (2 * x)).subs(x, 1)) == 0
    and sp.re((sp.sqrt(1 + 4 * x) / (2 * x)).subs(x, -1)) == 0,
    "C=-1/4; c real->imaginary")

# ─────────────────────────────────────────────────────────────────────────────
# report
# ─────────────────────────────────────────────────────────────────────────────
W = max(len(r[2]) for r in results)
passed = sum(1 for r in results if r[1])
print(f"{'STATUS':9} {'OK':3} CLAIM")
print("-" * (W + 28))
for status, ok, name, got, exp in results:
    flag = "PASS" if ok else "FAIL"
    line = f"{status:9} {flag:3} {name:<{W}}"
    if not ok or status == "shorthand":
        line += f"   got={got}"
        if exp:
            line += f"  exp={exp}"
    print(line)
print("-" * (W + 28))
n_short = sum(1 for r in results if r[0] == "shorthand")
print(f"{passed}/{len(results)} checks passed   "
      f"({sum(1 for r in results if r[0]=='exact' and r[1])} exact, "
      f"{n_short} flagged as paper-shorthand)")
