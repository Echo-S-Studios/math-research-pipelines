"""The construction catalogue — one builder per matrix family.

Each construction emits an **exact integer matrix** plus a label, a provenance
string, and a note. The functions are faithful ports of the tool's builders; the
``OPS`` catalogue and :func:`build` dispatcher mirror its operator algebra so the
Python side can reproduce any plate (and the *Seed batch*) the browser produces.

Families and the single invariant that drives each (see the guide):

============= ===================================== =================
construction  what it generates                     driven by
============= ===================================== =================
companion     custom integer sequence / growth law  ρ
kron (⊗)      deterministic fractal texture         M (Mahler)
dsum (⊕)      multi-voice / multi-channel           rank
commutator    volume-preserving flow (tr = 0)       tr = 0
cartan        E₈ quantizer / Aₙ modal timbre        det / spectrum
circulant     frequency-domain / circular filter    DFT spectrum
ring          signed diffusion / spectral layout    det / ρ
random        reproducible noise / null model       seed + M
============= ===================================== =================

References: Bourbaki, *Lie Groups and Lie Algebras* (Cartan matrices);
Conway & Sloane, *SPLAG* (E₈, unimodular); Davis, *Circulant Matrices*;
Harary (1953) and signed-network synchronization (frustrated ring);
Hammack, Imrich & Klavžar, *Handbook of Product Graphs* (Kronecker).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence

from .linalg import Matrix, matmul, zeros
from .seeds import Seed, SEED_BY_ID
from .text import sub


# --- the raw constructions ------------------------------------------------------
def companion(poly: Sequence[int]) -> Matrix:
    """Companion matrix of a monic polynomial (coefficients **high -> low**).

    Built to match the tool exactly: sub-diagonal ones, last column
    ``-poly`` low->high. Its characteristic polynomial is *poly* and its
    eigenvalues are the Galois conjugates of the seed value. ``O(d**2)``.
    """
    n = len(poly) - 1
    C = zeros(n)
    for i in range(1, n):
        C[i][i - 1] = 1
    for i in range(n):
        C[i][n - 1] = -poly[n - i]
    return C


def kron(A: Matrix, B: Matrix) -> Matrix:
    """Kronecker (tensor) product ``A ⊗ B``; eigenvalues are products λμ.

    Size ``(n*m) x (n*m)``. ``O((n*m)**2)``.
    """
    n, m = len(A), len(B)
    C = zeros(n * m)
    for i in range(n):
        for j in range(n):
            for k in range(m):
                for l in range(m):
                    C[i * m + k][j * m + l] = A[i][j] * B[k][l]
    return C


def dsum(A: Matrix, B: Matrix) -> Matrix:
    """Block-diagonal direct sum ``A ⊕ B``; the two spectra coexist. ``O((n+m)**2)``."""
    n, m = len(A), len(B)
    C = zeros(n + m)
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j]
    for i in range(m):
        for j in range(m):
            C[n + i][n + j] = B[i][j]
    return C


def commutator(A: Matrix, B: Matrix) -> Matrix:
    """Lie bracket ``[A, B] = AB - BA`` of equal-size matrices (trace 0). ``O(n**3)``."""
    if len(A) != len(B):
        raise ValueError("commutator requires equal sizes")
    AB = matmul(A, B)
    BA = matmul(B, A)
    n = len(A)
    return [[AB[i][j] - BA[i][j] for j in range(n)] for i in range(n)]


def _cartan_edges(n: int, edges: Sequence[Sequence[int]]) -> Matrix:
    A = zeros(n)
    for i in range(n):
        A[i][i] = 2
    for a, b in edges:
        A[a][b] = -1
        A[b][a] = -1
    return A


def cartan_a(n: int) -> Matrix:
    """Cartan matrix of ``Aₙ`` (path graph Laplacian + 2I form). ``det = n+1``."""
    return _cartan_edges(n, [(i, i + 1) for i in range(n - 1)])


def cartan_d(n: int) -> Matrix:
    """Cartan matrix of ``Dₙ`` (n >= 4). ``det = 4``."""
    edges = [(i, i + 1) for i in range(n - 2)]
    edges.append((n - 3, n - 1))
    return _cartan_edges(n, edges)


def cartan_e8() -> Matrix:
    """Cartan matrix of ``E₈`` — unimodular (``det = 1``), the optimal 8-D lattice."""
    return _cartan_edges(8, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7)])


def fib_word(n: int) -> List[int]:
    """First *n* Fibonacci numbers starting ``[1, 1, ...]``."""
    a = [1, 1]
    while len(a) < n:
        a.append(a[-1] + a[-2])
    return a[:n]


def lucas_word(n: int) -> List[int]:
    """First *n* Lucas numbers starting ``[2, 1, ...]``."""
    a = [2, 1]
    while len(a) < n:
        a.append(a[-1] + a[-2])
    return a[:n]


def circulant(row: Sequence[int]) -> Matrix:
    """Circulant matrix from its first *row*; eigenvalues are the DFT of the row."""
    n = len(row)
    return [[row[(j - i + n) % n] for j in range(n)] for i in range(n)]


def frustrated_ring(n: int) -> Matrix:
    """Signed-ring Laplacian ``L = D̄ - W`` with alternating ±1 edges.

    Positive semidefinite. Balanced (``det = 0``) when ``n ≡ 0 (mod 4)``,
    frustrated (``det > 0``) when ``n ≡ 2 (mod 4)`` — read the ``det`` chip rather
    than assuming. ``O(n**2)``.

    Edge case: ``n = 2`` is a *digon*, not a simple cycle — its two antiparallel
    ±1 edges cancel, giving the zero matrix (``det = 0``). The mod-4 rule applies
    to genuine cycles ``n >= 4``.
    """
    W = zeros(n)
    for i in range(n):
        j = (i + 1) % n
        s = -1 if i % 2 == 0 else 1
        W[i][j] += s
        W[j][i] += s
    L = zeros(n)
    for i in range(n):
        d = sum(abs(W[i][j]) for j in range(n))
        L[i][i] = d
        for j in range(n):
            if j != i:
                L[i][j] = -W[i][j]
    return L


# --- a built result -------------------------------------------------------------
@dataclass(frozen=True)
class Built:
    """The output of a construction: a matrix plus presentation metadata."""

    M: Matrix
    name: str
    prov: str
    note: str = ""


def _S(reg: Optional[Dict[str, Seed]], sid: str) -> Seed:
    return (reg or SEED_BY_ID)[sid]


# --- construction builders (registry-aware) -------------------------------------
def build_companion(a: str, reg: Optional[Dict[str, Seed]] = None) -> Built:
    s = _S(reg, a)
    return Built(companion(s.poly), f"C({s.glyph})", "companion · " + s.field, s.note)


def build_kron(a: str, b: str, reg: Optional[Dict[str, Seed]] = None) -> Built:
    sa, sb = _S(reg, a), _S(reg, b)
    return Built(kron(companion(sa.poly), companion(sb.poly)),
                 f"{sa.glyph} ⊗ {sb.glyph}",
                 "kronecker · " + sa.field + " × " + sb.field,
                 "spectrum = pairwise products of the two conjugate orbits.")


def build_dsum(a: str, b: str, reg: Optional[Dict[str, Seed]] = None) -> Built:
    sa, sb = _S(reg, a), _S(reg, b)
    return Built(dsum(companion(sa.poly), companion(sb.poly)),
                 f"{sa.glyph} ⊕ {sb.glyph}",
                 "direct sum · " + sa.field + " ⊕ " + sb.field,
                 "char-poly is the product of the two seed polynomials.")


def build_commutator(a: str, b: str, reg: Optional[Dict[str, Seed]] = None) -> Built:
    sa, sb = _S(reg, a), _S(reg, b)
    A, B = companion(sa.poly), companion(sb.poly)
    if len(A) != len(B):
        raise ValueError(
            f"[A,B] needs equal sizes — {sa.glyph} is {len(A)}×{len(A)}, "
            f"{sb.glyph} is {len(B)}×{len(B)}.")
    return Built(commutator(A, B), f"[{sa.glyph},{sb.glyph}]",
                 "commutator · trace 0",
                 "trace(AB−BA)=0 by construction; verify the trace chip reads 0.")


def build_cartan(ctype: str, n: int) -> Built:
    if ctype == "E8":
        return Built(cartan_e8(), "E₈", "cartan · rank 8 · unimodular",
                     "positive-definite; eigenvalues are 2−2cos(angle) for the Aₙ chain.")
    if ctype == "D":
        n = max(4, n)
        return Built(cartan_d(n), "D" + sub(n), "cartan · det 4",
                     "positive-definite; eigenvalues are 2−2cos(angle) for the Aₙ chain.")
    n = max(1, n)
    return Built(cartan_a(n), "A" + sub(n), "cartan · det " + str(n + 1),
                 "positive-definite; eigenvalues are 2−2cos(angle) for the Aₙ chain.")


def build_circulant(word: str, n: int) -> Built:
    n = max(2, n)
    row = lucas_word(n) if word == "lucas" else fib_word(n)
    return Built(circulant(row),
                 ("luc" if word == "lucas" else "fib") + "-circ" + sub(n),
                 "circulant · row [" + ",".join(map(str, row)) + "]",
                 "eigenvalues are the discrete Fourier transform of the first row.")


def build_ring(n: int) -> Built:
    n = max(2, n - (n % 2))  # force even order, like the tool
    if n < 2:
        n = 4
    return Built(frustrated_ring(n), "ring∓" + sub(n), "signed Laplacian · D̄−A",
                 "λ_min = 0 ⇒ balanced (det 0); λ_min > 0 ⇒ frustrated. Read det/ρ.")


def build_random(n: int, seed: int) -> Built:
    from .prng import rand_int_matrix
    n = max(1, n)
    return Built(rand_int_matrix(n, seed), "rand·s" + str(seed),
                 "seeded mulberry32 · n=" + str(n),
                 "reproducible from the seed; compare its Mahler measure to the structured plates.")


def build_custom(matrix: Sequence[Sequence[int]], name: str = "custom") -> Built:
    """Wrap a user-supplied **square integer** matrix as a plate input.

    Raises ``ValueError`` with a specific message for the common mistakes: ragged
    rows, non-square shape, or non-integer entries (the analysis is defined over
    ℤ/ℚ, so floats and symbols are rejected here rather than silently coerced).
    """
    if not matrix or not matrix[0]:
        raise ValueError("custom matrix is empty — provide an n×n grid of integers.")
    n = len(matrix)
    widths = {len(r) for r in matrix}
    if widths != {n}:
        raise ValueError(
            f"custom matrix must be square with equal-length rows; got {n} rows "
            f"of widths {sorted(widths)}.")
    M: Matrix = []
    for i, row in enumerate(matrix):
        out_row: List[int] = []
        for j, x in enumerate(row):
            xf = float(x)
            if abs(xf - round(xf)) > 1e-9:
                raise ValueError(
                    f"entry [{i}][{j}] = {x!r} is not an integer; this system works "
                    f"over ℤ (use a companion/Cartan/… construction for algebraic seeds).")
            out_row.append(int(round(xf)))
        M.append(out_row)
    return Built(M, name, "user matrix · n=" + str(n), "custom integer matrix.")


# --- catalogue + dispatcher -----------------------------------------------------
@dataclass(frozen=True)
class OpSpec:
    key: str
    label: str
    needs: List[str]   # subset of {"A","B","type","N","word","seed"}
    glyph: str
    desc: str


OPS: Dict[str, OpSpec] = {
    "companion": OpSpec("companion", "Companion C(p)", ["A"], "C",
        "Companion matrix of a monic integer minimal polynomial. Eigenvalues = the "
        "Galois conjugates; characteristic polynomial = the seed polynomial."),
    "kron": OpSpec("kron", "Kronecker A ⊗ B", ["A", "B"], "⊗",
        "Tensor product of two companion matrices. Eigenvalues are pairwise products "
        "λᵢμⱼ; Mahler measures compose multiplicatively."),
    "dsum": OpSpec("dsum", "Direct sum A ⊕ B", ["A", "B"], "⊕",
        "Block-diagonal sum. The two spectra coexist; char-poly = product of the two. "
        "A ⊕ A is the canonical derogatory witness."),
    "comm": OpSpec("comm", "Commutator [A,B]", ["A", "B"], "[,]",
        "Lie bracket AB − BA of two equal-size companions. Always trace-free."),
    "cartan": OpSpec("cartan", "Cartan matrix", ["type", "N"], "𝒞",
        "Cartan matrix of a root system. det Aₙ = n+1, det Dₙ = 4, det E₈ = 1."),
    "circ": OpSpec("circ", "Fibonacci/Lucas circulant", ["word", "N"], "↻",
        "Circulant from a Fibonacci or Lucas first row. Eigenvalues = DFT of that row."),
    "ring": OpSpec("ring", "Frustrated ring Laplacian", ["N"], "∿",
        "Signed ring Laplacian (alternating ±1 edges). Singular when balanced."),
    "rand": OpSpec("rand", "Random integer (seeded)", ["N", "seed"], "⚄",
        "Reproducible random integer matrix, entries in [−3, 3] — the control family."),
}


def build(op: str,
          *,
          a: str = "phi", b: str = "sq2",
          ctype: str = "A", word: str = "fib",
          n: int = 5, seed: int = 42,
          matrix: Optional[Sequence[Sequence[int]]] = None,
          name: str = "custom",
          reg: Optional[Dict[str, Seed]] = None) -> Built:
    """Dispatch to a construction by key, mirroring the tool's ``readParams``.

    Raises ``ValueError`` for invalid combinations (e.g. a commutator of unequal
    sizes, a non-square custom matrix), exactly as the tool surfaces them.
    """
    if op == "companion":
        return build_companion(a, reg)
    if op == "kron":
        return build_kron(a, b, reg)
    if op == "dsum":
        return build_dsum(a, b, reg)
    if op == "comm":
        return build_commutator(a, b, reg)
    if op == "cartan":
        return build_cartan(ctype, n)
    if op == "circ":
        return build_circulant(word, n)
    if op == "ring":
        return build_ring(n)
    if op == "rand":
        return build_random(n, seed)
    if op == "custom":
        if matrix is None:
            raise ValueError("op 'custom' requires a matrix= argument.")
        return build_custom(matrix, name)
    raise ValueError(f"unknown construction: {op!r}")


def seed_batch_specs() -> List[Built]:
    """Reproduce the tool's *Seed batch* exactly (same nine plates, same order)."""
    return [
        build_companion("phi"), build_companion("gap"), build_companion("K"),
        build_cartan("E8", 8), build_cartan("A", 5),
        build_kron("phi", "sq3"), build_circulant("fib", 6),
        build_ring(6), build_random(4, 42),
    ]
