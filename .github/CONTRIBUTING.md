# Contributing

This repo holds three exact-arithmetic verification pipelines. The bar for a
contribution is simple: a claim is real only if a machine check reproduces it,
and no float is allowed to decide anything.

## Exactness discipline (non-negotiable)

All three pipelines share one rule: **no float ever crosses a decision boundary.**

- Every decision — equality, sign, root count, residual-is-zero, similarity,
  gate selection — is made in exact rationals/integers (`sympy`, `fractions`,
  `ℚ[x]`). Floats (`mpmath`, `numpy`, `float`) appear **only** for displayed
  magnitudes and cross-checks, never on the boundary of a comparison that drives
  an outcome.
- A new or changed claim **must** ship with a machine-checked test, and that test
  must **cite the paper locus** it verifies (theorem / equation / section). A
  claim without a named, passing test is not a claim here.
- Keep the epistemic grading honest: only `[FORCED]` / `[COMPUTED]` results are
  asserted as proofs. `[DECLARED]` / `[POSITED]` / `[OPEN]` choices are recorded
  as context, not proven.

## Test entry points (per pipeline)

Run from the repo root. Each pipeline is self-contained.

- **lambda2c-emissiongap-verification**
  ```bash
  cd lambda2c-emissiongap-verification && pip install -r requirements.txt && pytest
  ```

- **matrix-plates**
  ```bash
  cd matrix-plates && pip install -e ".[dev]" && make test && make verify
  ```

- **residual-return-verification**
  ```bash
  cd residual-return-verification && pip install -r requirements.txt && python3 verify.py
  ```
  Use `python3 verify.py --quick` for the fast probe gate (re-derives every
  displayed number in ~2 s).

## Before opening a PR

- Run the suite(s) for every pipeline you touched; they must be **green** before
  you open the PR. State which ones you ran.
- CI runs the same suites per-pipeline, **path-filtered** — a change under one
  pipeline directory only triggers that pipeline's checks.
- Update the relevant `README.md` if behavior, test counts, or claim counts
  change.

## Edit the canonical directories, not the archives

`Zipped-Tarred-Pipelines/` contains duplicate **offline archives** (`.zip` /
`.tar`) of the three pipelines for distribution. They are not the source of
truth. Make all edits in the canonical pipeline directories
(`lambda2c-emissiongap-verification/`, `matrix-plates/`,
`residual-return-verification/`); do not edit inside the archives.
