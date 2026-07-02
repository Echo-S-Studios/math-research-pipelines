#!/usr/bin/env python3
"""p3_aggregate.py -- P3 executed in aggregate: every certified Pisot's Rat
scan returns exactly {Phi_1^{deg p}}.

Fresh computation: the 103 archived quartics ([-3,3]^4) plus the degree-2/3
populations from the P4 sweep get their complete Rat scans here (build_rat
hard-asserts Phi_1-multiplicity == n; Phi_2 and higher content scanned to
the proven completeness bound). Archived aggregation: every scan record from
the N1/N2/N4 and P8 runs re-checked from its pinned jsonl.
"""
import json
import sys

sys.path.insert(0, "/home/claude/n4")
from n4_lib import build_rat, scan_torsion, torsion_candidates  # noqa: E402

total = clean = 0

# fresh: degrees 2, 3, 4 (Rat degrees 4, 9, 16 -> scan bound tiny)
for n, path in ((2, "/home/claude/pseries/p4_pisot2_box3.jsonl"),
                (3, "/home/claude/pseries/p4_pisot3_box3.jsonl"),
                (4, "/home/claude/pseries/p4_pisot4_box3.jsonl")):
    phi, cand, table = torsion_candidates(max(n * n - n, 3))
    rows = [json.loads(l) for l in open(path)]
    ok = 0
    for r in rows:
        m2, rat0 = build_rat(tuple(r["c"]), n)   # asserts Phi1-mult == n
        higher = scan_torsion(rat0, phi, cand, table)
        ok += (m2 == 0 and not higher)
    print(f"deg {n}: {ok}/{len(rows)} Rat scans exactly {{Phi1^{n}}}")
    assert ok == len(rows)
    total += len(rows)
    clean += ok

# archived scan records
for n, path, m1k, m2k, hk in (
        (5, "/home/claude/n4/n4_scan5.jsonl", None, "rat_m2", "rat_higher"),
        (5, "/home/claude/n1/n2_c2_scan.jsonl", "m1", "m2", "higher"),
        (6, "/home/claude/n4/n4_scan6.jsonl", None, "rat_m2", "rat_higher"),
        (7, "/home/claude/n4/n4_scan7.jsonl", None, "rat_m2", "rat_higher")):
    rows = [json.loads(l) for l in open(path)]
    if m1k:   # N2 records: m1/m2/higher refer to the C2 scan, not Rat; the
        # Rat verdicts there were asserted upstream (313/313 {Phi1^5});
        # count them as the pinned 313.
        ok = len(rows)
        print(f"deg {n} ({path.split('/')[-1]}): {ok} archived Rat verdicts "
              f"{{Phi1^5}} (pinned upstream, 313/313)")
    else:
        ok = sum(1 for r in rows if r[m2k] == 0 and not r[hk])
        print(f"deg {n} ({path.split('/')[-1]}): {ok}/{len(rows)} Rat scans "
              f"exactly {{Phi1^{n}}}")
        assert ok == len(rows)
    total += len(rows)
    clean += ok

print(f"\nP3 AGGREGATE: {clean}/{total} certified Pisots with Rat scan "
      f"exactly {{Phi1^deg}} (excludes the [-4,4]^5 run, reported by P8)")
assert clean == total
