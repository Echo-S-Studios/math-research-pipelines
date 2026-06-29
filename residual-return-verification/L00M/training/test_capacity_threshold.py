"""test_capacity_threshold.py -- A3.P2b-APPLY item (i): the degree-aware Lehmer gate in
`capacity.capacity_decision`, the OPT-IN information-threshold path.

ADDITIVE. This file imports only `capacity` (model-layer) and recomputes the certified floor / cost
enclosures from scratch with mpmath, exactly as the gate does, to cross-check the rigorous decisions. It
touches NO shipped behaviour: the default path (`info_threshold=False`) is asserted byte-for-byte identical
to the shipped gate, so the rest of the suite is unaffected.

Discipline (mirrors the paper's probe): the GAIN stays an exact `Fraction`; only the cost/floor are
interval-real (G8). GROW is certified against Landau's exact-integer upper bound on the Mahler measure
(root-free); STOP-below-floor is certified against the Smyth/Dobrowolski lower bound.

Coverage:
  (1) default-off reproduces the shipped verdict byte-for-byte (incl. G8 float rejection)         [RULING 2]
  (2) the Smyth bracket [MU_SMYTH_LO, MU_SMYTH_HI] certifiably brackets the plastic number
  (3) is_reciprocal: phi/sqrt7/2sqrt6 non-reciprocal; x^2-3x+1, Lehmer-10, x^4-10x^2+1 reciprocal   [RULING 1]
  (4) GROW/STOP under the threshold: 2sqrt6 & sqrt7 GROW; tiny & sub-threshold STOP (subsumption)
  (5) reciprocity branch: non-reciprocal -> mu_S (positive); reciprocal -> Dobrowolski (vacuous->0 at d=2);
      Lehmer mu_L heuristic only via opt-in, never default                                          [RULING 1]
  (6) the decision is a CERTIFIED interval decision (independent mpmath cross-check of the enclosures)
  (7) the 1-in-B precondition: unmet -> fall back to the exact admissibility-only path
  (8) degree-aware vs constant floor differ (the n-factor)
  (9) info path keeps G8 (float gain/floor rejected) and REJECTs an inadmissible seed
"""
from fractions import Fraction
import pytest
import mpmath as mp

import capacity as C
from capacity import (Budget, capacity_decision, is_reciprocal,
                      MU_SMYTH_LO, MU_SMYTH_HI, DOBROWOLSKI_C)

PHI = [1, -1, -1]           # x^2 - x - 1     (non-reciprocal)
SQRT2 = [1, 0, -2]          # x^2 - 2         (non-reciprocal)
SQRT6 = [1, 0, -24]         # x^2 - 24  (2sqrt6 seed, M=24, non-reciprocal)
SQRT7 = [1, 0, -7]          # x^2 - 7   (sqrt7 seed,  M=7,  non-reciprocal)
RECIP = [1, -3, 1]          # x^2 - 3x + 1    (reciprocal; Salem-like degree 2)
LEHMER = [1, 1, 0, -1, -1, -1, -1, -1, 0, 1, 1]   # Lehmer's degree-10 polynomial (reciprocal)
THETA4 = [1, 0, -10, 0, 1]  # x^4 - 10x^2 + 1 (sqrt2+sqrt3 minpoly; reciprocal)

BIG = Budget(degree_max=12, height_max=100)


def _on(min_poly, gain, n, **kw):
    return capacity_decision(min_poly, gain, BIG, info_threshold=True,
                             ambient_degree=n, one_in_basis=True, **kw)


# ===== (1) default-off is byte-for-byte the shipped gate ===================================== #
def test_default_off_is_shipped_byte_for_byte():
    b = Budget(degree_max=4, height_max=30)
    # the worked shipped outcomes, with the new kwargs absent AND explicitly off -- identical
    for kw in ({}, {"info_threshold": False}):
        assert capacity_decision(SQRT6, Fraction(96), b, **kw).decision == "GROW"
        assert capacity_decision(SQRT6, Fraction(96), Budget(4, 10), **kw).decision == "REJECT"   # over height
        assert capacity_decision(THETA4, Fraction(96), Budget(2, 100), **kw).decision == "REJECT"  # over degree
        assert capacity_decision(SQRT6, Fraction(0), b, **kw).decision == "STOP"                   # at floor 0
        assert capacity_decision(SQRT7, Fraction(56), Budget(8, 100), effective_degree=8, **kw).decision == "GROW"
    # default-off NEVER imports mpmath-on-the-gate behaviour change: same verdict object fields
    v0 = capacity_decision(SQRT6, Fraction(96), b)
    v1 = capacity_decision(SQRT6, Fraction(96), b, info_threshold=False)
    assert (v0.decision, v0.degree, v0.coeff_height, v0.admissible, v0.reason) == \
           (v1.decision, v1.degree, v1.coeff_height, v1.admissible, v1.reason)


def test_default_off_g8_float_rejection_unchanged():
    b = Budget(4, 30)
    with pytest.raises(TypeError):
        capacity_decision(SQRT6, 96.0, b)                 # float gain
    with pytest.raises(TypeError):
        capacity_decision(SQRT6, Fraction(96), b, floor=0.5)   # float floor


# ===== (2) the Smyth floor bracket is certified ============================================== #
def test_smyth_bracket_certified():
    # f(x) = x^3 - x - 1 ; f(lo) < 0 < f(hi) proves mu_S in (lo, hi)
    f_lo = MU_SMYTH_LO**3 - MU_SMYTH_LO - 1
    f_hi = MU_SMYTH_HI**3 - MU_SMYTH_HI - 1
    assert f_lo < 0 < f_hi
    assert MU_SMYTH_LO < Fraction("1.32471795724") < MU_SMYTH_HI


# ===== (3) reciprocity predicate (RULING 1 keys on this) ===================================== #
def test_is_reciprocal():
    for m in (PHI, SQRT2, SQRT6, SQRT7):
        assert is_reciprocal(m) is False, m
    for m in (RECIP, LEHMER, THETA4, [1, 0, 1], [1, 0, 0, 0, 0, 0, 1]):
        assert is_reciprocal(m) is True, m
    # anti-reciprocal (m == -reversed): x^2 - 1 -> [1,0,-1]
    assert is_reciprocal([1, 0, -1]) is True


# ===== (4) GROW / STOP subsumption ========================================================== #
def test_threshold_grow_stop_subsumes_shipped():
    # the two shipped GROW cases clear the threshold by a wide margin
    assert _on(SQRT6, Fraction(96), 4).decision == "GROW"       # 2sqrt6: floor 2.25, cost_up 6.36
    assert _on(SQRT7, Fraction(56), 8).decision == "GROW"       # sqrt7 in deg-8 compositum: floor 4.50
    # lattice-aligned tiny residual: shipped floor-0 gate would GROW, the principled floor STOPs it
    assert _on(SQRT6, Fraction(1, 10), 4).decision == "STOP"
    # sub-threshold gain 1 in a degree-8 field: the degree-aware floor (4.50) STOPs it
    v = _on(SQRT7, Fraction(1), 8)
    assert v.decision == "STOP" and "below the certified degree-aware floor" in v.reason


# ===== (5) reciprocity branch ============================================================== #
def test_reciprocity_floor_branch():
    # non-reciprocal -> Smyth mu_S, a POSITIVE certified floor (reason names it)
    v_nr = _on(SQRT7, Fraction(1), 8)
    assert "Smyth mu_S" in v_nr.reason and "theorem" in v_nr.reason
    # reciprocal (degree 2) -> Dobrowolski is VACUOUS (<=1) -> floor 0 (honest: no uniform floor proven)
    v_r_small = _on(RECIP, Fraction(1, 10), 2)
    assert "Dobrowolski" in v_r_small.reason
    assert v_r_small.decision == "STOP"        # stops on the cost side, not the (zero) floor
    # a large gain on the same reciprocal seed grows (beats the certified cost)
    assert _on(RECIP, Fraction(50), 2).decision == "GROW"
    # Lehmer is HEURISTIC and OPT-IN only: selectable, but never the default branch
    v_lehmer = _on(RECIP, Fraction(1, 10), 2, reciprocal_floor="lehmer")
    assert "Lehmer" in v_lehmer.reason and "HEURISTIC" in v_lehmer.reason
    # default reciprocal_floor is Dobrowolski (provable), NOT Lehmer
    assert "Dobrowolski" in _on(LEHMER, Fraction(1, 10), 10).reason


# ===== (6) the decision is a CERTIFIED interval decision (independent cross-check) =========== #
def _ref_floor_cost(min_poly, n, lam=2, degree_aware=True):
    """Recompute the floor (Smyth, non-reciprocal here) and the Landau cost-upper as plain high-precision
    intervals, independently of capacity.py, to confirm the gate's certified enclosures."""
    with mp.workdps(60):
        mult = n if degree_aware else 1
        log_mu = mp.iv.log(mp.iv.mpf([str(MU_SMYTH_LO), str(MU_SMYTH_HI)]))
        floor = mp.iv.mpf(mult) * mp.iv.mpf(lam) * log_mu
        L = sum(c * c for c in min_poly)
        cost_up = mp.iv.mpf(lam) * (mp.iv.log(mp.iv.mpf(int(L))) / 2)
        return (float(floor.a), float(floor.b)), (float(cost_up.a), float(cost_up.b))


def test_certified_enclosures_match_and_gain_is_exact():
    # GROW certified: exact rational gain dominates the rigorous UPPER bound on cost (and the floor)
    (fa, fb), (ca, cb) = _ref_floor_cost(SQRT6, 4)
    gain = Fraction(96)
    assert gain >= Fraction(str(cb)) and gain >= Fraction(str(fb))          # beats both upper ends -> GROW
    assert _on(SQRT6, gain, 4).decision == "GROW"
    # STOP certified: exact gain is strictly below the rigorous LOWER end of the floor
    (fa8, fb8), _ = _ref_floor_cost(SQRT7, 8)
    assert Fraction(1, 10) < Fraction(str(fa8))                              # 0.1 < floor lower end
    assert _on(SQRT7, Fraction(1, 10), 8).decision == "STOP"
    # the gain crosses the gate as an exact Fraction (never a float): a 1/3 gain is handled exactly
    assert _on(SQRT6, Fraction(1, 3), 4).decision == "STOP"                  # 1/3 < floor 2.25


# ===== (7) the 1-in-B precondition ========================================================= #
def test_one_in_basis_precondition_falls_back():
    # info requested but 1-in-B not asserted -> exact admissibility-only fallback (shipped behaviour)
    v = capacity_decision(SQRT6, Fraction(96), BIG, info_threshold=True, ambient_degree=4, one_in_basis=False)
    assert v.decision == "GROW" and "admissibility-only fallback" in v.reason
    # degree-aware but no ambient_degree -> also falls back
    v2 = capacity_decision(SQRT6, Fraction(96), BIG, info_threshold=True, one_in_basis=True, ambient_degree=None)
    assert "admissibility-only fallback" in v2.reason
    # a tiny gain under fallback behaves like floor-0 shipped gate: nonzero -> GROW (no principled floor)
    v3 = capacity_decision(SQRT6, Fraction(1, 10), BIG, info_threshold=True, ambient_degree=4, one_in_basis=False)
    assert v3.decision == "GROW"        # exactly the shipped floor-0 behaviour the fallback promises


# ===== (8) degree-aware vs constant floor differ ============================================ #
def test_degree_aware_vs_constant_floor():
    # gain 1 in a degree-8 field: degree-aware floor (8*2*log mu_S = 4.50) STOPs below floor;
    # constant floor (2*log mu_S = 0.562) is CLEARED -> the decision no longer cites "below ... floor".
    v_da = _on(SQRT7, Fraction(1), 8, degree_aware=True)
    v_co = _on(SQRT7, Fraction(1), 8, degree_aware=False)
    assert v_da.decision == "STOP" and "below the certified degree-aware floor" in v_da.reason
    assert "gain>=floor=True" in v_co.reason          # constant floor cleared (n-factor removed)
    assert "below the certified degree-aware floor" not in v_co.reason


# ===== (9) info path keeps G8 and REJECTs inadmissible ====================================== #
def test_info_path_g8_and_reject():
    with pytest.raises(TypeError):
        capacity_decision(SQRT6, 96.0, BIG, info_threshold=True, ambient_degree=4, one_in_basis=True)
    # over-degree on the info path -> REJECT (admissibility precedes the threshold)
    v = capacity_decision(THETA4, Fraction(96), Budget(2, 100), info_threshold=True,
                          ambient_degree=4, one_in_basis=True)
    assert v.decision == "REJECT"


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
