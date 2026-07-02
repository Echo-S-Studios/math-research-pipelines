# n4-degree67 — N4 executed: Pisot censuses and cross-shell scans at degrees 6–7

Execution of whitepaper next-step **N4** (`pisot_residue_whitepaper.v12.tex`,
§"Box and degree extensions", subsection N4). Exact arithmetic only.

## Results

| box | candidates | Pisot | patterns | scans |
|---|---:|---:|---|---|
| `[-2,2]^6` | 15 625 | **160** | 159 two-pair+spectator, 1 one-pair, 0 totally real | 160/160 Rat `{Φ1^6}`; 159/159 C2 `{Φ1^{deg S*}}`, detector 2 |
| `[-2,2]^7` | 78 125 | **414** | **309 three-pair** (first population), 105 two-pair | 414/414 Rat `{Φ1^7}`; 414/414 C2 `{Φ1^42}`, detector = pairs |

**Zero mirrored cross-shell classes through degree 7.** Degree-5 regression
gate: reproduces the archived 83/67/16 census and all 67 scans exactly.

Load-bearing census finding: the degenerate-chain population at degree 7
contains a **genuine Pisot**, `x^7-2x^6+2x^5+2x^4-2x^3-x^2+1`
(c = (1,−1,−2,2,2,−2,−2)), invisible to all four SC/RH certificate paths and
caught only by the in-run exact adjudication (non-reciprocity ⇒ no unimodular
roots ⇒ scaled Schur–Cohn sandwich). The empty-chain gap is not hypothetical:
unconditional adjudication is mandatory census discipline.

P7 resolved affirmatively: 3 sextic instances with reducible Rat°
(shapes 12+18, 12+18, 6+24), S* shrinking to degrees 12/12/24, scans still
inert.

Cross-engine: `n4_spot.gp` (PARI/GP `factor` + `poliscyclo`, an independent
decision path) agrees 4/4 with the sympy Newton/trial-division route,
including the adjudicated instance (`n4_spot.out`).

## Files

| file | role |
|---|---|
| `n4_lib.py` | generic-degree census (unconditional 4-path chain + in-run adjudication) and scan machinery (Rat, S* selection, composed square, torsion scans) |
| `n4_census_run.py` | census driver: degree-5 regression gate, then degrees 6, 7 |
| `n4_scan_run.py` | checkpointed, shardable scan driver |
| `n4_spot.gp` / `n4_spot.out` | GP cross-engine deck + pinned transcript |
| `n4_pisot{5_regression,6,7}.jsonl` | certified censuses |
| `n4_scan{5,6,7}.jsonl` | per-instance scan records |
| `n4_census.log` | census run transcript (tallies, adjudication partition) |

Engines: sympy 1.14.0 / Python 3.11.15; PARI/GP 2.15.4. Runtimes: censuses
42 s; scans 415 s (deg 6) + 1794 s wall (deg 7, four shards).
