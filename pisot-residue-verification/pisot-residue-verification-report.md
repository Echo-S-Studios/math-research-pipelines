# Zero-Shot Verification Report — pisot-residue-verification

Independent re-verification of every claim of the whitepaper *"The Pisot
Cross-Shell Residue: A Reduction Lemma, Sharpness Witnesses, and an Exhaustive
Quintic Execution of the nu-Criterion"*, executed autonomously on 2026-07-02.

## 1. Integrity

**Zip SHA-256 match: YES.**

```
sha256(pisot-residue-verification.zip) =
f803ce52dbdfd070390df72749c3e77829783e732a5f231e2d60e31be9160404   (expected: identical)
```

Additionally, all 16 SHA-pinned artifacts in `MANIFEST.sha256` were verified
independently with `sha256sum -c` before the pipeline ran: **16/16 OK**. No
pinned artifact was edited at any point.

## 2. Environment

| component | version |
|---|---|
| OS | Ubuntu 24.04.4 LTS (Linux 6.18.5, single-core execution) |
| Python | 3.11.15 |
| sympy | 1.14.0 (exact pin satisfied) |
| PARI/GP | `GP/PARI CALCULATOR Version 2.15.4 (released)` |

The stack matches the whitepaper session's pinned versions (sympy 1.14.0,
PARI/GP 2.15.4); only the Python patch line differs (3.11.15 vs 3.12.3), which
had no observable effect — stage S10 confirmed byte-identical regeneration.

Command executed (primary path): `python3 run_all.py --extended` — **exit code 0**, total wall time 910 s.

## 3. Stage table

| id | verdict | wall s | evidence line (verbatim from stage output) |
|----|---------|-------:|---|
| S0 | PASS | 0.0 | `manifest: ALL OK` (16/16 committed artifacts) |
| S1 | PASS | 1.7 | `ALL ASSERTIONS PASSED in 1.4s -- every decision in Z[x]; no float anywhere.` |
| S2 | PASS | 1.9 | `cascade    rejects: +-1=39 (exp 39)  sturm=257 (exp 257)  reducible=45 (exp 45)  Salem=37 (exp 37)  sum=378 (exp 378)` |
| S3 | PASS | 67.6 | `CENSUS COMPLETE: 37/37 relationally inert; every complete scan returned exactly {Phi1^12}.` |
| S4 | PASS | 5.2 | `S4 OK: front2 sweep re-asserted via runpy; 103 quartic Pisots persisted, SHA pinned` + `pisot103.json sha256 fb349dc136e149718726df2e729184681b33fd22abb68585e077df7b0dfe792d` |
| S5 | PASS | 0.8 | `cross-engine: 55/55 signatures identical (sympy 1.14.0 trial division vs PARI/GP 2.15.4 factor+poliscyclo)` |
| S6 | PASS | 62.5 | `certified Pisot quintics: 83 (real5=0, mixed=16, 2pair=67)` |
| S7 | PASS | 68.5 | `NU FRONT COMPLETE in 68s: 67 two-pair instances (67 distinct-shell, 0 same-shell); mirrored cross-shell classes found: 0.` |
| S8 | PASS | 1.8 | `signatures agreeing: 237/237 (canonical 14/14, census 37/37, P4 103/103, P5 83/83); mismatches: 0` + `474 scan executions` |
| S9 | PASS | 1.4 | `S9 OK: supplementary claims verified in 1.1s -- all decisions exact` |
| S11 | PASS | 698.3 | `S11 COMPLETE (N1): 67/67 sympy C2 scans returned exactly {Phi1^(deg S*)} in 698s` |
| S10 | PASS | 0.0 | `manifest: ALL OK` (post-run: all regenerated artifacts byte-identical to pinned versions) |

All success-criteria lines from the task's STEP 3 appear verbatim in the
matching stage outputs. No stage was skipped; the PARI/GP fallback path was not
needed.

## 4. Claim checklist (README "Claim → verifier map")

| whitepaper item | claim | verdict | proved by |
|---|---|---|---|
| Lemma 2.3 | `2*phi(M)^2 >= M`, tight only at `M=2` (swept to 2e5) | ✅ | S1: `violations=[], tight cases=[2]` |
| §2 engine block | canonical signatures A–X, Lehmer, mixed, ledger-O, two-route, Kronecker square | ✅ | S1: `ALL ASSERTIONS PASSED ... no float anywhere.` |
| Prop. 3.3 (Z\*) | signature `{Phi1^4, Phi2^4}`; per-factor pins; torsion across factors | ✅ | S1 (`Z* x^4-3x^2+1 ... OK` + witness line) + S9 C3 |
| §7.1 census | Burnside 729/27/378; cascade 39/257/45/37; 37/37 `{Phi1^12}` | ✅ | S2 + S3: `CENSUS COMPLETE: 37/37 relationally inert` |
| §7.2 quartics | 103/103 `{Phi1^4}`; (EG) probe unfalsified (`theta > phi`) | ✅ | S4: `SWEEP COMPLETE ... both unfalsified on the box` |
| Thm. 6.1 (quintic box) | 83 Pisots (0/16/67); 83/83 `{Phi1^5}`; 67/67 `C2 = {Phi1^20}`; 0 mirrored classes | ✅ | S6 + S7: `mirrored cross-shell classes found: 0.` |
| Prop. 5.2 (no level-2 pin) | every modulus of `Rat0` attained ≥ twice, per instance | ✅ | S9 C2: `Rat0 has no real roots -> every modulus attained >= twice` |
| §7.3 ledger M run 3 | 237/237 signatures, dual-path, GP-native selection | ✅ | S8: `signatures agreeing: 237/237 ...` |
| run-2 consistency | 55/55 across engines | ✅ | S5: `cross-engine: 55/55 signatures identical` |
| Prediction P5 | `{-2..2}^6` family: exactly 7875 twist-classes | ✅ | S9 C1: `orbits 7875 (expect 7875)` |
| Next-step N1 | full sympy C2 coverage | ✅ | S11: `S11 COMPLETE (N1): 67/67 ...` |
| App. A manifest | artifact SHA-256 integrity + regeneration determinism | ✅ | S0 + S10: `manifest: ALL OK` (both), plus independent `sha256sum -c` 16/16 OK |

Predictions P1/P2/P8 are `[OPEN]` by design (the falsifiable frontier) and were
not treated as pipeline assertions, per the rules of engagement.

## 5. Deviations

**None.** Every stage returned PASS; exit code 0. No WARN (the exact sympy
1.14.0 pin was installed, so the S10 versioning caveat never triggered), no
NOT RUN (PARI/GP installed cleanly, so the fallback subset was unnecessary),
no non-benign `***` GP diagnostics, and no assertion failures anywhere.

## 6. Verdict

**All whitepaper claims verified.** The full extended pipeline
(`run_all.py --extended`, stages S0–S11 in canonical order) completed with exit
code 0 in 910 s on a single core under the exact pinned engine stack
(sympy 1.14.0 / PARI-GP 2.15.4). Every `[FORCED]`/`[COMPUTED]` claim in the
whitepaper's claim map reproduced exactly, both engines agree on all 237
dual-path signatures plus the 55 cross-engine signatures, the 67 quintic C2
scans were re-derived independently in sympy (N1), and all regenerated
artifacts are byte-identical to their SHA-pinned committed versions.
