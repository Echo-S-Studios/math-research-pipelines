"""test_detector_driven_gain.py -- the detector-driven-gain seam: the field-extension `gain` comes from
the detector's ACTUAL measured out-of-field residual, not a caller-supplied value.

The seam is closed when a FieldGrowingLearner extension proposal surfaced by the AnomalyDetector carries a
`gain` EQUAL to the measured out-of-field residual norm. AnomalyDetector stays propose-only (G2: only
confirm_extension grows the field); calibration gating is preserved; the explicit-gain override and the
info-threshold-off default are unchanged.

ADDITIVE: residual_learner.py and capacity.py are untouched; field_growing_learner.py and
anomaly_detector.py changed additively (existing behaviour byte-identical).
"""
from fractions import Fraction as F
import pytest

from residual_learner import ResidualLearner
from field_growing_learner import FieldGrowingLearner, FieldGrowthPlan, FieldGrowthRefusal
from anomaly_detector import AnomalyDetector

K_SQRT2 = [1, 0, -2]            # K = Q(sqrt2)
M_BETA = [1, 0, -10, 0, 1]     # beta = sqrt2 + sqrt3 (factors over K: e' = 2)
# beta = sqrt2 + sqrt3 against K=Q(sqrt2): residual = sqrt3, ||sqrt3||^2_{G_theta} = Tr(3) = 3*4 = 12
EXPECTED_GAIN = F(12)


def _detector(calibrated=True):
    cal = {"ok": calibrated}
    learner = ResidualLearner(K_SQRT2, [[1, 0]])
    fgl = FieldGrowingLearner(K_SQRT2, [[1, 0]])
    det = AnomalyDetector(learner, field_growing_learner=fgl,
                          extension_generator=M_BETA, calibration_ok=lambda: cal["ok"])
    return det, fgl, cal


# ===== (1) THE SEAM: detector-measured residual IS the growth gain (no caller gain) ========== #
def test_seam_detector_residual_is_the_growth_gain():
    det, fgl, _ = _detector()
    sc = det.propose_field_growth()                          # NO caller-supplied gain
    # the detector measured the exact out-of-field residual...
    assert sc.kind == "out_of_field" and sc.score == EXPECTED_GAIN and isinstance(sc.score, F)
    # ...and surfaced a FieldGrowingLearner proposal whose gain EQUALS it (the seam is closed)
    assert isinstance(sc.proposal, FieldGrowthPlan)
    assert sc.proposal.gain == sc.score == EXPECTED_GAIN
    # the gate judged the TRUE compositum degree, and it admitted
    assert sc.proposal.new_degree == 4 and sc.proposal.verdict.decision == "GROW"
    assert sc.proposal.verdict.degree == 4


def test_seam_end_to_end_residual_to_zero_through_learner():
    det, fgl, _ = _detector()
    plan = det.propose_field_growth().proposal               # auto-gain proposal
    assert fgl.degree == 2                                    # propose-only: detector did NOT grow
    rec = fgl.confirm_extension(plan)                         # the SOLE field-growth mutator
    assert fgl.degree == 4                                    # grown to Q(sqrt2,sqrt3)
    assert fgl.residual_norm(plan._res.beta_coords) == 0      # out-of-field beta now captured (residual 0)
    assert fgl.one_in_basis()                                 # 1 in B preserved
    assert rec["e_prime"] == 2 and fgl.verify_witness()
    assert det.verify_witness()                               # the detector's surfaced-proposal log verifies


# ===== (2) calibration gating preserved =================================================== #
def test_calibration_gated_suppression():
    det, fgl, cal = _detector(calibrated=False)
    sc = det.propose_field_growth()
    assert sc.score == EXPECTED_GAIN                          # the residual is still MEASURED (recorded)
    assert sc.proposal is None and sc.anomaly is False        # but NO proposal surfaced (uncalibrated)
    assert det.n_out_of_field == 1 and det.n_proposals == 0
    cal["ok"] = True                                          # once calibrated, the proposal surfaces
    assert isinstance(det.propose_field_growth().proposal, FieldGrowthPlan)


def test_detector_stays_propose_only():
    det, fgl, _ = _detector()
    det.propose_field_growth()
    det.propose_field_growth()
    assert fgl.degree == 2                                    # never auto-grows; confirm is required


# ===== (3) auto-gain default + explicit override (back-compat) ============================= #
def test_auto_gain_equals_measured_residual():
    fgl = FieldGrowingLearner(K_SQRT2, [[1, 0]])
    measured = fgl.out_of_field_residual_norm(M_BETA)
    assert measured == EXPECTED_GAIN
    plan = fgl.propose_extension(M_BETA)                      # gain=None -> AUTO
    assert plan.gain == measured                             # auto-gain == the measured residual


def test_explicit_gain_override_unchanged():
    fgl = FieldGrowingLearner(K_SQRT2, [[1, 0]])
    plan = fgl.propose_extension(M_BETA, gain=F(1, 2))        # explicit override
    assert plan.gain == F(1, 2) and plan.verdict.decision == "GROW"
    with pytest.raises(TypeError):
        fgl.propose_extension(M_BETA, gain=0.5)               # float gain rejected (G8)


# ===== (4) info-threshold stays OFF on the auto-gain path ================================== #
def test_info_threshold_stays_off_on_auto_path():
    fgl = FieldGrowingLearner(K_SQRT2, [[1, 0]])
    plan = fgl.propose_extension(M_BETA)                      # auto-gain, default floor=0
    assert "info_threshold" not in plan.verdict.reason


# ===== (5) the auto-gain is EXACT (G8) ===================================================== #
def test_auto_gain_is_exact_fraction():
    fgl = FieldGrowingLearner(K_SQRT2, [[1, 0]])
    g = fgl.out_of_field_residual_norm(M_BETA)
    assert isinstance(g, F) and g.denominator == 1 and g == 12
    # a different out-of-field element (2*beta) scales the residual exactly (4x): ||2 sqrt3||^2 = 4*12 = 48
    from compositum_nondisjoint import build_compositum
    res = build_compositum(K_SQRT2, M_BETA)
    two_beta = [2 * c for c in res.beta_coords]
    assert fgl.out_of_field_residual_norm(M_BETA, element_coords=two_beta) == 48


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
