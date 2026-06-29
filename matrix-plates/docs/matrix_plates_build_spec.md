# Matrix Plates — Build Spec

### Mahler-measure layout axis · the `charpoly ↦ companion` closure · exact computational backend

> **v1.1 note.** This document specifies the original two goals and the v1.0 backend. Release **1.1.0** extends the system — the matrix *house*, invariant factors / rational canonical form / `is_similar`, a queryable self-extending registry with provenance, an optional NumPy/SymPy bridge, caching, JSON/LaTeX/SymPy export, the `analyze`/`spectrum`/`extend`/`compare` CLI subcommands, and web custom-matrix input + companion view + export. See [`CHANGELOG.md`](../CHANGELOG.md) and the conceptual [`DESIGN.md`](DESIGN.md). The suite is now 133 tests and `verify` runs 10/10.

This spec defines two additions to the Matrix Plates system and the exact
computational backend that implements them:

- **Goal 1** — promote the Mahler measure `M` from a colour to the **layout
  axis**: a one-dimensional spectrum graded by `log M`, with the floor pinned at
  `M = 1` so the Lehmer gap stays visible.
- **Goal 2** — realize `Φ = companion ∘ charpoly` as a **closure** on matrices,
  feeding a plate's exact characteristic polynomial back into the seed registry
  to build its companion (rational-canonical) representative.

The two features are **independent** (ship either alone) but **compose**: because
`Φ` preserves `M`, a lifted companion lands in its source's bin in the spectrum
layout (see [§4](#4-composition)).

The constructions are classical; the contribution is the *pipeline* — read a
plate, lift its exact matrix and invariants, drive the matching generator — and a
backend that computes every invariant exactly, adding the **minimal polynomial**
so the closure can speak precisely about *similarity classes*.

---

## Deliverables

| Deliverable | Location | Role |
|---|---|---|
| Patched interactive tool | `web/matrix_plates.html` | reference tool + the edits below (13 in v1.0; v1.1 adds custom-matrix input, companion view, export) |
| Exact computational backend | `src/matrix_plates/` | stdlib-only Python package |
| CLI | `matrix-plates` console script | `gen / batch / histogram / lift / demo / verify / export` |
| Test suite | `tests/` | 133 tests vs. committed JS + sympy oracles (v1.1) |
| Worked examples | `examples/` | `phi_plus_phi.py`, `mahler_spectrum.py` |
| Field manual | `docs/matrix_plates_guide.md` | matrix-family → generator recipes |

The browser tool and the Python package share the same operator algebra, the same
seed registry, and a **bit-exact** `mulberry32` PRNG, so a `(construction, seeds,
params, RNG seed)` tuple reproduces the same matrix in both.

---

## 1. Mathematical foundations

### 1.1 Mahler measure and the grading

For a monic polynomial `p(x) = ∏(x − αᵢ)` the **Mahler measure** is

```
M(p) = |a_n| · ∏ max(1, |αᵢ|)   =   ∏_{|αᵢ| > 1} |αᵢ|   (monic case).
```

It is the product of eigenvalue magnitudes strictly outside the unit circle (the
*Mahler horizon*). For a monic **integer** polynomial, `log M(p)` is the
topological entropy of the associated `ℤ`-action by an automorphism of a compact
group (Lind–Schmidt–Ward, *Invent. Math.* 101, 1990). Two consequences fix the
axis design:

- Mahler measures **compose multiplicatively** — the `⊗` plate's measure is a
  product of the factors' measures — so the *additive*, uniform axis is `log M`.
- `log M` is the natural entropy coordinate, so binning in `log M` produces
  **equal-entropy buckets**.

### 1.2 The cyclotomic floor and Lehmer's problem

**Kronecker's theorem.** `M(p) = 1` for a monic integer polynomial iff every root
is a root of unity or zero — i.e. `p` is a product of cyclotomic polynomials and a
monomial. So `M = 1` is a hard **floor**, attained exactly by the "cyclotomic"
polynomials.

**Lehmer's problem (open).** The smallest known Mahler measure `> 1` is **Lehmer's
number** `L ≈ 1.17628`, the measure of `x¹⁰ + x⁹ − x⁷ − x⁶ − x⁵ − x⁴ − x³ + x + 1`
(Lehmer, *Ann. of Math.*, 1933). Whether any monic integer polynomial has a
measure in the open interval `(1, L)` is unknown; Lehmer's conjecture asserts the
infimum over non-cyclotomic polynomials is exactly `L`.

**Design consequence.** Pinning the layout's left edge at `M = 1` (never
auto-scaling to the data minimum) keeps the `(1, L)` band visible as deliberate
empty space. With the registry's seeds — all Salem/Pisot/quadratic-irrational,
never cyclotomic — that band is **empty by construction**, and the emptiness *is*
the signal (the "Lehmer phenomenon").

### 1.3 Companion matrices, similarity, and derogatory matrices

The **companion matrix** `C(p)` of a monic degree-`d` polynomial `p` has
characteristic polynomial `p` and is **non-derogatory**: its minimal polynomial
equals its characteristic polynomial. Equivalently, `C(p)` has a single invariant
factor and a single Jordan block per eigenvalue.

Two matrices are **similar** iff they share the same **rational canonical form**,
i.e. the same list of *invariant factors*. The characteristic polynomial is the
*product* of the invariant factors; the minimal polynomial is the *largest*
(last) invariant factor. Therefore:

> The characteristic polynomial is a **complete similarity invariant only for
> non-derogatory matrices** (those with a single invariant factor, i.e. minimal
> polynomial = characteristic polynomial). (Horn & Johnson, *Matrix Analysis* 2e,
> §3.2–§3.3; Gantmacher, *The Theory of Matrices*.)

A matrix is **derogatory** when `deg(minimal) < deg(characteristic) = n` — some
eigenvalue has geometric multiplicity `> 1`. The canonical source is any
`A ⊕ A`: the repeated invariant factor collapses in the minimal polynomial.

### 1.4 The minimal polynomial — definition and exact computation

The minimal polynomial `m_A` is the least-degree monic polynomial with
`m_A(A) = 0`. For an integer matrix it has **integer coefficients** (it divides
the monic integer characteristic polynomial in `ℚ[x]`; Gauss's lemma).

**Exact algorithm (rational Krylov).** Flatten the matrix powers `I, A, A², …`
into vectors of `ℚ^{n²}` and find the least `m` for which `A^m` is linearly
dependent on `{I, …, A^{m−1}}`. The monic dependence

```
A^m + c_{m−1}A^{m−1} + … + c₀I = 0
```

*is* the minimal polynomial. Carrying the elimination in the polynomial basis
recovers `c₀…c_{m−1}` directly, with leading coefficient exactly `1`. Using
`fractions.Fraction` keeps it exact; the result's denominators are all `1`. Cost:
at most `n+1` powers and `O(n)` reductions of length-`n²` vectors → `O(n⁴)`
rational operations. Implemented in `linalg.min_poly`.

This is the quantity the reference tool does **not** compute, and it is exactly
what turns "same spectrum" into a precise statement about similarity ([§3](#3-goal-2--charpoly--companion-closure)).

---

## 2. Goal 1 — Mahler as the layout axis

### 2.1 Rationale

`M` currently drives only `viridis(tFor(p.mahler))` (edge + dot colour).
Promoting it to the layout axis turns the sheet into a `log M` spectrum.

- **Axis is `log M`, not `M`** — entropy units; multiplicative composition
  becomes additive ([§1.1](#11-mahler-measure-and-the-grading)).
- **Floor pinned at `M = 1`** — keeps the Lehmer gap visible ([§1.2](#12-the-cyclotomic-floor-and-lehmers-problem)).
- **Histogram over a plain sort** — sorting shows order; a histogram shows
  *density*, and density is what reveals clustering. The lighter sorted reflow is
  provided as a one-liner ([§2.5](#25-python-api), [§2.8](#28-alternative--sorted-reflow)).

### 2.2 Precision note — what the family separation actually is

The colloquial framing "the structured family clusters in `[φ, 2]` while the
random control scatters right" **overstates the separation** and is worth
correcting precisely (the underlying point survives the correction).

The structured seeds do **not** all sit in `[φ, 2]`. Only the *quadratic units*
(`φ`, `τ`, `√2`) do. Cartan, circulant, and ring constructions have **large**
measures and sit far right, often to the right of a random plate. Here is the
actual seed-batch spectrum (ascending `M`):

| Plate | Family | `M` |
|---|---|---:|
| `C(φ)` | structured | 1.618 |
| `C(K)` | structured | 5.854 |
| `C(φ⁻⁴)` | structured | 6.854 |
| `φ ⊗ √3` | structured | 9.000 |
| `A₅` | structured | 22.392 |
| **`rand·s42`** | **random** | **24.000** |
| `ring∓₆` | structured | 55.713 |
| `E₈` | structured | 177.673 |
| `fib-circ₆` | structured | 170240.000 |

The random plate lands **mid-pack**, with four structured plates to its right. So
the defensible, robust claims are:

1. **The `(1, L)` band is empty** — no integer matrix's characteristic polynomial
   lands there (conjecturally; certainly none of the seeds do). This is the real
   signal, and it is what the pinned floor exposes.
2. **Structured seeds take discrete, characteristic Mahler values** (`φ`, `2`,
   `3`, `5`, `φ⁴`, the Cartan/circulant integers), each tied to its number field;
   **random matrices form a scattered continuum**. The contrast is
   *discreteness vs. scatter*, not *left vs. right*.

The implementation reflects this honestly: the random family is marked (dashed
border / dashed SVG outline) wherever it lands, rather than assumed to be rightmost.

### 2.3 Algorithm and binning

```
B    = clamp(⌈√n⌉, 3, 12)                  # √n rule (between Sturges and Rice; Scott 1979)
hi   = max(maxLogM, log 1.18)              # keep Lehmer (≈1.176) on-axis for tiny galleries
span = hi or 1
k(p) = clamp(⌊ log M(p) / span · B ⌋, 0, B−1)   # log 1 = 0 ⇒ M=1 sits at the left edge
```

Within each bin, plates are sorted by `M` for a clean gradient. Bucketing is
`O(n)`; the worst-case within-bin sort (everything in one bin) is `O(n log n)`.
Bin assignment uses the **exact** `M` (from the integer char-poly), so
near-multiple eigenvalues never perturb it.

### 2.4 HTML edits (applied in `web/matrix_plates.html`)

Anchored to existing functions/markup (not line numbers). Patch map:

| # | Region (anchor) | Change |
|---|---|---|
| 1 | end of `<style>` | spectrum / axis / family CSS |
| 2 | `.console`, after `ctlSeedInt` | `Layout` `<select>` |
| 3 | before `<div class="sheet" id="sheet">` | `<div id="maxis">` ruler |
| 4 | state, after `let uid=0;` | `layoutMode`, `PLATE_NODES`, `familyOf`, `spectrumBins` |
| 5 | replace `addPlate` | unified version that calls `relayout()` |
| 6 | after `recolorAll` | `relayout`, `drawMahlerAxis` |
| 7 | replace `clear` handler | reset node map + axis via `relayout()` |
| 8 | near `gen`/`batch` listeners | wire `#layout` change |

The core of patch 6 (the histogram branch of `relayout`) is the binning above;
`replaceChildren(...nodes)` **moves** existing DOM nodes rather than recreating
them, so each plate's expanded-spectrum canvas state and toggle listener survive
every relayout — no re-`wirePlate`, no re-`drawSpectrum`. An `animationend`
listener strips `.reveal` after the first rise so relayout never replays the
entrance animation.

### 2.5 Python API

```python
from matrix_plates import (Gallery, build_histogram, render_ascii, render_svg,
                           sorted_reflow, comparison_table)

g    = Gallery.seed_batch()
hist = build_histogram(g.plates, max_log_m=g.max_log_m)   # MahlerHistogram
print(render_ascii(hist))                                  # monospaced report
open("spectrum.svg", "w").write(render_svg(hist))          # standalone SVG, tool palette
ranked = sorted_reflow(g.plates)                           # the lighter variant
```

`MahlerHistogram` exposes `bins`, `lo_logm` (always `0.0`), `hi_logm`, `span`,
`m_max`, `lehmer_fraction()`, `lehmer_band_occupants()` (expected empty), and
`bin_of(plate)`.

### 2.6 Edge cases

- **Range growth mid-session.** A new high-`M` plate raises `maxLogM`; `relayout`
  re-bins every plate and `recolorAll` re-grades the gradient (both fire from
  `addPlate`).
- **Single plate / all measures equal.** `hi` is floored at `log 1.18`, so `span`
  is never `0`; one plate lands in bin 0.
- **`M = 1` exactly** (reachable only via a cyclotomic char-poly, e.g. from Goal
  2): `log 1 = 0` ⇒ bin 0, coincident with the floor tick.
- **Huge measures compress the axis.** `fib-circ₆` has `M = 170240` (`log ≈ 12`),
  so the span dwarfs the quadratic units — expected; the spectrum is logarithmic.
- **Root-plot fuzz is irrelevant here.** Binning uses the exact `M`, not the
  plotted Durand–Kerner roots.

### 2.7 Verification

1. Press **Seed batch**, switch **Layout → Mahler spectrum**: `C(φ)` near
   `log 1.618 ≈ 0.48`, the `rand` plate mid-axis (dashed), `fib-circ₆` at the far
   right edge.
2. The axis shows a teal `M=1` floor tick and a gold `Lehmer` tick.
3. The `(1, L)` band is empty (`min M = φ ≈ 1.618`).
4. Toggle back to **Insertion**: original order returns, axis hides, no animation
   replay, expanded spectra stay drawn.

CLI: `matrix-plates histogram --mode spectrum` (and `--svg/--html` to export).

### 2.8 Alternative — sorted reflow

If density isn't needed, the spectrum branch reduces to a single sorted append
(no bins, no axis):

| Mode | Shows | Cost/add | Plate width | Use when |
|---|---|---|---|---|
| Histogram (primary) | clustering + family separation + `M` axis | `O(n log n)` | shared per bin | demonstrating the Lehmer spectrum |
| Sorted reflow | monotone order only | `O(n log n)` | full grid width | you just want plates ranked by `M` |

---

## 3. Goal 2 — `charpoly ↦ companion` closure

### 3.1 Rationale

`analyse` returns the exact monic integer characteristic polynomial as
`p.coeffs`. Feeding it back as a registry seed and building its companion realizes
`Φ = companion ∘ charpoly` on matrices.

- `companion(charpoly(M))` is the **rational-canonical / companion representative**
  of `M`'s char-poly: identical spectrum, `det`, `tr`, `ρ`, `M` — different
  *entries* unless `M` was already a companion.
- `Φ` is **idempotent**: a companion's char-poly is its defining polynomial, so
  `Φ(companion(p)) = companion(p)`. `Φ` is a **retraction** of matrix space onto
  companion matrices (fixed point after one step).
- Companion polynomials are monic, so the lift never leaves the algebraic
  integers — it preserves the registry invariant that excludes the non-monic ZFP
  values. The registry becomes **self-extending**: each lifted plate is a reusable
  seed for `companion` / `⊗` / `⊕` / `[A,B]`.

### 3.2 Precision note — equal char-poly ⇏ similar

"Identity on spectra but not on entries — a clean demonstration of similarity
classes" is right on spectra and is **sharpened** on similarity. `Φ` is the
identity on the *characteristic* polynomial, a complete similarity invariant
**only for non-derogatory matrices** ([§1.3](#13-companion-matrices-similarity-and-derogatory-matrices)). For a **derogatory** input —
any `A ⊕ A` — `Φ` keeps the spectrum but **changes the minimal polynomial**, so
the output is **not similar** to the input. The operation therefore demonstrates
two facts at once:

1. equal characteristic polynomial ⇒ equal `det`/`tr`/`ρ`/`M` (**always**); and
2. equal characteristic polynomial ⇏ **similar** (the derogatory case).

The second point is the sharper "similarity classes" lesson, and the `⊕` operator
produces the witness for free.

| Quantity | Under `Φ = companion ∘ charpoly` |
|---|---|
| characteristic polynomial, spectrum, `det`, `tr`, `ρ`, `M` | **invariant** |
| matrix order / dimension (= polynomial degree) | **invariant** |
| matrix entries | changes (unless input already a companion) |
| minimal polynomial / similarity class | invariant iff input non-derogatory; **changes** if derogatory |
| second application | **fixed point** (identical entries) |

### 3.3 The worked witness — `φ ⊕ φ`

Build `φ ⊕ φ` (Direct sum, Seed A = `φ`, Seed B = `φ`) and lift it:

```
φ ⊕ φ   (derogatory)                companion of (x²−x−1)² = x⁴−2x³−x²+2x+1
⎡ 0  1  0  0 ⎤                      ⎡ 0  0  0 −1 ⎤
⎢ 1  1  0  0 ⎥                      ⎢ 1  0  0 −2 ⎥
⎢ 0  0  0  1 ⎥                      ⎢ 0  1  0  1 ⎥
⎣ 0  0  1  1 ⎦                      ⎣ 0  0  1  2 ⎦
```

Both report `det 1`, `tr 2`, `ρ ≈ 1.618`, `M ≈ 2.618 (= φ²)`, both flagged
`unimodular` — **identical spectral chips, different entries**. They are **not
similar**:

```
min poly(φ⊕φ)      = x² − x − 1            (degree 2)
min poly(companion) = x⁴ − 2x³ − x² + 2x + 1  (degree 4 = char poly)
```

This is the similarity-class demonstration; `φ ⊕ φ` is derogatory and its
companion lift is non-derogatory. (Generated independently in `examples/phi_plus_phi.py`,
asserted in `tests/test_closure.py`, and printed by `matrix-plates demo`.)

### 3.4 HTML edits (applied in `web/matrix_plates.html`)

| # | Region (anchor) | Change |
|---|---|---|
| 9 | `plateHTML`, between `.chips` and `.p-toggle` | `.p-lift` button (`↦ companion seed`) |
| 10 | append inside `wirePlate` | wire `.p-lift` |
| 11 | after the `seedById` derived map | `SIG_TO_ID`, `bySig`, `genCount` |
| 12 | near operator catalogue / console wiring | `liftToSeed`, `refreshSeedMenus` |
| 13 | end of `<style>` | `.p-lift` CSS |

`liftToSeed` validates the char-poly is monic integer, dedupes by polynomial
signature (`coeffs.join(',')`), mints a `p̂ₖ` seed (glyph `p̂` + subscript) only on
a novel signature, registers it (self-extending the *Seed A/B* menus), and builds
`companion(charpoly)`.

### 3.5 Python API

```python
from matrix_plates import Registry, lift, similarity_class_demo, Gallery, build

reg = Registry()                      # self-extending: built-ins + generated p̂ₖ
g   = Gallery()
parent = g.add(build("dsum", a="phi", b="phi"))
res = lift(parent, reg, gallery=g)    # LiftResult
res.spectrum_preserved, res.idempotent, res.similar   # (True, False, False)
res.note                              # "derogatory input: ... NOT similar."

d = similarity_class_demo()           # the φ⊕φ witness, fully compared
d.same_char_poly, d.same_min_poly, d.similar          # (True, False, False)
```

`is_similar_to_companion_lift(plate)` returns `not plate.derogatory` — the crisp
predicate Goal 2 demonstrates.

### 3.6 Edge cases

- **Idempotence / fixed point.** Lifting a companion plate produces a
  byte-identical companion (`Φ∘Φ = Φ`); the button confirms a reused seed.
- **Derogatory input (the feature).** `φ ⊕ φ` → same spectrum, different minimal
  polynomial — not similar ([§3.3](#33-the-worked-witness--φ--φ)). The frustrated ring is another organic
  derogatory case (`ring∓₆` has `min/char = 3/6`).
- **Degree 1.** `[[k]] → x − k → [[k]]`: trivial fixed point.
- **Lifting a built-in companion reuses its own seed.** `C(φ⁻⁴)`'s char-poly *is*
  `x²−7x+1`, the `gap` seed's signature, so the lift reuses `gap` immediately —
  the registry-level fixed point. To *mint* a new seed, lift a matrix with a novel
  char-poly (e.g. `φ ⊕ φ`).
- **Dimension is preserved, not grown.** Companion of a degree-`d` char-poly is
  `d × d`. To build higher-degree algebraic integers, first `⊕`/`⊗` two generated
  seeds, then lift (at the usual `d⁴` analysis cost).
- **Multiple roots stress Durand–Kerner.** Derogatory lifts create repeated roots
  (e.g. `(x²−x−1)²`); the spectrum *plot* may smear. The chips stay exact — trust
  them.
- **Non-monic / non-integer input.** Guarded; the lift refuses anything that is
  not a monic integer polynomial, keeping the registry within the algebraic
  integers.
- **No registry persistence.** Generated seeds live in memory only; re-log the
  source tuple to regenerate.

### 3.7 Verification

1. **Fixed point.** `C(φ)` → **↦ companion seed** → identical `[[0,1],[1,1]]`;
   re-lifting reuses the seed.
2. **Same spectrum, not similar.** `φ ⊕ φ` → lift → the right-hand matrix of
   [§3.3](#33-the-worked-witness--φ--φ); identical chips, minimal-polynomial degrees 2 vs 4.
3. **Self-extending registry.** After a lift, `p̂ₖ` appears in *Seed A/B*; build
   `p̂₁ ⊗ √2` (an `8×8`) to confirm generated seeds feed every binary operator.

CLI: `matrix-plates demo`, `matrix-plates lift dsum --seed-a phi --seed-b phi`.

---

## 4. Composition

`Φ` preserves `M`, so a lifted plate has the **same** Mahler measure as its
source. In **Mahler spectrum** layout the lifted companion therefore lands in its
parent's bin — a direct visual proof that the lift is spectrum-preserving. The
`φ ⊕ φ` demonstration is sharpest here: the derogatory input and its non-similar
companion sit in the **same column** (identical `M`) while differing in entries
and minimal polynomial — "same height on the Lehmer axis, different matrix" made
visible. (Asserted by `tests/test_closure.py::TestComposition` and the
`Compose:` line of `matrix-plates verify`.)

---

## 5. System architecture

Pure-Python, **stdlib only** (no third-party runtime dependency). Module map:

| Module | Responsibility |
|---|---|
| `linalg` | exact integer/rational LA: `matmul`, big-int `matpow`, Faddeev–LeVerrier `char_poly`, rational-Krylov `min_poly`, exact `rank` |
| `roots` | Durand–Kerner complex roots; `mahler_from_roots`, `spectral_radius`, unit-circle classification |
| `prng` | bit-exact `mulberry32` + seeded integer matrices |
| `seeds` | the nine algebraic-integer seeds (monic integer minimal polynomials) |
| `operators` | constructions (`companion`, `kron`, `dsum`, `commutator`, Cartan `A/D/E₈`, `circulant`, `frustrated_ring`, `random`) + `OPS` catalogue + `build` dispatcher |
| `invariants` | `analyse(M)` → full chip set **plus** `minpoly`, `deg_min`, `derogatory` |
| `plates` | `Plate`, `Gallery` (insertion order + running `log M` ceiling) |
| `histogram` | **Goal 1**: binning, `family_of`, `spectrum_bins`, ASCII/SVG renderers, sorted reflow |
| `closure` | **Goal 2**: `Registry`, `lift`, `LiftResult`, `similarity_class_demo` |
| `render_html` | static gallery + spectrum HTML (tool palette), with minimal-polynomial annotations |
| `cli` | the `matrix-plates` command |

**Exactness boundary.** `char_poly`, `det`, `tr`, `rank`, `minpoly`,
`derogatory`, and `unimodular` are **integer-exact**. `mahler`, `ρ`, the
Frobenius norm, and eigenvalue *positions* are floating point (transcendental in
general); the integer chips are authoritative for anything quantitative.

**Testing strategy.** The suite cross-checks the pure-Python core against two
independent oracles committed under `tests/fixtures/`:

- `ground_truth_js.json` — captured by running the reference engine's **verbatim
  JS under Node** (matrices, char-polys, PRNG outputs);
- `oracle_sympy.json` — an **independent sympy** computation (char-poly, minimal
  polynomial, Mahler, `ρ`, `det`, `tr`, `rank`, derogatory flag).

Because both are committed, the suite is stdlib-only at test time (no Node/sympy
needed). `make test` runs all 133 tests; `matrix-plates verify` runs the build-spec
checklist.

---

## 6. Reproducibility and cross-tool parity

Every output is reproducible from the tuple
`(construction, seed A, seed B, type, word, n, RNG seed)`. The only stochastic
source is `mulberry32`, deterministic given its integer seed. The Python port
reproduces every 32-bit truncation (`| 0`, `>>> 0`, `Math.imul`) and the
operator-precedence subtlety in the second mixing step
(`(t + imul(...)) ^ t`, where the `+` is a full-width add coerced back to 32 bits
*before* the XOR). A regression test pins the first eight outputs for seeds 42 and
7 against the Node capture, so any drift from the JS generator is caught
immediately. Result: a tuple regenerates the exact matrix — hence the exact
content — in **either** tool.

---

## 7. Complexity summary

| Operation | Cost |
|---|---|
| `matmul` | `O(n·m·p)` |
| `matpow(A,k)` (exact big-int) | `O(n³ log k)` |
| `char_poly` (Faddeev–LeVerrier) | `O(n⁴)`, integer-exact |
| `min_poly` (rational Krylov) | `O(n⁴)` rational ops |
| `rank` (rational elimination) | `O(n³)` |
| `dk_roots` (Durand–Kerner) | `O(n²)` per iteration |
| `analyse` | `O(n⁴)` + `O(n² · iters)` |
| histogram `build` / relayout | `O(n)` bucket + `O(n log n)` worst case |
| `drawMahlerAxis` | `O(1)` (fixed tick set) |
| `lift` (`Φ`) | `O(d²)` companion fill + `O(d⁴)` analysis |
| signature dedupe | `O(d)` key build, `O(1)` map hit |

The lift adds no asymptotic cost beyond the per-plate analysis it triggers.

---

## 8. Verification matrix

Consolidated expected values (exact unless marked ≈). All are asserted in the test
suite and/or `matrix-plates verify`.

| Object | `det` | `tr` | `M` | `min/char` deg | notes |
|---|---:|---:|---:|:---:|---|
| `C(φ)` `=[[0,1],[1,1]]` | −1 | 1 | ≈1.618 | 2/2 | lift = fixed point |
| `C(√2)` | −2 | 0 | 2 | 2/2 | both roots outside |
| `C(φ⁻⁴)` (`x²−7x+1`) | 1 | 7 | ≈6.854 | 2/2 | unimodular |
| `E₈` (Cartan) | 1 | 16 | ≈177.673 | 8/8 | unimodular |
| `A₅` (Cartan) | 6 | 10 | ≈22.392 | 5/5 | `det = n+1` |
| `D₄` (Cartan) | 4 | 8 | — | — | `det Dₙ = 4` |
| `fib-circ₆` | −170240 | 6 | 170240 | 6/6 | far-right bin |
| `ring∓₆` (frustrated) | 4 | 12 | ≈55.713 | **3/6** | derogatory; `n≡2 (mod 4)` |
| `ring∓₄`, `ring∓₈` (balanced) | 0 | — | — | — | `n≡0 (mod 4)` |
| `ring∓₂` (digon) | 0 | — | — | — | edges cancel → zero matrix |
| **`φ ⊕ φ`** | **1** | **2** | **≈2.618 (φ²)** | **2/4** | **derogatory** |
| `companion((x²−x−1)²)` | 1 | 2 | ≈2.618 | 4/4 | same spectrum, **not similar** to `φ⊕φ` |

Checklist (Goal-flagged) in `matrix-plates verify`: floor pinned at `M=1`; `(1,L)`
band empty; `C(φ)` lift fixed point; `φ⊕φ` equal char-poly but not similar;
degree-1 fixed point; mint-then-reuse (`Φ∘Φ`); generated seed feeds `⊗`; lifted
companion shares the parent's bin. (all checks pass; `verify` is 10/10 in v1.1.)

---

## 9. References

- **Mahler measure = entropy.** D. Lind, K. Schmidt, T. Ward, *Mahler measure and
  entropy for commuting automorphisms of compact groups*, Invent. Math. 101 (1990).
- **Lehmer's problem / the gap.** D. H. Lehmer, *Factorization of certain
  cyclotomic functions*, Ann. of Math. 34 (1933); C. Smyth, *The Mahler measure of
  algebraic numbers: a survey* (2008); D. Boyd, *Reciprocal polynomials having
  small measure*, Math. Comp. (1980, 1989).
- **Cyclotomic floor (`M = 1`).** Kronecker's theorem; see Smyth (2008) for the
  modern statement.
- **Companion / rational canonical form / derogatory matrices.** R. Horn &
  C. Johnson, *Matrix Analysis*, 2nd ed. (2013), §3.2–§3.3; F. Gantmacher, *The
  Theory of Matrices*; Dummit & Foote, *Abstract Algebra* (rational canonical form).
- **Faddeev–LeVerrier.** A. Householder, *The Theory of Matrices in Numerical
  Analysis* (1964).
- **Eigenvalues.** Durand–Kerner / Weierstrass simultaneous iteration.
- **Histogram bin heuristics.** H. Sturges (1926); the Rice rule; D. Scott, *On
  optimal and data-based histograms*, Biometrika (1979).
- **Already in the tool.** Conway & Sloane, *SPLAG* (E₈, unimodular, quantization);
  Davis, *Circulant Matrices*; Bourbaki, *Lie Groups and Lie Algebras* (Cartan
  matrices); Harary (1953) and signed-network synchronization (frustrated ring).
