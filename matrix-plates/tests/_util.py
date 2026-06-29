"""Shared test helpers (not collected as tests).

Loads the committed ground-truth fixtures:
* ``ground_truth_js.json`` — captured by running the reference engine's verbatim
  JS under Node (matrices, char-polys, PRNG outputs).
* ``oracle_sympy.json`` — an independent sympy oracle (char-poly, minimal
  polynomial, Mahler, rho, det, trace, rank, derogatory).

Because both fixtures are committed, the suite needs no Node or sympy at test
time — it is stdlib-only.
"""

from __future__ import annotations

import json
import pathlib

_FIX = pathlib.Path(__file__).resolve().parent / "fixtures"


def load(name: str) -> dict:
    return json.loads((_FIX / name).read_text(encoding="utf-8"))


JS = load("ground_truth_js.json")
ORACLE = load("oracle_sympy.json")


def close(a: float, b: float, rel: float = 1e-6, abs_: float = 1e-9) -> bool:
    """True if *a* and *b* agree to a relative or absolute tolerance."""
    return abs(a - b) <= max(abs_, rel * max(abs(a), abs(b)))
