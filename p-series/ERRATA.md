# ERRATA — p-series package (2026-07-02 referee pass)

## E1 — degree-2 census undercount (fixed)

The v1 adjudication rule "reciprocal ⇒ not Pisot" is `[FORCED]` only for
degree ≥ 3. At degree 2 the reciprocals `x²−kx+1, k ≥ 3` **are** Pisot
(θ, 1/θ), and `x²−3x+1 = minpoly(φ²)` sits in the empty-chain population
(c₀ = 1 degenerates all four paths), so the first run silently dropped it.

Fix: `p_census.py` (and the sibling `n4-degree67/n4_lib.py`) now guard the
reciprocal disposal with `n >= 3` and decide degree-2 self-inversive
candidates by the exact discriminant (disc < 0 ⇒ unimodular pair ⇒ not
Pisot; disc > 0 ⇒ real pair θ, 1/θ, interior 1 automatic — the sandwich
cannot separate unimodular pairs and is not used there).

Cascades: `p4_pisot2_box3.jsonl` 6 → **7** rows (adjudicated instance
`(1,−3)`); P4 12 → **13** totally-real instances (twelve strict + the
golden equality; the new certificate is `P(φ) = 1−√5 < 0`, θ = φ² — P4
unfalsified); P3 aggregate 2661 → **2662**. Degree ≥ 3 outputs are
untouched (verified: the degree-5 census reproduces its pinned instance
set exactly under the patched library).

## Changed pins

| file | old digest (first pin) | new |
|---|---|---|
| `p_census.py` | `5b6c…` (see git history) | this revision |
| `p4_totally_real.py` | unchanged logic; rerun output | this revision |
| `p4_pisot2_box3.jsonl` | 6-row version | 7-row version |
| `p4_run.log` / `p3_aggregate_run.log` | — | regenerated post-fix |
| `../n4-degree67/n4_lib.py` | first pin | same E1 guard (deg ≥ 3 behavior identical) |

All other artifacts: unchanged, digests as pinned. The referee's own
independent census (chain-first + enclosures) lists the same seven
degree-2 instances.
