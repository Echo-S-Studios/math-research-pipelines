# B1-READINESS — kira-language

**STATUS: READY for the B1 wire.** Every PREP_PLAN §3 invariant is green, codified as executable
assertions in `test_b1_readiness.py` and backed by the per-increment suites. *2026-06-23.*

> **Scope of "ready":** the disjoint language space is *prepared* for B1 — the live KIRA
> `/api/language/*` wire. **B1 itself is a separate, Ace-gated, cross-repo step and is NOT part of this
> prep** (no KIRA route is added here). This document records the prep gate, not the wire.

---

## The §3 checklist — all green (codified in `test_b1_readiness.py`)

| # | Invariant | Verified by | Evidence |
|---|---|---|---|
| 1 | **Import-safe** | `test_import_safe` | `import kira_language` pulls no numpy/loom; every shipped module imports clean + side-effect-free |
| 2 | **ASCII/cp1252-safe** | `test_ascii_cp1252_safe` | `py -m kira_language` under `PYTHONIOENCODING=cp1252` (no PYTHONUTF8) → pure-ASCII JSON |
| 3 | **Exact** (zero-tol) | `test_exact_zero_tolerance` | `nu(P0)=∅`, `R_K(𝟙)=∅` by `==`; exact `ker(L)` membership + idempotent projector; all-Fraction |
| 4 | **Float quarantined** | `test_float_quarantined_and_declared` | `read` float → `exact:false` + declared `tol`; `read exact:true` → Fraction-as-string |
| 5 | **Firewall** | `test_firewall` | default `laws` exclude INTERPRETIVE/FALSE; `WIRED_JURISDICTIONS=(THEOREM,COMPUTED)`; new verbs COMPUTED |
| 6 | **One-way** | `test_one_way_and_live_phi` | L00M references `kira_language` **nowhere**; only `loom_bridge` imports loom; φ agrees with **live** loom |
| 7 | **Persistent** | `test_persistent` | lexicon `persist→restore` exact; sha256 chain verifies; tamper → `verify` False |
| 8 | **KIRA-shell-ready** | `test_kira_shell_ready` | the §4 contract (13 verbs) complete; in-proc `dispatch(req)` == subprocess for every endpoint |
| 9 | **Green** | `test_suite_green_headline` + the run | full suite **121 passed** (collectable, ≥ the increment-6 headline) |
| 10 | **Math preserved** | `test_math_preserved` | `LAW_BANK`=27 (20 THEOREM/5 COMPUTED/2 INTERPRETIVE); KL_DTA spine + conformance collect; candidates pristine |

The readiness gate is **load-bearing** (mutation-proven, not vacuous): a firewall breach
(`WIRED += INTERPRETIVE`), a one-way breach (`holding` imports `loom`), and an exact breach
(projector returns its input) are each caught by the corresponding readiness test.

---

## Build provenance — increments 1–7 (local repo, no remote)

| Increment | Axis | Commit | What | Gate |
|---|---|---|---|---|
| base + 1 | — / ABILITY | `a1ce76c` → `6cd3800` | semantic-kernel base + φ-bridge + read-only api; **exact-Fraction core** `holding.py` | 25 → 40 → 48 |
| 2 | SYNTAX | `f925e50` | layered package `kira_language/` + import-safety + cp1252 | 48 |
| (prep) | — | `bd9fccd` | B1-readiness prep plan + handoff | — |
| 3 | NLP | `4817b62` | **exact acquisition loop** `acquisition.py` (Sylvester `L`, exact `ker(L)`, idempotent projector, word) | 65 |
| 4 | NLP | `d1312ed` | **growing lexicon** `lexicon.py` (exact dedup by residue, deterministic ids, COMPUTED) | 77 |
| 5 | ABILITY | `663e00e` | **sha256-chain JSON store** `store.py` (exact round-trip, tamper-evident) | 89 |
| 6 | ABILITY | `f06ba5d` | **full KIRA-shell dispatch** (lexicon/render/observe/propose/commit/persist/restore; robustness fix) | 111 |
| 7 | GATE | *(this, held)* | **B1-readiness gate** `test_b1_readiness.py` + `B1_READINESS.md` | 121 |

## Test inventory (121 total)

| File | Tests | Pins |
|---|---|---|
| `test_KL_DTA.py` | 9 | the verifier spine (unchanged) |
| `test_kl_dta_conformance.py` | 16 | the 3-route closure incl. the exact loom route |
| `test_holding.py` | 8 | the exact-Fraction core, zero tolerance |
| `test_bridge_loom.py` | 2 | the one-way φ keystone vs live loom |
| `test_language_api.py` | 13 | dispatch local-equivalence + firewall (the original surface) |
| `test_acquisition.py` | 17 | exact `ker(L)`, projector, word, generalization |
| `test_lexicon.py` | 12 | growing dict, exact dedup, deterministic ids |
| `test_store.py` | 12 | exact persistence, sha256 chain, tamper-evidence |
| `test_dispatch_full.py` | 22 | the full §4 surface, robustness, fact-only render |
| `test_b1_readiness.py` | 10 | the §3 checklist (this gate) |

## The gate (reproduce)

```
cd C:\Users\acead\projects\kira-language
py -m pytest -q                          # -> 121 passed
py -m pytest test_b1_readiness.py -v      # -> the §3 checklist, 10 passed
```

---

## Next (separate, Ace-gated)

**B1** = add additive `/api/language/observe|propose|commit|read|render|persist|restore` routes to KIRA
that shell into `py -m kira_language`, gated by KIRA's existing single emission gate. That is the live
wire — a distinct cross-repo step requiring Ace's go. It is **not** started here.
