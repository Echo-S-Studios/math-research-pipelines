"""test_paper_claims.py -- machine-checked reproduction of EVERY displayed number added to
paper/vector_substrate.tex in the 28-30pp expansion (figures + the discriminant-as-information-volume and
spectral-unification results + the certified-interval and lattice-noise examples + the fields catalog).

RESEARCH / paper-verification probe. ADDITIVE: it imports no shipped learner/capacity/compositum code and
mutates nothing; it recomputes the paper's numbers from scratch with sympy (exact) and mpmath (certified
intervals / high precision). Honesty: PROVABLE quantities are checked EXACTLY (sympy); the certified-interval
log-M enclosure is a rigorous interval (mpmath.iv); model-dependent constants (lambda, mu_S) are pinned at
their documented values. Model-layer only; the KIRA engine is never imported.

Sections (mirror the paper):
  (1) det(trace-form Gram) = d_K (integral basis) or index^2 * d_K (product sub-order)        [catalog]
  (2) Jeffreys-prior / Minkowski volume sqrt(det G) = sqrt|d_K| (integral basis)               [Result B]
  (3) different (m'(gen)), N(different) = |disc(m)| = |d_K|                                     [catalog]
  (4) spectral unification: M rho(x) M^-1 = diag(sigma_k(x)); charpoly(rho(theta)) = m_theta   [Result C]
  (5) Mahler measure as spectral invariant: M(theta) = prod_{|lambda|>1} |lambda|              [Result C]
  (6) certified-interval threshold: rigorous [lo,hi] ∋ log M; gain >= lambda*hi => GROW        [E.1]
  (7) lattice-aligned noise: tiny trace-zero residual (gain 1/10): floor=0 GROWs, Smyth STOPs  [E.2]
  (8) figure data: Q(sqrt5) projection coeff 5/3 & residual 5/3; plastic mu_S, Lehmer mu_L     [Figs 2,3,4]
"""
import os
import sys
from fractions import Fraction

import sympy as sp
import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

x = sp.symbols("x")
s2, s3, s5, s7 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(5), sp.sqrt(7)
PHI = (1 + s5) / 2
PHIc = (1 - s5) / 2
c2 = sp.root(2, 3)                                   # real cube root of 2
OM = -sp.Rational(1, 2) + sp.sqrt(3) * sp.I / 2      # primitive cube root of unity (x^2+x+1 root)

LAMBDA = 2
# Smyth's floor: the plastic number, the real root of x^3 - x - 1 (non-reciprocal minimal Mahler measure).
MU_SMYTH = sp.real_root(sp.CRootOf(x**3 - x - 1, 0), 1)   # exact algebraic number; numerically 1.3247...


# --------------------------------------------------------------------------- #
#  the catalog: (name, M = embedding matrix rows=embeddings cols=basis, d_K, index)
# --------------------------------------------------------------------------- #
def _catalog():
    M5 = sp.Matrix([[1, PHI], [1, PHIc]])
    M_2 = sp.Matrix([[1, s2], [1, -s2]])
    M_3 = sp.Matrix([[1, s3], [1, -s3]])
    M_7 = sp.Matrix([[1, s7], [1, -s7]])
    M_i = sp.Matrix([[1, sp.I], [1, -sp.I]])
    # Q(cbrt2): basis {1, c, c^2}; embeddings c -> c, c*OM, c*OM^2
    M_c = sp.Matrix([[1, c2, c2**2],
                     [1, c2 * OM, c2**2 * OM**2],
                     [1, c2 * OM**2, c2**2 * OM**4]])
    # Q(sqrt2,sqrt3): product basis {1, s2, s3, s6}; 4 sign embeddings
    rows = []
    for a in (1, -1):
        for b in (1, -1):
            rows.append([1, a * s2, b * s3, a * b * sp.sqrt(6)])
    M_23 = sp.Matrix(rows)
    return [
        ("Q(sqrt5)", M5, 5, 1),
        ("Q(sqrt2)", M_2, 8, 1),
        ("Q(sqrt3)", M_3, 12, 1),
        ("Q(sqrt7)", M_7, 28, 1),
        ("Q(i)", M_i, -4, 1),
        ("Q(cbrt2)", M_c, -108, 1),
        ("Q(sqrt2,sqrt3)", M_23, 2304, 2),   # product basis spans an index-2 sub-order
    ]


def _gram(M):
    """Trace-form Gram G = M^T M (real even for complex M)."""
    return sp.simplify(M.T * M)


# == (1) det(trace Gram) = d_K (integral basis) or index^2 d_K (sub-order) ===================== #
def test_det_gram_is_discriminant():
    for name, M, dK, idx in _catalog():
        G = _gram(M)
        detG = sp.nsimplify(sp.simplify(G.det()))
        expected = idx**2 * dK
        assert sp.simplify(detG - expected) == 0, f"{name}: det G = {detG} != {expected}"


# == (2) Jeffreys / Minkowski volume sqrt(det |G|) = sqrt|d_K| (integral basis) ================ #
def test_jeffreys_volume_is_sqrt_discriminant():
    # For an integral basis the Fisher/Jeffreys volume of one lattice cell is sqrt|d_K|.
    expect = {
        "Q(sqrt5)": sp.sqrt(5), "Q(sqrt2)": 2 * sp.sqrt(2), "Q(sqrt3)": 2 * sp.sqrt(3),
        "Q(sqrt7)": 2 * sp.sqrt(7), "Q(i)": sp.Integer(2), "Q(cbrt2)": 6 * sp.sqrt(3),
    }
    for name, M, dK, idx in _catalog():
        if name not in expect:
            continue
        G = _gram(M)
        vol = sp.sqrt(sp.Abs(sp.nsimplify(G.det())))      # sqrt|det G|
        assert sp.simplify(vol - expect[name]) == 0, f"{name}: vol {vol} != {expect[name]}"
        # and it equals sqrt|d_K|
        assert sp.simplify(vol - sp.sqrt(sp.Abs(dK))) == 0, f"{name}: vol != sqrt|d_K|"
    # the index-2 product order: vol = 2*sqrt(2304) = 96 = index * sqrt|d_K|
    G23 = _gram(_catalog()[-1][1])
    assert sp.sqrt(G23.det()) == 96
    assert sp.simplify(sp.sqrt(G23.det()) - 2 * sp.sqrt(2304)) == 0


# == (2b) Model-2 volume rescaling: det(G/n) = n^{-d} det G, so cell volume scales by n^{-d/2} ==== #
def test_information_volume_model2_rescaling():
    # rem:volmodel: the Model-2 metric on the residual subspace is G/n; its volume element rescales one
    # cell by n^{-d/2} (since det(cA) = c^d det A). This pins "information volume = sqrt|d_K|" as the
    # Model-1 (c=1) reading, consistent with conj:model.
    for name, M, dK, idx in _catalog():
        G = _gram(M)
        n = M.shape[0]                                   # number of embeddings = degree
        d = M.shape[1]                                   # basis size
        detG = sp.nsimplify(sp.simplify(G.det()))
        detGn = sp.nsimplify(sp.simplify((G / n).det()))
        assert sp.simplify(detGn - sp.Rational(1, n) ** d * detG) == 0, f"{name}: det(G/n) != n^-d det G"
        # the volume (sqrt|det|) rescales by exactly n^{-d/2}
        lhs = sp.sqrt(sp.Abs(detGn))
        rhs = sp.Rational(1, n) ** sp.Rational(d, 2) * sp.sqrt(sp.Abs(detG))
        assert sp.simplify(lhs - rhs) == 0, f"{name}: volume rescale != n^-d/2"


# == (9) reciprocity: the worked seeds are NON-reciprocal, so Smyth's floor is unconditional for them ==== #
def _is_reciprocal(coeffs):
    """coeffs low-to-high, monic; reciprocal iff the coefficient list is palindromic up to an overall sign."""
    rev = list(reversed(coeffs))
    return rev == list(coeffs) or [-c for c in rev] == list(coeffs)


def test_worked_seeds_are_non_reciprocal():
    # rem:reciprocal: Smyth's floor mu_S is a THEOREM only for non-reciprocal integers; the reciprocal case
    # (Salem numbers, units) has NO proven uniform floor. The paper's worked seeds are all non-reciprocal,
    # so their positive floors are unconditional -- this asserts exactly that.
    for name, coeffs in [("phi: x^2-x-1", [-1, -1, 1]),
                         ("2sqrt6: x^2-24", [-24, 0, 1]),
                         ("sqrt7: x^2-7", [-7, 0, 1])]:
        assert not _is_reciprocal(coeffs), f"{name} unexpectedly reciprocal"
    # sanity: a genuinely reciprocal polynomial (x^2 - 3x + 1, a Salem-like unit) is detected as reciprocal
    assert _is_reciprocal([1, -3, 1])


# == (3) different = (m'(gen)); N(different) = |disc(m)| = |d_K|  (monogenic catalog) ========== #
def test_different_norm_is_discriminant():
    cases = {
        "Q(sqrt5)": (x**2 - x - 1, 5),
        "Q(sqrt2)": (x**2 - 2, 8),
        "Q(sqrt3)": (x**2 - 3, 12),
        "Q(sqrt7)": (x**2 - 7, 28),
        "Q(i)":     (x**2 + 1, -4),
        "Q(cbrt2)": (x**3 - 2, -108),
    }
    for name, (m, dK) in cases.items():
        # N(m'(gen)) = prod over roots of m of m'(root) = +- disc(m); |.| = |d_K| for a monogenic O_K
        disc = sp.discriminant(m, x)
        assert disc == dK, f"{name}: disc(m) = {disc} != {dK}"
        roots = sp.Poly(m, x).all_roots()
        mp_ = sp.diff(m, x)
        Nprime = sp.simplify(sp.prod([mp_.subs(x, r) for r in roots]))
        assert sp.Abs(sp.nsimplify(Nprime)) == sp.Abs(dK), f"{name}: |N(m'(gen))| != |d_K|"


# == (4) spectral unification: M rho(x) M^-1 = diag(conjugates); charpoly(rho(theta)) = m =====  #
def _companion(coeffs_monic):
    """Companion matrix of a monic poly given low-to-high coeffs [c0,...,c_{n-1},1]."""
    n = len(coeffs_monic) - 1
    C = sp.zeros(n, n)
    for i in range(1, n):
        C[i, i - 1] = 1
    for i in range(n):
        C[i, n - 1] = -coeffs_monic[i]
    return C


def test_spectral_diagonalisation_exact_small_fields():
    # Q(sqrt5): rho(phi) = companion(x^2 - x - 1); M diagonalises it to diag(phi, phi').
    rho_phi = _companion([-1, -1, 1])               # x^2 - x - 1
    M5 = sp.Matrix([[1, PHI], [1, PHIc]])
    D = sp.simplify(M5 * rho_phi * M5.inv())
    assert sp.simplify(D - sp.diag(PHI, PHIc)) == sp.zeros(2, 2)
    # Q(sqrt2): rho(sqrt2) = companion(x^2 - 2); M diagonalises to diag(sqrt2, -sqrt2).
    rho_2 = _companion([-2, 0, 1])
    M_2 = sp.Matrix([[1, s2], [1, -s2]])
    D2 = sp.simplify(M_2 * rho_2 * M_2.inv())
    assert sp.simplify(D2 - sp.diag(s2, -s2)) == sp.zeros(2, 2)


def test_spectral_charpoly_equals_minpoly_and_eigs_are_conjugates():
    # Q(sqrt2+sqrt3): rho(theta) = companion(x^4 - 10x^2 + 1); charpoly = the minimal polynomial.
    rho_th = _companion([1, 0, -10, 0, 1])          # x^4 - 10 x^2 + 1
    cp = sp.factor(rho_th.charpoly(x).as_expr())
    assert sp.simplify(cp - (x**4 - 10 * x**2 + 1)) == 0
    # eigenvalues (numeric) are exactly the four conjugates +-sqrt2 +-sqrt3
    conj = sorted(float(sp.N(v)) for v in (s2 + s3, s2 - s3, -s2 + s3, -s2 - s3))
    eig = sorted(float(re) for re in mp.polyroots([1, 0, -10, 0, 1]))
    assert all(abs(a - b) < 1e-9 for a, b in zip(conj, eig)), (conj, eig)


# == (5) Mahler measure as a spectral invariant: M = prod_{|lambda|>1} |lambda| =============== #
def _mahler_from_spectrum(coeffs_high_to_low):
    roots = mp.polyroots(coeffs_high_to_low)
    prod = mp.mpf(1)
    for r in roots:
        if abs(r) > 1:
            prod *= abs(r)
    return prod


def test_mahler_is_spectral_invariant():
    # theta = sqrt2 + sqrt3: M(theta) = prod_{|lambda|>1}|lambda| over spec(rho(theta)) = 5 + 2 sqrt6.
    M_theta = _mahler_from_spectrum([1, 0, -10, 0, 1])
    assert abs(M_theta - float(5 + 2 * sp.sqrt(6))) < 1e-9
    # plastic number (Smyth): M = mu_S itself (only the real root exceeds 1).
    M_plastic = _mahler_from_spectrum([1, 0, -1, -1])     # x^3 - x - 1
    assert abs(M_plastic - float(sp.N(MU_SMYTH))) < 1e-12
    # its complex conjugate pair lies strictly inside the unit circle (|lambda| = 1/sqrt(mu_S))
    roots = mp.polyroots([1, 0, -1, -1])
    cmod = [abs(r) for r in roots if abs(r.imag) > 1e-12]
    assert cmod and all(m < 1 for m in cmod)
    assert abs(cmod[0] - float(sp.N(1 / sp.sqrt(MU_SMYTH)))) < 1e-9


# == (6) certified-interval threshold: rigorous enclosure of log M; gain >= lambda*hi => GROW = #
def test_certified_interval_threshold_grows():
    mp.mp.dps = 30
    for M_seed, gain, lo, hi in [
        (7, Fraction(56), Fraction(194591, 100000), Fraction(194592, 100000)),    # sqrt7 in the compositum
        (24, Fraction(96), Fraction(317805, 100000), Fraction(317806, 100000)),   # 2 sqrt6 in Q(sqrt2+sqrt3)
    ]:
        # the rational bounds rigorously enclose log M: exp(lo) < M < exp(hi) (high precision, with margin)
        assert mp.e ** mp.mpf(str(lo)) < M_seed < mp.e ** mp.mpf(str(hi))
        # certified GROW: the EXACT rational gain dominates lambda * (certified upper bound of the cost)
        assert Fraction(gain) >= LAMBDA * hi
        # cross-check against an independent interval-arithmetic enclosure (mpmath.iv)
        iv = mp.iv.log(M_seed)
        assert float(iv.a) >= float(lo) - 1e-6 and float(iv.b) <= float(hi) + 1e-6


# == (7) lattice-aligned noise: tiny trace-zero off-axis residual; floor=0 GROWs, Smyth STOPs = #
def test_lattice_aligned_noise_stopped_by_floor():
    G = sp.Matrix([[2, 1], [1, 3]])                 # Q(sqrt5) trace Gram in {1, phi}
    t = sp.Matrix([2, 1])                           # trace vector: Tr(1)=2, Tr(phi)=1
    sqrt5 = sp.Matrix([-1, 2])                       # sqrt5 = 2 phi - 1, trace-zero off-axis direction
    r = sp.Rational(1, 10) * sqrt5                   # an arbitrarily-small exact multiple
    assert (t.T * r)[0] == 0                         # trace-zero (G-orthogonal to 1)
    gain = sp.simplify((r.T * G * r)[0])
    assert gain == sp.Rational(1, 10)               # ||r||^2_G = 1/10, exact
    floor = LAMBDA * sp.log(MU_SMYTH)               # Smyth floor lambda * log mu_S
    assert float(gain) > 0                          # shipped gate (floor=0) would GROW
    assert float(gain) < float(floor)               # principled Smyth floor STOPs it (0.1 < 0.5623)
    assert abs(float(floor) - 0.5623) < 1e-3


# == (8) figure data: Q(sqrt5) projection coefficient and residual; plastic / Lehmer constants = #
def test_figure_projection_numbers():
    # Fig.2 (Minkowski-plane projection of sqrt5 onto R.sigma(phi)): coefficient and residual norm are 5/3.
    G = sp.Matrix([[2, 1], [1, 3]])
    B = sp.Matrix([[0], [1]])                        # forced basis <phi>
    xv = sp.Matrix([-1, 2])                          # sqrt5
    a_star = sp.simplify((B.T * G * B).inv() * (B.T * G * xv))
    assert a_star[0] == sp.Rational(5, 3)
    P = B * (B.T * G * B).inv() * B.T * G
    r = xv - P * xv
    assert sp.simplify((r.T * G * r)[0]) == sp.Rational(5, 3)
    # in the Minkowski plane: sigma(phi)=(phi,phi'), sigma(sqrt5)=(sqrt5,-sqrt5); Euclidean proj coeff = 5/3
    sig_phi = sp.Matrix([PHI, PHIc])
    sig_r5 = sp.Matrix([s5, -s5])
    coeff = sp.simplify((sig_phi.T * sig_r5)[0] / (sig_phi.T * sig_phi)[0])
    assert coeff == sp.Rational(5, 3)


def test_figure_threshold_and_floor_numbers():
    assert abs(float(LAMBDA * sp.log(24)) - 6.356) < 1e-3       # 2 sqrt6 cost
    assert abs(float(LAMBDA * sp.log(7)) - 3.892) < 1e-3        # sqrt7 cost
    assert abs(float(LAMBDA * sp.log(MU_SMYTH)) - 0.5623) < 1e-3   # constant floor
    assert abs(float(4 * LAMBDA * sp.log(MU_SMYTH)) - 2.25) < 1e-2  # degree-aware n=4
    assert abs(float(8 * LAMBDA * sp.log(MU_SMYTH)) - 4.50) < 1e-2  # degree-aware n=8
    # Lehmer's number mu_L ~ 1.17628 is the largest real root of Lehmer's degree-10 polynomial
    L = [1, 1, 0, -1, -1, -1, -1, -1, 0, 1, 1]
    mu_L = max(float(r.real) for r in mp.polyroots(L) if abs(r.imag) < 1e-9)
    assert abs(mu_L - 1.17628) < 1e-4


def test_paper_claims_model_layer_no_kira():
    assert "kira_server_canonical" not in sys.modules


if __name__ == "__main__":
    import mpmath as _mp
    _mp.mp.dps = 30
    print("log 7  in", _mp.iv.log(7))
    print("log 24 in", _mp.iv.log(24))
    print("mu_S =", _mp.mpf(str(sp.N(MU_SMYTH, 20))), " 2 log mu_S =", float(2 * sp.log(MU_SMYTH)))
    print("M(sqrt2+sqrt3) =", _mahler_from_spectrum([1, 0, -10, 0, 1]), " 5+2sqrt6 =", float(5 + 2 * sp.sqrt(6)))
