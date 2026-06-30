# SPEC — Building on the Emission Algebra Substrate

*A build specification for a fresh session provisioned with (a) the pipelines you were given and (b) the operator algebra (the λ-ring with two characters). This document provisions structure and laws as ground truth, then gives each use case a **basis → affordance → degrees of freedom → verification bar**. It instructs; it does not constrain. The use cases are foundations to build *from*, not recipes to execute.*

---

## 0. How to read this spec

You are receiving two things and a discipline.

1. **The pipelines** (in this repository): the **residual-return** package (`residual-return-verification/verify.py`; the λ=2c derivation at `residual-return-verification/L00M/training/test_a3p2c_lambda_conformal.py`; the capacity gate `residual-return-verification/L00M/training/capacity.py`); the **λ=2c & emission-gap** package (`lambda2c-emissiongap-verification/`, whose `emission_algebra.py` and `emission_closure_guard.py` are the runnable emission-semiring engine); and the **matrix-plates** package (`matrix-plates/src/matrix_plates/`, the exact ⊕/⊗/Mahler engine — `operators.py`, `seeds.py`, `invariants.py`). Plus the four companion papers (*Lehmer's Box* → `papers/lehmers_box.pdf`; *The Emission–Gap Theorem* → `lambda2c-emissiongap-verification/papers/emission_gap_paper.tex`; *The Occupant of the Salem Slot* → `papers/salem_slot.pdf`; *The Generative Content of a Conserved Emptiness* → `papers/generative_emptiness.pdf`) and the operator-algebra white paper (`papers/operatoralgebrawhitepaper.pdf`), whose laws are machine-checked here by `lambda2c-emissiongap-verification/tests/test_p2_09_emission_algebra.py` and `matrix-plates/tests/test_operators.py`.
2. **This spec**: the verified substrate (§1), the operator API (§2), the constraints that keep you inside it (§3), the use-case bases (§4), the workflow (§5), and the honest boundary (§6).
3. **The discipline**: *scratch the maths yourself, then validate in exact arithmetic.* Every claim below carries an epistemic tag. You may rely on `[forced]`/`[computed]` facts directly (re-derivation still encouraged). You must **derive and validate** `[plausible]`/`[speculative]` claims before relying on them — they are hypotheses, scoped for you, not results.

**Tags.** `[forced]` proved and machine-checked in exact arithmetic · `[computed]` verified to a finite range · `[plausible]` structurally motivated, not yet proved · `[speculative]` a hypothesis worth testing · `[declared]` a modelling/interpretive choice.

**Non-constraint clause.** Where a use case lists "degrees of freedom," those are yours to decide. Where it lists a "verification bar," that is the minimum you must prove before the affordance holds. Between the two, build freely. Do not treat the example encodings as the only encodings.

### Repository map — where the substrate lives

Every fact and pointer in this spec resolves to a real file in this repo. Paths are repo-relative.

| What | In this repository |
|---|---|
| residual-return package · driver | `residual-return-verification/verify.py` |
| capacity / Northcott gate | `residual-return-verification/L00M/training/capacity.py` (tests `test_capacity.py`, `test_capacity_threshold.py`) |
| λ = 2c (derived) | `lambda2c-emissiongap-verification/tests/test_p1_01_identity.py`; runtime: `residual-return-verification/L00M/training/test_a3p2c_lambda_conformal.py` |
| emission semiring engine — cost floor, monoid invariant | `lambda2c-emissiongap-verification/emission_algebra.py` (test `tests/test_p2_09_emission_algebra.py`) |
| closure guard — per-object certificate | `lambda2c-emissiongap-verification/emission_closure_guard.py` (test `tests/test_p2_08_closure_guard.py`) |
| operators ⊕ (`dsum`), ⊗ (`kron`), seed catalog, Mahler measure | `matrix-plates/src/matrix_plates/operators.py`, `seeds.py`, `invariants.py` (tests in `matrix-plates/tests/`) |
| ℤ/4ℤ charge; arg ∈ (π/2)ℤ; no Salem emitted | `lambda2c-emissiongap-verification/tests/test_p2_02_angle.py` |
| ⊕/⊗/ψ² algebra laws (`M(A⊕B)=M(A)M(B)`, `spec(A⊗B)`, `M(A²)`) | `lambda2c-emissiongap-verification/tests/test_p2_01_algebra.py` |
| 27-subfield census; `spec(ad_R)={0,±√5}`; `β₄>φ` | `lambda2c-emissiongap-verification/tests/test_p2_07_uniform.py` |
| ℤ/4ℤ-graded two-route closure (KL_DTA) | `residual-return-verification/kira-language/KL_DTA.py` (test `tests/test_kl_dta_conformance.py`) |
| companion papers + white paper (PDF) | `papers/lehmers_box.pdf`, `papers/salem_slot.pdf`, `papers/generative_emptiness.pdf`, `papers/operatoralgebrawhitepaper.pdf` |
| live, explorable versions | the *Lehmer's Box closure instrument* and the *Emission Algebra compendium* (the two interactive tools on the project site) |

Run order: `make test` (matrix-plates) · `pytest` (lambda2c) · `python3 verify.py` (residual-return).

---

## 1. The verified substrate (ground truth)

These are machine-verified this program. Treat as reliable; re-derive when in doubt.

| # | Fact | Tag | Backing |
|---|---|---|---|
| S1 | **Cost floor.** Each adjunction costs `λ·log M(θ)`; the floor is `λ·log φ` (`λ=2c`, derived). `M(S) ⊆ {1} ∪ [φ,∞)`; the band `(1,φ)` is empty. | `[forced]` | `emission_algebra.py` · `test_p2_03_mahler_gap` · `test_p1_01_identity` · Box §3 |
| S2 | **Conserved charge.** Every root's argument lies in `(π/2)ℤ ≅ ℤ/4ℤ`. The charge is conserved by `⊕, ⊗, ψ²`; the off-charge (Salem) sector is kinematically unreachable — no runtime check needed. | `[forced]` | `test_p2_02_angle` · Gen.Empt. §2; Box §4 |
| S3 | **λ-ring.** `(⊕, ⊗)` is a commutative semiring (`⊗` distributes over `⊕`; identities `∅`, `{1}`). Squaring `(·)² = ψ²` is the Adams operation: a semiring endomorphism, `ψᵐ∘ψⁿ = ψᵐⁿ`, tied to exterior powers by Newton `p₂ = e₁²−2e₂`, equal to the diagonal of `A⊗A = Sym²A ⊕ Λ²A`. | `[forced]` | `test_p2_01_algebra` · matrix-plates `operators.py` · white paper §2–3 |
| S4 | **Character I — magnitude.** Mahler measure `M`: additive on `⊕` (`M(A⊕B)=M(A)M(B)`), intertwines `ψ²` (`M(ψ²A)=M(A)²`), but **tropical** on `⊗`: `log M(A⊗B) = Σ (log\|λ\|+log\|μ\|)⁺`. Its `⊕`-image is the monoid `⟨φ,2,3,5,β²⟩`. | `[forced]` | `test_p2_01_algebra` · `emission_algebra.py` · white paper §4 |
| S5 | **The monoid.** `β² = φ²√5`. Atoms `{φ,2,3,5}` are multiplicatively independent (norms `−1,4,9,25`). **5 atoms, rank 4 → non-factorial**: `β²·β² = 5·φ⁴`. Least generator `φ` (= the floor). Group basis `{φ,2,3,√5}`. Membership is decidable (= factorization). `N(X) ∼ C(log X)⁴` (nowhere dense, exponentially sparse). | `[forced]`/`[computed]` | `test_constants` · `test_p1_09_kform` · `emission_algebra.py` · PSLQ audit · white paper §4 |
| S6 | **Character II — phase.** The `ℤ/4ℤ` charge: **sumset** on `⊗` (`χ(A⊗B)=χ(A)+χ(B) mod 4`), **doubling** on `ψ²` (`χ(ψ²A)=2χ(A)`), **union** on `⊕`. Full group realized only via a Lorentzian seed (`K=x⁴+5x²−5`, its `±iβ` at `±π/2`). | `[forced]`/`[computed]` | `test_p2_02_angle` · `test_p1_09_kform` (K) · white paper §5 |
| S7 | **Self-iteration (the three powers).** From the golden seed: `⊕ᵏ → M=φᵏ` (linear); `(ψ²)∘ᵏ → M=φ^(2ᵏ)` (doubling tower, degree fixed at 2); `⊗ᵏ → M=φ^(Sₖ)`, `Sₖ = k·C(k−1,⌊(k−1)/2⌋)` (super-exponential). Entropy density `log M/deg = ½log φ` is **constant** under `⊕`. | `[forced]`/`[computed]` | matrix-plates `operators.py` (⊕,⊗ iteration) · white paper §7 |
| S8 | **The Adams family.** Every `ψⁿ` is a semiring endomorphism with `χ(ψⁿA)=n·χ mod 4`. Hence `ψ⁴` sends every object to charge 0 (**realification**: keeps magnitude `M⁴`, discards phase); `ψ³ ≡ ψ⁻¹` on charge (**phase inversion**). | `[forced]` | white paper §3 |
| S9 | **The coupling.** `√5 = φ + φ⁻¹` threads the floor (Char I), the self-action grow eigenvalue `spec(ad_R)={0,±√5}`, and the charge. The construction is single-dominant-scale (golden) plus an incommensurable gate spread `{√2,√3,√5}` that cannot unify into one root system. | `[forced]` | `test_p1_02_gate_ladder` · `test_p2_07_uniform` · Occupant §7 (ZFP: separate Plate-Matrices repo) |
| S10 | **Fixed points / idempotents.** `M(ψ²A)=M(A) ⟺ M(A)=1` (cyclotomic locus). `minpoly`, `Φ` are spectrum-preserving idempotents (fix both characters). | `[forced]` | `test_p1_05_keystone` · matrix-plates `canonical.py` · white paper §6 |

**The deep property (orienting, `[forced]`).** This substrate is a complexity measure that is *exact and computable* — the rare third option between Kolmogorov (exact, uncomputable) and statistical MDL (computable, asymptotic). The price is the restriction to a finitely generated algebraic substrate; the dividend is everything in §4. Hold this when choosing what to build.

---

## 2. The operator API

Compute with objects = finite multisets of nonzero algebraic integers (eigenvalue multisets). Three operators, two readouts.

```
OBJECTS        A = {λ₁,…,λ_d}     (eigenvalue multiset of an algebraic-integer matrix)

OPERATORS      A ⊕ B  = A ⊎ B                      deg += , M *= ,  χ  ⊎=
               A ⊗ B  = {λμ}                       deg *= , M tropical, χ sumset
               ψⁿ(A)  = {λⁿ}                        deg fixed, M ↦ Mⁿ, χ ↦ nχ mod 4
               (ψ² = squaring;  ψ⁴ = realify;  ψ³ = phase-invert)

READOUT I      M(A) = ∏ max(1,|λ|)                 magnitude → monoid ⟨φ,2,3,5,β²⟩
READOUT II     χ(A) = {⌊2·arg λ / π⌉ mod 4}        phase → ℤ/4ℤ multiset

GUARANTEES     • any word in {⊕,⊗,ψⁿ} keeps M ≥ φ  (floor never erodes — tropical reason)
               • any such word conserves χ          (Salem/off-charge sector unreachable)
               • membership M(A) ∈ image  ⟺  M factors over {φ,2,3,√5}   (decidable)
```

**Plethysm hooks** (when you need finer structure than `⊗`): `A⊗A = Sym²A ⊕ Λ²A`; `ψ²A` is the diagonal inside `Sym²A`; `tr Λ²A = e₂`. Use these to split a tensor square into symmetric/antisymmetric parts with known traces.

**The design law (your primary knob, `[forced]`).** Three properties are independently tunable:
- **representational dimension (magnitude)** = rank of the monoid = **number of multiplicatively independent seeds**. Add independent seeds → more dimension.
- **the floor** = the smallest seed measure (here `φ`). Pick the seed with the smallest non-trivial measure.
- **the grading** = the angle lattice = **the seed field**. Pick the field to pick the charge group.

You set capacity, floor, and invariant *separately* by choosing seeds, smallest-measure seed, and field.

---

## 3. Constraints (the guardrails — non-negotiable)

Violating any of these voids the guarantees in §2.

1. **Exact arithmetic only.** `sympy`/`fractions` over `ℚ`/`ℚ(√5)`/the relevant field; `mpmath` for high-precision display and roots, never for a decision. **No float crosses a decision boundary.** (The harness bugs this program were *all* float64 round-trips, rounding-before-PSLQ, and the like — see §5.)
2. **Seeds must be algebraic integers with the intended structure.** For the `ℤ/4ℤ` charge you need a Lorentzian quartic contributing `±i` (the role `ℚ(5^{1/4})` plays). A different charge group needs a different field — and the charge group for that field must be **derived**, not assumed (see UC-3).
3. **Stay in the emission semiring for the guarantees.** `⊕, ⊗, ψⁿ, minpoly, Φ` are spectral — their effect on the spectrum is forced, so S1–S2 hold. The **entry-level operators** (commutator `[A,B]`, Cartan embeddings, circulant) are *not* spectral and need separate treatment.
4. **The free commutator is the one door.** By Shoda's theorem any traceless matrix is a commutator, so an *unconstrained* `[A,B]` can carry a foreign object (e.g. a sub-φ Salem) and breaks the field. If your construction uses a commutator, it must be the **self-action** `ad_R = [R,·]` (whose spectrum is forced to `{0,±√5}`) or be guarded by the exact `ℚ(√5)` closure check. Never expose a free commutator without that guard.
5. **Tag everything.** Carry `[forced]`/`[computed]`/`[plausible]`/`[speculative]`/`[declared]` through every claim you add, with a backing check identifier. A claim without a check is not a result.

---

## 4. Use-case specifications

Each is a **basis** (what verified property it rests on), an **affordance** (what it gives), **degrees of freedom** (yours to decide), a **verification bar** (prove this before relying), and a **status**. Build between the freedoms and the bar.

### UC-1 — Bounded-capacity symbolic store / learner · `[tight]`
- **Basis.** Character I (S1, S4, S5). Cost `= λ·log M(θ) ≥ λ·log φ`, composition-rigid by the tropical structure.
- **Affordance.** Exact, **per-step** (not asymptotic) capacity accounting that **cannot be silently inflated by deep nesting**; total cost is a monoid element you can **factor back into generation history**; and because the monoid is non-factorial, a single cost maps to genuinely different histories — a hash with *designed collisions*. Read either as cost-equivalence classes ("same capacity, different path") or as a consistency check (two paths that should agree but don't → an error surfaced).
- **Degrees of freedom.** What you store (any object expressible as an algebraic-integer eigenvalue multiset); the budget; whether to exploit collisions as equivalence or as redundancy.
- **Verification bar.** Confirm your operations are spectral (§3.3); confirm each cost factors over `{φ,2,3,√5}`; confirm your specific composition keeps `M ≥ φ` (it does for spectral words — verify your word is spectral).
- **Status.** `[tight]`, end to end. **Already half-built**: the residual-return capacity gate is this affordance in the wild. Start by reading `residual-return-verification/L00M/training/capacity.py` (with `test_capacity.py`) and the λ=2c derivation (`residual-return-verification/L00M/training/test_a3p2c_lambda_conformal.py`; `lambda2c-emissiongap-verification/tests/test_p1_01_identity.py`), then extend. The cost-floor invariant itself is `lambda2c-emissiongap-verification/emission_algebra.py`.

### UC-2 — Invariant-safe record store (compile-time superselection) · `[tight]`
- **Basis.** Character II (S2, S6) — the charge is a *homomorphism*, conserved by every spectral op.
- **Affordance.** "Illegal states unrepresentable" enforced **by conservation law, not by runtime guards**. The forbidden region (your chosen off-charge sector) is kinematically unreachable: no operation in the semiring can enter it, so there is nothing to check at runtime.
- **Degrees of freedom.** Which invariant you encode as the charge; which sector you designate forbidden.
- **Verification bar.** Prove every operation in your construction is charge-preserving (i.e. spectral, §3.3); prove the free commutator is excluded or guarded (§3.4). If both hold, the invariant holds by S6 with no further check.
- **Status.** `[tight]`. **Already in the wild**: `KL_DTA` carries the graded charge with a two-route (carrier vs matrix) corroboration closure — that grade axis *is* this mechanism. Read `residual-return-verification/kira-language/KL_DTA.py` and its two-route closure (test `residual-return-verification/kira-language/test_kl_dta_conformance.py`), then generalize the invariant. The angle/charge census it rests on is `lambda2c-emissiongap-verification/tests/test_p2_02_angle.py`.

### UC-3 — Configurable safety discipline (charge by field design) · `[plausible]`
- **Basis.** The charge group is induced by the seed field (S2, design law in §2). `ℚ(5^{1/4})` gives `ℤ/4ℤ`.
- **Affordance.** *Designable* invariants — choose the seed field to choose the conserved charge group (and hence which sector is forbidden), tuned to the safety property you want.
- **Degrees of freedom.** The seed field; the target charge group `ℤ/nℤ`; the forbidden sector.
- **Verification bar.** **This is the work.** The `ℤ/4ℤ` result is specific to the angle lattice `(π/2)ℤ` that `ℚ(5^{1/4})` produces. For any other field you must **derive** the angle lattice, prove the charge group, and prove conservation under your operators — do not assume `ℤ/nℤ` transfers. Use the subfield-census route (`nfsubfields` / Sturm signatures) as *Lehmer's Box* did for `K`; the runnable version is `lambda2c-emissiongap-verification/tests/test_p2_07_uniform.py` (the exhaustive 27-subfield census that forces any Salem in `K` to degree 4).
- **Status.** `[plausible]` — the *mechanism* (lattice from field) is structural and general; the *specific charge group per field* is unproven and must be established case by case.

### UC-4 — Structured content-addressing / classification · `[plausible]`
- **Basis.** Two orthogonal characters (S4 + S6): a sparse, factorizable magnitude coordinate and a finite phase label.
- **Affordance.** Address or classify algebraic-data objects by the pair `(factorization over {φ,2,3,√5}, charge multiset)` — a structured coordinate with a rank-4 sparse magnitude part and a `ℤ/4ℤ` phase part.
- **Degrees of freedom.** The addressing/classification scheme; how you use the sparsity (`N(X)∼(log X)⁴`).
- **Verification bar.** The characters are **coarse** invariants. Prove they separate *your* object set adequately before relying on them: non-factoriality (S5) means magnitude collisions exist, and the charge multiset is low-resolution. Measure the collision rate on your data; the addressing is only as injective as you demonstrate.
- **Status.** `[plausible]` — the coordinates exist and are exact; their discriminating power for a given corpus is an empirical question you must answer.

### UC-5 — Tropical computation layer · `[speculative]`
- **Basis.** `log M` on `⊗` is `(max,+)` (S4). The `⊗`-cost landscape is piecewise-linear.
- **Affordance (hypothesis).** A built-in tropical semiring — *potentially* encode shortest-path / assignment / dynamic-programming problems into `⊗`-structure and read the optimum off the measure.
- **Degrees of freedom.** The encoding from a combinatorial problem into objects and `⊗`.
- **Verification bar.** **High.** The tropical structure is `[forced]`; that *useful* problems encode into it is unproven. Before any claim, exhibit one concrete problem (e.g. a small shortest-path instance) whose `(max,+)` solution is recovered exactly by `log M(A⊗B)`, and characterize which problems can and cannot be expressed. Negative results here are information.
- **Status.** `[speculative]`. Pursue only with a worked instance in hand.

### UC-6 — Multi-scale / renormalization-style representation · `[speculative]`
- **Basis.** `ψⁿ` semiring endomorphisms; cyclotomic fixed points (S8, S10). `ψ²` is a scale-coherent zoom (squares magnitude, doubles phase).
- **Affordance (hypothesis).** A multi-scale operator family; iterating `ψ²` gives a `φ^(2ᵏ)` magnitude tower at fixed degree, away from the trivial (`M=1`) locus — a candidate renormalization hierarchy.
- **Degrees of freedom.** Which `ψⁿ` to apply; how to assemble a scale hierarchy.
- **Verification bar.** The endomorphism and tower properties are `[forced]`; the *renormalization interpretation* is not. Show that `ψⁿ`-iteration produces meaningful scale structure for your data, and that the fixed-point locus (cyclotomic) behaves as a stable manifold for your purpose, before adopting the framing.
- **Status.** `[speculative]`.

### Cross-cutting — the Adams knob `ψⁿ` · `[tight]` (existence) / `[plausible]` (utility)
Available to every use case above:
- `ψ⁴` — **realification**: collapse to charge 0, keep magnitude `M⁴`. Use to project out the phase grading when you want a magnitude-only view.
- `ψ³ = ψ⁻¹` (on charge) — **phase inversion**.
- General `ψⁿ` — move between the two characters' resolutions (full phase-graded ↔ magnitude-only) by a controlled, lossy, *reversible-on-charge* operator.

Existence and laws are `[forced]`; whether a given projection is *useful* for your task is `[plausible]` — verify the lossy step preserves what you need.

---

## 5. Workflow (how to build and verify)

**The loop, every time.** (1) Derive the local property by hand (scratch the maths). (2) Encode it as assertions. (3) Validate in exact arithmetic. (4) Tag the result with its backing check. A claim that hasn't been through (3) is not a result — say so.

**Toolchain, matched to the link:**
- symbolic algebra & exact identities → `sympy` (`fractions.Fraction` for rationals);
- high-precision roots / measures for display → `mpmath` (set `dps` high; never decide on the float);
- **number fields** (subfields, Galois groups, signatures) → **PARI/GP** via `cypari2` (`nfsubfields`, `polsturm`, `galoisinit`);
- **integer relations among logs** (membership, independence) → **PSLQ** (`mp.pslq`) — *feed it full precision, never rounded values*;
- semiring identities → exact eigenvalue-multiset products (propagate eigenvalues from the seed; do **not** root-find structured high-multiplicity polynomials).

**Harness lessons (avoid the failures we hit — all were tooling, never the math):**
- float64 round-trips defeat high-precision tolerances → keep roots native (`mp.polyroots`), never `complex(...)`;
- rounding before `pslq` makes it miss exact relations → pass full precision;
- wide BFS over `{⊕,⊗,ψ²}` at high degree OOMs → cap degree / dedup aggressively / enumerate the monoid directly when you only need values;
- a malformed assertion (wrong limit numerator, set-equality on non-canonical forms) reads as a FAIL → when something fails, first suspect the assertion, then the claim.

**Verification bar by tier:** `[forced]` needs a passing exact check; `[computed]` needs the check plus the range stated; `[plausible]` needs the derivation *and* a validating computation before you may rely on it; `[speculative]` needs a worked concrete instance before any claim at all.

---

## 6. The boundary (state it, don't hide it)

- **Internal, not external.** This coherence is real and machine-verified end to end, but it lives *inside* the algebra. The use-classes that fit are ones whose domain can be **encoded as exact algebraic data**: symbolic state, record stores, capacity accounting, invariant enforcement. The moment you need messy perception at intake, you are outside the substrate **by design** — the encoder front-end is the named open front. Do not claim reach you cannot encode.
- **Open fronts (carry forward).** The perception/encoder front-end; the free commutator at unbounded size (handled per-instance, not by one uniform theorem); discovery in the already-disjoint case; and Lehmer's problem itself. The λ-ring recognition explains why the pipelines cohere; **it does not touch Lehmer.**
- **Universal vs local.** The *substrate* (kinematic emptiness ≡ conserved charge ≡ superselection) is a domain-universal pattern. The *content* (`x⁴−1`, the floor `φ`, the graded factorization, the `√5` limit, the monoid) is local to this number theory — theorems here, **not exported engines**. Keep the two on separate pages. The one genuinely portable piece is differential: a 2-to-1 fold has a `√`-branch point generically. `√5 = φ+φ⁻¹` is this construction's own.

---

## 7. Quick reference

**Constants & identities.** `φ=(1+√5)/2` · `√5=φ+φ⁻¹` · `β²=φ²√5=(5+3√5)/2` · `β⁴=5φ⁴` · `φ⁻⁴=(7−3√5)/2=5−3φ` (the bottom grain) · `L₄=φ⁴+φ⁻⁴=7` · `Sₖ=k·C(k−1,⌊(k−1)/2⌋)` (`1,2,6,12,30,60,140,…`) · `N(X)∼C(log X)⁴`.

**Catalog seeds** (polynomial · measure · charge):

| seed | poly | M | χ | role |
|---|---|---|---|---|
| φ | `x²−x−1` | `φ` | `{0,2}` | floor atom / golden self-action |
| τ | `x²+x−1` | `φ` | `{0,2}` | (= φ measure) |
| √2 | `x²−2` | `2` | `{0,2}` | atom |
| √3 | `x²−3` | `3` | `{0,2}` | atom; gate root |
| √5 | `x²−5` | `5` | `{0,2}` | atom; gate root |
| gap | `x²−7x+1` | `φ⁴` | `{0,2}` | trace `L₄=7`; bottom-grain source |
| K | `x⁴+5x²−5` | `β²=φ²√5` | `{0,1,2,3}` | Lorentzian; realizes full `ℤ/4ℤ` |

**Monoid:** atoms `{φ,2,3,5,β²}`, relation `β²=φ²√5`, group basis `{φ,2,3,√5}`, rank 4, non-factorial (`β²·β²=5·φ⁴`), least generator `φ`.

**Operator laws:** `⊕` (deg +, M ×, χ ⊎) · `⊗` (deg ×, M tropical, χ sumset) · `ψⁿ` (deg fixed, M ↦ Mⁿ, χ ↦ nχ mod 4).

**Where to look in this repo:** capacity / cost → `residual-return-verification/verify.py`, `…/L00M/training/capacity.py`, and the λ=2c package `lambda2c-emissiongap-verification/` (`tests/test_p1_01_identity.py`) · emission semiring — floor, monoid, cost → `lambda2c-emissiongap-verification/emission_algebra.py` + `emission_closure_guard.py` (tests `test_p2_09_emission_algebra.py`, `test_p2_08_closure_guard.py`) · operators ⊕/⊗ and the seed catalog → `matrix-plates/src/matrix_plates/operators.py`, `seeds.py`, `invariants.py` · grading / invariant → `residual-return-verification/kira-language/KL_DTA.py` and the angle census `lambda2c-emissiongap-verification/tests/test_p2_02_angle.py` · field / charge derivation → the 27-subfield census `lambda2c-emissiongap-verification/tests/test_p2_07_uniform.py` · the operator laws → the white paper `papers/operatoralgebrawhitepaper.pdf` + `lambda2c-emissiongap-verification/tests/test_p2_01_algebra.py` and `matrix-plates/tests/test_operators.py`.

---

## 8. Minimal reference kernel

A correct, minimal engine. It **provisions the structure**; the application is yours. Do not treat it as the mandated implementation — extend, replace, or re-encode freely, but preserve the laws (§2) and constraints (§3).

```python
# emission_kernel.py — reference engine for the emission algebra.
# Objects are eigenvalue multisets. Exact where it decides; mpmath for the magnitude readout.
import sympy as sp, mpmath as mp
mp.mp.dps = 50
x = sp.symbols('x')
PHI = (1 + mp.sqrt(5)) / 2

# --- seed catalog: name -> integer coeffs (high power -> low) ---
CATALOG = {
    'phi': [1,-1,-1], 'tau': [1,1,-1], 'r2': [1,0,-2], 'r3': [1,0,-3],
    'r5': [1,0,-5], 'gap': [1,-7,1], 'K': [1,0,5,0,-5],
}
def seed(name):                       # -> eigenvalue multiset (object)
    return mp.polyroots([mp.mpf(c) for c in CATALOG[name]], maxsteps=400, extraprec=300)

# --- the three operators (closed on objects) ---
def osum(A, B):  return list(A) + list(B)            # (+)  direct sum
def oten(A, B):  return [a*b for a in A for b in B]  # (x)  tensor
def adams(A, n): return [a**n for a in A]            # psi^n  (sq = adams(A,2))

# --- the two characters (readouts) ---
def measure(A):                                      # Character I  -> R>=1
    m = mp.mpf(1)
    for a in A: m *= max(mp.mpf(1), abs(a))
    return m
def charge(A):                                       # Character II -> Z/4Z multiset
    return sorted(int(mp.nint((mp.arg(a) % (2*mp.pi)) / (mp.pi/2))) % 4 for a in A)

# --- membership: is a measure in the spectrum?  (= factorization over {phi,2,3,sqrt5}) ---
def factor_measure(M, cap=10**6):                    # -> [e_phi, e_2, e_3, e_sqrt5] or None
    basis = [mp.log(PHI), mp.log(2), mp.log(3), mp.log(mp.sqrt(5))]
    rel = mp.pslq([mp.log(mp.mpf(M))] + basis, maxcoeff=cap, maxsteps=10**4)
    if rel is None or abs(rel[0]) != 1: return None
    s = rel[0]
    return [-c // s for c in rel[1:]]

# --- guard: does an object respect the floor? ---
def floor_ok(A, tol=1e-9):
    m = measure(A)
    return m <= 1 + tol or m >= float(PHI) - tol

if __name__ == "__main__":
    G, K = seed('phi'), seed('K')
    assert floor_ok(oten(G, G)) and charge(oten(K, G)) == sorted((p+q) % 4
        for p in charge(K) for q in charge(G))          # sumset law
    assert abs(measure(adams(G, 2)) - measure(G)**2) < 1e-12   # M(psi^2 A)=M(A)^2
    print("kernel ok:", factor_measure(measure(osum(seed('r3'), G))))  # 3*phi -> [1,0,1,0]
```

Everything in §4 builds on this surface. This kernel is illustrative (mpmath); the **exact** engines already exist in this repo over the same seed catalog — `matrix-plates/src/matrix_plates/operators.py` + `invariants.py` (integer-exact ⊕/⊗ and Mahler measure; seeds in `seeds.py`) and `lambda2c-emissiongap-verification/emission_algebra.py` (the cost-floor / monoid invariant). If you need exact (not high-precision) decisions on the field side, reuse those modules directly, or mirror them in `sympy`/PARI per §5.

---

## 9. Decision procedures

Three questions you will ask constantly. All three are decidable; here are the procedures and what each answer licenses.

**D1 — Is a measure `M` in the spectrum?** (membership)
Run `factor_measure(M)`. A return of `[e_φ, e_2, e_3, e_√5]` (non-negative, with the realizability rule: an odd `e_√5` forces `e_φ ≥ 2`) certifies `M ∈ M(S)` and *hands you the factorization*. `None`, or any exponent negative/non-integer, certifies `M ∉ M(S)`. This is exact membership in a complexity class — the property that makes UC-1 and UC-4 possible. (Feed PSLQ full precision — §5.)

**D2 — Is an operator spectral?** (do the guarantees hold)
An operator is spectral iff its effect on the eigenvalue multiset is a fixed function of the inputs' eigenvalues. `⊕, ⊗, ψⁿ, minpoly, Φ` qualify. To test a candidate `T`: prove `spec(T(A,B,…))` is determined by `spec(A), spec(B), …` alone (no dependence on basis/representative). If yes, S1–S2 apply and the floor and charge are preserved. If no — as for a free commutator, where the output depends on the *matrices*, not just their spectra — it is **entry-level**: guard it (§3.4) or exclude it. Never assume; this is the line between "guaranteed" and "needs a separate proof."

**D3 — What charge group does a candidate seed field induce?**
The charge group is the angle lattice of the field's units/roots. Procedure (the subfield-census route *Lehmer's Box* used for `K`, runnable at `lambda2c-emissiongap-verification/tests/test_p2_07_uniform.py`): take the field `F`, compute its Galois closure and group; locate the roots' arguments; the smallest `n` with all arguments in `(2π/n)ℤ` is the charge group `ℤ/nℤ`; verify the operators close on it (`⊗` sumset, `ψ²` doubling stay internal). **Do not port `ℤ/4ℤ` to another field** — `ℤ/4ℤ` is specific to the `±i` that `ℚ(5^{1/4})` supplies. This procedure is the verification bar for UC-3.

---

## 10. Composing the use cases

The use cases share one substrate, so they stack — the two characters are orthogonal, so an invariant discipline and a capacity account run on the same objects without interference.

- **UC-1 ⊕ UC-2 (capacity + invariant, `[tight]`).** Character I bills the construction; Character II keeps it in-sector. Because the charge is conserved by exactly the operators that accrue cost, *every paid step is also a safe step* — no separate enforcement pass. This is the natural default stack and is what the residual-return + KL_DTA pair already approximates.
- **The Adams knob across any stack (`[tight]` existence).** Insert `ψ⁴` to drop to a magnitude-only view (charge 0, `M⁴`) when phase is noise for a sub-task, then resume graded work — the phase grading is recoverable because you never destroyed the magnitude relations. `ψ³` to invert phase. Use `ψⁿ` to move between the two characters' resolutions mid-construction.
- **UC-4 over UC-1's history (`[plausible]`).** Content-address the *cost-equivalence classes* UC-1's non-factoriality produces: `β²·β² = 5·φ⁴` means distinct histories share an address by design. Decide whether that is a feature (dedup) or a collision to break (add a charge coordinate) — verify the separation on your corpus.
- **UC-5 / UC-6 are not yet load-bearing.** Keep them off any stack whose correctness matters until their verification bars (§4) are met. Compose them only in exploratory branches.

**Rule for any stack:** the guarantees compose iff every operator in the stack is spectral (D2). One unguarded entry-level operation anywhere voids S1–S2 for the whole stack.

---

## 11. Extending the substrate (protocol)

To add to the substrate without voiding guarantees, follow the matching protocol. Each ends at a check you must pass.

- **Add a seed.** Choose an algebraic integer; compute its measure and charge (kernel §8). It enters the monoid as a generator: re-run the audit — is it a new independent atom (changes the rank, hence the representational dimension) or a relation (like `gap = φ⁴`, `K = φ²√5`)? *Check:* its measure must be `≥ φ` (else it breaches the floor and is inadmissible), and its arguments must lie in the existing charge lattice (else it changes the charge group — that is UC-3 territory, re-derive via D3).
- **Add an operator.** Run D2. If spectral, prove its action on `M` and `χ` (state the two laws explicitly, as in §2) and confirm it preserves the floor and conserves the charge. If not spectral, you are adding an entry-level operator: specify its guard (the exact-field closure check) and the conditions under which it may fire. *Check:* a passing floor-preservation test on a spanning sample, plus the charge law verified exactly.
- **Add a character.** A new readout is a *homomorphism* `(S,⊕,⊗) → (target)`. Prove it respects `⊕` and `⊗` (and state its `ψⁿ` law). Only then is it a character with the leverage of S4/S6. *Check:* the two homomorphism identities, verified on catalog products and tensors.

Anything that fails its check is not an extension of the substrate — it is a different object, and the guarantees of §1 no longer apply to it. Say so, and tag accordingly.

---

## 12. Failure signatures & acceptance

**Conceptual failure modes** (the §5 list is tooling; these are about the work):

- **Silent substrate exit.** A measure stops factoring over `{φ,2,3,√5}`, or a charge leaves `ℤ/4ℤ`. Signature: `factor_measure` returns `None` for an object you built from seeds. Cause: an entry-level operator fired unguarded, or a non-algebraic-integer slipped in. Treat as a hard stop, not a tolerance issue.
- **Overclaim drift.** A `[plausible]`/`[speculative]` affordance gets cited as established because it "obviously works." Signature: a claim with no backing check, or a check that asserts the conclusion. Re-tag and re-derive; the discipline is the only thing keeping the theory honest.
- **Charge leak.** An operation you assumed spectral wasn't. Signature: `charge(T(A,B)) ≠` the predicted sumset/doubling/union. Cause: failed D2. Guard or exclude the operator.
- **Floor erosion (should be impossible).** If `measure` ever returns a value in `(1, φ)`, you are either outside the substrate or have a precision bug. The floor is `[forced]` rigid under spectral words — so this signature means a constraint (§3) was violated, never that the theorem failed.
- **Reframe-as-mechanism.** Treating a numerical identity (e.g. `5 − 3φ = φ⁻⁴`) as a causal mechanism. State exact identities as identities; reserve "forces"/"generates" for proven implications.

**Acceptance criteria (definition of done), by tier:**

| tier | a build is "done" when… |
|---|---|
| `[forced]` | the property is proved from definitions **and** a passing exact-arithmetic check exists, named by identifier |
| `[computed]` | the above, plus the verified range/degree is stated explicitly |
| `[plausible]` | the derivation is written **and** a validating computation passes **and** the limits (where it might fail) are named |
| `[speculative]` | at least one concrete worked instance succeeds, with the class of cases it does/doesn't cover characterized — negative results recorded, not hidden |

A use-case deliverable is complete when: every operator in it passes D2 (or is guarded), every magnitude claim passes D1, the charge law is verified exactly, the epistemic tags and backing identifiers are present, and the boundary (§6) is stated for the specific build.

---

## Appendix A — Symbols & glossary

| symbol | meaning |
|---|---|
| `φ` | golden ratio `(1+√5)/2`; the floor; least generator of Character I |
| `√5 = φ+φ⁻¹` | the coupling; grow eigenvalue of `spec(ad_R)={0,±√5}`; only irrational ingredient of the spectrum |
| `β² = φ²√5` | measure of the Lorentzian seed `K`; the one non-independent atom |
| `Sₖ = k·C(k−1,⌊(k−1)/2⌋)` | tensor-power exponent; mean-abs-deviation sum of the symmetric binomial |
| `φ⁻⁴ = (7−3√5)/2 = 5−3φ` | the bottom grain (smallest gap among small measures); the gap seed's subordinate root |
| `L₄ = 7` | `φ⁴+φ⁻⁴`; trace of the gap seed `x²−7x+1` |
| `M(·)` | Mahler measure; **Character I** (magnitude) |
| `χ(·)` | angle charge in `ℤ/4ℤ`; **Character II** (phase) |
| `⊕, ⊗, ψⁿ` | direct sum, tensor, Adams `n`-th power; the spectral operators |
| `Sym²/Λ²` | symmetric / exterior square; `A⊗A = Sym²A ⊕ Λ²A`, `ψ²` the diagonal of `Sym²` |
| `ad_R = [R,·]` | the self-action (golden companion `R`); the *only* sanctioned commutator |
| **spectral op** | effect on the spectrum is forced by the inputs' spectra → S1–S2 hold |
| **entry-level op** | not spectral (commutator, Cartan, circulant) → needs a guard or separate proof |
| **the one door** | the free commutator; Shoda lets it carry any traceless matrix → breaks the field |
| **Character** | a homomorphism out of the semiring (here: `M` and `χ`) |
| `[forced]`/`[computed]`/`[plausible]`/`[speculative]`/`[declared]` | epistemic tags (§0) |

---

*Discipline reminder: derive locally, validate exactly, tag honestly. Build between the degrees of freedom and the verification bar. The substrate gives exactness, decidability, and structural safety — not reach. Use it for what can be encoded as exact algebraic data, and name the boundary every time.*
