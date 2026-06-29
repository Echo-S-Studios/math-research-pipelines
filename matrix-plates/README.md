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

```
matrix-plates/
├── README.md   CHANGELOG.md   pyproject.toml   Makefile   LICENSE   MANIFEST.md
├── docs/
│   ├── DESIGN.md                     # the "plates" + "companion closure" metaphors
│   ├── matrix_plates_build_spec.md   # the comprehensive spec (math + both goals)
│   ├── matrix_plates_guide.md        # matrix-family → generator field manual
│   ├── HTML_EDITS.md                 # changelog of the edits to the reference tool
│   └── matrix_plates.html.patch      # unified diff: reference → patched tool
├── web/
│   ├── matrix_plates.html    # patched interactive tool
│   └── README.md
├── src/matrix_plates/        # the exact backend (see docs §5 / DESIGN §4 for the map)
│   ├── linalg.py  roots.py  prng.py  seeds.py  operators.py
│   ├── polynomial.py  canonical.py  cache.py        # exact ℚ[x], invariant factors, memoization
│   ├── invariants.py  plates.py  histogram.py  closure.py
│   ├── export.py  bridge.py                         # JSON/LaTeX/SymPy; optional numpy/sympy
│   └── render_html.py  text.py  cli.py
├── examples/
│   ├── phi_plus_phi.py       # the derogatory similarity witness
│   └── mahler_spectrum.py    # the seed-batch spectrum → SVG/HTML
└── tests/                    # 133 tests (1 skipped without hypothesis)
    └── fixtures/             # ground_truth_js.json, oracle_sympy.json, ground_truth.js,
                              # invariant_factors_oracle.json
```

## Testing

```bash
make test          # python -m unittest discover -s tests  (stdlib only)
make verify        # the build-spec checklist (10/10)
```

133 tests cross-check the pure-Python core against independent oracles committed
under `tests/fixtures/`: the reference engine's **verbatim JS run under Node**
(matrices, char-polys, PRNG), an **independent sympy** computation (char-poly,
minimal polynomial, Mahler, `ρ`, `det`, `tr`, `rank`), and a sympy
**determinantal-divisor** oracle for the invariant factors. The Smith-normal-form
code is additionally fuzzed on 4000 random matrices. `test_property.py` adds
`hypothesis` coverage when that optional package is installed (skipped otherwise);
`test_bridge.py` validates the optional numpy/sympy bridge when present.

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

## A precise caveat (see spec §2.2 / DESIGN §3.5)

The "structured clusters in `[φ, 2]`, random scatters right" framing is a useful
slogan but **not literally true**: only the quadratic units (`φ`, `τ`, `√2`) sit in
`[φ, 2]`; `E₈`, the Fibonacci circulant, and the frustrated ring have large
measures, and the random plate often lands mid-pack. The robust signals are the
**empty `(1, Lehmer)` band** and the **discreteness** of structured Mahler values
versus the **scatter** of the random control.

## License

MIT — see [`LICENSE`](LICENSE).
