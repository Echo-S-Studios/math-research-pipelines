"""test_holding.py -- the EXACT-Fraction core: zero-tolerance identities + parity with the float kernel.

Everything here is decided with == on Fraction (NO tolerance) -- this is the G8-clean core that may
wire live into L00M. We also cross-check that float(exact reading) matches the float semantic_kernel,
proving the exact core is a faithful REFINEMENT (the same algebra, decided exactly), not a new one.
"""
from fractions import Fraction

from kira_language import holding as Q
from kira_language.holding import H, VOID, ONE, E1, E2, I, P0
from kira_language import semantic_kernel as K

SAMPLES = [
    H(1, 2, "1/2", "3/10"), ONE, E1, E2, I, P0,
    H("3/2", "-1/2", "1/3", "2/7"), H(2, 0, 0, 0), H("1/2", "1/2", 0, 0), H(7, 3, 2, 5),
]


def test_carrier_axioms_and_cocycle_exact():
    for X in SAMPLES:
        assert X + VOID == X and VOID + X == X          # ∅ = additive identity
        assert X * ONE == X and ONE * X == X            # 𝟙 = multiplicative identity
        assert -(-X) == X
    # the cocycle product, exactly: e1*e2=i, e2*e1=-i (anticommute), i^2=-1, e1^2=e2^2=1
    assert E1 * E2 == I
    assert E2 * E1 == H(0, 0, 0, -1)
    assert I * I == H(-1, 0, 0, 0)
    assert E1 * E1 == ONE and E2 * E2 == ONE


def test_cayley_hamilton_exact():
    """Φ_X(X) = X² - tr(X)X + det(X)𝟙 == ∅ EXACTLY (zero tolerance)."""
    for X in SAMPLES:
        assert Q.Phi(X, X) == VOID


def test_det_multiplicative_exact():
    for a in SAMPLES:
        for b in SAMPLES:
            assert Q.det(a * b) == Q.det(a) * Q.det(b)


def test_det_of_M_is_det_squared_exact():
    for X in SAMPLES:
        assert Q.det(Q.M(X)) == Q.det(X) ** 2


def test_R_K_nilpotent_exact():
    """R_K² = 0 exactly (the trace-free Gram has bite-depth ≤ 2)."""
    for X in SAMPLES:
        assert Q.R_K(Q.R_K(X)) == VOID
        assert Q.residual_height(X) <= 2


def test_nu_vs_R_K_distinction_exact():
    """The cross-review distinction, now EXACT: ν(P0)=0 (idempotent) but R_K(P0)≠0 (not conformal)."""
    assert Q.nu(P0) == VOID                       # P0 is a symmetric idempotent (a gate)
    assert Q.is_gate(P0) is True
    assert Q.R_K(P0) == H(0, 0, "1/2", 0)         # trace-free residual, exact
    assert Q.R_K(P0) != VOID
    assert Q.det(P0) == 0 and Q.rank(P0) == 1
    assert Q.R_K(ONE) == VOID                      # 𝟙 is conformal -> R_K = 0 exactly


def test_type_lattice_exact():
    # the φ keystone Cl(1/2,1,-1/2,0): tr=1, det=-1 -> by CH satisfies X² = X + 1 EXACTLY (the golden law).
    keystone = H("1/2", 1, "-1/2", 0)
    assert Q.tr(keystone) == 1 and Q.det(keystone) == -1
    assert Q.TYPE(keystone) == ["gen"]            # exactly the golden generation law
    assert set(Q.TYPE(P0)) == {"idem", "rest"} and Q.MASS(P0) == 2
    assert Q.TYPE(H(7, 3, 2, 5)) == ["free"]      # generic: no special law vanishes


def test_cross_check_with_float_kernel():
    """float(exact reading) matches the float semantic_kernel within tol -> faithful refinement."""
    for X in SAMPLES:
        Kc = K.Cl(float(X.a), float(X.b), float(X.c), float(X.d))
        assert abs(float(Q.det(X)) - K.det(Kc)) < 1e-9
        assert abs(float(Q.tr(X)) - 2 * K.tau(Kc)) < 1e-9
        assert abs(float(Q.disc(X)) - K.disc(Kc)) < 1e-9
        assert abs(float(Q.R_K(X).max_abs()) - abs(K.R_K(Kc))) < 1e-9
        assert Q.rank(X) == K.rank(Kc)
