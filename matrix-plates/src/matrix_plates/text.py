"""Formatting helpers shared by renderers and the CLI.

These mirror the small string utilities in ``matrix_plates.html`` (``sub``,
``fmt``, ``polyStr``, ``viridis``) so that Python output is byte-compatible with
the reference tool's labels and colour grading. Pure formatting only — no math.
"""

from __future__ import annotations

from typing import List, Sequence

_MINUS = "\u2212"  # U+2212 MINUS SIGN (the tool uses this, not ASCII '-')

_SUBSCRIPTS = {
    "0": "\u2080", "1": "\u2081", "2": "\u2082", "3": "\u2083", "4": "\u2084",
    "5": "\u2085", "6": "\u2086", "7": "\u2087", "8": "\u2088", "9": "\u2089",
}


def sub(n: int | str) -> str:
    """Render *n* using Unicode subscript digits, e.g. ``sub(12) -> '₁₂'``."""
    return "".join(_SUBSCRIPTS.get(ch, ch) for ch in str(n))


def fmt_num(x: float | int) -> str:
    """Signed integer-or-2dp formatter matching the tool's ``fmt``.

    Integers render exactly; non-integers round to 2 dp. Negative values use the
    Unicode minus sign so matrix grids align with the reference rendering.
    """
    r = round(x)
    if abs(x - r) < 1e-9:
        v: float | int = r
    else:
        v = round(x * 100) / 100
    return (_MINUS + str(abs(v))) if v < 0 else str(v)


def poly_str(coeffs: Sequence[int]) -> str:
    """Pretty-print a polynomial given coefficients **high -> low**.

    Mirrors ``polyStr`` in the tool: drops zero terms, suppresses unit
    coefficients on positive-degree terms, and uses the Unicode minus sign.
    Example: ``poly_str([1, -2, -1, 2, 1]) -> 'x₄ \u2212 2x₃ \u2212 x₂ + 2x + 1'``.
    """
    n = len(coeffs) - 1
    out = ""
    for i, a in enumerate(coeffs):
        p = n - i
        if a == 0 and not (p == 0 and out == ""):
            continue
        mag = abs(a)
        term = "" if (mag == 1 and p > 0) else str(mag)
        if p > 1:
            term += "x" + sub(p)
        elif p == 1:
            term += "x"
        if out == "":
            out = (_MINUS if a < 0 else "") + term
        else:
            out += (" " + _MINUS + " " if a < 0 else " + ") + term
    return out or "0"


# --- viridis colour map (same control points as the tool) ----------------------
_VIRIDIS: List[List[int]] = [
    [68, 1, 84], [72, 40, 120], [62, 74, 137], [49, 104, 142], [38, 130, 142],
    [31, 158, 137], [53, 183, 121], [110, 206, 88], [253, 231, 37],
]


def viridis(t: float) -> str:
    """Linear viridis interpolation; returns a CSS ``rgb(...)`` string."""
    t = max(0.0, min(1.0, t))
    f = t * (len(_VIRIDIS) - 1)
    i = min(len(_VIRIDIS) - 2, int(f))
    fr = f - i
    c = [round(v + (_VIRIDIS[i + 1][k] - v) * fr) for k, v in enumerate(_VIRIDIS[i])]
    return f"rgb({c[0]},{c[1]},{c[2]})"
