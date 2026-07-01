# `papers/` — drop-in papers, docs & tools for the Pages site

Put any PDF, **LaTeX source** (`.tex`), **Markdown document**, or **self-contained HTML tool** you
want published on the [GitHub Pages site](../site/index.html) **in this folder**, then add one entry to
[`catalog.json`](catalog.json). On the next deploy the Pages workflow **compiles the contributed
`papers/*.tex` to PDF** (`latexmk`, multi-pass, no bibtex), copies every `papers/*.pdf` and
`papers/*.html` onto the site, **renders every `papers/*.md` to a themed HTML page** (with LaTeX math),
and shows a card for each catalog entry — `pdf`/`doc` cards in **"Additional papers"**, `tool` cards in
**"Interactive"**. Adding a `.pdf`, `.md`, or `.html` needs **no workflow edit** — only a `.tex` does
(one line, see below).

> **`.tex` sources.** Drop a self-contained `.tex` here and it is compiled in CI exactly like the two
> λ=2c pipeline papers; the catalog entry then points at the **compiled** filename (`my_paper.pdf`, not
> `my_paper.tex`). Keep the source standalone (no `\input` of files outside `papers/`) so the CI
> `working_directory: papers` compile finds everything it needs. **One workflow edit is required:** add
> the filename to the `root_file` list of the *Compile contributed papers* step in
> [`pages.yml`](../.github/workflows/pages.yml) — this version of `latex-action` does not glob, so each
> `.tex` is listed explicitly.

> This folder is for **extra / contributed PDFs**. It is separate from the two pipelines'
> own paper sources (`lambda2c-emissiongap-verification/papers/*.tex`, compiled in CI, and
> `residual-return-verification/L00M/paper/*.pdf`), which already have their own built-in
> cards on the landing page.

## How to add a paper

1. Copy the PDF into this folder, e.g. `papers/my_paper.pdf`.
2. Add an object to the array in `catalog.json`:

```json
[
  {
    "file": "my_paper.pdf",
    "title": "Title shown on the card",
    "series": "optional small label (a project, author, or venue)",
    "pages": "12 pp",
    "tag": "PDF",
    "description": "One or two sentences describing the paper."
  }
]
```

Fields:

| field | required | notes |
|---|---|---|
| `file` | ✅ | filename **as served** (no path) — a `.pdf` (including one **compiled from a sibling `.tex`**), a `.md` when `kind` is `"doc"`, or a `.html` when `kind` is `"tool"`. For a `.tex` source, name the **compiled** PDF here. |
| `title` | ✅ | card heading |
| `description` | ✅ | one–two sentence summary |
| `kind` | optional | `"pdf"` (default), `"doc"`, or `"tool"`. A `"doc"` is a Markdown file — rendered to a themed HTML page (LaTeX math included) at deploy. A `"tool"` is a self-contained `.html` page — copied as-is and shown as an **Interactive** card. |
| `series` | optional | small label above the title (defaults to "Contributed") |
| `pages` | optional | e.g. `"24 pp"` (use `"read"` for docs, `"live"` for tools) |
| `tag` | optional | short badge text (defaults to `PDF`, or `DOC` / `TOOL`) |

For a Markdown write-up instead of a PDF, drop e.g. `notes.md` here and add
`{ "kind": "doc", "file": "notes.md", "title": "…", "description": "…" }`. Math in
`$…$` / `$$…$$` is typeset automatically.

For a self-contained interactive page, drop e.g. `widget.html` here and add
`{ "kind": "tool", "file": "widget.html", "title": "…", "description": "…" }`. It is served
as-is (keep it dependency-light), and its card appears under **Interactive**.

3. Commit both the PDF and the updated `catalog.json`, and deploy (push to the default
   branch, or run the **Deploy GitHub Pages** workflow manually). The card appears under
   *Additional papers* on the site.

An empty `catalog.json` (`[]`) simply means no extra cards yet; remove an entry (and its file) to
take a card down.

## Current contents

The files in this folder and their cards on the live site (see [`catalog.json`](catalog.json) for
the exact metadata):

**Additional papers** (`pdf` / `doc`)

| File | Card |
|---|---|
| `lehmers_box.tex` → `.pdf` | Lehmer's Box (14 pp, compiled in CI) |
| `salem_slot.pdf` | The Occupant of the Salem Slot (11 pp) |
| `generative_emptiness.pdf` | The Generative Content of a Conserved Emptiness (7 pp) |
| `operatoralgebrawhitepaper.pdf` | The Operator Algebra of the Emission Semiring (6 pp) |
| `charge_measure_coupling.tex` → `.pdf` | The Charge–Measure Coupling (13 pp, compiled in CI) |
| `z5_no_salem_dichotomy.tex` → `.pdf` | The ℤ/5ℤ Case of the No-Salem Dichotomy (9 pp, compiled in CI) |
| `lehmersproblemanintroduction.md` → `.html` | Lehmer's Problem: An Introduction (primer) |
| `EMISSIONALGEBRASPEC.md` → `.html` | Building on the Emission Algebra — a build spec |

**Interactive** (`tool`)

| File | Card |
|---|---|
| `lehmers_box_instrument.html` | Lehmer's Box — closure instrument |
| `emissionalgebracompendium.html` | The Emission Algebra — a machine-verified account |

The four pipeline-paper cards (the two λ=2c papers and the two residual-return papers) and the
Matrix Plates tool are **not** listed here — they come straight from the pipelines and are
hard-wired in [`site/index.html`](../site/index.html) and [`pages.yml`](../.github/workflows/pages.yml).

