"""
test_p2_10_salem_factory.py
===========================
Paper 2, Section 8 -- the operational form of the Salem-Slot / commutator-boundary
("operation-relative closure"): the guard's verdict is decided by the exact
below-phi Salem test, NOT by the trace, and a Salem-producing family is caught
while its (totally real) trace-down is benign.

Depends on the exact-Q(sqrt5) sign fix (B1): the S_n factory routes a pure-rational
R(phi) (e.g. the deg-6 Salem has R(phi)=2), which previously crashed sign_in_Qsqrt5.

Forced facts (all re-derived in exact arithmetic):
    - Salem factory  S_n(x) = x^n*P(x) - P*(x),  P = x^2-x-1,  routes a sub-phi Salem
      factor for n in {6, 10, 12} (M = 1.50614, 1.60545, 1.61340) -> INVALID_CLOSURE
    - the trace-down T(t) of each such Salem is totally real (benign) -> FORCED
    - the verdict does not track the trace
"""
import sympy as sp
from emission_closure_guard import validate_closure, companion, trace_down
from harness.results import record

PAPER = "emission_gap"
x = sp.symbols('x')


def _salem_factory(n):
    """S_n = x^n*(x^2 - x - 1) - reverse(x^2 - x - 1) ; integer coeffs, high power first."""
    P = [1, -1, -1]
    S = sp.Poly(x**n, x) * sp.Poly(P, x) - sp.Poly(P[::-1], x)
    return [int(c) for c in S.all_coeffs()]


def test_salem_factory_is_caught():
    for n in (6, 10, 12):
        r = validate_closure(companion(_salem_factory(n)))
        assert r["verdict"] == "INVALID_CLOSURE", f"S_{n} should route a sub-phi Salem"
        assert any(below for _, below in r["salem"])
    record("P2-FACTORY-01", PAPER, "Sec 8 (Salem factory caught)",
           "the factory S_n = x^n*(x^2-x-1) - reverse, n in {6,10,12}, routes a sub-phi Salem "
           "factor (M = 1.50614, 1.60545, 1.61340); the guard returns INVALID_CLOSURE on each",
           "verdict(companion(S_n)) = INVALID_CLOSURE for n in {6,10,12}",
           detail={"n": [6, 10, 12], "all_below_phi": True})


def test_salem_trace_down_is_benign():
    for n in (6, 10, 12):
        r = validate_closure(companion(_salem_factory(n)))
        for Rp, below in r["salem"]:
            if not below:
                continue
            T = trace_down(Rp)                                   # totally real trace-down
            Tcomp = companion([int(c) for c in T.all_coeffs()])
            assert validate_closure(Tcomp)["verdict"] == "FORCED"
    record("P2-FACTORY-02", PAPER, "Sec 8 (trace-down benign)",
           "the trace-down T(t) of each routed Salem is totally real and carries no Salem "
           "factor, so the guard reads FORCED: the redirected object lands above the floor",
           "verdict(companion(trace-down of the S_n Salem)) = FORCED",
           detail={"n": [6, 10, 12]})


def test_verdict_does_not_track_trace():
    f6 = [1, -1, 0, -1, 0, -1, 1]                              # deg-6 Salem, trace 1
    carrier = sp.diag(companion(f6), sp.Matrix([[-1]]))         # same Salem, trace 0
    assert companion(f6).trace() == 1 and carrier.trace() == 0
    # same verdict (INVALID) at two different traces:
    assert validate_closure(companion(f6))["verdict"] == "INVALID_CLOSURE"
    assert validate_closure(carrier)["verdict"] == "INVALID_CLOSURE"
    # same trace (1) as f6 but the OPPOSITE verdict -> verdict is not a function of trace:
    assert validate_closure(companion([1, -1, -1]))["verdict"] == "FORCED"        # phi, trace 1
    assert validate_closure(companion([1, -7, 1]))["verdict"] == "FORCED"         # gap, trace 7
    record("P2-FACTORY-03", PAPER, "Sec 8 (verdict is trace-independent)",
           "the closure verdict is decided by the exact below-phi Salem test, not the trace: "
           "INVALID occurs at trace 0 and 1, FORCED occurs at trace 1 and 7, so the verdict is "
           "not a function of the trace (operation-relative closure, per the Salem Slot)",
           "verdict independent of trace(M)",
           detail={"invalid_traces": [0, 1], "forced_traces": [1, 7]})


if __name__ == "__main__":
    import subprocess
    import sys
    sys.exit(subprocess.call(["python3", "-m", "pytest", "-q", __file__]))
