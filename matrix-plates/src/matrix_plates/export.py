"""Export plates to JSON, LaTeX, and runnable SymPy code.

All exporters read the exact :class:`~matrix_plates.invariants.Analysis`, so the
serialized invariants are the integer-exact ones (char-poly, minimal polynomial,
invariant factors, det, trace, rank) plus the floating-point spectral quantities
(Mahler measure, house). Nothing here mutates state.
"""

from __future__ import annotations

import json
import re
from typing import Iterable, List, Union

from .plates import Plate
from .polynomial import Poly

PlateOrList = Union[Plate, Iterable[Plate]]


def _plates(obj: PlateOrList) -> List[Plate]:
    return [obj] if isinstance(obj, Plate) else list(obj)


def plate_to_dict(p: Plate) -> dict:
    """A JSON-serializable dict of a plate's matrix and full invariant set."""
    a = p.analysis
    prov = None
    if p.provenance is not None:
        prov = {"kind": p.provenance.kind, "label": p.provenance.label,
                "parents": list(p.provenance.parents), "seed": p.provenance.seed}
    return {
        "id": p.id, "name": p.name, "provenance_label": p.prov, "family": p.family,
        "matrix": [list(row) for row in p.M],
        "n": a.n,
        "char_poly": list(a.coeffs),
        "min_poly": list(a.minpoly),
        "invariant_factors": [list(f) for f in a.invariant_factors],
        "det": a.det, "trace": a.tr, "rank": a.rank,
        "mahler": a.mahler, "house": a.house, "rho": a.rho, "frobenius": a.frob,
        "derogatory": a.derogatory, "defective": a.defective,
        "unimodular": a.unimodular,
        "spectrum": {"outside": a.outside, "on": a.on, "inside": a.inside},
        "flags": {"at_floor": a.at_floor, "in_lehmer_gap": a.in_lehmer_gap},
        "provenance": prov,
    }


def export_json(obj: PlateOrList, indent: int = 2) -> str:
    """Serialize a plate or gallery to JSON."""
    data = [plate_to_dict(p) for p in _plates(obj)]
    return json.dumps(data if len(data) != 1 else data[0], indent=indent)


def _bmatrix(M: List[List[int]]) -> str:
    rows = " \\\\\n".join(" & ".join(str(x) for x in row) for row in M)
    return "\\begin{bmatrix}\n" + rows + "\n\\end{bmatrix}"


def export_latex(p: Plate) -> str:
    """A LaTeX block: the matrix plus its characteristic and minimal polynomials."""
    a = p.analysis
    cp = Poly.from_high_low(a.coeffs).latex()
    mp = Poly.from_high_low(a.minpoly).latex()
    facs = ",\\; ".join(Poly.from_high_low(f).latex() for f in a.invariant_factors)
    lines = [
        f"% {p.name} — {p.prov}",
        "\\[",
        f"A = {_bmatrix(p.M)}",
        "\\]",
        "\\begin{align*}",
        f"\\chi_A(x) &= {cp} \\\\",
        f"m_A(x) &= {mp} \\\\",
        f"\\text{{invariant factors}} &= \\{{ {facs} \\}} \\\\",
        f"\\det A &= {a.det}, \\quad \\operatorname{{tr}} A = {a.tr}, "
        f"\\quad M(A) = {round(a.mahler, 6)}, \\quad \\house{{A}} = {round(a.house, 6)}",
        "\\end{align*}",
    ]
    return "\n".join(lines)


def _ident(name: str) -> str:
    s = re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_")
    return ("A_" + s) if (not s or s[0].isdigit()) else s


def export_sympy(p: Plate) -> str:
    """Runnable SymPy code reconstructing the matrix, with its invariants as comments."""
    a = p.analysis
    var = _ident(p.name)
    rows = ",\n    ".join("[" + ", ".join(str(x) for x in row) + "]" for row in p.M)
    cp = Poly.from_high_low(a.coeffs)
    mp = Poly.from_high_low(a.minpoly)
    return (
        "from sympy import Matrix, symbols\n"
        "x = symbols('x')\n\n"
        f"# {p.name} — {p.prov}\n"
        f"{var} = Matrix([\n    {rows},\n])\n\n"
        f"# characteristic polynomial: {cp!r}\n"
        f"# minimal polynomial:        {mp!r}\n"
        f"# det = {a.det}, trace = {a.tr}, rank = {a.rank}\n"
        f"# Mahler measure ~ {round(a.mahler, 6)}, house ~ {round(a.house, 6)}\n"
        f"# derogatory = {a.derogatory}, defective = {a.defective}, "
        f"unimodular = {a.unimodular}\n"
        f"assert {var}.charpoly(x).all_coeffs() == {a.coeffs}\n"
    )
