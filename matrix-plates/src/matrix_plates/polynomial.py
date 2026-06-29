"""Exact univariate polynomials over the rationals.

A small ``Poly`` type backing the invariant-factor / rational-canonical-form
machinery in :mod:`matrix_plates.canonical`. Coefficients are
:class:`fractions.Fraction`, stored low-to-high (index = power), trailing zeros
trimmed, so every operation is exact. The rest of the codebase represents
polynomials as **high → low** integer lists (e.g. char-poly coefficients); use
:meth:`Poly.from_high_low` / :meth:`to_high_low` to bridge.

``ℚ[x]`` is a Euclidean domain, so it has long division and gcd — exactly what
Smith normal form over a PID requires.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Sequence, Tuple, Union

Number = Union[int, Fraction]


class Poly:
    """An exact polynomial over ``ℚ``, coefficients stored low → high."""

    __slots__ = ("c",)

    def __init__(self, coeffs: Sequence[Number]) -> None:
        c = [Fraction(x) for x in coeffs]
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        if not c:
            c = [Fraction(0)]
        self.c: List[Fraction] = c

    # --- constructors ---
    @classmethod
    def zero(cls) -> "Poly":
        return cls([0])

    @classmethod
    def one(cls) -> "Poly":
        return cls([1])

    @classmethod
    def x(cls) -> "Poly":
        return cls([0, 1])

    @classmethod
    def from_high_low(cls, coeffs: Sequence[Number]) -> "Poly":
        """Build from coefficients given **high → low** (the codebase convention)."""
        return cls(list(reversed(list(coeffs))))

    # --- introspection ---
    @property
    def degree(self) -> int:
        return len(self.c) - 1 if not self.is_zero else -1

    @property
    def is_zero(self) -> bool:
        return len(self.c) == 1 and self.c[0] == 0

    @property
    def leading(self) -> Fraction:
        return self.c[-1]

    @property
    def is_constant(self) -> bool:
        return self.degree <= 0

    def is_monic(self) -> bool:
        return (not self.is_zero) and self.leading == 1

    def to_high_low(self) -> List[Number]:
        """Coefficients **high → low**; ints where exact, else Fractions."""
        out: List[Number] = []
        for v in reversed(self.c):
            out.append(int(v) if v.denominator == 1 else v)
        return out

    # --- arithmetic ---
    def __add__(self, o: "Poly") -> "Poly":
        n = max(len(self.c), len(o.c))
        a = self.c + [Fraction(0)] * (n - len(self.c))
        b = o.c + [Fraction(0)] * (n - len(o.c))
        return Poly([a[i] + b[i] for i in range(n)])

    def __sub__(self, o: "Poly") -> "Poly":
        n = max(len(self.c), len(o.c))
        a = self.c + [Fraction(0)] * (n - len(self.c))
        b = o.c + [Fraction(0)] * (n - len(o.c))
        return Poly([a[i] - b[i] for i in range(n)])

    def __neg__(self) -> "Poly":
        return Poly([-v for v in self.c])

    def __mul__(self, o: Union["Poly", Number]) -> "Poly":
        if isinstance(o, (int, Fraction)):
            return Poly([v * Fraction(o) for v in self.c])
        out = [Fraction(0)] * (len(self.c) + len(o.c) - 1)
        for i, ai in enumerate(self.c):
            if ai == 0:
                continue
            for j, bj in enumerate(o.c):
                out[i + j] += ai * bj
        return Poly(out)

    __rmul__ = __mul__

    def scale(self, k: Number) -> "Poly":
        return Poly([v * Fraction(k) for v in self.c])

    def divmod(self, o: "Poly") -> Tuple["Poly", "Poly"]:
        """Polynomial long division → ``(quotient, remainder)`` over ``ℚ``."""
        if o.is_zero:
            raise ZeroDivisionError("polynomial division by zero")
        r = Poly(self.c)
        q = Poly.zero()
        while (not r.is_zero) and r.degree >= o.degree:
            shift = r.degree - o.degree
            coef = r.leading / o.leading
            term = Poly([Fraction(0)] * shift + [coef])
            q = q + term
            r = r - term * o
        return q, r

    def __mod__(self, o: "Poly") -> "Poly":
        return self.divmod(o)[1]

    def __floordiv__(self, o: "Poly") -> "Poly":
        return self.divmod(o)[0]

    def monic(self) -> "Poly":
        """Return ``self`` scaled to leading coefficient 1 (zero stays zero)."""
        if self.is_zero:
            return Poly.zero()
        return Poly([v / self.leading for v in self.c])

    def gcd(self, o: "Poly") -> "Poly":
        """Monic gcd via the Euclidean algorithm in ``ℚ[x]``."""
        a, b = Poly(self.c), Poly(o.c)
        while not b.is_zero:
            a, b = b, a % b
        return a.monic()

    def deriv(self) -> "Poly":
        if self.degree <= 0:
            return Poly.zero()
        return Poly([self.c[i] * i for i in range(1, len(self.c))])

    def is_squarefree(self) -> bool:
        """True iff no repeated roots, i.e. ``gcd(p, p')`` is constant.

        A matrix is diagonalizable iff its minimal polynomial is squarefree, so
        this is the test behind the ``defective`` flag.
        """
        if self.degree <= 1:
            return True
        return self.gcd(self.deriv()).is_constant

    def eval(self, x: Number) -> Fraction:
        acc = Fraction(0)
        for v in reversed(self.c):
            acc = acc * Fraction(x) + v
        return acc

    # --- equality / hashing / display ---
    def __eq__(self, o: object) -> bool:
        return isinstance(o, Poly) and self.c == o.c

    def __hash__(self) -> int:
        return hash(tuple(self.c))

    def __repr__(self) -> str:
        from .text import poly_str
        return poly_str(self.to_high_low()) if all(
            v.denominator == 1 for v in self.c) else "Poly(" + repr(self.c) + ")"

    def latex(self, var: str = "x") -> str:
        """LaTeX string, e.g. ``x^{2} - x - 1``."""
        terms: List[str] = []
        for p in range(self.degree, -1, -1):
            a = self.c[p]
            if a == 0:
                continue
            mag = abs(a)
            coeff = "" if (mag == 1 and p > 0) else (
                str(mag) if mag.denominator == 1 else f"\\frac{{{mag.numerator}}}{{{mag.denominator}}}")
            if p == 0:
                body = coeff or "1"
            elif p == 1:
                body = coeff + var
            else:
                body = coeff + var + "^{" + str(p) + "}"
            terms.append(("- " if a < 0 else "+ ") + body)
        if not terms:
            return "0"
        s = " ".join(terms)
        return s[2:] if s.startswith("+ ") else "-" + s[2:]
