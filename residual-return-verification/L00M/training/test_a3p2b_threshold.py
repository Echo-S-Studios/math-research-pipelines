"""test_a3p2b_threshold.py -- A3.P2b RESEARCH probe: the GROW threshold = information gain vs cost.

Reproducible evidence for A3_P2B_RESEARCH.md. RESEARCH only -- it imports the shipped capacity gate to
COMPARE against, but modifies nothing. The derived rule:

    GAIN   = ||r||^2_G = n * Fisher(r)            (P2a: degree-scaled Fisher information of the residual)
    COST   = lambda * log M(theta),  M = H^deg    (Arakelov/Northcott arithmetic cost; log M = entropy)
    FLOOR  = lambda * log mu_L  > 0               (Lehmer/Smyth: M >= mu_L > 1 -> a NONZERO minimum cost)
    GROW iff  Northcott-admissible (exact, A3.P0+P1)  AND  GAIN >= COST  ( >= FLOOR for any seed ).

Exact pieces (||r||^2_G, landau_bound_sq, Northcott admissibility) stay exact; the threshold itself is
intrinsically float (log M transcendental) -- flagged in the doc. lambda and the effective Lehmer
constant are conjectural; this probe pins the LOGIC and the subsumption. lambda is the DERIVED identity 2c
(test_a3p2c_lambda_conformal.py, companion Thm 4.6); the reciprocal (Lehmer) floor remains OPEN.
"""
import math
import os
import sys
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from capacity import (is_admissible, landau_bound_sq, coeff_height, mahler_float,
                      Budget, capacity_decision)

# Mahler-measure floors (theorems / conjecture). Smyth's bound is a THEOREM for non-reciprocal theta.
MU_SMYTH = 1.3247179572447458     # plastic number, root of x^3 - x - 1 (non-reciprocal floor; THEOREM)
MU_LEHMER = 1.1762808182599175    # smallest known Salem (conjectural universal floor)
LAMBDA = 2                         # = 2c at c=1 (Gaussian); lambda = 2c is now DERIVED (Thm 4.6; test_a3p2c). [FORCED]

# The shipped GROW cases (the actual learner/compositum residual norms + their seed minpolys):
#   2*sqrt6 in Q(sqrt2+sqrt3):  ||r||^2_G = 96, seed x^2-24 (M=24);  ambient degree n=4
#   sqrt7   in Q(sqrt2,sqrt3,sqrt7) compositum: field-residual 56, seed x^2-7 (M=7); n=8
GROW_CASES = [("2*sqrt6", Fraction(96), [1, 0, -24], 4),
              ("sqrt7",   Fraction(56), [1, 0, -7], 8)]


def _cost(seed_minpoly, lam=LAMBDA):
    return lam * math.log(mahler_float(seed_minpoly))         # lambda * log M(theta)  (float; research)


def _floor(n, lam=LAMBDA, mu=MU_SMYTH, degree_aware=False):
    return (n if degree_aware else 1) * lam * math.log(mu)    # lambda * log mu_L, optionally * n


def _proposed_decision(gain, seed_minpoly, n, budget, *, degree_aware=False):
    """The A3.P2b PROPOSED rule (NOT shipped). gain = ||r||^2_G (exact Fraction); the rest float."""
    if not is_admissible(seed_minpoly, budget):
        return "REJECT"                                       # Northcott (exact, unchanged from A3.P0+P1)
    if float(gain) < _floor(n, degree_aware=degree_aware):
        return "STOP"                                         # below the Lehmer-floor minimum cost
    if float(gain) < _cost(seed_minpoly):
        return "STOP"                                         # gain does not cover THIS seed's cost
    return "GROW"


# -- (1) the derived threshold SUBSUMES the shipped GROW cases ---------------- #
def test_a3p2b_threshold_subsumes_grow_cases():
    big = Budget(degree_max=64, height_max=256)
    for name, gain, mp, n in GROW_CASES:
        # the shipped gate (floor=0) GROWs these
        assert capacity_decision(mp, gain, big).decision == "GROW", name
        # the derived gain-vs-cost threshold ALSO clears (gain >> cost), with or without the degree-aware floor
        assert float(gain) >= _cost(mp), f"{name}: gain {gain} < cost {_cost(mp):.3f}"
        assert _proposed_decision(gain, mp, n, big) == "GROW", name
        assert _proposed_decision(gain, mp, n, big, degree_aware=True) == "GROW", name


# -- (2) the Lehmer floor is a NONZERO minimum -> sub-floor residual: shipped GROWs, proposed STOPS -- #
def test_a3p2b_lehmer_floor_is_nonzero_and_changes_subthreshold():
    assert _floor(1) > 0 and MU_SMYTH > 1                     # a positive minimum cost exists (theorem, non-recip)
    tiny = Fraction(1, 10)                                    # a tiny but nonzero off-axis residual
    seed = [1, 0, -24]
    big = Budget(degree_max=64, height_max=256)
    # shipped gate: floor = 0 -> a nonzero residual is NOT stopped (it would grow if admissible)
    assert capacity_decision(seed, tiny, big).decision == "GROW"
    # proposed gate: floor = lambda*log(mu) ~ 0.56 -> the tiny residual is STOPPED (below the cheapest seed)
    assert float(tiny) < _floor(4)
    assert _proposed_decision(tiny, seed, 4, big) == "STOP"


# -- (3) the DEGREE-AWARE floor (n-scaled) differs from the constant floor ----- #
def test_a3p2b_degree_aware_floor_differs():
    seed = [1, 0, -7]
    big = Budget(degree_max=64, height_max=256)
    gain = Fraction(1)                                        # gain that clears the constant floor but not n*floor
    assert float(gain) >= _floor(8, degree_aware=False)       # constant floor ~0.56 -> passes
    assert float(gain) < _floor(8, degree_aware=True)         # degree-aware floor 8*lambda*0.28 ~4.50 -> below
    assert _proposed_decision(gain, seed, 8, big, degree_aware=False) in ("GROW", "STOP")  # cost may still bind
    assert _proposed_decision(gain, seed, 8, big, degree_aware=True) == "STOP"             # degree-aware STOPS it


# -- (4) the exact pieces stay EXACT (admissibility + Landau bound are integers) -- #
def test_a3p2b_exact_pieces_unchanged():
    # the COST/threshold is float (log M), but the certified admissibility + Landau bound are exact ints
    assert landau_bound_sq([1, 0, -24]) == 577 and coeff_height([1, 0, -24]) == 24
    assert is_admissible([1, 0, -24], Budget(64, 256)) is True
    assert is_admissible([1, 0, -24], Budget(64, 10)) is False
    # and ||r||^2_G enters the threshold as an EXACT Fraction (no float on the gain side)
    assert isinstance(GROW_CASES[0][1], Fraction)


def test_a3p2b_model_layer_no_kira():
    assert "kira_server_canonical" not in sys.modules
