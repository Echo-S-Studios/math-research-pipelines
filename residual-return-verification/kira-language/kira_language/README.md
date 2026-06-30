# `kira_language/` — the shipped language package

The layered, import-safe package behind the language layer. KIRA shells it as
`py -m kira_language` (one JSON request on stdin → one JSON result on stdout, ASCII-safe). Importing
the package itself does **no work and no I/O**: only `holding` (a pure-stdlib leaf) is eagerly bound;
numpy is pulled in only if you import `dispatch`/`semantic_kernel`.

The layers are one-directional — **nothing lower imports anything higher**:

```
holding (L0, exact, stdlib)
   |
   |<-  acquisition  lexicon  store          (exact, stdlib; the learning/persistence loop)
   |<-  semantic_kernel  loom_bridge  portable_io   (L1: float readings / the loom bridge / ASCII)
   |
dispatch (L3: the JSON-in/out KIRA shell over all of the above)
```

---

## Modules

| File | Layer | Role |
|---|---|---|
| [`holding.py`](holding.py) | L0 (exact) | **The exact-Fraction Cl(2,0) carrier — the B1 hard gate.** `H(a,b,c,d)` with coordinates in ℚ; `+ − · conj rev M ν R_K tr det disc rank Φ` and the `LAWS`/`TYPE`/`MASS` lattice, all staying in ℚ on rational input so synonymy (`X==Y`), `ν=0`, `R_K=0`, `det=0`, gate, and `residual_height` are decided **exactly (zero tolerance)**. Pure stdlib (`fractions`) — no numpy, no float, no `loom`. This is the module that may wire live into `L00M`. `R_K(X) = M(X) − τ(M(X))·1` is the trace-free Gram (zero ⟺ conformal; `R_K² = 0` always). |
| [`acquisition.py`](acquisition.py) | exact | **The exact recursive-return / acquisition loop.** The Sylvester self-action `L(X) = R·X + X·R − X` over the **φ keystone** `R = H(1/2, 1, −1/2, 0)` (= `loom.companion([1,-1,-1])` in carrier coords); `is_captured(X) = (L(X)==VOID)`; the exact rational nullspace `ker(L) = span{e₁+2e₂, i}` (dim 2, the phi-slack where learned values live); `project(X)` = the exact idempotent orthogonal projector onto `ker(L)` (the "commit"); and `word(X)` = a sign-aware sparse code (an `L1`-relative, sqrt-free, **COMPUTED** label). Hand-rolled `Fraction` Gaussian elimination, **no float / no numpy / no `loom`**. Rewires the float `candidates/recursive_return_nlp.py` into an exact-only mechanism. |
| [`lexicon.py`](lexicon.py) | exact | **The growing dictionary.** `Lexicon.add/lookup/generalize/snapshot` over the captures: the dedup key is the **exact committed residue** (`acquisition.project(X)`, `==` on `Fraction`), so tokens that return to the same exact value collapse to ONE entry (e.g. `X` and `X+ONE`) while distinct residues stay distinct (e.g. `i` vs `2i`, same word, different value). Stable ids are a sha256 of the canonical Fraction string (order-independent). Entries are tagged `COMPUTED` (learned, never `THEOREM`). |
| [`store.py`](store.py) | exact | **Exact JSON persistence + a sha256 hash-chain.** `manifest/persist/load/verify/restore` mirror the substrate's witness store (`sha256(prev + json)[:16]` from a `"genesis"` seed). `restore` **re-derives** the lexicon by replaying each value through the acquisition loop and cross-checks id/coords/word/jurisdiction — so `restore(persist(lex)) == lex` exactly and any edited record breaks both the chain and the re-derivation. Deterministic ASCII bytes; pure stdlib + `lexicon`/`holding`. |
| [`semantic_kernel.py`](semantic_kernel.py) | L1 (float) | **The database base (the dictionary + firewall + audit).** The compressed `KL_DTA` kernel: a `Cl` carrier, the trace-zero residual `R_K`, a 27-entry jurisdiction-tagged `LAW_BANK` (the narrative firewall — `THEOREM`/`COMPUTED`/`INTERPRETIVE`/`FALSE_AS_STATED`), a `Row`/`dataset` data layer, `search_statements`/`paragraph`, sha256 digests, and the `audit()` closure gate (`closure==True`). **Float** (spectral readings: `eigvalsh`, entropy, purity) — the quarantined-float layer; its decisions never cross into an exact `L00M` decision. Does **not** import `loom`. |
| [`loom_bridge.py`](loom_bridge.py) | L1 | **The one-way φ-keystone bridge to `loom`.** The only runtime/library module that imports `loom`. `phi_keystone()` confirms, read-only and **never raising**, that the void law `x²=x+1` → `loom.companion([1,-1,-1]) = [[0,1],[1,1]]` → `Cl(0.5, 1, −0.5, 0)` → `loom.mahler_measure ≈ φ` — the single object where the acquisition `R`, `KL_DTA`'s keystone, and `loom`'s `CATALOG_SEEDS["phi"]` coincide. If `loom` is unreachable it returns `{"loom_reachable": False, …}` rather than crashing. Resolves the L00M root via `KIRA_LANG_L00M_ROOT`, else `../../L00M`. |
| [`dispatch.py`](dispatch.py) | L3 | **The KIRA-shell JSON-in/out surface** (mirrors `L00M`'s `vector_api`). One request JSON → one result JSON, **never raising across the wire** (every endpoint catches its own exceptions; ASCII output). The 13 verbs: **QUERY** `read[/exact]·laws·search·audit·bridge·lexicon`, **GENERATE** `render` (alias `speak`), **INGEST** `observe·propose·commit` (the acquisition+lexicon loop; `commit` is the **sole** state-growing verb, propose-for-confirm), **STORE** `persist·restore`. Stateless: the lexicon travels IN the request. Firewalled: only `WIRED_JURISDICTIONS` cross as fact. `read` is float (declared `tol`); `read exact:true`, `render`, `observe/propose/commit` return exact Fraction-as-string. |
| [`portable_io.py`](portable_io.py) | util | **ASCII/cp1252-safe stdout** so `py -m kira_language` never tracebacks on a legacy Windows console (KIRA shells it raw, no `PYTHONUTF8`). A `_GLYPH_ASCII` transliteration table + an `_AsciiSafeStdout` proxy; `install()` is idempotent and never raises. Stdlib-only, ported from `KL_DTA`'s output guard. |
| [`__init__.py`](__init__.py) | — | The import-safe package surface: eagerly binds only `holding` (and re-exports `H`, `VOID`, `ONE`). Importing pulls no numpy and no `loom`. |
| [`__main__.py`](__main__.py) | — | The `py -m kira_language` entry: `portable_io.install()` then `dispatch.main()` (stdin→stdout). Import-safe (guarded). |

---

## The exact path vs the float layer

The decision-bearing path is **all exact `fractions`**:
`holding` → `acquisition` → `lexicon` → `store`, and the exact branches of `dispatch`
(`read exact:true`, `render`, `observe`, `propose`, `commit`). The **float layer** —
`semantic_kernel` (spectral readings) and plain `read` — is quarantined behind declared tolerances
and is the only thing that pulls numpy. This split is the **B1 hard gate** (decision (d)): exact
facts are exact; analytic readings carry an explicit, named tolerance, and never feed an `L00M`
decision.

See [`../README.md`](../README.md) for the layer overview, [`../SCOPING.md`](../SCOPING.md) for the
design decisions, and [`../B1_READINESS.md`](../B1_READINESS.md) for the readiness gate. The φ
keystone reaches the exact core over in [`../../L00M`](../../L00M/README.md) one-way.
