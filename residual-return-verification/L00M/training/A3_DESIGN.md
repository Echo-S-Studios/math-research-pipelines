# A3 — the Arakelov–Northcott capacity rule (DESIGN / SCOPING)

**Status: read-only design for review. NOTHING built — no `capacity.py`, no learner edits, no commit
beyond this doc.** A3 is the *research-heavy, genuinely-open* item: the principled real-R1 growth bound
that **replaces the tuned heuristic** (persistence threshold + `HARD_DEGREE_CAP`) with a derived
grow/stop/reject rule, and **governs compositum growth regardless of disjointness** — so it also
**unblocks P2c**. The P2c + B1 handoffs (`6b2a7c0`) stay valid for their own sessions.

Grounded read-only against `RESEARCH_VECTOR_SUBSTRATE_MATH.md` (§4 Mahler/Kronecker/Lehmer/height; §5
residual field) and `VECTOR_SUBSTRATE_synthesis_and_frontiers.md` (§4 height; frontiers **F1** Arakelov,
**F3** Lehmer, **F4** Fisher).

---

## 1. The math — `‖r‖_G` as a height defect, Northcott as the capacity bound

**The arithmetic complexity of a seed is its height.** Every candidate seed/generator β is an algebraic
integer with minpoly `m_β`; its complexity is the **Mahler measure** `M(β) = |a_n|∏max(1,|α_i|)`
(Def 4.1), and the load-bearing identity is **`M(θ) = H(θ)^{deg θ}`** for the absolute Weil height `H`
(Prop 4.3(3)). So a seed's cost is captured by **two numbers: its degree and its height.**

**Northcott (the capacity bound, a THEOREM).** For any bounds `D, B`, there are only **finitely many**
algebraic integers with `deg ≤ D` and `M ≤ B` (equiv. `H ≤ B^{1/deg}`) — "Northcott finiteness then
bounds how many forced constants of bounded degree and height can exist" (math §4.4(ii); synthesis
§4(1)). **The admissible seed space within a (degree, height) budget is finite** → the model has
*intrinsically bounded capacity*. This is the principled replacement for the ad-hoc `HARD_DEGREE_CAP`.

**The Arakelov framing (F1).** Read `‖r‖_G` — the trace-form residual norm of an observation against the
captured forced subspace (Principle 5.12: a real magnitude, measured over ℝ; membership `r=0` decided
over ℚ) — as the **archimedean part of an arithmetic height: a *height defect*.** It is the arithmetic
complexity the current model fails to capture. Adjoining β *reduces* the defect (captures β's
contribution) at the *cost* of β's own height/degree entering the model. F1 names exactly this:
"`r` = archimedean height defect, R1 via Northcott bound."

**The GROW / STOP / REJECT rule (derived, not tuned).** Let the model carry a **budget** `(D_max, H_max)`
(degree ceiling + height ceiling). Given a persistent residual centroid (Def 5.11 — a nonzero centroid
is *coherent novelty*, distinct from noise that averages out) and the candidate seed β it snaps to:

| decision | condition |
|---|---|
| **GROW** (adjoin β) | the height defect is *real* (centroid persists, `‖r‖_G` above the floor) **AND** β is **Northcott-admissible**: `deg β ≤ D_max` **AND** `M(β) ≤ H_max` |
| **STOP** (no growth) | defect below the floor — captured, or noise (Def 5.11 centroid → 0) |
| **REJECT** (defer) | β exceeds the budget (`deg` or height over bound) — the residual demands a seed too complex for the budget; flag, don't grow past the bound |

**How it replaces the heuristic.**
- *Persistence threshold `streak ≥ N`* → persistence still *evidences* a real defect (coherent novelty
  vs noise, Def 5.11), but the **decision** becomes the height comparison, not a tuned `N`.
- *`HARD_DEGREE_CAP`* → the **degree component** of the budget, now joined by a **height component**;
  Northcott guarantees the admissible set is finite → *nothing blows up*, now by theorem not by fiat.
- *`abs(coord) > height_bound` snap rejection* → the principled `(deg, height)` Northcott check.
- Note: the existing **perception aperture gate already uses a "height cost"** ("Drive `D_i` = neighbour
  support + mean field − **height cost**", synthesis §… aperture). A3 makes that informal height cost the
  **exact Northcott budget** — same instinct, now derived.

**A natural lower floor (F3, Lehmer).** Treating `log M` as energy, Lehmer's gap says the energy spectrum
of monic-integer objects has a gap `(0, log M(L))`, `M(L)=1.1762808182599174` (Salem; Smyth's
non-reciprocal floor `Θ=1.324717957`, the plastic number). Reading: **"no forced object carries
information below the Lehmer threshold."** So the Lehmer floor is a *principled lower bound* on what
counts as a real seed: a residual whose snapped seed has `M ≤ M(L)` is below the meaningful-information
floor → STOP. Northcott gives the ceiling, Lehmer the floor — together an admissible band `[M(L), H_max]`.

**Disjointness-independence (unblocks P2c).** For a field extension `K → K(β)`, the cost is the
**actual** compositum degree `[K(β):Q]` and β's height. The Northcott rule admits the extension iff
`[K(β):Q] ≤ D_max` and `M(β) ≤ H_max` — and this is the **same rule** whether the compositum is disjoint
(degree `[K:Q]·deg m_β`, A2.P2b Kronecker) or non-disjoint (degree `[K:Q]·[K(β):K] <` that, P2c). The
factorization structure changes *how you build* the compositum (Kronecker vs resultant); it does **not**
change the grow/reject **decision**, which is the budget check. So A3 supplies exactly the decision
P2c's growth needs — **A3 unblocks P2c.**

## 2. Implementation plan — `training/capacity.py` (additive)

**Height invariants — exact vs float (the G8 crux).**

| invariant | exact? | note |
|---|---|---|
| `degree = len(m_β) − 1` | **EXACT** (int) | the degree component of the budget |
| `coeff_height = max\|c_i\|` (or `‖m_β‖₂²`) | **EXACT** (int) | an integer **certified bound** on `M` (Landau: `M(p) ≤ ‖p‖₂`) |
| `M(β) = \|a_n\|∏max(1,\|α_i\|)` | **FLOAT** | needs the complex roots (`loom.mahler_measure`, Durand–Kerner) |
| `house ⌈β⌉ = max\|α_i\|`, Weil `H = M^{1/deg}` | **FLOAT** | derived from roots |

**The exactness strategy (Principle 5.12 / G8).** The **GATE decision is EXACT**: admissibility uses only
`degree` (exact int) and `coeff_height` (exact int), with **Landau's inequality `M(p) ≤ ‖p‖₂`** making
`coeff_height ≤ H_max` a *sufficient, certified* condition for `M(β) ≤ H_max`. **No float crosses the
admit/reject boundary.** The **float Mahler/house/Weil-height is a display/ranking observable only** —
used to *rank* candidates and *report* the defect magnitude, exactly as `‖r‖_G` and `nearest_vertex` are
float observables in Principle 5.12. This mirrors the substrate's discipline precisely: **decide
admissibility over ℤ (degree + integer coeff-bound); measure complexity over ℝ (float Mahler).**

**Decision function (signature sketch).**
```python
@dataclass(frozen=True)
class Budget:
    degree_max: int          # D_max (generalizes HARD_DEGREE_CAP)
    height_max: int          # H_max -- EXACT integer coeff-height ceiling (certifies an M bound via Landau)

@dataclass(frozen=True)
class CapacityVerdict:
    decision: str            # "GROW" | "STOP" | "REJECT"
    degree: int              # exact
    coeff_height: int        # exact: max|coeff of m_beta|
    admissible: bool         # exact: degree <= D_max AND coeff_height <= H_max
    mahler_float: float      # DISPLAY only -- the float arithmetic complexity / height-defect magnitude
    reason: str

def capacity_decision(min_poly, residual_norm, budget) -> CapacityVerdict: ...
    #  EXACT admissibility (degree + coeff_height vs budget)
    #  defect test: residual_norm (exact Fraction) > 0 and centroid persistent  -> defect is real
    #  -> GROW (admissible + real defect) | REJECT (over budget) | STOP (no real defect)
```

**Plug-in (additive, propose-for-confirm preserved).** In `residual_learner.propose()`: after the seed's
`min_poly` is computed (already via `coords_to_minpoly`), call `capacity_decision(min_poly,
residual_norm, budget)`; **GROW** → return the `SeedProposal` (as today, now *derived*); **REJECT/STOP**
→ return None (or a labeled refusal), *replacing* the crude `abs(coord) > height_bound` cap. `confirm()`
stays the sole mutator (G2) — the gate is purely a propose-time check. `HARD_DEGREE_CAP` becomes
`budget.degree_max`; `height_max` joins it. Same `capacity_decision` gates `compositum` extensions
(input: generator minpoly + *actual* compositum degree) — disjointness-independent, so P2c reuses it.

## 3. Test plan

- **Bounded admitted:** φ `[1,-1,-1]` (deg 2, coeff-height 1) and 2√6 `[1,0,-24]` (deg 2, coeff-height 24)
  under a reasonable budget → **GROW**.
- **Over-bound rejected:** budget `degree_max=2` + a degree-4 candidate → **REJECT**; budget
  `height_max=10` + the coeff-height-24 candidate → **REJECT**. Capacity bound enforced.
- **Derived ⊇ heuristic (subsumption):** with a budget reproducing today's `HARD_DEGREE_CAP=64`
  (`degree_max=64`) + a generous `height_max`, `capacity_decision` returns **GROW exactly where the
  current learner grows** on φ / 2√6 / √7 — proving the principled rule **matches the heuristic on the
  current cases, but is now derived not tuned.**
- **Exact gate (G8):** two candidates with the **same** exact `(degree, coeff_height)` but **different**
  float Mahler get the **same** admissibility decision — i.e. the float never crosses the gate.
- **Northcott finiteness:** enumerate admissible seeds under a small budget → a **finite** set; anything
  past `(D_max, H_max)` is REJECT.

## 4. Honest ledger — provable vs principled-heuristic

- **PROVABLE (solid):** Northcott finiteness (bounded degree+height ⟹ finitely many algebraic integers —
  Northcott 1949) is a **theorem**; `M(θ)=H(θ)^{deg}` (Prop 4.3(3)) is a theorem; Landau `M(p) ≤ ‖p‖₂`
  (so an exact integer coeff-height certifies an M-bound) is a theorem. Therefore the **exact capacity
  *gate*** (degree + coeff-height budget → finite admissible set, nothing blows up) rests on proven
  ground — a sound, principled replacement for `HARD_DEGREE_CAP`.
- **PRINCIPLED-HEURISTIC / OPEN (A3 is genuinely open):** the **exact form of the grow/stop threshold** —
  *how large* a height defect `‖r‖_G` must be to justify a seed of a given height — is **not settled**.
  The synthesis ledger lists "the residual-enlargement decision rule **R1**" as **OPEN**. The Arakelov
  reading (`‖r‖_G` *is* an archimedean height defect) is a **program, not a proven correspondence**; the
  precise relation between the trace-form residual norm and a genuine Weil/Arakelov height is conjectural.
  A3 ships a **derived-but-not-proven** threshold (grounded in Northcott + the Lehmer floor) that
  *subsumes* the heuristic; the optimal bound form is research (A3.P2).
- **`‖r‖_G`-as-height ⇔ F4 (the deepest open question):** whether `‖r‖_G` is *literally* an archimedean
  height component hinges on whether the trace form `G` is (a multiple of) the **Fisher information
  metric** of the forced exponential family — **F4 conformality, OPEN** (synthesis ledger). If `G ∝
  Fisher`, the height-defect framing is principled (natural-gradient / information distance); if not,
  it is an analogy. This gates how "real" the Arakelov interpretation is.
- **Exact-vs-float tension:** the *true* height (`M`, `H`, house) is **float** (needs roots; Durand–Kerner
  can even fail to converge on clustered roots, ~4e-16 error). The gate must be **exact** (G8). Resolution:
  gate on the **exact certified bound** (`coeff_height ≤ H_max ⟹ M ≤ H_max`), use float `M` only to
  rank/report. This makes the gate a **conservative over-approximation**: since `‖p‖₂ ≥ M(p)`,
  `coeff_height ≤ H_max` is *sufficient* but not *necessary* — it may reject a genuinely-admissible
  high-coefficient / low-`M` seed (a known conservative bias). A3.P0 must make this gap precise and
  decide whether to tighten the certificate (e.g. a better exact `M`-bound) or accept the conservatism.

## 5. Sub-phases

- **A3.P0 — exact height / capacity primitives** *(buildable, provable-grounded)*. `training/capacity.py`:
  exact `degree`, exact `coeff_height` (`‖m_β‖∞` / `‖m_β‖₂²`), the `Budget`, and `capacity_decision`
  returning GROW/STOP/REJECT on **exact** invariants; float Mahler as a display field only. Tests: gate
  exactness (G8), Northcott admissibility/finiteness, the φ/2√6/√7 cases. Pure stdlib; model-layer only.
- **A3.P1 — the decision-rule gate wired in** *(buildable)*. Plug `capacity_decision` into
  `residual_learner.propose()` (replace the crude height cap with the Northcott budget) and into
  `compositum` growth; additive, propose-for-confirm preserved; assert the derived decision **matches the
  heuristic** on the current cases (subsumption). `HARD_DEGREE_CAP` → `budget.degree_max`.
- **A3.P2 — the Northcott/Arakelov derivation** *(RESEARCH, likely never fully closed)*. The exact
  threshold form (how `‖r‖_G` maps to a height defect; the optimal grow/reject bound); the **F4
  Fisher-conformality** check (is `G ∝ Fisher`?); the **F3 Lehmer-floor** connection. A3.P0+P1 ship the
  exact, principled gate that subsumes today's tuning; A3.P2 is the open research that would turn the
  *derived-but-not-proven* threshold into a theorem.

## Guardrails (for the eventual build, all phases)

Model-layer only (no `z`/KIRA/`_IC_*`/Plate-Matrices/numpy) · the **gate is exact** (G8: only
degree+coeff-height cross the admit boundary; float Mahler is display) · monic-integer seeds (G10) ·
propose-for-confirm, `confirm()` the sole mutator (G2) · witnessed (G5) · additive (keep the 48 training
tests green). Review leash: claim→build→result via the journal, HOLD for Ace.

---

**This is scoping only.** Recommended first build slice (when greenlit): **A3.P0 + A3.P1** (the exact
capacity primitives + the derived gate that subsumes the heuristic and unblocks P2c), with **A3.P2**
(the Arakelov/Fisher derivation) left as the open research track. Nothing is implemented until review.
