# `web/matrix_plates.html` — the patched interactive tool

This is the reference `matrix_plates.html` with the two build-spec features applied
(all build-spec edits: 13 from v1.0, plus v1.1 — custom-matrix input, an inline companion-form view, and per-plate JSON/LaTeX/SymPy export; and (v1.1.1) an exact BigInt-rational engine that computes the minimal polynomial, invariant factors, derogatory/defective flags, and the companion similarity verdict in-browser — (v1.1.2) made to scale via a fraction-free Krylov minimal polynomial and a hybrid that runs the Smith form only for derogatory matrices (no practical size cap); see [`docs/matrix_plates_build_spec.md`](../docs/matrix_plates_build_spec.md) and [`docs/HTML_EDITS.md`](../docs/HTML_EDITS.md)).
Open it in any browser — it is a single self-contained file with no build step,
no network, and no dependencies.

> **Hosted live.** This exact file is published on the project's GitHub Pages site
> at **[echo-s-studios.github.io/math-research-pipelines/tool/](https://echo-s-studios.github.io/math-research-pipelines/tool/)**
> (deployed from this path) — open it there to use the tool without cloning the
> repo. The version history and the apply-able diff that produced it live in
> [`docs/HTML_EDITS.md`](../docs/HTML_EDITS.md) and
> [`docs/matrix_plates.html.patch`](../docs/matrix_plates.html.patch); the SHA-256
> of the shipped file is recorded there too.

## What changed vs. the reference

**Goal 1 — Mahler as the layout axis.** A new **Layout** control (`Insertion` /
`Mahler spectrum`). In spectrum mode the sheet becomes a histogram in `log M`:

- the left edge is pinned at **`M = 1`** (the cyclotomic / Kronecker floor), *not*
  auto-scaled to the data minimum, so the empty `(1, Lehmer)` band stays visible;
- a ruler under the console marks the `M = 1` floor (teal), Lehmer's number
  `≈ 1.176` (gold), and the current `M_max` (right edge);
- bins use the `⌈√n⌉` rule, capped to `[3, 12]`;
- the random control family renders with a dashed border.

**Goal 2 — `charpoly ↦ companion` closure.** Each plate gains a **`↦ companion seed`**
button. It lifts the plate's exact characteristic polynomial into the seed
registry and builds its companion matrix — the rational-canonical representative
of that spectrum. The registry is **self-extending**: the new `p̂ₖ` seed appears
in *Seed A* / *Seed B* and feeds every binary operator (`⊗`, `⊕`, `[A,B]`).

The two compose: because the lift preserves `M`, a lifted companion lands in its
parent's bin in spectrum mode — and the `φ ⊕ φ` case puts a derogatory matrix and
its non-similar companion in the **same column** (identical `M`, different minimal
polynomial).

## How to run

```bash
# just open it
xdg-open web/matrix_plates.html      # Linux
open     web/matrix_plates.html      # macOS
```

Quick tour: press **Seed batch**, switch **Layout → Mahler spectrum** (watch the
axis and family separation), then build **Direct sum** with Seed A = `φ`, Seed B =
`φ` and click **↦ companion seed** — the lifted plate shares the parent's bin but
carries a different minimal polynomial.

## What's in the tool

Everything the tool computes is exact and runs in-browser — no backend, no network.

- **Constructions** — the same catalogue as the package: `Companion C(p)`,
  `Kronecker A⊗B`, `Direct sum A⊕B`, `Commutator [A,B]`, `Cartan` (A/D/E₈),
  `Fibonacci/Lucas circulant`, `Frustrated ring`, `Random (seeded)`, and **Custom
  matrix** (a textarea parsed from rows / JSON, with square-and-integer validation
  and specific error messages).
- **Invariant chips** — `det`, `tr`, `ρ`, `‖·‖_F`, **Mahler `M`**, `rank`,
  `integer`, `unimodular`, the eigenvalue split relative to the unit circle, plus
  (v1.1.1) the **minimal polynomial**, **invariant factors**, and
  `derogatory` / `defective` flags — all from the exact BigInt-rational engine.
- **Companion-form panel** — every plate renders `companion(charpoly)` inline next
  to it, with a one-line **exact similarity verdict** (similar ⇔ non-derogatory).
- **Per-plate export** — JSON, LaTeX (`bmatrix` + polynomial), or runnable SymPy,
  written via an in-browser download.
- **The two build-spec features** — the **Layout** control (Insertion / Mahler
  spectrum) and the **`↦ companion seed`** lift button, described above.

The exact engine (v1.1.1 / v1.1.2) uses `Frac` BigInt rationals, a fraction-free
Krylov minimal polynomial over exact BigInt matrix powers, and a hybrid that returns
`[charpoly]` directly for non-derogatory matrices (avoiding Smith-form coefficient
swell) and runs the Smith normal form only for derogatory ones — so min-poly and the
flags compute at any size, with only the full factor *list* for very large
derogatory matrices deferred.

## Parity with the Python backend

The browser tool and the `matrix_plates` Python package implement the same operator
algebra over the same seed registry, including a **bit-exact** `mulberry32` PRNG, so
a given `(construction, seeds, params, RNG seed)` tuple reproduces the same matrix
in both. Both compute the exact rational **minimal polynomial**, **invariant
factors**, and the **similarity verdict** (the Python package additionally exposes a
headless CLI and the JSON/LaTeX/SymPy/HTML exporters); the patched tool was
validated against the backend on a 14-matrix exactness battery and a 378-matrix fuzz
(see [`docs/HTML_EDITS.md`](../docs/HTML_EDITS.md)). For the package and CLI see the
top-level [`README.md`](../README.md); for the module map see
[`../src/matrix_plates/README.md`](../src/matrix_plates/README.md).

## Troubleshooting

- **Nothing happens / no plates** — press **Seed batch** (or **Press plate** with a
  construction selected). The sheet is empty until you generate something.
- **Custom matrix rejected** — entries must be integers and the grid must be square;
  the tool reports the exact offending cell or shape. This system works over ℤ — use
  a `Companion` / `Cartan` / … construction for algebraic (irrational) seeds.
- **`↦ companion seed` is disabled** — the lift needs a monic integer characteristic
  polynomial; non-liftable plates leave the button inactive.
- **The Mahler axis "starts" empty on the left** — that is intentional: the floor is
  pinned at `M = 1` and the `(1, Lehmer)` band is shaded to keep the conjecturally
  empty gap visible, never auto-scaled to the data minimum.
- **The root plot smears near a double root** — eigenvalue *positions* and `M`/`ρ`
  are floating point; the polynomial chips (char-poly, minimal polynomial, invariant
  factors, det, tr, rank) are exact — trust those.

## See also

- [`../README.md`](../README.md) — the package, CLI, and exactness boundary.
- [`../docs/README.md`](../docs/README.md) — index of the design docs.
- [`../docs/DESIGN.md`](../docs/DESIGN.md) — the plates / companion-closure metaphors.
- The repo's other exact-arithmetic pipelines and the full
  [live site](https://echo-s-studios.github.io/math-research-pipelines/) — see the
  top-level [`README.md`](../../README.md).
