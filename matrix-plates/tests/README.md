# `tests/` — the suite and its committed oracles

**139 tests** run under `python -m unittest discover -s tests` (133 core +
hypothesis property tests when the optional `hypothesis` package is installed),
plus the build-spec checklist (`matrix-plates verify` → **10/10**). The core suite
is **stdlib-only**: every cross-check runs against ground truth *committed under
[`fixtures/`](fixtures/)*, so no Node and no sympy are needed at test time. From
the package root:

```bash
make test          # PYTHONPATH=src python -m unittest discover -s tests -v
make verify        # the build-spec checklist (10/10)
```

The optional `pip install -e ".[dev]"` extra adds `sympy` / `numpy` / `hypothesis`,
which unlock the live-oracle bridge tests and the property tests; without them
those tests skip gracefully rather than fail. See [`../README.md`](../README.md)
and [`../src/matrix_plates/README.md`](../src/matrix_plates/README.md).

## Shared helper

[`_util.py`](_util.py) (not collected as tests) loads the committed JSON fixtures
into `JS` (`ground_truth_js.json`) and `ORACLE` (`oracle_sympy.json`), and provides
`close(a, b, rel, abs_)` for tolerance comparisons on the floating-point quantities.

## Test files → what they verify

| File | Verifies |
|---|---|
| [`test_linalg.py`](test_linalg.py) | Exact linear algebra: `matmul`, big-integer `matpow` (Fibonacci to power 200, no overflow), `char_poly` / `determinant` / `rank` against the JS and sympy oracles. |
| [`test_minpoly.py`](test_minpoly.py) | The exact minimal polynomial (the Goal-2 workhorse) vs the sympy oracle, including the derogatory `φ ⊕ φ` case (min-poly degree 2 < char-poly degree 4) and that a companion is non-derogatory (min = char). |
| [`test_polynomial.py`](test_polynomial.py) | The `Poly` type: high↔low round-trip, exact arithmetic, long division `divmod`, monic `gcd`, and `is_squarefree`. |
| [`test_canonical.py`](test_canonical.py) | Invariant factors / rational canonical form / similarity against the **determinantal-divisor oracle**: each factor's product is the char-poly, the divisibility chain holds, the last factor is the minimal polynomial, `φ ⊕ φ` is **not** similar to `companion((x²−x−1)²)`, permutation-conjugate matrices are similar, RCF is idempotent and preserves the char-poly. |
| [`test_operators.py`](test_operators.py) | Construction parity with the reference JS builders (companions, kron, dsum, commutator, Cartan A/D/E₈, Fibonacci/Lucas circulants, frustrated ring) plus operator-algebra laws (commutators trace-free, `seed_batch_specs`). |
| [`test_prng.py`](test_prng.py) | `mulberry32` **bit-exact** parity with the reference JS — the first eight outputs for seeds 42 and 7 pinned against `ground_truth_js.json`, plus the `[−3,3]` range of `rand_int_matrix`. |
| [`test_invariants.py`](test_invariants.py) | `analyse()` — the full bundle: exact integer invariants (det / tr / rank / char-poly / min-poly / degrees) against the sympy oracle, and the float quantities (Mahler, ρ) within tolerance. |
| [`test_edge_cases.py`](test_edge_cases.py) | The derogatory-vs-defective distinction (independent flags): `φ ⊕ φ` derogatory but not defective; a Jordan block defective but not derogatory; repeated eigenvalues, cyclotomic, and singular cases. |
| [`test_histogram.py`](test_histogram.py) | Goal 1: the floor pinned at `M = 1` (not the data minimum), the `⌈√n⌉` bin rule, `family_of` (structured vs seeded-random), `sorted_reflow`, and the ASCII / SVG renderers. |
| [`test_lehmer.py`](test_lehmer.py) | The Lehmer gap and the house-vs-Mahler distinction: `LEHMER ≈ 1.17628`, the floor pinned (not auto-scaled), the `(1, L)` band empty for the stock seeds, and `√2` showing house ≠ Mahler. |
| [`test_closure.py`](test_closure.py) | Goal 2: `Φ` fixed points (a companion lifts to itself), `φ ⊕ φ` lifting to a non-similar companion, the self-extending registry's signature dedupe, similarity classes, and composition (a lifted companion shares its parent's Mahler bin). |
| [`test_provenance.py`](test_provenance.py) | `Provenance` kinds (`construct` / `lift`) and `Gallery.lineage` / `descendants` across successive lifts. |
| [`test_cache.py`](test_cache.py) | The memoization layer matches the raw kernels and accumulates hits. |
| [`test_export.py`](test_export.py) | JSON / LaTeX / SymPy export: dict keys + round-trip, and that the exported invariants match the analysis. |
| [`test_bridge.py`](test_bridge.py) | The optional NumPy / SymPy bridge — **live** exact agreement (sympy char-poly / min-poly / Mahler) and approximate agreement (numpy Mahler) when those packages are present; skips otherwise. |
| [`test_property.py`](test_property.py) | The **hypothesis property tests** (below). |
| [`test_verify_spec.py`](test_verify_spec.py) | Encodes the build-spec checklist (the CLI's `_checks()`) and the named numeric anchors (`C(φ)→1.618`, `C(√2)→2`, `C(φ⁻⁴)→6.854`, E₈ unimodular, balanced vs frustrated rings) as assertions. |

## The committed oracles ([`fixtures/`](fixtures/))

The suite cross-checks the pure-Python core against **three independent sources of
ground truth**, all committed so the core suite needs no external tools:

- **[`ground_truth.js`](fixtures/ground_truth.js)** — the *generator*: the
  verbatim functions lifted from `matrix_plates.html` (`matmul`, `charPoly`,
  `mulberry32`, `randIntMat`, `companion`, `kron`, `dsum`, `commutator`,
  `frustratedRing`, …). Running it under Node emits the JSON fixture below; it is
  the auditable provenance of that file, not loaded by the tests directly.
- **[`ground_truth_js.json`](fixtures/ground_truth_js.json)** (`JS`, 25 records) —
  the captured output of that JS run: reference matrices (companions, `φ ⊕ φ`,
  kron, Cartan, circulant, rings), their char-polys, and the first PRNG outputs for
  seeds 42 / 7. This is how the Python port is checked for **bit-exact parity**
  with the browser engine (linalg, operators, PRNG).
- **[`oracle_sympy.json`](fixtures/oracle_sympy.json)** (`ORACLE`, 10 records) — an
  **independent sympy** computation: char-poly, minimal polynomial, `deg_char`,
  `deg_min`, `derogatory`, Mahler, `ρ`, `det`, `trace`, `rank`. Used by
  `test_invariants` / `test_minpoly` / `test_linalg` so the exact engine is checked
  against a different implementation, not just the JS one.
- **[`invariant_factors_oracle.json`](fixtures/invariant_factors_oracle.json)**
  (11 records, some carrying an inline `matrix`) — a sympy **determinantal-divisor**
  oracle for the invariant factors. `test_canonical` checks the Smith-form output
  against it, including the cases that separate `φ ⊕ φ` from its companion and a
  Jordan block, plus identity / cyclotomic controls.

The Smith-normal-form code was additionally **fuzzed on 4000 random matrices** (0
failures) during development — a one-off validation recorded in
[`../CHANGELOG.md`](../CHANGELOG.md), not a fixture in the committed suite.

## The hypothesis property tests

[`test_property.py`](test_property.py) generates random square integer matrices
(orders 1–4, entries in `[−3, 3]`, `max_examples=120`) and asserts the structural
invariants that must hold for *every* matrix, complementing the fixed-fixture
cross-checks:

- the characteristic polynomial is monic, integer, and degree `n`;
- the minimal polynomial **divides** the characteristic polynomial;
- `Φ` preserves the char-poly, and a companion is non-derogatory (`min = char`);
- the invariant factors **multiply to the char-poly**, form a divisibility chain,
  and end with the minimal polynomial;
- a matrix is similar to its own rational canonical form;
- the reported house matches the spectral radius.

The whole module is wrapped in a `try`-import: with `hypothesis` installed these
run as live property tests; without it, a single skipped placeholder keeps the core
suite stdlib-only.
