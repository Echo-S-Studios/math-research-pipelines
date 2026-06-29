"""Spectrum: complex roots of the characteristic polynomial, plus the derived
quantities the tool plots and grades by.

The *exact* invariants (``det``, ``tr``, char-poly coefficients) come from
:mod:`matrix_plates.linalg`. This module is the only one that uses floating
point, and only for quantities that are inherently transcendental to display:
the eigenvalue *positions* and the Mahler measure / spectral radius read off
them.

Root accuracy caveat (carried from the guide): Durand–Kerner converges slowly
near multiple roots — e.g. ``(x**2 - x - 1)**2`` from a derogatory lift. The
plotted points may smear; trust the integer chips for anything quantitative.

Reference: Durand–Kerner / Weierstrass simultaneous iteration. Householder,
*The Theory of Matrices in Numerical Analysis*; the Mahler-measure formula
``M(p) = |a_n| * prod max(1, |lambda_i|)`` and its reading as the entropy of the
associated Z-action are due to Lind, Schmidt & Ward, *Invent. Math.* 101 (1990).
"""

from __future__ import annotations

import cmath
import math
from typing import List, Sequence, Tuple


def dk_roots(coeffs: Sequence[float], iters: int = 240, tol: float = 1e-13) -> List[complex]:
    """Roots of a polynomial given **high -> low** coefficients.

    Faithful port of the tool's ``dkRoots``: spread initial guesses on a circle
    of radius ``0.6 * (1 + max|a_i|)`` rotated by ``0.37`` rad to avoid landing a
    guess exactly on a real root, then iterate the Weierstrass correction until
    the max step falls below *tol* (or *iters* is reached). ``O(n**2)`` per step.
    """
    n = len(coeffs) - 1
    if n <= 0:
        return []

    def P(z: complex) -> complex:
        r = complex(coeffs[0], 0.0)
        for i in range(1, n + 1):
            r = r * z + coeffs[i]
        return r

    R = 1.0
    for i in range(1, n + 1):
        R = max(R, abs(coeffs[i]))
    R = 1.0 + R
    z: List[complex] = []
    for k in range(n):
        a = 2 * math.pi * k / n + 0.37
        z.append(complex(0.6 * R * math.cos(a), 0.6 * R * math.sin(a)))

    for _ in range(iters):
        md = 0.0
        for i in range(n):
            den = complex(coeffs[0], 0.0)
            for j in range(n):
                if j != i:
                    den *= (z[i] - z[j])
            if den == 0:
                den = complex(1e-18, 0.0)
            corr = P(z[i]) / den
            z[i] -= corr
            md = max(md, abs(corr))
        if md < tol:
            break
    return z


def spectral_radius(roots: Sequence[complex]) -> float:
    """``rho`` = the largest eigenvalue magnitude. ``O(n)``."""
    return max((abs(z) for z in roots), default=0.0)


def mahler_from_roots(roots: Sequence[complex], lead: float = 1.0) -> float:
    """Mahler measure ``|lead| * prod_{|z|>1} |z|``.

    For a monic char-poly ``lead == 1`` and this is the product of eigenvalue
    magnitudes strictly outside the unit circle (the *Mahler horizon*). ``O(n)``.
    """
    m = abs(lead) if lead else 1.0
    for z in roots:
        m *= max(1.0, abs(z))
    return m


def classify_unit_circle(roots: Sequence[complex],
                         eps: float = 1e-4) -> Tuple[int, int, int]:
    """Count eigenvalues ``(outside, on, inside)`` the unit circle.

    Matches the tool's thresholds (``> 1.0001`` outside, ``< 0.9999`` inside,
    else on). The 'on' count is the part that contributes 1 to the Mahler
    measure; the 'outside' count is what makes it exceed 1.
    """
    outside = inside = on = 0
    for z in roots:
        r = abs(z)
        if r > 1.0 + eps:
            outside += 1
        elif r < 1.0 - eps:
            inside += 1
        else:
            on += 1
    return outside, on, inside
