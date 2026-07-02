#!/usr/bin/env python3
"""p4_totally_real.py -- P4 executed: totally-real Pisot sweep, degrees 2-7,
with an exact theta >= phi certificate per instance.

Certificate: for a totally-real Pisot P (monic, irreducible, exactly one
root theta > 1, all other roots in (-1,1)), theta > phi iff P(phi) < 0
(theta is the ONLY root exceeding 1 > all others, and P -> +inf), and
theta = phi iff P = x^2 - x - 1. P(phi) is evaluated EXACTLY in Z[phi]:
phi^2 = phi + 1 reduces P(phi) to a + b*phi with a, b in Z, and
sign(a + b*phi) = sign of (2a + b) + b*sqrt(5), decided by integer squares.

Populations swept:
  deg 2, 3: boxes [-3,3]^n (fresh censuses, same discipline);
  deg 4:    [-3,3]^4 (the archived quartic sweep; re-certified here);
  deg 5:    [-2,2]^5 and [-3,3]^5 (archived censuses: totally-real counts 0);
  deg 6, 7: [-2,2]^n (archived: 0).
"""
import json
import sys

sys.path.insert(0, "/home/claude/pseries")
sys.path.insert(0, "/home/claude/n4")
from p_census import census_box  # noqa: E402


def eval_at_phi(c_asc):
    """P(phi) for monic P with ascending coeffs c_asc + [1]; returns (a, b)
    with P(phi) = a + b*phi, computed via phi^k = F_k*phi + F_{k-1}."""
    coeffs = list(c_asc) + [1]
    a = b = 0
    fk1, fk = 1, 0          # F_{-1}=1, F_0=0: phi^0 = 0*phi + 1
    for k, cf in enumerate(coeffs):
        if k == 0:
            pa, pb = 1, 0    # phi^0 = 1
        else:
            fk1, fk = fk, fk + fk1   # F_{k-1}, F_k
            pa, pb = fk1, fk         # phi^k = F_k*phi + F_{k-1}
        a += cf * pa
        b += cf * pb
    return a, b


def sign_a_plus_b_phi(a, b):
    """Exact sign of a + b*(1+sqrt5)/2 = ((2a+b) + b*sqrt5)/2."""
    u, v = 2 * a + b, b
    if u >= 0 and v >= 0:
        return 1 if (u or v) else 0
    if u <= 0 and v <= 0:
        return -1 if (u or v) else 0
    if u > 0 > v:
        return 1 if u * u > 5 * v * v else (-1 if u * u < 5 * v * v else 0)
    return 1 if 5 * v * v > u * u else (-1 if 5 * v * v < u * u else 0)


def certify(c):
    a, b = eval_at_phi(c)
    s = sign_a_plus_b_phi(a, b)
    if s == 0:
        assert list(c) == [-1, -1], ("P(phi)=0 off the golden minimal poly", c)
        return "theta == phi (the equality case x^2-x-1)"
    assert s < 0, ("theta < phi: P4 FALSIFIER", c)
    return "theta > phi certified (P(phi) < 0 exactly)"


def main():
    tr = []
    for n in (2, 3):
        rows, _ = census_box(n, -3, 3, f"/home/claude/pseries/p4_pisot{n}_box3.jsonl")
        tr += [(n, tuple(r["c"])) for r in rows if r["pairs"] == 0]
        print(f"  deg {n}: {sum(1 for r in rows if r['pairs']==0)} totally real "
              f"of {len(rows)} Pisot")
    # deg 4, archived quartic sweep box [-3,3]^4: re-derive the totally-real set
    rows4, _ = census_box(4, -3, 3, "/home/claude/pseries/p4_pisot4_box3.jsonl")
    tr4 = [(4, tuple(r["c"])) for r in rows4 if r["pairs"] == 0]
    print(f"  deg 4: {len(tr4)} totally real of {len(rows4)} Pisot "
          f"(archived sweep: 103 Pisot, 1 totally real)")
    assert len(rows4) == 103 and len(tr4) == 1, "quartic regression drift"
    assert tr4[0][1] == (1, 2, -2, -3), tr4
    tr += tr4
    # deg 5-7 archived censuses: totally-real counts are zero
    for path, n in (("/home/claude/n4/n4_pisot5_regression.jsonl", 5),
                    ("/home/claude/n1/pisot_n2.jsonl", 5),
                    ("/home/claude/n4/n4_pisot6.jsonl", 6),
                    ("/home/claude/n4/n4_pisot7.jsonl", 7)):
        rows = [json.loads(l) for l in open(path)]
        z = sum(1 for r in rows if r["real_roots"] == n)
        print(f"  deg {n} ({path.split('/')[-1]}): totally real = {z}")
        assert z == 0
    print(f"\nP4 population: {len(tr)} totally-real Pisot instances "
          f"across degrees 2-7 boxes")
    eq = 0
    for n, c in sorted(tr):
        v = certify(c)
        eq += v.startswith("theta ==")
        print(f"  deg {n} c={c}: {v}")
    assert eq == 1, "equality case count != 1"
    print("\nP4 VERDICT: theta >= phi on every totally-real Pisot found; "
          "equality exactly once, at x^2-x-1. Zero falsifiers.")


if __name__ == "__main__":
    main()
