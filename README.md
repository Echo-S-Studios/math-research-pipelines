# math-research-pipelines

Three machine-verified, exact-arithmetic mathematics pipelines. Each one re-derives every
load-bearing claim of its companion paper(s) in exact arithmetic — exact rationals and integers
at every decision boundary, so **no float ever crosses a decision boundary**. Each claim is
graded by epistemic status and pinned to a named, runnable test; you can reproduce every number
yourself rather than trust a rendered PDF.

[![matrix-plates CI](https://github.com/Echo-S-Studios/math-research-pipelines/actions/workflows/matrix-plates.yml/badge.svg)](https://github.com/Echo-S-Studios/math-research-pipelines/actions/workflows/matrix-plates.yml)
[![lambda2c CI](https://github.com/Echo-S-Studios/math-research-pipelines/actions/workflows/lambda2c.yml/badge.svg)](https://github.com/Echo-S-Studios/math-research-pipelines/actions/workflows/lambda2c.yml)
[![residual-return CI](https://github.com/Echo-S-Studios/math-research-pipelines/actions/workflows/residual-return.yml/badge.svg)](https://github.com/Echo-S-Studios/math-research-pipelines/actions/workflows/residual-return.yml)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

> The three top-level pipeline directories are the **canonical source of truth**.
> `Zipped-Tarred-Pipelines/` holds duplicate offline-distribution archives only.

---

## The three pipelines

| Pipeline | What it verifies | Approach | Tests | Run command |
|---|---|---|---|---|
| [**lambda2c-emissiongap-verification**](lambda2c-emissiongap-verification/README.md) | Every `[FORCED]` (and the few `[COMPUTED]`) claim of *The Exchange Rate λ = 2c* and *The Emission-Gap Theorem* — the identity λ = 2c, the three-gate ladder `{1/4, 1/2, 1} → {2, 3, 5}`, the Mahler floor `M ∈ {1} ∪ [φ, ∞)`, and the no-Salem closure | `sympy` + `fractions`, Sturm root-counting, Faddeev–LeVerrier; closure-not-enumeration plus an exhaustive 27-subfield check; `mpmath`/floats only for displayed magnitudes | **90 FORCED claims, all pass** (lambda_2c 41 · emission_gap 40 · 9 catalog constants; 0 failed) | `cd lambda2c-emissiongap-verification && pip install -r requirements.txt && pytest` |
| [**matrix-plates**](matrix-plates/README.md) | Exact integer-matrix invariants graded by Mahler measure, the `companion ∘ charpoly` closure, and the `φ ⊕ φ` derogatory / non-similar similarity witness | Stdlib-only exact ℤ/ℚ engine: Faddeev–LeVerrier char-poly, rational Krylov minimal polynomial, Smith normal form over `ℚ[x]` for invariant factors; cross-checked against committed JS, sympy, and determinantal-divisor oracles | **139 tests pass** (133 core + hypothesis property tests when the optional `hypothesis` package is installed) **plus a build-spec checklist 10/10** | `cd matrix-plates && pip install -e ".[dev]" && make test && make verify` |
| [**residual-return-verification**](residual-return-verification/README.md) | Every load-bearing claim of *The Vector Substrate* and *Residual Return* — Gram matrices, residual norms, minimal polynomials, Fisher matrices, floors, certified-interval enclosures, kernels, projectors, and hash digests — against three independent witnesses and the real engines | Exact-core `fractions` (no float in any decision), driven through `pytest`; a data-driven claim map pins each theorem/equation to a test node and a commit hash; `numpy` only for quarantined float readings | **`verify.py` ALL GREEN** — Part A probes 13 + 20 + a third witness 56/57 (the 1 flag is an intentional, documented "shorthand" note, not a failure); Part B walkthrough 55/55; Part C engines training 137 + kira-language 121 | `cd residual-return-verification && pip install -r requirements.txt && python3 verify.py` |

---

## What makes this rigorous

The three pipelines were built independently, but they share one discipline:

- **Exact arithmetic at every decision boundary.** Rationals and integers (`sympy`,
  `fractions`, in-browser `BigInt`) carry every quantity that a verdict depends on. The
  load-bearing primitives are exact by construction — **Sturm** root-counting and
  `Poly.count_roots` for signatures and Salem straddles, **Smith normal form over `ℚ[x]`** for
  invariant factors, **Faddeev–LeVerrier** and rational Krylov for characteristic and minimal
  polynomials. `mpmath` and floats appear only for displayed magnitudes and cross-checks —
  **no float crosses a decision boundary.**
- **Epistemic grading.** Claims are graded `[FORCED]` / `[COMPUTED]` (mathematical
  consequences) versus `[DECLARED]` / `[POSITED]` / `[OPEN]` (modelling choices). Only the
  forced claims are asserted as proofs; the declared and open ones are recorded as context, not
  smuggled in as results.
- **Closure, not enumeration.** Where the statement is universal — *no Salem number is emitted*,
  *the Mahler floor survives every operation* — the argument is an invariant preserved by every
  spectral operation, with a runtime certificate, rather than a finite sample. Where enumeration
  *is* used (the 27 subfields of `K`) it is genuinely exhaustive, and it corrects an
  overstatement rather than papering over one.
- **Committed oracles + pinned versions.** Independent ground truth ships in the repo: a
  verbatim JS run under Node, an independent `sympy` computation, determinantal-divisor oracles,
  a from-scratch third audit harness by a different author. Dependency versions are pinned and
  stamped into the result artifacts; a bit-exact `mulberry32` PRNG keeps the browser tool and
  the Python backend reproducible from the same seed tuple.
- **Every claim pinned to a named test.** Each paper claim maps to a specific test node (and, in
  residual-return, a commit hash). A dismissal therefore has to point at a concrete failing test,
  not at absent evidence — *a genuine failure is itself information.*

---

## Quickstart

Each pipeline is self-contained; run them independently.

**lambda2c-emissiongap-verification** — Python 3.12; 90 FORCED claims, ~59 s under pytest.

```bash
cd lambda2c-emissiongap-verification
pip install -r requirements.txt
pytest
# optional: python build_pdfs.py   # renders both papers to output/*.pdf (needs TeX Live)
```

**matrix-plates** — stdlib-only core; the `[dev]` extra adds the optional sympy/numpy/hypothesis bridge.

```bash
cd matrix-plates
pip install -e ".[dev]"
make test       # 133 core tests (+ hypothesis property tests when installed)
make verify     # the build-spec checklist (10/10)
# open web/matrix_plates.html in any browser for the interactive tool
```

**residual-return-verification** — Python 3.10+; a full green run drives both probes, the walkthrough, and both engine suites.

```bash
cd residual-return-verification
pip install -r requirements.txt
python3 verify.py            # everything (Parts A–C)
python3 verify.py --quick    # just the two probes — re-derive every number (~2 s)
```

---

## Interactive tool

[`matrix-plates/web/matrix_plates.html`](matrix-plates/web/matrix_plates.html) is a single
self-contained file — **no build, no network, no dependencies.** Open it in any browser to build
integer matrices graded by **Mahler measure**, run the `companion ∘ charpoly` closure, read the
**invariant factors**, **derogatory / defective** flags, and the **similarity verdict**, and
**export JSON / LaTeX / SymPy** — all computed in-browser in exact `BigInt` rational arithmetic,
at any matrix size via a fraction-free minimal polynomial. It mirrors the Python backend operator
algebra over the same seed registry, including a **bit-exact `mulberry32` PRNG**, so a
`(construction, seeds, params, RNG seed)` tuple reproduces the same matrix in both. See
[`matrix-plates/web/README.md`](matrix-plates/web/README.md).

---

## Papers

The companion papers ship alongside their verification suites, with `.tex` sources so the prose
is auditable:

- **lambda2c-emissiongap-verification**
  - [`papers/lambda_2c_paper.tex`](lambda2c-emissiongap-verification/papers/lambda_2c_paper.tex)
    — *The Exchange Rate λ = 2c: A Conformal Identity, Its Gate, and Its Flip*
  - [`papers/emission_gap_paper.tex`](lambda2c-emissiongap-verification/papers/emission_gap_paper.tex)
    — *The Emission-Gap Theorem*
  - Both render to `output/*.pdf` via `python build_pdfs.py` (needs TeX Live).
- **residual-return-verification**
  - [`L00M/paper/vector_substrate.pdf`](residual-return-verification/L00M/paper/vector_substrate.pdf)
    — *The Vector Substrate: Number Fields as Exact Learning Geometry* (29 pp)
  - [`L00M/paper/residual_return_learning.pdf`](residual-return-verification/L00M/paper/residual_return_learning.pdf)
    — *Residual Return: Exact Learning Dynamics and Language* (30 pp)
  - `.tex` sources for both ship beside the PDFs.
- **matrix-plates** has no companion paper; see
  [`docs/DESIGN.md`](matrix-plates/docs/DESIGN.md) for the metaphors and
  [`docs/matrix_plates_build_spec.md`](matrix-plates/docs/matrix_plates_build_spec.md) for the
  full spec.

---

## Repository layout

```
math-research-pipelines/
├── lambda2c-emissiongap-verification/   # λ = 2c & Emission-Gap: 90 FORCED claims under pytest
├── matrix-plates/                       # Mahler-measure plates + companion closure + browser tool
├── residual-return-verification/        # exact learning substrate: verify.py drives Parts A–C
└── Zipped-Tarred-Pipelines/             # duplicate offline-distribution archives (NOT canonical)
    ├── lambda2c-emissiongap-verification.zip
    ├── matrix-plates-1.1.2.tar
    └── residual-return-verification-v2.tar
```

The three pipeline directories are the **canonical source of truth**. The contents of
`Zipped-Tarred-Pipelines/` are convenience snapshots for offline distribution — do not edit them
or treat them as authoritative.

---

## License & citation

This repository is released under the **MIT License** — Copyright (c) 2026 Echo-S Studios — see
[`LICENSE`](LICENSE). The companion papers are included under the same MIT terms (these can be
swapped to **CC-BY** for the prose if preferred). To cite this work, see
[`CITATION.cff`](CITATION.cff).
