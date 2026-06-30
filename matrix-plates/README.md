# Matrix Plates

Exact integer-matrix constructions, a **Mahler-measure spectrum** layout, and the
**`companion ∘ charpoly` closure** — the computational backend for
[`web/matrix_plates.html`](web/matrix_plates.html), plus the patched tool itself.

Each construction emits an exact integer matrix (a *plate*) graded by the Mahler
measure of its characteristic polynomial. Every invariant is computed in exact
integer / rational arithmetic — characteristic **and minimal polynomial**, the
**invariant factors** (a complete similarity invariant via Smith normal form over
`ℚ[x]`), determinant, trace, rank — plus the matrix **house** `⌈A⌉ = max|λ|`
alongside the Mahler measure. See [`docs/DESIGN.md`](docs/DESIGN.md) for the
metaphors and [`docs/matrix_plates_build_spec.md`](docs/matrix_plates_build_spec.md)
for the full spec.

- **Goal 1 — Mahler as the layout axis.** A `log M` spectrum with the floor pinned
  at `M = 1` (the cyclotomic / Kronecker floor), so the empty `(1, Lehmer)` band
  stays visible; the SVG shades the Lehmer gap.
- **Goal 2 — `charpoly ↦ companion` closure.** Lift a plate's exact characteristic
  polynomial into a **queryable, self-extending** seed registry and build its
  companion (rational-canonical) representative, with full **provenance** of each
  lift.

The two compose: because the lift preserves `M`, a lifted companion lands in its
source's Mahler bin — and `φ ⊕ φ` puts a derogatory matrix and its **non-similar**
companion in the same bin (same spectrum, different minimal polynomial /
invariant factors).

> **Try it live.** The interactive tool is hosted on the project's GitHub Pages
> site at **[echo-s-studios.github.io/math-research-pipelines/tool/](https://echo-s-studios.github.io/math-research-pipelines/tool/)**
> — no install, exact in-browser BigInt arithmetic. matrix-plates is one of three
> exact-arithmetic pipelines in this repo; see [Related pipelines](#related-pipelines)
> and the [live site](https://echo-s-studios.github.io/math-research-pipelines/).

## Install

Pure Python, **standard library only** — no third-party runtime dependency.

```bash
pip install -e .            # exposes the `matrix-plates` console script
# or run in place:
export PYTHONPATH=src
python -m matrix_plates.cli --help
```

Optional: `pip install -e ".[dev]"` adds `sympy`, `numpy`, and `hypothesis` — used
only for the optional verification bridge and property tests. The committed
fixtures mean the core suite itself needs nothing extra.

## Quickstart

```bash
matrix-plates demo                       # the φ ⊕ φ similarity-class demonstration
matrix-plates verify                     # the build-spec checklist (10/10)
matrix-plates batch                      # reproduce the tool's seed batch
matrix-plates analyze '[[0,1,0,0],[1,1,0,0],[0,0,0,1],[0,0,1,1]]'   # full data + companion form
matrix-plates compare phi sq2            # spectrum / Mahler / house / similarity, side by side
matrix-plates extend phi --in-batch      # lift through Φ; show lineage + what it extends
matrix-plates spectrum --svg s.svg --html s.html
matrix-plates export phi --format latex  # or json | sympy | html  (--out FILE)
```

A *target* for `analyze` / `compare` / `extend` / `export` is a seed id (`phi`,
`sq2`, … → its companion) or a matrix literal (`'[[0,1],[1,1]]'` or `'0 1; 1 1'`).

```python
import matrix_plates as mp

a = mp.analyse(mp.build("dsum", a="phi", b="phi").M)   # φ ⊕ φ
a.deg_char, a.deg_min, a.derogatory, a.defective       # (4, 2, True, False)
a.house, a.invariant_factors                           # (1.618…, [[1,-1,-1],[1,-1,-1]])

mp.is_similar(a.M, mp.rational_canonical_form(a.M))    # True
d = mp.similarity_class_demo()
d.same_char_poly, d.same_invariant_factors, d.similar  # (True, False, False)

g = mp.Gallery.seed_batch()
print(mp.render_ascii(mp.build_histogram(g.plates, max_log_m=g.max_log_m)))
print(mp.export_json(g.plates))                        # or export_latex / export_sympy
```

## The interactive tool

[`web/matrix_plates.html`](web/matrix_plates.html) is the reference tool with all
build-spec edits applied — a single self-contained file (no build, no network).
Press **Seed batch**, switch **Layout → Mahler spectrum**, use a plate's **↦
companion seed** button, or pick **Custom matrix** to type your own and read its
spectral data, **minimal polynomial**, **invariant factors** (derogatory / defective),
**companion form** with an exact similarity verdict, and **JSON / LaTeX / SymPy**
export — all computed in-browser with exact BigInt rational arithmetic (no backend),
at any matrix size via a fraction-free minimal polynomial.
See [`web/README.md`](web/README.md).

## Repository layout

Each subdirectory carries its own README with a deeper map; this is the overview.

```
matrix-plates/
├── README.md   CHANGELOG.md   pyproject.toml   Makefile   LICENSE   MANIFEST.md
├── docs/                     # → docs/README.md  (index of the design docs)
│   ├── DESIGN.md                     # the "plates" + "companion closure" metaphors
│   ├── matrix_plates_build_spec.md   # the comprehensive spec (math + both goals)
│   ├── matrix_plates_guide.md        # matrix-family → generator field manual
│   ├── HTML_EDITS.md                 # changelog of the edits to the reference tool
│   └── matrix_plates.html.patch      # unified diff: reference → patched tool
├── web/                      # → web/README.md
│   └── matrix_plates.html    # patched interactive tool (hosted at the Pages site /tool/)
├── src/matrix_plates/        # → src/matrix_plates/README.md  (module-by-module map)
│   ├── linalg.py  roots.py  prng.py  seeds.py  operators.py
│   ├── polynomial.py  canonical.py  cache.py        # exact ℚ[x], invariant factors, memoization
│   ├── invariants.py  plates.py  histogram.py  closure.py
│   ├── export.py  bridge.py                         # JSON/LaTeX/SymPy; optional numpy/sympy
│   └── render_html.py  text.py  cli.py
├── examples/                 # → examples/README.md
│   ├── phi_plus_phi.py       # the derogatory similarity witness
│   └── mahler_spectrum.py    # the seed-batch spectrum → SVG/HTML
└── tests/                    # → tests/README.md  (139 tests; 133 core + hypothesis)
    └── fixtures/             # ground_truth_js.json, oracle_sympy.json, ground_truth.js,
                              # invariant_factors_oracle.json
```

**Where things live.** The exact kernels are `linalg.py` (Faddeev–LeVerrier
char-poly, rational Krylov minimal polynomial, rank), `polynomial.py` (the `Poly`
type over ℚ), and `canonical.py` (Smith normal form over ℚ[x] → invariant factors /
similarity). Goal 1 is `histogram.py`; Goal 2 is `closure.py`. `invariants.analyse`
ties them together into a `Plate`, memoized through `cache.py`. Presentation is
`render_html.py` / `export.py` / `text.py`, and the `matrix-plates` console script
is `cli.py`. The optional sympy/numpy oracles live in `bridge.py`. See
[`src/matrix_plates/README.md`](src/matrix_plates/README.md) for one or two lines on
every module and a seed→plate→invariants→spectrum/closure→export data-flow diagram.

## Testing

```bash
make test          # python -m unittest discover -s tests  (stdlib only)
make verify        # the build-spec checklist (10/10)
```

The suite is **139 tests** (133 core + the `hypothesis` property tests, run when
that optional package is installed) plus the **10/10** build-spec checklist. It
cross-checks the pure-Python core against independent oracles committed under
`tests/fixtures/`: the reference engine's **verbatim JS run under Node** (matrices,
char-polys, PRNG), an **independent sympy** computation (char-poly, minimal
polynomial, Mahler, `ρ`, `det`, `tr`, `rank`), and a sympy **determinantal-divisor**
oracle for the invariant factors. The Smith-normal-form code was additionally fuzzed
on 4000 random matrices (0 failures). `test_property.py` adds `hypothesis` coverage
when that optional package is installed (skipped otherwise); `test_bridge.py`
validates the optional numpy/sympy bridge when present. See
[`tests/README.md`](tests/README.md) for the file-by-file map and the oracle layout.

## Exactness & reproducibility

`det`, `tr`, `rank`, characteristic polynomial, **minimal polynomial**,
**invariant factors**, `derogatory`, `defective`, and `unimodular` are
**integer-exact** (Faddeev–LeVerrier; rational Krylov; Smith normal form over
`ℚ[x]`). `mahler`, **house** `⌈A⌉`, `ρ`, and eigenvalue positions are floating
point — trust the integer engravings for anything quantitative. House is a *max*
and Mahler a *product*; they differ (e.g. `√2`: house `≈1.414`, Mahler `2`). The
`mulberry32` PRNG is a **bit-exact** port of the tool's generator, so a
`(construction, seeds, params, RNG seed)` tuple reproduces the same matrix in both
the browser tool and the Python package.

## Worked examples

Three short reads that the package was built to make precise.

**1. Same spectrum, not similar — `φ ⊕ φ`.** The flagship Goal-2 case. The
derogatory parent and its companion lift agree on char-poly / det / trace / Mahler
and are both unimodular, but split on the minimal polynomial and the invariant
factors:

```python
import matrix_plates as mp
d = mp.similarity_class_demo()
d.same_char_poly, d.same_det, d.same_mahler        # (True, True, True)
d.same_min_poly, d.same_invariant_factors, d.similar  # (False, False, False)
mp.analyse(d.parent.M).invariant_factors           # [[1,-1,-1],[1,-1,-1]]  (φ⊕φ)
mp.analyse(d.child.M).invariant_factors            # [[1,-2,-1,2,1]]        (companion)
```

Run it end to end with `matrix-plates demo`, or
[`examples/phi_plus_phi.py`](examples/phi_plus_phi.py).

**2. House and Mahler come apart — `√2`.** House is a *max*, Mahler a *product*, so
they disagree whenever more than one eigenvalue leaves the unit circle:

```python
a = mp.analyse(mp.build("companion", a="sq2").M)   # companion of x²−2
round(a.house, 3), round(a.mahler, 3)              # (1.414, 2.0)  →  M > ⌈A⌉
```

Contrast `φ` (only one root outside), where house `=` Mahler `= φ`. Compare them
directly with `matrix-plates compare sq2 phi`.

**3. The closure is self-extending.** Lifting mints a new `p̂ₖ` seed; lifting the
same spectrum again reuses it (the fixed point), and the generated seed feeds every
binary operator:

```python
from matrix_plates.closure import Registry, lift
g, reg = mp.Gallery(), Registry()
parent = g.add(mp.build("dsum", a="phi", b="phi"))
first  = lift(parent, reg, gallery=g)              # mints  p̂₁
second = lift(first.child, reg, gallery=g)         # reuses p̂₁  (idempotent Φ)
first.reused, second.reused                        # (False, True)
g.lineage(second.child)                            # parent → child → grandchild
```

The CLI surfaces lineage and "what extends this seed" with
`matrix-plates extend phi --in-batch`.

## Troubleshooting

- **`ModuleNotFoundError: matrix_plates`** — install it (`pip install -e .`) or run
  in place with `export PYTHONPATH=src` before `python -m matrix_plates.cli …`. The
  examples expect `PYTHONPATH=../src` from inside `examples/`.
- **`ValueError: char_poly requires an integer matrix` / "entry … is not an
  integer"** — this system works over ℤ. Floats and symbols are rejected at the
  door (`build_custom`); use a `companion` / `cartan` / … construction for algebraic
  seeds rather than typing irrational entries.
- **`[A,B] needs equal sizes`** — the commutator and Kronecker pairings require
  compatible seed degrees; pick seeds whose companions match (`compare` prints each
  size).
- **"char-poly is not a monic integer polynomial — cannot lift"** — only monic
  integer characteristic polynomials lift to an algebraic-integer seed; a non-monic
  or non-integer input cannot become a registry seed.
- **The Mahler value looks slightly off / the root plot smears** — `mahler`,
  `house`, `ρ`, and eigenvalue *positions* are floating point (Durand–Kerner
  converges slowly near multiple roots, e.g. `(x²−x−1)²`). Trust the **integer
  engravings** (char-poly, minimal polynomial, invariant factors, det, tr, rank).
- **`sympy` / `numpy` / `hypothesis` checks skipped** — these are optional `[dev]`
  extras; `pip install -e ".[dev]"` enables the live oracle bridge and the property
  tests. The core suite is stdlib-only and passes without them.

## A precise caveat (see spec §2.2 / DESIGN §3.5)

The "structured clusters in `[φ, 2]`, random scatters right" framing is a useful
slogan but **not literally true**: only the quadratic units (`φ`, `τ`, `√2`) sit in
`[φ, 2]`; `E₈`, the Fibonacci circulant, and the frustrated ring have large
measures, and the random plate often lands mid-pack. The robust signals are the
**empty `(1, Lehmer)` band** and the **discreteness** of structured Mahler values
versus the **scatter** of the random control.

## Related pipelines

matrix-plates is one of three exact-arithmetic verification pipelines in the
[**math-research-pipelines**](../README.md) repo, all sharing the discipline that
**no float crosses a decision boundary**:

- [**lambda2c-emissiongap-verification**](../lambda2c-emissiongap-verification/) —
  verifies *The Exchange Rate λ = 2c* and *The Emission-Gap Theorem*, including the
  integer-quadratic Mahler floor `M ∈ {1} ∪ [φ, ∞)` and the no-Salem closure (the
  same Mahler-measure / Lehmer territory this package explores, on the theorem side).
- [**residual-return-verification**](../residual-return-verification/) — exact
  learning geometry over number fields (*The Vector Substrate*, *Residual Return*).

The whole project is published on GitHub Pages at
**[echo-s-studios.github.io/math-research-pipelines](https://echo-s-studios.github.io/math-research-pipelines/)**,
with this package's interactive tool hosted at
**[/tool/](https://echo-s-studios.github.io/math-research-pipelines/tool/)** —
the same exact engine as the backend, running entirely in-browser.

## License

MIT — see [`LICENSE`](LICENSE).
