"""anomaly_detector.py -- A7: a streaming, exact, fully-local anomaly / novelty detector.

The substrate's cleanest product use-case: residual = novelty. This WRAPS the existing learner +
detection (it adds no new math), turning them into a calibration-gated novelty detector over a stream
of EXACT observations. Two novelty channels:

  (a) IN-FIELD / off-axis novelty   -- the in-field residual norm ||r||_G of an observation against the
      ResidualLearner's forced basis B (0 = in-distribution; > 0 = off-axis novelty).
  (b) OUT-OF-FIELD novelty          -- the field-residual of an observation against the captured field K
      inside a working field W (0 = in K; > 0 = needs a field extension), via CompositumLearner /
      field_extension.WorkingField.

For each observation it emits an AnomalyScore. The alert is CALIBRATION-GATED: novelty is always scored,
but an `anomaly` is raised only once the calibration gate passes. Persistent novelty is surfaced as a
growth PROPOSAL (a SeedProposal in-field, or a FieldExtensionProposal out-of-field) through the existing
propose-for-confirm path -- the detector NEVER auto-grows or auto-acts; only an explicit confirm() by the
caller mutates anything. Surfaced proposals are recorded in a tamper-evident sha256 witness chain (G5).

Lightweight, pure stdlib; exact (Fraction/int, G8); monic-integer seeds/generators (G10); model-layer
only (grows the model, never z; no KIRA, no _IC_*, no Plate-Matrices, no numpy).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, Union

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from residual_learner import ResidualLearner            # noqa: E402  (in-field / off-axis tier)
from compositum import CompositumLearner, FieldExtensionProposal  # noqa: E402  (out-of-field tier)
from field_growing_learner import FieldGrowingLearner, FieldGrowthPlan  # noqa: E402  (auto-gain growth tier)

Frac = Fraction
Number = Union[int, Fraction]


@dataclass(frozen=True)
class AnomalyScore:
    """The per-observation result. `proposal` is a gated SUGGESTION only -- never auto-acted."""
    kind: str                  # "in_field" | "out_of_field"
    score: Fraction            # EXACT novelty score (a residual norm); 0 == in-distribution
    novel: bool                # score > novelty_threshold (raw novelty, pre-calibration)
    anomaly: bool              # novel AND calibrated -> an actual alert
    calibrated: bool           # the calibration-gate state at this observation
    proposal: object = None    # SeedProposal | FieldExtensionProposal | None -- a suggestion, never acted

    @property
    def score_float(self) -> float:
        return float(self.score)   # DISPLAY only


class AnomalyDetector:
    """Streaming novelty/anomaly detector over the exact substrate. Wraps a ResidualLearner (in-field
    tier) and, optionally, a CompositumLearner (out-of-field tier). Scores, gates, and surfaces growth
    proposals -- it never grows the model itself (propose-for-confirm; the caller confirms)."""

    def __init__(
        self,
        learner: ResidualLearner,
        *,
        compositum: Optional[CompositumLearner] = None,
        field_growing_learner: Optional[FieldGrowingLearner] = None,
        extension_generator: Optional[Sequence[int]] = None,
        calibration_ok: Optional[Callable[[], bool]] = None,
        novelty_threshold: Number = Fraction(0),
    ):
        if not isinstance(learner, ResidualLearner):
            raise TypeError("learner must be a ResidualLearner")
        if compositum is not None and not isinstance(compositum, CompositumLearner):
            raise TypeError("compositum must be a CompositumLearner or None")
        if field_growing_learner is not None and not isinstance(field_growing_learner, FieldGrowingLearner):
            raise TypeError("field_growing_learner must be a FieldGrowingLearner or None")
        self.learner = learner
        self.compositum = compositum
        # the auto-gain growth tier (optional): detection feeds the EXACT out-of-field residual into the
        # field-growing learner's gate -- no caller-supplied gain. Still propose-only (the caller confirms).
        self.field_growing_learner = field_growing_learner
        self.extension_generator = list(extension_generator) if extension_generator is not None else None
        self._calibration_ok = calibration_ok or (lambda: True)
        self.novelty_threshold = Frac(novelty_threshold)
        # stats + tamper-evident log of surfaced proposals (G5)
        self.n_in_field = 0
        self.n_out_of_field = 0
        self.n_alerts = 0
        self.n_proposals = 0
        self._witness: List[dict] = []
        self._prev_hash = "genesis"

    def calibrated(self) -> bool:
        return bool(self._calibration_ok())

    # -- the streaming entry point ------------------------------------------ #
    def observe(self, coords: Sequence[Number], *, space: str = "in_field") -> AnomalyScore:
        """Score one EXACT observation. space='in_field' (ResidualLearner coords) or
        space='out_of_field' (working-field coords). Never grows the model."""
        if space == "in_field":
            return self._score_in_field(coords)
        if space == "out_of_field":
            return self._score_out_of_field(coords)
        raise ValueError(f"space must be 'in_field' or 'out_of_field', got {space!r}")

    def _score_in_field(self, x) -> AnomalyScore:
        self.learner.observe(x)                                  # updates residual-field + streak (no growth)
        score = self.learner.state()["last_residual_norm"]       # exact ||r||_G ; 0 == in-distribution
        proposal = None
        if score > self.novelty_threshold and self.calibrated():  # surface a proposal ONLY when calibrated
            proposal = self.learner.propose()                     # gated by persistence too; pure (no growth)
        return self._finish("in_field", score, proposal)

    def _score_out_of_field(self, x) -> AnomalyScore:
        if self.compositum is None:
            raise ValueError("no out-of-field tier configured (pass compositum=CompositumLearner(...))")
        det = self.compositum.detect(x)                          # field-residual against captured K (pure)
        score = det.field_residual_norm
        proposal = None
        if score > self.novelty_threshold and self.calibrated():  # surface a proposal ONLY when calibrated
            cand = self.compositum.propose(x)                     # FieldExtensionProposal or a Refusal
            proposal = cand if isinstance(cand, FieldExtensionProposal) else None
        return self._finish("out_of_field", score, proposal)

    def propose_field_growth(self, *, generator_min_poly: Optional[Sequence[int]] = None,
                             element_coords: Optional[Sequence[Number]] = None) -> AnomalyScore:
        """The auto-gain seam: measure the out-of-field residual via the FieldGrowingLearner and surface a
        growth proposal whose gain IS that measured residual -- detection driving growth without a
        caller-supplied gain. Calibration-gated like every proposal; STILL propose-only (the returned
        FieldGrowthPlan is a suggestion -- only confirm_extension() grows the field, G2)."""
        if self.field_growing_learner is None:
            raise ValueError("no auto-gain growth tier configured (pass field_growing_learner=...)")
        gen = list(generator_min_poly) if generator_min_poly is not None else self.extension_generator
        if gen is None:
            raise ValueError("no extension generator (pass generator_min_poly= or set extension_generator)")
        fgl = self.field_growing_learner
        score = fgl.out_of_field_residual_norm(gen, element_coords=element_coords)   # EXACT measured residual
        proposal = None
        if score > self.novelty_threshold and self.calibrated():     # surface ONLY when calibrated
            cand = fgl.propose_extension(gen, element_coords=element_coords)          # gain=None -> auto (== score)
            proposal = cand if isinstance(cand, FieldGrowthPlan) else None
        return self._finish("out_of_field", score, proposal)

    def _finish(self, kind: str, score: Fraction, proposal) -> AnomalyScore:
        calibrated = self.calibrated()
        novel = score > self.novelty_threshold
        anomaly = novel and calibrated                           # CALIBRATION-GATED alert
        if kind == "in_field":
            self.n_in_field += 1
        else:
            self.n_out_of_field += 1
        if anomaly:
            self.n_alerts += 1
        if proposal is not None:
            self.n_proposals += 1
            self._witness_proposal(kind, score, proposal)        # G5: record the surfaced proposal
        return AnomalyScore(kind=kind, score=score, novel=novel, anomaly=anomaly,
                            calibrated=calibrated, proposal=proposal)

    # -- tamper-evident witness of surfaced proposals (G5) ------------------ #
    def _witness_proposal(self, kind: str, score: Fraction, proposal) -> dict:
        mp = (getattr(proposal, "min_poly", None) or getattr(proposal, "generator_min_poly", None)
              or getattr(proposal, "m_beta", None))
        body = {
            "event": "novelty_proposal",
            "index": len(self._witness),
            "kind": kind,
            "score": str(score),
            "proposal_type": type(proposal).__name__,
            "min_poly": list(mp) if mp is not None else None,
            "prev_hash": self._prev_hash,
        }
        digest = hashlib.sha256(
            (self._prev_hash + json.dumps(body, sort_keys=True, separators=(",", ":"))).encode()
        ).hexdigest()[:16]
        record = dict(body, hash=digest)
        self._witness.append(record)
        self._prev_hash = digest
        return record

    def verify_witness(self) -> bool:
        prev = "genesis"
        for rec in self._witness:
            body = {k: rec[k] for k in
                    ("event", "index", "kind", "score", "proposal_type", "min_poly", "prev_hash")}
            if body["prev_hash"] != prev:
                return False
            digest = hashlib.sha256(
                (prev + json.dumps(body, sort_keys=True, separators=(",", ":"))).encode()
            ).hexdigest()[:16]
            if digest != rec["hash"]:
                return False
            prev = digest
        return True

    def stats(self) -> dict:
        return {"in_field": self.n_in_field, "out_of_field": self.n_out_of_field,
                "alerts": self.n_alerts, "proposals": self.n_proposals,
                "witness_len": len(self._witness), "calibrated": self.calibrated()}


# --------------------------------------------------------------------------- #
# __main__: an in-distribution stream (quiet) -> off-axis + out-of-field anomalies
# --------------------------------------------------------------------------- #
def _demo() -> None:
    from residual_learner import g_orthogonal_integer_vector
    from compositum import Factor
    from field_extension import _unit

    PHI4 = [1, 0, -10, 0, 1]                                    # K = Q(sqrt2+sqrt3), power basis
    learner = ResidualLearner(PHI4, [[1, 0, 0, 0], [0, 1, 0, 0]], persistence_N=3)
    comp = CompositumLearner([[4, 0, 0, 0], [0, 8, 0, 0], [0, 0, 12, 0], [0, 0, 0, 24]],
                             Factor("Q(sqrt7)", [[2, 0], [0, 14]], [1, 0, -7]))
    cal = {"ok": False}
    det = AnomalyDetector(learner, compositum=comp, calibration_ok=lambda: cal["ok"])
    w = g_orthogonal_integer_vector(learner._cols, learner._G)

    print("-- in-distribution stream (in span B): quiet --")
    for a, b in [(2, 1), (-3, 4), (5, -2)]:
        s = det.observe([Frac(a), Frac(b), Frac(0), Frac(0)])
        print(f"  score={s.score}  novel={s.novel}  anomaly={s.anomaly}")

    print("-- off-axis anomaly stream (calibration OFF -> alert suppressed) --")
    for _ in range(3):
        s = det.observe([Frac(1) + w[0], Frac(0) + w[1], Frac(0) + w[2], Frac(0) + w[3]])
        print(f"  score={s.score}  novel={s.novel}  anomaly={s.anomaly}  proposal={type(s.proposal).__name__}")

    print("-- calibration ON: the next off-axis observation alerts + surfaces a proposal --")
    cal["ok"] = True
    s = det.observe([Frac(1) + w[0], Frac(0) + w[1], Frac(0) + w[2], Frac(0) + w[3]])
    print(f"  score={s.score}  anomaly={s.anomaly}  proposal={type(s.proposal).__name__}  (learner degree still {len(learner._cols)})")

    print("-- out-of-field anomaly: sqrt7 (calibration ON) --")
    s7 = det.observe(_unit(1, 8), space="out_of_field")
    print(f"  score={s7.score}  anomaly={s7.anomaly}  proposal={type(s7.proposal).__name__}  (compositum degree still {comp.degree})")
    print("stats:", det.stats(), " witness_ok:", det.verify_witness())


if __name__ == "__main__":
    _demo()
