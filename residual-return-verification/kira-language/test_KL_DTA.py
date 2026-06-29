"""Tests for KL_DTA.py.

Pins the load-bearing algebraic identities (so a refactor can't silently break them) and the
Windows-console output-portability fix (cp1252 must never traceback). Discoverable by
`py -m pytest`. KL_DTA is a standalone module — these tests import it directly and do not touch
loom / constants / vendor (it is wired into nothing).
"""
import io

from KL_DTA import (
    Cl, VOID, ONE, S1, S3, Ii, Xg, P0, R1, PHI,
    Phi, det, M, res, sclose,
    run, verify_all,
    _flow_off_cone, _cd_norm_multiplicative,
    _ascii_safe, _AsciiSafeStdout,
)

TOL = 1e-9
SAMPLES = [Xg, ONE, S1, S3, Ii, R1, P0, Cl(1.0, 0.5, 0.3, 0.7), Cl(PHI, 1.0, 0.0, 0.0)]


# ── End-to-end: the whole verification passes ────────────────────────────────────────────────

def test_run_returns_true():
    """run() executes verify_all + render_results and returns the PASS verdict."""
    assert run() is True


def test_verdict_every_subcheck_passes():
    v = verify_all()["verdict"]
    assert v["passed"] is True
    assert all(val is True for val in v.values())


# ── Load-bearing identities (pinned so they can't silently regress) ───────────────────────────

def test_cayley_hamilton_residual_below_tol():
    """Phi_X(X) = X^2 - tr(X)X + det(X)1 = 0 for every holding (Cayley-Hamilton)."""
    for X in SAMPLES:
        assert res(Phi(X, X), VOID) < TOL


def test_det_is_multiplicative():
    """det(a.b) = det(a).det(b) — the composition-algebra property."""
    for a in SAMPLES:
        for b in SAMPLES:
            assert sclose(det(a * b), det(a) * det(b))


def test_det_of_observation_is_det_squared():
    """det(M(X)) = det(X)^2 (the Born square)."""
    for X in SAMPLES:
        assert sclose(det(M(X)), det(X) ** 2)


def test_hurwitz_wall_breaks_at_dim_16():
    """Norm-multiplicativity holds for R,C,H,O (dims 1,2,4,8) and BREAKS at 16 (sedenions)."""
    for d in (1, 2, 4, 8):
        assert _cd_norm_multiplicative(d) is True
    assert _cd_norm_multiplicative(16) is False


def test_flow_off_cone_is_not_vacuous():
    """The seam check must be FALSE on the null cone — would be True everywhere under `... or True`."""
    assert _flow_off_cone(Xg) is True      # invertible, det != 0 -> off the cone
    assert _flow_off_cone(P0) is False     # rank-1 idempotent, det = 0 -> ON the cone
    assert _flow_off_cone(VOID) is False   # the cone tip


# ── Output portability: cp1252 must never traceback ───────────────────────────────────────────

def test_ascii_safe_is_pure_ascii_and_keeps_verdict():
    heavy = "═" * 10 + "  ∅ 𝟙 φ ψ ε ν Φ χ λ → ⟹ ⊕ ⊗ ½ ² ③ ⑧ ℝ 𝕆  passed=True"
    out = _ascii_safe(heavy)
    out.encode("ascii")  # must not raise
    assert "passed=True" in out
    # the common framework glyphs are mapped, not dropped to '?'
    assert _ascii_safe("∅ 𝟙 φ passed=True") == "0 1 phi passed=True"


def test_ascii_safe_stdout_survives_strict_cp1252():
    """A strict cp1252 sink would raise on the glyphs; the proxy must transliterate, not crash."""
    raw = io.BytesIO()
    sink = io.TextIOWrapper(raw, encoding="cp1252", errors="strict",
                            write_through=True, newline="")
    proxy = _AsciiSafeStdout(sink)
    proxy.write("═══ verdict ∅ 𝟙 φ passed=True\n")  # must NOT raise
    sink.flush()
    text = raw.getvalue().decode("cp1252")
    assert "passed=True" in text
    assert "=== verdict 0 1 phi passed=True" in text
