# p-series — the falsifier table, executed in full

Artifact package for the definitive P1–P8 pass (report:
`../pisot-residue-verification/p-series-execution-report.md`). Exact
arithmetic throughout; every output SHA-pinned in `MANIFEST.sha256`.

## Contents

| file | role |
|---|---|
| `p_census.py` | box-parametrized census (unconditional 4-path chain + in-run exact adjudication; E1-corrected degree-2 branch) |
| `p4_totally_real.py` | P4: totally-real sweep, degrees 2–7, exact θ vs φ certificates in Z[φ] |
| `p8_box445.py` | P8/P1/P2: [−4,4]⁵ census + 1063 composed-square scans (shardable, checkpointed) |
| `p3_aggregate.py` | P3: fresh degree-2–4 Rat scans + archived-record aggregation |
| `p4_pisot{2,3,4}_box3.jsonl` | pinned censuses, degrees 2–4 in [−3,3]ⁿ (degree 2: 7 rows, E1-corrected) |
| `p8_pisot5_box4.jsonl` / `p8_scan5_box4.jsonl` | pinned [−4,4]⁵ census (1545) and live scans (1063) |
| `p4_run.log`, `p3_aggregate_run.log`, `p8_census.log`, `p8_aggregate.log`, `p3_box4_mixed.log`, `p_resolved.log` | pinned run transcripts |
| `deps/` | **deliberate duplicates**: read-only inputs pinned in external bundles (`pisot_n2.jsonl`, `n2_c2_scan.jsonl`, `n3_census.jsonl`, `pisot83.jsonl`), staged here so `RUNBOOK.sh` is self-contained; digests match the rev-2 bundle pins |
| `RUNBOOK.sh` | zero-shot regeneration + pin comparison (~15 min; needs `../n4-degree67/` for the shared library and archived scan records) |
| `ERRATA.md` | E1 fix log (changed pins) |

Results: P2 resolved 0/313 (+0/1063 next box); P3 2662/2662; P4 13/13
(twelve strict + golden equality); P5 7875; P6 589/589; P7 3+9 witnesses,
all inert; P8 empty through [−4,4]⁵; P1 zero-falsifier base 2016 live
instances. Nothing promoted.
