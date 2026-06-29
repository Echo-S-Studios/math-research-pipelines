# A3.P2b — the exact-threshold / R1 derivation: how large `‖r‖_G` justifies a seed

**Status: research pass, HELD for review. No shipped code touched** (this doc + the probe
`training/test_a3p2b_threshold.py` only). R1 — *"when does a persistent residual justify adjoining a
seed?"* — is a **research question, not a settled theorem**; this pass lands a **characterized result
assembled from classical pieces** (the Fisher reading of A3.P2a, Mahler/Northcott height theory, the
Smyth/Lehmer floor) **+ exact evidence**, with a **proposed (not applied)** refinement to
`capacity.capacity_decision`. It does not claim to resolve an open mathematical problem. Builds on A3.P2a
(`‖r‖²_G = n·Fisher(r)`) and A3.P0+P1 (the exact Northcott admissibility).

## 1. The information economy — gain vs cost

Capturing a residual buys information; the seed that captures it costs arithmetic complexity. Make both
sides *information* (nats), then compare:

- **GAIN** `= ‖r‖²_G = n·Fisher(r)` (A3.P2a): the degree-scaled Fisher information the residual carries
  — the model improvement from capturing `r`.
- **COST** `= λ·log M(θ)`, with `M(θ) = H(θ)^d` (Mahler = `height^degree`, A3.P0). `log M` is the seed's
  **topological entropy** (Lind–Schmidt–Ward) — its intrinsic description length. `λ` is the exchange
  rate (information price of one parameter).
- **FLOOR (positive only for non-reciprocal).** A positive Mahler floor is a THEOREM **only in the
  non-reciprocal case**: **Smyth's `μ_S = 1.3247…` (plastic number, root of `x³−x−1`) gives `M(θ) ≥ μ_S`
  for non-reciprocal `θ`**, so `log M ≥ log μ_S > 0` there. The **reciprocal case is the unsolved core of
  Lehmer's problem** (Salem numbers, units arise naturally as seeds): no uniform positive floor is proven —
  only Dobrowolski's degree-dependent bound (`→1` as degree grows, NOT uniform) or Lehmer's conjectural
  `μ_L = 1.1763…`. So **the cheapest genuine seed has a strictly positive cost only for non-reciprocal
  seeds**; the worked seeds (`φ`, `2√6`, `√7`) are all non-reciprocal, so their floors are unconditional.

## 2. The derived threshold

```
  REJECT   if  NOT Northcott-admissible   (deg > D_max  or  M > H_max)        [EXACT, A3.P0+P1]
  STOP     if  ‖r‖²_G  <  λ·log M(θ)        (gain does not cover the seed's cost)
                in particular if  ‖r‖²_G < λ·log μ_L   (below the cheapest possible seed)
  GROW     if  Northcott-admissible  AND  ‖r‖²_G ≥ λ·log M(θ)
```

This **refines** A3.P0+P1's `STOP` (which uses `floor = 0`, so *any* nonzero residual passes) with a
**nonzero, seed-dependent threshold**: a residual must carry at least the seed's worth of information,
and at minimum `λ·log μ_L > 0`.

## 3. Per-field evidence (probe, exact gain · float cost)

`λ = 2` (representative), `μ_S = 1.3247…`, `log μ_S = 0.2812…`. Constant floor `λ·log μ_S = 0.562…`.

| case | `n` | GAIN `‖r‖²_G` | seed `M` | COST `λ·log M` | floor (const · deg-aware) | decision |
|---|---|---|---|---|---|---|
| `2√6` (shipped GROW) | 4 | **96** | 24 | `6.36` | `0.56 · 2.25` | **GROW** (96 ≫ all) |
| `√7`  (shipped GROW) | 8 | **56** | 7 | `3.89` | `0.56 · 4.50` | **GROW** (56 ≫ all) |
| tiny off-axis | 4 | `1/10` | 24 | — | `0.56` | **STOP** (`0.1 < 0.56`); *shipped gate GROWs it* |
| sub-threshold | 8 | `1` | 7 | — | const `0.56` ✓ · deg-aware `4.50` | const **passes**, deg-aware **STOPs** |

The shipped GROW cases clear by a wide margin → **the derived threshold SUBSUMES `φ/2√6/√7`.** The
sub-floor rows show where a principled floor would differ from today's `floor = 0`.

## 4. Provable vs conjectural — the honest ledger

- **PROVABLE (theorems):** Northcott finiteness (bounded deg+height ⇒ finite); `M = H^deg`; Landau
  `M(p)² ≤ Σc_i²` (the exact certified `landau_bound_sq`, A3.P0); the **Lehmer/Smyth lower bound**
  (`M ≥ μ_S = 1.3247…` for non-reciprocal `θ` — a theorem ⇒ a *positive* cost floor exists). And A3.P2a
  `‖r‖²_G = n·Fisher(r)` on the residual subspace.
- **CONJECTURAL / model-dependent:** the **exchange rate `λ`** (the information price of a parameter —
  MDL suggests `~2`, BIC `~½ log N`; the exact value for this substrate is *not* derived); the
  **effective floor constant** (`μ_L` Lehmer vs `μ_S` Smyth vs Dobrowolski's degree-dependent bound);
  the gain↔cost framing itself (a principled *model*, not a forced identity). These are where R1 stays
  open.
- **EXACT vs FLOAT (sharpened):** the **admissibility** side is exact (degree + `landau_bound_sq`,
  A3.P0+P1). The **threshold** side is **intrinsically float** — `log M(θ)` is transcendental, so
  `‖r‖²_G ≥ λ·log M` cannot be a pure `ℚ/ℤ` decision. An exact gate would need **certified interval
  arithmetic** on `log M` (Arb-style) to render the comparison a certified rational decision. (The gain
  `‖r‖²_G` stays an exact `Fraction`; only the cost is float.) This is the real boundary: capacity is
  exact, the *information threshold* is not.

## 5. The degree-aware floor (testing the A3.P2a hypothesis)

Because `‖r‖²_G = n·Fisher(r)`, a **constant** floor on `‖r‖²_G` corresponds to a Fisher-significance
threshold of `(λ·log μ_L)/n` — **shrinking with `n`**. So in a high-degree field a residual that is
intrinsically tiny (small Fisher) can still clear a constant floor (the `n` amplifies it) — the gate
grows too eagerly. A **degree-aware floor `n·λ·log μ_L`** keeps the Fisher-significance threshold
*constant across fields*. The probe shows a `gain = 1` that clears the constant floor (`0.56`) but not
the degree-aware floor in `n = 8` (`4.50`).

**Verdict on the current gate.** For the shipped cases (`φ/2√6/√7`, gains `96/56`) the residuals
dominate *any* floor, so **today's `floor = 0` is already correct on those cases.** A principled
refinement is warranted **for robustness**, not for the current outcomes: a `floor = 0` gate will grow
on an arbitrarily small but exactly-off-axis residual (noise that lands on the lattice). A nonzero,
Lehmer-derived, optionally degree-aware floor would `STOP` such sub-threshold residuals.

## 6. The 1 ∈ B caveat (carried from P2a)

The gain identity `‖r‖²_G = n·Fisher(r)` holds **only when `1 ∈ B`** (so `r ⟂_G 1`, trace-zero). `1` is
**not auto-injected**. So the *threshold derivation depends on `1 ∈ B`*: if `1 ∉ B`, the residual can
carry an along-`1` component that is **not** Fisher information, and `‖r‖²_G` overstates the gain. **A
principled gate should condition on (or enforce) `1 ∈ B`** — e.g. inject the constant into the forced
basis, or measure the gain only on the trace-zero component of `r`. This is part of the proposed change.

## 7. PROPOSED follow-up (separate — NOT applied this pass; the shipped suite stays green)

A refinement to `capacity.capacity_decision` (today: `floor = 0`, exact admissibility only):
```python
# PROPOSED (not shipped). Adds the information-threshold; keeps Northcott admissibility exact.
def capacity_decision(min_poly, residual_norm, budget, *, effective_degree=None,
                      ambient_degree=None,            # n -- REQUIRES 1 in B (else the gain reading is invalid)
                      lam=2, mu_floor=MU_SMYTH, degree_aware=True):
    # 1) REJECT if not Northcott-admissible            (UNCHANGED, exact)
    # 2) floor = (ambient_degree if degree_aware else 1) * lam * log(mu_floor)      # Lehmer-derived, > 0
    #    cost  = lam * log(M(min_poly))                                             # CERTIFIED interval (Arb)
    #    STOP if residual_norm < floor  or  residual_norm < cost
    # 3) else GROW
```
Caveats to honor on apply: requires `1 ∈ B`; needs `ambient_degree`; `log` via **certified interval
arithmetic** to preserve a G8-style certified decision; `lam`/`mu_floor` are tunable/conjectural — ship
them as named, documented parameters, not magic constants. **Recommendation:** apply the **degree-aware,
Lehmer-floored** version (it subsumes `φ/2√6/√7` and adds robustness against sub-threshold noise), gated
on `1 ∈ B`, with `log` certified — but only after Ace reviews `λ`/`μ` choices. *Not applied here.*

## 8. Reproducibility + closure

`training/test_a3p2b_threshold.py` asserts: the GROW cases clear the threshold (subsumption); the Lehmer
floor is a positive minimum and changes the sub-threshold decision (shipped `GROW` vs proposed `STOP`);
the degree-aware floor differs from the constant floor; the certified pieces (`landau_bound_sq`,
`is_admissible`) stay exact integers and the gain stays an exact `Fraction`.

**A3.P2b closes A3.P2** (P2a Fisher + P2b threshold). The capacity *gate* (A3.P0+P1) is shipped and
exact; the *information threshold* is now derived and characterized — provable where it can be (Northcott,
Landau, the Lehmer floor), honestly conjectural where it must be (`λ`, the effective floor, the float
`log M`). The principled refinement is **proposed, not applied** — Ace's call.
