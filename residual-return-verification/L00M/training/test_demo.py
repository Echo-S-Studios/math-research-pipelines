"""test_demo.py -- assert-bearing gate for the A1+A2+A7 end-to-end demo.

Runs demo.run() and asserts the end-state invariants of all three acts hold: in-field growth captures
the off-axis residual to 0 with the exact minpoly; the cross-field extension captures sqrt7 to 0; the
anomaly detector's calibration gate suppresses then surfaces, and the detector never grows the model.
Every witness chain verifies.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from demo import run


def test_demo_runs_and_end_state_invariants_hold():
    r = run(verbose=False)

    # ACT 1 -- in-field: grew with the EXACT minpoly, off-axis residual -> 0, witnessed
    assert r["in_field"]["minpoly"] == [1, 0, -24]          # x^2 - 24 = minpoly(2 sqrt6)
    assert r["in_field"]["num_seeds"] == 3                  # basis grew 2 -> 3
    assert r["in_field"]["final_residual_norm"] == 0        # the novel direction is now captured
    assert r["in_field"]["witness_ok"] is True

    # ACT 2 -- out-of-field: extended 4 -> 8, sqrt7 residual -> 0, witnessed
    assert (r["out_of_field"]["old_degree"], r["out_of_field"]["new_degree"]) == (4, 8)
    assert r["out_of_field"]["final_residual_norm"] == 0    # sqrt7 captured by Q(sqrt2,sqrt3,sqrt7)
    assert r["out_of_field"]["witness_ok"] is True

    # ACT 3 -- anomaly detector: calibration gate + propose-only
    assert r["anomaly"]["in_distribution_alert"] is False   # quiet on in-distribution
    assert r["anomaly"]["any_alert_when_off"] is False      # suppressed while uncalibrated
    assert r["anomaly"]["alert_when_on"] is True            # alerts once calibrated
    assert r["anomaly"]["proposal_surfaced"] is True        # surfaces a growth proposal
    assert r["anomaly"]["detector_grew"] is False           # but NEVER auto-grows the model
    assert r["anomaly"]["witness_ok"] is True

    # ACT 4 -- the capacity gate REJECTS an over-budget candidate (principled finite bound)
    assert r["capacity_reject"]["verdict"] == "REJECT"      # derived Northcott decision, not a tuned cap
    assert r["capacity_reject"]["proposal_is_none"] is True  # propose() returns None
    assert r["capacity_reject"]["did_not_grow"] is True      # the learner did not grow
    assert r["capacity_reject"]["coeff_height"] == 24        # 2sqrt6 height 24 > budget height 10
