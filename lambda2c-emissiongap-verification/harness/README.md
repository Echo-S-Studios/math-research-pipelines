# `harness/` — the exact-arithmetic engine and the results ledger

Two modules, imported by every test and orchestrator in the suite:

| Module | Role |
|---|---|
| [`algebra.py`](algebra.py) | the shared **exact-arithmetic primitives** — companion matrices, the self-action `ad`, the reciprocal trace-down, Sturm-based Salem detection, Mahler measure |
| [`results.py`](results.py) | the **append-only results JSON lifecycle** — one record per proven claim, with a final summary |

`__init__.py` is empty: `harness` is a plain package, put on `sys.path` by [`../conftest.py`](../conftest.py) and [`../run_tests.py`](../run_tests.py) so `from harness.algebra import ...` resolves whether `pytest` is launched from the package root or via the orchestrator.

The discipline is the same one the two papers declare (see [`../papers/`](../papers/README.md)): **every decision boundary is evaluated symbolically** (`sympy` + `fractions`) or by **exact root counting** (Sturm via `sympy.Poly.count_roots`). `mpmath` (60 digits) and Python floats appear **only** for displayed magnitudes and Mahler-*value* cross-checks — never on a decision path. This mirrors the top-level invariant of the whole repo: *no float crosses a decision boundary* (see the [repository README](../../README.md#what-makes-this-rigorous)).

---

## `algebra.py` — the exact primitives

Module-global setup: `mp.mp.dps = 60` (mpmath precision, for value cross-checks only) and the symbols `x, t, y`. Polynomials are passed as **integer coefficient lists, high degree first** (`[1, b, c]` == `x^2 + b x + c`).

### Canonical constants

| Name | Value | Minimal polynomial / note |
|---|---|---|
| `PHI` | `(1 + sqrt5)/2` | golden ratio, root of `x^2 - x - 1` (exact `sympy` algebraic) |
| `PSI` | `(1 - sqrt5)/2` | golden conjugate `= -1/phi` |
| `SQRT5` | `sqrt5` | exact |
| `PHI_f`, `PSI_f` | floats | display-only readouts of `PHI`, `PSI` |
| `MU_S` | `1.3247…` | Smyth's plastic number, real root of `x^3 - x - 1` (smallest non-reciprocal Mahler measure); computed by `mp.findroot` |
| `LEHMER_POLY` | `[1,1,0,-1,-1,-1,-1,-1,0,1,1]` | Lehmer's degree-10 polynomial, the smallest known Salem number |
| `BETA4_POLY` | `[1,-1,-1,-1,1]` | minimal degree-4 Salem polynomial `x^4 - x^3 - x^2 - x + 1` (`beta4 ≈ 1.72208`) |

### Integer sequences

- **`lucas(n)`** — exact Lucas number `L_n = phi^n + psi^n`, simplified to an integer.
- **`fib(n)`** — exact Fibonacci number `F_n = (phi^n - psi^n)/sqrt5`, simplified to an integer.

Both are built from the exact algebraic `PHI`/`PSI`, not from float recurrences, so e.g. `L_4 = 7` and `{F_3, F_4, F_5} = {2, 3, 5}` come out as exact integers (the gate discriminants the papers turn on).

### Polynomials and matrices

- **`poly(coeffs)`** — wraps an integer coefficient list as a `sympy.Poly` in `x`.
- **`companion(coeffs)`** — the **standard companion matrix** whose characteristic polynomial is the given monic `coeffs` (asserts a leading `1`). Subdiagonal ones; last column carries `-c[n-i]`.
- **`R_C(C)`** — the **gate companion** the papers use, `R_C = [[0, C], [1, -1]]`, whose charpoly is `x^2 + x - C` (note the sign), with discriminant `D = 1 + 4C` (Paper 1, `eq:companion`).
- **`charpoly_coeffs(M)`** — integer coefficient list (high first) of `M`'s characteristic polynomial.
- **`ad_operator(M)`** — the **self-action** `ad_M = [M, ·] : X ↦ MX − XM`, materialised as an `n^2 × n^2` matrix over the standard basis `{E_ij}`. This is the trifurcation channel of Paper 1 (`prop:trifurcation`) and the derivation of Paper 2 (`def:selfaction`): its spectrum is the eigenvalue **difference set** of `M` (for the golden seed, `{0, ±sqrt5}`).
- **`kron(A, B)`**, **`dsum(A, B)`** — Kronecker product `(⊗)` and direct sum `(⊕)`, the two spectral operations of the emission algebra (`⊗` composes Mahler measures, `⊕` multiplies them).

### Heights, reciprocity, Salem detection

- **`mahler_mp(coeffs)`** — Mahler measure `|a_n| · ∏ max(1, |α_i|)` as a high-precision `mpf`. Computed from `mp.polyroots` at extra precision; this is a **value cross-check**, never a decision.
- **`is_reciprocal(coeffs)`** — exact palindrome test (allowing an overall sign flip).
- **`signature(coeffs)`** — exact metric signature `(r1, r2)`: `r1` real roots counted by **Sturm** (`count_roots(-oo, oo)`), `r2 = (deg − r1)//2` complex-conjugate pairs. No float touches the count.
- **`trace_down(coeffs)`** — the exact **trace-down polynomial** `T(t)` with `R(x) = x^m · T(x + 1/x)` for a reciprocal `R` of even degree `2m`. Built from the Chebyshev-like recurrence `x^k + x^{-k} = p_k(t)`: `p0 = 2`, `p1 = t`, `p_{k+1} = t·p_k − p_{k-1}` (Paper 2, `def:tracedown`). This is the change of variable that relocates the Salem question to a single straddle boundary.
- **`flip_straddle(coeffs)`** — the exact **Sturm certificate** for the Salem flip (Paper 2, `lem:salemflip`): for `R` irreducible, reciprocal, degree `2m ≥ 4`, the trace-down `T` must be totally real with **exactly one** root in `(2, ∞)` and `m−1` inside `(−2, 2)`, with none at `±2`. Returns `(bool, counts)`; all counts are Sturm root counts.
- **`is_salem(coeffs)`** — exact Salem classification: a thin wrapper that returns the flip-straddle verdict.
- **`n_on_circle(coeffs, tol=1e-12)`** — counts roots on `|z| = 1`. **Diagnostic/display only** (uses float roots and a tolerance) — never a decision boundary, by construction.

> The package root also ships two larger self-contained engines — [`../emission_closure_guard.py`](../emission_closure_guard.py) and [`../emission_algebra.py`](../emission_algebra.py) — which re-implement the trace-down / flip-straddle primitives and add the runtime closure **certificate** and the functional emission algebra. They are exercised by `tests/test_p2_08` and `tests/test_p2_09`; see [`../tests/README.md`](../tests/README.md).

---

## `results.py` — the append-only results JSON lifecycle

A **single shared JSON document** that every test appends to. The path comes from the `RESULTS_JSON` environment variable (set by the orchestrator); otherwise it defaults to [`../output/results.json`](../output/results.json). The file **ships mostly empty** (an empty `results` list) and is populated as the suite runs.

### The three lifecycle functions

- **`results_path()`** — `os.environ["RESULTS_JSON"]` or the default `output/results.json`.
- **`init_results(meta=None, path=None)`** — resets the JSON to a fresh skeleton at the **start** of a run, stamping `generated_utc` and an optional `meta` block (the runner records dependency versions here).
- **`record(test_id, paper, locus, claim, equation, status="FORCED", detail=None)`** — appends **one proven-claim record** via a locked read–modify–write, stamping `logged_utc`. One call per claim, from inside the test function, after its exact assertions pass.
- **`finalize(summary=None)`** — stamps `completed_utc` at the **end** of a run and computes the `summary` block: `total_claims`, `forced`, `computed`, `failed`, and `by_paper` (`lambda_2c`, `emission_gap`). A caller-supplied `summary` is merged in (e.g. the pytest exit status).

### Concurrency and resilience

A module-level `threading.Lock` (`_LOCK`) guards every read–modify–write, so parallel appends never corrupt the document. `record` is **self-healing**: if the file is missing or unparseable it rebuilds the skeleton before appending, so a single claim never loses the whole ledger.

### Record shape

```json
{
  "test_id":  "P1-IDENT-01",
  "paper":    "lambda_2c",            // or "emission_gap" or "shared"
  "locus":    "Thm 3.1 / eq:lambda2c",
  "claim":    "lambda = 2c (the 2 is the inverted 1/2 of the KL quadratic term)",
  "equation": "lambda = 2*c",
  "status":   "FORCED",              // or "COMPUTED" / "FAILED"
  "detail":   { "...": "exact witnesses" },
  "logged_utc": "..."
}
```

`test_id` prefixes: `CONST-*` (catalog constants), `P1-*` (Paper 1, `lambda_2c`), `P2-*` (Paper 2, `emission_gap`).

### Who drives the lifecycle

| Entry point | `init` | `record` | `finalize` |
|---|---|---|---|
| `pytest` directly | [`../conftest.py`](../conftest.py) `pytest_sessionstart` | the test bodies | `conftest.py` `pytest_sessionfinish` |
| [`../run_tests.py`](../run_tests.py) | the runner (stamps `meta.versions`), then sets `RESULTS_NO_INIT=1` so each per-file `pytest` **appends rather than resets** | the test bodies | the runner |

A populated, finalized run yields **90 records** — `lambda_2c` 41, `emission_gap` 40, plus 9 catalog (`shared`) constants — **all `FORCED`, 0 `FAILED`** (see [the top-level README §6 and §8](../README.md#6-the-results-json)).
