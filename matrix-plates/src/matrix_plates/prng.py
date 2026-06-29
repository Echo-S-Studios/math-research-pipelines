"""Reproducible pseudo-randomness: a bit-exact port of the tool's ``mulberry32``.

This is the one stochastic source in the whole system, and reproducibility
*across tools* depends on it matching the JavaScript generator exactly. The port
reproduces every 32-bit truncation (``| 0``, ``>>> 0``, ``Math.imul``) and the
operator-precedence subtlety in the second mixing step (``(t + imul(...)) ^ t``,
where the ``+`` is a full-width add coerced back to 32 bits *before* the XOR).

The regression test ``tests/test_prng.py`` pins the first eight outputs for
seeds 42 and 7 against ``tests/fixtures/ground_truth_js.json``, captured by
running the reference engine under Node — so any drift from the JS generator is
caught immediately.
"""

from __future__ import annotations

import math
from typing import Callable, List

from .linalg import Matrix

_U32 = 0xFFFFFFFF


def _imul(x: int, y: int) -> int:
    """C-style 32-bit multiply, the semantics of JS ``Math.imul``."""
    return ((x & _U32) * (y & _U32)) & _U32


def mulberry32(seed: int) -> Callable[[], float]:
    """Return a deterministic generator of floats in ``[0, 1)``.

    Bit-for-bit identical to the tool's ``mulberry32(seed)``. The closure holds
    the 32-bit state ``a`` and advances it on each call.
    """
    a = seed & _U32

    def nxt() -> float:
        nonlocal a
        a = (a + 0x6D2B79F5) & _U32
        t = _imul(a ^ (a >> 15), 1 | a) & _U32
        t = (((t + _imul(t ^ (t >> 7), 61 | t)) & _U32) ^ t) & _U32
        return ((t ^ (t >> 14)) & _U32) / 4294967296.0

    return nxt


def rand_int_matrix(n: int, seed: int) -> Matrix:
    """Seeded ``n x n`` integer matrix with entries in ``[-3, 3]``.

    Matches the tool's ``randIntMat``: ``floor(rnd() * 7) - 3`` row-major. This
    is the control family against which the structured Mahler grading is read.
    ``O(n**2)``.
    """
    rnd = mulberry32(seed)
    return [[math.floor(rnd() * 7) - 3 for _ in range(n)] for _ in range(n)]


def sample(seed: int, count: int) -> List[float]:
    """First *count* outputs of ``mulberry32(seed)`` — convenience for testing."""
    rnd = mulberry32(seed)
    return [rnd() for _ in range(count)]
