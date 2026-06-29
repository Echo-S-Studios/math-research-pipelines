# A3.P2a — the Fisher-metric question (F4): RESEARCH findings

**Status: research pass, HELD for review. No shipped code touched** (a verification probe +
this doc only). The corpus lists **F4** — "the information-geometry conformality of trace-form vs
Fisher" — as **OPEN**. This pass resolves it to a **characterized result with exact computational
evidence**, and marks provable vs conjectural precisely. Reproducible probe:
`training/test_a3p2_fisher.py` (sympy, exact). Read-only refs: `RESEARCH_VECTOR_SUBSTRATE_MATH.md`
§2 (Minkowski embedding / Prop 2.4), §4 (Mahler/height), `..synthesis..` F4.

## 0. The question

Is the trace-form Gram `G` (the substrate's metric, in which `r = x − Px` and `‖r‖_G` live) **the
Fisher information metric** of a natural statistical model on the number field — exactly, conformally
(`G = c·Fisher`), or only by analogy? If yes, `‖r‖_G` is an *information distance*, which would justify
reading A3's height-defect threshold information-geometrically (natural gradient).

## 1. The structural fact — `G = MᵀM` (trace form = Minkowski-embedding Gram)

For `K = Q(θ)` of degree `n` with basis `{ω₁,…,ω_d}` and the `n` embeddings `σ_k`, let `M` be the
embedding matrix `M_{ki} = σ_k(ω_i)`. Since `Tr(xy) = Σ_k σ_k(x)σ_k(y)`,
```
G_{ij} = Tr(ω_i ω_j) = Σ_k σ_k(ω_i) σ_k(ω_j) = (MᵀM)_{ij}      i.e.  G = MᵀM.
```
The trace form **is** the pullback of the Euclidean metric under the Minkowski embedding. *Verified
exactly* (sympy) for every test field below.

## 2. Two natural models — and what their Fisher metric is

**Model 1 — isotropic Gaussian location (Minkowski space).** Parameter = field coordinates `a`
(`x = Σ a_i ω_i`); the element is the **mean** `μ(a) = M a` of an isotropic Gaussian `N(Ma, I)` in
`Rⁿ`. The Fisher information of a location family `N(μ(a), I)` is `Jᵀ J` with `J = ∂μ/∂a = M`:
```
Fisher₁ = MᵀM = G        (exactly, for totally real fields).      [PROVABLE]
```
With covariance `c·I` instead of `I`, `Fisher₁ = (1/c) G` — **conformal**, constant `c`.

**Model 2 — the ZFP max-entropy exponential family on the `n` conjugates.** The substrate's own
zero-free-parameter measure is *uniform* on the `n` Galois conjugates (the ignition-cloud `p = 1/N`).
Take the discrete exponential family `p(i; a) ∝ exp((Ma)_i)` over the `n` embeddings, sufficient
statistic = the embedding columns. Its Fisher information at the uniform point `a = 0` is the
covariance of the sufficient statistic:
```
Fisher₂ = (1/n) MᵀM − (1/n²) t tᵀ = (1/n)( G − (1/n) t tᵀ ),   t_i = Tr(ω_i)  (trace vector).
```
The correction `(1/n²) t tᵀ` is **rank-1 along the trace vector** — i.e. along the constant `1`
(`Tr(1) = n`). On the **trace-zero subspace** `{v : tᵀv = 0}`, it vanishes:
```
for tᵀv = 0:   vᵀ G v = n · vᵀ Fisher₂ v        i.e.  G = n · Fisher₂  on trace-zero.   [PROVABLE]
```

**The residual lives there — _when_ the forced basis contains `1`.** The residual `r = x − Px` is
`G`-orthogonal to the forced subspace `B`; **if `1 ∈ B`** then `r ⟂_G 1`, i.e. `Tr(r) = 0`, and
```
‖r‖²_G = n · Fisher₂(r)                                          [PROVABLE, when 1 ∈ B]
```
— **the residual norm IS, up to the explicit constant `n = degree`, a Fisher / information distance.**

> **Caveat (load-bearing).** The learner does **not** auto-inject `1` into the forced basis `B`. So
> `r ⟂_G 1` — hence the Fisher reading — is a **usage convention, true only when `1 ∈ B`.** When
> `1 ∉ B` the residual can carry a nonzero-trace (along-`1`) component and the identity above does not
> apply to it. The exact equivalence `r ⟂_G 1 ⟺ 1 ∈ span(B)` is verified both ways in the probe.

## 3. Exact per-field evidence (all verified by the probe)

| field (basis) | `n` | `G` | `G = MᵀM`? | `Fisher₂` (Model 2) | residual relation |
|---|---|---|---|---|---|
| `Q(√5)` `{1,φ}` | 2 | `[[2,1],[1,3]]` | ✓ | `[[0,0],[0,5/4]]` | `‖√5‖²_G = 10 = 2·Fisher₂(√5)=2·5` |
| `Q(√2,√3)` `{1,√2,√3,√6}` | 4 | `diag(4,8,12,24)` | ✓ | `diag(0,2,3,6) = ¼·diag(0,8,12,24)` | `G = 4·Fisher₂` on `span{√2,√3,√6}` |
| `Q(√2,√3,√7)` (8-dim) | 8 | `diag(8,56,16,112,24,168,48,336)` | ✓ | `diag(0,7,2,14,3,21,6,42) = ⅛·diag(0,56,…)` | `G = 8·Fisher₂` on the residual |

Notes: in the orthogonal-surd bases the trace vector is `t = (n,0,…,0)` (only `1` has nonzero trace),
so `Fisher₂ = (1/n)·G` off the `1`-axis. In the power basis `{1,φ}`, `t = (2,1)` (`Tr(φ)=1`), so the
result is stated on the trace-zero *subspace* `span{√5}` — the relation `G = n·Fisher₂` is
**basis-independent** there. The compositum's `Fisher₂` factorizes with `G = G_K ⊗ G_L` (Prop 3.3),
the conformal constant scaling as `1/n`.

## 4. Honest verdict — provable vs conjectural

**RESOLVED to a characterized result (not a single closed model-free theorem):**

- **PROVABLE (theorem + exact computation):**
  1. `G = MᵀM` exactly (totally real fields). Hence `G = Fisher₁` of the isotropic Gaussian location
     family, **conformal constant `c = 1`** (whole space).
  2. `Fisher₂ = (1/n)(G − (1/n) t tᵀ)`, and on the trace-zero **residual** subspace `G = n·Fisher₂`
     exactly, so **`‖r‖²_G = n · Fisher₂(r)`** — conformal constant **`c = n` (the degree)**.
  3. Both verified exactly on `Q(√5)`, `Q(√2,√3)`, and the compositum `Q(√2,√3,√7)`.

- **CONJECTURAL / MODEL-DEPENDENT (the honest open part):**
  - There is **no unique canonical "the Fisher metric of the substrate."** Two natural models give two
    answers — `c = 1` (isotropic Gaussian, whole space) and `c = n` (ZFP max-entropy exp-family, residual
    subspace). The relationship is conformal-with-an-explicit-constant, but **which model is canonical is
    an interpretive choice**, not forced by the substrate.
  - The clean `G = MᵀM` is for **totally real** fields (all test cases). **Fields with complex
    embeddings** carry the standard `2×` normalization on complex places (the positive-definite companion
    of §2.6); `G = Fisher` there needs that normalization and is **not verified here** — flagged.
  - The `c = n` residual result requires `1 ∈ B` (so `r ⟂_G 1`). **`1` is NOT auto-injected** into the
    forced basis — this is a *usage convention*, not a guarantee; when `1 ∉ B` the Fisher identity does
    not apply to the residual. Verified both ways in the probe: `r ⟂_G 1 ⟺ 1 ∈ span(B)`.

**One-line verdict:** *Yes — `G` is exactly a Fisher information metric for natural models (provably,
computed), and on the residual subspace `‖r‖²_G = n·Fisher`; it is conformal to Fisher with an explicit
model-/degree-dependent constant, not a unique model-free identity. F4's information-geometry reading is
justified, with the constant pinned down.*

## 5. Payoff for A3.P2b (and a proposed — NOT applied — follow-up)

`‖r‖²_G = n·Fisher(r)` on the residual subspace means the height defect that A3.P2b thresholds is, up to
the explicit degree factor `n`, an **information radius** (a natural-gradient step length). So A3.P2b's
rule "*how large must `‖r‖_G` be to justify a seed of height `H`?*" can be posed information-
geometrically: **grow when the information gained (the Fisher distance the residual represents) exceeds
the information cost of the seed (its height/complexity, via the Northcott/Arakelov bound).**

**Proposed (separate, NOT applied this pass; the shipped suite stays green):** when A3.P2b sets the
capacity `floor`, it should be read as a **Fisher/information radius scaled by the field degree `n`** —
i.e. the `c = n` conformal factor is real and *grows with the field*, so a degree-aware floor is more
principled than a constant one. This is a hypothesis for A3.P2b to test, not a change to ship now.

## 6. Reproducibility

`training/test_a3p2_fisher.py` builds the symbolic embedding matrices, computes both Fisher metrics, and
**asserts**: `G = MᵀM`; `Fisher₂ = (1/n)(G − (1/n)t tᵀ)`; `G = n·Fisher₂` on the trace-zero subspace;
the exact `Fisher₂` matrices above; and `‖√5‖²_G = 2·Fisher₂(√5)`. sympy-exact; model-layer only.

**A3.P2b** (the exact-threshold / R1 derivation — how large `‖r‖_G` to justify a seed of height `H`, via
the Arakelov height-defect + Northcott + the Lehmer floor, now informed by `‖r‖²_G = n·Fisher`) is the
**next** sub-phase, not this pass.
