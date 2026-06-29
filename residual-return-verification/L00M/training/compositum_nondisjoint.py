"""compositum_nondisjoint.py -- P2c core: build the TRUE compositum K(beta) exactly when beta's minpoly
PARTIALLY FACTORS over K (the non-disjoint case the tensor Kronecker-Gram shortcut gets wrong).

Given K = Q(alpha) by its monic-integer minpoly m_alpha (deg m) and a new algebraic-integer generator
beta by its monic-integer minpoly m_beta over Q (deg k), construct the compositum Q(alpha, beta):

  1. tensor ring  R = Q[x,y]/(m_alpha(x), m_beta(y))  (dim m*k). alpha = x, beta = y.
  2. theta = alpha + c*beta for the smallest c>=1 that is a PRIMITIVE element of Q(alpha,beta); its
     regular representation M_theta on R has minimal polynomial m_theta_full (Smith normal form, reused).
  3. m_theta_full is REDUCIBLE in general (it is the product over the distinct tensor factors -- e.g.
     K=Q(sqrt2), beta=sqrt2+sqrt3, c=1 gives degree 6 = (x^4-22x^2+25)*(x^2-3), the spurious x^2-3 from
     the embedding where x=-sqrt2 collapses theta to sqrt3). Factor it over Q (bounded Kronecker).
  4. SELECT the compositum factor F: the irreducible factor with m | deg(F) AND alpha expressible as a
     Q-polynomial in theta on the F-component (an exact nullspace + linear solve over Q). This rejects the
     spurious x^2-3 (Q(sqrt3) does not contain sqrt2) and keeps F = m_theta. e' = deg(F)/m = [K(beta):K].
  5. With alpha = sum a_i theta^i recovered, beta = (theta - alpha)/c gives beta's coordinates in the
     compositum power basis {1, theta, ..., theta^{m*e'-1}} -- so the previously out-of-field beta is now
     captured (residual -> 0).

Returns the exact m_theta (HIGH->LOW int), e', the new degree m*e', beta's coords, and the factorization.
The caller (compositum.py) branches on e': e'==k disjoint / e'==1 already-in-K / 1<e'<k true compositum.

Exact (Fraction/int, G8); monic-integer (G10). Reuses invariant_factors (SNF/minpoly), companion_high,
and number_field_factor (bounded Kronecker). Model-layer only: pure stdlib + fractions.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from fractions import Fraction as F
from typing import List, Optional, Sequence, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from integral_basis import _guard_int_monic                       # noqa: E402  (G10)
from invariant_factors import invariant_factors, companion_high    # noqa: E402  (SNF; rho(theta))
from number_field_factor import factor_over_Q, FactorizationUnsupported  # noqa: E402


def trace_form_gram(m_theta) -> List[List[F]]:
    """Exact trace-form Gram of Q(theta) on the power basis {1, theta, ..., theta^{D-1}}:
    G[i][j] = Tr_{Q(theta)/Q}(theta^{i+j}) = trace(C(m_theta)^{i+j}), C the companion matrix. Exact Fraction."""
    m_theta = _guard_int_monic(m_theta)
    D = len(m_theta) - 1
    C = companion_high(list(m_theta))
    powers = [[[F(1) if i == j else F(0) for j in range(D)] for i in range(D)]]   # C^0
    for _ in range(2 * D - 1):
        prev = powers[-1]
        powers.append([[sum(prev[i][t] * C[t][j] for t in range(D)) for j in range(D)] for i in range(D)])
    def tr(p):
        return sum(powers[p][i][i] for i in range(D))
    return [[tr(i + j) for j in range(D)] for i in range(D)]


@dataclass(frozen=True)
class CompositumResult:
    """The exact compositum K(beta) = Q(theta)."""
    m_theta: List[int]            # HIGH->LOW monic-integer minpoly of the primitive element theta
    e_prime: int                  # [K(beta) : K]
    new_degree: int               # [K(beta) : Q] = m * e_prime
    beta_coords: List[F]          # beta in the power basis {1, theta, ..., theta^{new_degree-1}}
    alpha_coords: List[F]         # alpha (the K generator) in the same basis
    c: int                        # theta = alpha + c*beta (the primitive-element shift used)
    factorization: List[List[int]]   # the full Q-factorization of m_theta_full (witness/audit)


# --------------------------------------------------------------------------- #
# exact linear algebra over Q (nullspace + solve), used by the factor selection
# --------------------------------------------------------------------------- #
def _rref(rows: List[List[F]]) -> Tuple[List[List[F]], List[int]]:
    """Reduced row echelon form (exact Q). Returns (rref_rows, pivot_columns)."""
    M = [row[:] for row in rows]
    if not M:
        return M, []
    nrows, ncols = len(M), len(M[0])
    pivots: List[int] = []
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, nrows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][c]
        M[r] = [v / inv for v in M[r]]
        for i in range(nrows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        pivots.append(c)
        r += 1
        if r == nrows:
            break
    return M, pivots


def _nullspace(mat: List[List[F]]) -> List[List[F]]:
    """Basis of the right null space {v : mat @ v = 0} (exact Q)."""
    if not mat:
        return []
    ncols = len(mat[0])
    R, pivots = _rref(mat)
    pivot_set = set(pivots)
    free = [c for c in range(ncols) if c not in pivot_set]
    basis: List[List[F]] = []
    for fcol in free:
        v = [F(0)] * ncols
        v[fcol] = F(1)
        for ri, pc in enumerate(pivots):
            v[pc] = -R[ri][fcol]
        basis.append(v)
    return basis


def _solve(cols: List[List[F]], target: List[F]) -> Optional[List[F]]:
    """Solve sum_j a_j * cols[j] = target over Q. Returns a (len == len(cols)) or None if inconsistent.
    cols are column vectors (each length N); assumes a unique/consistent solution when columns are
    independent (our use: theta-power columns on an e'-cyclic component)."""
    if not cols:
        return None
    N = len(target)
    D = len(cols)
    aug = [[cols[j][i] for j in range(D)] + [target[i]] for i in range(N)]
    R, pivots = _rref(aug)
    # inconsistency: a pivot in the augmented (last) column
    if (D) in pivots:
        return None
    a = [F(0)] * D
    for ri, pc in enumerate(pivots):
        if pc < D:
            a[pc] = R[ri][D]
    # verify (guards against a free-variable mis-pick on dependent columns)
    for i in range(N):
        if sum(a[j] * cols[j][i] for j in range(D)) != target[i]:
            return None
    return a


# --------------------------------------------------------------------------- #
# tensor regular representations of alpha (=x) and beta (=y) on R = Q[x,y]/(m_a, m_b)
# --------------------------------------------------------------------------- #
def _mul_matrices(m_alpha_hl: List[int], m_beta_hl: List[int]):
    """Return (M_x, M_y, N, m, k): multiplication-by-x and -by-y matrices on R (basis x^i y^j,
    idx = i*k + j), with x^m, y^k reduced by the (monic) minpolys."""
    m = len(m_alpha_hl) - 1
    k = len(m_beta_hl) - 1
    N = m * k
    # low->high coefficient lists of the reduction rules: x^m = -(a_0 + a_1 x + ... + a_{m-1} x^{m-1})
    a_low = [F(-c) for c in m_alpha_hl[:0:-1]]   # m_alpha_hl high->low: [1, a_{m-1},...,a_0]; tail reversed
    # a_low[i] is the coefficient of x^i in (x^m reduced). Build carefully:
    a_low = [F(-m_alpha_hl[m - i]) for i in range(m)]      # x^m -> sum_i a_low[i] x^i
    b_low = [F(-m_beta_hl[k - j]) for j in range(k)]       # y^k -> sum_j b_low[j] y^j

    def idx(i, j):
        return i * k + j

    M_x = [[F(0)] * N for _ in range(N)]
    M_y = [[F(0)] * N for _ in range(N)]
    for i in range(m):
        for j in range(k):
            col = idx(i, j)
            # x * x^i y^j
            if i + 1 < m:
                M_x[idx(i + 1, j)][col] += F(1)
            else:
                for ii in range(m):
                    if a_low[ii] != 0:
                        M_x[idx(ii, j)][col] += a_low[ii]
            # y * x^i y^j
            if j + 1 < k:
                M_y[idx(i, j + 1)][col] += F(1)
            else:
                for jj in range(k):
                    if b_low[jj] != 0:
                        M_y[idx(i, jj)][col] += b_low[jj]
    return M_x, M_y, N, m, k


def _matadd_scaled(A, B, c):
    return [[A[i][j] + c * B[i][j] for j in range(len(A))] for i in range(len(A))]


def _matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def _matpoly_eval(coeffs_hl: List[int], M):
    """Evaluate the polynomial coeffs_hl (HIGH->LOW) at the matrix M: sum_t c_t M^t."""
    N = len(M)
    low = coeffs_hl[::-1]                       # low->high
    R = [[F(0)] * N for _ in range(N)]
    P = [[F(1) if i == j else F(0) for j in range(N)] for i in range(N)]   # M^0
    for t, c in enumerate(low):
        if c != 0:
            for i in range(N):
                Ri, Pi = R[i], P[i]
                for j in range(N):
                    Ri[j] += c * Pi[j]
        if t + 1 < len(low):
            P = [[sum(P[i][t2] * M[t2][j] for t2 in range(N)) for j in range(N)] for i in range(N)]
    return R


def _operator_minpoly_hl(M) -> List[int]:
    """Minimal polynomial of the matrix M (largest invariant factor), HIGH->LOW monic-integer if integral."""
    facs = invariant_factors(M)                 # LOW->HIGH monic Fraction polys; last = minpoly
    mp_low = facs[-1]
    hl = [mp_low[t] for t in range(len(mp_low) - 1, -1, -1)]
    return [int(c) if F(c).denominator == 1 else c for c in hl]


# --------------------------------------------------------------------------- #
# the compositum construction
# --------------------------------------------------------------------------- #
def build_compositum(m_alpha, m_beta, *, max_shift: int = 6) -> CompositumResult:
    """Construct Q(alpha, beta) exactly. alpha/beta are monic-integer minpolys (HIGH->LOW). Returns a
    CompositumResult (m_theta, e' = [K(beta):K], beta-coords, ...). Raises FactorizationUnsupported if the
    operator minpoly degree exceeds the Kronecker bound; ValueError if no primitive shift c<=max_shift
    works (degenerate)."""
    m_alpha = _guard_int_monic(m_alpha)
    m_beta = _guard_int_monic(m_beta)
    M_x, M_y, N, m, k = _mul_matrices(m_alpha, m_beta)

    for c in range(1, max_shift + 1):
        M_theta = _matadd_scaled(M_x, M_y, F(c))
        m_full = _operator_minpoly_hl(M_theta)
        facs = factor_over_Q(m_full)            # may raise FactorizationUnsupported (degree > cap)
        # SELECT: irreducible factor F with m | deg(F) and alpha in Q[theta] on the F-component.
        best: Optional[CompositumResult] = None
        for Fhl in facs:
            D = len(Fhl) - 1
            if D % m != 0:
                continue
            # F-component R_F = nullspace of F(M_theta)
            FM = _matpoly_eval(Fhl, M_theta)
            R_F = _nullspace(FM)
            if not R_F:
                continue
            w = R_F[0]
            # theta-power columns on w: [w, M_theta w, ..., M_theta^{D-1} w]
            cols = []
            cur = w[:]
            for _ in range(D):
                cols.append(cur)
                cur = _matvec(M_theta, cur)
            a = _solve(cols, _matvec(M_x, w))   # alpha = sum a_i theta^i  on the w-line?
            if a is None:
                continue                        # alpha not a Q-poly in theta here -> reject (e.g. x^2-3)
            # verify on ALL of R_F (consistency across the whole F-component, not just w)
            ok = True
            for u in R_F:
                lhs = [F(0)] * N
                pu = u[:]
                for ai in a:
                    if ai != 0:
                        lhs = [lhs[t] + ai * pu[t] for t in range(N)]
                    pu = _matvec(M_theta, pu)
                if lhs != _matvec(M_x, u):
                    ok = False
                    break
            if not ok:
                continue
            # alpha_coords = a (len D); beta = (theta - alpha)/c, theta = e_1 in the power basis
            alpha_coords = list(a) + [F(0)] * (D - len(a))
            theta_coords = [F(0)] * D
            if D >= 2:
                theta_coords[1] = F(1)
            else:                                # D==1 means theta in Q -> degenerate, skip
                ok = False
            if not ok:
                continue
            beta_coords = [(theta_coords[t] - alpha_coords[t]) / c for t in range(D)]
            cand = CompositumResult(
                m_theta=[int(x) for x in Fhl],
                e_prime=D // m,
                new_degree=D,
                beta_coords=beta_coords,
                alpha_coords=alpha_coords,
                c=c,
                factorization=[list(f) for f in facs],
            )
            # prefer the minimal-degree valid factor (the actual compositum), then lexicographically
            if best is None or (cand.new_degree, cand.m_theta) < (best.new_degree, best.m_theta):
                best = cand
        if best is not None:
            return best
    raise ValueError(f"no primitive element alpha + c*beta found for c <= {max_shift} (degenerate input)")


if __name__ == "__main__":
    # canonical witness: K = Q(sqrt2), beta = sqrt2 + sqrt3
    res = build_compositum([1, 0, -2], [1, 0, -10, 0, 1])
    print("m_theta      :", res.m_theta, " (deg", res.new_degree, ")")
    print("e' = [K(b):K]:", res.e_prime, " (expect 2; disjoint tensor would be 8)")
    print("c            :", res.c)
    print("beta coords  :", [str(x) for x in res.beta_coords])
    print("factorization:", res.factorization)
