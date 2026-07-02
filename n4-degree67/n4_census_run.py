#!/usr/bin/env python3
"""N4 census driver: degree-5 regression gate, then degrees 6 and 7."""
import json
import sys

sys.path.insert(0, "/home/claude/n4")
from n4_lib import census

# ---- regression gate: [-2,2]^5 must reproduce the archived 83/67/16 ----
rows5, tal5 = census(5, "/home/claude/n4/n4_pisot5_regression.jsonl")
tp5 = sum(1 for r in rows5 if r["pairs"] == 2)
mx5 = sum(1 for r in rows5 if r["pairs"] == 1)
r55 = sum(1 for r in rows5 if r["pairs"] == 0)
assert (len(rows5), tp5, mx5, r55) == (83, 67, 16, 0), "deg-5 regression drift"
ref = [json.loads(l)["c"] for l in open("/home/claude/n1/pisot83.jsonl")]
assert [r["c"] for r in rows5] == ref, "deg-5 instance-set drift"
print("REGRESSION deg 5: 83/67/16 and instance set MATCH archived pisot83")

# ---------------------------------------------- degree 6, then degree 7 ----
rows6, tal6 = census(6, "/home/claude/n4/n4_pisot6.jsonl")
rows7, tal7 = census(7, "/home/claude/n4/n4_pisot7.jsonl")
print("N4 CENSUS COMPLETE")
