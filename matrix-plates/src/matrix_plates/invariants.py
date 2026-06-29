"""Per-matrix analysis — invariant chips, the minimal polynomial, the rational
canonical form, the matrix *house*, and structural flags.

:func:`analyse` reproduces every quantity the tool's ``analyse`` reports, routed
through the memoized exact kernels (:mod:`matrix_plates.cache`), and adds:

* **minimal polynomial** + ``derogatory`` (``deg(min) < deg(char)``);
* **invariant factors** (the complete similarity invariant) + ``similarity_key``;
* **house** ``⌈A⌉`` — the maximum eigenvalue modulus (Schinzel–Zassenhaus
  "house" of an algebraic integer; for a matrix it equals the spectral radius
  ``ρ``). House is a *max*; the Mahler measure is a *product* — two matrices can
  share one and differ in the other, so they give complementary insight;
* ``defective`` — not diagonalizable, i.e. the minimal polynomial is not
  squarefree (has a repeated root);
* Lehmer-gap flags: ``at_floor`` (``M = 1``, the Kronecker/cyclotomic floor) and
  ``in_lehmer_gap`` (``1 < M < L``, conjecturally empty).

Exactness boundary: ``coeffs``, ``det``, ``tr``, ``rank``, ``minpoly``,
``invariant_factors``, ``derogatory``, ``defective``, ``unimodular`` are
integer-exact. ``mahler``, ``house``/``rho``, ``frob`` and eigenvalue positions
are floating point.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from . import cache
from .linalg import Matrix, frobenius, is_integer_matrix, rank as exact_rank, trace
from .polynomial import Poly
from .roots import (classify_unit_circle, dk_roots, mahler_from_roots,
                    spectral_radius)

#: Smallest known Mahler measure > 1 (Lehmer 1933) — the single source of truth.
LEHMER = 1.17628


@dataclass
class Analysis:
    """The complete invariant bundle for one matrix."""

    M: Matrix
    n: int
    coeffs: List[int]                 # characteristic polynomial, high -> low (monic)
    det: int
    tr: int
    rank: int
    frob: float
    roots: List[complex] = field(repr=False, default_factory=list)
    mahler: float = 1.0
    rho: float = 0.0
    integer: bool = True
    unimodular: bool = False
    # --- minimal polynomial / similarity ---
    minpoly: List[int] = field(default_factory=lambda: [1])
    deg_char: int = 0
    deg_min: int = 0
    derogatory: bool = False
    defective: bool = False
    invariant_factors: List[List[int]] = field(default_factory=list)
    # --- spectrum classification relative to the unit circle ---
    outside: int = 0
    on: int = 0
    inside: int = 0

    @property
    def char_poly(self) -> List[int]:
        """Alias for :attr:`coeffs` (characteristic polynomial, high -> low)."""
        return self.coeffs

    @property
    def house(self) -> float:
        """The matrix house ``⌈A⌉`` = max eigenvalue modulus = spectral radius."""
        return self.rho

    @property
    def num_invariant_factors(self) -> int:
        return len(self.invariant_factors)

    @property
    def similarity_key(self) -> Tuple[Tuple[int, ...], ...]:
        """Hashable complete similarity invariant (equal ⇔ similar)."""
        return tuple(tuple(f) for f in self.invariant_factors)

    @property
    def at_floor(self) -> bool:
        """``M = 1`` — a Kronecker/cyclotomic plate (roots of unity / zero)."""
        return abs(self.mahler - 1.0) < 1e-9

    @property
    def in_lehmer_gap(self) -> bool:
        """``1 < M < L`` — the conjecturally empty Lehmer gap."""
        return (1.0 + 1e-9) < self.mahler < (LEHMER - 1e-9)

    def spectrum_split(self) -> Tuple[int, int, int]:
        return self.outside, self.on, self.inside


def analyse(M: Matrix) -> Analysis:
    """Compute the full invariant set for an integer matrix *M* (memoized kernels)."""
    n = len(M)
    coeffs, det = cache.char_poly(M)
    roots = dk_roots(coeffs)
    mahler = mahler_from_roots(roots, coeffs[0])
    rho = spectral_radius(roots)
    tr = trace(M)
    rnk = exact_rank(M)
    integer = is_integer_matrix(M)
    unimodular = integer and abs(det) == 1
    mp = cache.min_poly(M)
    invf = cache.invariant_factors(M)
    defective = not Poly.from_high_low(mp).is_squarefree()
    outside, on, inside = classify_unit_circle(roots)
    return Analysis(
        M=M, n=n, coeffs=coeffs, det=det, tr=tr, rank=rnk, frob=frobenius(M),
        roots=roots, mahler=mahler, rho=rho, integer=integer, unimodular=unimodular,
        minpoly=mp, deg_char=len(coeffs) - 1, deg_min=len(mp) - 1,
        derogatory=(len(mp) - 1) < (len(coeffs) - 1), defective=defective,
        invariant_factors=invf, outside=outside, on=on, inside=inside,
    )
