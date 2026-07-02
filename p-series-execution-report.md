# Execution Report — The P-Series, Run in Full

Definitive pass over all eight rows of the whitepaper's falsifier table
(§9), 2026-07-02. Every resolved row re-asserted from pinned data; every
open row given a fresh falsifier search. Exact arithmetic throughout.
Artifacts in `p-series/` (SHA-pinned).

## Status table

| ID | prediction | run | outcome |
|----|---|---|---|
| P1 | general Pisot inertness | falsifier scan over every live instance on record + the new [−4,4]⁵ box | **2016/2016 composed-square scans clean** (313 + 67 + 159 + 414 + 1063); zero falsifiers; stays [OPEN] — evidence, not promotion |
| P2 | 0 mirrored classes in [−3,3]⁵ | re-asserted from pinned `n2_c2_scan.jsonl` | **resolved: 0/313**; corollary at the next box: **0/1063 in [−4,4]⁵** |
| P3 | every certified Pisot's Rat scan = {Φ₁^deg} | fresh scans deg 2–4 (6+37+103) + archived deg 5–7 + new box | **2661/2661** (1116 + 1545); [FORCED] by Thm 7.13 and observed without exception |
| P4 | totally-real Pisot ⇒ θ ≥ φ, equality only at degree 2 | fresh sweep deg 2–3 ([−3,3]ⁿ), deg 4 re-census, deg 5–7 + [−4,4]⁵ populations | **12/12 certified exactly** (sign of P(φ) in Z[φ]): θ > φ eleven times, θ = φ exactly once, at x²−x−1; zero falsifiers; stays [OPEN] as a general statement |
| P5 | N3 Burnside = 7875 | re-asserted (in-run assert + pinned log) | **resolved: 7875** |
| P6 | every N3 Salem class inert | re-asserted from pinned `n3_census.jsonl` | **resolved: 589/589 {Φ₁¹²}** |
| P7 | reducible Rat° instances exist | re-asserted from pinned `n4_scan6.jsonl` + new box | **resolved: 3 instances** at degree 6 (shapes 12+18, 12+18, 6+24; S\* degrees 12/12/24) **+ 9 new at degree 5** in [−4,4]⁵ (shapes 10+10, S\* still 20); all inert |
| P8 | same-shell two-pair quintics | merged-shell hunt extended to [−4,4]⁵ (1063 live scans) | **none found**: detector = 2 on all 1063; empty range now [−2,2]⁵ ∪ [−3,3]⁵ ∪ [−4,4]⁵ (1443 two-pair quintics) plus every degree-6/7 live instance; stays [OPEN] |

## The new computations

**P4 (first standalone execution).** Populations: degree 2, [−3,3]²: 6
Pisots, all totally real; degree 3, [−3,3]³: 37 Pisots, 5 totally real;
degree 4, [−3,3]⁴: 103 Pisots, 1 totally real (fresh census matches the
archived quartic sweep exactly, 103 = 103); degrees 5–7 boxes and [−4,4]⁵:
0 totally real. Certificate per instance: P(φ) evaluated exactly in Z[φ]
(φ² = φ+1 reduction; sign of a + bφ via integer squares against √5) — since
θ is the unique root above 1, θ > φ ⟺ P(φ) < 0 and θ = φ ⟺ P = x²−x−1.
Result: eleven strict certificates, one equality (the golden minimal
polynomial), zero falsifiers.

**P8/P1/P2 at [−4,4]⁵.** Census: 59 049 candidates → **1545 Pisot quintics**
(1063 two-pair, 482 one-pair, 0 totally real); degenerate chains 7416
(162 reciprocal / 7220 reducible / 33 irreducible non-Pisot / **1 Pisot**).
The 1 is a degree-5 first: x⁵−4x⁴+2x³+x²−3x+1 (c = (1,−3,1,2,−4)) is
invisible to all four certificate paths and was caught only by the exact
in-run adjudication — the degenerate-chain Pisot phenomenon is not a
degree-7 quirk; it reaches quintics one box out. (It lies outside [−3,3]⁵,
so the archived 431 census remains complete, consistent with the rev-2
adjudication; it is a one-pair instance, its typing closed by the reduction
theorem.) Scans: **1063/1063 clean** — Rat = {Φ₁⁵} on all 1545 (1063
in-scan + 482 one-pair batch), detector = 2 on every live instance (no
merged shell anywhere), composed squares exactly {Φ₁²⁰}, no Φ₂, no higher
content. Nine instances have reducible Rat° (shape 10+10, both factors
carrying unimodular roots so S\* remains degree 20) — **P7 witnesses now
exist at degree 5**, first observed one box out from the archived census.

**P3 aggregate.** Fresh complete Rat scans for degrees 2–4 (146 instances)
plus every archived record: 2661/2661 = {Φ₁^deg}, no Φ₂, no higher content
anywhere — Thm 7.13's forced prediction observed without exception across
six degrees and five boxes.

## Verdict

The P-series is fully executed. Resolved: P2, P5, P6, P7 (P7
affirmatively). Forced-and-observed: P3 (2661/2661), P5. Open with
strictly enlarged zero-falsifier evidence: P1 (2016 live instances),
P4 (12 totally-real instances, equality pattern exactly as predicted),
P8 (1443 two-pair quintics across three boxes, no merged shell anywhere).
Nothing is promoted; the falsifiable frontier stands, now much better
tested. Methodological yield: two more degenerate-chain Pisots (degree 4
in [−3,3]⁴ re-census; degree 5 in [−4,4]⁵) — unconditional in-run
adjudication is confirmed as mandatory census discipline at every degree.
