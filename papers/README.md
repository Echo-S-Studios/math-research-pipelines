# `papers/` — drop-in PDFs for the Pages site

Put any PDF **or Markdown document** you want published on the
[GitHub Pages site](../site/index.html) **in this folder**, then add one entry to
[`catalog.json`](catalog.json). On the next deploy the Pages workflow copies every
`papers/*.pdf` onto the site, **renders every `papers/*.md` to a themed HTML page** (with
LaTeX math), and shows an **"Additional papers"** card for each catalog entry — no HTML or
workflow edits required.

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
| `file` | ✅ | filename in this folder (no path) — a `.pdf`, or a `.md` when `kind` is `"doc"` |
| `title` | ✅ | card heading |
| `description` | ✅ | one–two sentence summary |
| `kind` | optional | `"pdf"` (default) or `"doc"`. A `"doc"` is a Markdown file — rendered to a themed HTML page (LaTeX math included) at deploy; the card links to that page |
| `series` | optional | small label above the title (defaults to "Contributed") |
| `pages` | optional | e.g. `"24 pp"` (use `"read"` for docs) |
| `tag` | optional | short badge text (defaults to `PDF`, or `DOC` for docs) |

For a Markdown write-up instead of a PDF, drop e.g. `notes.md` here and add
`{ "kind": "doc", "file": "notes.md", "title": "…", "description": "…" }`. Math in
`$…$` / `$$…$$` is typeset automatically.

3. Commit both the PDF and the updated `catalog.json`, and deploy (push to the default
   branch, or run the **Deploy GitHub Pages** workflow manually). The card appears under
   *Additional papers* on the site.

`catalog.json` ships as an empty list `[]`; that simply means no extra cards yet.
