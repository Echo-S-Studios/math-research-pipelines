# `web/matrix_plates.html` — the patched interactive tool

This is the reference `matrix_plates.html` with the two build-spec features applied
(all build-spec edits: 13 from v1.0, plus v1.1 — custom-matrix input, an inline companion-form view, and per-plate JSON/LaTeX/SymPy export; and (v1.1.1) an exact BigInt-rational engine that computes the minimal polynomial, invariant factors, derogatory/defective flags, and the companion similarity verdict in-browser — (v1.1.2) made to scale via a fraction-free Krylov minimal polynomial and a hybrid that runs the Smith form only for derogatory matrices (no practical size cap); see [`docs/matrix_plates_build_spec.md`](../docs/matrix_plates_build_spec.md) and [`docs/HTML_EDITS.md`](../docs/HTML_EDITS.md)).
Open it in any browser — it is a single self-contained file with no build step,
no network, and no dependencies.

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

## Parity with the Python backend

The browser tool and the `matrix_plates` Python package implement the same operator
algebra over the same seed registry, including a **bit-exact** `mulberry32` PRNG, so
a given `(construction, seeds, params, RNG seed)` tuple reproduces the same matrix
in both. The Python package adds exact rational **minimal-polynomial** computation
(hence the derogatory / similarity verdict) and a headless CLI; see the top-level
[`README.md`](../README.md).
