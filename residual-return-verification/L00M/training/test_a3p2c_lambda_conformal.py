"""test_a3p2c_lambda_conformal.py -- A3.P2c probe: the exchange rate is the DERIVED identity lambda = 2c.

Companion to Section 4.3 of residual_return_learning.tex (Theorem: lambda = 2c) and the substrate's
"no canonical model" conjecture. RESEARCH probe: it imports the shipped capacity gate to COMPARE
against, and mutates nothing. It is written for EXTRAPOLATION -- lambda = 2c is SOLVED from the MDL
balance at run time, not hard-coded; the shipped value LAMBDA = 2 must then EMERGE as the c = 1 instance,
and the degree-aware reading as the c = n instance.

    GAIN  = ||r||^2_G = n * Fisher(r)              (P2a, exact Fraction; the conformal choice c does NOT
                                                    change the gain -- it is a fixed geometric quantity)
    D_KL  = (1/(2c)) * ||r||^2_G                   (2nd-order KL with Fisher = G/c)
    COST  = lambda * log M(theta)                  (entropy; log M transcendental)
    balance:  D_KL >= log M  <=>  ||r||^2_G >= 2c * log M   =>   lambda = 2c   (FORCED identity)

In capacity.py the conformal constant c is carried by `mult = (ambient_degree if degree_aware else 1)`:
the floor mult*lam*log(mu_S) is exactly 2c*log(mu_S) with lam = 2 the structural "2" and mult the "c".

Exact pieces (||r||^2_G, the self-action spectrum, the gate ladder) stay exact (sympy / Fraction); only
log(mu) is transcendental and is bracketed by the certified Smyth interval [MU_SMYTH_LO, MU_SMYTH_HI].
"""
import math
import os
import sys
from fractions import Fraction

import sympy as sp

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from capacity import (Budget, capacity_decision, is_reciprocal, mahler_float,
                      MU_SMYTH_LO, MU_SMYTH_HI)

MU_SMYTH = 1.3247179572447458     # plastic number, root of x^3 - x - 1 (non-reciprocal floor; Smyth THEOREM)

# Shipped GROW cases: (name, exact residual norm ||r||^2_G, seed minpoly, ambient degree n).
GROW_CASES = [("2*sqrt6", Fraction(96), [1, 0, -24], 4),
              ("sqrt7",   Fraction(56), [1, 0,  -7], 8)]


# -- (1) lambda = 2c is DERIVED, not posited (solved symbolically; the shipped 2 must EMERGE) ---- #
def test_lambda_is_two_c_derived():
    c, gain, logM = sp.symbols("c gain logM", positive=True)
    lam = sp.solve(sp.Eq(gain / (2 * c), logM), gain)[0] / logM   # gain at the MDL balance, per unit logM
    assert sp.simplify(lam - 2 * c) == 0                          # FORCED: lambda = 2c
    assert sp.simplify(lam.subs(c, 1) - 2) == 0                   # c = 1 -> lambda = 2  (shipped value emerges)
    n = sp.Symbol("n", positive=True)
    assert sp.simplify(lam.subs(c, n) - 2 * n) == 0              # c = n -> lambda = 2n (degree-aware reading)


# -- (2) the two shipped floors are the two readings of 2c*log(mu_S) ----------------------------- #
def test_floors_unify_under_lambda_2c():
    floor = lambda c, n=1: 2 * c * n * math.log(MU_SMYTH)
    assert round(floor(1), 4) == 0.5624          # c = 1: the constant floor
    assert round(floor(1, 4), 4) == 2.2496       # c = n = 4: degree-aware floor
    assert round(floor(1, 8), 4) == 4.4992       # c = n = 8: degree-aware floor
    # the certified Smyth bracket really does contain mu_S (so the interval gate is rigorous)
    assert MU_SMYTH_LO <= Fraction(MU_SMYTH).limit_denominator(10 ** 10) <= MU_SMYTH_HI


# -- (3) shipped GROW decisions are INVARIANT across c in [1, n] (the REAL capacity gate) -------- #
def test_shipped_decisions_invariant_in_c():
    # c is carried by the engine's  mult = (ambient_degree if degree_aware else 1);  lam stays the base "2",
    # so the effective rate mult*lam = 2c. Verify the shipped GROW holds for BOTH readings: c=1 and c=n.
    budget = Budget(degree_max=8, height_max=64)
    for name, gain, seed, n in GROW_CASES:
        for degree_aware in (False, True):        # c = 1 (mult = 1)  and  c = n (mult = n)
            v = capacity_decision(seed, gain, budget, info_threshold=True, one_in_basis=True,
                                  ambient_degree=n, lam=2, degree_aware=degree_aware)
            assert v.decision == "GROW", (name, "c=n" if degree_aware else "c=1", v.decision, v.reason)


# -- (4) the DEFAULT path (info_threshold off) is byte-for-byte unchanged by lam/c --------------- #
def test_default_path_unchanged_by_c():
    budget = Budget(degree_max=8, height_max=64)
    seed, gain = [1, 0, -24], Fraction(96)
    base = capacity_decision(seed, gain, budget)                 # the shipped default verdict
    for c in (1, 2, 4, 7):
        v = capacity_decision(seed, gain, budget, lam=2 * c)    # lam must never touch the default path
        assert (v.decision, v.reason) == (base.decision, base.reason)


# -- (5) self-action spectrum {0, +-sqrt(1+4C)} and the forced gate ladder sqrt(1+4C) in {2,3,5} - #
def test_self_action_spectrum_and_gate_ladder():
    for C, gap2 in [(sp.Rational(1, 4), 2), (sp.Rational(1, 2), 3), (sp.Integer(1), 5)]:
        R = sp.Matrix([[0, C], [1, -1]])                        # companion of x^2 + x - C
        E = [sp.Matrix([[1, 0], [0, 0]]), sp.Matrix([[0, 1], [0, 0]]),
             sp.Matrix([[0, 0], [1, 0]]), sp.Matrix([[0, 0], [0, 1]])]
        ad = sp.Matrix([[(R * e - e * R)[i, j] for i in range(2) for j in range(2)] for e in E]).T
        eig = ad.eigenvals()
        assert sp.Integer(0) in eig                             # the captured (0) channel persists
        assert all(sp.simplify(e ** 2 - gap2) == 0 for e in eig if e != 0)   # gap^2 = 1 + 4C
        assert sp.simplify(sp.sqrt(1 + 4 * C) - sp.sqrt(gap2)) == 0          # ladder: sqrt2, sqrt3, sqrt5
    # golden-gate frame-shift value c = sqrt(1+4C)/(2C) at C = 1 is sqrt5/2
    assert sp.simplify(sp.sqrt(1 + 4 * sp.Integer(1)) / (2 * 1) - sp.sqrt(5) / 2) == 0


# -- (6) the forced FLIP: the frame-shift c (hence the metric G/c) goes real -> imaginary at C=-1/4 #
def test_discriminant_flip_threshold():
    C = sp.Symbol("C", real=True)
    D = 1 + 4 * C                                                # discriminant of x^2 + x - C
    assert sp.solve(sp.Eq(D, 0), C) == [sp.Rational(-1, 4)]      # the unique flip / PARADOX point
    c_frame = sp.sqrt(1 + 4 * C) / (2 * C)                       # the frame-shift conformal constant
    assert sp.im(c_frame.subs(C, sp.Integer(1))) == 0           # D > 0: c real  -> G/c is PD (Fisher valid)
    assert sp.re(c_frame.subs(C, sp.Integer(-1))) == 0          # D < 0: c imaginary -> rotation, metric indefinite
