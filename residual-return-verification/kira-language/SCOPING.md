# kira-language — Scoping & Roadmap

**Status: HELD for Ace's review. Scope only — nothing in this doc is built or wired yet.**
*Date: 2026-06-23.*

---

## 0. What this project is, and the posture

`kira-language` is a **disjoint wiring hub** built around `KL_DTA.py`. Its job: turn the
test-pinned *grammar of operations/readings on a Cl(2,0) holding* into a layer that wires
**language → through KIRA → through matrix-plates → into L00M**.

**The non-negotiable invariant — one-way dependency:**

```
kira-language  ──reads──▶  loom   (the φ keystone bridge; ALLOWED)
L00M           ──imports─▶  KL_DTA / kira-language   (NEVER)
```

L00M stays exactly as it is. It never learns this project exists. The bridge reaches out
*from here*; nothing reaches back in. (This mirrors loom's own G9 kernel-independence —
the bridge lives only in test/bridge code, never in either kernel.)

Two disciplines carried over from L00M and preserved here:
- **Two-route closure ethos** — every identity is checked two independent ways, residual 0
  (here: cocycle/`Cl` route vs numpy matrix route; the loom bridge adds a third, exact route).
- **Exact-vs-asserted firewall** — the *algebra* is proven content (wireable); the *ToE/physics
  narrative* is commentary only, **never wired as if proven**.

### What was set up this turn (verified)

| Item | Result |
|---|---|
| Folder | `C:\Users\acead\projects\kira-language\` created |
| Files copied (not moved) | `KL_DTA.py`, `test_KL_DTA.py`, `test_kl_dta_conformance.py` (byte-identical) |
| L00M originals | untouched, still committed |
| `py KL_DTA.py` here | runs, exit 0, `passed=True` |
| `conftest.py` | added — one-way loom reach (see below) |
| Full suite here | **25 passed in 2.00s** |

### How this project reaches loom (recommended option, in place)

`test_kl_dta_conformance.py` needs `loom` for its exact third route. The options were:
**(i)** sys.path to the L00M clone · **(ii)** vendor a copy of loom · **(iii)** leave the test
pointing at L00M.

**Chosen / recommended: (i), via `conftest.py`** — it *appends* the L00M root to `sys.path`
(env-overridable `KIRA_LANG_L00M_ROOT`, default sibling `../L00M`). Appending (not prepending)
means the **local** `KL_DTA.py` is always the module under test; only `loom` — absent here —
falls through to the real kernel. Cleanest one-way option: no duplication, **no drift**, bridge
stays honest against the live loom.

> **Vendoring (option ii) is the documented fallback**, to be taken only if/when kira-language
> must run with no L00M clone present (e.g. isolated CI). It buys portability at the cost of a
> drift-management burden. **Flagged as a scoping decision, not taken now.**

---

## Build log

**2026-06-23 — Increment 1 BUILT (held for Ace's independent verification; no commit).** Decisions a–f ratified.
- `git init` (local, branch `main`, no remote, **no commit** — separate history enforces the one-way rule).
- `semantic_kernel.py` — the **database base** (copy of the candidate + (b) gloss fixes: `observer`/`framework`
  equations stay THEOREM with factual invariants, interpretive prose split into 2 `INTERPRETIVE` rows;
  `orbit_regimes` iteration convention made explicit). Audit `closure` still **True** (now 27 statements).
- `bridge_loom.py` — the **one-way φ-keystone bridge** (the only module importing loom; self-bootstraps the
  path; never raises). Live result: `agree=true`, companion `[[0,1],[1,1]]`, Mahler == φ.
- `language_api.py` — **read-only JSON dispatch** (`read`/`laws`/`search`/`audit`/`bridge`), mirroring
  `vector_api`; **firewall at the wire** (`wired_only` default → 25 laws; full → 27); float + declared
  tolerance (exact core = next increment); `ensure_ascii` output; never raises across the wire.
- Tests: `test_language_api.py` (local-equivalence + firewall) + `test_bridge_loom.py`. **Gate: 40 passed**
  (25 original + 15 new). One self-caught bug — a wrong test assertion that conflated `ν` and `R_K` (corrected;
  it now pins the §7.3 distinction).
- **Deferred (immediate follow-ups):** exact-Fraction core (d) · `recursive_return` rewire (f) ·
  import-safety/cp1252 guard · JSON store.

**2026-06-23 — Increment 1 GREENLIT** (independent verification PASS, 7/7 checks) and committed
locally (no remote). Recorded nuance: `bridge_loom` is the only *runtime/library* module importing
loom; `test_kl_dta_conformance.py` also imports loom (read-only, test-only) — so the one-way rule
holds for shipped modules, not literally every file in the tree.

---

## 1. The Language, formalized

> Claim to pin down: *"the operations produce genuine language."* Made precise below — it is a
> **many-sorted algebraic signature with observations**: a generative grammar over one unit, an
> enumerable lexicon, total denotation maps, and a judgemental layer where *a reading vanishing
> is the truth condition*. Syntax + semantics + a typing theory = a language.

**The unit (the sort).** A **holding** `X ∈ Cl(2,0) ≅ M₂(ℝ)`, coordinates `(a,b,c,d)` over the
basis `{𝟙, e₁, e₂, i}`. This is the atom — the "word."

**The productions (grammar — closed `Holding → Holding`).** How holdings are formed from holdings.
Closure is the grammaticality guarantee: any composition yields a holding.

| Production | Symbol | Role |
|---|---|---|
| fold | `X + Y` | ∅-rooted superposition (identity ∅) |
| negate | `−X`, `X − Y` | additive involution |
| geometric product | `X · Y` | carrier-rooted (identity 𝟙); `= inner ⊕ outer` |
| scalar action | `a · X` | grade-preserving scaling |
| conjugation | `X̃ = tr·𝟙 − X` | prov-pairing involution |
| reversion | `rev X` | transpose (negates `i`) |
| observation | `M(X) = X̄X` | Gram/moment map → symmetric cone |
| defect | `ν(X) = M(X) − X` | the "rest"/agreement obstruction |
| char-poly op | `Φ_X(Y) = Y² − tr(X)Y + det(X)𝟙` | binary; `Φ_X(X)=∅` (Cayley–Hamilton) |
| polar factor | `X = Q·P` | (witnesser Q ∈ O(2), witness P = √M) |
| flow | `exp(t·G)` via ε | one-parameter evolution (clock/boost/shear) |

**The semantics (readings — `Holding → Scalar / Type / Sign`).** The "meaning" of a holding is
the tuple of its readings. All total; all residual-0-verifiable.

| Reading | Codomain | Meaning |
|---|---|---|
| `tr` | ℚ/ℝ | additive provenance (λ₁+λ₂) |
| `det` | ℚ/ℝ | multiplicative provenance (λ₁λ₂); split norm `a²−b²−c²+d²` |
| `disc` | ℚ/ℝ | spectral gap² `tr²−4det` |
| `obs`, `q`, `pt`, `s2` | ℚ/ℝ | derived prov-at-two-depths readings |
| `rank` | {0,1,2} | K-theory stratum (∅ / null-cone / invertible) |
| `TYPE` | ⊆ {idem,rest,metric,flow,gen} | residual-signature: which laws vanish |
| `MASS` | ℕ | how many laws vanish (intersection multiplicity) |
| `ε` = sign(disc) | {−,0,+} | flow class (elliptic/parabolic/hyperbolic) |
| `spectrum` | ℂ² | eigenvalues (analytic) |
| `mahler` | ℝ | growth rate (analytic, via loom bridge) |

**The judgements (the proof/typing layer — where meaning becomes truth).**
- **Synonymy / witness:** `X ≡ Y  ⟺  (X−Y) = ∅` (residual `< _tol`). *A reading vanishing is the
  truth condition.* This is the satisfaction predicate of the language.
- **Up-to-gauge:** `X ≈ Y  ⟺  M(X) = M(Y)` (same observation; differ only by the time/phase fiber).
- **Typing:** `X : τ` where `τ = TYPE(X)` — a holding's type is the set of laws it satisfies.
- **Capture (substrate word for "learned"):** residual against a basis `= 0`.

**The lexicon (vocabulary — explicit and enumerable).** The "known words," already present in
`KL_DTA.py` as data, to be exposed as a queryable table:

| Set | Count | Members |
|---|---|---|
| `BASIS` | 4 | 𝟙, e₁, e₂, i |
| `CONSTANTS` | 13 | ∅, 𝟙, e₁, e₂, i, R, P, P₀=½(𝟙+e₂), φ𝟙, ψ𝟙, −𝟙, Rₙ(n=2), 𝟙+i |
| `NODES` | 8 | ① ∅, ② carrier, ③ divide, ④ M, ⑤ ν, ⑥ L0-cocycle, ⑦ L★-seed-eq, ⑧ norm |
| `LAWS` | 5 | idem (X²=X), rest (ν=∅), metric (X²=𝟙), flow (X̄=−X), gen (X²=X+𝟙) |

> **The genuinely novel content of this language: meaning is residual-valued.** A sentence
> *means* its tuple of readings; two sentences are *synonymous* iff a residual vanishes (ν=0);
> a holding's *type* is which laws vanish on it. That is a complete little language — and it is
> exactly the "semantic candidate" Ace approved.

---

## 2. Key decisions (surfaced for Ace — recommendation given, but his call)

### (a) Is "the language" operations-on-one-algebra, catalog-of-constants, or a composition?
**Recommendation: a defined composition, layered.**
- **Grammar = operations-on-one-algebra** (KL_DTA's strength) — the productions + readings + judgements above. This is the language *proper*.
- **Lexicon = extensible by the catalog-of-constants** — each L00M degree-2 catalog seed maps to a
  named holding via `unmat(loom.companion(minpoly))`, adding lexicon entries through the bridge.

So: **language = grammar(KL_DTA) over lexicon( KL_DTA-core ∪ loom-degree-2-catalog )**. The two
stop being rivals: one supplies the rules, the other supplies extra words.
→ **Needs Ace:** confirm the layering (vs. picking one side).

### (b) The narrative firewall (algebra wired, physics commentary-only)
**Recommendation: enforce structurally at the JSON boundary.** Only algebraic readings
(tr/det/M/ν/rank/TYPE/MASS/spectrum/mahler — all residual-0-verifiable) ever cross the dispatch
surface or land in the store. The ToE/physics narrative stays in docstrings and, if surfaced at
all, only in a clearly-labelled `commentary` field that is **never consumed as a claim**. The
firewall becomes *what is allowed to cross the wire*, not a matter of discipline.
→ **Recommended as policy; Ace to ratify** (this is a guardrail, low controversy).
→ **UPDATE (§7): already implemented** in the `KL_DTA__Vsemantic_kernel.py` candidate as
  `Stmt.jurisdiction` (THEOREM/COMPUTED/INTERPRETIVE/FALSE_AS_STATED) — decision (b) is *built*,
  not just designed, and the candidate's 25-entry `LAW_BANK` is correctly tagged (20 THEOREM / 5 COMPUTED).
  *(The shipped `kira_language` kernel acted on the §7.2 recommendation below and is now **27**:
  20 THEOREM / 5 COMPUTED / 2 INTERPRETIVE — the two gloss companions demoted out of THEOREM.)*

### (c) Degree-2 scope, or generalize beyond Cl(2,0)≅M₂(ℝ)?
**Recommendation: explicit degree-2 grammar layer for v1, with a generalization *seam*.**
- v1 is honest: Cl(2,0) is degree-2 / 4-real-dim, and the proven loom bridge is degree-2 only.
- BUT the *readings* (tr/det/M/ν/rank/Φ/spectrum/mahler) are all already defined for
  general-degree companions in loom. So design the reading API against a `Holding` protocol that
  can *later* accept a loom companion of any degree — without rewriting the carrier now.
- Degree-4 catalog seeds (`K, cons, res`) and the substrate's degree-4 learner field
  (Q(√2+√3)) are **explicitly out of v1 scope** and noted as the generalization frontier.
→ **Needs Ace:** degree-2-honest v1 (recommended), or a general-degree carrier from day one?

### (d) Exactness: exact-Fraction reimplementation, or bounded-float boundary?
**Recommendation: exact-Fraction core + a sharply-bounded float layer.**
- The *algebra* is rational: `+ − · conj rev M ν disc Φ tr det rank TYPE MASS` on rational inputs
  stay in ℚ. An exact-Fraction `Holding` satisfies the substrate's G8 with no loss — and Cl(2,0)
  needs no irrationals for its core.
- Floats appear **only** in analytic readings (`√` in the polar factor, `exp` flows, `spectrum`,
  `mahler`) — quarantined behind declared tolerances mirroring the bridge's existing
  `ALG_TOL=1e-9` / `DK_TOL=1e-6`.
- This is the clean wiring story into the exact substrate, and it keeps the firewall sharp: exact
  facts are exact; analytic readings carry an explicit, named tolerance.
→ **Needs Ace:** confirm the exact-core reimplementation is worth it (recommended) vs. shipping a
  documented float boundary first.
→ **UPDATE (§7): both external candidates are float today.** `recursive_return` is *intrinsically*
  numerical (gradient flow + SVD) — it stays float by nature. The semantic kernel is rational
  except its spectral readings (`eigvalsh`/entropy/purity/probs), which fit the quarantined-float
  layer exactly. Its core algebra (mul/mat/M/τ/det/R_K) is rational-expressible → exact-core-able.

---

## 3. The wiring path

**Through KIRA (mirror `vector_api`'s shell).** A new `language_api.py` with `dispatch(req)` +
`main()` reading one request JSON from stdin and writing one result JSON to stdout, so a KIRA
endpoint is exactly `py -c "import language_api; language_api.main()"`. Verified by **local
equivalence** (in-process `dispatch(req)` diffed against the same subprocess), the repo's own
pattern. Proposed endpoints:

| Endpoint | Input → Output |
|---|---|
| `read` | a holding `(a,b,c,d)` → all readings (tr/det/disc/obs/rank/TYPE/MASS/ε) |
| `type` | a holding → `TYPE` + `MASS` |
| `witness` | two holdings → `ν`, `≡`, `≈` (the synonymy judgement) |
| `product` / `fold` | two holdings → their `·` / `+` (a production) |
| `lexicon` | (none) → the enumerable named vocabulary |
| `bridge` | a degree-2 minpoly → holding via `unmat(companion)` + readings + 3-route residual |

**Into matrix-plates / L00M.** Language flows *through* KIRA, never by import: the KIRA host calls
`language_api` (this project), then feeds results into L00M's existing `vector_api` / substrate
store. kira-language is never on L00M's import graph — one-way preserved end to end.

**Bridge to loom at the φ keystone (and generalizing the 3-route conformance).** The keystone
(`x²=x+1`, companion `[[0,1],[1,1]]` = `Cl(0.5,1,-0.5,0)`, Mahler = φ) is both KL_DTA's seed and
`CATALOG_SEEDS["phi"]`. Generalize the existing 4-poly bridge to **all degree-2 catalog seeds**
(`phi, tau, sq2, sq3, sq5, gap`) so every degree-2 constant becomes a *verified* lexicon entry
(three routes agree, residual 0). Degree-4 seeds stay out (the (c) frontier).

**Persistence + stable IDs (if a "database" is wanted).** Mirror `vector_substrate_store`: a
holding's stable ID = its monic-integer minpoly when it is an algebraic-integer holding, else a
canonical hash of its exact (Fraction) components. Lexicon/growth records persisted as
`(id, name, components, readings)`, with the same `sha256(prev+json)[:16]` hash-chain (genesis
seed) the substrate already uses — so records drop natively into the L00M store later.
→ **Needs Ace:** is a persistent "database" in scope for v1, or is an in-memory/JSON lexicon enough?

---

## 4. New modules + tests (named; **not built this turn**)

**Modules**

| Module | One-line purpose |
|---|---|
| `holding.py` | Exact-Fraction core carrier: the `Holding` value type + closed productions (`+ − · conj rev M ν Φ`). |
| `readings.py` | The semantics as a clean importable API (tr/det/disc/obs/q/pt/s2/rank/TYPE/MASS/ε/spectrum). |
| `lexicon.py` | The enumerable vocabulary (BASIS/CONSTANTS/NODES/LAWS) as queryable data with stable IDs. |
| `bridge_loom.py` | The read-only one-way loom bridge (degree-2 minpoly↔holding, φ keystone, generalized 3-route check). **The only module that imports loom.** |
| `language_api.py` | JSON-in/out py-shell dispatch (mirror `vector_api.main`) — the KIRA wiring entrypoint. |
| `language_store.py` | *(if DB)* persistence + stable IDs + sha256 hash-chain (mirror `vector_substrate_store`). |

**Tests**

| Test | Pins |
|---|---|
| `test_holding.py` | Exact algebra: closure, identities, associativity, CH / det-mult / det(M)=det² at **zero tolerance** (Fraction). |
| `test_readings.py` | Each reading's value on the lexicon == KL_DTA's; load-bearing identities exact. |
| `test_lexicon.py` | Vocabulary enumerable; names/IDs unique + stable; TYPE/MASS correct per entry. |
| `test_language_api.py` | Local equivalence: in-process `dispatch(req)` == subprocess JSON (mirror `test_vector_api`). |
| `test_bridge_loom.py` | Generalized 3-route conformance over all degree-2 catalog seeds (extends `test_kl_dta_conformance.py`). |
| `test_KL_DTA.py`, `test_kl_dta_conformance.py` | **Kept as-is — the 25/25 regression pins must stay green throughout.** |

**Concrete improvements to `KL_DTA.py` "as-is" (later turns; no behavior change)**
- Extract the value type + readings into `holding.py` / `readings.py`; have `KL_DTA.py` *import*
  them, so the 2,890-line file becomes the **narrative + `verify_all` harness over the clean API**
  (a faithful representation — behavior byte-identical, 25 tests green throughout).
- Keep `run()` / `render_results()` as the **print harness**; the importable API and the JSON
  **dispatch entrypoint live in the new modules, distinct from the print harness** (so `import`
  gives you the language, not a 319-line verdict).

---

## 5. First buildable increment (smallest, verifiable)

**Increment 1 — `language_api.py` (read-only JSON dispatch) + `test_language_api.py`.**

> **REVISED by §7** — the semantic-kernel candidate already ships the dictionary (`LAW_BANK`),
> the firewall (`jurisdiction`), the data layer (`Row`/`dataset`), search/paragraph, sha256
> digests (stable IDs), and an `audit()` closure gate. So the cheapest first increment is no
> longer "build a dispatch over the original's readings" but **"wrap the kernel's existing
> audit/search/LAW_BANK behind `language_api` + add `bridge_loom.py` (φ keystone)"** — see §7.5.

- **Why this first:** it is the highest-signal "wire language through KIRA" artifact, it is small
  (a dispatch dict + `main()` + ~5 payload wrappers over KL_DTA's *existing* readings), and it is
  **decision-independent**: it reuses KL_DTA as-is (float is fine for a read-only compute surface,
  with a declared tolerance, exactly as `vector_api.residual_field` is float), needs **no**
  exactness reimplementation, **no** loom bridge, and **no** change to KL_DTA's behavior.
- **Endpoints v0:** `read`, `type`, `witness`, `product`/`fold`, `lexicon` (the `bridge` endpoint
  is deliberately deferred to Increment 2, since it needs `bridge_loom.py`).
- **Verified by:** in-process `dispatch(req)` == subprocess JSON (local equivalence), and the
  existing **25/25 stay green**.
- **Payoff:** stands up the exact KIRA wiring *shape* (a mirror of `vector_api`) at near-zero risk;
  every later piece (exact core, loom bridge, store) layers onto a proven surface.

**Then, in order (each gated by the review leash):**
1. `bridge_loom.py` + `test_bridge_loom.py` + add the `bridge` endpoint — the generalized
   degree-2 conformance, the one-way bridge made first-class.
2. `holding.py` / `readings.py` + their exact tests — *gated on decision (d)*; swap the dispatch's
   underlying readings float→Fraction (API surface unchanged).
3. `lexicon.py` + `test_lexicon.py` — the queryable vocabulary, IDs.
4. `language_store.py` — *gated on the §3 persistence decision*.
5. Refactor `KL_DTA.py` to import the extracted core (no behavior change; 25 stay green).

---

## 6. Guardrails (must hold every turn)

- **Disjoint, one-way:** kira-language may read/bridge to loom; **L00M never imports KL_DTA /
  kira-language.** The bridge lives only in `bridge_loom.py` / `conftest.py`.
- **Two-route closure ethos preserved** (cocycle vs matrix; loom = third, exact route).
- **Exact-vs-asserted firewall:** algebra = wired content; ToE/physics = commentary, never wired
  as proven (enforced at the JSON boundary, §2b).
- **The 25/25 copied tests stay green** as the regression floor, untouched, every increment.
- **Review leash:** claim → build → gate (tests green) → REPORT → HOLD; build proceeds only on
  Ace's go.

---

## 7. External candidates — verified & cross-reviewed (2026-06-23)

Two external files (`candidates/`, marked unrewired) were brought in, **run, and independently
math-checked** (not docstring-trusted). They are directly on-point for the language/dictionary layer.

### 7.1 `recursive_return_nlp.py` — the acquisition loop (VERIFIED)

A self-contained M₂(ℝ) demo: tokens flow by gradient descent to residual 0 (`ker(L)`); equal
residues collapse to one learned dictionary value. Run + **independent** checks:

| Claim | Verified | How (independent of docstring) |
|---|---|---|
| `R=(P+Pᵀ)/2 = [[0,1],[1,1]]`, charpoly `x²−x−1` | ✓ | by hand + run = the **φ companion** (= `loom.companion([1,-1,-1])`, confirmed equal) |
| `R²=R+I`, `N²=−I`, `{R,N}=N` ⟹ `L(N)=0`, `N∈ker(L)` | ✓ | hand-computed each product; run confirms |
| `dim ker(L) = 2` | ✓ | Sylvester eigenvalues `λᵢ+λⱼ−1`; zero at `φ+ψ−1=0` (double); run shows dim 2 |
| residual ‖ν‖→0, `M(M)=M` every token | ✓ | run: 3.9e-17 / 1.1e-16 / 0.0 / 1.3e-16 |
| 4 tokens → 2 values; cos +1/+1/−0.99/+1 | ✓ | run reproduces exactly |
| grad flow `X←X−η·LᵀL·X` lands in `ker(L)` | ✓ | `ker(LᵀL)=ker(L)`; PSD descent kills nonzero-eigval components; the 2-dim μ=0 space is untouched |

**Fragility flagged (as Ace predicted):** `Lmat = I⊗R + Rᵀ⊗I − I4` is the *column-major* Sylvester
identity, applied with **row-major** `reshape`. It is correct **only because R is symmetric** (then
`I⊗R+R⊗I` is reshape-order-agnostic). R is always symmetric by construction (`(P+Pᵀ)/2`), so it is
correct today — but swapping in a non-symmetric operator (or raw `P`, or `N`) would make `Lmat`
silently wrong. Latent, not active. *Also:* the file **runs on import** (no `__main__` guard) — not
import-safe as a module; would need a guard to wire.

### 7.2 `KL_DTA__Vsemantic_kernel.py` — the dictionary/firewall (VERIFIED)

Same carrier; adds a trace-zero residual `R_K`, a jurisdiction-tagged `LAW_BANK`, a data/row layer,
search/paragraph, sha256 digests, and an `audit()` gate. Run (`--mode audit`) → `closure: true`.

| Claim | Verified | How (independent) |
|---|---|---|
| `audit closure==True` | ✓ | run; all residuals below 1e-10 |
| symmetry / PSD-min / prob-sum / mass-τ / anisotropy | ✓ | 7.1e-15 / −7.6e-17 / 2.2e-16 / 7.1e-15 / 3.3e-16 |
| **`R_K²=0`** (residual_nilpotence) | ✓ | run 9.6e-14 **and proved**: `R_K(X)`=trace-free symmetric; for trace-zero 2×2, CH ⟹ `Y²=−det(Y)·I` (scalar) ⟹ second `R_K`=0 |
| `τ(R_K(X))=0` | ✓ | `R_K` is the trace-free part ⟹ scalar coord 0 (by construction) |
| `P0 spectrum {0,0,1,2}` | ✓ | run + hand: `dM(P0)` splits into `[[1,1],[1,1]]`→{2,0} and `[[1,−1],[0,0]]`→{1,0} |
| `Σλ(M(X))=2τ(M(X))`, `|p₂−p₁|=‖R_K‖_spec/τ` | ✓ | trace identity; trace-free part has eigenvalues ±½·gap |
| empty statement slots / gate failures | ✓ | run: `[]` / `0`; `gate_trace_seen=[0,0.5,1]` = rank/2 |

**Jurisdiction-tag audit (decision (b), already built).** All 25 candidate `LAW_BANK` entries inspected via
`--mode laws`: **20 THEOREM, 5 COMPUTED** (`word, statement, data_row, semantic_compression,
paragraph_circuit`) — matching "math=THEOREM, word/statement/data/compression=COMPUTED". No
INTERPRETIVE / FALSE_AS_STATED entries: the kernel **dropped the entire ToE narrative** and banked
only defensible statements. *(Shipped update: the first flag below was acted on — the shipped
`kira_language` kernel adds 2 INTERPRETIVE gloss companions, so its `LAW_BANK` is now **27**
= 20 THEOREM / 5 COMPUTED / 2 INTERPRETIVE.)* Two flags for Ace:
- **`observer` & `framework`** (both THEOREM): the *equations* are exact (definitional aliases of
  `R_K`), but the *glosses* ("observer is residual / not external spectator", "framework is residual
  ledger / not a wrapper") are **interpretive prose riding a THEOREM tag** — the one porous spot.
  Recommend: keep the equation THEOREM, demote the gloss to an INTERPRETIVE companion. (Also note
  `residual`/`observer`/`framework` are three names for the same operator `R_K` — relabeling by design.)
- **`orbit_regimes`** `λ(Mⁿ(X))=λ(M(X))^(2ⁿ)`: exponent is **convention-ambiguous** — correct if `n`
  counts folds *of the record M(X)*, off-by-one under literal `Mⁿ(X)` (should be `2^(n−1)`).
  Qualitative trichotomy (collapse/gate/diverge) is right; not numerically tested by `audit`. Disambiguate.

**Portability:** the kernel prints Unicode with **no cp1252 guard** — crashes on a legacy Windows
console unless `PYTHONUTF8=1`. The original `KL_DTA.py` has `_AsciiSafeStdout`; the kernel needs it.

### 7.3 Cross-review — dictionary / semantics / maths validity

- **Same carrier, exactly.** Kernel mul/mat == original KL_DTA mul/mat: `max|Δ| = 0.0` over 3000
  random trials. Same `mat`/`cl`(=`unmat`) convention, same cocycle product (e₁²=e₂²=1, i²=−1). The
  two KL_DTA variants are the **same algebra**.
- **Two residuals, reconciled (compatible, complementary — not in conflict):**
  - original **`ν(X)=M(X)−X`**: zero ⟺ symmetric **idempotent** (gate/projector). "Is X a projector?"
  - kernel **`R_K(X)=M(X)−τ(M(X))·1`**: zero ⟺ `M(X)` scalar ⟺ X is scalar×orthogonal (conformal);
    the **trace-free Gram** = the leftover direction. `R_K²=0` (bite-depth 2). "What direction/
    information-imbalance is left?" (= the anisotropy reading `|p₂−p₁|`).
  - recursive_return **`L(X)=RX+XR−X`**: zero ⟺ `X∈ker(L)` (the 2-dim φ-slack = the **lexicon**).
  - All three are "an M-derived residual → 0 = commit/rest." Recommend exposing **both ν and R_K**
    as distinct readings (idempotence-defect vs Gram-anisotropy) — they answer different questions.
- **Maps onto our framework.** recursive_return's loop (residual→0 = commit; `ker(L)`=lexicon;
  generalize by return-to-zero; sign=discriminator) is the **same shape as the `ResidualLearner`
  capture loop** (`r=x−Px=0` = captured; basis = lexicon) and the scoping's "ν=0 = synonymy/rest."
  The kernel's `R_K` + readings (entropy/purity/anisotropy/regime) are the **"readings as semantics"**
  layer, with the firewall built in. The dictionary mechanism is **sound** and **coheres** with
  KL_DTA's M/ν/residual readings (it literally uses `M(M)=M` idempotence as its on-shell check).
- **φ keystone unifies all three (confirmed, the natural bridge anchor):** recursive_return's `R`,
  KL_DTA's keystone `Cl(0.5,1,−0.5,0)`, and `loom.CATALOG_SEEDS["phi"]=[1,−1,−1]` are the **same
  object** (verified equal). This is where the 3-route conformance already lands.

### 7.4 "Rewiring for our intents" assessment

| Convention | recursive_return | semantic kernel |
|---|---|---|
| Exact-Fraction vs float | intrinsically float (gradient/SVD) | rational core; float only for spectral readings (→ quarantined-float layer) |
| Disjoint one-way (no loom import) | ✓ (constructs R directly; bridge test should assert `R==companion([1,-1,-1])`) | ✓ (no loom; add `bridge_loom.py`) |
| Firewall | ✗ — interpretive "NLP/meaning/speak" framing needs tagging | ✓ **built** (`Stmt.jurisdiction`) |
| Import-safe | ✗ runs on import (needs `__main__` guard) | ✓ guarded |
| cp1252 portability | ✓ ASCII-only output | ✗ needs `_AsciiSafeStdout` |
| loom bridge | add via `bridge_loom.py` | add via `bridge_loom.py` |

### 7.5 Verdict + revised base & first increment

- **Base recommendation:** make `KL_DTA__Vsemantic_kernel.py` the **base for the language
  database** (it already ships the dictionary + firewall + data-layer + audit + digests + a clean
  frozen carrier). Keep the original `KL_DTA.py` as the **reference verifier + conformance spine**
  (full two-route closure, the proven algebra, the keystone bridge). Treat `recursive_return_nlp.py`
  as the **acquisition-loop reference** (how new lexicon entries are learned) — parallel to
  `ResidualLearner`. → **Needs Ace's call.**
- **Revised first increment (cheaper than the original §5 plan):** **wrap the semantic kernel's
  existing `audit()` / `search()` / `LAW_BANK` behind `language_api.py` (JSON-in/out, mirror
  `vector_api`) + add `bridge_loom.py` confirming the φ keystone (`R == loom.companion([1,-1,-1])`).**
  Verifiable by: in-process `dispatch(req)` == subprocess JSON; `audit closure==True` surfaced over
  JSON; keystone residual 0. Reuses the already-built firewall + dictionary; adds only the dispatch
  shell + the one-way loom bridge. Defers the exact-core (decision d) and the import-safety/cp1252
  rewiring as small follow-ups. **No candidate behavior modified; the 25/25 stay green.**

---

## Decisions awaiting Ace (summary)

| # | Decision | Recommendation |
|---|---|---|
| a | language = ops / catalog / composition? | **Composition** (grammar=ops, lexicon extensible by catalog) |
| b | narrative firewall mechanism | **Already BUILT** in the semantic kernel (`Stmt.jurisdiction`); ratify + fix 2 glosses (§7.2) |
| c | degree-2 v1, or generalize now? | **Degree-2 v1 with a generalization seam** |
| d | exact-Fraction core, or bounded float? | **Exact core + quarantined float**; both candidates float today (§7.4) |
| **e** | **base = original KL_DTA or semantic kernel?** | **Semantic kernel = database base**; original = verifier spine; recursive_return = acquisition loop |
| **f** | **adopt recursive_return as the acquisition loop?** | Yes, after rewiring (main-guard, exact/float story, firewall its prose) — mirrors `ResidualLearner` |
| — | persistent "database" in v1 scope? | Kernel already has digests (stable IDs) + rows; in-memory/JSON likely enough for v1 |
| — | vendor loom, or sys.path bridge? | **sys.path bridge (in place)**; vendor only if isolated CI needs it |
| — | git-init kira-language as its own repo? | Surface — not done this turn (setup only) |
