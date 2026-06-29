# Changelog

## 1.1.2 — fraction-free hybrid (lifts the inline cap)

Smith normal form over `ℚ[x]` suffers catastrophic intermediate coefficient swell
on *generic* matrices: a random 12×12 produced ~16,000-bit rational coefficients
and took seconds, even though the answer (the matrix is non-derogatory) is the
single, tiny characteristic polynomial. The fix is a **hybrid** that never runs
Smith elimination on that case:

- The **minimal polynomial** is computed by fraction-free rational **Krylov**
  (low swell), giving `derogatory` and `defective` directly. This now drives the
  whole computation and is available at **any size** — the `n ≤ 12` cap is gone.
- **Invariant factors**: a non-derogatory matrix has a single factor equal to the
  characteristic polynomial (returned directly, no Smith form); only *derogatory*
  matrices — which are structured and small-coefficient — run the Smith form. The
  full factor *list* defers only for derogatory matrices with `n > 24` (above the
  tool's 16×16 maximum), where the minimal polynomial and flags are still shown.
- Applied to **both** backends: `canonical.invariant_factors` (Python) and the
  in-browser engine. Generic timings: Python 16×16 `0.5s → 0.1s`, 24×24 `0.86s`;
  the browser's worst case (a 16×16 `kron` of degree-4 seeds) is ~0.6s one-time,
  everything ≤ 9×9 instant — versus the previous multi-second swell.
- Bug fixes in the browser engine: `minPolyKrylov` now uses exact **BigInt**
  matrix powers (float `matmul` overflowed 2⁵³ on `kron(res,res)`, corrupting the
  Krylov vectors); and a stray escape in the companion verdict was corrected.
- Validated against the Python backend on a 378-matrix fuzz (355 non-derogatory,
  23 derogatory): invariant factors, minimal polynomial, `derogatory`, `defective`
  all agree exactly.

## 1.1.1 — in-browser exact similarity

The interactive tool now computes the **minimal polynomial** and **invariant
factors** itself, using an exact **BigInt rational** engine (a `Fraction` type and
polynomials over `ℚ`, with the Smith normal form of `xI−A` over `ℚ[x]`) — a port of
`polynomial.py` / `canonical.py`. So `web/matrix_plates.html` decides similarity
standalone, with no backend and no floating point:

- Each plate shows its minimal polynomial, invariant factors, and **derogatory /
  defective** chips; the companion panel gives the exact verdict ("A is similar /
  NOT similar to this companion", with the invariant factors that decide it).
- JSON export now includes `min_poly`, `invariant_factors`, `derogatory`, `defective`.
- Inline computation is capped at `n ≤ 12` (≈40 ms at the cap; the backend handles
  larger). Validated against the Python backend on a 14-matrix battery (derogatory,
  defective, cyclotomic, identity/zero/scalar, `E₈`, `kron`) — exact agreement.

## 1.1.0 — improvement roadmap

A feature release implementing the full improvement roadmap. The core stays
pure-Python and exact (zero runtime dependencies); 133 tests pass (1 skipped when
the optional `hypothesis` is absent), `verify` runs 10/10.

### Mahler measure & spectrum
- **House** `⌈A⌉ = max|λ|` (Schinzel–Zassenhaus house = spectral radius) reported
  alongside the Mahler measure, with `at_floor` (`M = 1`) and `in_lehmer_gap`
  (`1 < M < L`) flags. `LEHMER` is now a single source of truth.
- The spectrum SVG shades the **Lehmer gap** so the conjecturally-empty band is
  explicit; within-bin ordering is now deterministic for near-equal `M`.

### Companion closure & self-extension  *(priority 1)*
- **Invariant factors** / **rational canonical form** via exact Smith normal form
  over `ℚ[x]` (`canonical.py`), giving a *complete* similarity invariant
  (`is_similar`, `similarity_key`). Cross-checked against a sympy
  determinantal-divisor oracle and fuzzed on 4000 random matrices (0 failures).
- **Queryable registry**: `Registry.query_extends`, `spectrum_contains`,
  `similarity_classes`.
- **Provenance**: every plate records how it was made; `Gallery.lineage` /
  `descendants` trace successive companion lifts.

### Exact arithmetic & performance
- Optional **NumPy/SymPy bridge** (`bridge.py`) for fast approximate and exact
  independent verification; lazily imported, never a hard dependency.
- **Memoization** (`cache.py`) of characteristic / minimal polynomials and
  invariant factors, keyed by a frozen matrix view.
- Documented that Faddeev–LeVerrier is already integer-exact (no intermediate
  swell beyond exact big-integers).

### Tooling
- Web tool: **custom-matrix input**, an inline **companion-form** panel, and
  per-plate **JSON / LaTeX / SymPy export** buttons.  *(priority 2)*
- New CLI subcommands: `analyze`, `spectrum`, `extend`, `compare`; `export` gains
  `--format json|latex|sympy|html`. Clearer errors for singular / non-integer /
  ill-formed matrices.
- New `Poly` type and `export.py` (`export_json` / `export_latex` / `export_sympy`).

### Testing & docs  *(priority 3)*
- New suites: `test_polynomial`, `test_canonical`, `test_cache`,
  `test_provenance`, `test_export`, `test_bridge`, `test_edge_cases`,
  `test_lehmer`, `test_property` (hypothesis, skipped if absent).
- Edge cases covered: derogatory vs defective, repeated eigenvalues, cyclotomic
  floor, nilpotent / singular, identity.
- New `docs/DESIGN.md` explaining the *plates* and *companion closure* metaphors
  with worked examples.

## 1.0.0 — initial release
Exact integer-matrix system: Goal 1 (Mahler-measure spectrum layout) and Goal 2
(`companion ∘ charpoly` closure with a self-extending seed registry), a patched
self-contained web tool, build spec, and 72 tests against sympy/JS oracles.
