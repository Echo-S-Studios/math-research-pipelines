"""test_compositum_nondisjoint.py -- P2c: the non-disjoint compositum (compositum.py's REFUSED
non_disjoint branch grown into real growth), plus its exact primitives (bounded Kronecker
Q-factorization, factor-selection, true-compositum construction).

ADDITIVE: imports only model-layer modules; the existing A2.P2b disjoint tests (test_compositum.py)
stay byte-identical (they use base_min_poly=None -- the unchanged tensor path).

Canonical witness: K = Q(sqrt2), beta = sqrt2 + sqrt3. m_beta = x^4 - 10x^2 + 1 FACTORS over K into two
quadratics, so e' = [K(beta):K] = 2 and the TRUE compositum Q(sqrt2,sqrt3) has degree [K:Q]*e' = 4 -- NOT
the disjoint tensor degree 2*4 = 8. After growth beta's residual is 0.
"""
import ast
import subprocess
import sys
import textwrap
from fractions import Fraction as F
import pytest

from number_field_factor import (factor_over_Q, is_irreducible_over_Q, FactorizationUnsupported,
                                  KRONECKER_DEGREE_CAP)
from compositum_nondisjoint import build_compositum, trace_form_gram
from compositum import CompositumLearner, Factor, FieldExtensionProposal, FieldExtensionRefusal
from field_extension import _unit, WorkingField

G_SQRT2 = [[2, 0], [0, 4]]                 # trace Gram of Q(sqrt2) on {1, sqrt2}
M_ALPHA = [1, 0, -2]                       # x^2 - 2  (K = Q(sqrt2))
M_BETA = [1, 0, -10, 0, 1]                 # x^4 - 10x^2 + 1  (beta = sqrt2 + sqrt3)


# ===== (1) bounded Kronecker Q-factorization ================================================= #
def test_factor_over_Q_correctness():
    assert factor_over_Q(M_BETA) == [[1, 0, -10, 0, 1]]                       # irreducible over Q
    assert factor_over_Q([1, 0, -5, 0, 6]) == [[1, 0, -3], [1, 0, -2]]       # (x^2-3)(x^2-2)
    # the c=1 witness operator-minpoly: (x^2-3) * (x^4-22x^2+25)
    assert factor_over_Q([1, 0, -25, 0, 91, 0, -75]) == [[1, 0, -3], [1, 0, -22, 0, 25]]
    assert factor_over_Q([1, 0, 0, 0, 0, 0, 1]) == [[1, 0, 1], [1, 0, -1, 0, 1]]   # x^6+1
    assert is_irreducible_over_Q([1, -3, 1])                                  # x^2-3x+1 (reciprocal, irred)


def test_factor_reconstructs_product():
    import mpmath as mp
    f = [1, 0, -25, 0, 91, 0, -75]
    facs = factor_over_Q(f)
    # multiply the factors back (LOW->HIGH convolution) and compare to f
    acc = [1]
    for fac in facs:
        lo = fac[::-1]
        acc = [sum(acc[i] * lo[j] for i in range(len(acc)) for j in range(len(lo)) if i + j == t)
               for t in range(len(acc) + len(lo) - 1)]
    assert acc[::-1] == f


def test_factor_over_Q_refuses_above_bound():
    big = [1] + [0] * (KRONECKER_DEGREE_CAP + 1)         # degree cap+1
    with pytest.raises(FactorizationUnsupported):
        factor_over_Q(big)


# ===== (2) true-compositum construction + exact factor-selection ============================= #
def test_build_compositum_witness():
    res = build_compositum(M_ALPHA, M_BETA)
    assert res.e_prime == 2                              # [K(beta):K] = 2 (m_beta splits over K)
    assert res.new_degree == 4                           # [Q(sqrt2,sqrt3):Q] = 4 -- NOT the tensor 8
    assert res.m_theta == [1, 0, -22, 0, 25]             # minpoly of theta = 2sqrt2+sqrt3
    # the spurious x^2-3 factor was correctly REJECTED (alpha=sqrt2 not in Q(sqrt3))
    assert [1, 0, -3] in res.factorization and res.m_theta in res.factorization
    # beta = (-7/20)theta + (1/20)theta^3 reconstructs sqrt2+sqrt3 (verified via the trace Gram: it is
    # captured with residual 0 in Q(theta))
    G = trace_form_gram(res.m_theta)
    W = WorkingField(G, [_unit(i, 4) for i in range(4)])
    assert W.detect(res.beta_coords).field_residual_norm == 0


def test_build_compositum_disjoint_and_in_K():
    # disjoint: Q(sqrt2,sqrt3) + sqrt7 -> e' = 2 = deg(m_beta), degree 8
    r = build_compositum([1, 0, -10, 0, 1], [1, 0, -7])
    assert r.e_prime == 2 and r.new_degree == 8
    # already in K: Q(sqrt2) + sqrt2 -> e' = 1
    r2 = build_compositum(M_ALPHA, M_ALPHA)
    assert r2.e_prime == 1


# ===== (3) the CANONICAL WITNESS end-to-end: detect -> propose -> confirm -> residual 0 ======= #
def test_p2c_witness_grows_true_compositum_not_tensor():
    beta = Factor("Q(sqrt2+sqrt3)", [[1]], M_BETA)       # gram unused on the non-disjoint path
    L = CompositumLearner(G_SQRT2, beta, base_min_poly=M_ALPHA)
    assert L.degree == 2                                  # captured field starts as K = Q(sqrt2)
    p = L.propose()
    assert isinstance(p, FieldExtensionProposal)
    assert p.disjoint is False and p.e_prime == 2
    assert p.old_degree == 2 and p.new_degree == 4        # TRUE compositum degree 4, NOT tensor 8
    assert p.m_theta == [1, 0, -22, 0, 25]
    assert L.degree == 2                                  # propose did NOT grow (pure)
    rec = L.confirm(p)
    assert L.degree == 4                                  # grown to the degree-4 compositum
    # the previously out-of-field beta is now captured (residual 0) in Q(theta)
    det = L.detect(p.beta_coords)
    assert det.field_residual_norm == 0 and det.in_field
    # witness records old->new degree, e', and m_theta; the chain verifies
    assert rec["old_degree"] == 2 and rec["new_degree"] == 4 and rec["e_prime"] == 2
    assert rec["m_theta"] == [1, 0, -22, 0, 25] and rec["disjoint"] is False
    assert L.verify_witness()


def test_p2c_witness_tamper_evident():
    beta = Factor("Q(sqrt2+sqrt3)", [[1]], M_BETA)
    L = CompositumLearner(G_SQRT2, beta, base_min_poly=M_ALPHA)
    L.confirm(L.propose())
    assert L.verify_witness()
    L._witness[0]["new_degree"] = 8                       # tamper: pretend it was the tensor degree
    assert not L.verify_witness()


# ===== (4) the negatives ==================================================================== #
def test_p2c_already_in_K_refused():
    # adjoin sqrt2 to Q(sqrt2): beta in K, e' = 1 -> refusal, no growth
    L = CompositumLearner(G_SQRT2, Factor("s2", [[1]], M_ALPHA), base_min_poly=M_ALPHA)
    r = L.propose()
    assert isinstance(r, FieldExtensionRefusal) and r.kind == "already_in_k"
    assert L.degree == 2                                  # no growth


def test_p2c_over_hard_degree_cap_refused():
    beta = Factor("Q(sqrt2+sqrt3)", [[1]], M_BETA)
    # the true compositum is degree 4; a cap of 3 refuses it
    r = CompositumLearner(G_SQRT2, beta, base_min_poly=M_ALPHA, degree_cap=3).propose()
    assert isinstance(r, FieldExtensionRefusal) and r.kind == "over_cap"


def test_p2c_over_kronecker_bound_refused_with_zassenhaus_message():
    # K = Q(sqrt2,sqrt3) [m=4], beta = sqrt5+sqrt7 [deg 4], disjoint -> m_theta degree 16 > Kronecker 12
    G_K = [[4, 0, 0, 0], [0, 8, 0, 0], [0, 0, 12, 0], [0, 0, 0, 24]]
    beta = Factor("Q(sqrt5+sqrt7)", [[1]], [1, 0, -24, 0, 4])
    r = CompositumLearner(G_K, beta, base_min_poly=[1, 0, -10, 0, 1], degree_cap=20).propose()
    assert isinstance(r, FieldExtensionRefusal) and r.kind == "factor_unsupported"
    assert "Zassenhaus" in r.reason


# ===== (5) guardrails: confirm is the sole mutator; exact; model-layer ======================= #
def test_p2c_confirm_is_sole_mutator_and_single_step():
    beta = Factor("Q(sqrt2+sqrt3)", [[1]], M_BETA)
    L = CompositumLearner(G_SQRT2, beta, base_min_poly=M_ALPHA)
    p = L.propose()
    L.propose()                                          # pure: still no growth
    assert L.degree == 2
    L.confirm(p)
    assert L.degree == 4
    with pytest.raises(ValueError):
        L.confirm(p)                                     # already extended -- single-step growth


def test_p2c_exact_only():
    beta = Factor("Q(sqrt2+sqrt3)", [[1]], M_BETA)
    L = CompositumLearner(G_SQRT2, beta, base_min_poly=M_ALPHA)
    p = L.propose()
    assert all(isinstance(c, (int, F)) for c in p.beta_coords)     # exact (G8)
    assert all(isinstance(c, int) for c in p.m_theta)              # monic-integer (G10)
    L.confirm(p)


def test_p2c_model_layer_no_kira_no_numpy():
    """The P2c path runs in a CLEAN subprocess with no numpy / KIRA / Plate-Matrices imported (the
    in-process sys.modules is polluted by other tests, so a fresh interpreter is the honest check)."""
    import compositum_nondisjoint as cnd
    code = textwrap.dedent(
        """
        import os, sys
        sys.path.insert(0, os.path.dirname(%r))
        from compositum import CompositumLearner, Factor
        L = CompositumLearner([[2,0],[0,4]], Factor("b", [[1]], [1,0,-10,0,1]), base_min_poly=[1,0,-2])
        rec = L.confirm(L.propose())
        assert L.degree == 4 and rec["e_prime"] == 2 and L.verify_witness()
        assert "numpy" not in sys.modules and "loom" not in sys.modules
        assert not any(m.startswith("kira") for m in sys.modules)
        print("CLEAN")
        """ % (cnd.__file__,)
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "CLEAN" in out.stdout
    # static check: the new modules import no numpy / sympy / kira
    for mod in (cnd.__file__,
                cnd.__file__.replace("compositum_nondisjoint", "number_field_factor")):
        imported = set()
        for node in ast.walk(ast.parse(open(mod, encoding="utf-8").read())):
            if isinstance(node, ast.Import):
                imported |= {n.name.split(".")[0] for n in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert "numpy" not in imported and "sympy" not in imported
        assert not any(m.startswith("kira") for m in imported)


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
