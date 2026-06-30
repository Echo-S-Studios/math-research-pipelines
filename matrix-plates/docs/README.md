# `docs/` — design documents index

The reference material behind **matrix-plates**: the metaphors, the full build
spec, the matrix-family field manual, and the auditable record of the edits that
turned the upstream reference tool into the shipped one. For the package overview
and CLI quickstart see [`../README.md`](../README.md); for the module-by-module map
of the backend see [`../src/matrix_plates/README.md`](../src/matrix_plates/README.md);
for the interactive tool see [`../web/README.md`](../web/README.md).

## The documents

### [`DESIGN.md`](DESIGN.md)
The conceptual companion to the spec — what the two metaphors **mean** in
mathematical terms. It defines a *plate* (an exact integer matrix graded by the
entropy `log M` of its spectrum), explains the **companion closure**
`Φ = companion ∘ charpoly` as a canonical spectral representative / retraction /
self-extending algebra of algebraic integers, and walks five worked examples where
the system reveals something genuine: `φ ⊕ φ` (same spectrum, not similar), `√2`
(house and Mahler come apart), the empty Lehmer gap, derogatory ≠ defective, and
`E₈` (structure ≠ small entropy). Ends with an "idea → module" table. **Read this
first** for the why; read the build spec for the how.

### [`matrix_plates_build_spec.md`](matrix_plates_build_spec.md)
The comprehensive specification (544 lines): the mathematical foundations (Mahler
measure and the entropy grading, the cyclotomic floor and Lehmer's problem,
companion matrices / similarity / derogatory matrices), both goals in full (Goal 1
the `log M` layout axis with the floor pinned at `M = 1`; Goal 2 the `Φ` closure
and self-extending registry), the composition argument, the deliverables table,
and the verification checklist. Includes a v1.1 note recording the release's
additions (house, invariant factors / RCF / `is_similar`, the queryable registry,
the bridge, caching, export, and the extra CLI subcommands) and the *Precision*
note that sharpens the colloquial "structured plates hug `[φ, 2]`" framing into
the defensible signal — the empty `(1, L)` band plus discreteness vs scatter. The
authoritative reference for **anyone implementing, extending, or auditing** the
math.

### [`matrix_plates_guide.md`](matrix_plates_guide.md)
The developer field manual (307 lines): a matrix-family → generator cookbook that
maps every construction the tool emits to a concrete computational use and names
the single invariant that steers it — companion (`ρ`, growth-law / sequence
generator), Kronecker (`M`, fractal texture), direct sum (`rank`, multi-voice),
commutator (`tr = 0`, volume-preserving flow), Cartan (`det` / spectrum), circulant
(DFT spectrum), frustrated ring (`det` / `ρ`), random (the null model). Runnable
dependency-free JavaScript throughout, including a `matmul`/`matpow`/`apply`
toolkit (and its BigInt variant for exact terms beyond `2⁵³`). For **users turning
plates into generative content** — no new mathematics assumed.

### [`HTML_EDITS.md`](HTML_EDITS.md)
The change record for [`../web/matrix_plates.html`](../web/matrix_plates.html): the
named, anchor-based list of every edit applied to the upstream reference tool
(13 in v1.0 for Goals 1 and 2, plus the v1.1 / v1.1.1 / v1.1.2 additions — custom
matrix input, the inline companion view, per-plate export, the exact BigInt
rational engine, and the fraction-free hybrid that lifts the size cap). Carries the
**SHA-256 provenance** of both the unpatched reference and the shipped patched file,
and documents how the patched file was validated (`node --check`, a headless-DOM
parity battery against the Python backend and the sympy oracle, including the
378-matrix fuzz). For **anyone auditing what changed and why**.

### [`matrix_plates.html.patch`](matrix_plates.html.patch)
The byte-exact, apply-able unified diff (543 lines, 16 hunks) that reproduces the
shipped tool from a fresh copy of the reference:
`patch -p1 < docs/matrix_plates.html.patch` (or `git apply --check`) against the
unpatched `matrix_plates.html` yields the file whose SHA-256 is recorded in
`HTML_EDITS.md`. You do **not** need this for normal use — the patched file in
`web/` is already finished. The patch exists so the transformation is auditable and
re-runnable. For **reviewers reproducing the build from upstream**.
