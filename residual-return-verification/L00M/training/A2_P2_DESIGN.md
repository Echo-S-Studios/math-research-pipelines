# A2.P2 — out-of-field detection + field-extension growth (DESIGN / SCOPING)

**Status: accepted scope, phased build under review.** The agreed first slice is the **exact,
bounded, disjoint** path: **P2a** (observation model + out-of-field *detection*, no growth) then
**P2b** (disjoint-compositum *growth* + the √7 confirm test). **P2c** (non-disjoint compositum) and
**P2d** (capacity policy / regime-B abstract-minpoly Trager factorization) are **deferred** — they
merge with the A2.P3 / Arakelov research track and are **not** to be built on this line.

Grounded against `RESEARCH_VECTOR_SUBSTRATE_MATH.md` §3 (Lemma 3.2, Prop 3.3, Def 3.5, Rem 3.4),
readable on the `plate-matrices` branch under `design/` or in `Downloads/Research/`.

## 0. The reframing

A2.P0/P1 grow the basis **inside one fixed field K**. P2 handles the residual that is **off-*field***,
not just off-axis: an algebraic element **not in K** (e.g. `√7` when `K = Q(√2,√3)`). Capturing it
isn't a new column — it's **closing K under multiplication by α**, a **tensor field-extension**
`K → K·Q(α)`. In-field growth adds **1** dimension; field-extension adds **`[K(α):K]`** dimensions.

## 1. The math

**Detection — is the residual element α in K?**

- **(A) Working-field regime (exact, cheap — the build target).** Observations live in a *declared*
  over-field `W`; the captured field `K ⊆ W` is the model. Then **α ∈ K ⟺ α lies in the Q-span of
  K's basis inside W** — exact linear algebra, the *same* projector/residual idea one level up: the
  **field-residual** `α − P_K(α)` (in W's trace form) is `0` iff α ∈ K. Reuses the L0 projector; no
  floats (Prop 2.4: σ injective ⇒ distinct elements, distinct coords).
- **(B) Abstract regime (deferred).** α arrives only by minpoly `m_α`; `α ∈ K ⟺ m_α has a linear
  factor over K`; disjoint ⟺ `m_α` irreducible over K (Lemma 3.2). Needs number-field factorization
  (Trager). **Deferred to P2d/P3.**

**Extension construction — exact, cheap (Prop 3.3), the disjoint case.** If `Q(α)` is linearly
disjoint from `K`:
- `M = K·Q(α)`, degree `d·e` (Lemma 3.2).
- Represent M in the **product basis `{eᵢ fⱼ}`** (not a single-generator power basis); the trace-form
  Gram is the **Kronecker product** `G_M = G_K ⊗ G_L` (Prop 3.3),
  `det G_M = (det G_K)^e (det G_L)^d` (Rem 3.4) — built exactly, no re-tracing in the big field.
- The learner needs basis + Gram + projector, not a generator; `projector_matrix` takes any Gram.

**Worked example (√7), exact:**
- `K = Q(√2,√3)`, product basis `{1,√2,√3,√6}`, `G_K = diag(4,8,12,24)`, `det G_K = 9216 = 2¹⁰·3²`.
- `L = Q(√7)`, basis `{1,√7}`, `G_L = diag(2,14)`, `det G_L = 28`.
- Disjoint: `[K:Q]·[L:Q] = 4·2 = 8 = [M:Q]` (Lemma 3.2).
- `M = Q(√2,√3,√7)`, degree 8, `G_M = G_K ⊗ G_L = diag(8,56,16,112,24,168,48,336)`,
  `det G_M = 9216²·28⁴`.

## 2. How it extends `residual_learner`

- **`observe`** gains a richer intake (an exact element of `W`, regime A). The in-field path is
  unchanged when `x ∈ K`.
- **Out-of-field detection** (`field_residual`): persistent nonzero ⇒ out-of-field candidate.
  Decision rule: **in-field growth iff the new direction closes (adds 1 dim); field-extension iff
  `[K(α):K] ≥ 2`** (adds a whole `Q(α)` slab).
- **`propose`** returns an in-field `SeedProposal` (P1) **or** a `FieldExtensionProposal`.
- **`confirm` (still the sole mutator)** on an extension: build `M` in the product basis,
  `G_M = G_K ⊗ G_L`, **lift every existing seed** `eᵢ ↦ eᵢ⊗1`, **adjoin `1⊗α`**, re-derive
  `P = projector_matrix(B_M, G_M)`. The out-of-field α is now in `M` ⇒ residual → 0. Witness it.

## 3. Guardrails (unchanged posture, bigger mutation)

Model-layer only, exact (Fraction/int), monic-integer seeds, no `z`/KIRA/PM/numpy. A field extension
is a larger, structured mutation → **confirm-only (G2)**, **witnessed (G5)** with
`{kind: field_extension, alpha_minpoly, old_degree, new_degree, disjoint}`. New cheap self-check at
confirm: **`det G_M == (det G_K)^e·(det G_L)^d`** (Rem 3.4). A **HARD DEGREE CAP** bounds the
working/extension degree so nothing blows up.

## 4. Test plan (√7)

1. Learner over `K = Q(√2,√3)` (product basis, `G_K = diag(4,8,12,24)`).
2. Stream in-`K` observations + a persistent `√7` component.
3. Assert **detection**: √7 flagged out-of-field (`field_residual ≠ 0`); in-field path does not fire.
4. Assert **propose** returns a `FieldExtensionProposal` (degree `4→8`, disjoint), not an in-field seed.
5. `confirm()` → `M = Q(√2,√3,√7)`, `G_M == G_K ⊗ G_L == diag(8,56,16,112,24,168,48,336)`,
   `det G_M == 9216²·28⁴`; seeds lifted; `1⊗√7` adjoined.
6. Assert **capture**: √7's residual in `M` → 0 exactly; witness intact + records the extension.
7. Negative: `√6` (already in `K`) detected **in-field**, not an extension.

## 5. Honest hard parts / open questions

1. **Observation representation** — regime (A) (declared working over-field `W`) is the tractable,
   exact target; regime (B) (abstract minpolys) needs Trager factorization — deferred.
2. **In-field / disjointness test** — regime (A) cheap (subspace membership); regime (B) heavy.
3. **Non-disjoint compositum** — Prop 3.3's Kronecker shortcut needs disjointness; partial
   factorization breaks it. **Deferred (P2c).**
4. **Product-basis vs power-basis** — Kronecker Gram is natural in the product basis;
   `coords_to_minpoly`/`companion` assume a single generator. **Represent M in the product basis.**
5. **Unbounded growth / capacity** — each extension multiplies the dimension. The
   extend-vs-in-field-vs-reject decision and a stopping bound are the genuine cross-field R1 problem,
   tied to **Northcott/Arakelov (Frontier F1, A2.P3)**. Ship behind propose-for-confirm with a **hard
   degree cap**; leave the principled bound to P3. **(P2d, deferred.)**
6. **Float-presented observations** — embeddings vs exact elements: LLL/PSLQ = **A2.P3**. P2 stays
   exact (elements presented exactly).

## Sub-phases

- **P2a** — observation model (regime A: working field `W`) + exact out-of-field detection
  (`field_residual`); **detection only, no growth.** ← first build.
- **P2b** — disjoint-compositum growth: product basis + `G_K⊗G_L` (Prop 3.3), seed lift, projector
  re-derive, witness; the √7 test.
- **P2c** *(deferred → P3 track)* — non-disjoint compositum (partial factorization / primitive element).
- **P2d** *(deferred → P3 track)* — capacity/decision policy (Northcott/Arakelov), regime B (Trager).
