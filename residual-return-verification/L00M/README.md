# `L00M/` — the L0 exact core (number-field learning geometry)

`L00M` is the **engine root** of this package: the exact vector substrate the two papers describe,
the `training/` learner built on it, and the `paper/` artifacts + companion probes. This directory's
own three modules are the **L0 exact core** — the smallest layer everything else stands on.

> **Float-free by construction.** The exact core (`integral_basis`, `projector`, `loom`'s integer
> invariants, and the entire `holding` carrier over in
> [`../kira-language`](../kira-language/README.md)) is **pure-stdlib `fractions`** — `Fraction`/`int`
> at every decision boundary. The only floats are clearly-labelled *display charts* (Minkowski
> embeddings, Durand–Kerner eigenvalues, Mahler measure): they never feed a membership or growth
> decision (the substrate's **G8** discipline, Principle 5.12).

---

## 1. The three L0 modules

| File | Role |
|---|---|
| [`integral_basis.py`](integral_basis.py) | **The coordinate object + the trace-form metric.** A number field `K = Q[x]/(min_poly)` is realized as a ℚ-vector space on the power basis `{1, θ, …, θ^(d-1)}`. `gram_trace_form(ib)` builds the Gram `G[i][j] = Tr_{K/Q}(b_i·b_j)` **exactly** from conjugate power sums via **Newton's identities** — never by summing Durand–Kerner roots (G8). Also: `conjugate_power_sums`, `mult_in_power_basis`, `field_trace`, `trace_form_inner/norm/pairing`, and `_guard_int_monic` (the algebraic-integer-seed guard, G10). `embed_minkowski` is the one **float display chart** (evaluate an element at the Galois conjugates) and is explicitly never used in a decision. |
| [`projector.py`](projector.py) | **The orthogonal projector + the exact residual.** `projector_matrix(B, G)` = `B (BᵀGB)⁻¹ BᵀG`, the `G`-orthogonal projector onto `col(B)`; `residual(x, P) = x − Px`; `residual_norm(x, P, G) = ⟨r,r⟩_G` — **zero IFF `x` is captured by the forced subspace**, decided exactly over ℚ/ℤ. `gram_inverse` is the exact rational Gauss–Jordan inverse (and also serves `IntegralBasis.I2P`); a rank-deficient `B` returns the `NO_PROJECTION` sentinel rather than a float blow-up. |
| [`loom.py`](loom.py) | **The matrix-invariant kernel.** `charpoly` (Faddeev–LeVerrier, exact `Fraction`→`int` with an integer-matrix guard), `minpoly_faddeev_leverrier` (rational Krylov dependence detection), `companion`, the weave closure `weave = companion ∘ charpoly` (and `weave_n` to verify idempotence), and `classify` (the full invariant bundle: trace, det, charpoly, minpoly, mahler, derogatory, unimodular). The `M = 1` Mahler floor is decided **exactly** over ℤ[x] by Kronecker's criterion (cyclotomic-product test), immune to the Durand–Kerner float smear. `eigenvalues`/`mahler_measure` are the **float display layer** (one shared Durand–Kerner kernel). This is the same `loom` the language layer reaches read-only across the [φ-keystone bridge](../kira-language/README.md). |

The integer-matrix guards in `loom.charpoly`/`minpoly` are deliberate: integer invariants are
ground truth, so a non-integer coefficient **raises** rather than silently `int()`-truncating to a
wrong-but-plausible answer.

---

## 2. What builds on the L0 core

```
L00M/
  integral_basis.py  projector.py  loom.py        <- the L0 exact core (this directory)
  training/          the learner, cross-field bridge, capacity gate, anomaly detector + tests
  paper/             the two PDFs + .tex sources + the companion probes (import NO engine)
```

- **[`training/`](training/README.md)** — the lightweight, fully-local learner. It **reuses** the L0
  core rather than reinventing it: `residual_learner.py` imports `integral_basis.gram_trace_form`,
  `projector.projector_matrix`, `projector.residual`, `projector.residual_norm`, and the seed guard
  directly (see its module header). "Capture" (`r = x − Px == 0`) is the substrate's word for
  *learned*; persistent off-axis residual is *novelty*; under a principled, Northcott-finite capacity
  gate, novelty becomes a new exact basis direction (in-field) or a new exact field extension
  (cross-field). Full engine suite: **137** tests.
- **The language layer** — over in [`../kira-language`](../kira-language/README.md), a **sibling** tree
  (not a subdirectory), reached only through the one-way `loom_bridge` (`KIRA_LANG_L00M_ROOT` →
  this `L00M`). It reads `loom` read-only at the **φ keystone** (the void law `x²=x+1` →
  `loom.companion([1,-1,-1]) = [[0,1],[1,1]]`, Mahler = φ). `L00M` never imports the language layer.
- **[`paper/`](paper/README.md)** — the committed PDFs (`vector_substrate.pdf` 29pp,
  `residual_return_learning.pdf` 30pp), their `.tex` sources, and the three companion probes that
  re-derive every displayed number from scratch (importing **no** engine).

---

## 3. Running it

The L0 modules are libraries; the two entry-point demos are:

```sh
py L00M/loom.py             # the golden seed x^2 - x - 1: companion, charpoly, minpoly, invariants
py L00M/training/demo.py    # the end-to-end learner story (in-field grow -> off-field extend -> anomaly)
```

`loom.py`'s `__main__` weaves the golden seed `[1, -1, -1]` and prints its invariant bundle
(`trace=1 det=-1 mahler≈1.618 derogatory=False unimodular=True`). For the whole package — both
papers walked claim-by-claim against these modules — run `py verify.py` from the package root (see
the [top-level README](../README.md)). Part C runs the real `training` engine (137) and the
`kira-language` engine (121) against the actual code, not just the standalone probes.

---

## 4. Provenance

The L0 modules are pinned at L00M HEAD `f238d6b`; per-file commit hashes and suite counts are in
[`../MANIFEST.txt`](../MANIFEST.txt), and per-file digests in [`../SHA256SUMS`](../SHA256SUMS). These
papers are part of the wider [math-research-pipelines](../../README.md) repo and its live
[GitHub Pages site](https://echo-s-studios.github.io/math-research-pipelines/) (both PDFs are mirrored
at `/papers/vector_substrate.pdf` and `/papers/residual_return_learning.pdf`).
