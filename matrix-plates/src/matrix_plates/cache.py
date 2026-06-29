"""Memoization for the expensive exact invariants.

Repeated operations on the same matrix (re-analysing, lifting then comparing,
grouping a gallery into similarity classes) recompute the characteristic and
minimal polynomials and the invariant factors. Those are ``O(n⁴)`` each, so we
cache them keyed by a frozen (tuple-of-tuples) view of the matrix.

The caches are process-global and bounded (LRU). Use :func:`clear_caches` between
unrelated workloads and :func:`cache_info` to inspect hit rates.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, List, Tuple

from . import canonical as _canon
from .linalg import Matrix
from .linalg import char_poly as _char_poly
from .linalg import min_poly as _min_poly

FrozenMatrix = Tuple[Tuple[int, ...], ...]


def freeze(M: Matrix) -> FrozenMatrix:
    """A hashable, immutable view of an integer matrix."""
    return tuple(tuple(int(x) for x in row) for row in M)


def _thaw(key: FrozenMatrix) -> Matrix:
    return [list(row) for row in key]


@lru_cache(maxsize=8192)
def _char_poly_key(key: FrozenMatrix) -> Tuple[Tuple[int, ...], int]:
    coeffs, det = _char_poly(_thaw(key))
    return tuple(coeffs), det


@lru_cache(maxsize=8192)
def _min_poly_key(key: FrozenMatrix) -> Tuple[int, ...]:
    return tuple(_min_poly(_thaw(key)))


@lru_cache(maxsize=8192)
def _inv_factors_key(key: FrozenMatrix) -> Tuple[Tuple[int, ...], ...]:
    return tuple(tuple(f) for f in _canon.invariant_factors(_thaw(key)))


def char_poly(M: Matrix) -> Tuple[List[int], int]:
    """Cached characteristic polynomial (**high → low**) and determinant."""
    coeffs, det = _char_poly_key(freeze(M))
    return list(coeffs), det


def min_poly(M: Matrix) -> List[int]:
    """Cached minimal polynomial (**high → low**)."""
    return list(_min_poly_key(freeze(M)))


def invariant_factors(M: Matrix) -> List[List[int]]:
    """Cached invariant factors (each monic integer, **high → low**)."""
    return [list(f) for f in _inv_factors_key(freeze(M))]


def cache_info() -> Dict[str, str]:
    """Hit/miss/size for each cache (as ``functools`` reprs)."""
    return {
        "char_poly": str(_char_poly_key.cache_info()),
        "min_poly": str(_min_poly_key.cache_info()),
        "invariant_factors": str(_inv_factors_key.cache_info()),
    }


def clear_caches() -> None:
    """Drop all memoized results."""
    _char_poly_key.cache_clear()
    _min_poly_key.cache_clear()
    _inv_factors_key.cache_clear()
