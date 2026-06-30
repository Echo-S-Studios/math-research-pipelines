# `site/` — the GitHub Pages source

This folder is the source for the project's live site,
**[echo-s-studios.github.io/math-research-pipelines](https://echo-s-studios.github.io/math-research-pipelines/)**.
It is **not** served as-is — the published site is *assembled* by the
[`Deploy GitHub Pages`](../.github/workflows/pages.yml) workflow, which compiles the λ=2c papers,
renders the Markdown docs, copies the PDFs and tools, and deploys the result via the official
GitHub Actions Pages pipeline (`upload-pages-artifact` → `deploy-pages`). There is no Jekyll and no
build tooling to install.

## Files

| File | Role |
|---|---|
| `index.html` | The single, self-contained landing page (dark/gold theme matching the Matrix Plates tool). Hard-codes the four pipeline-paper cards and the Matrix Plates tool card, then **fetches [`../papers/catalog.json`](../papers/catalog.json) at load** and renders a card for each entry — `pdf`/`doc` entries into **Additional papers**, `tool` entries into **Interactive**. Accessible (skip-link, landmarks, `prefers-reduced-motion`), responsive, with Open Graph / JSON-LD metadata and an inline-SVG favicon. |
| `render_docs.py` | The build-time Markdown renderer. Converts every `papers/*.md` (except `README.md`) into a themed HTML page with LaTeX math typeset by KaTeX (via `pymdown-extensions` arithmetic + KaTeX auto-render). Run by the Pages workflow as `python site/render_docs.py papers _site/papers`. Deps: `markdown`, `pymdown-extensions`. |

## How a deploy is assembled

The [`pages.yml`](../.github/workflows/pages.yml) `build` job produces `_site/`:

```
_site/
├── index.html                     # = site/index.html
├── tool/index.html                # = matrix-plates/web/matrix_plates.html
└── papers/
    ├── lambda_2c_paper.pdf         # compiled from .tex in CI (xu-cheng/latex-action)
    ├── emission_gap_paper.pdf      # compiled from .tex in CI
    ├── vector_substrate.pdf        # copied from residual-return-verification/L00M/paper/
    ├── residual_return_learning.pdf
    ├── <every papers/*.pdf>        # contributed PDFs (drop-zone)
    ├── <every papers/*.html>       # contributed self-contained tools (drop-zone)
    ├── <every papers/*.md → .html> # contributed Markdown docs, rendered
    └── catalog.json                # drives the "Additional papers" / "Interactive" cards
```

## Adding to the site

You almost never edit this folder to add content. Drop a file into [`../papers/`](../papers/) and add
one [`catalog.json`](../papers/catalog.json) entry — see [`../papers/README.md`](../papers/README.md).
Edit `index.html` only to change the page's structure, hard-coded cards, or styling; edit
`render_docs.py` only to change how Markdown docs are themed.

## Activation (one-time, already done)

GitHub Pages **Source** must be set to **GitHub Actions** (Settings → Pages). The site then
redeploys on every push to `main` that touches `site/`, `papers/`, the pipeline papers, or the
tool. A published Pages site is world-readable even for a private repo — keep that in mind when
adding content here.
