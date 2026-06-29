"""test_kl_dta_conformance.py -- the THIRD independent route.

KL_DTA.py already verifies its Clifford algebra Cl(2,0) two ways (its "two-route
closure"): the cocycle/Cl route (Cl.__mul__, tr, det, ...) and the numpy 2x2
matrix route (mat/mmul/mdet). This file adds loom's EXACT integer companion-matrix
route as a third, independent witness -- proving KL_DTA's Cl(2,0) and loom's exact
2x2 companion algebra are the SAME M2(R).

Guardrail posture (mirrors test_conformance.py): importing BOTH loom and KL_DTA is
fine HERE because this is a TEST -- neither kernel imports the other, so G9's
kernel-independence is preserved; the bridge lives ONLY in this test. KL_DTA stays
standalone (it is wired into nothing). loom's arithmetic stays exact (Fraction/int);
only the cross-route float comparison carries a tolerance (G8 intact).

loom.charpoly RAISES on a non-integer matrix, so we feed it ONLY integer 2x2
companions and assert integrality before crossing the bridge (G10 discipline: the
exact route only ever sees integer matrices).

The anchor is the phi keystone -- the void law x^2 = x + 1, minpoly [1,-1,-1],
companion [[0,1],[1,1]], which is Cl(0.5, 1, -0.5, 0) under KL_DTA's mat/unmat iso.
"""
import cmath
import itertools
import math
import os
import subprocess
import sys

import numpy as np
import pytest

import loom
import KL_DTA
from KL_DTA import Cl, ONE, VOID, tr, det, disc, mat, unmat, Phi, res

# KL_DTA is float (1e-12 internal tol); loom is exact (int/Fraction) with a float
# Durand-Kerner display layer. Two tolerances for the cross-route comparison:
ALG_TOL = 1e-9   # algebraic invariants: KL_DTA float vs loom exact-cast-to-float (effectively exact)
DK_TOL = 1e-6    # Durand-Kerner float layer (eigenvalues, Mahler) -- matches test_conformance.py


# ── The bridge set: integer 2x2 companions (so loom's exact route accepts them) ───────────────
# (label, high-to-low monic integer minpoly). loom.companion builds the exact integer
# matrix; unmat lifts it into Cl(2,0). We never hardcode the matrix/Cl literals (except
# the keystone, asserted) -- they are derived, so a transcription slip can't pass silently.
COMPANION_POLYS = [
    ("phi_voidlaw", [1, -1, -1]),   # x^2 - x - 1  == the void law x^2 = x + 1 ; companion [[0,1],[1,1]]
    ("x2_3x_p1",    [1, -3, 1]),    # x^2 - 3x + 1 ; real spectrum (3 +/- sqrt5)/2
    ("x2_m1",       [1, 0, -1]),    # x^2 - 1      ; roots +/-1
    ("x2_x_p1",     [1, -1, 1]),    # x^2 - x + 1  ; disc < 0, COMPLEX spectrum (exercises the complex path)
]


def _bridge_items():
    items = []
    for label, poly in COMPANION_POLYS:
        C = loom.companion(poly, order="high")          # exact integer 2x2 (list-of-lists)
        X = unmat(np.array(C, dtype=float))             # the corresponding Cl(2,0) element
        items.append((label, poly, C, X))
    return items


BRIDGE = _bridge_items()
IDS = [b[0] for b in BRIDGE]


def _int_mat(X):
    """KL_DTA.mat(X) as an integer list-of-lists; assert integrality FIRST (loom would raise)."""
    m = mat(X)
    out = []
    for i in range(2):
        row = []
        for j in range(2):
            v = float(m[i][j])
            assert abs(v - round(v)) < ALG_TOL, f"non-integer entry {v}: loom's exact route would raise"
            row.append(int(round(v)))
        out.append(row)
    return out


def _kl_spectrum(X):
    """KL_DTA's spectrum: roots of Y^2 - tr(X)Y + det(X) via its own discriminant. Handles complex."""
    t, d = tr(X), det(X)
    s = cmath.sqrt(t * t - 4.0 * d)
    return sorted([(t + s) / 2.0, (t - s) / 2.0], key=lambda z: (z.real, z.imag))


def _loom_spectrum(poly):
    return sorted((complex(z) for z in loom.eigenvalues(poly)), key=lambda z: (z.real, z.imag))


# ── (1) The __main__ guard: importing KL_DTA must NOT run the verdict ─────────────────────────

def test_importing_kl_dta_does_not_run_verdict():
    """The __main__ guard keeps `import KL_DTA` side-effect-free -- no verdict printed."""
    here = os.path.dirname(os.path.abspath(__file__))
    proc = subprocess.run([sys.executable, "-c", "import KL_DTA"],
                          cwd=here, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == ""
    assert "KL_DTA verified" not in proc.stdout


# ── (2) Round-trip: loom companion <-> Cl(2,0), both directions ───────────────────────────────

@pytest.mark.parametrize("label,poly,C,X", BRIDGE, ids=IDS)
def test_companion_roundtrip(label, poly, C, X):
    """loom.companion -> Cl -> mat == the same integer companion ; KL_DTA's iso is involutive."""
    assert _int_mat(X) == C
    assert unmat(mat(X)) == X


# ── (3) The phi keystone, all three routes ────────────────────────────────────────────────────

def test_phi_keystone():
    """The void law x^2 = x + 1: companion [[0,1],[1,1]] == Cl(0.5,1,-0.5,0), invariants agree."""
    poly = [1, -1, -1]
    C = loom.companion(poly, order="high")
    assert C == [[0, 1], [1, 1]]                                  # the void-law companion
    X0 = unmat(np.array(C, dtype=float))
    assert X0 == Cl(0.5, 1.0, -0.5, 0.0)                          # the (corrected) worked seed
    assert _int_mat(X0) == [[0, 1], [1, 1]]                       # round-trips back exactly
    # KL_DTA Cl-route invariants
    assert abs(tr(X0) - 1.0) < ALG_TOL                            # trace 1
    assert abs(det(X0) - (-1.0)) < ALG_TOL                        # det -1
    assert abs(disc(X0) - 5.0) < ALG_TOL                          # discriminant 5 (= d_F of Q(sqrt5))
    # loom exact route, same matrix
    assert loom.charpoly(C) == [1, -1, -1]
    assert loom.trace(C) == 1
    assert loom.charpoly(C)[-1] == -1                             # c_0 == det
    # Mahler measure == phi (the void law's growth rate)
    assert abs(loom.mahler_measure(poly) - KL_DTA.PHI) < DK_TOL


# ── (4) Cayley-Hamilton agreement: X kills its own charpoly, and it's loom's charpoly ──────────

@pytest.mark.parametrize("label,poly,C,X", BRIDGE, ids=IDS)
def test_cayley_hamilton_agreement(label, poly, C, X):
    # KL_DTA: Phi_X(X) = X^2 - tr(X)X + det(X)*1 == 0
    assert res(Phi(X, X), VOID) < ALG_TOL
    # loom's exact charpoly of the same matrix == [1, -tr, det] == the seed poly
    cp = loom.charpoly(_int_mat(X))
    assert cp == poly
    assert all(abs(float(a) - b) < ALG_TOL
               for a, b in zip(cp, [1.0, -tr(X), det(X)]))


# ── (5) det multiplicativity in BOTH routes, cross-checked ────────────────────────────────────

def test_det_multiplicativity_cross_route():
    """det(X.Y) = det(X)det(Y): KL_DTA Cl-route AND loom's exact integer route agree."""
    for (_, _, _, X), (_, _, _, Y) in itertools.product(BRIDGE, BRIDGE):
        XY = X * Y
        # KL_DTA Cl-route (float)
        assert abs(det(XY) - det(X) * det(Y)) < ALG_TOL
        # loom exact route on the same matrices (the Cl product maps to the matrix product)
        dX = loom.charpoly(_int_mat(X))[-1]
        dY = loom.charpoly(_int_mat(Y))[-1]
        dXY = loom.charpoly(_int_mat(XY))[-1]
        assert dXY == dX * dY                                     # exact integer identity
        assert abs(det(XY) - float(dXY)) < ALG_TOL               # cross-route: float == exact


# ── (6) Spectrum agreement: KL_DTA disc-route == loom Durand-Kerner ───────────────────────────

@pytest.mark.parametrize("label,poly,C,X", BRIDGE, ids=IDS)
def test_spectrum_agreement(label, poly, C, X):
    kl = _kl_spectrum(X)
    lm = _loom_spectrum(poly)
    assert len(kl) == len(lm) == 2
    for a, b in zip(kl, lm):
        assert abs(a - b) < DK_TOL


# ── (7) THE PAYOFF: three-route closure on the phi keystone ───────────────────────────────────

def test_three_route_closure_on_phi_keystone():
    """KL_DTA's two-route closure promoted to THREE: Cl cocycle route, KL_DTA numpy-matrix
    route, and loom's exact integer companion route all agree on tr/det/charpoly/spectrum
    for the void-law keystone x^2 = x + 1."""
    poly = [1, -1, -1]
    C = loom.companion(poly, order="high")
    X = unmat(np.array(C, dtype=float))
    Mx = mat(X)

    # trace & det in all three routes
    cl_route = (tr(X), det(X))                                    # route 1: Cl cocycle
    np_route = (KL_DTA.mtr(Mx), KL_DTA.mdet(Mx))                  # route 2: KL_DTA numpy matrix
    loom_route = (float(loom.trace(C)), float(loom.charpoly(C)[-1]))  # route 3: loom exact companion
    for route in (cl_route, np_route, loom_route):
        assert abs(route[0] - 1.0) < ALG_TOL                     # trace == 1
        assert abs(route[1] - (-1.0)) < ALG_TOL                  # det == -1

    # characteristic polynomial: all three agree on x^2 - x - 1
    assert loom.charpoly(C) == [1, -1, -1]
    assert all(abs(float(a) - b) < ALG_TOL
               for a, b in zip(loom.charpoly(C), [1.0, -tr(X), det(X)]))

    # spectrum: Cl disc-route vs loom Durand-Kerner (== golden ratio and its conjugate)
    kl, lm = _kl_spectrum(X), _loom_spectrum(poly)
    for a, b in zip(kl, lm):
        assert abs(a - b) < DK_TOL
    assert abs(max(kl, key=lambda z: z.real).real - KL_DTA.PHI) < DK_TOL

    # the closure's fixed point: X kills its own characteristic polynomial (Cayley-Hamilton)
    assert res(Phi(X, X), VOID) < ALG_TOL
    # and the growth rate is phi
    assert abs(loom.mahler_measure(poly) - KL_DTA.PHI) < DK_TOL
