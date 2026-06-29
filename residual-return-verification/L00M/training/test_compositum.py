"""test_compositum.py -- assert-bearing gate for A2.P2b (disjoint-compositum GROWTH).

The sqrt7 scenario: over K = Q(sqrt2,sqrt3), a persistent sqrt7 (out-of-field) is detected, an
extension is proposed (degree 4->8, disjoint), and confirm() grows K into W = Q(sqrt2,sqrt3,sqrt7)
with the Kronecker Gram G_W = G_K (x) G_L; the sqrt7 residual -> 0, witnessed. Non-disjoint (sqrt6,
already in K) and over-cap candidates are refused with no growth.
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

import compositum as cm
from compositum import CompositumLearner, Factor, FieldExtensionProposal, FieldExtensionRefusal
from field_extension import kron, _unit, HARD_DEGREE_CAP

F = Fraction
G_K = [[4, 0, 0, 0], [0, 8, 0, 0], [0, 0, 12, 0], [0, 0, 0, 24]]    # K = Q(sqrt2,sqrt3), det 9216
G_L = [[2, 0], [0, 14]]                                             # L = Q(sqrt7), det 28
SQRT7 = Factor("Q(sqrt7)", G_L, [1, 0, -7])                         # generator minpoly x^2 - 7

SQRT7_AXIS = _unit(1, 8)     # 1 (x) sqrt7   -- out of K
SQRT6_AXIS = _unit(6, 8)     # sqrt2 (x) sqrt3 = sqrt6 -- already IN K


def _L():
    return CompositumLearner(G_K, SQRT7)


# -- the sqrt7 scenario: detect -> propose -> confirm -> grow -> residual 0 -- #
def test_p2b_sqrt7_detect_propose_confirm_grows_and_zeros_residual():
    L = _L()
    # detect flags out-of-field
    det = L.detect(SQRT7_AXIS)
    assert det.in_field is False and det.extension_flagged is True
    assert det.field_residual_norm == 56                  # G_W[1][1]

    # propose a disjoint extension (no growth yet)
    p = L.propose(SQRT7_AXIS)
    assert isinstance(p, FieldExtensionProposal)
    assert (p.old_degree, p.new_degree, p.disjoint) == (4, 8, True)
    assert p.generator_min_poly == [1, 0, -7]
    assert L.degree == 4                                   # propose did NOT grow (G2)

    # confirm grows K -> W = Q(sqrt2,sqrt3,sqrt7)
    rec = L.confirm(p)
    assert L.degree == 8
    assert L.working_gram == kron(G_K, G_L)               # G_W = G_K (x) G_L (Prop 3.3)
    assert [L.working_gram[i][i] for i in range(8)] == [8, 56, 16, 112, 24, 168, 48, 336]
    assert L.detect(SQRT7_AXIS).field_residual_norm == 0  # the novel element is now captured

    # witnessed (G5)
    assert rec["event"] == "field_extension"
    assert (rec["old_degree"], rec["new_degree"]) == (4, 8)
    assert rec["generator_min_poly"] == [1, 0, -7]
    assert rec["prev_hash"] == "genesis" and len(rec["hash"]) == 16
    assert L.verify_witness() is True


def test_p2b_witness_tamper_evident():
    L = _L()
    L.confirm(L.propose(SQRT7_AXIS))
    assert L.verify_witness() is True
    L._witness[0]["new_degree"] = 999                      # tamper
    assert L.verify_witness() is False


# -- propose is pure; confirm is the sole mutator (G2) ---------------------- #
def test_p2b_confirm_is_the_only_mutator():
    L = _L()
    p = L.propose(SQRT7_AXIS)
    for _ in range(3):
        L.detect(SQRT7_AXIS)
        L.propose(SQRT7_AXIS)                             # pure -- must not grow
    assert L.degree == 4
    L.confirm(p)
    assert L.degree == 8                                   # only confirm grew
    # single-step growth: propose now refuses, and re-confirming the old proposal raises
    assert isinstance(L.propose(SQRT7_AXIS), FieldExtensionRefusal)
    with pytest.raises(ValueError):
        L.confirm(p)                                       # already extended


# -- non-disjoint (sqrt6 already in K) is refused, no growth ----------------- #
def test_p2b_non_disjoint_already_in_K_refused_no_growth():
    L = _L()
    r = L.propose(SQRT6_AXIS)                              # sqrt6 = sqrt2*sqrt3 in K
    assert isinstance(r, FieldExtensionRefusal)
    assert r.kind == "non_disjoint"
    assert "deferred to P2c" in r.reason
    assert L.degree == 4                                   # NO growth


# -- over-cap extension refused (nothing blows up) -------------------------- #
def test_p2b_over_cap_extension_refused():
    with pytest.raises(ValueError):
        CompositumLearner(G_K, SQRT7, degree_cap=4)        # would-be degree 8 > cap 4


# -- a mixed element: out-of-field before confirm, captured after ----------- #
def test_p2b_mixed_element_residual_zero_after_growth():
    L = _L()
    v = [F(0), F(5), F(2), F(0), F(0), F(0), F(0), F(0)]   # 2*sqrt2 (in K) + 5*sqrt7 (out)
    assert L.detect(v).field_residual_norm == 25 * 56      # 1400 before growth
    L.confirm(L.propose(SQRT7_AXIS))
    assert L.detect(v).field_residual_norm == 0            # fully captured after the extension


# -- G10: generator must be a monic-integer algebraic integer --------------- #
def test_p2b_g10_monic_integer_generator():
    with pytest.raises(ValueError):
        CompositumLearner(G_K, Factor("bad", G_L, [2, 0, -7]))          # non-monic
    with pytest.raises(ValueError):
        CompositumLearner(G_K, Factor("bad", G_L, [1, F(1, 2), -7]))    # non-integer (G10)


# -- exactness (G8) + Kronecker det relation -------------------------------- #
def test_p2b_exact_and_det_relation():
    L = _L()
    assert all(isinstance(v, Fraction) for row in L.working_gram for v in row)
    assert L.detect(SQRT7_AXIS).field_residual_norm == Fraction(56)
    det = 1
    for i in range(8):
        det *= L.working_gram[i][i]
    assert det == 9216 ** 2 * 28 ** 4                     # det G_W = (det G_K)^[L:Q] (det G_L)^[K:Q]


# -- model-layer only: stdlib + projector/field_extension; no KIRA, no numpy - #
def test_p2b_model_layer_only_no_kira_no_numpy():
    code = textwrap.dedent(
        """
        import os, sys
        sys.path.insert(0, os.path.dirname(%r))
        import compositum as cm
        from field_extension import _unit
        L = cm.CompositumLearner([[4,0,0,0],[0,8,0,0],[0,0,12,0],[0,0,0,24]],
                                  cm.Factor("Q(sqrt7)", [[2,0],[0,14]], [1,0,-7]))
        L.confirm(L.propose(_unit(1, 8)))
        assert L.degree == 8 and L.detect(_unit(1, 8)).field_residual_norm == 0
        assert "numpy" not in sys.modules and "loom" not in sys.modules
        assert "kira_server_canonical" not in sys.modules
        assert not any(m.startswith("kira") for m in sys.modules)
        print("CLEAN")
        """ % (cm.__file__,)
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "CLEAN" in out.stdout

    imported = set()
    for node in ast.walk(ast.parse(open(cm.__file__, encoding="utf-8").read())):
        if isinstance(node, ast.Import):
            for n in node.names:
                imported.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module.split(".")[0])
    assert {"field_extension", "integral_basis"} <= imported   # reuses P2a detection + the G10 guard
    assert "numpy" not in imported
    assert not any(m.startswith("kira") for m in imported)
