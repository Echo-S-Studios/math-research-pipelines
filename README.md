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
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21121863.svg)](https://doi.org/10.5281/zenodo.21121863)

**🌐 Live site — [echo-s-studios.github.io/math-research-pipelines](https://echo-s-studios.github.io/math-research-pipelines/)** ·
read every paper, open the interactive tools, and browse the build spec. Each card is described in
[**Live site (GitHub Pages)**](#live-site-github-pages) below.

> The three top-level pipeline directories and the `relational-charge-verification/` deposit are the
> **canonical source of truth**. `Zipped-Tarred-Pipelines/` holds duplicate offline-distribution archives only.

---

## Live site (GitHub Pages)

The project's public face is **[echo-s-studios.github.io/math-research-pipelines](https://echo-s-studios.github.io/math-research-pipelines/)**
— a single landing page that links every paper and tool. It is built by
[`.github/workflows/pages.yml`](.github/workflows/pages.yml) from [`site/index.html`](site/index.html)
and the [`papers/`](papers/) drop-zone: the two λ=2c papers are compiled from `.tex` in CI, the
residual-return PDFs and the interactive tools are copied in, and every Markdown doc is rendered to a
themed HTML page. Drop a new PDF, Markdown doc, or self-contained HTML tool into [`papers/`](papers/)
with one [`papers/catalog.json`](papers/catalog.json) entry and it publishes on the next deploy
(see [`papers/README.md`](papers/README.md)).

The landing page has three sections; here is every card it links, with the file behind it.

### The papers — the four pipeline companions

| Card | On the site | Behind it | What it is |
|---|---|---|---|
| **The Exchange Rate λ = 2c** | `/papers/lambda_2c_paper.pdf` | compiled in CI from [`lambda_2c_paper.tex`](lambda2c-emissiongap-verification/papers/lambda_2c_paper.tex) (24 pp) | The conformal identity λ = 2c, its gate ladder `{¼,½,1} → {2,3,5}`, and its flip — verified by the **lambda2c** suite. |
| **The Emission-Gap Theorem** | `/papers/emission_gap_paper.pdf` | compiled in CI from [`emission_gap_paper.tex`](lambda2c-emissiongap-verification/papers/emission_gap_paper.tex) (16 pp) | The integer-quadratic Mahler spectrum `{1} ∪ [φ,∞)` and the cost floor; a closure argument rules out an emitted Salem. |
| **The Vector Substrate** | `/papers/vector_substrate.pdf` | [`vector_substrate.pdf`](residual-return-verification/L00M/paper/vector_substrate.pdf) (29 pp) | Number fields as exact learning geometry — verified by the **residual-return** suite. |
| **Residual Return** | `/papers/residual_return_learning.pdf` | [`residual_return_learning.pdf`](residual-return-verification/L00M/paper/residual_return_learning.pdf) (30 pp) | Exact learning dynamics and language; capture ⟺ residual = 0. |

### Interactive — three in-browser tools

| Card | On the site | Behind it | What it is |
|---|---|---|---|
| **Matrix Plates explorer** | `/tool/` | [`matrix-plates/web/matrix_plates.html`](matrix-plates/web/matrix_plates.html) | Build integer matrices graded by Mahler measure, run the `companion ∘ charpoly` closure, read invariant factors / similarity verdicts, export JSON/LaTeX/SymPy — all in exact in-browser BigInt arithmetic. |
| **Lehmer's Box — closure instrument** | `/papers/lehmers_box_instrument.html` | [`papers/lehmers_box_instrument.html`](papers/lehmers_box_instrument.html) | A live closure instrument: plot roots, compose seeds with the spectral operators, watch emissions stay in the box, then throw a Salem number at it. Math computed in-browser. |
| **The Emission Algebra — a machine-verified account** | `/papers/emissionalgebracompendium.html` | [`papers/emissionalgebracompendium.html`](papers/emissionalgebracompendium.html) | A guided compendium of the whole stack — the confinement, the occupant, the generative emptiness, the generation rates, and the finitely generated Mahler-measure monoid. |

### Additional papers — the companion stack + a build spec

| Card | On the site | Behind it | What it is |
|---|---|---|---|
| **Lehmer's Box** | `/papers/lehmers_box.pdf` | [`papers/lehmers_box.tex`](papers/lehmers_box.tex) (14 pp, compiled in CI) | The golden floor and the angle lattice that confine emission away from Salem numbers — without resolving Lehmer's problem. |
| **The Occupant of the Salem Slot** | `/papers/salem_slot.pdf` | [`papers/salem_slot.pdf`](papers/salem_slot.pdf) (11 pp) | The positive content of the empty slot: the trace redirection, the grow channel, and the √5 limit at the floor. |
| **The Generative Content of a Conserved Emptiness** | `/papers/generative_emptiness.pdf` | [`papers/generative_emptiness.pdf`](papers/generative_emptiness.pdf) (7 pp) | Kinematic voids as superselection generators: the ℤ/4ℤ charge and the five objects it produces. |
| **The Operator Algebra of the Emission Semiring** | `/papers/operatoralgebrawhitepaper.pdf` | [`papers/operatoralgebrawhitepaper.pdf`](papers/operatoralgebrawhitepaper.pdf) (6 pp) | The spectral operators ⊕, ⊗, (·)² as a λ-ring with two characters (Mahler measure and the ℤ/4ℤ charge). |
| **The Charge–Measure Coupling** | `/papers/charge_measure_coupling.pdf` | [`papers/charge_measure_coupling.tex`](papers/charge_measure_coupling.tex) (13 pp, compiled in CI) | Two orthogonal characters on the spectral semiring (Mahler measure + a cyclic conjugate-angle charge), a parity-graded floor, and the matrix commutator as the one exit that re-admits the Salem spectrum. |
| **The ℤ/5ℤ Case of the No-Salem Dichotomy** | `/papers/z5_no_salem_dichotomy.pdf` | [`papers/z5_no_salem_dichotomy.tex`](papers/z5_no_salem_dichotomy.tex) (9 pp, compiled in CI) | The pentagon sector: four forced results sharpen the floor to μ_S = 1.3247, while the full μ(5) = 2 stays computed. |
| **Relational Charge on the Spectral Semiring** | `/papers/relational_charge_paper.pdf` | [`relational-charge-verification/`](relational-charge-verification/) (23 pp, sealed deposit + exact engines) | Refactors the charge into a reference-free relational invariant; a rigidity theorem (integrality fixes the gauge); exactly-decidable coherence types on the Salem sector (β₄, Lehmer, a 37-instance degree-12 census, all inert). |
| **Lehmer's Problem: An Introduction** | `/papers/lehmersproblemanintroduction.html` | rendered from [`papers/lehmersproblemanintroduction.md`](papers/lehmersproblemanintroduction.md) | A from-scratch primer on Lehmer's problem — the Mahler measure, Lehmer's number, and why the Salem case is the open heart. |
| **Building on the Emission Algebra — a build spec** | `/papers/EMISSIONALGEBRASPEC.html` | rendered from [`papers/EMISSIONALGEBRASPEC.md`](papers/EMISSIONALGEBRASPEC.md) | A build specification over the substrate, with every fact mapped to the file in this repo that checks it. |

---

## The three pipelines

| Pipeline | What it verifies | Approach | Tests | Run command |
|---|---|---|---|---|
| [**lambda2c-emissiongap-verification**](lambda2c-emissiongap-verification/README.md) | Every `[FORCED]` (and the few `[COMPUTED]`) claim of *The Exchange Rate λ = 2c* and *The Emission-Gap Theorem* — the identity λ = 2c, the three-gate ladder `{1/4, 1/2, 1} → {2, 3, 5}`, the Mahler floor `M ∈ {1} ∪ [φ, ∞)`, and the no-Salem closure | `sympy` + `fractions`, Sturm root-counting, Faddeev–LeVerrier; closure-not-enumeration plus an exhaustive 27-subfield check; `mpmath`/floats only for displayed magnitudes | **95 FORCED claims, all pass** (lambda_2c 41 · emission_gap 45 · 9 catalog constants; 0 failed) | `cd lambda2c-emissiongap-verification && pip install -r requirements.txt && pytest` |
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

**lambda2c-emissiongap-verification** — Python 3.12; 95 FORCED claims, ~62 s under pytest.

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
├── README.md  LICENSE  CITATION.cff  .zenodo.json  .gitignore   # repo root: this file + governance + Zenodo metadata
├── lambda2c-emissiongap-verification/   # λ = 2c & Emission-Gap: 95 FORCED claims under pytest
├── matrix-plates/                       # Mahler-measure plates + companion closure + browser tool
├── residual-return-verification/        # exact learning substrate: verify.py drives Parts A–C
├── relational-charge-verification/      # Relational Charge paper (sealed deposit PDF) + exact engines (sympy + PARI/GP)
├── papers/                              # Pages drop-zone: contributed PDFs / docs / HTML tools + catalog.json
├── site/                               # GitHub Pages source: the landing page (index.html, render_docs.py)
├── .github/                            # CI workflows (incl. Pages deploy) + community files
└── Zipped-Tarred-Pipelines/             # duplicate offline-distribution archives (NOT canonical)
    ├── lambda2c-emissiongap-verification.zip
    ├── matrix-plates-1.1.2.tar
    └── residual-return-verification-v2.tar
```

The three pipeline directories, together with the `relational-charge-verification/` deposit, are the
**canonical source of truth**. The contents of `Zipped-Tarred-Pipelines/` are convenience snapshots
for offline distribution — do not edit them or treat them as authoritative.

---

## Documentation map

Every directory carries a README explaining what lives there. Start at the pipeline root, then
drill into the sub-package READMEs.

- **lambda2c-emissiongap-verification** — [README](lambda2c-emissiongap-verification/README.md) ·
  [`harness/`](lambda2c-emissiongap-verification/harness/README.md) ·
  [`papers/`](lambda2c-emissiongap-verification/papers/README.md) ·
  [`tests/`](lambda2c-emissiongap-verification/tests/README.md) ·
  [`output/`](lambda2c-emissiongap-verification/output/README.txt)
- **matrix-plates** — [README](matrix-plates/README.md) ·
  [`src/matrix_plates/`](matrix-plates/src/matrix_plates/README.md) ·
  [`docs/`](matrix-plates/docs/README.md) ·
  [`examples/`](matrix-plates/examples/README.md) ·
  [`tests/`](matrix-plates/tests/README.md) ·
  [`web/`](matrix-plates/web/README.md)
- **residual-return-verification** — [README](residual-return-verification/README.md) ·
  [`L00M/`](residual-return-verification/L00M/README.md) ·
  [`L00M/training/`](residual-return-verification/L00M/training/README.md) ·
  [`L00M/paper/`](residual-return-verification/L00M/paper/README.md) ·
  [`kira-language/`](residual-return-verification/kira-language/README.md) ·
  [`kira-language/kira_language/`](residual-return-verification/kira-language/kira_language/README.md) ·
  [`kira-language/candidates/`](residual-return-verification/kira-language/candidates/README.md)
- **Site & meta** — [`papers/`](papers/README.md) ·
  [`site/`](site/README.md) ·
  [`.github/`](.github/OVERVIEW.md) ·
  [`Zipped-Tarred-Pipelines/`](Zipped-Tarred-Pipelines/README.md)

---

## License & citation

This repository is released under the **MIT License** — Copyright (c) 2026 Echo-S Studios — see
[`LICENSE`](LICENSE). The companion papers are included under the same MIT terms (these can be
swapped to **CC-BY** for the prose if preferred). To cite this work, see
[`CITATION.cff`](CITATION.cff).
