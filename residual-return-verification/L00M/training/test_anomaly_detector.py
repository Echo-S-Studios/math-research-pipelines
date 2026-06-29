"""test_anomaly_detector.py -- assert-bearing gate for A7 (streaming anomaly/novelty detector).

The detector wraps ResidualLearner (in-field/off-axis novelty) + CompositumLearner (out-of-field
novelty), emits a calibration-gated anomaly signal, and SURFACES growth proposals through the existing
propose-for-confirm path -- it never grows the model itself.
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

import anomaly_detector as ad
from anomaly_detector import AnomalyDetector, AnomalyScore
from residual_learner import ResidualLearner, SeedProposal, g_orthogonal_integer_vector
from compositum import CompositumLearner, Factor, FieldExtensionProposal
from field_extension import _unit

F = Fraction
PHI4 = [1, 0, -10, 0, 1]                                            # K = Q(sqrt2+sqrt3), power basis
G_K = [[4, 0, 0, 0], [0, 8, 0, 0], [0, 0, 12, 0], [0, 0, 0, 24]]   # Q(sqrt2,sqrt3) product Gram
SQRT7 = Factor("Q(sqrt7)", [[2, 0], [0, 14]], [1, 0, -7])
SQRT7_AXIS = _unit(1, 8)


def _setup(cal_ok=True):
    flag = {"ok": cal_ok}
    learner = ResidualLearner(PHI4, [[1, 0, 0, 0], [0, 1, 0, 0]], persistence_N=3)
    comp = CompositumLearner(G_K, SQRT7)
    det = AnomalyDetector(learner, compositum=comp, calibration_ok=lambda: flag["ok"])
    w = g_orthogonal_integer_vector(learner._cols, learner._G)      # off-axis direction (2*sqrt6)
    return det, learner, comp, flag, w


def _off_axis(w):
    return [F(1) + w[0], F(0) + w[1], F(0) + w[2], F(0) + w[3]]


def _in_dist(a, b):
    return [F(a), F(b), F(0), F(0)]                                 # a*1 + b*theta  in span B


# -- in-distribution stream is quiet ---------------------------------------- #
def test_a7_in_distribution_stream_no_anomaly():
    det, _, _, _, _ = _setup(cal_ok=True)
    for a, b in [(2, 1), (-3, 4), (5, -2), (0, 7)]:
        s = det.observe(_in_dist(a, b))
        assert s.score == 0 and s.novel is False and s.anomaly is False
        assert s.proposal is None
    assert det.stats()["alerts"] == 0


# -- an off-axis anomaly is flagged (calibrated) ---------------------------- #
def test_a7_off_axis_anomaly_flagged():
    det, _, _, _, w = _setup(cal_ok=True)
    s = det.observe(_off_axis(w))
    assert s.kind == "in_field"
    assert s.score == 96 and s.novel is True and s.anomaly is True   # exact off-axis residual norm


# -- an out-of-field anomaly is flagged + surfaces a FieldExtensionProposal -- #
def test_a7_out_of_field_anomaly_flagged():
    det, _, _, _, _ = _setup(cal_ok=True)
    s = det.observe(SQRT7_AXIS, space="out_of_field")
    assert s.kind == "out_of_field"
    assert s.score == 56 and s.novel is True and s.anomaly is True
    assert isinstance(s.proposal, FieldExtensionProposal)
    assert (s.proposal.old_degree, s.proposal.new_degree) == (4, 8)


# -- the calibration gate suppresses alerts (and proposals) until calibrated - #
def test_a7_calibration_gate_suppresses_until_calibrated():
    det, _, _, flag, w = _setup(cal_ok=False)
    for _ in range(3):                                              # OFF: novelty scored, alert suppressed
        s = det.observe(_off_axis(w))
        assert s.novel is True and s.anomaly is False and s.proposal is None
    assert det.stats()["alerts"] == 0
    flag["ok"] = True                                              # ON: now it alerts + surfaces a proposal
    s = det.observe(_off_axis(w))
    assert s.anomaly is True and isinstance(s.proposal, SeedProposal)


# -- the detector PROPOSES; it never auto-acts (no growth) ------------------ #
def test_a7_proposes_but_never_auto_grows():
    det, learner, comp, _, w = _setup(cal_ok=True)
    n0 = learner.state()["num_seeds"]
    s = None
    for _ in range(3):
        s = det.observe(_off_axis(w))
    assert isinstance(s.proposal, SeedProposal)
    assert learner.state()["num_seeds"] == n0                      # detector did NOT grow the basis
    # the surfaced proposal is real: the CALLER (not the detector) confirms -> growth happens then
    learner.confirm(s.proposal)
    assert learner.state()["num_seeds"] == n0 + 1

    # out-of-field: same -- proposes, never auto-grows
    s7 = det.observe(SQRT7_AXIS, space="out_of_field")
    assert isinstance(s7.proposal, FieldExtensionProposal)
    assert comp.degree == 4                                         # detector did NOT extend the field
    comp.confirm(s7.proposal)
    assert comp.degree == 8


# -- surfaced proposals are witnessed (G5), tamper-evident ------------------ #
def test_a7_witness_of_surfaced_proposals():
    det, _, _, _, w = _setup(cal_ok=True)
    for _ in range(3):
        det.observe(_off_axis(w))
    det.observe(SQRT7_AXIS, space="out_of_field")
    assert det.stats()["proposals"] >= 1
    assert det.verify_witness() is True
    det._witness[0]["score"] = "999"                               # tamper
    assert det.verify_witness() is False


# -- exact (G8): scores are Fraction; a float observation is rejected -------- #
def test_a7_exact_scores_floats_rejected():
    det, _, _, _, w = _setup(cal_ok=True)
    s = det.observe(_off_axis(w))
    assert isinstance(s.score, Fraction)
    with pytest.raises(TypeError):
        det.observe([1.5, 0, 0, 0])                                # float -> rejected by the exact core


# -- model-layer only: stdlib + the learner/detection stack; no KIRA, no numpy #
def test_a7_model_layer_only_no_kira_no_numpy():
    code = textwrap.dedent(
        """
        import os, sys
        sys.path.insert(0, os.path.dirname(%r))
        from fractions import Fraction as F
        import anomaly_detector as ad
        from residual_learner import ResidualLearner
        from compositum import CompositumLearner, Factor
        from field_extension import _unit
        det = ad.AnomalyDetector(ResidualLearner([1,0,-10,0,1], [[1,0,0,0],[0,1,0,0]], persistence_N=3),
                                 compositum=CompositumLearner([[4,0,0,0],[0,8,0,0],[0,0,12,0],[0,0,0,24]],
                                                              Factor("Q(sqrt7)", [[2,0],[0,14]], [1,0,-7])))
        assert det.observe([F(2), F(1), F(0), F(0)]).anomaly is False
        assert det.observe(_unit(1, 8), space="out_of_field").anomaly is True
        assert "numpy" not in sys.modules and "kira_server_canonical" not in sys.modules
        assert not any(m.startswith("kira") for m in sys.modules)
        print("CLEAN")
        """ % (ad.__file__,)
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "CLEAN" in out.stdout

    imported = set()
    for node in ast.walk(ast.parse(open(ad.__file__, encoding="utf-8").read())):
        if isinstance(node, ast.Import):
            for n in node.names:
                imported.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module.split(".")[0])
    assert {"residual_learner", "compositum"} <= imported          # wraps the existing learner + detection
    assert "numpy" not in imported
    assert not any(m.startswith("kira") for m in imported)
