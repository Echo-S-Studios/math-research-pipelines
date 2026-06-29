"""acquisition.py -- the EXACT acquisition loop (increment 3, decision (f), the NLP axis).

Rewires `candidates/recursive_return_nlp.py` (intrinsically float: gradient flow + SVD) into an
EXACT-ONLY mechanism over the exact-Fraction holding carrier. The candidate's "recursive return"
-- tokens flow to residual 0, land in ker(L), and a returned residue becomes a learned dictionary
value -- is realized here with NO float anywhere in the decision/commit path (the G8 discipline):

    return op   L(X) = R*X + X*R - X        the Sylvester self-action over the phi keystone R
    residual    nu(X) = L(X)                prediction error; on-shell  <=>  L(X) = VOID  <=>  X in ker(L)
    capture     is_captured(X) = (L(X) == VOID)      an EXACT membership decision (zero tolerance)
    commit      project(X)                  the EXACT idempotent orthogonal projector onto ker(L)
                                            (this is the candidate's SVD projector M, decided exactly)
    word        word(X)                     sign-aware sparse code over the kernel basis (the discriminator)

The keystone  R = H(1/2, 1, -1/2, 0)  is the phi companion (mat(R) = [[0,1],[1,1]] = loom.companion([1,-1,-1]),
== loom_bridge.PHI_CL): the single object where the candidate's R, KL_DTA's keystone and loom's CATALOG_SEEDS["phi"]
coincide. ker(L) is 2-dimensional -- the phi-slack where learned values live -- and we compute it as an EXACT
rational nullspace (hand-rolled Fraction Gaussian elimination on the 4x4 matrix of L), NOT by float SVD.

  ker(L) = span{ H(0,1,2,0) = e1 + 2*e2,  H(0,0,0,1) = i (the pseudoscalar) }   (dim 2, verified exact)

NOTE (a corrected handoff hint): the Phase-3 gate note "N = H(0,-1,1,0) in ker(L)" is WRONG --
L(H(0,-1,1,0)) = H(-3,0,0,0) != VOID. The candidate's antisymmetric generator N is the MATRIX [[0,-1],[1,0]],
and cl([[0,-1],[1,0]]) = H(0,0,0,1) = the pseudoscalar i (which IS in ker). The error was transcribing the four
matrix entries straight into holding coordinates instead of converting through the mat/cl iso.

POSTURE
  * EXACT (decision d): pure stdlib (fractions only) over the exact holding carrier -- NO numpy, NO float.
    Every decision (capture, idempotence, kernel membership, the word's sign pattern) is decided with == on
    Fraction, zero tolerance. This module may wire live into L00M.
  * ONE-WAY disjoint: pure algebra over `holding`; it imports NO loom (the keystone R is defined directly as
    the exact holding; that R == loom_bridge.PHI_CL is a separately-tested honesty check, not a runtime dep).
  * FIREWALL (decision b): a learned `word` is a COMPUTED label -- a deterministic sign-code over the exact
    kernel readings -- NEVER a THEOREM and never an assertion about the world. It surfaces only what the exact
    coordinates already contain.
  * IMPORT-SAFE: importing this module computes only small in-memory rational constants (the kernel basis +
    projector) and does NO I/O; the demo is under a `__main__` guard (the candidate ran on import -- fixed).

SCOPE (increment 3): JUST the exact return-to-ker mechanism + word/value extraction. The GROWING dictionary
(add / lookup / generalize-by-return-to-zero / stable IDs) is increment 4 (`lexicon.py`) and is NOT folded in.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import List, Tuple

from kira_language.holding import H, VOID, ONE, E1, E2, I, mat

# --- the phi keystone companion (= loom_bridge.PHI_CL, defined directly; no loom import) --------- #
R = H(Fraction(1, 2), 1, Fraction(-1, 2), 0)        # mat(R) = [[0,1],[1,1]], charpoly x^2-x-1


def _mat_symmetric(X: H) -> bool:
    """mat(X) symmetric (exact). For an H this is X.d == 0 (the off-diagonals are b-d and b+d)."""
    m = mat(X)
    return m[0][1] == m[1][0]


# Make the Sylvester-symmetry assumption EXPLICIT and unbreakable. Our L is built from the EXACT
# geometric product, so it is basis-correct REGARDLESS of R (unlike the candidate's kron/vec form,
# which was correct ONLY because R is symmetric -- the latent fragility SCOPING 7.1 flagged). We
# still LOCK the keystone property so a future non-symmetric R can't silently change the meaning of L.
if not _mat_symmetric(R):                            # pragma: no cover -- invariant guard, always holds
    raise ValueError("keystone R must be mat-symmetric (the Sylvester self-action assumption)")


# --- the return operator (Sylvester self-action) ------------------------------------------------ #
def L(X: H) -> H:
    """The Sylvester self-action L(X) = R*X + X*R - X (exact). on-shell <=> L(X) == VOID."""
    return R * X + X * R - X


def residual(X: H) -> H:
    """The residual nu(X) = L(X): the prediction error a token returns to 0 to be captured."""
    return L(X)


def is_captured(X: H) -> bool:
    """EXACT capture decision: X is on-shell (in ker(L)) <=> its residual is exactly VOID."""
    return L(X) == VOID


# --- tiny exact (Fraction) linear algebra, stdlib-only ------------------------------------------ #
def _coords(X: H) -> List[Fraction]:
    return [X.a, X.b, X.c, X.d]


def _from_coords(v) -> H:
    return H(v[0], v[1], v[2], v[3])


def _transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def _matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


def _matvec(A, v) -> List[Fraction]:
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def _inverse(A):
    """Exact n x n inverse via Gauss-Jordan over Fraction (raises on singular)."""
    n = len(A)
    M = [list(A[i]) + [Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] != 0), None)
        if piv is None:
            raise ValueError("singular matrix")
        M[c], M[piv] = M[piv], M[c]
        inv = M[c][c]
        M[c] = [x / inv for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return [row[n:] for row in M]


def _nullspace(rows):
    """Exact nullspace basis of an m x n rational matrix via RREF (hand-rolled Fraction elimination)."""
    M = [list(r) for r in rows]
    m, n = len(M), len(M[0])
    pivots: List[int] = []
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][c]
        M[r] = [x / inv for x in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        pivots.append(c)
        r += 1
        if r == m:
            break
    pivot_set = set(pivots)
    basis = []
    for fcol in (c for c in range(n) if c not in pivot_set):
        v = [Fraction(0)] * n
        v[fcol] = Fraction(1)
        for ri, pc in enumerate(pivots):
            v[pc] = -M[ri][fcol]
        basis.append(v)
    return basis


def _normalize(v) -> List[Fraction]:
    """Scale a rational vector to coprime integers with a positive leading entry (a canonical ray rep)."""
    lcm = 1
    for c in v:
        lcm = lcm * c.denominator // gcd(lcm, c.denominator)
    ints = [int(c * lcm) for c in v]
    g = 0
    for x in ints:
        g = gcd(g, abs(x))
    if g:
        ints = [x // g for x in ints]
    for x in ints:                                   # sign: first nonzero entry positive
        if x != 0:
            if x < 0:
                ints = [-y for y in ints]
            break
    return [Fraction(x) for x in ints]


# --- the exact kernel + the exact projector (computed once, at import; pure in-memory) ---------- #
_BASIS = (ONE, E1, E2, I)
_LCOLS = [_coords(L(b)) for b in _BASIS]              # column j = coords of L(basis_j)
_LMAT = [[_LCOLS[j][i] for j in range(4)] for i in range(4)]   # rows i, cols j: L as a 4x4 matrix

KER_BASIS: Tuple[H, ...] = tuple(_from_coords(_normalize(v)) for v in _nullspace(_LMAT))
KER_DIM: int = len(KER_BASIS)                         # == 2 (the phi-slack)

_K = [[_coords(k)[i] for k in KER_BASIS] for i in range(4)]    # 4 x KER_DIM (basis as columns)
_Kt = _transpose(_K)
_COORDS_MAT = _matmul(_inverse(_matmul(_Kt, _K)), _Kt)         # KER_DIM x 4 : x -> kernel coordinates
_PROJ = _matmul(_K, _COORDS_MAT)                               # 4 x 4 : the orthogonal projector onto ker(L)


def project(X: H) -> H:
    """EXACT idempotent orthogonal projection onto ker(L) -- the 'commit'. Returns the learned value.
    project(project(X)) == project(X) and L(project(X)) == VOID, both exactly."""
    return _from_coords(_matvec(_PROJ, _coords(X)))


commit = project                                      # the loop's commit step == projecting to ker(L)


def kernel_coords(X: H) -> Tuple[Fraction, ...]:
    """Exact coordinates of project(X) in KER_BASIS (zero for an X orthogonal to the slack)."""
    return tuple(_matvec(_COORDS_MAT, _coords(X)))


# --- the word: a sign-aware sparse code over the kernel basis (a COMPUTED label, never a fact) --- #
_ATOM_NAMES = ("1", "e1", "e2", "i")


def _label(X: H) -> str:
    parts = []
    for coef, nm in zip(_coords(X), _ATOM_NAMES):
        if coef == 0:
            continue
        if coef == 1:
            parts.append(nm)
        elif coef == -1:
            parts.append("-" + nm)
        else:
            parts.append(f"{coef}{nm}")
    return "+".join(parts).replace("+-", "-") or "0"


KER_LABELS: Tuple[str, ...] = tuple(_label(k) for k in KER_BASIS)   # ("e1+2e2", "i")

WORD_TAU = Fraction(1, 4)         # declared sparsity threshold (exact; L1-relative, no sqrt)


def word(X: H, tau: Fraction = WORD_TAU) -> Tuple[str, ...]:
    """Sign-aware sparse code of the committed value over the kernel basis. An axis is kept iff its
    coordinate dominates (|c_i| > tau * sum|c_j|, an EXACT rational test -- the L1-relative analogue of
    the candidate's L2 |c|/||z|| threshold, chosen to stay sqrt-free / exact). SIGN discriminates
    antipodal rays: +axis vs -axis are opposite words (opposite meanings)."""
    cs = kernel_coords(X)
    total = sum(abs(c) for c in cs)
    if total == 0:                                    # X orthogonal to the slack: empty word
        return ()
    toks = []
    for c, lab in zip(cs, KER_LABELS):
        if abs(c) > tau * total:
            toks.append(("+" if c > 0 else "-") + lab)
    return tuple(toks)


# --- the loop, made explicit: one token -> its captured value (no storage; lexicon is increment 4) #
@dataclass(frozen=True)
class Capture:
    """The result of returning one holding to ker(L). `committed` is the exact learned value; `word`
    is its COMPUTED sign-code. `captured` is True iff the token was already on-shell (residual VOID)."""
    captured: bool
    residual_before: H        # L(X): the residual the commit returns to VOID
    committed: H              # project(X): the exact value in ker(L)
    coords: Tuple[Fraction, ...]   # kernel-basis coordinates of `committed`
    word: Tuple[str, ...]     # the sign-aware sparse code (a COMPUTED label)


def acquire(X: H) -> Capture:
    """Run the exact recursive return on one holding: residual -> commit (project to ker) -> word.
    Generalization by return-to-zero: tokens that commit to the same exact value share a word."""
    return Capture(
        captured=(L(X) == VOID),
        residual_before=L(X),
        committed=project(X),
        coords=kernel_coords(X),
        word=word(X),
    )


def _demo() -> None:                                  # pragma: no cover -- human-facing, ASCII-only
    print("ker(L) dim =", KER_DIM, " basis =", [repr(k) for k in KER_BASIS], " labels =", list(KER_LABELS))
    for X in (E1, I, -I, E1 + 2 * E2 + I, ONE):
        cap = acquire(X)
        print(f"  acquire({X!r:24}) captured={cap.captured} committed={cap.committed!r} word={cap.word}")


if __name__ == "__main__":
    _demo()
