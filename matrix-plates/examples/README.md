# `examples/` — the two flagship worked examples

Two runnable scripts, one per goal, each demonstrating the matrix-plates system on
the canonical case. Both import the package (`matrix_plates`) and assume it is
importable — either install it (`pip install -e .` from the package root) or set
`PYTHONPATH=../src` as shown below. They are stdlib-only at runtime, exactly like
the core package.

For the conceptual background see [`../docs/DESIGN.md`](../docs/DESIGN.md)
(§3.1 and §3.3 are these two examples); for the same demonstrations from the CLI
see `matrix-plates demo` and `matrix-plates spectrum`; for the package overview see
[`../README.md`](../README.md).

## [`phi_plus_phi.py`](phi_plus_phi.py) — the derogatory similarity witness (Goal 2)

Builds `φ ⊕ φ` (two golden-ratio companion blocks) and its companion lift
`companion(charpoly(φ ⊕ φ)) = companion((x²−x−1)²)`, then prints both matrices and
their invariants side by side. The point: the two share **everything spectral** —
characteristic polynomial `(x²−x−1)²`, `det 1`, `tr 2`, Mahler measure `φ²`, both
unimodular — yet are **not similar**, because their minimal polynomials differ in
degree (2 for the derogatory parent vs 4 for the companion). It is the whole
"equal characteristic polynomial ⇏ similar" lesson in one pair; the minimal
polynomial / invariant factors are what separate the similarity classes. Drives
`matrix_plates.similarity_class_demo()`.

```bash
cd examples
PYTHONPATH=../src python3 phi_plus_phi.py
```

## [`mahler_spectrum.py`](mahler_spectrum.py) — the seed-batch spectrum (Goal 1)

Loads the tool's nine-plate *Seed batch*, bins it in `log M` with the floor pinned
at `M = 1`, and prints the ASCII Mahler spectrum plus the lighter sorted reflow
(plates in ascending `M`). It then writes two self-contained artifacts to the
current directory:

- `spectrum.svg` — the spectrum axis with the teal `M = 1` floor tick, the gold
  Lehmer tick, and the shaded (conjecturally empty) `(1, L)` band;
- `spectrum.html` — the full page: the SVG axis on top, the binned plates below.

The script's own docstring carries the precision note: the robust signal is the
**empty `(1, Lehmer)` band** plus the discreteness of structured Mahler values, not
the false slogan that every structured plate sits in `[φ, 2]` (`E₈`, the Fibonacci
circulant, and the frustrated ring all have large measures; the random plate often
lands mid-pack). Drives `Gallery.seed_batch()`, `build_histogram`, `render_ascii`,
`render_svg`, `sorted_reflow`, and `spectrum_html`.

```bash
cd examples
PYTHONPATH=../src python3 mahler_spectrum.py
# writes spectrum.svg and spectrum.html into the current directory
```
