"""test_acquisition.py -- the EXACT acquisition loop (increment 3), decided at zero tolerance.

Everything here is == on Fraction/H -- no tolerance (the G8 core that may wire live into L00M).
Deliberately built to be LOAD-BEARING, closing the blind spots the foundation mutation-audit found:
  * exact VALUE pins (not loose bounds) -- so a wrong-but-idempotent projector (e.g. identity) is caught;
  * an INDEPENDENT matrix-route oracle for L and the mat/cl iso -- so a single-route bug can't hide;
  * an explicit NON-membership disproof (the corrected handoff hint) -- pinning what is NOT in ker(L).
"""
from fractions import Fraction

from kira_language import acquisition as A
from kira_language.acquisition import (
    R, L, residual, is_captured, project, commit, kernel_coords, word, acquire,
    Capture, KER_BASIS, KER_DIM, KER_LABELS, _PROJ,
)
from kira_language.holding import H, VOID, ONE, E1, E2, I, mat, cl

Q0 = Fraction(0)
SAMPLES = [
    ONE, E1, E2, I, R, H(7, 3, 2, 5), H("1/2", "1/2", 0, 0),
    H("3/2", "-1/2", "1/3", "2/7"), H(0, 1, 2, 0), H("-5/4", "7/9", "-2/3", "11/13"), VOID,
]


# --- an INDEPENDENT matrix-route oracle (own mat/multiply/cl; never calls H.__mul__) ------------ #
def _mat_t(X):
    return [[X.a + X.c, X.b - X.d], [X.b + X.d, X.a - X.c]]


def _mm(P, Qm):
    return [[P[0][0] * Qm[0][0] + P[0][1] * Qm[1][0], P[0][0] * Qm[0][1] + P[0][1] * Qm[1][1]],
            [P[1][0] * Qm[0][0] + P[1][1] * Qm[1][0], P[1][0] * Qm[0][1] + P[1][1] * Qm[1][1]]]


def _madd(P, Qm):
    return [[P[i][j] + Qm[i][j] for j in range(2)] for i in range(2)]


def _msub(P, Qm):
    return [[P[i][j] - Qm[i][j] for j in range(2)] for i in range(2)]


def _cl_t(m):
    p, q = m[0]
    r, s = m[1]
    return H((p + s) / 2, (q + r) / 2, (p - s) / 2, (r - q) / 2)


def _L_oracle(X):
    mR, mX = _mat_t(R), _mat_t(X)
    return _cl_t(_msub(_madd(_mm(mR, mX), _mm(mX, mR)), mX))


# --- the keystone + its symmetry (the locked Sylvester assumption) ------------------------------ #
def test_keystone_is_phi_and_mat_symmetric_exact():
    assert R == H("1/2", 1, "-1/2", 0)
    assert mat(R) == [[0, 1], [1, 1]]                 # the phi companion
    assert R.d == 0 and A._mat_symmetric(R) is True   # mat-symmetric (the Sylvester assumption)
    assert mat(R)[0][1] == mat(R)[1][0]


def test_keystone_equals_loom_bridge_phi_cl():
    """Honesty check: the acquisition keystone IS the one-way bridge keystone (no loom call needed)."""
    from kira_language.loom_bridge import PHI_CL
    assert [float(c) for c in R.coords] == PHI_CL      # [0.5, 1.0, -0.5, 0.0]


# --- L matches an independent oracle, exactly (no single-route bug can hide) --------------------- #
def test_L_matches_matrix_oracle_exact():
    for X in SAMPLES:
        assert L(X) == _L_oracle(X)
        assert residual(X) == L(X)


def test_mat_cl_iso_roundtrip_exact():
    """Pin holding.mat/cl directly (the audit found them uncovered): mat == independent, cl o mat == id."""
    for X in SAMPLES:
        assert mat(X) == _mat_t(X)
        assert cl(mat(X)) == X


# --- ker(L): exact dim 2, exact basis, and the NON-membership disproof -------------------------- #
def test_kernel_exact_dim_and_basis():
    assert KER_DIM == 2
    assert KER_BASIS == (H(0, 1, 2, 0), H(0, 0, 0, 1))      # e1+2e2  and  the pseudoscalar i
    assert KER_LABELS == ("e1+2e2", "i")
    for k in KER_BASIS:
        assert L(k) == VOID and is_captured(k) is True       # each basis element is exactly on-shell


def test_corrected_handoff_hint_is_not_in_kernel():
    """The Phase-3 gate hint 'N = H(0,-1,1,0) in ker' is WRONG. Pin the disproof exactly."""
    N_bogus = H(0, -1, 1, 0)
    assert L(N_bogus) == H(-3, 0, 0, 0)                # != VOID
    assert is_captured(N_bogus) is False
    # the candidate's real antisymmetric generator N = matrix [[0,-1],[1,0]] = cl(...) = pseudoscalar i:
    assert cl([[0, -1], [1, 0]]) == I and is_captured(I) is True


def test_keystone_R_not_in_kernel_exact():
    assert is_captured(R) is False
    assert L(R) == H("5/2", 1, "-1/2", 0)             # 2*R^2 - R, exact


# --- the commit: an EXACT idempotent orthogonal projector ONTO ker(L) (value-pinned) ------------ #
def test_projector_exact_matrix_value():
    """Pin the projector matrix itself -- idempotency alone is also satisfied by the identity, so a
    trivial/wrong-but-idempotent projector must not pass."""
    assert _PROJ == [
        [Q0, Q0, Q0, Q0],
        [Q0, Fraction(1, 5), Fraction(2, 5), Q0],
        [Q0, Fraction(2, 5), Fraction(4, 5), Q0],
        [Q0, Q0, Q0, Fraction(1, 1)],
    ]
    assert _PROJ != [[Fraction(1 if i == j else 0) for j in range(4)] for i in range(4)]  # not identity


def test_projector_is_idempotent_and_lands_in_kernel_exact():
    for X in SAMPLES:
        p = project(X)
        assert project(p) == p                         # P^2 = P, exact
        assert L(p) == VOID and is_captured(p) is True  # range(P) subset ker(L)
    for k in KER_BASIS:
        assert project(k) == k                          # identity on ker(L)
    assert commit is project


def test_projector_exact_values_on_witnesses():
    assert project(ONE) == VOID                          # ONE is orthogonal to the slack
    assert project(E1) == H(0, "1/5", "2/5", 0)          # exact committed value
    assert project(I) == I                               # already on-shell
    assert project(VOID) == VOID


def test_kernel_coords_exact():
    assert kernel_coords(E1) == (Fraction(1, 5), Q0)
    assert kernel_coords(I) == (Q0, Fraction(1, 1))
    assert kernel_coords(H(0, 1, 2, 0)) == (Fraction(1, 1), Q0)
    assert kernel_coords(ONE) == (Q0, Q0)


# --- the word: sign discrimination + generalization-by-return-to-zero --------------------------- #
def test_word_sign_aware_sparse_code():
    assert word(E1) == ("+e1+2e2",)
    assert word(I) == ("+i",)
    assert word(-I) == ("-i",)                           # antipodal ray -> opposite word (opposite meaning)
    assert word(ONE) == ()                               # orthogonal to slack -> empty
    assert word(H(0, 1, 2, 0) + I) == ("+e1+2e2", "+i")  # both axes dominate


def test_sign_discriminates_antipodes():
    assert word(I) != word(-I)
    assert word(E1) != word(-E1)


def test_generalization_same_residue_same_value_and_word():
    """Tokens differing by something orthogonal to ker, or by positive scale, commit to the SAME ray."""
    # E1 and E1+ONE differ by ONE (orthogonal to the slack) -> identical exact committed value:
    assert project(E1 + ONE) == project(E1)
    assert acquire(E1 + ONE).committed == acquire(E1).committed
    assert acquire(E1 + ONE).word == acquire(E1).word
    # positive scaling stays on the same ray -> same word (generalization across magnitude):
    assert word(3 * E1) == word(E1)
    assert word(5 * I) == word(I)
    # a different residue -> a different word:
    assert word(I) != word(E1)


# --- the loop record (Capture) ------------------------------------------------------------------ #
def test_acquire_record_exact():
    cap = acquire(I)
    assert isinstance(cap, Capture)
    assert cap.captured is True and cap.residual_before == VOID
    assert cap.committed == I and cap.coords == (Q0, Fraction(1, 1)) and cap.word == ("+i",)

    cap2 = acquire(E1)
    assert cap2.captured is False
    assert cap2.residual_before == H(2, 0, 0, 0) == L(E1)
    assert cap2.committed == H(0, "1/5", "2/5", 0)
    assert is_captured(cap2.committed) is True            # the learned value is on-shell

    cap0 = acquire(VOID)
    assert cap0.captured is True and cap0.committed == VOID and cap0.word == ()


# --- exactness / no-float discipline (decision d) ----------------------------------------------- #
def test_everything_is_exact_no_float():
    for X in SAMPLES:
        assert isinstance(is_captured(X), bool)
        for comp in project(X):
            assert isinstance(comp, Fraction)
        for c in kernel_coords(X):
            assert isinstance(c, Fraction)
        for tok in word(X):
            assert isinstance(tok, str)
    # the projector + kernel basis are all exact rationals:
    for row in _PROJ:
        for v in row:
            assert isinstance(v, Fraction)
    for k in KER_BASIS:
        for comp in k:
            assert isinstance(comp, Fraction)


def test_module_is_numpy_free():
    """Exact-only: the acquisition module pulls no numpy (pure stdlib + holding)."""
    import inspect
    src = inspect.getsource(A)
    assert "import numpy" not in src and "from numpy" not in src
