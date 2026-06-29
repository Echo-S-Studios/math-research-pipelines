"""holding.py -- the EXACT-Fraction core carrier for kira-language (decision (d), the B1 hard gate).

Cl(2,0) is a RATIONAL algebra: +, -, *, conj, rev, M, nu, R_K, tr, det, disc, rank, TYPE, MASS all
stay in Q on rational input. This module is the exact carrier + exact (rational) readings, PURE STDLIB
(fractions only -- NO numpy, NO float), so synonymy (X==Y), nu=0, R_K=0, det=0 and the type lattice are
decided EXACTLY (zero tolerance) -- the G8 discipline L00M's substrate requires.

HARD RULE (decision (d)): no float from a transcendental reading (spectrum / entropy / purity / Mahler /
polar sqrt / exp) lives here. Those stay in the float layer (semantic_kernel.py), quarantined behind
declared tolerances, and NEVER cross into an exact decision. THIS module is what may wire live into L00M.

Convention matches semantic_kernel / KL_DTA exactly:
    basis {1, e1, e2, i=e1*e2},  e1^2 = e2^2 = 1,  i^2 = -1
    mat(X) = [[a+c, b-d],[b+d, a-c]]   (the shared mat/cl iso)

Inputs: ints / strings ("1/2", "0.5", "3") give EXACT rationals; a float is taken at its decimal repr
(Fraction(str(x)) -- the documented boundary, mirroring vector_api._fr). Pass strings for true exactness.
"""
from __future__ import annotations

from fractions import Fraction
from typing import List, Tuple, Union

Number = Union[int, str, Fraction, float]


def _q(x) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, float):
        return Fraction(str(x))          # decimal-faithful boundary (documented)
    return Fraction(x)                   # int, or str like "1/2" / "0.5" / "3"


class H:
    """An exact holding X = a*1 + b*e1 + c*e2 + d*i in Cl(2,0), coordinates in Q."""

    __slots__ = ("a", "b", "c", "d")

    def __init__(self, a: Number = 0, b: Number = 0, c: Number = 0, d: Number = 0) -> None:
        self.a, self.b, self.c, self.d = _q(a), _q(b), _q(c), _q(d)

    def __iter__(self):
        return iter((self.a, self.b, self.c, self.d))

    def __getitem__(self, i: int) -> Fraction:
        return (self.a, self.b, self.c, self.d)[i]

    def __eq__(self, o) -> bool:
        return isinstance(o, H) and (self.a, self.b, self.c, self.d) == (o.a, o.b, o.c, o.d)

    def __ne__(self, o) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash((self.a, self.b, self.c, self.d))

    def __add__(self, o: "H") -> "H":
        return H(self.a + o.a, self.b + o.b, self.c + o.c, self.d + o.d)

    def __sub__(self, o: "H") -> "H":
        return H(self.a - o.a, self.b - o.b, self.c - o.c, self.d - o.d)

    def __neg__(self) -> "H":
        return H(-self.a, -self.b, -self.c, -self.d)

    def __mul__(self, o):
        if isinstance(o, (int, Fraction)):                      # exact scalar only (no float)
            return H(self.a * o, self.b * o, self.c * o, self.d * o)
        if not isinstance(o, H):
            return NotImplemented
        A, B, C, D = self.a, self.b, self.c, self.d
        E, F, G, Hh = o.a, o.b, o.c, o.d
        return H(
            A * E + B * F + C * G - D * Hh,
            A * F + B * E - C * Hh + D * G,
            A * G + B * Hh + C * E - D * F,
            A * Hh + B * G - C * F + D * E,
        )

    def __rmul__(self, o):
        if isinstance(o, (int, Fraction)):
            return self * o
        return NotImplemented

    def __repr__(self) -> str:
        return f"H({self.a}, {self.b}, {self.c}, {self.d})"

    @property
    def coords(self) -> Tuple[Fraction, Fraction, Fraction, Fraction]:
        return (self.a, self.b, self.c, self.d)

    def as_strings(self) -> List[str]:
        return [str(self.a), str(self.b), str(self.c), str(self.d)]

    def max_abs(self) -> Fraction:
        return max(abs(self.a), abs(self.b), abs(self.c), abs(self.d))


VOID = H(0, 0, 0, 0)
ONE = H(1, 0, 0, 0)
E1 = H(0, 1, 0, 0)
E2 = H(0, 0, 1, 0)
I = H(0, 0, 0, 1)
P0 = H(Fraction(1, 2), 0, Fraction(1, 2), 0)


# --- the exact (rational) readings ----------------------------------------- #
def mat(X: H) -> List[List[Fraction]]:
    return [[X.a + X.c, X.b - X.d], [X.b + X.d, X.a - X.c]]


def cl(m) -> H:
    p, q = m[0][0], m[0][1]
    r, s = m[1][0], m[1][1]
    return H((p + s) / 2, (q + r) / 2, (p - s) / 2, (r - q) / 2)


def tr(X: H) -> Fraction:
    return 2 * X.a


def conj(X: H) -> H:
    return H(X.a, -X.b, -X.c, -X.d)          # tr*1 - X


def rev(X: H) -> H:
    return H(X.a, X.b, X.c, -X.d)            # transpose (negate the i/grade-2 part)


def M(X: H) -> H:
    return rev(X) * X                         # the Gram / measurement X^T X


def tau(X: H) -> Fraction:
    return X.a                                # tr/2 = the scalar coordinate


def nu(X: H) -> H:
    return M(X) - X                           # idempotence-defect (zero <=> symmetric idempotent)


def R_K(X: H) -> H:
    return M(X) - ONE * tau(M(X))             # trace-free Gram (zero <=> conformal)


def det(X: H) -> Fraction:
    return X.a * X.a - X.b * X.b - X.c * X.c + X.d * X.d


def disc(X: H) -> Fraction:
    t = tr(X)
    return t * t - 4 * det(X)


def rank(X: H) -> int:
    if X == VOID:
        return 0
    if det(X) == 0:
        return 1
    return 2


def Phi(X: H, Y: H) -> H:
    return Y * Y - tr(X) * Y + det(X) * ONE    # characteristic polynomial; Phi_X(X)=0 (Cayley-Hamilton)


# --- the type lattice (which laws vanish EXACTLY) -------------------------- #
def law_idem(X: H) -> H:
    return X * X - X


def law_rest(X: H) -> H:
    return nu(X)


def law_metric(X: H) -> H:
    return X * X - ONE


def law_flow(X: H) -> H:
    return rev(X) + X


def law_gen(X: H) -> H:
    return X * X - X - ONE


LAWS = [("idem", law_idem), ("rest", law_rest), ("metric", law_metric),
        ("flow", law_flow), ("gen", law_gen)]


def TYPE(X: H) -> List[str]:
    sig = [k for k, fn in LAWS if fn(X) == VOID]
    return sig if sig else ["free"]


def MASS(X: H) -> int:
    return sum(1 for _, fn in LAWS if fn(X) == VOID)


def is_gate(X: H) -> bool:
    return nu(X) == VOID                       # M(X)=X <=> symmetric idempotent


def residual_height(X: H) -> int:
    if X == VOID:
        return 0
    if R_K(X) == VOID:
        return 1
    if R_K(R_K(X)) == VOID:                     # R_K^2 = 0 always -> height <= 2
        return 2
    return 3
