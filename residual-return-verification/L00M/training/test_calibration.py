"""test_calibration.py -- the concrete variance calibration over the Welford accumulator.

Closes the previously-unused per-coordinate Welford variance ``_M2`` by giving it a real consumer:
``variance_calibration``. Persistence (the streak) tests that the residual DIRECTION holds; calibration
tests that its MAGNITUDE has SETTLED -- so an aligned-but-volatile stream persists yet stays uncalibrated,
and never surfaces a proposal. Exact Fraction throughout (no float in the gate).
"""
from fractions import Fraction

from residual_learner import ResidualLearner, variance_calibration, g_orthogonal_integer_vector

PHI4 = [1, 0, -10, 0, 1]                       # x^4 - 10x^2 + 1 = minpoly(sqrt2+sqrt3)


def _learner():
    L = ResidualLearner(PHI4, [[1, 0, 0, 0], [0, 1, 0, 0]], persistence_N=3)
    w = g_orthogonal_integer_vector(L._cols, L._G)   # off-axis integer dir, G-orthogonal to {1, theta}
    return L, w


def _obs(scale, w):
    return [Fraction(1) + scale * w[0], Fraction(scale * w[1]),
            Fraction(scale * w[2]), Fraction(scale * w[3])]


def test_stable_stream_calibrates_after_warmup():
    L, w = _learner()
    cal = variance_calibration(L)
    assert cal() is False                          # nothing observed yet -> not warmed up
    for _ in range(3):                             # residual is exactly w each tick -> zero spread
        L.observe(_obs(1, w))
    assert L._streak >= 3 and L._n_acc >= 3
    assert sum(L._M2) == 0                          # perfectly stable -> zero Welford variance (exact)
    assert cal() is True                            # warmed up AND settled -> calibrated


def test_volatile_stream_persists_but_blocks_calibration():
    L, w = _learner()
    cal = variance_calibration(L)
    for k in range(6):                              # same DIRECTION w, alternating MAGNITUDE 1x / 10x
        L.observe(_obs(1 if k % 2 == 0 else 10, w))
    assert L._streak >= 3                            # the direction persists (aligned) -> persistence met
    assert sum(L._M2) > 0                            # ... but the magnitude is volatile
    assert cal() is False                            # calibration BLOCKS the unsettled centroid


def test_calibration_gates_propose_end_to_end():
    L, w = _learner()
    L._calibration_ok = variance_calibration(L)     # install the concrete calibration
    for k in range(6):                              # volatile: persists but should never propose
        L.observe(_obs(1 if k % 2 == 0 else 10, w))
    assert L._streak >= 3                            # persistence satisfied
    assert L.propose() is None                       # ... calibration blocks -> no proposal surfaced


def test_default_calibration_is_permissive_unchanged():
    # the constructor default stays lambda: True, so existing behaviour is unaffected
    L, w = _learner()
    for _ in range(3):
        L.observe(_obs(1, w))
    assert L._calibration_ok() is True               # default permissive
    assert L.propose() is not None                   # stable stream still proposes under the default
