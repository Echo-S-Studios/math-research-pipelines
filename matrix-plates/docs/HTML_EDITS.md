# Edits to `matrix_plates.html`

`web/matrix_plates.html` is the upstream reference tool with the two build-spec
features applied. This file is the change record; the **byte-exact, apply-able
diff** is [`matrix_plates.html.patch`](matrix_plates.html.patch), and the full
rationale is in [`matrix_plates_build_spec.md`](matrix_plates_build_spec.md).

## Provenance (checksums)

| Artifact | SHA-256 |
|---|---|
| upstream reference (unpatched) | `97187b781289324e9e8ee725138dcec0fd389b08a6dcb7a8140561e225442ca3` |
| `web/matrix_plates.html` (patched, shipped, v1.1.2) | `fd6db69c181ca014934739b7580471644121bbb81988d61061d3f4f98cbfa04d` |

The diff is 16 hunks (12 from v1.0 + 4 from v1.1). Applying it to the reference reproduces the shipped file
exactly (verified below).

## Reproduce / verify the patch

```bash
# from a directory containing the UNPATCHED reference matrix_plates.html:
patch -p1 < docs/matrix_plates.html.patch
sha256sum matrix_plates.html
#   -> fd6db69c181ca014934739b7580471644121bbb81988d61061d3f4f98cbfa04d

# or check-only, without writing (needs git):
git apply --check docs/matrix_plates.html.patch
```

If you only have the patched file (the normal case), no action is needed — it is
already the finished tool. The patch exists so the transformation is auditable and
re-runnable against a fresh copy of the reference.

## The edits (v1.0: 13 named changes)

All edits are anchored to existing functions or markup, not line numbers. The two
features are independent (either may be applied alone) but compose.

### Goal 1 — Mahler measure as the layout axis

| # | Region (anchor) | Change |
|---|---|---|
| 1 | end of `<style>` | spectrum / axis / family CSS (`.sheet.spectrum`, `.mbin`, `.maxis`, `.plate.fam-random`) |
| 2 | `.console`, after the `ctlSeedInt` block | `Layout` `<select>` (Insertion / Mahler spectrum) |
| 3 | before `<div class="sheet" id="sheet">` | `<div id="maxis">` axis ruler |
| 4 | state, after `let uid=0;` | `layoutMode`, `PLATE_NODES`, `familyOf`, `spectrumBins` |
| 5 | replace `addPlate` | unified version routing through `relayout()` (node reuse, no animation replay) |
| 6 | after `recolorAll` | `relayout` (log-M histogram, floor pinned at M=1) + `drawMahlerAxis` |
| 7 | replace the `clear` handler | reset `PLATE_NODES` + axis via `relayout()` |
| 8 | near the `gen`/`batch` listeners | wire `#layout` change → `relayout()` |

### Goal 2 — `charpoly ↦ companion` closure

| # | Region (anchor) | Change |
|---|---|---|
| 9 | `plateHTML`, between `.chips` and `.p-toggle` | `.p-lift` button (`↦ companion seed`) |
| 10 | append inside `wirePlate` | wire `.p-lift` → `liftToSeed` |
| 11 | after the `seedById` derived map | `SIG_TO_ID`, `bySig`, `genCount` (polynomial-signature dedupe) |
| 12 | near the console wiring | `liftToSeed`, `refreshSeedMenus` (self-extending registry) |
| 13 | end of `<style>` | `.p-lift` CSS |

(Patches 1 and 13 are both CSS appended before `</style>`, applied as a single
block in the shipped file; the diff shows them together.)

## v1.1 additions (web tooling)

Three further edits make the tool a standalone analyser, independent of the Python
backend, matching the v1.1 CLI/library features:

| # | Region (anchor) | Change |
|---|---|---|
| v1.1-a | `OPS` catalogue + console markup + `readParams`/`syncControls` + `ctl` map | **Custom matrix** construction: a textarea (`#cmatrix`) parsed by `parseMatrix` (rows on lines, space/comma-separated, or JSON), with square/integer validation and specific error messages |
| v1.1-b | `plateHTML` detail + `wirePlate` | inline **companion-form panel** (`companion(charpoly)` rendered next to the plate) and a one-line similarity note |
| v1.1-c | after `liftToSeed`; CSS before `</style>` | per-plate **export buttons** — `exportPlate` writes JSON, LaTeX (`bmatrixLatex` + `polyLatex`), or runnable SymPy via `downloadText`; plus the supporting styles |
| v1.1.1-d | before `analyse`; `plateHTML` chips + detail; `companionPanel`; `exportPlate` JSON | **exact rational engine** (`Frac` BigInt + `ℚ[x]` polynomials + Smith normal form `smithDiagonal`/`invariantFactorsExact`) → inline **minimal polynomial**, **invariant factors**, `derogatory`/`defective` chips, and the exact companion similarity verdict |
| v1.1.2-e | `minPolyKrylov`, `matmulBig`, `invariantInfo` (hybrid) | fraction-free rational **Krylov** minimal polynomial (exact BigInt matrix powers) drives a **hybrid**: non-derogatory → `[charpoly]` directly (no Smith swell); Smith form runs only for derogatory matrices. The `n ≤ 12` cap is lifted — min-poly / flags compute at any size; only the full factor *list* for derogatory `n > SNF_MAX_N` (24) defers |

These are additive and independent of the Goal 1 / Goal 2 edits.

## Validation of the patched file

- JavaScript passes `node --check` (syntax).
- Loads without runtime error under a headless DOM shim; `spectrumBins`,
  `familyOf`, `companion`, `charPoly`, and `analyse` return values matching the
  Python backend and the sympy oracle (e.g. `analyse(φ⊕φ).mahler ≈ 2.618034`).
- v1.1 functions validated under the DOM shim: `parseMatrix` (valid / non-square
  / non-integer), `OPS.custom.build`, `polyLatex`, `bmatrixLatex`, `sanitizeName`,
  and `companion(charPoly(φ⊕φ))` all match the Python backend.
- v1.1.1 exact engine validated against the backend on a 14-matrix battery
  (derogatory `φ⊕φ`, defective Jordan/nilpotent, cyclotomic, identity/zero/scalar,
  `E₈` 8×8, `kron` 4×4): invariant factors, minimal polynomial, `derogatory`,
  `defective`, and `isSimilar` agree exactly.
- v1.1.2 hybrid validated against the backend on a 378-matrix fuzz (355
  non-derogatory exercising the `[charpoly]` path, 23 derogatory exercising the
  Smith path): invariant factors, minimal polynomial, `derogatory`, `defective`
  all agree exactly, including the `kron(res,res)` 16×16 case that revealed the
  float-overflow bug now fixed by exact BigInt matrix powers.
- Shares a bit-exact `mulberry32` PRNG with the Python package, so a
  `(construction, seeds, params, RNG seed)` tuple reproduces the same matrix in
  both tools.
