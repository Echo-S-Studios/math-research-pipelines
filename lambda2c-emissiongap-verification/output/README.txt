================================================================================
output/  --  run-time artifacts of the lambda=2c / Emission-Gap verification
================================================================================

This directory collects everything a run PRODUCES. It ships nearly empty and is
populated as the suite runs; the populated results.json is the deliverable.

--------------------------------------------------------------------------------
WHAT LANDS HERE
--------------------------------------------------------------------------------

  results.json            <- run_tests.py / pytest
      One JSON record per proven claim, plus a final summary block. Ships mostly
      empty (an empty "results" list, null timestamps, empty meta) and is filled
      in on each run. A complete, finalized run holds:

          90 claims, all FORCED, 0 failed
          by_paper: lambda_2c 41, emission_gap 40  (+ 9 catalog "shared" constants)

      Lifecycle (see ../harness/results.py):
        - init_results()  resets to the skeleton and stamps generated_utc + meta
                          (run_tests.py records dependency versions under
                           meta.versions; conftest.py records trigger/rootdir).
        - record(...)     each test appends one claim (locked read-modify-write).
        - finalize(...)   stamps completed_utc and computes the summary block.
      The path is taken from the env var RESULTS_JSON, else this file by default.

  lambda_2c_paper.pdf     <- build_pdfs.py  (3 pdflatex passes; ~24 pp)
  emission_gap_paper.pdf  <- build_pdfs.py  (2 pdflatex passes; ~16 pp)
      Rendered from ../papers/*.tex for full session context. The .tex sources
      are canonical and committed; the PDFs are build artifacts (NOT committed).
      If pdflatex is absent, build_pdfs.py reports it and exits 0 without
      failing the run -- the test suite does not depend on TeX. The same two
      papers are also compiled in CI and published on the live Pages site
      (see CROSS-LINKS below).

--------------------------------------------------------------------------------
HOW TO PRODUCE THESE
--------------------------------------------------------------------------------

  python ../run_all.py        # build PDFs, then run the suite step by step
  python ../build_pdfs.py     # just the two PDFs  (needs TeX Live / pdflatex)
  python ../run_tests.py      # just results.json  (file-by-file, append mode)
  pytest -v                   # results.json via conftest.py init/finalize

--------------------------------------------------------------------------------
RECORD SHAPE (results.json -> results[])
--------------------------------------------------------------------------------

  {
    "test_id":  "P1-IDENT-01",            # CONST-* | P1-* | P2-*
    "paper":    "lambda_2c",              # lambda_2c | emission_gap | shared
    "locus":    "Thm 3.1 / eq:lambda2c",
    "claim":    "lambda = 2c ...",
    "equation": "lambda = 2*c",
    "status":   "FORCED",                 # FORCED | COMPUTED | FAILED
    "detail":   { ... exact witnesses ... },
    "logged_utc": "..."
  }

The full per-file -> test_id map is in ../tests/README.md; the core-equation
table is in ../README.md section 5.

--------------------------------------------------------------------------------
EPISTEMIC DISCIPLINE (why these artifacts can be trusted)
--------------------------------------------------------------------------------

  - Every decision boundary is exact (sympy + fractions) or an exact root count
    (Sturm / Poly.count_roots). No float crosses a decision boundary.
  - mpmath (60 digits) and floats appear ONLY for displayed magnitudes and
    Mahler-VALUE cross-checks -- never on a verdict. So the numbers in each
    record's "detail" are float READOUTS of facts decided exactly upstream.
  - Only [FORCED]/[COMPUTED] claims are recorded as proofs; [DECLARED]/[POSITED]
    modelling choices are context, not results.
  - Versions are stamped into meta.versions, so a results.json is reproducible
    against ../requirements.txt (sympy 1.14.0, mpmath 1.3.0, numpy 2.4.4,
    pytest 9.1.1; Python 3.12.3).

--------------------------------------------------------------------------------
TROUBLESHOOTING
--------------------------------------------------------------------------------

  - results.json still shows "results": [] after a run:
      the suite was not actually run, or RESULTS_JSON pointed elsewhere. Run
      `pytest -v` from the package root, or `python ../run_tests.py`.

  - No PDFs appear / "pdflatex not found":
      install TeX Live (provides pdflatex; lmodern optional). build_pdfs.py
      exits 0 by design when pdflatex is missing -- this is not a test failure.

  - total_claims != 90 / "failed" > 0:
      a real failure is information (see ../README.md). Re-run a single file,
      e.g. `pytest -v ../tests/test_p2_02_angle.py`, and read its assertions.

  - "completed_utc": null or no summary block:
      the run did not reach finalize() (interrupted session). Re-run to
      completion; finalize stamps completed_utc and the summary.

--------------------------------------------------------------------------------
CROSS-LINKS
--------------------------------------------------------------------------------

  ../README.md            package overview, workflow, section-5 claim table
  ../harness/README.md    the exact primitives and the results.json lifecycle
  ../papers/README.md     the two .tex sources and how the PDFs are built
  ../tests/README.md      per-file -> test_id map and the record flow
  ../../README.md         the three-pipeline repository overview

  Live Pages site:  https://echo-s-studios.github.io/math-research-pipelines/
      hosts both papers compiled from ../papers/*.tex in CI:
        /papers/lambda_2c_paper.pdf
        /papers/emission_gap_paper.pdf

  Sibling pipelines in the same repo (../../):
      matrix-plates/                  Mahler-measure plates + browser tool
      residual-return-verification/   exact learning substrate (verify.py)
================================================================================
