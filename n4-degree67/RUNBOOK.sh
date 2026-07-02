#!/bin/bash
# RUNBOOK.sh — zero-shot regeneration of the n4-degree67 package.
# Requires: Python >= 3.11 + sympy 1.14, PARI/GP on PATH; ~50 min
# (dominated by the 414 degree-7 composed-square scans, four shards).
# The exact command sequence below was executed in the authoring container;
# regenerated censuses match the pins byte-identically, scan JSONLs minus
# the per-row `secs` field, and the GP deck's stdout byte-identically.
set -euo pipefail
B="$(cd "$(dirname "$0")" && pwd)"
for W in /home/claude/n1 /home/claude/n4; do
  if [ -e "$W" ]; then echo "refusing: $W exists (stale)"; exit 1; fi
done
echo "== 0. manifest =="
(cd "$B" && sha256sum -c MANIFEST.sha256)
echo "== 1. assemble the authoring layout =="
mkdir -p /home/claude/n1 /home/claude/n4
cp "$B/stage_a_certify.py" /home/claude/n1/
cp "$B"/n4_lib.py "$B"/n4_census_run.py "$B"/n4_scan_run.py "$B"/n4_spot.gp /home/claude/n4/
# the degree-5 pinned reference the census gate compares against
cp "$B"/../p-series/deps/pisot83.jsonl /home/claude/n1/
cd /home/claude/n4
echo "== 2. censuses (degree-5 regression gate, then 6 and 7) =="
python3 n4_census_run.py | tee census.out
grep -q "REGRESSION deg 5: 83/67/16 and instance set MATCH" census.out
grep -q "N4 CENSUS COMPLETE" census.out
echo "== 3. scans (deg 5 regression; deg 6; deg 7 in four shards) =="
python3 n4_scan_run.py n4_pisot5_regression.jsonl n4_scan5.jsonl > s5.out
python3 n4_scan_run.py n4_pisot6.jsonl n4_scan6.jsonl > s6.out
for s in 0 1 2 3; do python3 n4_scan_run.py n4_pisot7.jsonl n4_scan7_s$s.jsonl $s 4 > s7_$s.out 2>&1 & done; wait
cat n4_scan7_s0.jsonl n4_scan7_s1.jsonl n4_scan7_s2.jsonl n4_scan7_s3.jsonl > n4_scan7.jsonl
python3 - <<'EOF'
import json
for f, n in (("n4_scan5.jsonl", 83), ("n4_scan6.jsonl", 160), ("n4_scan7.jsonl", 414)):
    rows = [json.loads(l) for l in open(f)]
    assert len(rows) == n and all(r["clean"] for r in rows), (f, len(rows))
    print(f"OK  {f}: {n}/{n} clean")
EOF
echo "== 4. GP cross-engine deck =="
gp -q n4_spot.gp > spot.out 2> spot.err
diff "$B/n4_spot.out" spot.out
if grep -v "Warning: new stack size" spot.err | grep -q '[*][*][*]'; then
  echo "H2: non-benign gp stderr"; exit 1
fi
echo "== 5. regenerated vs pinned (minus secs for scans) =="
B_ENV="$B" python3 - <<'EOF'
import json, os
B = os.environ["B_ENV"]
def rows(p): return [json.loads(l) for l in open(p)]
def strip(rs): return [{k: v for k, v in r.items() if k != "secs"} for r in rs]
for f in ("n4_pisot5_regression.jsonl", "n4_pisot6.jsonl", "n4_pisot7.jsonl"):
    assert open(f, "rb").read() == open(f"{B}/{f}", "rb").read(), f
    print(f"OK  {f} byte-identical to pin")
for f in ("n4_scan5.jsonl", "n4_scan6.jsonl", "n4_scan7.jsonl"):
    assert strip(rows(f)) == strip(rows(f"{B}/{f}")), f
    print(f"OK  {f} == pin (minus secs)")
EOF
echo "N4 RUNBOOK: ALL GREEN"
