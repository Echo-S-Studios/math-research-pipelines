"""test_language_api.py -- local equivalence + firewall + endpoint sanity for the dispatch surface.

Mirrors L00M's test_vector_api: every endpoint's in-process dispatch(req) must equal the SAME
request run through the subprocess (`py -c "import language_api; language_api.main()"`). Read-only.
Also pins the (b) firewall: INTERPRETIVE statements never cross the wire as fact by default.
"""
import json
import os
import subprocess
import sys

import pytest

from kira_language import dispatch as language_api
from kira_language.semantic_kernel import INTERPRETIVE, FALSE_AS_STATED, WIRED_JURISDICTIONS

HERE = os.path.dirname(os.path.abspath(__file__))

REQUESTS = [
    {"endpoint": "read", "x": [0.5, 0.0, 0.5, 0.0]},     # P0 gate (rank-1 idempotent)
    {"endpoint": "read", "x": [1.0, 2.0, 0.5, 0.3]},     # generic
    {"endpoint": "laws"},                                # firewalled (wired only)
    {"endpoint": "laws", "wired_only": False},           # full bank, tagged
    {"endpoint": "search", "query": "residual"},
    {"endpoint": "audit", "samples": 64},
    {"endpoint": "bridge"},                              # one-way loom keystone
    {"endpoint": "nope"},                                # unknown endpoint
]


def _subprocess(req):
    """Run the request through the exact KIRA shell convention and parse the last stdout line."""
    proc = subprocess.run(
        [sys.executable, "-m", "kira_language"],
        cwd=HERE, input=json.dumps(req), capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize("req", REQUESTS, ids=[r["endpoint"] + ("_full" if r.get("wired_only") is False else "") for r in REQUESTS])
def test_local_equivalence(req):
    """in-process dispatch == subprocess JSON (round-tripped through JSON for parity)."""
    inproc = json.loads(json.dumps(language_api.dispatch(req), default=str))
    assert inproc == _subprocess(req)


def test_read_endpoint_values():
    # P0 is a rank-1 GATE (M(P0)=P0, idempotent) -- but NOT conformal, so its trace-free residual
    # R_K is NONZERO (= 0.5). This pins the nu-vs-R_K distinction (cross-review SCOPING.md 7.3):
    # nu(P0)=M-X=0, but R_K(P0)=M-tau(M).1 != 0 because M(P0) is not a scalar multiple of 1.
    p0 = language_api.dispatch({"endpoint": "read", "x": [0.5, 0.0, 0.5, 0.0]})
    assert p0["gate"] is True and p0["rank"] == 1 and p0["regime"] == "gate"
    assert p0["exact"] is False                      # float this increment, declared
    assert p0["residual_height"] == 2                # R_K^2 = 0: bite-depth 2
    assert abs(p0["residual_norm"] - 0.5) < p0["tol"]
    # ONE = identity is CONFORMAL (M(1)=1 is scalar), so the trace-free residual R_K IS zero.
    one = language_api.dispatch({"endpoint": "read", "x": [1.0, 0.0, 0.0, 0.0]})
    assert one["residual_norm"] < one["tol"]


def test_firewall_default_excludes_interpretive():
    """wired_only (default) must NOT leak INTERPRETIVE / FALSE_AS_STATED across the wire as fact."""
    wired = language_api.dispatch({"endpoint": "laws"})
    juris = {s["jurisdiction"] for s in wired["statements"]}
    assert INTERPRETIVE not in juris and FALSE_AS_STATED not in juris
    assert all(s["wired"] for s in wired["statements"])
    # ...but they exist when explicitly requested, and are tagged non-wired.
    full = language_api.dispatch({"endpoint": "laws", "wired_only": False})
    interp = [s for s in full["statements"] if s["jurisdiction"] == INTERPRETIVE]
    assert len(interp) >= 2                                   # observer_reading + framework_reading
    assert all(s["wired"] is False for s in interp)
    assert full["count"] > wired["count"]


def test_search_is_firewalled():
    hits = language_api.dispatch({"endpoint": "search", "query": "residual"})
    assert all(s["jurisdiction"] in WIRED_JURISDICTIONS for s in hits["statements"])


def test_audit_closure_true():
    assert language_api.dispatch({"endpoint": "audit", "samples": 64})["closure"] is True


def test_unknown_endpoint_is_soft_error():
    r = language_api.dispatch({"endpoint": "nope"})
    assert "error" in r and "endpoints" in r            # never raises across the wire
