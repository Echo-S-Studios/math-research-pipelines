# `tests/` — the verification suite (one core equation per file)

Twenty-one `pytest` files re-derive every **`[FORCED]`** (and the few `[COMPUTED]`) claim of the two companion papers in exact arithmetic. Each file is written to be **read as a derivation**: the module docstring names the paper locus and the core equation(s); each test function carries the derivation as exact `sympy`/`fractions` steps; every assertion is an exact identity (symbolic equality or Sturm root count); and on success the function **appends one record** to [`../output/results.json`](../output/results.json) via `harness.results.record(...)`.

> This page maps each file to its claim and to the `test_id`s it logs. The canonical *core-equation* table is [the top-level README §5](../README.md#5-the-test-suite--core-equation-per-file); the descriptions below are verified against the actual module docstrings and `record(...)` calls in these files. For the primitives the tests import (`companion`, `R_C`, `ad_operator`, `trace_down`, `flip_straddle`, `is_salem`, `signature`, `mahler_mp`, …) see [`../harness/README.md`](../harness/README.md).

The suite runs in catalog → Paper 1 → Paper 2 order (the zero-padded filenames sort naturally, which is how [`../run_tests.py`](../run_tests.py) orders them). A full run logs **90 records, all `FORCED`, 0 `FAILED`** — **9** catalog (`shared`), **41** Paper 1 (`lambda_2c`), **40** Paper 2 (`emission_gap`).

---

## The per-file → `results.json` flow

Each test function does the same three things, in order:

1. **Derive** the claim with exact `sympy`/`fractions` steps (and Sturm root counts for any signature or Salem question).
2. **Assert** the exact identity — symbolic equality, exact integer/rational equality, or an exact root count. Floats and `mpmath` appear only inside displayed magnitudes and Mahler-*value* cross-checks, never on the decision.
3. **`record(test_id, paper, locus, claim, equation, status="FORCED", detail=...)`** — append one proven-claim record, with exact witnesses in `detail`.

So **one test function ⇒ one record**. The shared JSON is initialized once at session start (by [`../conftest.py`](../conftest.py) under bare `pytest`, or by [`../run_tests.py`](../run_tests.py) which also stamps dependency versions), appended to by every test, and finalized with the summary block at session end. See [`../harness/README.md`](../harness/README.md#resultspy--the-append-only-results-json-lifecycle) for the lifecycle.

---

## Catalog constants — `test_constants.py` (9 records, `paper="shared"`)

The reference foundation: every constant that appears in a forced equation elsewhere is anchored here once, each pinned to its **exact minimal polynomial**.

| `test_id` | Function | Establishes |
|---|---|---|
| `CONST-01` | `test_phi_and_tau_minpolys` | `φ : x²−x−1`, `τ : x²+x−1`; `φ·ψ = −1` (det), `φ+ψ = 1` (trace) |
| `CONST-02` | `test_mu_S_plastic` | `μ_S` is the plastic number, real root of `x³−x−1`, and `μ_S < φ` (Smyth floor below golden) |
| `CONST-03` | `test_lehmer_is_salem_below_mu_S` | Lehmer's degree-10 polynomial is an irreducible Salem polynomial, `M ≈ 1.17628 < μ_S` (exact flip-straddle classification) |
| `CONST-04` | `test_beta4_minimal_degree4_salem` | `x⁴−x³−x²−x+1` is the minimal degree-4 Salem polynomial; `β₄ ≈ 1.72208 > φ` |
| `CONST-05` | `test_gate_radicand_seeds` | `x²−D` for `D ∈ {2,3,5}` are the gate seeds; `M(x²−D) = D` exactly |
| `CONST-06` | `test_gap_seed_is_phi4` | `gap = φ⁴` has minpoly `x²−7x+1`; `φ⁴ + φ⁻⁴ = L₄ = 7` |
| `CONST-07` | `test_Kformation_minpoly` | `K = 5^{1/4}/φ` has minpoly `x⁴+5x²−5` |
| `CONST-08` | `test_zc_and_critical` | `z_c = √3/2` has minpoly `4x²−3` (the `C=1/2` gate, `D=3`); critical `φ²/3` has minpoly `9x²−9x+1` |
| `CONST-09` | `test_lucas_fibonacci_seed_identities` | `{F₃,F₄,F₅} = {2,3,5}` are the gate discriminants; `L₄ = 7 = F₃+F₅`; Pell `L₄²−5F₄² = 4` |

---

## Paper 1 — `λ = 2c` (41 records, `paper="lambda_2c"`)

| File | Locus | `test_id`s | Core claim |
|---|---|---|---|
| `test_p1_01_identity.py` | Thm 3.1 / §5 | `P1-IDENT-01…05` | `λ = 2c`; `σ = 1/(2c) = 1/λ`; Čencov rescaling `F = G/c ⇒ c→kc rescales F→F/k`; the three canonicalizations `c ∈ {1, n, √(1+4C)/(2C)}`; **c free, so λ does not freeze** |
| `test_p1_02_gate_ladder.py` | §6, Thm 6.2 | `P1-LAD-01…06` | `R_C = [[0,C],[1,−1]] ⇒` charpoly `x²+x−C`, `D=1+4C`; `spec(ad_{R_C}) = {−√D, 0, +√D}`, centralizer `= span{I, R_C}`; ladder `{1/4,1/2,1} → {2,3,5}`; gate-balance / Mahler-radius `r(R_C)=√(1+4C)`; **exactly three valid gates forced** |
| `test_p1_03_frameshift.py` | Def 7.1 | `P1-FRAME-01…02` | `2cC = √(1+4C) ⇒ c = √(1+4C)/(2C)`; at `C=1`, `c = √5/2`, `λ = √5 = φ−ψ` |
| `test_p1_04_gate_forced.py` | §8–9 | `P1-GATE-01, -02, -03, -04, -05a, -05b, -06` | `#channels(d) = d²−d+1 = 3 ⇔ d=2`; min Mahler over integer quadratics `= φ` only at disc 5; the gap `(1,φ)` is empty; the cubic objection dissolves; the minpoly/squaring firewall collapses to `ℚ(√5)`; the keystone `R²=R+I` is unique to the golden companion |
| `test_p1_05_keystone.py` | Thm 10.3 | `P1-KEY-01…04` | the degree-2 minimum is the disc-5 tie `{φ, τ}`; Perron breaks it to `R²=R+I`; `φ` = smallest Perron root of a `2×2` primitive non-negative integer matrix; each keystone constraint is load-bearing (drop-one) |
| `test_p1_06_L4.py` | Prop 10.6 | `P1-L4-01…04` | `Rⁿ = F_n R + F_{n−1} I`, `L_n = tr(Rⁿ)`; Pell `L_n²−5F_n² = 4(−1)ⁿ`; `R⁴ = [[2,3],[3,5]]`, charpoly `x²−7x+1`, entries `{2,3,5}={F₃,F₄,F₅}`, `L₄ = F₃+F₅ = 7`; gap-seed roots |
| `test_p1_07_flip.py` | Prop 11.2 | `P1-FLIP-01…03` | `sign(D=1+4C)` sets eigenvalues/field/channel (at `C=−1`: roots `e^{±2πi/3}`, `M=1`, `D=−3`); trace form `G = diag(2, 2D)`, `det G = 4D` (Riemannian ↔ Lorentzian); `ℚ(i)` instance and gate/flip co-location at `D=0` |
| `test_p1_08_boundary.py` | §13–14 | `P1-BND-01…03` | `D = (2x+1)² = 1+4C`; `D = 4z²`, `C = z²−1/4` (any real coherence keeps `D ≥ 0`); Kuramoto critical coherence `z_c = √3/2` is the `C=1/2` gate (`D=3`) |
| `test_p1_09_kform.py` | Prop 16.1 | `P1-KFORM-01…02` | `x⁴+5x²−5 --(y=x²)--> y²+5y−5` straddles the fold; real roots `±K`, `K = 5^{1/4}/φ`; `M = β² = (5+3√5)/2` |
| `test_p1_10_secondflip.py` | §17–18 | `P1-2FLIP-01…03` | multiplicative flip on `|λ|`: `M=1 ⇔` cyclotomic (Kronecker); the two flips meet at `C=−1` (`x²+x+1`, `M=1`, `D=−3`); Lehmer band ordering `1 < L < μ_S < φ` |
| `test_p1_11_emission_resolution.py` | §15 | `P1-EMIS-01…02` | the catalog measures lie in `{1} ∪ [φ, ∞)`, min `φ`, no Salem; the floor is resolved in-system: cost `λ·log M ≥ λ·log φ > 0`, the band `(1, μ_S)` disjoint from the catalog (Paper 1 states it in-framework, citing Paper 2 for the proofs) |

---

## Paper 2 — the Emission-Gap Theorem (40 records, `paper="emission_gap"`)

| File | Locus | `test_id`s | Core claim |
|---|---|---|---|
| `test_p2_01_algebra.py` | §2 | `P2-ALG-01…05` | conjugate-travel hinge: an integer matrix has an integer charpoly, so eigenvalue ⇒ all `ℚ`-conjugates are eigenvalues; spectral semantics — `⊗` composes (`μ_i ν_j`), `⊕` unions spectra & multiplies Mahler, `(·)²` squares Mahler; **`⊗` is tropical on `M`** (`φ⊗φ = φ²`, not `φ⁴` — an on-circle guard for the corrected tensor-Mahler law) |
| `test_p2_02_angle.py` | Thm 3.2 | `P2-ANG-01…05` | **the central mechanism**: catalog args ∈ `(π/2)ℤ`; the quarter lattice is closed under `+` (tensor) and `×2` (square), never halved; an on-circle emitted eigenvalue is a 4th root of unity; a Salem's on-circle conjugates have irrational angle; ⇒ **no Salem emitted** (contradiction) |
| `test_p2_03_mahler_gap.py` | Lem 4.1, Cor 4.3 | `P2-GAP-01…03` | base case: no irreducible integer quadratic has `M ∈ (1, φ)`; degree-raising (`⊕`, `(·)²`, `⊗`) keeps the image inside `{1} ∪ [φ, ∞)`; cost floor `log M ≥ log φ` |
| `test_p2_04_nonlocal.py` | Rem 5.2, Prop 5.3 | `P2-NL-01…04` | four structurally analogous gaps with distinct endpoints (`φ ≠ log φ ≠ √5`); a degree-`2m` Salem field has signature `(2, m−1)` (indefinite trace form), catalog K places off the circle; finitely generated discrete sub-semigroup of `[φ, ∞)`, no accumulation at 1 |
| `test_p2_05_delta.py` | §6 | `P2-DELTA-01…04` | trace-down `R(x) = xᵐ T(x+1/x)`; Salem ⇔ `T` totally real with one root in `(2,∞)` and `m−1` in `(−2,2)`; the delta battery (`M` emits a Salem iff some reciprocal factor's `T` straddles `t=2`); spectral on-circle eigenvalues (4th roots of unity) have trace-downs in `{2, 0, −2}`, never astride |
| `test_p2_06_circulant_cartan.py` | §7 | `P2-CIRC-01`, `P2-CART-01`, `P2-COMM-01` | a circulant's field is abelian/cyclotomic (totally real or CM) ⇒ not Salem; Cartan eigenvalues `2−2cos(·) ∈ [0,4]` totally real, `⊕` multiplicative; a generic (traceless) commutator emits no degree-4 Salem (`x⁴+bx²+1`'s symmetric trace-down `t²+(b−2)` cannot straddle) |
| `test_p2_07_uniform.py` | §8 | `P2-UNIF-01…05` | `spec(ad_R) = {0, ±√5}`; real differences live in `K = ℚ(√2, √3, 5^{1/4})` (e.g. `2K`: `x⁴+20x²−80`, signature `(2,1)`); **exhaustively, every one of the 27 subfields of K** is totally real or signature `(2k,k)`, with exactly **4** Salem-shape `(2,1)` quartics; min degree-4 Salem `= β₄ > φ`; image has no sub-φ Salem |
| `test_p2_08_closure_guard.py` | §8 (certificate) | `P2-GUARD-01…06` | the runtime **closure certificate**: framework ops all read `FORCED`; a foreign Lehmer hit reads `INVALID_CLOSURE`; the φ floor **emerges** from the guard's exact verdict over planted Salem numbers straddling φ (not asserted); a degree-4 Salem reads `FORCED_ABOVE_FLOOR`; a cyclotomic control reads `FORCED`; the exact `ℚ(√5)` sign decides a **pure-rational** `R(φ)` (the deg-6 Salem has `R(φ)=2`) instead of crashing (**B1** regression) |
| `test_p2_09_emission_algebra.py` | §8 (system invariant) | `P2-EALG-01…07` | `cost = λ·log M = 2c·log M`; the floor `2c·log φ` survives every operation and composition (a global invariant, not a per-object re-check); the forbidden (Salem) channel stays empty; field confinement / provenance preserved; a foreign sub-φ Salem is rejected; the floor is **linear in the free c** (never frozen at `c=1`); the four readouts (height, entropy, channel, signature) are consistent |
| `test_p2_10_salem_factory.py` | §8 (operation-relative) | `P2-FACTORY-01…03` | the operational **Salem-Slot / commutator-boundary** form: the factory `Sₙ = xⁿ(x²−x−1) − reverse` routes a sub-φ Salem for `n ∈ {6,10,12}` → `INVALID_CLOSURE`; each Salem's totally-real **trace-down** reads `FORCED` (benign); and the verdict **does not track the trace** (INVALID at trace 0 and 1, FORCED at trace 1 and 7) |

`test_p2_08` and `test_p2_09` are the **operational layer** of the closure argument: their engines live at the package root — [`../emission_closure_guard.py`](../emission_closure_guard.py) (the exact runtime certificate + foreign-op tripwire) and [`../emission_algebra.py`](../emission_algebra.py) (the functional emission algebra with the floor built in). The guard certifies the **cost floor** (`INVALID_CLOSURE` only for a *sub-φ* Salem) and is therefore complementary to, not a replacement for, the stronger no-Salem **angle theorem** of `test_p2_02`. See the discussion of *closure, not enumeration* in [the top-level README §5](../README.md#5-the-test-suite--core-equation-per-file).

---

## Running

```bash
# from the package root
pytest -v                         # all 21 files, init/finalize via conftest.py
pytest -v tests/test_p2_02_angle.py   # a single file
python ../run_tests.py            # run file-by-file, stamping versions into results.json
```

Only `[FORCED]`/`[COMPUTED]` claims are asserted here; `[DECLARED]`/`[POSITED]` modelling choices (e.g. the Jeffreys reading `c=1`) are recorded as context, not proven. Expected outcome: **95 claims, all FORCED, 0 failed**. See [the top-level README §7–8](../README.md#7-epistemic-discipline) for the epistemic discipline and reproducibility notes.
