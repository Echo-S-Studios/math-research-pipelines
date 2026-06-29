# `training/` — lightweight local training on the Vector Substrate

A small, **exact, fully-local** learning system built on the L00M L0 vector core. It does not fit a
float parameter vector by gradient descent; it reads the **residual `r = x − Px`** of an observation
against a forced basis `B` in the trace-form metric `G`, and — under a gate — **grows the model**:
first a new exact basis direction (in-field), then, when the residual lives *off-field*, a new exact
**field extension** (disjoint compositum). "Capture" (`r = 0`) is the substrate's word for *learned*.
On top sits a streaming **anomaly/novelty detector** — the substrate's cleanest product surface
(residual = novelty). See `demo.py` for the whole story in one runnable script.

Pure stdlib (`fractions`, `math`, `hashlib`, `json`) — **no numpy, no framework**. Reuses the shipped
L0 (`../projector.py`, `../integral_basis.py`); reinvents nothing.

## Modules

| File | Role |
|---|---|
| `residual_learner.py` | **The T5 learner.** `ResidualLearner.observe/propose/confirm/state` — streams observations, reads `r = x − Px` + an exact-Welford residual-field centroid, and grows the forced basis `B` in-field under propose-for-confirm. |
| `coords_to_minpoly.py` | **The exact minpoly bridge (R1).** `coords_to_minpoly(coords, field)` → the exact monic-integer minimal polynomial of a field element, via the largest invariant factor of `xI − M` (Smith normal form). Wired into `propose()`. |
| `invariant_factors.py` | **Vendored SNF kernel** (byte-identical to the corpus artifact). The complete similarity invariant over `Q[x]`; the engine behind `coords_to_minpoly`. |
| `field_extension.py` | **Out-of-field detection.** `WorkingField` declares an exact over-field `W` (product basis, tensor Gram `G_W = G_K ⊗ G_L`); `field_residual(α) = α − P_K α` is `0` iff `α ∈ K`, else flags an extension is needed. Detection only. |
| `compositum.py` | **Disjoint field-extension growth.** `CompositumLearner` grows `K → K(β)` when a flagged out-of-field element persists: `confirm()` captures the new factor, re-derives the projector over `G_W = G_K ⊗ G_L`, and witnesses the extension. Disjoint case only. |
| `anomaly_detector.py` | **Streaming anomaly/novelty detector.** `AnomalyDetector` wraps the learner + detection: scores each observation (in-field + out-of-field novelty), emits a calibration-gated alert, and surfaces persistent novelty as a growth proposal — **propose-only, never auto-acts**. |
| `demo.py` | **Runnable end-to-end showcase.** `run()` walks the whole story: in-field capture → grow → `r=0`; out-of-field `√7` → extend → `r=0`; anomaly stream with the calibration gate suppress→surface. |

## Phase → commit map (all on L00M `main`)

| Phase | What | Commit |
|---|---|---|
| **A1** | T5 `ResidualLearner` (in-field basis growth) | `fea69c4` |
| **A2.P0** | exact in-field minpoly via SNF (`coords_to_minpoly` + vendored `invariant_factors`) | `c1db881` |
| **A2.P1** | wire the minpoly bridge into `propose()` (exact seed; nearest-int = labeled fallback) | `5a80216` |
| **A2.P2a** | out-of-field detection (`field_extension.WorkingField`) + the P2 design | `75524b3` |
| **A2.P2b** | disjoint-compositum growth (`compositum.CompositumLearner`) — completes the A2 cross-field learner | `c0b413f` |
| **A7** | streaming anomaly/novelty detector (`anomaly_detector.AnomalyDetector`) | `6ad20eb` |

**The package is complete: A1 (learner) + A2 (cross-field bridge + growth) + A7 (anomaly detector) +
a runnable `demo.py`** — the complete lightweight local training package.

## Guardrail invariants (hold across every module)

- **Model-layer only** — the learner grows the **model** (basis `B` / the field), and **NEVER** touches
  the perception engine's state `z`; it imports no KIRA server and sets no `_IC_*` (the closed
  perception loop, **G3**, stays closed by construction).
- **Exact (G8)** — `B`, `G`, `P`, `r`, and every membership decision are `Fraction`/`int`; floats are
  rejected and appear only in display fields.
- **Monic-integer seeds (G10)** — every proposed seed / generator is an algebraic integer, validated
  via `coords_to_minpoly` / `_guard_int_monic`.
- **Propose-for-confirm (G2)** — `propose()` only suggests; **`confirm()` is the sole mutator** of the
  model. The anomaly detector never confirms.
- **Witnessed (G5)** — every growth / extension / surfaced proposal is appended to a tamper-evident
  **sha256 hash-chain**.
- **Bounded** — `HARD_DEGREE_CAP` caps the working/extension field degree, so nothing blows up.

## Tests + demo

```
py training/demo.py          # the runnable end-to-end showcase
py -m pytest training/ -q    # the assert-bearing gate
```
48 assert-bearing tests: `residual_learner` 14 · `coords_to_minpoly` 7 · `field_extension` 9 ·
`compositum` 9 · `anomaly_detector` 8 · `demo` 1. Gate at every phase: training green + full L00M
suite green (465) + ZFP 74/74. Each module also has a `__main__` demo (`py training/<module>.py`).

## Pointers

- **`ROADMAP.md`** — the active direction + the preserved alternatives (B1 / A3·P2d / P2c), deferred,
  not dropped.
- **`WIRING_MAP.md`** — how `residual_learner` graduates into the live KIRA host (the `plate-matrices`
  branch): `_vectors_shell` bridge, `/api/training/*` endpoints, the single `_emission_allowed()` /
  `_CalibrationTracker` gate (what the calibration stub becomes), and the anchors+deltas persistence.
- **`A2_P2_DESIGN.md`** — the field-extension design and its math (Lemma 3.2, Prop 3.3, Rem 3.4).

## Deferred (next major thrust — Ace's direction call)

- **B1** — wire the learner into KIRA live (`WIRING_MAP.md` is the spec; cross-repo `plate-matrices`
  branch, separately reviewed).
- **A3 / P2d** — the **Arakelov/Northcott capacity rule**: the principled bound for *when* to grow
  (in-field vs extend vs reject) and *when to stop* — the genuine cross-field R1 open problem; also
  unblocks **P2c** (non-disjoint compositum). Today's heuristic ships behind propose-for-confirm + the
  hard degree cap.
