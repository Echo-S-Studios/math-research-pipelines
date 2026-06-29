"""test_bridge_loom.py -- the phi keystone bridge stays honest against LIVE loom (one-way).

This is the single point where kira-language reads loom. The bridge must agree with the live
kernel on the void-law keystone x^2 = x + 1, or the disjoint-but-bridged architecture is broken.
(loom is reached via conftest's path-shim AND bridge_loom's own self-bootstrap.)
"""
from kira_language import loom_bridge as bridge_loom


def test_phi_keystone_agrees_with_live_loom():
    r = bridge_loom.phi_keystone()
    assert r["loom_reachable"] is True, r            # loom must be present for the bridge test
    assert r["agree"] is True, r
    assert r["companion"] == [[0, 1], [1, 1]]        # the void-law companion
    assert r["minpoly"] == [1, -1, -1]               # x^2 - x - 1
    assert r["cl_coords"] == [0.5, 1.0, -0.5, 0.0]   # the shared Cl(2,0) keystone
    assert abs(r["mahler"] - r["phi"]) < r["tol"]["mahler"]   # growth rate == phi


def test_bridge_constants_match_live_companion():
    """The hardcoded anchors equal what live loom actually returns (no silent drift)."""
    r = bridge_loom.phi_keystone()
    assert r["companion"] == bridge_loom.PHI_COMPANION
    assert r["minpoly"] == bridge_loom.PHI_MINPOLY
    assert r["cl_coords"] == bridge_loom.PHI_CL
