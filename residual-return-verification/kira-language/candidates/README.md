# candidates/ — UNREWIRED EXTERNAL SOURCES

**These two files came from OUTSIDE our system.** They were sourced/authored elsewhere and are
**not yet rewired to kira-language conventions** (no exact-Fraction story, no loom bridge wired,
not import-disciplined to our rules). They are kept here, verbatim, as **review candidates** —
do **not** treat them as part of the project's wired surface yet.

| File | What it is | Verified this turn |
|---|---|---|
| `recursive_return_nlp.py` | A self-contained demo of a **recursive-return dictionary loop** on M₂(ℝ): tokens flow by gradient descent to residual 0 (`ker(L)`), and equal residues collapse to one learned dictionary value. The "acquisition loop." | runs; ‖ν‖→~1e-16 all tokens; M(M)=M; 4 tokens→2 values; cosine pattern +1/+1/−0.99/+1 as claimed. |
| `KL_DTA__Vsemantic_kernel.py` | A **compressed semantic kernel** over the same Cl(2,0)≅M₂(ℝ) carrier: a trace-zero residual `R_K`, a 25-entry `LAW_BANK` of jurisdiction-tagged statements (the **narrative firewall, already built**), a data/row layer, search/paragraph, sha256 digests, and an `audit()` gate. | all 5 CLI modes run; `audit ... closure==True`; R_K²=0 (9.6e-14); P0 spectrum {0,0,1,2}; jurisdiction tags correct (20 THEOREM / 5 COMPUTED). |

## Provenance
Copied (not moved) from the Claude local-agent uploads dir:
`...\local_ditto_7af96e11-...\uploads\c46e78e6-recursive_return_nlp.py` and
`...\37fc243a-KL_DTA__Vsemantic_kernel.py`.

## Posture / guardrails (unchanged)
- **Disjoint, one-way.** If/when wired, kira-language may bridge to `loom`; **L00M must never
  import these.** Neither file imports loom today (good for disjointness); a `bridge_loom.py`
  would add the read-only φ-keystone bridge.
- **Firewall.** `KL_DTA__Vsemantic_kernel.py` already enforces it via `Stmt.jurisdiction`
  (THEOREM/COMPUTED/INTERPRETIVE/FALSE_AS_STATED). `recursive_return_nlp.py` has interpretive
  framing ("NLP/meaning/speak") that would need firewalling if wired.
- **Do not modify behavior.** Verification only. Findings + the rewiring assessment live in
  `../SCOPING.md` §7.

## Known rewiring gaps (see SCOPING.md §7)
- `recursive_return_nlp.py` runs on import (**no `__main__` guard**) — not import-safe as a module.
- `KL_DTA__Vsemantic_kernel.py` prints Unicode with **no cp1252 guard** — crashes on a legacy
  Windows console unless `PYTHONUTF8=1` (the original `KL_DTA.py` has the `_AsciiSafeStdout` layer).
- Both are **float**; wiring into the exact substrate needs the §2(d) exact/float decision.

## What each candidate became (the rewired, shipped surface)

These two files are kept here **pristine** as the review/reference originals. The project's *wired*
surface — built from them, with the gaps above closed — lives in
[`../kira_language/`](../kira_language/README.md):

| Candidate (here, verbatim) | Rewired into | What changed |
|---|---|---|
| `recursive_return_nlp.py` (float; gradient flow + SVD; runs on import) | [`../kira_language/acquisition.py`](../kira_language/acquisition.py) | re-implemented **exact-only** over the `holding` Fraction carrier: the return op `L(X)=R·X+X·R−X`, an exact rational `ker(L)` nullspace (no SVD), an exact idempotent projector, and the sign-word — all decided with `==` on `Fraction`, zero tolerance; `__main__`-guarded. The corrected handoff hint (`N=H(0,-1,1,0) ∉ ker(L)`; the real generator is `i`) is pinned. |
| `KL_DTA__Vsemantic_kernel.py` (float; the dictionary/firewall/audit) | [`../kira_language/semantic_kernel.py`](../kira_language/semantic_kernel.py) | the project's **base copy** (kept float — the quarantined spectral-readings layer), with only honesty-critical fixes (decision (b): interpretive prose split into `INTERPRETIVE` rows; the `orbit_regimes` iteration convention made explicit). Its 27-entry `LAW_BANK` is the shipped firewall. |

So the candidates are the *acquisition-loop reference* and the *database base*; the exact wiring,
the φ-bridge, the growing lexicon, the store, and the dispatch shell are all in the package. The
verdict and the increment plan are `SCOPING.md` §7.5.

## Where this sits

- **The layer overview** — [`../README.md`](../README.md) (the Cl(2,0) carrier, the return operator,
  the lexicon, the store, dispatch; the one-way `../L00M` bridge).
- **The scope + this review** — [`../SCOPING.md`](../SCOPING.md) (§7 is the full verified
  cross-review of these two files); the readiness gate is [`../B1_READINESS.md`](../B1_READINESS.md).
- **The package map** — [`../kira_language/README.md`](../kira_language/README.md).
- **The package + site** — the residual-return [package README](../../README.md) and the live
  [GitHub Pages site](https://echo-s-studios.github.io/math-research-pipelines/).
