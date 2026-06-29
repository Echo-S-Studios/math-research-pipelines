"""test_field_growing_learner.py -- the learner-wiring increment: a non-disjoint OUT-OF-FIELD residual
driven to 0 THROUGH the learner (not just inside compositum.py).

FieldGrowingLearner owns an in-field ResidualLearner + cross-field growth; on a confirmed non-disjoint
extension it builds a FRESH ResidualLearner on the true compositum Q(theta) and re-homes the forced basis.
ResidualLearner is UNCHANGED (asserted: same module, no mutation of its fixed-ambient invariant).

ADDITIVE: imports only model-layer modules; existing ResidualLearner / AnomalyDetector / compositum /
capacity tests are untouched.
"""
import ast
import subprocess
import sys
from fractions import Fraction as F
import pytest

import field_growing_learner as fgl_mod
from field_growing_learner import FieldGrowingLearner, FieldGrowthPlan, FieldGrowthRefusal
from capacity import Budget

K_SQRT2 = [1, 0, -2]            # K = Q(sqrt2), degree 2
M_BETA = [1, 0, -10, 0, 1]     # beta = sqrt2 + sqrt3, m_beta over Q (factors over K: e' = 2)
M_THETA = [1, 0, -22, 0, 25]   # compositum primitive theta = 2sqrt2 + sqrt3


def _fresh(seeds=([1, 0],), **kw):
    return FieldGrowingLearner(K_SQRT2, [list(s) for s in seeds], **kw)


# ===== (1) the END-TO-END: out-of-field residual -> 0 through the learner ===================== #
def test_e2e_out_of_field_residual_driven_to_zero_through_learner():
    fgl = _fresh()                                       # K = Q(sqrt2), forced basis {1}
    assert fgl.degree == 2 and fgl.one_in_basis()
    # in-field capture still works on the in-field tier (3 = 3*1 is captured)
    assert fgl.residual_norm([3, 0]) == 0
    # beta = sqrt2+sqrt3 is OUT of K: its image is not in Q(sqrt2) -> propose a field extension
    plan = fgl.propose_extension(M_BETA, gain=F(1, 2))
    assert isinstance(plan, FieldGrowthPlan)
    assert plan.e_prime == 2 and plan.new_degree == 4    # TRUE compositum degree 4, NOT the tensor 8
    assert plan.m_theta == M_THETA and plan.verdict.decision == "GROW"
    assert fgl.degree == 2                               # propose did NOT grow (pure)
    rec = fgl.confirm_extension(plan)
    assert fgl.degree == 4                               # grown onto Q(sqrt2,sqrt3)
    # THE POINT: the previously out-of-field beta now has residual EXACTLY 0 through the (fresh) learner
    assert fgl.residual_norm(plan._res.beta_coords) == 0
    # the basis grew correctly: K's old column(s) + beta, all captured
    assert fgl.residual_norm([1, 0, 0, 0]) == 0          # the constant, re-homed
    # witness records old->new degree, e', m_theta and verifies
    assert rec["old_degree"] == 2 and rec["new_degree"] == 4 and rec["e_prime"] == 2
    assert rec["m_theta"] == M_THETA and rec["generator_min_poly"] == M_BETA
    assert fgl.verify_witness()


# ===== (2) effective_degree wiring: the gate judges the TRUE compositum degree =============== #
def test_effective_degree_is_true_compositum_degree():
    fgl = _fresh()
    plan = fgl.propose_extension(M_BETA, gain=F(1, 2))
    # capacity_decision was consulted with effective_degree = m*e' = 4 (not the tensor 8)
    assert plan.verdict.degree == 4
    # a budget that admits degree 4 GROWs (the disjoint tensor degree 8 would have been rejected by it)
    assert FieldGrowingLearner(K_SQRT2, [[1, 0]], budget=Budget(degree_max=4, height_max=256)) \
        .propose_extension(M_BETA, gain=F(1, 2)).verdict.decision == "GROW"
    # a budget below the compositum degree REJECTs (capacity gate, via effective_degree)
    r = FieldGrowingLearner(K_SQRT2, [[1, 0]], budget=Budget(degree_max=3, height_max=256)) \
        .propose_extension(M_BETA, gain=F(1, 2))
    assert isinstance(r, FieldGrowthRefusal) and r.kind == "capacity_reject"


def test_info_threshold_stays_off():
    # this increment wires effective_degree admissibility ONLY; the degree-aware Lehmer threshold is NOT
    # turned on (default floor=0). A tiny positive gain still GROWs (no nonzero floor is applied here).
    fgl = _fresh()
    plan = fgl.propose_extension(M_BETA, gain=F(1, 1000))
    assert plan.verdict.decision == "GROW"
    # the verdict reason is the plain admissibility path, not the info-threshold tag
    assert "info_threshold" not in plan.verdict.reason


# ===== (3) 1 in B preserved across the field change (LOAD-BEARING) =========================== #
def test_one_in_basis_preserved_across_growth():
    fgl = _fresh(seeds=[[1, 0]])                          # constant 1 is in B
    assert fgl.one_in_basis()
    fgl.confirm_extension(fgl.propose_extension(M_BETA, gain=F(1, 2)))
    assert fgl.one_in_basis()                             # still 1 in B in Q(theta) -- the re-home kept it
    # and it is the literal constant column [1,0,0,0]
    assert fgl.residual_norm([1, 0, 0, 0]) == 0


def test_rehome_preserves_subspace_with_a_nontrivial_basis():
    # B = {1, sqrt2}: sqrt2 re-homes to FRACTIONAL theta-coords; denominator-clearing keeps the SAME line,
    # so the captured subspace (and 1 in B) is preserved and sqrt2 stays captured.
    fgl = _fresh(seeds=[[1, 0], [0, 1]])                  # {1, sqrt2} in Q(sqrt2)
    fgl.confirm_extension(fgl.propose_extension(M_BETA, gain=F(1, 2)))
    assert fgl.degree == 4 and fgl.one_in_basis()
    from coords_to_minpoly import regular_representation  # re-express sqrt2 into Q(theta) to check capture
    from field_growing_learner import _embed_into_theta
    M_alpha = regular_representation(
        [F(0), F(27, 20), F(0), F(-1, 20)], M_THETA)      # alpha = sqrt2 image (independently known)
    sqrt2_in_theta = _embed_into_theta([F(0), F(1)], M_alpha, 4)
    assert fgl.residual_norm(sqrt2_in_theta) == 0         # sqrt2 still captured after the re-home


# ===== (4) field-growth witness is tamper-evident =========================================== #
def test_field_growth_witness_tamper_evident():
    fgl = _fresh()
    fgl.confirm_extension(fgl.propose_extension(M_BETA, gain=F(1, 2)))
    assert fgl.verify_witness()
    fgl._witness[0]["new_degree"] = 8                     # tamper: pretend it was the tensor degree
    assert not fgl.verify_witness()


# ===== (5) the negatives stay coherent at this level ======================================== #
def test_already_in_K_refused():
    fgl = _fresh()
    r = fgl.propose_extension(K_SQRT2, gain=F(1, 2))      # adjoin sqrt2 to Q(sqrt2): e' = 1
    assert isinstance(r, FieldGrowthRefusal) and r.kind == "already_in_k"
    assert fgl.degree == 2                                # no growth


def test_factor_unsupported_refused():
    # K = Q(sqrt2,sqrt3) [m=4], beta = sqrt5+sqrt7 [deg 4] -> m_theta degree 16 > Kronecker bound 12
    K = [1, 0, -10, 0, 1]
    fgl = FieldGrowingLearner(K, [[1, 0, 0, 0]], budget=Budget(degree_max=20, height_max=256))
    r = fgl.propose_extension([1, 0, -24, 0, 4], gain=F(1, 2))
    assert isinstance(r, FieldGrowthRefusal) and r.kind == "factor_unsupported"
    assert "Zassenhaus" in r.reason


def test_confirm_extension_is_sole_field_mutator():
    fgl = _fresh()
    plan = fgl.propose_extension(M_BETA, gain=F(1, 2))
    fgl.propose_extension(M_BETA, gain=F(1, 2))           # pure: still degree 2
    assert fgl.degree == 2
    fgl.confirm_extension(plan)
    assert fgl.degree == 4
    with pytest.raises(TypeError):
        fgl.confirm_extension(plan.m_theta)               # only a FieldGrowthPlan acts


# ===== (6) exact (G8) + model-layer purity ================================================== #
def test_g8_exact_only():
    fgl = _fresh()
    with pytest.raises(TypeError):
        fgl.propose_extension(M_BETA, gain=0.5)           # float gain rejected
    plan = fgl.propose_extension(M_BETA, gain=F(1, 2))
    rec = fgl.confirm_extension(plan)
    assert all(isinstance(c, int) for c in rec["m_theta"])    # monic-integer (G10)


def test_model_layer_no_kira_no_numpy_static():
    # the wiring module imports no numpy / sympy / kira (static AST check; the in-field tier may pull
    # heavier deps transitively, so the clean-room guarantee is asserted on THIS module's imports)
    imported = set()
    for node in ast.walk(ast.parse(open(fgl_mod.__file__, encoding="utf-8").read())):
        if isinstance(node, ast.Import):
            imported |= {n.name.split(".")[0] for n in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert "numpy" not in imported and "sympy" not in imported
    assert not any(m.startswith("kira") for m in imported)


def test_model_layer_clean_subprocess():
    code = (
        "import os, sys\n"
        "sys.path.insert(0, os.path.dirname(%r))\n"
        "from field_growing_learner import FieldGrowingLearner\n"
        "from fractions import Fraction as F\n"
        "fgl = FieldGrowingLearner([1,0,-2], [[1,0]])\n"
        "fgl.confirm_extension(fgl.propose_extension([1,0,-10,0,1], gain=F(1,2)))\n"
        "assert fgl.degree == 4 and fgl.one_in_basis() and fgl.verify_witness()\n"
        "assert not any(m.startswith('kira') for m in sys.modules)\n"
        "print('CLEAN')\n"
    ) % (fgl_mod.__file__,)
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "CLEAN" in out.stdout


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
