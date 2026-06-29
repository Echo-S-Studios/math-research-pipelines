"""bridge_loom.py -- the ONE-WAY phi-keystone bridge to loom.

The only RUNTIME / LIBRARY module that imports loom. (The pre-existing conformance test,
test_kl_dta_conformance.py, also imports loom read-only -- so this holds for shipped modules,
not literally every file in the tree.) Direction is strictly one-way:
kira-language READS loom (the phi keystone); L00M NEVER imports kira-language.

Read-only and NEVER raises: it returns a structured result (so the JSON dispatch surface
stays G6-safe). If loom is unreachable it reports {"loom_reachable": False, ...} rather than
crashing.

Self-bootstraps the loom path so it works BOTH under pytest (conftest also sets it) AND in a
bare `py -c "import language_api; language_api.main()"` subprocess (no conftest there):
override with env KIRA_LANG_L00M_ROOT, else default to the sibling clone ../L00M.

The keystone: the void law x^2 = x + 1  ->  minpoly [1,-1,-1]  ->  loom.companion = [[0,1],[1,1]]
            ->  Cl(0.5, 1, -0.5, 0) under the shared mat/cl convention  ->  Mahler measure = phi.
This is the single object where recursive_return's R, KL_DTA's keystone, and loom's
CATALOG_SEEDS["phi"] all coincide -- the natural, verified bridge anchor.
"""
from __future__ import annotations

import os
import sys

PHI_MINPOLY = [1, -1, -1]            # x^2 - x - 1  ==  the void law x^2 = x + 1
PHI_COMPANION = [[0, 1], [1, 1]]     # loom.companion(PHI_MINPOLY, order="high")
PHI_CL = [0.5, 1.0, -0.5, 0.0]       # unmat(companion) in Cl(2,0)  (shared mat/cl convention)
_PHI = (1 + 5 ** 0.5) / 2

CL_TOL = 1e-12
MAHLER_TOL = 1e-6


def _ensure_loom_on_path() -> str:
    """Append the L00M clone to sys.path (one-way). Returns the resolved root."""
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.environ.get("KIRA_LANG_L00M_ROOT") or os.path.normpath(
        os.path.join(here, os.pardir, os.pardir, "L00M")   # ../../L00M : the package sits one level under the repo root
    )
    if os.path.isdir(root) and root not in sys.path:
        sys.path.append(root)            # APPEND: never shadows local modules
    return root


def _cl_from_companion(comp):
    """Carrier coords from a 2x2 companion via the shared mat/cl convention (loom-free)."""
    p, q, r, s = comp[0][0], comp[0][1], comp[1][0], comp[1][1]
    return [(p + s) / 2.0, (q + r) / 2.0, (p - s) / 2.0, (r - q) / 2.0]


def phi_keystone() -> dict:
    """Confirm the phi keystone against LIVE loom, read-only and one-way. Never raises."""
    root = _ensure_loom_on_path()
    try:
        import loom
    except Exception as e:                                   # loom absent: report, do not crash
        return {"loom_reachable": False, "loom_root": root, "error": repr(e)}
    try:
        comp = loom.companion(PHI_MINPOLY, order="high")
        comp = [[int(c) for c in row] for row in comp]       # normalize Matrix -> list[list[int]]
        charpoly = [int(c) for c in loom.charpoly(comp)]
        mahler = float(loom.mahler_measure(PHI_MINPOLY))
        cl = _cl_from_companion(comp)
        agree = (
            comp == PHI_COMPANION
            and charpoly == PHI_MINPOLY
            and all(abs(a - b) < CL_TOL for a, b in zip(cl, PHI_CL))
            and abs(mahler - _PHI) < MAHLER_TOL
        )
        return {
            "loom_reachable": True,
            "loom_root": root,
            "minpoly": charpoly,
            "companion": comp,
            "cl_coords": cl,
            "mahler": mahler,
            "phi": _PHI,
            "agree": bool(agree),
            "tol": {"cl": CL_TOL, "mahler": MAHLER_TOL},
        }
    except Exception as e:                                   # loom present but call failed: report
        return {"loom_reachable": True, "loom_root": root, "error": repr(e)}
