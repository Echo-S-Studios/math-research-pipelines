"""number_field_factor.py -- P2c: the exact factorization primitive for the non-disjoint compositum.

Two exact, pure-stdlib services on monic-integer polynomials (HIGH->LOW, the package minpoly
convention, e.g. x^4-10x^2+1 = [1,0,-10,0,1]):

  factor_over_Q(min_poly)  -- factor a monic-integer polynomial into monic-integer irreducibles over Q,
                              by KRONECKER'S METHOD (exact: a degree-d factor is pinned by its values at
                              d+1 integer points, each of which must divide f at that point; interpolate
                              the finitely-many candidates over Q and trial-divide). Bounded: it only runs
                              up to KRONECKER_DEGREE_CAP (=12, comfortably covers the canonical-witness
                              degree-8 resultant and realistic seeds); above the cap it raises
                              FactorizationUnsupported rather than risk the combinatorial blow-up (the
                              Zassenhaus upgrade -- squarefree -> mod-p -> Hensel -> recombination -- is the
                              documented next step, NOT built here). A defensive candidate-count guard also
                              refuses pathological divisor explosions below the cap.

  is_irreducible_over_Q(min_poly)  -- convenience: len(factor_over_Q(.)) == 1 (with multiplicity 1).

Exact (Fraction/int, G8); monic-integer in/out (G10). Reuses the vendored Q[x] poly kernel in
invariant_factors.py (LOW->HIGH Fraction polys); converts at the boundary. Model-layer only: pure
stdlib + fractions; no KIRA / z / Plate-Matrices / numpy / sympy.
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction as F
from typing import List, Sequence, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from invariant_factors import deg, trim, pmul, pdivmod, monic, is_zero  # noqa: E402  (Q[x] kernel; LOW->HIGH)

# Kronecker is exact but combinatorial; bound it. Above the cap we REFUSE (never run unbounded).
KRONECKER_DEGREE_CAP = 12
# Defensive: refuse if the interpolation search would enumerate more than this many candidates at one degree.
_CANDIDATE_BUDGET = 200_000


class FactorizationUnsupported(Exception):
    """Raised when a polynomial's degree exceeds the Kronecker bound (or a defensive search budget):
    a Zassenhaus-grade factorizer is required. Carries a clean, actionable message."""


# --------------------------------------------------------------------------- #
# convention helpers: public API is HIGH->LOW int; the Q[x] kernel is LOW->HIGH Fraction
# --------------------------------------------------------------------------- #
def _to_low(min_poly: Sequence) -> List[F]:
    """HIGH->LOW int/Fraction  ->  LOW->HIGH Fraction (the invariant_factors kernel convention)."""
    hi = [F(c) for c in min_poly]
    return trim(hi[::-1])


def _to_high_int(p_low: Sequence[F]) -> List[int]:
    """LOW->HIGH Fraction (assumed monic-integer)  ->  HIGH->LOW int."""
    p = trim(list(p_low))
    hi = p[::-1]
    out = []
    for c in hi:
        if c.denominator != 1:
            raise ValueError("non-integer coefficient where a monic-integer factor was expected")
        out.append(int(c))
    return out


def _eval_low(p_low: Sequence[F], x: int) -> F:
    """Evaluate a LOW->HIGH polynomial at integer x (Horner)."""
    acc = F(0)
    for c in reversed(p_low):
        acc = acc * x + c
    return acc


def _divisors(n: int) -> List[int]:
    """All integer divisors of n (positive AND negative). n != 0."""
    n = abs(int(n))
    ds = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds) + [-d for d in sorted(ds)]


def _lagrange_low(points: Sequence[int], values: Sequence[F]) -> List[F]:
    """Exact Lagrange interpolation -> LOW->HIGH Fraction polynomial through (points[i], values[i])."""
    result: List[F] = [F(0)]
    for i, (xi, yi) in enumerate(zip(points, values)):
        # basis_i(x) = prod_{j!=i} (x - xj)/(xi - xj)
        num: List[F] = [F(1)]          # LOW->HIGH
        den = F(1)
        for j, xj in enumerate(points):
            if j == i:
                continue
            num = pmul(num, [F(-xj), F(1)])   # multiply by (x - xj)
            den *= (xi - xj)
        scale = yi / den
        term = [c * scale for c in num]
        result = trim([(result[t] if t < len(result) else F(0)) + (term[t] if t < len(term) else F(0))
                       for t in range(max(len(result), len(term)))])
    return trim(result)


def _exact_divides(f_low: Sequence[F], g_low: Sequence[F]) -> bool:
    """Does g divide f exactly over Q[x] (zero remainder)?"""
    if is_zero(g_low):
        return False
    _, r = pdivmod(list(f_low), list(g_low))
    return is_zero(r)


# --------------------------------------------------------------------------- #
# mod-p (Rabin) irreducibility PRE-CHECK: certifies an irreducible input fast, so Kronecker's
# combinatorial search runs only on genuinely reducible polynomials (the disjoint compositum's
# irreducible degree-m*k minpoly is dispatched here in milliseconds instead of seconds).
# --------------------------------------------------------------------------- #
def _fp_pmod(a: List[int], f: List[int], p: int) -> List[int]:
    """a mod f over F_p (f monic, LOW->HIGH). Returns the remainder (LOW->HIGH, trimmed)."""
    a = [c % p for c in a]
    df = len(f) - 1
    while len(a) - 1 >= df and any(a):
        da = len(a) - 1
        lead = a[da]
        if lead:
            for i in range(df + 1):
                a[da - df + i] = (a[da - df + i] - lead * f[i]) % p
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        if a == [0]:
            break
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _fp_pmulmod(a: List[int], b: List[int], f: List[int], p: int) -> List[int]:
    r = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca:
            for j, cb in enumerate(b):
                r[i + j] = (r[i + j] + ca * cb) % p
    return _fp_pmod(r, f, p)


def _fp_powmod(base: List[int], e: int, f: List[int], p: int) -> List[int]:
    """base^e mod f over F_p."""
    result = [1]
    b = _fp_pmod(base, f, p)
    while e > 0:
        if e & 1:
            result = _fp_pmulmod(result, b, f, p)
        e >>= 1
        if e:
            b = _fp_pmulmod(b, b, f, p)
    return result


def _fp_gcd(a: List[int], b: List[int], p: int) -> List[int]:
    a = [c % p for c in a]
    b = [c % p for c in b]
    while any(b):
        a, b = b, _fp_pmod(a, _fp_monic(b, p), p)
    return _fp_monic(a, p) if any(a) else [0]


def _fp_monic(a: List[int], p: int) -> List[int]:
    a = [c % p for c in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    if not any(a):
        return [0]
    inv = pow(a[-1], p - 2, p)
    return [(c * inv) % p for c in a]


def _prime_factors(n: int) -> List[int]:
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def _irreducible_mod_p(f_low: List[F], p: int):
    """Rabin irreducibility of f over F_p. Returns True/False, or None if f is not squarefree mod p
    (inconclusive at this p)."""
    f = [int(c) % p for c in f_low]
    while len(f) > 1 and f[-1] == 0:
        f.pop()
    n = len(f) - 1
    if n < 1 or f[-1] % p == 0:
        return None
    f = _fp_monic(f, p)
    fprime = [(i * f[i]) % p for i in range(1, len(f))] or [0]
    if deg(_fp_gcd(f, fprime, p)) >= 1:               # not squarefree mod p -> inconclusive
        return None
    x = [0, 1]
    for q in _prime_factors(n):
        h = _fp_powmod(x, p ** (n // q), f, p)         # x^(p^(n/q)) mod f
        h = [(h[i] - (x[i] if i < len(x) else 0)) % p for i in range(max(len(h), 2))]
        if deg(_fp_gcd(f, h, p)) >= 1:
            return False
    full = _fp_powmod(x, p ** n, f, p)                 # x^(p^n) == x  <=>  irreducible
    full = [(full[i] - (x[i] if i < len(x) else 0)) % p for i in range(max(len(full), 2))]
    while len(full) > 1 and full[-1] == 0:
        full.pop()
    return not any(full)


def _quick_irreducible(f_low: List[F]) -> bool:
    """Try small primes; True if any certifies f irreducible over Q (sufficient, not necessary)."""
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23):
        verdict = _irreducible_mod_p(f_low, p)
        if verdict is True:
            return True
    return False


def _find_one_factor(f_low: List[F]) -> List[F] | None:
    """Kronecker: search for ONE nontrivial monic factor of f (LOW->HIGH, monic, deg>=2 assumed).
    Returns a monic LOW->HIGH factor of degree in [1, deg(f)//2], or None if f is irreducible."""
    n = deg(f_low)
    if _quick_irreducible(f_low):                      # fast path: certified irreducible -> no search
        return None
    # gather a generous pool of sample points, then PREFER points with smallest |f| (fewest divisors,
    # so the Kronecker candidate product stays small -- critical for the multiquadratic irreducible case).
    pool: List[tuple] = []
    kk = 0
    while len(pool) < n + 1 + 12:
        for cand in ((kk, -kk) if kk else (0,)):
            v = _eval_low(f_low, cand)
            if v != 0:
                pool.append((abs(int(v)), len(_divisors(int(v))), cand, int(v)))
        kk += 1
        if kk > n + 80:
            break
    pool.sort(key=lambda t: (t[1], t[0]))              # fewest divisors first, then smallest |f|
    sel_pts = [t[2] for t in pool]
    sel_vals = [t[3] for t in pool]
    for d in range(1, n // 2 + 1):
        sub_pts = sel_pts[:d + 1]
        sub_vals = sel_vals[:d + 1]                  # f(point) integers (monic-int f), fewest-divisor points
        divisor_sets = [_divisors(v) for v in sub_vals]
        total = 1
        for ds in divisor_sets:
            total *= len(ds)
            if total > _CANDIDATE_BUDGET:
                raise FactorizationUnsupported(
                    f"Kronecker candidate search at degree {d} exceeds budget {_CANDIDATE_BUDGET}; "
                    "Zassenhaus upgrade required")
        # enumerate candidate value-vectors; the first coordinate may be taken positive (sign symmetry)
        from itertools import product
        for combo in product(*divisor_sets):
            if combo[0] < 0:           # g and -g are the same factor up to sign; fix the leading sample sign
                continue
            g = _lagrange_low(sub_pts, [F(c) for c in combo])
            if deg(g) != d:
                continue
            gm = monic(g)
            # monic-integer candidate only (Gauss: a monic-int f has monic-int factors)
            if any(c.denominator != 1 for c in gm):
                continue
            if _exact_divides(f_low, gm):
                return gm
    return None


def factor_over_Q(min_poly: Sequence) -> List[List[int]]:
    """Factor a monic-integer polynomial (HIGH->LOW) into monic-integer irreducibles over Q (with
    multiplicity), via bounded Kronecker. Returns a list of HIGH->LOW int factors whose product is
    min_poly. Raises FactorizationUnsupported if deg > KRONECKER_DEGREE_CAP.

    >>> factor_over_Q([1,0,-10,0,1])           # x^4-10x^2+1, irreducible over Q
    [[1, 0, -10, 0, 1]]
    >>> sorted(factor_over_Q([1,0,-25,0,91,0,-75]))   # (x^4-10x^2+1)?  no -- (deg6) = (deg4)(x^2-3)
    """
    f_low = _to_low(min_poly)
    n = deg(f_low)
    if n < 1:
        raise ValueError("min_poly must have degree >= 1")
    if n > KRONECKER_DEGREE_CAP:
        raise FactorizationUnsupported(
            f"factorization degree {n} exceeds Kronecker bound {KRONECKER_DEGREE_CAP}; "
            "Zassenhaus upgrade required")
    if monic(f_low) != f_low:
        # normalize to monic (the inputs are monic-int minpolys; this is belt-and-suspenders)
        f_low = monic(f_low)
    factors: List[List[int]] = []
    stack = [f_low]
    while stack:
        g = stack.pop()
        if deg(g) <= 1:
            factors.append(_to_high_int(g))
            continue
        h = _find_one_factor(g)
        if h is None:
            factors.append(_to_high_int(g))     # irreducible
        else:
            q, r = pdivmod(g, h)
            assert is_zero(r)
            stack.append(monic(h))
            stack.append(monic(q))
    return sorted(factors, key=lambda p: (len(p), p))


def is_irreducible_over_Q(min_poly: Sequence) -> bool:
    """True iff min_poly is irreducible over Q (a single factor of multiplicity 1)."""
    return factor_over_Q(min_poly) == [[int(c) for c in min_poly]] or \
        len(factor_over_Q(min_poly)) == 1


if __name__ == "__main__":
    for mp in ([1, 0, -10, 0, 1], [1, 0, -25, 0, 91, 0, -75], [1, 0, -2], [1, 0, -5, 0, 6],
               [1, -3, 1], [1, 0, 0, 0, 0, 0, 1]):
        print(f"{mp} -> {factor_over_Q(mp)}")
