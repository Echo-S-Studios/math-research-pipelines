"""Optional NumPy / SymPy bridge — speed and independent verification.

The core stays pure-Python and exact; this module is a *bridge* for two things
the stdlib core does not do:

* **NumPy** — fast floating-point eigenvalues / characteristic polynomial for
  large matrices, useful as a quick approximate sanity check (NOT exact);
* **SymPy** — a second, independent *exact* computation of the characteristic
  and minimal polynomials and the Mahler measure, for cross-verification.

Both are imported lazily and are entirely optional: every function raises a
clear :class:`ImportError` (with the missing package named) only if you call it
without the library installed. Nothing here is a runtime dependency of the core.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .invariants import analyse
from .linalg import Matrix


def have_numpy() -> bool:
    try:
        import numpy  # noqa: F401
        return True
    except ImportError:
        return False


def have_sympy() -> bool:
    try:
        import sympy  # noqa: F401
        return True
    except ImportError:
        return False


def _require(pkg: str):
    try:
        return __import__(pkg)
    except ImportError as exc:  # pragma: no cover - exercised only when absent
        raise ImportError(
            f"this function needs the optional package '{pkg}'. Install it with "
            f"`pip install {pkg}` (or `pip install matrix-plates[dev]`). The core "
            f"package itself has no third-party dependencies."
        ) from exc


# --- NumPy: fast, approximate -------------------------------------------------
def numpy_eigenvalues(M: Matrix) -> List[complex]:
    """Floating-point eigenvalues via NumPy (approximate; fast for large n)."""
    np = _require("numpy")
    return [complex(z) for z in np.linalg.eigvals(np.array(M, dtype=float))]


def numpy_mahler(M: Matrix) -> float:
    """Approximate Mahler measure from NumPy eigenvalues (sanity check only)."""
    prod = 1.0
    for z in numpy_eigenvalues(M):
        prod *= max(1.0, abs(z))
    return prod


# --- SymPy: exact, independent ------------------------------------------------
def sympy_char_poly(M: Matrix) -> List[int]:
    """Exact characteristic polynomial (**high → low**) via SymPy."""
    sp = _require("sympy")
    x = sp.symbols("x")
    return [int(c) for c in sp.Matrix(M).charpoly(x).all_coeffs()]


def sympy_min_poly(M: Matrix) -> List[int]:
    """Exact minimal polynomial (**high → low**) via SymPy (Krylov over QQ)."""
    sp = _require("sympy")
    x = sp.symbols("x")
    A = sp.Matrix(M)
    n = A.shape[0]
    basis: list = []
    P = sp.eye(n)
    for k in range(n + 1):
        vec = list(P)
        coeffs = [sp.Integer(0)] * (k + 1)
        coeffs[k] = sp.Integer(1)
        for bvec, piv, bc in basis:
            if vec[piv] != 0:
                f = vec[piv] / bvec[piv]
                vec = [vec[i] - f * bvec[i] for i in range(len(vec))]
                L = max(len(coeffs), len(bc))
                cc = coeffs + [sp.Integer(0)] * (L - len(coeffs))
                bb = bc + [sp.Integer(0)] * (L - len(bc))
                coeffs = [cc[i] - f * bb[i] for i in range(L)]
        piv = next((i for i, v in enumerate(vec) if v != 0), None)
        if piv is None:
            return [int(c) for c in reversed(coeffs)]
        nrm = vec[piv]
        vec = [v / nrm for v in vec]
        coeffs = [c / nrm for c in coeffs]
        basis.append((vec, piv, coeffs))
        P = A * P
    return sympy_char_poly(M)


def sympy_mahler(M: Matrix) -> float:
    """Exact Mahler measure (as a float) via SymPy eigenvalues."""
    sp = _require("sympy")
    prod = sp.Integer(1)
    for val, mult in sp.Matrix(M).eigenvals().items():
        prod *= sp.Max(1, sp.Abs(val)) ** mult
    return float(prod)


def verify(M: Matrix) -> Dict[str, object]:
    """Cross-check the exact core against available oracles.

    Returns a report with the core result and, for whichever of SymPy / NumPy is
    installed, whether the char-poly / minimal polynomial / Mahler measure agree.
    Skipped checks are reported as ``None``.
    """
    a = analyse(M)
    report: Dict[str, object] = {
        "char_poly": a.coeffs, "min_poly": a.minpoly, "mahler": a.mahler,
        "sympy": None, "numpy": None,
    }
    if have_sympy():
        cp = sympy_char_poly(M)
        mp = sympy_min_poly(M)
        mh = sympy_mahler(M)
        report["sympy"] = {
            "char_poly_match": cp == a.coeffs,
            "min_poly_match": mp == a.minpoly,
            "mahler_match": abs(mh - a.mahler) <= 1e-6 * max(1.0, abs(mh)),
        }
    if have_numpy():
        mh = numpy_mahler(M)
        report["numpy"] = {
            "mahler_close": abs(mh - a.mahler) <= 1e-3 * max(1.0, abs(mh)),
        }
    return report
