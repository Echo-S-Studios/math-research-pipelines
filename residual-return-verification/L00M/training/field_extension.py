"""field_extension.py -- A2.P2a: out-of-field DETECTION (no growth).

The exact, bounded, disjoint slice of the A2.P2 design (see A2_P2_DESIGN.md). A WorkingField
declares an exact over-field W (regime A) in a PRODUCT basis with the tensor trace-form Gram
G_W = G_K (x) G_L (Prop 3.3, RESEARCH_VECTOR_SUBSTRATE_MATH section 3.3). The current captured
sub-field K <= W is a Q-subspace of W. The FIELD-RESIDUAL of an observation alpha in W is the
projection residual of alpha onto K inside W's trace form -- REUSING the L0 projector:

    field_residual(alpha) = alpha - P_K alpha        (exact;  == 0  iff  alpha in K)

A persistent nonzero field-residual means alpha would need a field EXTENSION to be captured. This
module only DETECTS and FLAGS that; it NEVER grows the basis or adjoins a field (that is A2.P2b,
gated separately). A HARD DEGREE CAP bounds the working-field degree NOW, so nothing can blow up
once growth lands.

Exact (Fraction/int, G8); model-layer only (no KIRA, no z, no _IC_*, no Plate-Matrices, no numpy).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence, Union

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import projector as _pj   # noqa: E402  (projector_matrix, residual, residual_norm, NO_PROJECTION)

Frac = Fraction
Number = Union[int, Fraction]

# Capacity bound (Northcott-style): the working/extension field degree may NEVER exceed this.
# Declared NOW even though extension GROWTH lands in A2.P2b, so nothing can blow up later.
HARD_DEGREE_CAP = 64


def _exact(c: Number) -> Fraction:
    if isinstance(c, float):
        raise TypeError("coordinates must be exact (int/Fraction), not float (G8)")
    return Frac(c)


def _unit(k: int, n: int) -> List[Fraction]:
    return [Frac(1) if t == k else Frac(0) for t in range(n)]


def _t(M):
    return [[M[i][j] for i in range(len(M))] for j in range(len(M[0]))]


def kron(A: Sequence[Sequence[Number]], B: Sequence[Sequence[Number]]) -> List[List[Fraction]]:
    """Exact Kronecker product A (x) B over Fraction."""
    p, q, r, s = len(A), len(A[0]), len(B), len(B[0])
    out = [[Frac(0)] * (q * s) for _ in range(p * r)]
    for i in range(p):
        for j in range(q):
            aij = Frac(A[i][j])
            if aij == 0:
                continue
            for k in range(r):
                for m in range(s):
                    out[i * r + k][j * s + m] = aij * Frac(B[k][m])
    return out


def tensor_gram(*grams) -> List[List[Fraction]]:
    """G = G_1 (x) G_2 (x) ... : the trace-form Gram of a disjoint compositum in the product basis is
    the Kronecker product of the factor Grams (Prop 3.3). Exact."""
    if not grams:
        raise ValueError("need at least one factor Gram")
    G = [[Frac(c) for c in row] for row in grams[0]]
    for nxt in grams[1:]:
        G = kron(G, nxt)
    return G


@dataclass(frozen=True)
class FieldDetection:
    """Result of out-of-field DETECTION. Carries no action -- A2.P2b would act on it; P2a only reports."""
    in_field: bool                      # is alpha in the captured sub-field K?  (field_residual == 0)
    field_residual: List[Fraction]      # exact alpha - P_K alpha (W-coords)
    field_residual_norm: Fraction       # exact <fr, fr>_{G_W}; == 0 IFF in-field
    extension_flagged: bool             # True iff an extension WOULD be needed (alpha not in K)
    subfield_degree: int                # [K : Q]
    working_degree: int                 # [W : Q]
    note: str = ""


class WorkingField:
    """An exact over-field W (product basis + tensor Gram G_W) with a captured sub-field K <= W.

    Detects whether an observation alpha in W lies in K (field_residual == 0) or would need an
    extension (field_residual != 0). DETECTION ONLY -- it never mutates the basis or adjoins a field.
    """

    def __init__(self, gram, subfield_basis, *, degree_cap: int = HARD_DEGREE_CAP):
        n = len(gram)
        if n == 0 or any(len(row) != n for row in gram):
            raise ValueError("gram must be a non-empty square matrix")
        if n > degree_cap:                                   # capacity bound (hard) -- nothing blows up
            raise ValueError(f"working-field degree {n} exceeds HARD_DEGREE_CAP {degree_cap}")
        if not subfield_basis:
            raise ValueError("captured sub-field needs at least one basis vector")
        for col in subfield_basis:
            if len(col) != n:
                raise ValueError(f"sub-field basis vectors must have length {n} (= [W:Q])")
        self.gram = [[_exact(c) for c in row] for row in gram]
        self.subfield_basis = [[_exact(c) for c in col] for col in subfield_basis]
        self.degree = n
        self.subfield_degree = len(self.subfield_basis)
        self.degree_cap = degree_cap
        self._P_K = _pj.projector_matrix(_t(self.subfield_basis), self.gram)   # reuse the L0 projector
        if self._P_K is _pj.NO_PROJECTION:
            raise ValueError("captured sub-field basis is rank-deficient (B^T G B singular)")

    def _as_element(self, alpha) -> List[Fraction]:
        if hasattr(alpha, "power_coords"):
            alpha = alpha.power_coords
        v = list(alpha)
        if len(v) != self.degree:
            raise ValueError(f"observation must have length {self.degree} (= [W:Q]); got {len(v)}")
        return [_exact(c) for c in v]

    def field_residual(self, alpha) -> List[Fraction]:
        """Exact alpha - P_K alpha in W-coords (the L0 projection residual against K)."""
        return _pj.residual(self._as_element(alpha), self._P_K)

    def field_residual_norm(self, alpha) -> Fraction:
        """Exact <field_residual, field_residual>_{G_W}; == 0 IFF alpha is in the captured sub-field K."""
        return _pj.residual_norm(self._as_element(alpha), self._P_K, self.gram)

    def is_in_field(self, alpha) -> bool:
        return self.field_residual_norm(alpha) == 0

    def detect(self, alpha) -> FieldDetection:
        """DETECTION ONLY: is alpha in K, or would it need an extension? Pure -- never grows/mutates."""
        element = self._as_element(alpha)
        fr = _pj.residual(element, self._P_K)
        rn = _pj.residual_norm(element, self._P_K, self.gram)
        in_field = (rn == 0)
        return FieldDetection(
            in_field=in_field,
            field_residual=fr,
            field_residual_norm=rn,
            extension_flagged=(not in_field),
            subfield_degree=self.subfield_degree,
            working_degree=self.degree,
            note=("in captured sub-field K" if in_field else
                  "OUT OF FIELD -- would need an extension (A2.P2b); flagged only, not grown"),
        )

    @classmethod
    def from_two_factors(cls, captured_gram, extension_gram, *, degree_cap: int = HARD_DEGREE_CAP):
        """W = K . L in the product basis, captured sub-field = K (the `captured_gram` factor).
        G_W = captured_gram (x) extension_gram (Prop 3.3); K = span{e_i (x) f_0} (the f_0 slots)."""
        d1, d2 = len(captured_gram), len(extension_gram)
        G_W = kron(captured_gram, extension_gram)
        subfield_basis = [_unit(i * d2, d1 * d2) for i in range(d1)]   # e_i (x) f_0  spans K
        return cls(G_W, subfield_basis, degree_cap=degree_cap)


# --------------------------------------------------------------------------- #
# __main__: detect sqrt6 (in K) vs sqrt7 (out of field) in W = Q(sqrt2,sqrt3,sqrt7)
# --------------------------------------------------------------------------- #
def _demo() -> None:
    G_K = [[4, 0, 0, 0], [0, 8, 0, 0], [0, 0, 12, 0], [0, 0, 0, 24]]   # Q(sqrt2,sqrt3), det 9216
    G_L = [[2, 0], [0, 14]]                                            # Q(sqrt7), det 28
    W = WorkingField.from_two_factors(G_K, G_L)                        # W = Q(sqrt2,sqrt3,sqrt7), deg 8
    print(f"W: degree {W.degree}, captured sub-field K degree {W.subfield_degree}")
    print("G_W diagonal =", [str(W.gram[i][i]) for i in range(W.degree)])  # 8,56,16,112,24,168,48,336
    # product basis e_i (x) f_j, flat index i*2 + j ; K = {i*2} = {0,2,4,6} = {1, sqrt2, sqrt3, sqrt6}
    cases = [("sqrt6 = e3(x)f0  (in K)", _unit(6, 8)),
             ("sqrt7 = e0(x)f1  (OUT of field)", _unit(1, 8)),
             ("sqrt14 = e1(x)f1 (OUT of field)", _unit(3, 8)),
             ("2*sqrt2 + 5*sqrt7 (mixed)", [Frac(0), Frac(5), Frac(2), Frac(0), Frac(0), Frac(0), Frac(0), Frac(0)])]
    for name, v in cases:
        d = W.detect(v)
        print(f"  {name}: field_residual_norm={d.field_residual_norm}  in_field={d.in_field}  "
              f"extension_flagged={d.extension_flagged}  residual={[str(c) for c in d.field_residual]}")


if __name__ == "__main__":
    _demo()
