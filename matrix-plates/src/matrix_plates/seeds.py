"""The algebraic-number seed registry.

Each seed names an algebraic integer by its *monic integer minimal polynomial*
(coefficients high -> low). The companion of that polynomial has the named value
and its Galois conjugates as eigenvalues — the foundation every binary operator
builds on. Only monic integer polynomials are admitted: the non-monic ZFP values
(``4x**2 - 3``, ``9x**2 - 9x + 1``, ...) are excluded on purpose because they are
not algebraic integers, and admitting them would break the integer-matrix
invariant downstream.

The nine entries reproduce the registry in ``matrix_plates.html`` verbatim,
including glyphs and field labels, so plate names match across tools.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Seed:
    """A named algebraic integer.

    Attributes
    ----------
    id:    short registry key (e.g. ``"phi"``).
    glyph: display glyph (e.g. ``"φ"``).
    field: number field label (e.g. ``"ℚ(√5)"``).
    poly:  monic integer minimal polynomial, coefficients **high -> low**.
    note:  human-readable provenance note.
    """

    id: str
    glyph: str
    field: str
    poly: List[int]
    note: str

    @property
    def degree(self) -> int:
        return len(self.poly) - 1

    def signature(self) -> str:
        """Comma-joined coefficient string — the dedupe key used by the closure."""
        return ",".join(str(c) for c in self.poly)


SEEDS: List[Seed] = [
    Seed("phi",  "φ",    "ℚ(√5)", [1, -1, -1],
         "Fibonacci Q-matrix — its powers list the Fibonacci numbers."),
    Seed("tau",  "τ",    "ℚ(√5)", [1, 1, -1],
         "reciprocal golden root, x²+x−1."),
    Seed("sq2",  "√2",   "ℚ(√2)", [1, 0, -2],
         "binary axis."),
    Seed("sq3",  "√3",   "ℚ(√3)", [1, 0, -3],
         "hexagonal axis."),
    Seed("sq5",  "√5",   "ℚ(√5)", [1, 0, -5],
         "golden discriminant."),
    Seed("gap",  "φ⁻⁴",  "ℚ(√5)", [1, -7, 1],
         "golden gap; conjugate is φ⁴ (x²−7x+1)."),
    Seed("K",    "K",    "ℚ(5¼)", [1, 0, 5, 0, -5],
         "quartic coherence; spectrum ±K real, ±iβ imaginary."),
    Seed("cons", "◇",    "ℚ(5¼)", [1, -6, 26, -16, -4],
         "consolidation quartic."),
    Seed("res",  "◆",    "ℚ(5¼)", [1, 2, 39, -52, 11],
         "resonance quartic."),
]


def base_registry() -> Dict[str, Seed]:
    """A fresh mutable ``id -> Seed`` map seeded with the nine built-ins.

    The closure (:mod:`matrix_plates.closure`) extends a copy of this with
    generated ``p̂_k`` seeds, so callers that want isolation get their own dict.
    """
    return {s.id: s for s in SEEDS}


# Convenience read-only view of the built-ins (do not mutate).
SEED_BY_ID: Dict[str, Seed] = {s.id: s for s in SEEDS}
