# `.github/` — CI workflows & community files

Automation and contribution scaffolding for the repository. The workflows run the three
verification suites on every relevant change and deploy the GitHub Pages site; the templates encode
the project's exactness discipline at the point of contribution.

## Workflows (`workflows/`)

Each suite has its own **path-filtered** workflow, so a change to one pipeline only runs that
pipeline's CI (with pip caching). Status badges for the first three appear at the top of the
[root README](../README.md).

| Workflow | Trigger | What it runs |
|---|---|---|
| [`matrix-plates.yml`](workflows/matrix-plates.yml) | push / PR touching `matrix-plates/**` | `pip install -e ".[dev]"`, then `make test` (139 tests) + `make verify` (10/10), on Python 3.9 and 3.12. |
| [`lambda2c.yml`](workflows/lambda2c.yml) | push / PR touching `lambda2c-emissiongap-verification/**` | `pip install -r requirements.txt`, then `pytest -v` (95 claims) on Python 3.12; uploads `output/results.json` as an artifact. |
| [`residual-return.yml`](workflows/residual-return.yml) | push / PR touching `residual-return-verification/**` | `quick` job: `verify.py --quick` (the always-on probe gate). `full` job: the complete `verify.py` (training + kira-language) on a weekly schedule + manual dispatch. |
| [`pages.yml`](workflows/pages.yml) | push to `main` touching `site/`, `papers/`, the pipeline papers, or the tool; or manual | Builds the Pages site: compiles the λ=2c papers from `.tex` (`xu-cheng/latex-action`), renders `papers/*.md` via [`site/render_docs.py`](../site/README.md), assembles `_site/`, and deploys with `upload-pages-artifact` → `deploy-pages`. **The sole Pages deployer** — see [`site/README.md`](../site/README.md). |

## Community files

| File | Purpose |
|---|---|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | The non-negotiable exactness discipline (no float crosses a decision boundary; new claims ship with a test and a paper locus) and the per-pipeline test entry points. |
| [`pull_request_template.md`](pull_request_template.md) | The PR checklist: which pipeline, the paper locus touched, suites run, no float regressions, claims pinned to tests. |
| [`ISSUE_TEMPLATE/`](ISSUE_TEMPLATE/) | `bug_report.md` (which pipeline / exact command / failing test), `claim_question.md` (ask about a verified claim or its scope), and `config.yml`. |

`SECURITY.md`, `CODE_OF_CONDUCT.md`, `FUNDING.yml`, and `CODEOWNERS` are intentionally **deferred**
while the repository is private — add them when/if it goes public and gains external contributors.
