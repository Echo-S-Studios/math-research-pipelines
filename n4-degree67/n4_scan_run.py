#!/usr/bin/env python3
"""N4 scan driver -- checkpointed, shardable.

Usage: python3 n4_scan_run.py <census_jsonl> <out_jsonl> [shard] [nshards]

Runs the full per-instance decision (Rat scan; S*/C2 for >= 2 pairs) for the
instances with index % nshards == shard, appending to out_jsonl (resume-safe:
already-recorded instances are skipped).
"""
import json
import os
import sys
import time

sys.path.insert(0, "/home/claude/n4")
from n4_lib import scan_instance, torsion_candidates

census_path, out_path = sys.argv[1], sys.argv[2]
shard = int(sys.argv[3]) if len(sys.argv) > 3 else 0
nshards = int(sys.argv[4]) if len(sys.argv) > 4 else 1

rows = [json.loads(l) for l in open(census_path)]
n = len(rows[0]["c"])
done = set()
if os.path.exists(out_path):
    for l in open(out_path):
        done.add(tuple(json.loads(l)["c"]))

phi_r, cand_r, table_r = torsion_candidates(n * n - n)

todo = [r for i, r in enumerate(rows)
        if i % nshards == shard and tuple(r["c"]) not in done]
print(f"[shard {shard}/{nshards}] {len(todo)} to scan (deg {n})", flush=True)
t0 = time.time()
with open(out_path, "a") as f:
    for i, r in enumerate(todo):
        rec = scan_instance(tuple(r["c"]), n, r["pairs"], phi_r, cand_r, table_r)
        f.write(json.dumps(rec) + "\n")
        f.flush()
        flag = "OK" if rec["clean"] else "*** ATTENTION ***"
        print(f"[shard {shard}] {i+1}/{len(todo)} c={r['c']} pairs={r['pairs']} "
              f"rat={{{rec['rat_verdict']}}}"
              + (f" det={rec.get('detector')} dS*={rec.get('deg_sstar')} "
                 f"c2={{{rec.get('c2_verdict','-')}}}" if r["pairs"] >= 2 else "")
              + f" {rec['secs']}s {flag}", flush=True)
print(f"[shard {shard}] DONE in {time.time()-t0:.0f}s", flush=True)
