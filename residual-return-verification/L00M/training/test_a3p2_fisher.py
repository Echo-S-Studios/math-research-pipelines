"""test_a3p2_fisher.py -- A3.P2a RESEARCH probe: trace-form Gram G vs the Fisher information metric (F4).

A reproducible, EXACT (symbolic, sympy) verification of the relationships derived in A3_P2_RESEARCH.md.
This is a RESEARCH probe -- it touches no shipped code and computes/asserts the Fisher-vs-G relationship
on the catalog fields so the result is checkable:

  Structural:  G = M^T M           (the trace form is the Gram of the Minkowski embedding M)
  Model 1:     Fisher_Gauss = M^T M = G      (isotropic Gaussian location N(Ma, I), totally real)
  Model 2:     Fisher_expfam(uniform) = (1/n)(G - (1/n) t t^T),  t = trace vector
               -> on the trace-zero (= residual) subspace:  G = n * Fisher_expfam   EXACTLY

Fields: Q(sqrt5), Q(sqrt2,sqrt3), and the compositum Q(sqrt2,sqrt3,sqrt7). sympy is used for exact
symbolic embeddings (research lane). Model-layer only; no z/KIRA/Plate-Matrices.
"""
import os
import sys
from fractions import Fraction

import sympy as sp

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

s2, s3, s5, s7 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(5), sp.sqrt(7)
PHI = (1 + s5) / 2


def _field_cases():
    """(name, basis_label, M (embedding matrix, rows = embeddings), G_expected, n)."""
    # -- Q(sqrt5) = Q(phi), power basis {1, phi}; 2 embeddings phi -> (1 +/- sqrt5)/2 --------
    Q5 = ("Q(sqrt5)", "{1, phi}",
          sp.Matrix([[1, (1 + s5) / 2],
                     [1, (1 - s5) / 2]]),
          sp.Matrix([[2, 1], [1, 3]]), 2)

    # -- Q(sqrt2,sqrt3), product basis {1, sqrt2, sqrt3, sqrt6}; 4 sign embeddings (s,t) --------
    rows23 = []
    for a in (1, -1):
        for b in (1, -1):
            rows23.append([1, a * s2, b * s3, a * b * sp.sqrt(6)])
    Q23 = ("Q(sqrt2,sqrt3)", "{1, sqrt2, sqrt3, sqrt6}",
           sp.Matrix(rows23), sp.diag(4, 8, 12, 24), 4)

    # -- compositum Q(sqrt2,sqrt3,sqrt7), product basis {1,sqrt7,sqrt2,sqrt14,sqrt3,sqrt21,sqrt6,sqrt42} --
    rows237 = []
    for a in (1, -1):           # sign of sqrt2
        for b in (1, -1):       # sign of sqrt3
            for c in (1, -1):   # sign of sqrt7
                rows237.append([1, c * s7, a * s2, a * c * sp.sqrt(14), b * s3,
                                b * c * sp.sqrt(21), a * b * sp.sqrt(6), a * b * c * sp.sqrt(42)])
    Q237 = ("Q(sqrt2,sqrt3,sqrt7)", "{1,sqrt7,sqrt2,sqrt14,sqrt3,sqrt21,sqrt6,sqrt42}",
            sp.Matrix(rows237), sp.diag(8, 56, 16, 112, 24, 168, 48, 336), 8)

    return [Q5, Q23, Q237]


def _fisher_data(M, G, n):
    d = M.shape[1]
    MtM = sp.simplify(M.T * M)
    t = sp.simplify(M.T * sp.ones(n, 1))                       # trace vector t_i = sum_k sigma_k(omega_i)
    fisher_gauss = MtM                                        # Model 1: isotropic Gaussian -> M^T M
    fisher_expfam = sp.simplify(sp.Rational(1, n) * (M.T * M) - sp.Rational(1, n * n) * (t * t.T))  # Model 2
    return d, MtM, t, fisher_gauss, fisher_expfam


# ===========================================================================  #
#  the assertions (exact, symbolic)
# ===========================================================================  #
def test_a3p2_G_equals_MtM_and_fisher_relationships():
    for name, label, M, G, n in _field_cases():
        d, MtM, t, fisher_gauss, fisher_expfam = _fisher_data(M, G, n)

        # (1) STRUCTURAL: the trace form is the Minkowski-embedding Gram, G = M^T M  (== Model-1 Fisher)
        assert sp.simplify(MtM - G) == sp.zeros(d, d), f"{name}: G != M^T M"
        assert sp.simplify(fisher_gauss - G) == sp.zeros(d, d), f"{name}: isotropic-Gaussian Fisher != G"

        # (2) Model-2 Fisher equals the centered trace form (1/n)(G - (1/n) t t^T) -- exact
        expected_expfam = sp.simplify(sp.Rational(1, n) * (G - sp.Rational(1, n) * (t * t.T)))
        assert sp.simplify(fisher_expfam - expected_expfam) == sp.zeros(d, d), f"{name}: exp-fam Fisher form"

        # (3) Tr(1) = n (the constant always has trace n); the centering (1/n^2) t t^T is rank-1 along t.
        #     (In an orthogonal-surd basis t = (n,0,...,0); in the power basis {1,phi} t = (2,1) -- the
        #      residual result below is basis-independent, stated on the trace-zero SUBSPACE.)
        assert t[0] == n, f"{name}: Tr(1) != n"

        # (4) on the TRACE-ZERO (= residual) subspace, G = n * Fisher_expfam  EXACTLY (conformal c = n).
        #     The residual r = x - Px is G-orthogonal to the forced subspace; since the forced subspace
        #     contains 1, r is orthogonal to 1, i.e. Tr(r) = 0 -> r lives in nullspace(t^T).
        null = (t.T).nullspace()                             # basis of {v : t^T v = 0}, dim d-1
        assert len(null) == d - 1
        for v in null:
            vGv = sp.simplify((v.T * G * v)[0])
            vFv = sp.simplify((v.T * fisher_expfam * v)[0])
            assert sp.simplify(vGv - n * vFv) == 0, f"{name}: G != n*Fisher on a trace-zero direction"
            assert vFv != 0                                  # a genuine (non-degenerate) information direction


def test_a3p2_residual_norm_is_degree_scaled_fisher():
    # ||r||^2_G == n * Fisher_expfam(r) for a concrete residual: sqrt5 = 2*phi - 1 in Q(sqrt5),
    # which is trace-zero (Tr(sqrt5) = 0), i.e. it lives in the residual subspace orthogonal to 1.
    name, label, M, G, n = _field_cases()[0]
    _, _, t, _, fisher = _fisher_data(M, G, n)
    r = sp.Matrix([-1, 2])                                    # coords of sqrt5 = -1 + 2*phi
    assert sp.simplify((t.T * r)[0]) == 0                     # trace-zero -> in the residual subspace
    rGr = sp.simplify((r.T * G * r)[0])
    rFr = sp.simplify((r.T * fisher * r)[0])
    assert rGr == 10 and rFr == sp.Rational(5, 2) * 2         # ||sqrt5||^2_G = 10, Fisher = 5
    assert sp.simplify(rGr - n * rFr) == 0                    # 10 == 2 * 5  (G = n * Fisher on the residual)


def test_a3p2_fisher_matrices_exact_values():
    # pin the exact Model-2 Fisher matrices (the documented evidence)
    cases = {c[0]: c for c in _field_cases()}
    _, _, M5, G5, n5 = cases["Q(sqrt5)"]
    F5 = _fisher_data(M5, G5, n5)[4]
    assert F5 == sp.Matrix([[0, 0], [0, sp.Rational(5, 4)]])              # Fisher(phi-direction) = 5/4

    _, _, M23, G23, n23 = cases["Q(sqrt2,sqrt3)"]
    F23 = _fisher_data(M23, G23, n23)[4]
    assert F23 == sp.diag(0, 2, 3, 6)                                     # = (1/4) diag(0,8,12,24)

    _, _, M237, G237, n237 = cases["Q(sqrt2,sqrt3,sqrt7)"]
    F237 = _fisher_data(M237, G237, n237)[4]
    assert F237 == sp.diag(0, 7, 2, 14, 3, 21, 6, 42)                     # = (1/8) diag(0,56,16,...)


def test_a3p2_model_layer_no_kira():
    # research probe: imports sympy (research lane) + stdlib only; the KIRA engine is never pulled.
    # (A bare startswith("kira") scan would false-fail in the FULL suite, where test_kira_matrix_modules
    #  has loaded the additive kira_matrix_modules; the guardrail is that the KIRA *engine* stays out.)
    assert "kira_server_canonical" not in sys.modules


def test_a3p2_residual_perp_1_requires_1_in_B():
    # CAVEAT (load-bearing, Ace): r perp_G 1 -- hence the ||r||^2_G = n*Fisher reading -- holds ONLY when
    # the forced basis B contains 1. 1 is NOT auto-injected. Demonstrated EXACTLY on Q(sqrt5) via the L0
    # projector: B = span{1} -> Tr(residual) = 0 (Fisher applies); B = span{phi} -> Tr(residual) = 5/3 != 0.
    from fractions import Fraction as Fr
    from projector import projector_matrix, residual
    G = [[Fr(2), Fr(1)], [Fr(1), Fr(3)]]
    t = (Fr(2), Fr(1))                                       # trace vector: Tr(1)=2, Tr(phi)=1
    def trace_of(r):                                         # Tr(element) = t . r
        return t[0] * r[0] + t[1] * r[1]
    # 1 IN B (span{1}): residual of phi is trace-zero -> r perp 1 -> the Fisher identity applies
    P1 = projector_matrix([[Fr(1)], [Fr(0)]], G)
    assert trace_of(residual([Fr(0), Fr(1)], P1)) == 0
    # 1 NOT in B (span{phi}): residual of 1 has NONZERO trace -> r not-perp 1 -> the Fisher reading does NOT apply
    Pphi = projector_matrix([[Fr(0)], [Fr(1)]], G)
    assert trace_of(residual([Fr(1), Fr(0)], Pphi)) == Fr(5, 3)
