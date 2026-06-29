"""compositum.py -- A2.P2b: disjoint-compositum field-extension GROWTH.

Builds on A2.P2a detection (field_extension.WorkingField). When a persistent element is flagged
out-of-field, propose a FieldExtensionProposal; confirm() -- the SOLE mutator (G2) -- GROWS the
captured field K into the disjoint compositum K(beta) by capturing the new generator's factor L:
the working Gram is the Kronecker product G_W = G_K (x) G_L (Prop 3.3), the projector is re-derived,
the growth is witnessed (sha256 chain), and the novel element's residual -> 0.

DISJOINT case only. A candidate already in K (non-disjoint, e.g. sqrt6 in Q(sqrt2,sqrt3)) is REFUSED
with a clear 'non-disjoint, deferred to P2c' message -- no growth. Over-cap extensions are refused
(HARD_DEGREE_CAP). P2c (non-disjoint compositum) and P2d (capacity policy / regime-B Trager
factorization) stay DEFERRED to the Arakelov/P3 track.

Exact (Fraction/int, G8); monic-integer generator (G10); model-layer only (no z/KIRA/_IC_*/PM/numpy);
propose-for-confirm (G2).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional, Union

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import integral_basis as _ib                  # noqa: E402  (_guard_int_monic, G10)
from field_extension import (                 # noqa: E402  (reuse the A2.P2a detection substrate)
    WorkingField, FieldDetection, HARD_DEGREE_CAP, kron, _unit, _exact,
)
from compositum_nondisjoint import (          # noqa: E402  (P2c: factor m_beta over K -> true compositum)
    build_compositum, trace_form_gram, CompositumResult,
)
from number_field_factor import FactorizationUnsupported   # noqa: E402  (bounded Kronecker refusal)

Frac = Fraction
Number = Union[int, Fraction]


@dataclass(frozen=True)
class Factor:
    """A candidate disjoint field factor L = Q(beta): its trace-form Gram + its generator's minpoly."""
    name: str
    gram: List[List[Number]]      # G_L (trace form of L)
    min_poly: List[int]           # monic-integer minpoly of beta (G10)


@dataclass(frozen=True)
class FieldExtensionProposal:
    """A gated SUGGESTION to grow K -> K(beta). confirm() acts; this does not. `disjoint` distinguishes the
    A2.P2b Kronecker-Gram extension (disjoint=True, new_degree = old * deg(L)) from the P2c TRUE compositum
    (disjoint=False, new_degree = old * e' with 1 < e' < deg(L)); the P2c fields carry the exact compositum
    minimal polynomial m_theta, the new generator's coordinates in the {1,theta,...} power basis, and e'."""
    generator_min_poly: List[int]
    old_degree: int               # [K : Q]
    new_degree: int               # [K(beta) : Q] = old_degree * (deg(L) disjoint | e' non-disjoint)
    disjoint: bool
    factor_name: str = ""
    reason: str = "persistent out-of-field element; disjoint extension"
    # -- P2c (non-disjoint true compositum) only; None for a disjoint proposal -------------------- #
    m_theta: Optional[List[int]] = None         # exact minpoly of the compositum primitive element theta
    beta_coords: Optional[List[Fraction]] = None  # beta in the power basis {1, theta, ..., theta^{new-1}}
    e_prime: Optional[int] = None               # [K(beta) : K]


@dataclass(frozen=True)
class FieldExtensionRefusal:
    """A clear refusal -- NO growth. kind in
    {'non_disjoint', 'already_in_k', 'over_cap', 'already_extended', 'factor_unsupported'}."""
    kind: str
    reason: str


class CompositumLearner:
    """Current captured field K + one candidate disjoint factor L = Q(beta). detect() (reusing the
    P2a field-residual) flags out-of-field elements; confirm() is the SOLE mutator and grows K into
    the disjoint compositum K(beta) via the Kronecker Gram G_W = G_K (x) G_L. Bounded by
    HARD_DEGREE_CAP; non-disjoint / over-cap are refused (no growth)."""

    def __init__(self, base_gram, candidate: Factor, *, degree_cap: int = HARD_DEGREE_CAP,
                 base_min_poly: Optional[List[int]] = None):
        if not isinstance(candidate, Factor):
            raise TypeError("candidate must be a Factor(name, gram, min_poly)")
        _ib._guard_int_monic(candidate.min_poly)              # G10: the generator is an algebraic integer
        self._G_K = [[_exact(c) for c in row] for row in base_gram]
        self.candidate = candidate
        self.degree_cap = degree_cap
        self.base_degree = len(self._G_K)
        self.extension_degree = len(candidate.gram)
        self.new_degree = self.base_degree * self.extension_degree
        self._extended = False
        self._witness: List[dict] = []
        self._prev_hash = "genesis"
        # P2c: when K's defining minpoly is supplied, the learner can DETECT non-disjointness (factor
        # m_beta over K) and grow into the TRUE compositum. The Kronecker tensor is then NOT eagerly built
        # (its degree m*k can exceed the cap even when the true compositum m*e' does not); the captured
        # field starts as K itself and the degree decision moves to propose(). Without base_min_poly the
        # A2.P2b disjoint behaviour is byte-for-byte unchanged.
        if base_min_poly is not None:
            self._base_min_poly = _ib._guard_int_monic(base_min_poly)
            if len(self._base_min_poly) - 1 != self.base_degree:
                raise ValueError("base_min_poly degree must equal [K:Q] = len(base_gram)")
            self._wf = WorkingField(self._G_K, [_unit(i, self.base_degree) for i in range(self.base_degree)],
                                    degree_cap=degree_cap)
            self.working_gram = None                          # decided per-proposal (disjoint vs true compositum)
        else:
            self._base_min_poly = None
            # Working field W = K (x) L. WorkingField enforces the degree cap, so an over-cap extension is
            # refused HERE -- the big field is never even built (nothing blows up).
            self._wf = WorkingField.from_two_factors(self._G_K, candidate.gram, degree_cap=degree_cap)
            self.working_gram = self._wf.gram                 # G_W = G_K (x) G_L (Prop 3.3)

    @property
    def degree(self) -> int:
        """[K : Q] of the CURRENT captured field (grows from base_degree to new_degree on confirm)."""
        return self._wf.subfield_degree

    @property
    def working_degree(self) -> int:
        return self.new_degree

    def detect(self, element) -> FieldDetection:
        """Is `element` (W-coords) in the current captured field, or out-of-field? Pure -- no growth."""
        return self._wf.detect(element)

    def propose(self, element=None) -> Union[FieldExtensionProposal, FieldExtensionRefusal, None]:
        """Propose how to grow the field. Pure -- never grows the field (that is confirm).

        Without base_min_poly (A2.P2b): an out-of-field element -> a disjoint FieldExtensionProposal; an
        element already in K -> a 'non_disjoint' Refusal. UNCHANGED.

        With base_min_poly (P2c): factor the candidate's minpoly m_beta over K = Q(alpha) and branch on
        e' = [K(beta):K]: e'==1 -> 'already_in_k' refusal; e'==deg(m_beta) -> a disjoint proposal (the
        Kronecker path); 1 < e' < deg(m_beta) -> a TRUE-compositum proposal (m_theta + beta-coords). An
        over-cap compositum -> 'over_cap'; a factorization beyond the Kronecker bound -> 'factor_unsupported'
        (Zassenhaus upgrade)."""
        if self._extended:
            return FieldExtensionRefusal("already_extended", "this learner has already grown once")
        if self._base_min_poly is None:
            det = self._wf.detect(element)
            if det.in_field:
                return FieldExtensionRefusal(
                    "non_disjoint",
                    "element is already in K (non-disjoint); deferred to P2c -- no growth")
            return FieldExtensionProposal(
                generator_min_poly=list(self.candidate.min_poly),
                old_degree=self.base_degree,
                new_degree=self.new_degree,
                disjoint=True,
                factor_name=self.candidate.name,
            )
        # ---- P2c: K's minpoly known -> detect non-disjointness by factoring m_beta over K ---------- #
        k = len(self.candidate.min_poly) - 1
        try:
            res: CompositumResult = build_compositum(self._base_min_poly, self.candidate.min_poly)
        except FactorizationUnsupported as exc:
            return FieldExtensionRefusal("factor_unsupported", str(exc))
        if res.e_prime == 1:
            return FieldExtensionRefusal(
                "already_in_k", "beta is already in K (e'=1, m_beta has a linear factor over K); no growth")
        if res.new_degree > self.degree_cap:
            return FieldExtensionRefusal(
                "over_cap", f"compositum degree {res.new_degree} exceeds HARD_DEGREE_CAP {self.degree_cap}")
        if res.e_prime == k:                                  # disjoint: m_beta stays irreducible over K
            return FieldExtensionProposal(
                generator_min_poly=list(self.candidate.min_poly),
                old_degree=self.base_degree, new_degree=res.new_degree, disjoint=True,
                factor_name=self.candidate.name,
                reason="persistent out-of-field element; disjoint extension (e'=deg m_beta)")
        # 1 < e' < k : non-disjoint TRUE compositum
        return FieldExtensionProposal(
            generator_min_poly=list(self.candidate.min_poly),
            old_degree=self.base_degree, new_degree=res.new_degree, disjoint=False,
            factor_name=self.candidate.name,
            reason=f"non-disjoint compositum: m_beta factors over K (e'={res.e_prime} < deg {k})",
            m_theta=list(res.m_theta), beta_coords=list(res.beta_coords), e_prime=res.e_prime)

    def confirm(self, proposal: FieldExtensionProposal) -> dict:
        """The SOLE mutator (G2). GROW K -> K(beta), re-derive the projector, and witness the extension.
        After this, the novel element's field-residual is 0 (it is now captured).

        disjoint  : the captured field becomes all of W = K (x) L over G_W = G_K (x) G_L (Prop 3.3).
        non-disjoint (P2c): the captured field becomes the TRUE compositum Q(theta) (degree m*e' < m*k),
                    over its exact trace-form Gram; the generator beta -- supplied in the {1,theta,...}
                    power basis -- is now captured (residual 0)."""
        if not isinstance(proposal, FieldExtensionProposal):
            raise TypeError("confirm() requires a FieldExtensionProposal from propose()")
        if self._extended:
            raise ValueError("already extended (single-step growth; a further extension is a new learner)")
        _ib._guard_int_monic(proposal.generator_min_poly)     # G10 re-validate at the mutation point
        self._captured_beta_coords = None
        if proposal.disjoint:
            gram = self.working_gram if self.working_gram is not None else kron(self._G_K, self.candidate.gram)
            # cheap exact self-check: the working Gram IS the Kronecker product (Prop 3.3 / Rem 3.4)
            assert gram == kron(self._G_K, self.candidate.gram)
            full_basis = [_unit(i, proposal.new_degree) for i in range(proposal.new_degree)]   # capture all of W
            self._wf = WorkingField(gram, full_basis, degree_cap=self.degree_cap)              # re-derive P
        else:
            _ib._guard_int_monic(proposal.m_theta)            # G10: the compositum generator is integral
            gram = trace_form_gram(proposal.m_theta)          # exact trace form of Q(theta)
            full_basis = [_unit(i, proposal.new_degree) for i in range(proposal.new_degree)]   # capture Q(theta)
            self._wf = WorkingField(gram, full_basis, degree_cap=self.degree_cap)
            self._captured_beta_coords = list(proposal.beta_coords)
        self._extended = True
        return self._witness_extension(proposal)

    # -- witness hash-chain (G5) -------------------------------------------- #
    _WITNESS_FIELDS = ("event", "index", "generator_min_poly", "old_degree", "new_degree", "disjoint",
                       "e_prime", "m_theta", "prev_hash")

    def _witness_extension(self, proposal: FieldExtensionProposal) -> dict:
        body = {
            "event": "field_extension",
            "index": len(self._witness),
            "generator_min_poly": list(proposal.generator_min_poly),
            "old_degree": proposal.old_degree,
            "new_degree": proposal.new_degree,
            "disjoint": proposal.disjoint,
            "e_prime": proposal.e_prime,                      # P2c: [K(beta):K] (None for disjoint)
            "m_theta": list(proposal.m_theta) if proposal.m_theta is not None else None,
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
# __main__: the sqrt7 scenario -- detect -> propose -> confirm -> residual 0
# --------------------------------------------------------------------------- #
def _demo() -> None:
    G_K = [[4, 0, 0, 0], [0, 8, 0, 0], [0, 0, 12, 0], [0, 0, 0, 24]]   # K = Q(sqrt2,sqrt3), det 9216
    sqrt7_factor = Factor("Q(sqrt7)", [[2, 0], [0, 14]], [1, 0, -7])   # L = Q(sqrt7), x^2 - 7
    L = CompositumLearner(G_K, sqrt7_factor)
    sqrt7 = _unit(1, 8)                                                # 1 (x) sqrt7  (out of K)
    print("before: captured degree", L.degree, " detect(sqrt7) flagged =", L.detect(sqrt7).extension_flagged)
    p = L.propose(sqrt7)
    print("propose ->", type(p).__name__, p.old_degree, "->", p.new_degree, " disjoint =", p.disjoint,
          " min_poly =", p.generator_min_poly)
    print("  (propose did not grow: degree still", L.degree, ")")
    rec = L.confirm(p)
    print("after confirm: captured degree", L.degree, " detect(sqrt7) residual_norm =",
          L.detect(sqrt7).field_residual_norm, " witness =", rec["event"], rec["hash"],
          " chain_ok =", L.verify_witness())
    print("non-disjoint sqrt6 (already in K):", type(CompositumLearner(G_K, sqrt7_factor).propose(_unit(6, 8))).__name__)


if __name__ == "__main__":
    _demo()
