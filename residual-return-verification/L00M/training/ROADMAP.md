# `training/` — roadmap

The lightweight-local-training package (see `README.md`). Records the **active direction** and the
**preserved alternatives** — deferred, *not dropped*. Each remains a real, scoped next thrust.

## Status — package COMPLETE + growth PRINCIPLED + A3.P2 (Fisher + threshold) SHIPPED

**A1 (learner) + A2 (cross-field bridge + growth) + A7 (anomaly detector) + a runnable demo + A3.P0+P1
(the Northcott capacity gate) + A3.P2 (Fisher + exact threshold)** are shipped on L00M `main`. The
substrate reads a residual and, under propose-for-confirm, grows the exact model to capture it — in-field,
then off-field — with a calibration-gated anomaly detector on top. As of **A3.P0+P1, growth is
principled**: the decision is the **derived, exact, Northcott-finite** `capacity_decision`
(GROW/STOP/REJECT), which **retired the tuned persistence/height heuristic and `HARD_DEGREE_CAP`**.

**A3.P2 is now SHIPPED (no longer deferred research):**

- **A3.P2a — Fisher (`d526098`).** `‖r‖²_G = n·Fisher(r)` on the trace-zero (residual) subspace.
- **A3.P2b — exact threshold (`c5605d7`).** The GROW threshold as information gain (`‖r‖²_G`) vs cost
  (`λ·log M(θ)`), with the provable Smyth/Lehmer floor.
- **F4 is RESOLVED — as a *synthesis of classical facts*, not a settled open problem.** The trace form
  **is** the Fisher metric of two natural models: `G = MᵀM` is the Fisher information of a Gaussian
  location family `N(Ma,I)` (Amari) — itself textbook ANT (`G = MᵀM`, `det G = d_K`, Neukirch/Marcus) —
  and `n⁻¹G` on the residual subspace is the Fisher of the max-entropy family on the conjugates. The
  contribution is the **assembly** + pinning the **model-dependent conformal constant** (`c = 1` Gaussian
  vs `c = n` max-entropy) + the residual-norm-as-information-distance reading. Honest caveats kept
  first-class: no canonical model (Čencov: Fisher is unique up to *scale*, so the `c` ambiguity is a
  model+scale choice); and the cost floor is unconditional only for **non-reciprocal** seeds (Smyth μ_S);
  reciprocal seeds are the unsolved Lehmer core (Dobrowolski → 1, not uniform).

**Also shipped this line of work:**

- **Research paper** — `paper/vector_substrate.{tex,pdf}` (29pp, vendored tectonic; probe-backed by
  `test_paper_claims.py`): the Vector Substrate thesis (vector space / matrix algebra / lattice, glued by
  `G = MᵀM`), the information geometry as a synthesis, the height/capacity gate, and the growth threshold.
- **Degree-aware Lehmer capacity gate** — `capacity.capacity_decision`'s **opt-in, default-off**
  information-threshold path: `floor = (n if degree_aware else 1)·λ·log μ`, cost certified via Landau's
  exact-integer upper bound (root-free, mpmath.iv), gain held exact; Smyth μ_S for non-reciprocal seeds,
  Dobrowolski for reciprocal (Lehmer μ_L heuristic opt-in only). Default-off is byte-for-byte the shipped
  gate.

## NEXT — P2c is the LIVE in-progress build

- **P2c — non-disjoint compositum** *(IN PROGRESS, this session)*. When a generator's minpoly
  **partially factors over `K`**, the Kronecker-Gram shortcut (`G_W = G_K ⊗ G_L`) is **invalid** — needs
  the **true compositum basis** (resultant / primitive-element, Trager, regime B) + exact Gram/projector
  re-derivation; extends `compositum.py`'s REFUSED `non_disjoint` branch into growth. The grow/reject
  decision reuses the **capacity gate** via `capacity_decision(..., effective_degree=)` on the *actual*
  compositum degree (disjointness-independent). Canonical witness: `K = Q(√2)`, adjoin `β = √2+√3`
  (`x⁴−10x²+1` factors over `Q(√2)`), `e' = 2`, true compositum `Q(√2,√3)` degree 4 (**not** the tensor's
  8). The likely real work: extending `coords_to_minpoly`/`invariant_factors` to factor over a number
  field, not just `ℚ`. **Handoff: `NEXT_SESSION_P2C.md`.**

- **B1 — wire the learner into KIRA live** *(DEFERRED, own SEPARATE future session)*. Graduate
  `residual_learner` into the live KIRA host per **`WIRING_MAP.md`**: `/api/training/*` via
  `_vectors_shell`, the `calibration_ok` stub → the real `_emission_allowed()` / `_CalibrationTracker` ECE
  gate, anchors+deltas persistence. Crosses into the **`plate-matrices` branch** (cross-repo, PM-only push
  to `l00m-backup main:plate-matrices`); separately-reviewed.

## Phase ledger (shipped, L00M `main`)

A1 `fea69c4` · A2.P0 `c1db881` · A2.P1 `5a80216` · A2.P2a `75524b3` · A2.P2b `c0b413f` ·
README `c90ff90` · ROADMAP `760125e` · A7 `6ad20eb` · capstone `3c61347` ·
A3_DESIGN `29102cd` · A3.P0 `e6ac495` · A3.P1 `218c02e` · A3.P2a `d526098` · A3.P2b `c5605d7` ·
paper `2785980` · A3.P2b reframe `fba88a4` · capacity gate `c8fdb8a` · ROADMAP refresh `(this commit)`.

A2 (disjoint cross-field learner), A7 (anomaly detector), A3.P0+P1 (principled capacity gate), and
A3.P2 (Fisher + threshold, with the research paper and the opt-in degree-aware Lehmer gate) are
**complete**. Guardrails held throughout; gate at every phase: training green + full L00M suite green +
ZFP 74/74. **P2c is the live next build; B1 is its own later session.**
