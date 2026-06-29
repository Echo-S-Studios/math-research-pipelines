"""Exact linear algebra over the integers and rationals.

Everything here is *exact*: matrices are lists of Python ``int`` (arbitrary
precision, so :func:`matpow` doubles as the guide's BigInt recipe for free), and
the only place rationals appear is :func:`min_poly`, where intermediate Gaussian
elimination needs division. No floating point is used for any quantity the tool
reports as a chip (``det``, ``tr``, char-poly coefficients, ``rank``); those are
integer-exact. Floating point enters only later, in :mod:`matrix_plates.roots`,
for *plotting* the spectrum.

Algorithms & references
-----------------------
* **Characteristic polynomial / determinant** — Faddeev–LeVerrier recurrence,
  which yields integer coefficients for an integer matrix in ``O(n**4)``.
  Householder, *The Theory of Matrices in Numerical Analysis* (1964).
* **Minimal polynomial** — exact-rational Krylov dependence: find the least
  ``m`` for which ``A**m`` is linearly dependent on ``{I, A, ..., A**(m-1)}`` in
  the ``n**2``-dimensional matrix space, reading the monic relation off the
  elimination. Horn & Johnson, *Matrix Analysis* 2e (2013), §3.3; Gantmacher,
  *The Theory of Matrices*, vol. 1.
* **Rank** — fraction-free... no: exact-rational Gaussian elimination, pivot
  count. Strang, *Introduction to Linear Algebra*.

Type alias: a ``Matrix`` is ``List[List[int]]`` (square unless noted).
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import List, Sequence, Tuple

Matrix = List[List[int]]


# --- primitives ----------------------------------------------------------------
def identity(n: int) -> Matrix:
    """The ``n x n`` identity. ``O(n**2)``."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def zeros(n: int) -> Matrix:
    """An ``n x n`` zero matrix. ``O(n**2)``."""
    return [[0] * n for _ in range(n)]


def clone(A: Matrix) -> Matrix:
    """A deep copy of *A*. ``O(n**2)``."""
    return [row[:] for row in A]


def trace(A: Matrix) -> int:
    """Sum of the diagonal. ``O(n)``."""
    return sum(A[i][i] for i in range(len(A)))


def transpose(A: Matrix) -> Matrix:
    """Matrix transpose. ``O(n*m)``."""
    return [list(col) for col in zip(*A)] if A else []


def matmul(A: Matrix, B: Matrix) -> Matrix:
    """Integer matrix product ``A @ B``. ``O(n*m*p)`` (skips zero multipliers)."""
    n, m, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(m):
            a = Ai[k]
            if a == 0:
                continue
            Bk = B[k]
            for j in range(p):
                Ci[j] += a * Bk[j]
    return C


def add_scaled_identity(A: Matrix, c: int) -> Matrix:
    """Return ``A + c*I`` (out of place). ``O(n**2)``."""
    B = clone(A)
    for i in range(len(B)):
        B[i][i] += c
    return B


def matpow(A: Matrix, k: int) -> Matrix:
    """``A**k`` by fast exponentiation, exact over Python big integers.

    ``O(n**3 * log k)``. This is the guide's ``matpow`` and, because Python ints
    are unbounded, also serves as its BigInt variant — terms never overflow.
    """
    if k < 0:
        raise ValueError("matpow requires k >= 0 (no inverse in integer ring)")
    R = identity(len(A))
    P = A
    while k > 0:
        if k & 1:
            R = matmul(R, P)
        P = matmul(P, P)
        k >>= 1
    return R


def apply(A: Matrix, v: Sequence[int]) -> List[int]:
    """Matrix-vector product ``A v``. ``O(n*m)``."""
    return [sum(a * v[j] for j, a in enumerate(row)) for row in A]


def frobenius(A: Matrix) -> float:
    """Frobenius norm ``sqrt(sum a_ij**2)``. ``O(n**2)``."""
    return math.sqrt(sum(x * x for row in A for x in row))


def is_integer_matrix(A: Sequence[Sequence[object]]) -> bool:
    """True iff every entry is (numerically) an integer. ``O(n**2)``."""
    for row in A:
        for x in row:
            if abs(float(x) - round(float(x))) > 1e-9:
                return False
    return True


# --- characteristic polynomial & determinant -----------------------------------
def char_poly(A: Matrix) -> Tuple[List[int], int]:
    """Characteristic polynomial (monic, **high -> low**) and determinant.

    Faddeev–LeVerrier. For an integer matrix every coefficient is an integer; the
    recurrence's division by ``k`` is exact and is asserted as a guard against an
    accidentally non-integer matrix. Returns ``(coeffs, det)`` with
    ``coeffs = [1, c1, ..., cn]`` and ``det = (-1)**n * cn``. ``O(n**4)``.
    """
    n = len(A)
    if n == 0:
        return [1], 1
    c: List[int] = []
    M = clone(A)
    for k in range(1, n + 1):
        if k > 1:
            M = matmul(A, add_scaled_identity(M, c[k - 2]))
        t = trace(M)
        if (-t) % k != 0:
            raise ValueError(
                "Faddeev-LeVerrier produced a non-integer coefficient at k=%d; "
                "char_poly requires an integer matrix." % k
            )
        c.append((-t) // k)
    coeffs = [1] + c
    det = ((-1) ** n) * coeffs[n]
    return coeffs, det


def determinant(A: Matrix) -> int:
    """Exact integer determinant (via :func:`char_poly`). ``O(n**4)``."""
    return char_poly(A)[1]


# --- exact rank -----------------------------------------------------------------
def rank(A: Matrix) -> int:
    """Exact rank via rational Gaussian elimination (pivot count). ``O(n**3)``.

    Uses :class:`fractions.Fraction`, so the result is exact for any integer
    matrix — unlike the tool's float elimination, which can misjudge rank on
    near-singular inputs. For integer matrices the two agree.
    """
    B = [[Fraction(x) for x in row] for row in A]
    n = len(B)
    m = len(B[0]) if n else 0
    r = 0
    row = 0
    for col in range(m):
        if row >= n:
            break
        piv = next((rr for rr in range(row, n) if B[rr][col] != 0), None)
        if piv is None:
            continue
        B[row], B[piv] = B[piv], B[row]
        pv = B[row][col]
        for rr in range(n):
            if rr == row or B[rr][col] == 0:
                continue
            f = B[rr][col] / pv
            B[rr] = [B[rr][cc] - f * B[row][cc] for cc in range(m)]
        row += 1
        r += 1
    return r


# --- minimal polynomial (the Goal-2 workhorse) ----------------------------------
def min_poly(A: Matrix) -> List[int]:
    """Exact minimal polynomial (monic, **high -> low**) of an integer matrix.

    Method (exact, rational Krylov). The minimal polynomial is the least-degree
    monic ``p`` with ``p(A) = 0``. Flatten the matrix powers ``I, A, A**2, ...``
    into vectors of ``Q**(n**2)`` and find the first power that is linearly
    dependent on the earlier ones; the monic dependence *is* the minimal
    polynomial. Bookkeeping the elimination in the polynomial basis recovers the
    coefficients directly, with leading coefficient exactly ``1``.

    The minimal polynomial of an integer matrix has integer coefficients (it
    divides the monic integer characteristic polynomial in ``Q[x]``; Gauss's
    lemma), so the returned coefficients are integers — asserted below.

    Cost: at most ``n+1`` powers and ``O(n)`` reductions of length-``n**2``
    vectors, i.e. ``O(n**4)`` rational operations. The degree of the result is
    ``len(...) - 1``; a *derogatory* matrix has ``deg(min) < deg(char) == n``.

    Reference: Horn & Johnson, *Matrix Analysis* 2e (2013), §3.3.
    """
    n = len(A)
    if n == 0:
        return [1]
    # basis rows after elimination: (reduced_vector, pivot_index, poly_coeffs_low_to_high)
    basis: List[Tuple[List[Fraction], int, List[Fraction]]] = []
    P = identity(n)
    for k in range(n + 1):
        vec: List[Fraction] = [Fraction(x) for r in P for x in r]
        coeffs: List[Fraction] = [Fraction(0)] * (k + 1)
        coeffs[k] = Fraction(1)  # this row currently equals 1 * A**k
        for bvec, piv, bc in basis:
            if vec[piv] != 0:
                f = vec[piv] / bvec[piv]
                vec = [vec[i] - f * bvec[i] for i in range(len(vec))]
                L = max(len(coeffs), len(bc))
                cc = coeffs + [Fraction(0)] * (L - len(coeffs))
                bb = bc + [Fraction(0)] * (L - len(bc))
                coeffs = [cc[i] - f * bb[i] for i in range(L)]
        piv = next((i for i, v in enumerate(vec) if v != 0), None)
        if piv is None:
            # vec reduced to 0  =>  sum_i coeffs[i] * A**i = 0, with coeffs[k] == 1.
            hi_to_lo = list(reversed(coeffs))
            result = []
            for c in hi_to_lo:
                if c.denominator != 1:
                    raise ValueError("non-integer minimal-polynomial coefficient "
                                     "(input is not an integer matrix)")
                result.append(int(c))
            return result
        nrm = vec[piv]
        vec = [v / nrm for v in vec]
        coeffs = [c / nrm for c in coeffs]
        basis.append((vec, piv, coeffs))
        P = matmul(A, P)
    # Unreachable for an n x n matrix: dependence is forced by degree n.
    return char_poly(A)[0]


# --- polynomial helpers ---------------------------------------------------------
def poly_mul(a: Sequence[int], b: Sequence[int]) -> List[int]:
    """Multiply two polynomials given **high -> low** coefficients. ``O(deg^2)``."""
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def poly_eq(a: Sequence[int], b: Sequence[int]) -> bool:
    """Structural equality of two coefficient lists (high -> low)."""
    return list(a) == list(b)
