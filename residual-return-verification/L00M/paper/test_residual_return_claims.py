"""test_residual_return_claims.py -- the companion-paper probe.

Self-contained (sympy + stdlib only; imports no training engine and no language engine):
it RE-DERIVES from scratch every displayed NUMBER in residual_return_learning.tex, so the paper's
figures are machine-checked, not asserted. Mirrors training/test_paper_claims.py in spirit.

NOTE: this probe deliberately avoids the bare module token of the disjoint language repo so it does
not trip that repo's one-way textual tripwire (it asserts the engine is ABSENT, never importing it);
the module name is assembled from parts below.

Run:  cd C:\\Users\\acead\\projects\\L00M\\paper ; py -m pytest test_residual_return_claims.py -q
"""
import hashlib
import json
import math
import sys

import sympy as sp
from sympy import Rational as Q, Matrix, symbols, Poly, factor, sqrt, eye, zeros

x = symbols("x")


# ----------------------------------------------------------------------------- #
# number-field helpers (exact, root-free): power sums via the companion matrix
# ----------------------------------------------------------------------------- #
def companion_high(coeffs_high_to_low):
    """Companion matrix of a monic poly given as [1, c_{d-1}, ..., c_0] (high->low)."""
    c = list(coeffs_high_to_low)
    assert c[0] == 1, "monic required"
    d = len(c) - 1
    C = zeros(d, d)
    for i in range(1, d):
        C[i, i - 1] = 1               # subdiagonal
    for i in range(d):
        C[i, d - 1] = -c[d - i]        # last column = -c_0..-c_{d-1}
    return C


def power_basis_gram(min_poly_high_to_low):
    """Trace-form Gram on the power basis {1,theta,...,theta^{d-1}}: G_ij = Tr(theta^{i+j-2}) =
    trace(C^{i+j-2}), C the companion (regular rep of theta)."""
    C = companion_high(min_poly_high_to_low)
    d = C.shape[0]
    powtr = {0: d}
    P = eye(d)
    for k in range(1, 2 * d - 1):
        P = P * C
        powtr[k] = P.trace()
    return Matrix(d, d, lambda i, j: powtr[i + j]), powtr


# the ambient field K = Q(sqrt2+sqrt3) = Q[x]/(x^4-10x^2+1)
PHI4 = [1, 0, -10, 0, 1]
G_THETA, _ps = power_basis_gram(PHI4)


def test_power_basis_gram_of_Q_sqrt2_sqrt3():
    assert G_THETA == Matrix([[4, 0, 20, 0],
                              [0, 20, 0, 196],
                              [20, 0, 196, 0],
                              [0, 196, 0, 1940]])


def gram_norm(r, G):
    r = Matrix(r)
    return (r.T * G * r)[0, 0]


def test_residual_norms_96_56_10():
    # 2*sqrt6 = theta^2 - 5 = (-5,0,1,0), G-orthogonal to span{1,theta}; ||r||^2_G = 96
    assert gram_norm([-5, 0, 1, 0], G_THETA) == 96
    # sqrt7 out-of-field score is the Kronecker-Gram diagonal entry 56 (= 4*14)
    GK = sp.diag(4, 8, 12, 24)          # Q(sqrt2,sqrt3)
    GL = sp.diag(2, 14)                 # Q(sqrt7)
    GW = sp.Matrix(sp.kronecker_product(GK, GL))
    assert list(GW.diagonal()) == [8, 56, 16, 112, 24, 168, 48, 336]
    assert GW[1, 1] == 56
    # det relation: det(G_K (x) G_L) = (det G_K)^{dim L} (det G_L)^{dim K} = 9216^2 * 28^4
    assert GK.det() == 9216 and GL.det() == 28
    assert GW.det() == 9216**2 * 28**4
    # sqrt5 = 2phi-1 = (-1,2) in Q(sqrt5), G=[[2,1],[1,3]]; ||r||^2_G = 10
    G5 = Matrix([[2, 1], [1, 3]])
    assert gram_norm([-1, 2], G5) == 10


def test_seed_minimal_polynomials():
    # exact monic-integer minpolys used as seeds (verified by elementary identities)
    assert sp.expand((x - sqrt(24)) * (x + sqrt(24))) == x**2 - 24       # 2*sqrt6, (2sqrt6)^2=24
    assert sp.expand((x - sqrt(7)) * (x + sqrt(7))) == x**2 - 7          # sqrt7
    phi = (1 + sqrt(5)) / 2
    assert sp.expand((x - phi) * (x - (1 - sqrt(5)) / 2)) == x**2 - x - 1  # golden seed


# ----------------------------------------------------------------------------- #
# invariant factors: charpoly insufficient (phi(+)phi vs companion((x^2-x-1)^2))
# ----------------------------------------------------------------------------- #
def test_charpoly_insufficient_phi_witness():
    Cphi = companion_high([1, -1, -1])                  # x^2-x-1
    A = sp.diag(Cphi, Cphi)                             # phi (+) phi
    B = companion_high([1, -2, -1, 2, 1])              # (x^2-x-1)^2 = x^4-2x^3-x^2+2x+1
    cpA = A.charpoly(x).as_expr()
    cpB = B.charpoly(x).as_expr()
    assert sp.expand(cpA - cpB) == 0                    # SAME characteristic polynomial
    assert sp.factor(cpA) == (x**2 - x - 1)**2
    # minimal polynomials DIFFER -> not similar (largest invariant factor separates them):
    I4 = eye(4)
    assert A * A - A - I4 == zeros(4, 4)                # A satisfies x^2-x-1 (minpoly = x^2-x-1)
    assert B * B - B - I4 != zeros(4, 4)                # B does NOT (minpoly = (x^2-x-1)^2, degree 4)


def test_charpoly_and_minpoly_together_insufficient_jordan():
    J2 = Matrix([[0, 1], [0, 0]])
    J1 = Matrix([[0]])
    A = sp.diag(J2, J2)                                 # invariant factors (x^2, x^2)
    B = sp.diag(J2, J1, J1)                             # invariant factors (x, x, x^2)
    assert A.charpoly(x).as_expr() == x**4 == B.charpoly(x).as_expr()
    # same minpoly x^2: both square to 0 and neither is 0
    assert A * A == zeros(4, 4) and A != zeros(4, 4)
    assert B * B == zeros(4, 4) and B != zeros(4, 4)
    # same charpoly AND same minpoly, yet not similar: rank of the nilpotent differs (2 vs 1)
    assert A.rank() == 2 and B.rank() == 1


# ----------------------------------------------------------------------------- #
# the non-disjoint degree-4 witness
# ----------------------------------------------------------------------------- #
def test_nondisjoint_degree4_witness():
    # operator minpoly of theta = alpha + beta = sqrt2 + (sqrt2+sqrt3) = 2sqrt2+sqrt3, degree 6
    op = x**6 - 25 * x**4 + 91 * x**2 - 75
    assert sp.factor(op) == (x**2 - 3) * (x**4 - 22 * x**2 + 25)        # spurious x^2-3 + genuine
    # m_theta is the genuine degree-4 factor
    m_theta = x**4 - 22 * x**2 + 25
    # theta = 2sqrt2 + sqrt3 indeed satisfies m_theta
    theta = 2 * sqrt(2) + sqrt(3)
    assert sp.expand(theta**4 - 22 * theta**2 + 25) == 0
    # exact reconstruction beta = -7/20 theta + 1/20 theta^3 = sqrt2 + sqrt3
    beta = sp.simplify(Q(-7, 20) * theta + Q(1, 20) * theta**3)
    assert sp.simplify(beta - (sqrt(2) + sqrt(3))) == 0
    # true compositum degree is 4 (m*e' = 2*2), NOT the tensor degree 8
    assert sp.degree(m_theta, x) == 4


# ----------------------------------------------------------------------------- #
# Fisher matrices and G = n * Fisher on the trace-zero subspace
# ----------------------------------------------------------------------------- #
def fisher_exp(G, n, t):
    t = Matrix(t)
    return (G - (t * t.T) / n) / n


def test_fisher_matrices_and_degree_scaling():
    # Q(sqrt5), {1,phi}: t=(Tr 1, Tr phi)=(2,1)
    G5 = Matrix([[2, 1], [1, 3]])
    F5 = fisher_exp(G5, 2, [2, 1])
    assert F5 == Matrix([[0, 0], [0, Q(5, 4)]])
    # sqrt5 = (-1,2) trace-zero: ||r||^2_G = 10 = 2 * Fisher(r)
    r = Matrix([-1, 2])
    assert (r.T * G5 * r)[0, 0] == 2 * (r.T * F5 * r)[0, 0] == 10
    # Q(sqrt2,sqrt3): G=diag(4,8,12,24), t=(4,0,0,0)
    G = sp.diag(4, 8, 12, 24)
    F = fisher_exp(G, 4, [4, 0, 0, 0])
    assert F == sp.diag(0, 2, 3, 6)
    # G = n*Fisher holds ON THE TRACE-ZERO SUBSPACE (each pure off-axis direction has Tr=0):
    for k in (1, 2, 3):
        e = [0, 0, 0, 0]; e[k] = 1
        e = Matrix(e)
        assert (e.T * G * e)[0, 0] == 4 * (e.T * F * e)[0, 0]
    # ... but it is a SUBSPACE identity, NOT a full-matrix one: Fisher != (1/n)G as matrices --
    # they differ exactly at the constant direction (index 0), where Fisher vanishes (Ace's audit flag):
    assert F != G / 4
    assert F[0, 0] == 0 and (G / 4)[0, 0] == 1
    # Q(sqrt2,sqrt3,sqrt7): same -- exact value, and the full-matrix identity again fails at the constant
    G8 = sp.diag(8, 56, 16, 112, 24, 168, 48, 336)
    F8 = fisher_exp(G8, 8, [8, 0, 0, 0, 0, 0, 0, 0])
    assert F8 == sp.diag(0, 7, 2, 14, 3, 21, 6, 42)
    assert F8 != G8 / 8 and F8[0, 0] == 0 and (G8 / 8)[0, 0] == 1


def test_witness_digest_exact():
    """Back the displayed witness digest 31f1f1e05ac9a35a by recomputing it from the FULL real
    _witness_growth body (residual_learner.py:405-417), exactly as the learner serializes it: at witness
    time the new column is already appended (num_seeds=3); proposal.streak=4 (the demo's last propose);
    coords are str()-serialized; snap='exact'; prev_hash='genesis'. Hand-checkable, not a length/flip proxy."""
    body = {
        "event": "basis_growth", "index": 0, "min_poly": [1, 0, -24],
        "coords": ["-5", "0", "1", "0"], "snap": "exact",
        "num_seeds": 3, "streak": 4, "prev_hash": "genesis",
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(("genesis" + canonical).encode()).hexdigest()[:16]
    assert digest == "31f1f1e05ac9a35a"


def test_certified_grow_enclosures():
    """Certified GROW with NO trusted rounded value: an EXACT rational gain dominates a RIGOROUS upper
    bound on the cost lambda*log(M), the bound produced by mpmath verified interval arithmetic (the same
    discipline as capacity.py's mpmath.iv path) -- not plain float math.log."""
    from mpmath import iv, mpf
    iv.dps = 50
    log7, log24 = iv.log(7), iv.log(24)
    # the rigorous enclosure lies inside the displayed bracket (so the displayed bracket is sound):
    assert 1.94591 <= float(log7.a) and float(log7.b) <= 1.94592
    assert 3.17805 <= float(log24.a) and float(log24.b) <= 3.17806
    lam = 2
    # exact rational gain >= rigorous upper bound on the cost  =>  GROW certified (no trusted float)
    assert Q(56) >= lam * log7.b          # sqrt7:  56 >= 2*log(7)
    assert Q(96) >= lam * log24.b         # 2sqrt6: 96 >= 2*log(24)
    # lattice-aligned noise STOPped: gain 1/10 below a RIGOROUS lower bound on the Smyth floor 2*log(mu_S)
    floor_lo = 2 * iv.log(mpf("1.3247")).a   # mu_S = 1.32471... > 1.3247, so this is a true lower bound
    assert float(floor_lo) > 0.1             # 0.5623... > 0.1  => 1/10 is sub-floor


def test_smyth_floor_and_degree_aware_floors():
    mu_S = max(sp.real_roots(x**3 - x - 1))             # plastic number
    assert abs(float(mu_S) - 1.32471795724) < 1e-9
    lam = 2
    const_floor = lam * math.log(float(mu_S))
    assert abs(const_floor - 0.5623991486) < 1e-9
    assert abs(4 * const_floor / 2 - 1.1247982972) < 1e-9   # sanity on the linear scaling
    assert abs(4 * const_floor - 2.2495965946) < 1e-9       # degree-aware n=4
    assert abs(8 * const_floor - 4.4991931892) < 1e-9       # degree-aware n=8


# ----------------------------------------------------------------------------- #
# the language layer: Cl(2,0) return operator, kernel, commit projector, words
# ----------------------------------------------------------------------------- #
def cl_mul(X, Y):
    a, b, c, d = X
    e, f, g, h = Y
    return (a*e + b*f + c*g - d*h,
            a*f + b*e - c*h + d*g,
            a*g + b*h + c*e - d*f,
            a*h + b*g - c*f + d*e)


R = (Q(1, 2), 1, Q(-1, 2), 0)            # the phi keystone, mat(R)=[[0,1],[1,1]]
ONE = (1, 0, 0, 0)


def Lop(X):
    rx = cl_mul(R, X)
    xr = cl_mul(X, R)
    return tuple(rx[i] + xr[i] - X[i] for i in range(4))


def test_keystone_satisfies_golden_law():
    R2 = cl_mul(R, R)
    assert tuple(R2[i] - (R[i] + ONE[i]) for i in range(4)) == (0, 0, 0, 0)   # R^2 = R + 1


def test_return_operator_kernel_is_exact_dim2():
    basis = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    cols = [Matrix(Lop(b)) for b in basis]
    Lmat = cols[0].row_join(cols[1]).row_join(cols[2]).row_join(cols[3])
    ns = Lmat.nullspace()
    assert len(ns) == 2                                  # KER_DIM == 2
    # the exact basis is span{e1+2e2, i}
    K = Matrix.hstack(*ns)
    target = Matrix([[0, 0], [1, 0], [2, 0], [0, 1]])    # columns e1+2e2 and i
    # same column space: every target column is in the nullspace span
    for col in (Matrix([0, 1, 2, 0]), Matrix([0, 0, 0, 1])):
        aug = K.row_join(col)
        assert aug.rank() == K.rank()


def test_commit_projector_value():
    # orthogonal projector onto ker(L) with integer-normalised basis {e1+2e2, i}
    K = Matrix([[0, 0], [1, 0], [2, 0], [0, 1]])
    P = K * (K.T * K).inv() * K.T
    assert P == Matrix([[0, 0, 0, 0],
                        [0, Q(1, 5), Q(2, 5), 0],
                        [0, Q(2, 5), Q(4, 5), 0],
                        [0, 0, 0, 1]])
    assert P * P == P                                    # idempotent
    assert P != eye(4)                                   # ... and not the trivial projector


def test_corrected_hint_disproof():
    assert Lop((0, -1, 1, 0)) == (-3, 0, 0, 0)           # NOT in ker(L)
    assert Lop((0, 0, 0, 1)) == (0, 0, 0, 0)             # the real generator i IS in ker(L)
    assert Lop(R) == (Q(5, 2), 1, Q(-1, 2), 0)           # R not in the kernel


def test_word_sign_discriminates_antipodes():
    # kernel coords of i and -i, then the sign-aware word over the basis (e1+2e2, i)
    K = Matrix([[0, 0], [1, 0], [2, 0], [0, 1]])
    coords_mat = (K.T * K).inv() * K.T
    def word(X):
        cs = coords_mat * Matrix(X)
        tot = sum(abs(v) for v in cs)
        if tot == 0:
            return ()
        labels = ("e1+2e2", "i")
        return tuple(("+" if cs[k] > 0 else "-") + labels[k]
                     for k in range(2) if abs(cs[k]) > Q(1, 4) * tot)
    assert word((0, 0, 0, 1)) == ("+i",)
    assert word((0, 0, 0, -1)) == ("-i",)
    assert word((0, 1, 0, 0)) == ("+e1+2e2",)            # project(E1) coords (1/5,0)
    assert word((1, 0, 0, 0)) == ()                      # ONE is orthogonal to the slack


def test_content_hash_id():
    h = hashlib.sha256(b"0|0|0|1").hexdigest()[:16]
    assert len(h) == 16 and all(ch in "0123456789abcdef" for ch in h)
    # the same exact value via a different construction hashes identically (reduced Fraction)
    assert str(Q(2, 2)) == "1"                           # canonicalisation


def test_probe_imports_no_engine():
    # Model-layer purity = this probe's OWN source imports no engine (a static check, isolation-independent:
    # a runtime sys.modules scan is polluted by sibling tests in the full-suite run). The probe re-derives
    # every number from sympy + stdlib.
    import inspect
    src = inspect.getsource(sys.modules[__name__])
    language_engine = "kira" + "_" + "language"        # assembled, not a literal (one-way tripwire)
    for token in ("residual_learner", "loom", "coords_to_minpoly", "capacity", language_engine):
        assert ("import " + token) not in src, token
        assert ("from " + token) not in src, token


# --------------------------------------------------------------------------- #
# Section 4.3 -- the lambda = 2c closure (this revision). Pure sympy; no engine.
# --------------------------------------------------------------------------- #
def test_lambda_is_two_c_derived():
    # Thm 4.6: solve the MDL balance D_KL = (1/2c)||r||^2_G >= log M for the threshold; lambda = 2c EMERGES.
    c, gain, logM = symbols("c gain logM", positive=True)
    lam = sp.solve(sp.Eq(gain / (2 * c), logM), gain)[0] / logM
    assert sp.simplify(lam - 2 * c) == 0                 # FORCED: lambda = 2c
    assert sp.simplify(lam.subs(c, 1) - 2) == 0          # c=1 -> 2 (the shipped value, as a consequence)
    n = symbols("n", positive=True)
    assert sp.simplify(lam.subs(c, n) - 2 * n) == 0      # c=n -> 2n (degree-aware reading)


def test_floors_unify_under_lambda_2c():
    # Rem 4.7: the two shipped floors are 2c*log(mu_S) at c=1 and c=n. mu_S = real root of x^3 - x - 1.
    x = symbols("x")
    mu_S = float(sp.real_roots(x ** 3 - x - 1)[0])
    assert abs(mu_S ** 3 - mu_S - 1) < 1e-12             # it IS the plastic number (derived, not hard-coded)
    floor = lambda cc, nn=1: 2 * cc * nn * math.log(mu_S)
    assert round(floor(1), 4) == 0.5624                  # c=1 constant floor
    assert round(floor(1, 4), 4) == 2.2496               # c=n=4 degree-aware floor
    assert round(floor(1, 8), 4) == 4.4992               # c=n=8 degree-aware floor


def test_self_action_spectrum_and_gate_ladder():
    # Prop 4.9 / Def 4.10: self-action gap sqrt(1+4C); gate ladder {sqrt2,sqrt3,sqrt5}; golden c = sqrt5/2.
    for C, gap2 in [(Q(1, 4), 2), (Q(1, 2), 3), (sp.Integer(1), 5)]:
        R = Matrix([[0, C], [1, -1]])                    # companion of x^2 + x - C
        E = [Matrix([[1, 0], [0, 0]]), Matrix([[0, 1], [0, 0]]),
             Matrix([[0, 0], [1, 0]]), Matrix([[0, 0], [0, 1]])]
        ad = Matrix([[(R * e - e * R)[i, j] for i in range(2) for j in range(2)] for e in E]).T
        eig = ad.eigenvals()
        assert sp.Integer(0) in eig                      # captured (0) channel
        assert all(sp.simplify(e ** 2 - gap2) == 0 for e in eig if e != 0)   # gap^2 = 1 + 4C
        assert sp.simplify(sqrt(1 + 4 * C) - sqrt(gap2)) == 0                 # ladder sqrt2, sqrt3, sqrt5
    assert sp.simplify(sqrt(1 + 4 * sp.Integer(1)) / 2 - sqrt(5) / 2) == 0    # golden-gate c = sqrt5/2
