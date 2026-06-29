"""field_growing_learner.py -- the both-tier coordinator that ACTS on a confirmed field extension.

A ResidualLearner reads residuals and grows its forced basis B *within a fixed ambient field* K = Q(theta)
-- its ambient field never changes (a deliberate invariant). When a persistent residual is OUT of K (it
lives in a strictly larger field), the model must grow the FIELD itself, not just the basis. That is a NEW
field, hence -- mathematically -- a NEW learner.

FieldGrowingLearner owns the in-field ResidualLearner (tier 1) and performs cross-field growth (tier 2):
on a confirmed extension K -> K(beta) it constructs a FRESH ResidualLearner on the true compositum Q(theta)
(P2c: factor m_beta over K; non-disjoint => degree m*e' < m*k), re-homing the forced basis B into the new
field. It is propose-for-confirm (confirm_extension is the SOLE field-growth mutator, G2) and witnessed
(sha256 chain, G5). It is DISTINCT from AnomalyDetector, which only scores/surfaces proposals and never acts.

ResidualLearner is left UNCHANGED. The re-home works because:
  * integral_basis_for returns the POWER basis with identity transforms, so a fresh ResidualLearner(m_theta)
    builds exactly trace_form_gram(m_theta) -- the same metric the P2c builder uses; coordinates align.
  * K embeds into Q(theta) via alpha -> alpha_coords (the compositum builder's image of the K generator);
    each old B column (a K element) maps through it. An embedded algebraic integer can have FRACTIONAL
    power-basis coords (Z[theta] subset O_K), so each re-homed column is scaled to clear denominators -- a
    per-column scaling that leaves the projector P = B(B^T G B)^-1 B^T G (hence every residual) INVARIANT,
    while yielding the integer-coord algebraic-integer seeds ResidualLearner expects. The new generator
    beta is appended (its beta_coords, denominator-cleared).
  * The constant 1 = [1,0,...,0] is basis element 0 in ANY power basis, so 1 in B SURVIVES the re-home --
    keeping the capacity gate's info-threshold precondition valid in Q(theta) for later. (Asserted in tests.)

The capacity decision for an extension consults the EXACT compositum degree:
    capacity_decision(m_beta, gain, budget, effective_degree = m*e')
so Northcott admissibility judges the real grown size, not the seed minpoly's degree. The gate's
info-threshold path stays OFF (default floor=0, exact admissibility only) -- this increment wires the
effective_degree admissibility, it does NOT turn on the degree-aware Lehmer threshold.

Exact (Fraction/int, G8); monic-integer (G10); model-layer only (no z/KIRA/_IC_*/Plate-Matrices/numpy);
propose-for-confirm with confirm the sole mutator (G2); sha256 witness (G5).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional, Sequence, Union

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import projector as _pj                       # noqa: E402  (exact projector_matrix / residual_norm)
from residual_learner import ResidualLearner   # noqa: E402  (in-field tier, UNCHANGED)
from coords_to_minpoly import regular_representation  # noqa: E402  (exact mult-by-element matrix)
from compositum_nondisjoint import (           # noqa: E402  (P2c true compositum)
    build_compositum, CompositumResult, trace_form_gram)
from number_field_factor import FactorizationUnsupported  # noqa: E402
from capacity import Budget, capacity_decision, CapacityVerdict  # noqa: E402  (A3 Northcott gate)
import integral_basis as _ib                  # noqa: E402  (G10 guard)

Frac = Fraction
Number = Union[int, Fraction]


@dataclass(frozen=True)
class FieldGrowthRefusal:
    """No field growth. kind in {'already_in_k','factor_unsupported','capacity_reject','capacity_stop'}."""
    kind: str
    reason: str


@dataclass(frozen=True)
class FieldGrowthPlan:
    """A gated SUGGESTION to grow the FIELD K -> Q(theta). confirm_extension() acts; this does not."""
    m_beta: List[int]              # the new generator's minpoly over Q
    old_degree: int                # [K:Q]
    new_degree: int                # [Q(theta):Q] = m * e'
    e_prime: int                   # [K(beta):K]
    m_theta: List[int]             # the compositum primitive element's minpoly
    gain: Fraction                 # the out-of-field residual norm fed to the gate (auto or override)
    verdict: CapacityVerdict       # capacity_decision(m_beta, gain, ..., effective_degree=new_degree)
    _res: CompositumResult         # the exact construction (alpha/beta coords) used by confirm


def _matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def _embed_into_theta(k_coords: Sequence[Fraction], M_alpha, D: int) -> List[Fraction]:
    """Image in Q(theta) of a K element sum_i k_coords[i]*alpha^i, via Horner on M_alpha = mult-by-(alpha
    image) on Q(theta): result = sum_i k_coords[i] * M_alpha^i e_0. Exact Fraction."""
    r = [Frac(0)] * D
    for i in range(len(k_coords) - 1, -1, -1):
        r = _matvec(M_alpha, r)
        r[0] += Frac(k_coords[i])
    return r


def _clear_denominators(v: Sequence[Fraction]) -> List[int]:
    """Scale a rational coordinate vector to the smallest integer vector on the same line (clears
    denominators). A per-column scaling -- it leaves the projector (hence every residual) invariant."""
    vv = [Frac(c) for c in v]
    denoms = [c.denominator for c in vv if c != 0]
    L = math.lcm(*denoms) if denoms else 1
    return [int(c * L) for c in vv]


def _transpose(M):
    return [[M[i][j] for i in range(len(M))] for j in range(len(M[0]))]


def _k_subspace_residual_norm(res: CompositumResult, m: int, element_coords: Sequence[Fraction]) -> Fraction:
    """Exact out-of-field residual norm in the working over-field Q(theta): the trace-form norm
    ||element - P_K(element)||^2_{G_theta}, where P_K projects onto the embedded K = Q(alpha) subspace
    {1, alpha, ..., alpha^{m-1}} (alpha's image in Q(theta)). This is the component of `element` forcing
    the extension. EXACT Fraction (G8). Reuses projector.projector_matrix / residual_norm."""
    D = res.new_degree
    M_alpha = regular_representation(res.alpha_coords, res.m_theta)   # mult-by-(alpha image) on Q(theta)
    e0 = [Frac(1)] + [Frac(0)] * (D - 1)
    k_cols = []                                                       # {alpha^0, ..., alpha^{m-1}} images
    cur = e0
    for _ in range(m):
        k_cols.append(cur)
        cur = _matvec(M_alpha, cur)
    G_theta = trace_form_gram(res.m_theta)
    P_K = _pj.projector_matrix(_transpose(k_cols), G_theta)          # G_theta-projector onto col(K-basis)
    if P_K is _pj.NO_PROJECTION:
        raise ValueError("embedded K subspace is G_theta-degenerate (no projector)")
    return _pj.residual_norm([Frac(c) for c in element_coords], P_K, G_theta)


class FieldGrowingLearner:
    """In-field ResidualLearner (tier 1) + cross-field growth (tier 2). confirm_extension is the sole
    field-growth mutator; on a confirmed non-disjoint extension it constructs a FRESH ResidualLearner on
    the true compositum Q(theta) and re-homes the forced basis."""

    def __init__(self, ambient_min_poly: Sequence[int], seeds: Sequence[Sequence[Number]], *,
                 persistence_N: int = 3, epsilon: Fraction = Fraction(1, 100),
                 budget: Optional[Budget] = None, calibration_ok=None):
        self._cfg = dict(persistence_N=int(persistence_N), epsilon=Frac(epsilon),
                         budget=budget, calibration_ok=calibration_ok)
        self.learner = ResidualLearner(ambient_min_poly, seeds, persistence_N=int(persistence_N),
                                       epsilon=Frac(epsilon), budget=budget, calibration_ok=calibration_ok)
        self._witness: List[dict] = []
        self._prev_hash = "genesis"
        self.growth_history: List[dict] = []

    # -- pass-throughs to the in-field tier -------------------------------------------------- #
    @property
    def degree(self) -> int:
        return self.learner.degree

    @property
    def ambient_min_poly(self) -> List[int]:
        return self.learner.ambient_min_poly

    @property
    def budget(self) -> Budget:
        return self.learner.budget

    def observe(self, x) -> None:
        """Feed an in-field observation to the in-field tier (never grows the field)."""
        self.learner.observe(x)

    def residual_norm(self, x) -> Fraction:
        """Exact field-residual norm of x against the CURRENT forced basis (pure; ==0 IFF captured)."""
        coords = self.learner._as_coords(x)
        return _pj.residual_norm(coords, self.learner._P, self.learner._G)

    def one_in_basis(self) -> bool:
        """True iff the constant 1 lies in the forced-basis span (the gate's info-threshold precondition)."""
        e0 = [Frac(1)] + [Frac(0)] * (self.degree - 1)
        return _pj.residual_norm(e0, self.learner._P, self.learner._G) == 0

    # -- out-of-field residual (the detector-driven gain) ------------------------------------ #
    def out_of_field_residual_norm(self, generator_min_poly: Sequence[int], *,
                                   element_coords: Optional[Sequence[Number]] = None) -> Fraction:
        """The EXACT out-of-field residual norm that motivates growing: ||element - P_K(element)||^2 in the
        working over-field Q(theta), with P_K the trace-form projection onto the embedded current field K.
        `element` defaults to the new generator beta (its Q(theta) coords); pass element_coords for a
        different out-of-field observation (already in Q(theta) power coords). EXACT Fraction (G8).
        Returns 0 if the generator is already in K (nothing forces an extension)."""
        m_beta = _ib._guard_int_monic(generator_min_poly)
        res = build_compositum(self.ambient_min_poly, m_beta)
        elt = res.beta_coords if element_coords is None else [Frac(c) for c in element_coords]
        return _k_subspace_residual_norm(res, self.degree, elt)

    # -- (tier 2) propose a field extension (pure; never grows) ------------------------------ #
    def propose_extension(self, generator_min_poly: Sequence[int], *, gain: Optional[Number] = None,
                          element_coords: Optional[Sequence[Number]] = None
                          ) -> Union[FieldGrowthPlan, FieldGrowthRefusal]:
        """Factor m_beta over the CURRENT field K and gate the extension. Pure -- confirm_extension() acts.

        gain: the out-of-field novelty magnitude fed to the capacity gate. By DEFAULT (gain=None) it is
        AUTO-COMPUTED as the exact out-of-field residual norm (out_of_field_residual_norm) -- the seam that
        lets detection drive growth without a caller-supplied value. An explicit gain is an OPTIONAL
        OVERRIDE (back-compat); a float gain is rejected (G8).

        Branches: beta in K (e'=1) -> 'already_in_k'; factorization beyond the Kronecker bound ->
        'factor_unsupported'; the Northcott gate (with effective_degree = the TRUE compositum degree m*e')
        -> 'capacity_reject'/'capacity_stop' or a FieldGrowthPlan to GROW."""
        if gain is not None and isinstance(gain, float):
            raise TypeError("gain must be exact (int/Fraction), not float (G8)")
        m_beta = _ib._guard_int_monic(generator_min_poly)
        try:
            res = build_compositum(self.ambient_min_poly, m_beta)
        except FactorizationUnsupported as exc:
            return FieldGrowthRefusal("factor_unsupported", str(exc))
        if res.e_prime == 1:
            return FieldGrowthRefusal("already_in_k", "beta is already in K (e'=1); no field growth")
        if gain is None:                                              # AUTO: the measured out-of-field residual
            elt = res.beta_coords if element_coords is None else [Frac(c) for c in element_coords]
            gain_f = _k_subspace_residual_norm(res, self.degree, elt)
        else:
            gain_f = Frac(gain)
        # the capacity gate judges the EXACT grown degree (info-threshold stays OFF: default floor=0)
        verdict = capacity_decision(m_beta, gain_f, self.budget, effective_degree=res.new_degree)
        if verdict.decision == "REJECT":
            return FieldGrowthRefusal(
                "capacity_reject",
                f"compositum degree {res.new_degree} exceeds the Northcott budget -- {verdict.reason}")
        if verdict.decision == "STOP":
            return FieldGrowthRefusal("capacity_stop", f"gain at/below floor -- {verdict.reason}")
        return FieldGrowthPlan(m_beta=list(m_beta), old_degree=self.degree, new_degree=res.new_degree,
                               e_prime=res.e_prime, m_theta=list(res.m_theta), gain=gain_f,
                               verdict=verdict, _res=res)

    # -- (tier 2) confirm: the SOLE field-growth mutator (G2) -------------------------------- #
    def confirm_extension(self, plan: FieldGrowthPlan) -> dict:
        """Grow the FIELD: construct a FRESH ResidualLearner on the true compositum Q(theta), re-homing the
        forced basis (each old column embedded K -> Q(theta) and denominator-cleared, then beta appended).
        After this the previously out-of-field beta is captured (residual 0). Witnessed (G5)."""
        if not isinstance(plan, FieldGrowthPlan):
            raise TypeError("confirm_extension() requires a FieldGrowthPlan from propose_extension()")
        res = plan._res
        D = res.new_degree
        m_theta = _ib._guard_int_monic(res.m_theta)           # G10 at the mutation point
        M_alpha = regular_representation(res.alpha_coords, m_theta)   # mult-by-(alpha image) on Q(theta)
        old_degree = self.degree
        # re-home each forced-basis column K -> Q(theta), clearing denominators (projector-invariant scaling)
        new_seeds: List[List[int]] = [
            _clear_denominators(_embed_into_theta(col, M_alpha, D)) for col in self.learner._cols]
        new_seeds.append(_clear_denominators(res.beta_coords))         # capture the new generator beta
        # the FRESH learner on Q(theta) -- ResidualLearner builds trace_form_gram(m_theta) itself
        self.learner = ResidualLearner(
            m_theta, new_seeds, persistence_N=self._cfg["persistence_N"], epsilon=self._cfg["epsilon"],
            budget=self._cfg["budget"], calibration_ok=self._cfg["calibration_ok"])
        record = self._witness_growth(old_degree, plan)
        self.growth_history.append(record)
        return record

    # -- field-growth witness hash-chain (G5) ------------------------------------------------ #
    _WITNESS_FIELDS = ("event", "index", "old_degree", "new_degree", "e_prime", "m_theta",
                       "generator_min_poly", "prev_hash")

    def _witness_growth(self, old_degree: int, plan: FieldGrowthPlan) -> dict:
        body = {
            "event": "field_growth",
            "index": len(self._witness),
            "old_degree": old_degree,
            "new_degree": plan.new_degree,
            "e_prime": plan.e_prime,
            "m_theta": list(plan.m_theta),
            "generator_min_poly": list(plan.m_beta),
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
            body = {k: rec[k] for k in self._WITNESS_FIELDS}
            if body["prev_hash"] != prev:
                return False
            digest = hashlib.sha256(
                (prev + json.dumps(body, sort_keys=True, separators=(",", ":"))).encode()
            ).hexdigest()[:16]
            if digest != rec["hash"]:
                return False
            prev = digest
        return True


# --------------------------------------------------------------------------- #
# __main__: K = Q(sqrt2) -> out-of-field beta = sqrt2+sqrt3 -> grow to Q(sqrt2,sqrt3), residual -> 0
# --------------------------------------------------------------------------- #
def _demo() -> None:
    fgl = FieldGrowingLearner([1, 0, -2], [[1, 0]])        # K = Q(sqrt2), forced basis {1}
    print("start: degree", fgl.degree, " 1 in B:", fgl.one_in_basis())
    plan = fgl.propose_extension([1, 0, -10, 0, 1], gain=Frac(1, 2))   # beta = sqrt2+sqrt3
    print("propose_extension ->", type(plan).__name__, "e'", plan.e_prime, "new_degree", plan.new_degree,
          "verdict", plan.verdict.decision)
    rec = fgl.confirm_extension(plan)
    print("after grow: degree", fgl.degree, " 1 in B:", fgl.one_in_basis(),
          " beta residual:", fgl.residual_norm(plan._res.beta_coords), " witness", rec["hash"],
          " chain_ok", fgl.verify_witness())


if __name__ == "__main__":
    _demo()
