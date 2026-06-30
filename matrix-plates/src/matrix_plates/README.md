# `matrix_plates` — the exact backend, module by module

This package is the stdlib-only computational backend behind the interactive tool
[`web/matrix_plates.html`](../../web/matrix_plates.html): the same operator algebra
over the same algebraic-integer seed registry, computed in **exact integer /
rational arithmetic**, with the minimal polynomial added so the
`companion ∘ charpoly` closure can make precise statements about *similarity
classes*. The public surface is re-exported from
[`__init__.py`](__init__.py) (`__version__ == "1.1.2"`); import it as `matrix_plates as mp`
and call `mp.build`, `mp.analyse`, `mp.Gallery`, `mp.lift`, etc.

For the metaphors see [`../../docs/DESIGN.md`](../../docs/DESIGN.md); for the full
spec see [`../../docs/matrix_plates_build_spec.md`](../../docs/matrix_plates_build_spec.md);
for the top-level overview and CLI quickstart see [`../../README.md`](../../README.md).

## Module map

The package is layered: low-level exact kernels at the bottom, the two goals
(Mahler spectrum, companion closure) in the middle, and presentation / CLI on top.
"Exact" means integer or `fractions.Fraction` arithmetic — no value a verdict
depends on is ever a float. "Float" means floating point, used only for
inherently transcendental display quantities (eigenvalue positions, Mahler
measure, house).

### Exact kernels

| Module | Exact? | Role |
|---|---|---|
| [`linalg.py`](linalg.py) | **exact** (ℤ / ℚ) | Core linear algebra over the integers and rationals: `matmul`, `matpow` (fast exponentiation over Python big integers — never overflows), `char_poly` + `determinant` (Faddeev–LeVerrier, integer-exact), `rank` (rational Gaussian elimination), and `min_poly` (the Goal-2 workhorse: exact rational Krylov dependence, monic, integer coefficients). `Matrix = List[List[int]]`. |
| [`polynomial.py`](polynomial.py) | **exact** (ℚ) | The `Poly` type — univariate polynomials over ℚ with `Fraction` coefficients stored low→high, trailing zeros trimmed. Long division (`divmod`), monic `gcd` (Euclidean), `deriv`, `is_squarefree` (the test behind the `defective` flag), and `latex`. Bridges the codebase's **high→low** integer convention via `from_high_low` / `to_high_low`. ℚ[x] is a Euclidean domain, which is what Smith form over a PID needs. |
| [`canonical.py`](canonical.py) | **exact** (ℚ[x]) | Rational canonical form and the complete similarity invariant. `invariant_factors` (the Smith normal form of `xI − A` over ℚ[x], with a fast non-derogatory short-circuit to avoid coefficient swell), `similarity_key`, `is_similar` (exact similarity over ℚ via equal invariant factors), and `rational_canonical_form` (⊕ of companions of the invariant factors). |
| [`prng.py`](prng.py) | float (deterministic) | `mulberry32` — a **bit-exact** port of the tool's JavaScript generator (reproduces every 32-bit truncation, `Math.imul`, and operator-precedence subtlety), plus `rand_int_matrix` (the `[−3,3]` control family) and `sample`. Outputs are floats but fully reproducible; this is the one stochastic source, and cross-tool reproducibility depends on it matching the JS exactly. |
| [`roots.py`](roots.py) | **float** | The *only* module that introduces floating point for math (not just display). `dk_roots` (Durand–Kerner eigenvalue positions, a faithful port of the tool's `dkRoots`), `spectral_radius` (`ρ`), `mahler_from_roots` (`M`), and `classify_unit_circle` (eigenvalue counts outside / on / inside). Roots smear near multiple roots — trust the integer chips for anything quantitative. |

### Seeds & constructions

| Module | Exact? | Role |
|---|---|---|
| [`seeds.py`](seeds.py) | **exact** | The algebraic-integer seed registry — nine `Seed`s naming an algebraic integer by its monic integer minimal polynomial (`phi`, `tau`, `sq2`, `sq3`, `sq5`, `gap`, `K`, `cons`, `res`), reproducing the tool's registry verbatim (glyphs and field labels included). Only monic integer polynomials are admitted — non-algebraic-integer ZFP values are excluded on purpose to keep the integer-matrix invariant. `base_registry()` returns a fresh mutable copy the closure can extend. |
| [`operators.py`](operators.py) | **exact** | The construction catalogue — one builder per matrix family (`companion`, `kron` ⊗, `dsum` ⊕, `commutator` [A,B], `cartan_a/d/e8`, `circulant` from a Fibonacci/Lucas row, `frustrated_ring`, `rand`, `custom`), each emitting an exact integer matrix plus a label/provenance/note (`Built`). The `OPS` catalogue and `build()` dispatcher mirror the tool's operator algebra; `build_custom` validates square integer input with specific error messages; `seed_batch_specs()` reproduces the tool's *Seed batch* exactly. |

### Goal 1 — the Mahler spectrum

| Module | Exact? | Role |
|---|---|---|
| [`histogram.py`](histogram.py) | mixed | Promotes `M` from a colour to the **layout axis**. `build_histogram` bins plates in `log M` with the floor **pinned at `M = 1`** (never auto-scaled), `spectrum_bins` (the `⌈√n⌉` rule clamped to `[3,12]`), `family_of` (structured vs the seeded-random control), `sorted_reflow` (the lighter monotone variant), and `render_ascii` / `render_svg`. Binning uses the exact `M`; the renderers are float (positions, viridis). Re-exports `LEHMER`. |

### Goal 2 — the companion closure

| Module | Exact? | Role |
|---|---|---|
| [`closure.py`](closure.py) | **exact** verdicts | `Φ = companion ∘ charpoly` as a closure. `lift` (validate monic-integer char-poly → dedupe against the registry → build the companion → classify the relationship), the self-extending `Registry` (deduplicates by char-poly signature so fixed points don't multiply), `divides` / `spectrum_contains` / `query_extends`, `similarity_classes`, `is_similar_to_companion_lift`, and `similarity_class_demo` (the worked `φ ⊕ φ` witness). The similarity verdict is exact: similar ⇔ the input is non-derogatory. |

### Analysis, plates & galleries

| Module | Exact? | Role |
|---|---|---|
| [`invariants.py`](invariants.py) | mixed | `analyse(M) → Analysis` — the complete invariant bundle for one matrix, routed through the memoized exact kernels. Exact: `coeffs`, `det`, `tr`, `rank`, `minpoly`, `invariant_factors`, `derogatory`, `defective`, `unimodular`. Float: `mahler`, `house`/`rho`, `frob`, eigenvalue positions. Adds the **house** `⌈A⌉` (a *max*; Mahler is a *product* — they come apart) and the Lehmer flags `at_floor` / `in_lehmer_gap`. `LEHMER = 1.17628` is the single source of truth. |
| [`cache.py`](cache.py) | — | LRU memoization (`maxsize=8192`) of `char_poly`, `min_poly`, and `invariant_factors`, keyed by a frozen tuple-of-tuples view of the matrix — those are `O(n⁴)` each and get recomputed across re-analysis / lifting / class-grouping. `cache_info()` and `clear_caches()` for inspection / isolation. |
| [`plates.py`](plates.py) | — | `Plate` (a built matrix + its `Analysis` + a stable id + `Provenance`), `Provenance` (`construct` / `lift` / `custom`, with lift parents), `build_plate`, and `Gallery` — an ordered collection with id-indexing, the running `log M` ceiling for Goal 1, and `lineage` / `descendants` to trace successive companion lifts. `Gallery.seed_batch()` preloads the tool's nine-plate batch. |

### Rendering & export

| Module | Exact? | Role |
|---|---|---|
| [`render_html.py`](render_html.py) | — | Self-contained HTML/SVG matching the tool's `Export .html` look. `gallery_html` (a plate sheet, each card annotated with char-poly, minimal polynomial, and a derogatory flag) and `spectrum_html` (the Goal-1 axis SVG on top, binned plates below). Dependency-free; same palette/typography as the reference. |
| [`export.py`](export.py) | — | Serialize a plate or gallery. `plate_to_dict` / `export_json` (matrix + full invariant set), `export_latex` (a LaTeX block: matrix + characteristic & minimal polynomials + invariant factors), and `export_sympy` (runnable SymPy code that reconstructs the matrix and asserts its char-poly). Reads the exact `Analysis`, so the serialized integer invariants are exact. |
| [`bridge.py`](bridge.py) | optional | The optional NumPy / SymPy bridge — **not a runtime dependency**. NumPy for fast *approximate* eigenvalues (sanity check only); SymPy for a second, independent **exact** char-poly / minimal polynomial / Mahler computation. Both lazily imported; each function raises a clear `ImportError` (naming the missing package) only if called without it. `verify(M)` cross-checks the core against whichever oracle is installed. |
| [`text.py`](text.py) | — | Pure formatting helpers mirroring the tool's `sub`, `fmt`, `polyStr`, and `viridis`, so Python output is byte-compatible with the reference labels and colour grading (Unicode subscripts and the U+2212 minus sign included). No math. |
| [`cli.py`](cli.py) | — | The `matrix-plates` console script. Subcommands `gen`, `batch`, `analyze`, `spectrum`/`histogram`, `extend`, `compare`, `lift`, `demo`, `verify` (the 10/10 build-spec checklist, encoded in `_checks()`), and `export`. A *target* is a seed id (→ its companion) or a matrix literal (JSON `'[[0,1],[1,1]]'` or `'0 1; 1 1'`). |

## Data flow

```
                 seeds.py          operators.py
              (algebraic-integer    (build / OPS:
                 registry)          companion, kron, dsum, …)
                     │                      │
                     └──────────┬───────────┘
                                ▼
                          Built (matrix + label + provenance)
                                │
                                ▼   plates.build_plate / Gallery.add
                          invariants.analyse  ──uses──▶  cache  ──▶  linalg / canonical / roots
                                │                                    (char_poly · min_poly · invariant_factors
                                ▼                                     · rank · det | dk_roots · mahler · house)
                          Plate  (Analysis + id + Provenance)
                                │
              ┌─────────────────┼──────────────────────────┐
              ▼                 ▼                           ▼
     histogram.build_histogram  closure.lift               export.* / render_html.*
     (Goal 1: log-M spectrum,   (Goal 2: Φ = companion∘    (JSON / LaTeX / SymPy /
      floor pinned at M=1)       charpoly; self-extending   HTML / SVG)
              │                  Registry; similarity)
              └─────────────▶ Gallery (lineage / descendants / max_log_m)
```

A seed (or a raw matrix) is **built** into a `Built`, **analysed** into a `Plate`
(whose `Analysis` carries every exact invariant, computed once and memoized), then
either **binned** into the Mahler spectrum (Goal 1) or **lifted** through `Φ` into
the self-extending registry (Goal 2) — and finally **exported** to JSON / LaTeX /
SymPy / HTML. The two goals compose: because `Φ` preserves `M`, a lifted companion
lands in its parent's `log M` bin, while `φ ⊕ φ` and its companion share that bin
yet differ in minimal polynomial and invariant factors — the same spectrum, a
different similarity class.

## Exactness boundary at a glance

- **Integer-exact** (trust for anything quantitative): `det`, `tr`, `rank`,
  characteristic polynomial, **minimal polynomial**, **invariant factors**,
  `derogatory`, `defective`, `unimodular`, rational canonical form, `is_similar`.
- **Floating point** (display only): `mahler`, **house** `⌈A⌉`, `ρ`, `frob`, and
  eigenvalue positions. House is a *max* and Mahler a *product*, so they differ
  (e.g. `√2`: house `≈ 1.414`, Mahler `2`).
- **Bit-exact but float-valued**: `mulberry32` — deterministic and reproducible
  across the browser tool and this package from the same seed.
