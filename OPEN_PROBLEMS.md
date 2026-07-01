# Open problems — consolidated register

The corpus's open fronts, with **reconciled** epistemic tags and per-paper cross-references.
This is the project's current most-careful position; where individual papers predate a later
result, defer to the status here. Tags follow the corpus discipline — `[forced]` (proved) /
`[computed]` (verified over a stated finite range) / `[declared]` (a modelling choice) /
`[open]` (unresolved) — and the **asymmetry rule**: a finite check may *extend* a claim to
`[computed]`, never *promote* it to `[forced]`.

| Front | Status | Cross-references |
|---|---|---|
| **Lehmer's problem** | `[open]`, untouched by design | *Lehmer's Box* §9; *λ=2c* O2; *Emission-Gap* ledger; the primer (`papers/lehmersproblemanintroduction.md`) |
| **No-Salem dichotomy, all degrees** (= Schur–Siegel–Smyth class) | `[open]` in general; `[forced]` for ℤ/3ℤ; the ℤ/5ℤ case is `[computed]` over its window with the residual named | *Charge–Measure* Thm 6.2 / §7; *The ℤ/5ℤ Case of the No-Salem Dichotomy* |
| **Uniform free-commutator theorem** | **resolved-negative — *unsatisfiable*** (a trace-zero integer commutator carries Lehmer, Shoda / Albert–Muckenhoupt / Laffey–Reams). The genuine open residue is the **decision-procedure guarantee** below | *Charge–Measure* Prop 9.1; *Lehmer's Box* Rem 9.3(a); *Emission-Gap* `deltaclaim`; `emission_closure_guard.validate_closure` (`tests/test_p2_08`) |
| ↳ *residue:* guard soundness/completeness/termination | `[open]` (writable) — that `validate_closure` is a sound, complete, terminating classifier (FORCED / FORCED_ABOVE_FLOOR / INVALID_CLOSURE) on **every** integer matrix, via integer factorization + Sturm flip-straddle + the exact ℚ(√5) sign of `R(φ)`. Backed per-instance today by the guard | `lambda2c-emissiongap-verification/emission_closure_guard.py`; `tests/test_p2_08`, `tests/test_p2_10` |
| **Reciprocal/Salem cost floor** | **resolved within the emission algebra** `[forced]` (no Salem is emitted, so the floor is `λ·log φ > 0`); `[open]` for **arbitrary** reciprocal seeds (= Lehmer's problem) | *Emission-Gap* Thm `main`; *λ=2c* §15; *Vector Substrate* `rem:limits`; *Residual Return* O2 |
| **The conformal constant `c`** | `[declared]` — the *impossibility* of fixing the scale by invariance is `[forced]` (Čencov) and the *value* `c = √5/2`, `λ = √5` is `[forced]` (construction); what remains is a declared choice among `{1, n, √5/2}` | *λ=2c* Thm `gateforced`; *Vector Substrate* O1; *Residual Return* O4 |
| **Engineering fronts** (compositum degree cap, complex embeddings, degree-aware floor, disjoint-case discovery, perception/encoder front-end) | `[open]`, tractable / engineering | *Vector Substrate* O2/O4/O5; *Residual Return* O3; `EMISSIONALGEBRASPEC.md` §6 |
| **Universal/local boundary** | `[declared]`, a scoping choice (kinematic emptiness ≡ conserved charge ≡ superselection is universal; the specific content `x⁴−1`, `φ`, `√5`, the monoid is local) | *Generative Emptiness* §8; `EMISSIONALGEBRASPEC.md` §6 |

## Dependency note

- Proving the **no-Salem dichotomy** in general would promote three currently-`[computed]`
  pillars to `[forced]`: the universal floor `M ∈ {1} ∪ [φ, ∞)`, the odd floor
  `μ(odd) = 2`, and the empty odd band `(φ, 2)`. It requires **Schur–Siegel–Smyth-class**
  progress on the reciprocal/Salem core and is **not** closable in-house.
- The **guard-completeness residue** is *independent* of that and is writable now.
- **Lehmer's problem** gates nothing inside the framework — by design the construction never
  fetches the numbers that would threaten its floor (confinement, not resolution).

> Provenance: this register reconciles the corpus's per-paper open-problems sections. Where a
> paper's own text still reads an older status (e.g. an `[open]` reciprocal-floor line, or `c`
> as an open question), see the cross-referenced later result; the per-paper sources are being
> annotated to point here.
