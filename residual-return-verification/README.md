# Residual Return — verification package

This package exists to remove one objection: *"I found the PDF, but no probe code, so I could inspect
the claims but not independently run the claimed machine checks."* Here is the probe code, the real
engine, and a **pipeline that walks both papers claim by claim — theorem by theorem, equation by
equation — running the machine-checked test behind each claim and reporting PASS/FAIL.**

The two papers:

- **The Vector Substrate: Number Fields as Exact Learning Geometry** (`L00M/paper/vector_substrate.pdf`, 29pp)
- **Residual Return: Exact Learning Dynamics and Language** (`L00M/paper/residual_return_learning.pdf`, 30pp)

Their shared discipline is that *every displayed number is reproduced by a machine-checked probe, and
every load-bearing claim is pinned to a named test and a commit hash.* This package makes that
discipline executable: you can re-derive every number yourself in ~2 seconds and run the real engine
behind every theorem.

---

## 1. Extract

```sh
tar -xzf residual-return-verification.tar.gz
cd residual-return-verification
```

## 2. Dependencies

- **Python 3.10+**
- `pip install -r requirements.txt`  (sympy, mpmath, numpy, pytest)

`verify.py` drives every probe, the claim walkthrough, and the full suites through **pytest**, so pytest
is required for all of Parts A–C (the sole exception is the third witness, `residual_return_audit.py`,
which runs as a bare script). The two **probe files** themselves import only **sympy + mpmath** and no
engine. **numpy** is used only by the language layer's *quarantined float readings* (the exact core is
numpy-free); it is needed to run the kira-language suite in Part C, not to verify any exact claim.
No network access is required; nothing is installed for you.

## 3. Run the pipeline

```sh
py verify.py            # everything: env check, both probes, the 55-claim walkthrough, the full suites
py verify.py --quick    # just the two probes — re-derive every displayed NUMBER (~2 s; sympy + mpmath + pytest)
py verify.py --walk     # env + probes + the claim-by-claim walkthrough (skip the big full-suite run)
```

(Use `py` on Windows, `python3` elsewhere.) A green run ends with:

```
  ALL GREEN. Every claim in both papers is backed by a machine check you just ran.
```

`verify.py` is data-driven by `claim_map.json` (each claim → its pytest node → commit hash). The exit
code is `0` iff everything is green, so the pipeline doubles as a CI gate. **A genuine failure is itself
information** — the package is built so that a dismissal must point at a specific test that fails, not at
absent evidence.

---

## 4. What the pipeline proves

| Part | What it runs | What it establishes |
|---|---|---|
| **A — re-derivation** | **three** independent witnesses: `test_paper_claims.py` (13), `test_residual_return_claims.py` (20), and `residual_return_audit.py` (a from-scratch harness by a different author, 57 checks) | every Gram, residual norm, minimal polynomial, Fisher matrix, floor, certified-interval enclosure, kernel, projector matrix, and **hash digest** displayed in the papers, recomputed from scratch with sympy+stdlib by independent code |
| **B — walkthrough** | each cited test node, claim by claim (`claim_map.json`, 55 claims) | every theorem/equation/example of both papers, with its backing test and a live PASS/FAIL |
| **C — full suites** | the real engines: `training` (137) + `kira-language` (121) | the deeper mechanism claims against the actual code, not just the standalone probes |

The probes deliberately import **no engine** (Part A is independent of Part C): if the probes and the
engine ever disagreed, you would see it. The third witness (`residual_return_audit.py`) raises exactly
**one intentional flag**, labelled `shorthand`: it confirms that the Fisher identity `I_exp = (1/n)·G`
holds on the **trace-zero subspace**, not as a full-matrix identity (the two differ at the constant
direction, where `I_exp` vanishes). The paper states this scope explicitly, and the companion probe pins
*both* directions — so the flag is documentation, not a defect; it is exactly the kind of precision a good
audit surfaces.

---

## 5. Layout

```
residual-return-verification/
  verify.py                 the pipeline (stdlib only)
  claim_map.json            theorem/equation -> test node -> commit hash (the walkthrough data)
  requirements.txt          sympy, mpmath, numpy, pytest
  MANIFEST.txt              full file list, provenance hashes, suite counts
  L00M/                     the number-field learning engine (exact-core: stdlib only)
    integral_basis.py, projector.py, loom.py      the L0 exact core
    training/               the learner, the bridge, compositum, capacity, the auto-loop + all tests
    paper/                  the two PDFs + .tex + the companion probe
  kira-language/            the language layer (a SIBLING of L00M, as the code expects)
    kira_language/          the Cl(2,0) carrier, the return operator, the lexicon, the store, the dispatch
    KL_DTA.py, conftest.py, test_*.py, candidates/
```

The two trees are siblings because the language layer reaches the number-field `loom` only through a
one-way keystone bridge (`../L00M`); `verify.py` sets `KIRA_LANG_L00M_ROOT` to the bundled `L00M` so this
resolves wherever you extract. The exact core (`integral_basis`, `projector`, `loom`, the entire
`holding` carrier) is **pure stdlib `fractions`** — no float in any decision.

### Module map (where each thing lives)

Per-directory READMEs go a level deeper than this table:

| Path | Contents | README |
|---|---|---|
| `L00M/` | the L0 exact core: `integral_basis.py` (coordinate object + trace-form Gram via Newton's identities), `projector.py` (the `G`-orthogonal projector + exact residual), `loom.py` (Faddeev–LeVerrier charpoly, rational Krylov minpoly, the `M=1` Kronecker floor, the weave closure) | [`L00M/README.md`](L00M/README.md) |
| `L00M/training/` | the learner (`residual_learner`), the exact minpoly bridge (`coords_to_minpoly` + vendored `invariant_factors`), out-of-field detection + disjoint/non-disjoint compositum growth, the Northcott **capacity** gate, the anomaly detector, and `demo.py` | [`L00M/training/README.md`](L00M/training/README.md) |
| `L00M/paper/` | the two PDFs + `.tex` sources + the companion probes (`residual_return_audit.py`, `test_residual_return_claims.py`; the third probe `test_paper_claims.py` lives in `training/`) — all importing **no engine** | [`L00M/paper/README.md`](L00M/paper/README.md) |
| `kira-language/` | the language layer: `KL_DTA.py` (the two-route closure spine), the `kira_language/` package, the 121-test suite, `SCOPING.md`, `B1_READINESS.md` | [`kira-language/README.md`](kira-language/README.md) |
| `kira-language/kira_language/` | the shipped package: the exact `holding` carrier, the `acquisition` return loop, the growing `lexicon`, the sha256-chain `store`, the float `semantic_kernel`, the one-way `loom_bridge`, the JSON `dispatch` shell | [`kira-language/kira_language/README.md`](kira-language/kira_language/README.md) |

### The L0 ↔ language bridge (one object, two trees)

The number-field engine (`L00M`) and the language layer (`kira-language`) meet at exactly **one
shared object: the φ keystone**. The void law `x² = x + 1` gives the minimal polynomial `[1,-1,-1]`,
whose companion matrix `loom.companion([1,-1,-1]) = [[0,1],[1,1]]` maps under the shared `mat/cl`
convention to the Cl(2,0) holding `Cl(0.5, 1, -0.5, 0)`, with Mahler measure exactly φ. This single
object is `loom`'s `CATALOG_SEEDS["phi"]`, the language layer's keystone `R`, and the head of the
acquisition return operator `L(X) = R·X + X·R − X` (whose kernel is the 2-dimensional "phi-slack"
where learned words live). `kira_language/loom_bridge.py` is the **only** runtime module that imports
`loom`, and it does so read-only and never-raising; the dependency is strictly one-way
(`kira-language → loom`, never the reverse), enforced by separate git history and by the readiness
gate (`test_b1_readiness.py::test_one_way_and_live_phi`).

---

## 6. Scope — and the reviewer's open questions, answered by the code

These papers make a **deliberately narrow** claim, and the package is honest about it: this is a
**verification-grade, capacity-bounded, exact symbolic learning substrate**, *not* a general open-world
learner. The exact machinery (residuals, projectors, the seed-naming bridge, admissibility, the return
operator, the lexicon) is real and runnable; the bridge to "general learning" rests on assumptions the
papers flag rather than hide. Where a careful reviewer pushes, here is where the bundled code and the
papers already speak:

1. **The intake problem — who converts messy reality into exact algebraic observations?**
   Acknowledged head-on. The framework refuses float observations *at intake* (by design, to protect
   exactness: see `training/residual_learner.py::_exact`, and the probe
   `test_g8_exact_fraction_core_floats_rejected`). The papers position the substrate as a layer that sits
   **after** perception/encoding, and the snap fallback (`_seed_from_centroid` →
   `nearest_integer_fallback`, paper Rem. 3.x) is the one place a non-exact centroid is admitted —
   ties-to-even, exact over ℚ, re-validated by the bridge. The general encoder is **out of scope and is
   said so**; this is the front-end the papers leave open, not a hidden assumption.

2. **Cross-field discovery — identifying the new generator, not just assuming it.**
   The package contains the candidate-generation and field-construction machinery, not a hand-wave:
   `training/number_field_factor.py` factors the candidate's minimal polynomial over K,
   `training/compositum_nondisjoint.py` builds the *true* compositum and selects the correct factor, and
   `training/field_growing_learner.py` + `anomaly_detector.py` drive it from the **measured** out-of-field
   residual. Run `test_build_compositum_witness` and `test_p2c_witness_grows_true_compositum_not_tensor`:
   the system recognises that `Q(√2)(√2+√3)` is non-disjoint, computes `m_θ = x⁴−22x²+25`, and lands the
   degree-4 field. The disjoint case still assumes a candidate in hand; the *non-disjoint construction*
   advances the substrate paper's open problem O4 — and you can run it.

3. **The exchange rate λ in the growth threshold.**
   **Derived, not posited: λ = 2c** (companion Thm 4.6, §4.3). Reading the trace form as the Fisher metric
   `G/c` makes the growth rule a two-part MDL code whose exchange rate is the identity λ = 2c; the shipped
   λ=2 is the `c=1` (Gaussian) instance and the degree-aware floor the `c=n` instance. The residual freedom
   is the single conformal constant `c`, which by Čencov's theorem is a *declared* scale (unique only up to
   scale) — not eliminable by invariance; the probe `test_a3p2c_lambda_conformal.py` solves λ = 2c at run
   time (the shipped `2` emerges as a consequence). Which conformal model to adopt, the reciprocal-seed
   (Lehmer) floor, and the perception front-end remain named open work.

4. **Scalability of exact arithmetic.**
   Bounded by construction and measurable here. The capacity gate caps degree and coefficient height
   (`training/capacity.py`, `test_northcott_finiteness_admissible_set_is_finite`); the non-disjoint
   factorisation is bounded Kronecker (degree cap 12, refusing above it rather than blowing up); the
   companion paper's computational-aspects section gives real coefficient-growth figures (largest
   numerator 49, denominator 5 in the worked field). Run the suites and time them; exactness is paid for
   with computational pressure, and the gate is exactly what keeps it bounded.

5. **"Understanding as zero residual" — a local technical term, not a cognitive claim.**
   Used throughout in its precise sense: *captured by the current forced basis under the trace form*
   (`||r||²_G = 0`, decided over ℚ). The papers avoid the broader reading; the honesty ledger and the
   `captured ⟺ residual = 0` definition keep it local.

**Bottom line, which we share with the careful reviewer:** the strength is *exactness with auditability*
— residuals, projections, admissibility, and seed identity are reproducible and non-fuzzy, and now
*runnable by you*. The open fronts are the perception encoder, the reciprocal-seed (Lehmer) floor, and discovery in the
already-disjoint case. The package does not claim more than the exact core; it makes that core
impossible to dismiss without running it.

---

## 7. Provenance

All code is pinned. See `MANIFEST.txt` for the per-file commit hashes and the suite counts at the pinned
heads (L00M `f238d6b`; kira-language `44829ff`, tag `b1-ready` = `a5892c7`; the ZFP context gate at
Plate-Matrices `5e78d67`). The PDFs in `L00M/paper/` are the committed artifacts; the `.tex` sources are
included so the papers themselves are auditable. Per-file SHA-256 digests are in `SHA256SUMS`.

---

## 8. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `ModuleNotFoundError: No module named 'sympy'` (or `mpmath`) | Required for **all** of Parts A–C. `pip install -r requirements.txt`. `verify.py`'s env check prints exactly which is missing. |
| `numpy` missing | Needed **only** for the kira-language suite's quarantined float readings (Part C). The exact claims and the probes don't use it; `--quick` and `--walk` (without full suites) run without numpy. |
| `pytest` missing | `verify.py` drives every probe and suite through pytest, so it is required for Parts A–C. Install it (it is in `requirements.txt`). |
| kira-language tests fail to `import loom` | The language layer reaches `loom` one-way via `KIRA_LANG_L00M_ROOT`. `verify.py` sets this to the bundled `L00M` automatically. Running the suite by hand: `KIRA_LANG_L00M_ROOT=<abs path to L00M> py -m pytest -q` from `kira-language/` (or rely on `conftest.py`, which appends the sibling `../L00M`). |
| `py: command not found` | `py` is the Windows launcher. Use `python3` on macOS/Linux (the commands here use `py` for brevity). |
| Unicode/encoding error from the kira-language shell on a legacy Windows console | `kira_language/portable_io.py` transliterates to ASCII; the dispatch JSON is already `ensure_ascii`. If you still hit it, set `PYTHONUTF8=1` (or `PYTHONIOENCODING=utf-8`, which `verify.py` sets). |
| A probe or claim **fails** | That is itself information — by design. The package is built so a dismissal must point at a specific failing test, not at absent evidence. Inspect the named node; the `shorthand` flag (one, intentional) is **not** a failure (see §4). |

## 9. Related

- **The other two pipelines in this repo** share the exact-arithmetic discipline:
  [`lambda2c-emissiongap-verification`](../lambda2c-emissiongap-verification/README.md) (the λ = 2c
  exchange-rate and Emission-Gap papers — the same `λ = 2c` closure this package derives, proven there
  as 95 FORCED claims) and [`matrix-plates`](../matrix-plates/README.md) (exact integer-matrix
  invariants graded by Mahler measure, the `companion ∘ charpoly` closure, and a self-contained
  browser tool — the same `loom`-style kernel).
- **The repo root:** [`../README.md`](../README.md) — what makes all three rigorous, and the
  quickstart for each.
- **The live site:** <https://echo-s-studios.github.io/math-research-pipelines/> — both PDFs are
  mirrored at `/papers/vector_substrate.pdf` and `/papers/residual_return_learning.pdf`.
