"""test_field_extension.py -- assert-bearing gate for A2.P2a (out-of-field DETECTION, no growth).

W = Q(sqrt2, sqrt3, sqrt7), degree 8, product basis e_i (x) f_j (flat index i*2 + j), tensor Gram
G_W = G_K (x) G_L (Prop 3.3). Captured sub-field K = Q(sqrt2, sqrt3) = span{e_i (x) f_0} = indices
{0,2,4,6} = {1, sqrt2, sqrt3, sqrt6}. Out-of-field axes {1,3,5,7} = {sqrt7, sqrt14, sqrt21, sqrt42}.

DETECTION ONLY: field_residual == 0 iff in K; != 0 flags an extension WOULD be needed (never grown).
"""
import ast
import os
import subprocess
import sys
import textwrap
from fractions import Fraction

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import field_extension as fx
from field_extension import WorkingField, FieldDetection, HARD_DEGREE_CAP, tensor_gram, kron, _unit

F = Fraction
G_K = [[4, 0, 0, 0], [0, 8, 0, 0], [0, 0, 12, 0], [0, 0, 0, 24]]   # Q(sqrt2,sqrt3) trace form, det 9216
G_L = [[2, 0], [0, 14]]                                            # Q(sqrt7) trace form, det 28


def _W():
    return WorkingField.from_two_factors(G_K, G_L)                 # W = Q(sqrt2,sqrt3,sqrt7), degree 8


# -- in-field: zero residual, no flag --------------------------------------- #
def test_in_field_elements_zero_residual_no_flag():
    W = _W()
    for v in (_unit(0, 8),                                  # 1
              _unit(2, 8),                                  # sqrt2
              _unit(4, 8),                                  # sqrt3
              _unit(6, 8),                                  # sqrt6 = sqrt2*sqrt3  (IN K)
              [F(3), F(0), F(5), F(0), F(0), F(0), F(0), F(0)]):   # 3 + 5 sqrt2
        d = W.detect(v)
        assert d.field_residual_norm == 0
        assert d.in_field is True
        assert d.extension_flagged is False
        assert all(c == 0 for c in d.field_residual)


# -- out-of-field: flagged, basis unchanged (no growth) --------------------- #
def test_out_of_field_flagged_and_no_growth():
    W = _W()
    before_basis = [list(col) for col in W.subfield_basis]
    before_P = [list(row) for row in W._P_K]
    before_deg = (W.degree, W.subfield_degree)

    for idx, norm in [(1, 56), (3, 112), (5, 168), (7, 336)]:      # sqrt7, sqrt14, sqrt21, sqrt42
        d = W.detect(_unit(idx, 8))
        assert d.in_field is False
        assert d.extension_flagged is True                 # extension WOULD be needed
        assert d.field_residual_norm == norm               # == G_W[idx][idx], exact
        assert d.field_residual == _unit(idx, 8)           # the off-field axis survives the projection

    # DETECTION ONLY -- nothing grew or mutated
    assert [list(col) for col in W.subfield_basis] == before_basis
    assert [list(row) for row in W._P_K] == before_P
    assert (W.degree, W.subfield_degree) == before_deg


# -- a surd already in K is in-field, NOT an extension ---------------------- #
def test_surd_already_in_K_is_in_field_not_extension():
    W = _W()
    d = W.detect(_unit(6, 8))                               # sqrt6 = sqrt2 * sqrt3 in Q(sqrt2,sqrt3)
    assert d.in_field is True and d.extension_flagged is False


# -- a mixed element: the residual isolates exactly the out-of-field part ---- #
def test_mixed_element_residual_isolates_out_of_field_component():
    W = _W()
    v = [F(0), F(5), F(2), F(0), F(0), F(0), F(0), F(0)]    # 2*sqrt2 (in K) + 5*sqrt7 (out)
    d = W.detect(v)
    assert d.in_field is False
    assert d.field_residual == [F(0), F(5), F(0), F(0), F(0), F(0), F(0), F(0)]   # only the sqrt7 axis
    assert d.field_residual_norm == 25 * 56                # 5^2 * G_W[1][1] = 1400


# -- tensor Gram == G_K (x) G_L (Prop 3.3) ---------------------------------- #
def test_tensor_gram_is_kronecker_and_det_relation():
    W = _W()
    assert W.degree == 8 and W.subfield_degree == 4
    assert [W.gram[i][i] for i in range(8)] == [8, 56, 16, 112, 24, 168, 48, 336]
    assert W.gram == tensor_gram(G_K, G_L) == kron(G_K, G_L)
    # det G_W == (det G_K)^[L:Q] * (det G_L)^[K:Q]  (Rem 3.4); G_W diagonal -> det = product
    det_GW = 1
    for i in range(8):
        det_GW *= W.gram[i][i]
    assert det_GW == 9216 ** 2 * 28 ** 4                    # (2^10*3^2)^2 * 28^4


# -- malformed / over-cap raise cleanly ------------------------------------- #
def test_malformed_and_over_cap_raise():
    W = _W()
    with pytest.raises(ValueError):
        W.detect([1, 2, 3])                                # wrong length (W is degree 8)
    with pytest.raises(TypeError):
        W.detect([1.5] * 8)                                # float coordinate (G8)
    with pytest.raises(ValueError):
        WorkingField.from_two_factors(G_K, G_L, degree_cap=4)   # degree 8 > cap 4 -> over-cap
    with pytest.raises(ValueError):
        WorkingField([[1, 0, 0], [0, 1, 0]], [_unit(0, 3)])     # non-square gram
    with pytest.raises(ValueError):
        WorkingField([[1, 0], [0, 1]], [[F(1), F(0)], [F(2), F(0)]])  # rank-deficient sub-field basis


def test_hard_degree_cap_declared_and_enforced():
    assert isinstance(HARD_DEGREE_CAP, int) and HARD_DEGREE_CAP >= 8
    assert _W().degree <= HARD_DEGREE_CAP                   # the demo field is within the cap


# -- exactness (G8) --------------------------------------------------------- #
def test_exact_fraction_core():
    W = _W()
    d = W.detect(_unit(1, 8))
    assert isinstance(d.field_residual_norm, Fraction)
    assert all(isinstance(c, Fraction) for c in d.field_residual)
    assert all(isinstance(v, Fraction) for row in W.gram for v in row)


# -- model-layer only: stdlib + projector; no KIRA, no numpy ---------------- #
def test_model_layer_only_no_kira_no_numpy():
    code = textwrap.dedent(
        """
        import os, sys
        sys.path.insert(0, os.path.dirname(%r))
        import field_extension as fx
        W = fx.WorkingField.from_two_factors([[4,0,0,0],[0,8,0,0],[0,0,12,0],[0,0,0,24]], [[2,0],[0,14]])
        assert W.detect(fx._unit(1, 8)).extension_flagged is True
        assert W.detect(fx._unit(6, 8)).in_field is True
        assert "numpy" not in sys.modules and "loom" not in sys.modules
        assert "kira_server_canonical" not in sys.modules
        assert not any(m.startswith("kira") for m in sys.modules)
        print("CLEAN")
        """ % (fx.__file__,)
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "CLEAN" in out.stdout

    imported = set()
    for node in ast.walk(ast.parse(open(fx.__file__, encoding="utf-8").read())):
        if isinstance(node, ast.Import):
            for n in node.names:
                imported.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module.split(".")[0])
    assert "projector" in imported                          # reuses the L0 projector
    assert "numpy" not in imported
    assert not any(m.startswith("kira") for m in imported)
