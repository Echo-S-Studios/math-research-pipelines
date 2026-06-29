"""Self-contained HTML/SVG export, matching the tool's ``Export .html`` look.

Two documents:

* :func:`gallery_html` — a plate sheet (the tool's static export), one card per
  plate, each annotated with its characteristic *and* minimal polynomial and a
  derogatory flag (the Goal-2 information the browser tool does not yet surface).
* :func:`spectrum_html` — the Goal-1 Mahler spectrum as a page: the SVG axis on
  top, then plates grouped into ``log M`` bins below.

Both are dependency-free and use the same palette/typography as the reference.
"""

from __future__ import annotations

import html
import math
from typing import List

from .histogram import MahlerHistogram, render_svg
from .plates import Plate
from .text import fmt_num, poly_str, viridis

_EXPORT_CSS = """
body{background:#0b0d18;color:#ececf4;font-family:ui-sans-serif,system-ui,sans-serif;margin:0;padding:28px}
h1{font-family:Georgia,serif;font-weight:500}
.thesis{font-family:Georgia,serif;font-style:italic;color:#cfd3e6;max-width:64ch}
.sheet{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;margin-top:18px}
.sheet.spectrum{grid-template-columns:repeat(var(--bins,6),minmax(0,1fr));align-items:start;overflow-x:auto}
.mbin{display:flex;flex-direction:column;gap:12px;min-width:0}
.plate{position:relative;border:1px solid #23273d;border-radius:12px;background:#0f1120;padding:14px 14px 12px 18px;overflow:hidden}
.plate.fam-random{border-style:dashed;border-color:#3a4258}
.edge{position:absolute;left:0;top:0;bottom:0;width:4px}
.hd{display:flex;justify-content:space-between;align-items:baseline}
.nm{font-family:Georgia,serif;font-size:17px}
.mh,.pv,.cp,.mp,.iv{font-family:ui-monospace,Menlo,monospace}
.mh{font-size:11px;color:#cfd3e6}
.pv{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#8e93ac;margin-top:3px}
.matwrap{margin:11px 0;overflow-x:auto}
.mat{position:relative;padding:4px 11px;display:inline-block}
.mat:before,.mat:after{content:"";position:absolute;top:0;bottom:0;width:6px;border:1.5px solid #5b628a}
.mat:before{left:0;border-right:0}.mat:after{right:0;border-left:0}
.grid{display:grid;gap:2px 12px;font-family:ui-monospace,Menlo,monospace;font-size:13px}
.grid span{text-align:right;color:#eef0fb}.grid span.zero{color:#5a607e}
.lbl{font-family:ui-monospace,Menlo,monospace;font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:#8e93ac;margin-top:8px}
.cp{font-size:13px;color:#fff;margin-top:2px}
.mp{font-size:12px;color:#9fe6b0;margin-top:2px}
.mp.derog{color:#e9c46a}
.iv{font-size:11px;color:#cfd3e6;margin-top:8px}
.axiswrap{margin:14px 0 4px}
"""


def _t_for(mahler: float, max_log_m: float) -> float:
    return max(0.0, min(1.0, math.log(mahler) / max(max_log_m, 1e-6)))


def _mat_html(M: List[List[int]]) -> str:
    n = len(M)
    cells = []
    for i in range(n):
        for j in range(n):
            z = " zero" if M[i][j] == 0 else ""
            cells.append(f'<span class="{z.strip()}">{html.escape(fmt_num(M[i][j]))}</span>')
    grid = (f'<div class="matwrap"><div class="mat"><div class="grid" '
            f'style="grid-template-columns:repeat({n},auto)">{"".join(cells)}</div></div></div>')
    return grid


def _static_plate(p: Plate, max_log_m: float) -> str:
    col = viridis(_t_for(p.mahler, max_log_m))
    a = p.analysis
    derog_cls = " derog" if a.derogatory else ""
    min_lbl = "minimal polynomial" + (" (derogatory — not similar to its companion)"
                                      if a.derogatory else " (= char-poly; non-derogatory)")
    uni = " · unimodular" if a.unimodular else ""
    fam = " fam-random" if p.family == "random" else ""
    return (
        f'<div class="plate{fam}"><span class="edge" style="background:{col}"></span>'
        f'<div class="hd"><span class="nm">{html.escape(p.name)}</span>'
        f'<span class="mh">M {round(p.mahler * 1000) / 1000}</span></div>'
        f'<div class="pv">{html.escape(p.prov)}</div>'
        + _mat_html(p.M) +
        f'<div class="lbl">characteristic polynomial</div>'
        f'<div class="cp">{html.escape(poly_str(a.coeffs))}</div>'
        f'<div class="lbl">{html.escape(min_lbl)}</div>'
        f'<div class="mp{derog_cls}">{html.escape(poly_str(a.minpoly))}</div>'
        f'<div class="iv">{p.n}×{p.n} · det {html.escape(fmt_num(a.det))} · '
        f'tr {html.escape(fmt_num(a.tr))} · ρ {round(a.rho * 1000) / 1000}'
        f' · deg(min) {a.deg_min}/{a.deg_char}{uni}</div></div>'
    )


def _doc(title: str, body: str) -> str:
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)}</title><style>{_EXPORT_CSS}</style></head>'
        f'<body>{body}</body></html>'
    )


def gallery_html(plates: List[Plate], max_log_m: float | None = None) -> str:
    """A self-contained plate-sheet HTML document for *plates*."""
    if max_log_m is None:
        max_log_m = max((p.log_mahler for p in plates), default=math.log(1.6))
    body = ('<h1>Matrix Plates</h1>'
            '<p class="thesis">Each plate is an exact integer matrix, graded by the '
            'Mahler measure of its characteristic polynomial; each card also shows the '
            'minimal polynomial and whether the matrix is derogatory.</p>'
            '<div class="sheet">'
            + "".join(_static_plate(p, max_log_m) for p in plates)
            + '</div>')
    return _doc("Matrix Plates — export", body)


def spectrum_html(hist: MahlerHistogram) -> str:
    """A Mahler-spectrum page: SVG axis on top, binned plates below."""
    svg = render_svg(hist)
    cols = []
    for b in hist.bins:
        cards = "".join(_static_plate(p, hist.hi_logm) for p in b.plates)
        cols.append(f'<div class="mbin">{cards}</div>')
    body = ('<h1>Matrix Plates — Mahler spectrum</h1>'
            '<p class="thesis">Layout axis is log M with the floor pinned at M = 1 '
            '(the cyclotomic floor); the empty band up to Lehmer’s number is the '
            'Lehmer phenomenon. Dashed cards are the random control family.</p>'
            f'<div class="axiswrap">{svg}</div>'
            f'<div class="sheet spectrum" style="--bins:{hist.n_bins}">'
            + "".join(cols) + '</div>')
    return _doc("Matrix Plates — Mahler spectrum", body)
