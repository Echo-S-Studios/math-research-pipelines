"""Rational canonical form and the similarity invariant.

Two matrices over ``ℚ`` are **similar iff they have the same invariant factors**
(equivalently, the same rational canonical form). The characteristic polynomial
alone is a complete similarity invariant *only* for non-derogatory matrices; the
minimal polynomial is just the *largest* invariant factor. The full list is the
complete invariant, computed here exactly via the **Smith normal form of
``xI − A`` over ``ℚ[x]``** (a PID), whose non-unit diagonal entries are the
invariant factors of ``A``.

Cross-checked against an independent sympy determinantal-divisor oracle in
``tests/test_canonical.py``.

Reference: Dummit & Foote, *Abstract Algebra*, §12.2 (rational canonical form,
invariant factors as the Smith form of ``xI − A``); Gantmacher, vol. 1.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Sequence, Tuple

from .linalg import Matrix
from .operators import companion, dsum
from .polynomial import Poly


def _xI_minus_A(A: Matrix) -> List[List[Poly]]:
    n = len(A)
    out: List[List[Poly]] = []
    for i in range(n):
        row: List[Poly] = []
        for j in range(n):
            # entry = (x if i==j else 0) - A[i][j]
            base = Poly([-A[i][j], 1]) if i == j else Poly([-A[i][j]])
            row.append(base)
        out.append(row)
    return out


def _smith_diagonal(M: List[List[Poly]]) -> List[Poly]:
    """Smith normal form diagonal of a square polynomial matrix over ``ℚ[x]``.

    Unimodular row/column operations only (swaps, add poly-multiples, scale by a
    nonzero constant), so the diagonal entries are the invariant factors of the
    presented module. ``O(n³)`` polynomial operations for our small ``n``.
    """
    n = len(M)
    M = [[p for p in row] for row in M]  # local copy
    for t in range(n):
        while True:
            # pivot = a minimal-degree nonzero entry in the trailing submatrix
            piv = None
            pdeg = None
            for i in range(t, n):
                for j in range(t, n):
                    if not M[i][j].is_zero and (pdeg is None or M[i][j].degree < pdeg):
                        pdeg = M[i][j].degree
                        piv = (i, j)
            if piv is None:
                break  # trailing block is all zero
            pi, pj = piv
            if pi != t:
                M[t], M[pi] = M[pi], M[t]                       # row swap
            if pj != t:
                for r in range(n):
                    M[r][t], M[r][pj] = M[r][pj], M[r][t]       # column swap
            changed = False
            # clear column t (row operations)
            for i in range(n):
                if i == t or M[i][t].is_zero:
                    continue
                q, _ = M[i][t].divmod(M[t][t])
                M[i] = [M[i][k] - q * M[t][k] for k in range(n)]
                if not M[i][t].is_zero:
                    changed = True
            # clear row t (column operations)
            for j in range(n):
                if j == t or M[t][j].is_zero:
                    continue
                q, _ = M[t][j].divmod(M[t][t])
                for i in range(n):
                    M[i][j] = M[i][j] - q * M[i][t]
                if not M[t][j].is_zero:
                    changed = True
            if changed:
                continue  # a smaller-degree entry appeared; re-pivot
            # enforce divisibility: pivot must divide every trailing entry
            bad = None
            for i in range(t + 1, n):
                for j in range(t + 1, n):
                    if not M[i][j].is_zero and not (M[i][j] % M[t][t]).is_zero:
                        bad = i
                        break
                if bad is not None:
                    break
            if bad is not None:
                M[t] = [M[t][k] + M[bad][k] for k in range(n)]  # pull a non-divisible entry into row t
                continue
            break
        if not M[t][t].is_zero:                                 # normalize pivot to monic (unit scale)
            inv = Fraction(1) / M[t][t].leading
            M[t] = [M[t][k].scale(inv) for k in range(n)]
    return [M[i][i] for i in range(n)]


def invariant_factors(A: Matrix) -> List[List[int]]:
    """Invariant factors of *A* as monic integer polynomials (**high → low**).

    The list ``[f₁, …, f_k]`` satisfies ``f₁ | f₂ | … | f_k`` with
    ``∏ fᵢ = charpoly(A)`` and ``f_k = minpoly(A)``. ``k = 1`` iff *A* is
    non-derogatory. For an integer matrix the factors have integer coefficients.

    The non-derogatory case is detected first via the (fast, low-swell) minimal
    polynomial and returns ``[charpoly]`` directly. This is essential for
    performance: Smith elimination over ``ℚ[x]`` suffers catastrophic
    intermediate coefficient swell on *generic* matrices (which are
    non-derogatory) — the answer is a single tiny polynomial, but the
    intermediates explode. Smith form is therefore run only for *derogatory*
    matrices, which are structured and keep small coefficients.
    """
    n = len(A)
    if n == 0:
        return []
    from .linalg import char_poly as _cp, min_poly as _mp
    cp = _cp(A)[0]
    mp = _mp(A)
    if (len(mp) - 1) == n:                 # non-derogatory ⇒ one factor = charpoly
        return [list(cp)]
    diag = _smith_diagonal(_xI_minus_A(A))
    facs = [p.monic() for p in diag if p.degree >= 1]
    out: List[List[int]] = []
    for f in facs:
        coeffs = f.to_high_low()
        out.append([int(c) for c in coeffs])  # integer for an integer matrix
    return out


def similarity_key(A: Matrix) -> Tuple[Tuple[int, ...], ...]:
    """A hashable complete similarity invariant: the tuple of invariant factors.

    ``similarity_key(A) == similarity_key(B)``  ⇔  *A* and *B* are similar.
    """
    return tuple(tuple(f) for f in invariant_factors(A))


def is_similar(A: Matrix, B: Matrix) -> bool:
    """Exact similarity test over ``ℚ`` via equality of invariant factors."""
    if len(A) != len(B):
        return False
    return similarity_key(A) == similarity_key(B)


def rational_canonical_form(A: Matrix) -> Matrix:
    """The rational canonical form of *A*: ``⊕`` of companions of its invariant factors.

    Two matrices are similar iff their rational canonical forms are equal, so this
    is a canonical representative of the similarity class.
    """
    facs = invariant_factors(A)
    if not facs:
        return [row[:] for row in A]
    block = companion(facs[0])
    for f in facs[1:]:
        block = dsum(block, companion(f))
    return block
