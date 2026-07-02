#!/bin/bash
# RUNBOOK.sh — zero-shot regeneration of the p-series package.
# Requires: Python >= 3.11 + sympy 1.14; ~15 min (dominated by the 1063
# [-4,4]^5 composed-square scans, run in four shards).
# The exact command sequence below was executed twice in the authoring
# container; regenerated JSONLs match the pins byte-identically (censuses)
# or minus the per-row `secs` field (scans).
set -euo pipefail
B="$(cd "$(dirname "$0")" && pwd)"; REPO="$(dirname "$B")"
for W in /home/claude/n1 /home/claude/n4 /home/claude/pseries; do
  if [ -e "$W" ]; then echo "refusing: $W exists (stale)"; exit 1; fi
done
echo "== 0. manifests =="
(cd "$B" && sha256sum -c MANIFEST.sha256)
(cd "$REPO/n4-degree67" && sha256sum -c MANIFEST.sha256)
echo "== 1. assemble the authoring layout =="
mkdir -p /home/claude/n1 /home/claude/n4 /home/claude/pseries
cp "$REPO/n4-degree67/stage_a_certify.py" "$B"/deps/*.jsonl /home/claude/n1/
cp "$REPO/n4-degree67"/n4_*.py "$REPO/n4-degree67"/n4_pisot*.jsonl \
   "$REPO/n4-degree67"/n4_scan*.jsonl /home/claude/n4/
cp "$B"/p_*.py "$B"/p4_totally_real.py "$B"/p8_box445.py /home/claude/pseries/
cd /home/claude/pseries
echo "== 2. P4 sweep (degrees 2-4 fresh; 5-7 asserted from pins) =="
python3 p4_totally_real.py | tee p4.out
grep -q "equality exactly once, at x^2-x-1. Zero falsifiers." p4.out
grep -q "P4 population: 13 totally-real" p4.out
echo "== 3. [-4,4]^5 census + 1063 scans (P8/P1/P2) =="
for s in 0 1 2 3; do python3 p8_box445.py $s 4 > p8_s$s.out 2>&1 & done; wait
grep -q '"pisot": 1545' p8_s0.out
test "$(wc -l < p8_scan5_box4.jsonl)" -eq 1063
python3 - <<'EOF'
import json
rows=[json.loads(l) for l in open('p8_scan5_box4.jsonl')]
assert all(r['clean'] and r['detector']==2 for r in rows), "P8/P1 falsifier?!"
print("1063/1063 clean, detector 2 everywhere")
EOF
echo "== 4. P3 aggregate + resolved-row re-asserts =="
python3 p3_aggregate.py | tee p3.out
grep -q "P3 AGGREGATE: 1117/1117" p3.out
echo "== 5. regenerated vs pinned =="
REPO_B="$B" python3 - <<'EOF'
import hashlib, json, os
B = os.environ["REPO_B"]
def rows(p): return [json.loads(l) for l in open(p)]
def strip(rs): return [{k: v for k, v in r.items() if k != "secs"} for r in rs]
for f in ("p4_pisot2_box3.jsonl", "p4_pisot3_box3.jsonl", "p4_pisot4_box3.jsonl",
          "p8_pisot5_box4.jsonl"):
    a = open(f, "rb").read(); b = open(f"{B}/{f}", "rb").read()
    assert a == b, f"{f}: byte mismatch"
    print(f"OK  {f} byte-identical to pin")
assert strip(rows("p8_scan5_box4.jsonl")) == strip(rows(f"{B}/p8_scan5_box4.jsonl"))
print("OK  p8_scan5_box4.jsonl == pin (minus secs)")
EOF
echo "P-SERIES RUNBOOK: ALL GREEN"
