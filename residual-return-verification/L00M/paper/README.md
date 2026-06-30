# `L00M/paper/` — the two papers + their `.tex` + the companion probes

The committed paper artifacts and the **probes that re-derive every displayed number from scratch**.
The shared discipline of both papers is that *every displayed number is reproduced by a
machine-checked probe* — this directory is where two of the three independent witnesses live (the
third, `test_paper_claims.py`, sits in [`../training/`](../training/README.md) alongside the engine
it deliberately does **not** import).

---

## 1. The papers

| Artifact | Title | Pages |
|---|---|---|
| [`vector_substrate.pdf`](vector_substrate.pdf) · [`.tex`](vector_substrate.tex) | *The Vector Substrate: Number Fields as Exact Learning Geometry* | 29 pp |
| [`residual_return_learning.pdf`](residual_return_learning.pdf) · [`.tex`](residual_return_learning.tex) | *Residual Return: Exact Learning Dynamics and Language over the Vector Substrate* | 30 pp |

The PDFs are the **committed artifacts**; the `.tex` sources ship beside them so the prose itself is
auditable. Both are also mirrored on the live
[GitHub Pages site](https://echo-s-studios.github.io/math-research-pipelines/) at
`/papers/vector_substrate.pdf` and `/papers/residual_return_learning.pdf`.

---

## 2. The companion probes — they import **no engine**

Each probe re-derives the papers' figures from **definitions**, with `sympy` (exact) + stdlib +
`mpmath` (rigorous interval enclosures) only. Importing no learner / `loom` / language engine is the
whole point: if a probe and the engine ever disagreed, you would see it (Part A is independent of
Part C). Two of them assert their own purity as a test.

| Probe | Where | What it pins | Engine? |
|---|---|---|---|
| [`test_residual_return_claims.py`](test_residual_return_claims.py) | here (`paper/`) | **20** checks: the *companion* paper. Power-basis Gram of `Q(√2+√3)`; residual norms 96/56/10; seed minpolys; the invariant-factor / Jordan witnesses (charpoly insufficient); the **non-disjoint degree-4 witness** (`m_θ = x⁴−22x²+25`, `β = −7/20·θ + 1/20·θ³`); Fisher matrices and `G = n·Fisher` **on the trace-zero subspace** (and the full-matrix gap at the constant direction); the witness digest `31f1f1e05ac9a35a`; certified-grow enclosures (`mpmath.iv`); the Smyth/degree-aware floors; the `λ = 2c` closure (Thm 4.6); and the Cl(2,0) return operator (`ker L` dim 2, the commit projector, sign-word antipodes). `test_probe_imports_no_engine` statically asserts the source imports no engine. | no |
| [`residual_return_audit.py`](residual_return_audit.py) | here (`paper/`) | **The third witness** — a from-scratch audit harness by a *different author*, run as a bare script (not pytest). It re-derives the same numbers a second, independent way and raises **exactly one** intentional flag, labelled `shorthand`: it documents that the Fisher identity `I_exp = (1/n)·G` holds on the **trace-zero subspace**, not as a full-matrix identity (the two differ at the constant direction, where `I_exp` vanishes). The paper states this scope explicitly and the companion probe pins *both* directions — so the flag is documentation, not a defect. | no |
| [`../training/test_paper_claims.py`](../training/test_paper_claims.py) | `training/` | **13** checks: the *substrate* paper. `det(trace Gram) = d_K` (or `index²·d_K`); the Jeffreys/Minkowski volume `√|d_K|`; the different-and-discriminant identity; spectral diagonalisation `M·ρ(x)·M⁻¹ = diag(σ_k)`; Mahler as a spectral invariant; the certified-interval grow threshold; lattice-aligned noise stopped by the Smyth floor; and the figure data (`Q(√5)` projection 5/3, plastic/Lehmer constants). It lives next to the engine precisely to prove it imports none of it (`test_paper_claims_model_layer_no_kira`). | no |

These three are **Part A** of the pipeline (`verify.py --quick` runs all of them, ~2 s): they
recompute every Gram, residual norm, minimal polynomial, Fisher matrix, floor, certified-interval
enclosure, kernel, projector matrix, and hash digest displayed in the papers, with independent code.

---

## 3. How they fit the pipeline

```
verify.py --quick   ->  the three probes only (Part A: re-derive every displayed NUMBER)
verify.py --walk    ->  + the 55-claim walkthrough (Part B: each claim -> its test -> PASS/FAIL)
verify.py           ->  + the full engine suites (Part C: training 137 + kira-language 121)
```

See the [package README](../README.md) for the full pipeline and the
[`claim_map.json`](../claim_map.json) walkthrough data (each claim → its pytest node → commit hash).
The probe page counts and provenance are recorded in [`../MANIFEST.txt`](../MANIFEST.txt).
