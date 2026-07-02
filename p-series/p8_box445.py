#!/usr/bin/env python3
"""p8_box445.py -- P8 (and P1/P2 next-box) executed: quintic census over
[-4,4]^5 with full composed-square scans of every two-pair instance.

The merged-shell hunt: any live instance with detector != 2, Phi_2 content,
higher cyclotomic content, or Phi_1 excess is a finding (P8 hit or P1
falsifier). Checkpointed like n4_scan_run.
"""
import json
import os
import sys
import time

sys.path.insert(0, "/home/claude/pseries")
sys.path.insert(0, "/home/claude/n4")
from p_census import census_box  # noqa: E402
from n4_lib import scan_instance, torsion_candidates  # noqa: E402

CEN = "/home/claude/pseries/p8_pisot5_box4.jsonl"
OUT = "/home/claude/pseries/p8_scan5_box4.jsonl"

shard = int(sys.argv[1]) if len(sys.argv) > 1 else 0
nshards = int(sys.argv[2]) if len(sys.argv) > 2 else 1

if not os.path.exists(CEN):
    if shard == 0:
        census_box(5, -4, 4, CEN)
    else:
        while not os.path.exists(CEN + ".done"):
            time.sleep(5)
if shard == 0 and not os.path.exists(CEN + ".done"):
    open(CEN + ".done", "w").write("ok")

rows = [json.loads(l) for l in open(CEN)]
live = [r for r in rows if r["pairs"] >= 2]
print(f"census: {len(rows)} Pisot, live two-pair: {len(live)}", flush=True)

done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        done.add(tuple(json.loads(l)["c"]))
phi, cand, table = torsion_candidates(20)
todo = [r for i, r in enumerate(live)
        if i % nshards == shard and tuple(r["c"]) not in done]
print(f"[shard {shard}/{nshards}] {len(todo)} to scan", flush=True)
t0 = time.time()
with open(OUT, "a") as f:
    for i, r in enumerate(todo):
        rec = scan_instance(tuple(r["c"]), 5, r["pairs"], phi, cand, table)
        f.write(json.dumps(rec) + "\n")
        f.flush()
        if not rec["clean"]:
            print(f"*** ATTENTION *** {rec}", flush=True)
        if (i + 1) % 50 == 0:
            print(f"[shard {shard}] {i+1}/{len(todo)}  {time.time()-t0:.0f}s",
                  flush=True)
print(f"[shard {shard}] DONE {len(todo)} in {time.time()-t0:.0f}s", flush=True)
