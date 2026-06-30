# `papers/` — the two companion LaTeX sources

The canonical `.tex` sources for the two papers this package verifies. The prose is **auditable**: every `[FORCED]` (and `[COMPUTED]`) claim tagged here is re-derived in exact arithmetic by a named test in [`../tests/`](../tests/README.md), and the mapping is the table in [the top-level README §5](../README.md#5-the-test-suite--core-equation-per-file).

| Source | Title | Rendered |
|---|---|---|
| [`lambda_2c_paper.tex`](lambda_2c_paper.tex) | *The Exchange Rate λ = 2c: A Conformal Identity, Its Gate, and Its Flip* | 24 pp |
| [`emission_gap_paper.tex`](emission_gap_paper.tex) | *The Emission-Gap Theorem: No Salem Number in the Spectral Image, and the Cost Floor It Forces* | 16 pp |

Both are `\documentclass[11pt]{article}`, author *Echo–Squirrel Research*. The second is explicitly *A Companion to "The Exchange Rate λ = 2c"* and is cited as `[13]` (`\cite{EG}`) by the first.

> **No PDFs are committed.** The PDFs are **build artifacts**, produced from these `.tex` sources by [`../build_pdfs.py`](../build_pdfs.py) (locally, into `../output/`) and by CI (onto the live Pages site). Keeping only the sources under version control means the prose, not a stale render, is the source of truth.

---

## What each paper establishes

### Paper 1 — `lambda_2c_paper.tex` (24 pp)

The growth rule of the residual-return framework adjoins a candidate algebraic direction `r` iff `‖r‖²_G ≥ λ·log M(θ)`, trading explained structure against description length through a single scalar **exchange rate** `λ`. The paper's answer to *"is λ forced or posited?"* is layered:

- **The identity `λ = 2c` is forced unconditionally** (Thm 3.1): the `2` is the inverted `½` of the quadratic Kullback–Leibler term and carries no freedom; the entire residual freedom is the conformal scale `c > 0`, which Čencov's theorem proves cannot be removed by any invariance argument. `σ = 1/(2c) = 1/λ` is the variance reading.
- **The gate is forced** to the golden level `C = 1` (Thm, §8) by two convergent derivations from disjoint premises — the statics (the minimal structure realising the ternary growth decision is degree 2, whose cost-minimal seed is golden) and the dynamics (the golden gate is the terminal firewall image, fixed by the unique self-reproducing **keystone** `R² = R + I`). Hence `c = √5/2` and `λ = √5` are the framework's forced *values*, with `λ = 2c` the universal identity beneath them.
- **The keystone is itself derived, not posited** (Thm 10.3): `φ` is the smallest Perron root of a `2×2` primitive non-negative integer matrix; the integer normalisation `L_4 = 7 = tr(R⁴)` is an invariant of that keystone, whose `R⁴ = [[2,3],[3,5]]` entries are the gate discriminants `{2,3,5} = {F_3,F_4,F_5}`.
- **The gate ladder and trifurcation** (§6): `spec(ad_{R_C}) = {−√(1+4C), 0, +√(1+4C)}`, the growth decision *is* this channel selection, with exactly three valid gates `{1/4, 1/2, 1} → {2, 3, 5}`.
- **The flip** `D = 1 + 4C` (§11): one sign change at `C = −1/4` that simultaneously inverts eigenvalues (real ↔ complex), the field, the trace-form signature (`det G = 4D`: Riemannian ↔ Lorentzian), and the channels. The **gate** (pins a value) and the **flip** (inverts a regime) co-locate at `D = 0`.
- **The reciprocal-seed cost floor is resolved in-system** (§15): the seeds and operations form a finitely generated emission algebra whose image contains no Salem number, so the cost floor is `λ·log φ > 0`, forced and uniform — with the full proofs deferred to the companion paper.

Section map: Introduction; the identity `λ=2c`; Čencov; three canonicalizations of `c`; the gate ladder and trifurcation; the frame-shift canonicalization; the gate is forced; the keystone is derived; the flip `D=1+4C`; gate versus flip; the flip boundary as a handled dynamical state; Kuramoto division of labour; the K-formation seed astride the fold; the second (multiplicative) flip; the emission algebra; computational realization; the epistemic ledger; open problems; and an appendix reproducing the keystone derivation. (`lambda_2c_paper.tex` is 719 lines.)

### Paper 2 — `emission_gap_paper.tex` (16 pp)

The cost floor of Paper 1's rule is positive iff `M(θ)` is bounded away from `1` over everything the construction can emit. The only obstruction is **Salem numbers** — reciprocal units with conjugates on the unit circle, which evade Smyth's non-reciprocal bound and may sit arbitrarily close to `1` as far as Lehmer's problem (open since 1933) is concerned. The paper does **not** resolve Lehmer. It proves a strictly weaker, system-internal statement sufficient for the floor:

> **No Salem number lies in the image of the spectral emission algebra.**

The mechanism is an **angle-confinement invariant** (Thm 3.2): every catalog eigenvalue has argument in `(π/2)ℤ`; the spectral operations `{⊗, ⊕, (·)², minpoly, Φ}` preserve this; so every emitted on-circle eigenvalue is a fourth root of unity — whereas a Salem number's on-circle conjugates are, by irreducibility, *not* roots of unity. The two are disjoint, so the spectral image omits every Salem number and the entire band `(1, μ_S)`; the floor is then `log μ_S > 0` by Smyth, realised at `log φ`.

The theorem appears in four equivalent forms (Mahler, entropy, channel-spectral, metric-signature). The entry-level operators are then closed by relocating the Salem question to a single **trace-down straddle** boundary (`θ + θ⁻¹` totally real with one conjugate past `t = 2`): the circulant is forced with no delta (cyclotomic ⇒ totally-real/CM ≠ Salem signature `(2, m−1)`), and the commutator is upgraded from per-instance to **uniform** by recognising the framework commutator as the **self-action** `ad_R = [R, ·]`, a derivation whose spectrum is the eigenvalue difference set. Real differences live in `K = ℚ(√2, √3, 5^{1/4})`, whose **every** subfield is totally real or signature `(2k, k)`; the only Salem-bearing subfield is `ℚ(5^{1/4})` of degree 4, where Salem measures exceed `φ`. So the floor `log φ` is forced at every size, not checked instance by instance. What honestly remains is the free (non-self-action) commutator at unbounded size and, beyond the system, Lehmer's problem.

Section map: the cost floor and strategy; the emission algebra; the theorem and its four forms; angle confinement; the Salem signature and main proof; the Mahler gap directly; the cost floor; the non-local identity (one gap, four domains); the delta (localizing Salem at the flip); the uniform bound (the self-action is a derivation); the epistemic ledger; and a reproducible-verification appendix. (`emission_gap_paper.tex` is 462 lines.)

---

## Building the PDFs

[`../build_pdfs.py`](../build_pdfs.py) renders both sources into [`../output/`](../output/README.txt):

- `lambda_2c_paper.tex` → **3 `pdflatex` passes** (cross-references plus the `[13]`/`\cite{EG}` citation to the companion paper).
- `emission_gap_paper.tex` → **2 `pdflatex` passes**.

The build runs each paper in a temp directory with `pdflatex -interaction=nonstopmode -halt-on-error`, copies the resulting PDF into `output/`, and reports its size. There is **no bibtex** step — the references are inline. If `pdflatex` is absent the script prints a notice and **exits 0** without failing the run; the test suite does not depend on TeX (see [the top-level README §9](../README.md#9-non-pip-dependencies)). TeX Live's `lmodern` is optional.

## CI and the live Pages site

The repository's [`pages.yml`](../../.github/workflows/pages.yml) workflow compiles **both** of these `.tex` sources (via `latexmk`, which runs as many passes as needed) and publishes them to the now-**live** GitHub Pages site:

- **<https://echo-s-studios.github.io/math-research-pipelines/>** — the landing page, with cards linking to both papers.
- **`/papers/lambda_2c_paper.pdf`** and **`/papers/emission_gap_paper.pdf`** — the compiled PDFs, served directly.

Because the workflow compiles on every push that touches `lambda2c-emissiongap-verification/papers/**`, the rendered site papers always track these sources. The same site also hosts the residual-return PDFs and the interactive Matrix Plates tool; see the [repository README](../../README.md#papers) and the [top-level `papers/` drop-zone README](../../papers/README.md).
