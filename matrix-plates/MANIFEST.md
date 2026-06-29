# MANIFEST — matrix-plates 1.1.2

**This archive is self-contained.** Nothing outside it is required to build, run,
test, or view the system. The package has **zero third-party runtime
dependencies**.

## Requirements

| To… | You need |
|---|---|
| run the backend, tests, CLI | Python ≥ 3.9 (standard library only) |
| view the interactive tool | any web browser (the HTML is one offline file, no server) |
| optional verification bridge / property tests | `sympy`, `numpy`, `hypothesis` — *not* needed to run the shipped suite |

## Integrity

`SHA256SUMS` lists every file. After extracting, verify with:

```bash
cd matrix-plates && sha256sum -c SHA256SUMS
```

Key file — the patched interactive tool, `web/matrix_plates.html`:
`fd6db69c181ca014934739b7580471644121bbb81988d61061d3f4f98cbfa04d`
(the upstream reference is `97187b781289324e9e8ee725138dcec0fd389b08a6dcb7a8140561e225442ca3`;
`docs/matrix_plates.html.patch` transforms one into the other).

## Contents

### Root

| Path | Purpose |
|---|---|
| `README.md` | overview, install, quickstart, repo layout |
| `CHANGELOG.md` | release notes (1.0.0, 1.1.0) |
| `MANIFEST.md` | this inventory |
| `SHA256SUMS` | checksums for every file (`sha256sum -c`) |
| `LICENSE` | MIT |
| `pyproject.toml` | packaging; stdlib-only; `matrix-plates` console script |
| `Makefile` | `test` / `verify` / `demo` / `histogram` / `export` / `clean` |
| `.gitignore` | ignores build/venv/pycache artifacts |

### `docs/`

| Path | Purpose |
|---|---|
| `DESIGN.md` | the *plates* and *companion closure* metaphors, mathematically, with worked examples |
| `matrix_plates_build_spec.md` | the comprehensive spec: math foundations, both goals, architecture, complexity, edge cases, verification matrix, references |
| `HTML_EDITS.md` | change record for the edits applied to the reference HTML (v1.0 + v1.1), with apply/verify steps |
| `matrix_plates.html.patch` | byte-exact, apply-able unified diff (reference → patched), 16 hunks |
| `matrix_plates_guide.md` | field manual: matrix-family → generator recipes |

### `web/`

| Path | Purpose |
|---|---|
| `matrix_plates.html` | the patched interactive tool (reference + all edits); single self-contained file; computes minimal polynomial / invariant factors / similarity inline (exact BigInt rationals) |
| `README.md` | what changed vs. the reference, how to run |

### `src/matrix_plates/` — the exact backend (stdlib only)

| Path | Purpose |
|---|---|
| `__init__.py` | public API surface |
| `linalg.py` | exact integer/rational LA: `matmul`, big-int `matpow`, Faddeev–LeVerrier `char_poly`, rational-Krylov `min_poly`, exact `rank` |
| `roots.py` | Durand–Kerner roots; Mahler measure, spectral radius (house), unit-circle classification |
| `prng.py` | bit-exact `mulberry32` + seeded integer matrices |
| `seeds.py` | the nine algebraic-integer seeds (monic integer minimal polynomials) |
| `operators.py` | constructions + `OPS` catalogue + `build` dispatcher + `build_custom` |
| `polynomial.py` | exact `Poly` over `ℚ` (add/mul/divmod/gcd/squarefree/derivative/LaTeX) |
| `canonical.py` | invariant factors / rational canonical form / `is_similar` via Smith normal form over `ℚ[x]` |
| `cache.py` | LRU memoization of char-poly / min-poly / invariant factors |
| `invariants.py` | `analyse(M)` → full chip set, minimal polynomial, invariant factors, **house**, derogatory / defective, Lehmer-gap flags |
| `plates.py` | `Plate`, `Provenance`, `Gallery` (id-indexed; lineage / descendants) |
| `histogram.py` | **Goal 1**: log-M binning, family split, ASCII/SVG (shaded Lehmer gap), sorted reflow |
| `closure.py` | **Goal 2**: `Φ = companion∘charpoly`, queryable self-extending `Registry`, spectrum-containment, similarity classes |
| `export.py` | JSON / LaTeX / SymPy exporters |
| `bridge.py` | optional NumPy/SymPy bridge (lazy; never a hard dependency) |
| `render_html.py` | static gallery + spectrum HTML export |
| `text.py` | formatting helpers (subscripts, signed numbers, polynomial printer, viridis) |
| `cli.py` | the `matrix-plates` command (gen / batch / analyze / spectrum / extend / compare / lift / demo / verify / export) |

### `examples/`

| Path | Purpose |
|---|---|
| `phi_plus_phi.py` | the φ ⊕ φ derogatory similarity-class witness |
| `mahler_spectrum.py` | seed-batch spectrum → ASCII + SVG + HTML |

### `tests/` — 133 tests, stdlib only (1 skipped without `hypothesis`)

| Path | Purpose |
|---|---|
| `_util.py` | fixture loader + float-closeness helper |
| `test_linalg.py` | products, big-int powers, char-poly, det, rank, poly helpers |
| `test_minpoly.py` | minimal polynomial vs sympy oracle (incl. derogatory cases) |
| `test_invariants.py` | `analyse` bundle vs oracle (exact integers + float tolerances) |
| `test_polynomial.py` | exact `Poly` arithmetic, division, gcd, squarefree, LaTeX |
| `test_canonical.py` | invariant factors / similarity / RCF vs sympy determinantal-divisor oracle |
| `test_cache.py` | memoization correctness, hit accounting, mutation safety |
| `test_prng.py` | `mulberry32` bit-exact parity with the reference JS |
| `test_operators.py` | constructions vs JS, operator laws, dispatcher, `build_custom` errors |
| `test_histogram.py` | floor pinned at M=1, binning, Lehmer band, reflow, renderers |
| `test_closure.py` | lift fixed point, φ⊕φ non-similarity, dedupe, composition |
| `test_provenance.py` | provenance records + gallery lineage / descendants |
| `test_export.py` | JSON / LaTeX / SymPy export (structure, roundtrip, runnable code) |
| `test_bridge.py` | optional numpy/sympy bridge (skips if absent) |
| `test_edge_cases.py` | derogatory vs defective, repeated eigenvalues, cyclotomic, nilpotent/singular |
| `test_lehmer.py` | Lehmer-gap regression + house-vs-Mahler distinction |
| `test_property.py` | hypothesis property tests (skipped if hypothesis absent) |
| `test_verify_spec.py` | the build-spec checklist + named numeric anchors |
| `fixtures/ground_truth_js.json` | reference-engine JS outputs (matrices, char-polys, PRNG) |
| `fixtures/oracle_sympy.json` | independent sympy oracle (char-poly, min-poly, Mahler, …) |
| `fixtures/invariant_factors_oracle.json` | sympy determinantal-divisor oracle for invariant factors |
| `fixtures/ground_truth.js` | the Node script that produced the JS fixtures |

## Quickstart

```bash
tar -xzf matrix-plates-*.tar.gz && cd matrix-plates   # version-agnostic; dir is unversioned
sha256sum -c SHA256SUMS          # optional integrity check
make test                        # 133 tests  -> OK (1 skipped without hypothesis)
make verify                      # build-spec checklist -> 10/10
xdg-open web/matrix_plates.html  # or: python3 -m http.server -d web 8000
```

See `README.md` for the full guide, `docs/DESIGN.md` for the concepts, and
`docs/matrix_plates_build_spec.md` for the design and verification matrix.
