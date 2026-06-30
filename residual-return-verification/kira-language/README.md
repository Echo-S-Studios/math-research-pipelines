# `kira-language/` — the residual-valued language layer

The language layer of the residual-return work: a small, complete language whose **meaning is
residual-valued** — a holding *means* the tuple of its readings, two holdings are *synonymous* iff a
residual vanishes (`ν = 0`, decided exactly), and a holding's *type* is which laws vanish on it. It
is built over the Clifford algebra **Cl(2,0) ≅ M₂(ℝ)** carrier, with a **return operator** whose
kernel is the "phi-slack" where learned words live, a growing **lexicon**, a tamper-evident
**store**, and a KIRA-shell **dispatch** surface.

> **A SIBLING of `L00M`, not a child.** This tree is disjoint from
> [`../L00M`](../L00M/README.md) and reaches it only across a **one-way** bridge:
>
> ```
> kira-language  ──reads──▶  loom            (the φ-keystone bridge; ALLOWED, read-only)
> L00M           ──imports─▶  kira-language   (NEVER)
> ```
>
> The bridge resolves `loom` via `KIRA_LANG_L00M_ROOT` (set by `verify.py` to the bundled `L00M`),
> else the sibling `../L00M`. `L00M` never learns this project exists; nothing reaches back in.

The full engine suite is **121 passed**; it is **Part C** of the package pipeline
(`verify.py` sets `KIRA_LANG_L00M_ROOT` and runs it). The exact decision core is **pure-stdlib
`fractions`** — numpy is pulled in only by the *quarantined float readings* (`semantic_kernel`,
`KL_DTA`), never by an exact decision.

---

## 1. Layout

```
kira-language/
  KL_DTA.py                the reference verifier + conformance spine (the two-route closure)
  conftest.py              the pytest one-way loom shim (appends ../L00M to sys.path)
  kira_language/           the shipped, layered package (carrier -> bridge -> dispatch)
  candidates/              UNREWIRED external sources (review-only; see candidates/README.md)
  SCOPING.md               the scope/roadmap + the §7 external-candidate review
  B1_READINESS.md          the readiness gate for the live KIRA wire (the §3 checklist)
  test_*.py                the 121-test suite (inventory below)
```

The shipped package lives in [`kira_language/`](kira_language/README.md) — see that directory's
README for the module-by-module map (the Cl(2,0) carrier, the return operator, the lexicon, the
store, dispatch). This README is the layer overview.

---

## 2. `KL_DTA.py` — the two-route closure

[`KL_DTA.py`](KL_DTA.py) is the **reference verifier and conformance spine** (~2,890 lines). Its
load-bearing content:

- **The carrier `Cl`** — a holding `X = a·𝟙 + b·e₁ + c·e₂ + d·i` in Cl(2,0) ≅ M₂(ℝ), basis
  `{𝟙, e₁, e₂, i}` (bits 00/01/10/11), with the geometric product driven by a precomputed cocycle
  table (`_MUL_TABLE`: `target = i⊕j`, `sign = (−1)^(bit1(i)·bit0(j))` — the single bit-product that
  *is* the noncommutativity). `__add__` = the fold, `__mul__` = the geometric product, `__eq__` = the
  witness (`residual < _tol`).
- **The readings unfolded from the product** — `tr`, `conj`, `det`, `rev`, the Gram/measurement
  `M(X) = X̄X`, the idempotence-defect `ν(X) = M(X) − X`, `disc`, `rank`, and the seed equation
  `Φ_X(Y) = Y² − tr(X)·Y + det(X)·𝟙` (Cayley–Hamilton, `Φ_X(X) = ∅`).
- **The type lattice** — `LAWS = {idem, rest, metric, flow, gen}`; a holding's `TYPE` is which of
  these vanish, its `MASS` is how many.
- **The two-route closure** — every operator identity is checked **two independent ways** (the
  cocycle/carrier route via `Cl` vs the matrix route via `mat`/`unmat` to numpy `M₂(ℝ)`), residual 0;
  `loom` adds a third, exact route at the φ keystone. The `symbolic_verify_*` functions give exact
  `sympy` proofs of Cayley–Hamilton, the golden law, the cocycle, and `det(X) = a²−b²−c²+d²`.

`KL_DTA.py` is **float** today (its decisions go through `math.isclose`); the **exact-Fraction core**
that may wire live into `L00M` is `kira_language/holding.py` (decision (d) — see `SCOPING.md` §2(d)).

---

## 3. The test suite (121)

| File | Tests | Pins |
|---|---|---|
| `test_KL_DTA.py` | 9 | the verifier spine (unchanged) |
| `test_kl_dta_conformance.py` | 16 | the 3-route closure incl. the **exact loom route** (the one test, besides `loom_bridge`, that imports `loom` read-only) |
| `test_holding.py` | 8 | the exact-Fraction core, **zero tolerance** |
| `test_bridge_loom.py` | 2 | the one-way φ keystone vs **live** loom |
| `test_language_api.py` | 13 | dispatch local-equivalence + firewall (the original read-only surface) |
| `test_acquisition.py` | 17 | exact `ker(L)`, the projector, the word, generalization by return-to-zero |
| `test_lexicon.py` | 12 | the growing dictionary, exact dedup, deterministic ids |
| `test_store.py` | 12 | exact persistence, the sha256 chain, tamper-evidence |
| `test_dispatch_full.py` | 22 | the full 13-verb surface, robustness, fact-only render |
| `test_b1_readiness.py` | 10 | the §3 readiness checklist (the wire gate) |

Reproduce with `KIRA_LANG_L00M_ROOT=<abs path to ../L00M> py -m pytest -q` (→ `121 passed`), or just
`py verify.py` from the package root, which sets the env var for you.

---

## 4. Posture, in brief

- **Exact (G8) where it matters** — the `holding` carrier and the whole acquisition/lexicon/store
  path are pure-stdlib `fractions`; membership, idempotence, `ker(L)` and dedup are decided with `==`
  on `Fraction`, zero tolerance. Float lives only in `semantic_kernel`/`KL_DTA` spectral readings,
  behind declared tolerances, and never crosses into an `L00M` exact decision.
- **Firewall (decision b)** — only `WIRED_JURISDICTIONS = (THEOREM, COMPUTED)` cross the wire as
  fact; `INTERPRETIVE`/`FALSE_AS_STATED` rows are recorded and tagged but never wired.
- **One-way + import-safe** — only `loom_bridge` (and the read-only conformance test) imports `loom`;
  `import kira_language` does no I/O and pulls no numpy.

---

## 5. Pointers (read these rather than re-deriving them here)

- **[`SCOPING.md`](SCOPING.md)** — what the project is, the one-way invariant, the seven key
  decisions (a–f), the wiring path, and **§7**: the verified, cross-reviewed assessment of the two
  external `candidates/` (which became `acquisition.py` and the `semantic_kernel` base).
- **[`B1_READINESS.md`](B1_READINESS.md)** — the readiness gate for **B1** (the live KIRA
  `/api/language/*` wire): the §3 checklist of 10 invariants, each codified as an executable
  assertion in `test_b1_readiness.py`, plus the increment-by-increment build provenance.
- **[`candidates/README.md`](candidates/README.md)** — the two unrewired external sources kept
  verbatim as review candidates.
- **[`kira_language/README.md`](kira_language/README.md)** — the package module map.

This layer is part of the [residual-return package](../README.md), which walks both papers
claim-by-claim via `verify.py`, and of the wider
[math-research-pipelines](../../README.md) repo / its live
[GitHub Pages site](https://echo-s-studios.github.io/math-research-pipelines/).
