# ERRATA — n4-degree67 package (2026-07-02 referee pass)

**E1 (shared with p-series).** `n4_lib.py`'s adjudication disposal
"reciprocal ⇒ not Pisot" is `[FORCED]` only for degree ≥ 3; the library now
guards it with `n >= 3` and decides degree-2 self-inversive candidates by
the exact discriminant. **No output of this package changes** — the N4
censuses run at degrees 5–7 where the original rule is valid; the degree-5
census was re-executed under the patched library and reproduces its pinned
instance set exactly. The re-pin is purely a soundness fix for the
library's generic contract. `stage_a_certify.py` (digest `d06d0c97…`,
identical to the N1-bundle pin) and `RUNBOOK.sh` are added to make the
package self-contained for zero-shot verification.

**E2 (documentation).** The whitepaper's displayed expansion of the
degree-7 adjudicated Pisot was a typo for its c-vector; the pinned
`n4_pisot7.jsonl` row and all scans always used the c-vector
`(1,−1,−2,2,2,−2,−2)`, i.e. x⁷−2x⁶−2x⁵+2x⁴+2x³−2x²−x+1. No data change.
