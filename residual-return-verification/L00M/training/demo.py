"""demo.py -- A1 + A2 + A7 end-to-end showcase of the lightweight local learner.

Runnable, pure stdlib, exact, model-layer. `run()` walks the WHOLE story with printed steps and
returns the end-state invariants (final residuals 0, witness chains verify, the detector never grew)
for the assert-bearing test. Run it directly:  py training/demo.py

  ACT 1  in-field: capture (r=0) -> persistent off-axis -> propose EXACT minpoly -> confirm -> grow -> r=0
  ACT 2  out-of-field: detect sqrt7 -> propose field extension -> confirm -> compositum Q(sqrt2,sqrt3,sqrt7) -> r=0
  ACT 3  anomaly detector on a stream: the calibration gate suppresses, then surfaces, a novelty proposal
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from residual_learner import ResidualLearner, g_orthogonal_integer_vector
from compositum import CompositumLearner, Factor
from anomaly_detector import AnomalyDetector
from field_extension import _unit

F = Fraction
PHI4 = [1, 0, -10, 0, 1]                                            # K = Q(sqrt2+sqrt3), power basis
G_K = [[4, 0, 0, 0], [0, 8, 0, 0], [0, 0, 12, 0], [0, 0, 0, 24]]   # Q(sqrt2,sqrt3) product Gram
SQRT7 = ("Q(sqrt7)", [[2, 0], [0, 14]], [1, 0, -7])


def _say(verbose, *a):
    if verbose:
        print(*a)


def run(verbose: bool = True) -> dict:
    result: dict = {}

    # ---- ACT 1 -- in-field: capture, off-axis novelty, grow the basis ------ #
    _say(verbose, "=" * 72)
    _say(verbose, "ACT 1 -- in-field: capture (r=0), persistent off-axis, propose minpoly, grow")
    learner = ResidualLearner(PHI4, [[1, 0, 0, 0], [0, 1, 0, 0]], persistence_N=3)
    w = g_orthogonal_integer_vector(learner._cols, learner._G)      # off-axis direction (2*sqrt6)
    learner.observe([F(2), F(1), F(0), F(0)])                       # in span B
    _say(verbose, f"  in-span obs        -> residual_norm = {learner.state()['last_residual_norm']}  (captured)")
    proposal = None
    for k in range(1, 4):
        learner.observe([F(1) + w[0], F(0) + w[1], F(0) + w[2], F(0) + w[3]])
        proposal = learner.propose()
        tag = ("SEED " + str(proposal.min_poly)) if proposal else "None"
        _say(verbose, f"  off-axis tick {k}    -> residual_norm = {learner.state()['last_residual_norm']}, "
                      f"streak = {learner.state()['streak']}, propose = {tag}")
    learner.confirm(proposal)
    learner.observe([F(1) + w[0], F(0) + w[1], F(0) + w[2], F(0) + w[3]])
    final1 = learner.state()["last_residual_norm"]
    _say(verbose, f"  confirm            -> basis grew to {learner.state()['num_seeds']} seeds; "
                  f"off-axis residual now {final1}; witness_ok = {learner.verify_witness()}")
    result["in_field"] = {
        "minpoly": proposal.min_poly, "num_seeds": learner.state()["num_seeds"],
        "final_residual_norm": final1, "witness_ok": learner.verify_witness(),
    }

    # ---- ACT 2 -- out-of-field: detect sqrt7, extend to the compositum ----- #
    _say(verbose, "=" * 72)
    _say(verbose, "ACT 2 -- out-of-field: detect sqrt7, propose extension, grow to the compositum")
    comp = CompositumLearner(G_K, Factor(*SQRT7))
    sqrt7 = _unit(1, 8)
    _say(verbose, f"  detect(sqrt7)      -> field_residual_norm = {comp.detect(sqrt7).field_residual_norm}  (out-of-field)")
    p2 = comp.propose(sqrt7)
    _say(verbose, f"  propose            -> FieldExtensionProposal {p2.old_degree}->{p2.new_degree}, "
                  f"disjoint = {p2.disjoint}, generator = {p2.generator_min_poly}")
    comp.confirm(p2)
    final2 = comp.detect(sqrt7).field_residual_norm
    _say(verbose, f"  confirm            -> compositum degree {comp.degree} = Q(sqrt2,sqrt3,sqrt7); "
                  f"sqrt7 residual now {final2}; witness_ok = {comp.verify_witness()}")
    result["out_of_field"] = {
        "old_degree": p2.old_degree, "new_degree": comp.degree,
        "final_residual_norm": final2, "witness_ok": comp.verify_witness(),
    }

    # ---- ACT 3 -- anomaly detector: calibration gate suppress -> surface --- #
    _say(verbose, "=" * 72)
    _say(verbose, "ACT 3 -- anomaly detector on a stream (calibration gate suppress -> surface)")
    cal = {"ok": False}
    learner2 = ResidualLearner(PHI4, [[1, 0, 0, 0], [0, 1, 0, 0]], persistence_N=3)
    comp2 = CompositumLearner(G_K, Factor(*SQRT7))
    det = AnomalyDetector(learner2, compositum=comp2, calibration_ok=lambda: cal["ok"])
    w2 = g_orthogonal_integer_vector(learner2._cols, learner2._G)
    quiet = det.observe([F(3), F(-2), F(0), F(0)])                  # in-distribution
    _say(verbose, f"  in-distribution    -> anomaly = {quiet.anomaly}  (quiet)")
    suppressed = []
    for _ in range(3):                                              # calibration OFF -> suppressed
        suppressed.append(det.observe([F(1) + w2[0], F(0) + w2[1], F(0) + w2[2], F(0) + w2[3]]).anomaly)
    _say(verbose, f"  off-axis x3 (cal OFF) -> anomaly = {suppressed}  (alerts suppressed)")
    cal["ok"] = True
    s_on = det.observe([F(1) + w2[0], F(0) + w2[1], F(0) + w2[2], F(0) + w2[3]])
    _say(verbose, f"  off-axis (cal ON)  -> anomaly = {s_on.anomaly}, proposal surfaced = {s_on.proposal is not None}; "
                  f"detector did NOT grow (learner still {learner2.state()['num_seeds']} seeds)")
    result["anomaly"] = {
        "in_distribution_alert": quiet.anomaly,
        "any_alert_when_off": any(suppressed),
        "alert_when_on": s_on.anomaly,
        "proposal_surfaced": s_on.proposal is not None,
        "detector_grew": learner2.state()["num_seeds"] != 2,
        "witness_ok": det.verify_witness(),
    }
    # ---- ACT 4 -- the capacity gate: an over-budget candidate is REJECTED -- #
    _say(verbose, "=" * 72)
    _say(verbose, "ACT 4 -- capacity gate: an over-budget candidate -> REJECT (derived Northcott bound, not a tuned cap)")
    from capacity import Budget
    learner3 = ResidualLearner(PHI4, [[1, 0, 0, 0], [0, 1, 0, 0]], persistence_N=3,
                               budget=Budget(degree_max=64, height_max=10))   # 2sqrt6 coeff_height 24 > 10
    w3 = g_orthogonal_integer_vector(learner3._cols, learner3._G)
    rejected = None
    for _ in range(3):
        learner3.observe([F(1) + w3[0], F(0) + w3[1], F(0) + w3[2], F(0) + w3[3]])
        rejected = learner3.propose()
    v = learner3._last_verdict
    _say(verbose, f"  persistent off-axis: seed coeff_height {v.coeff_height} > budget height 10 -> "
                  f"capacity_decision = {v.decision}; propose() = {rejected}; learner did NOT grow "
                  f"(still {learner3.state()['num_seeds']} seeds)")
    result["capacity_reject"] = {
        "verdict": v.decision,
        "proposal_is_none": rejected is None,
        "did_not_grow": learner3.state()["num_seeds"] == 2,
        "coeff_height": v.coeff_height,
    }

    _say(verbose, "=" * 72)
    _say(verbose, "DONE -- capture, grow in-field, extend cross-field, detect anomalies, and bound growth by a principled (Northcott) capacity. All exact, all witnessed.")
    return result


if __name__ == "__main__":
    run(verbose=True)
