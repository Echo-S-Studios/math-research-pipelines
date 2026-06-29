"""Goal 1 — Mahler measure as the layout axis.

Promotes ``M`` from a colour to the *layout axis*: a one-dimensional spectrum
graded by ``log M``. Three deliberate choices, each defended in the build spec:

1. **Axis is ``log M``, not ``M``.** For a monic integer polynomial ``log M`` is
   the topological entropy of the associated ``Z``-action (Lind–Schmidt–Ward,
   *Invent. Math.* 101, 1990), and Mahler measures compose multiplicatively, so
   the additive/uniform axis is logarithmic. Binning in ``log M`` gives
   equal-entropy buckets.
2. **Floor pinned at ``M = 1``, never auto-scaled to the data minimum.**
   ``M(p) = 1`` iff ``p`` is a product of cyclotomics and a monomial (Kronecker).
   The smallest known measure ``> 1`` is Lehmer's number ``L ≈ 1.17628`` (Lehmer,
   *Ann. of Math.*, 1933); whether anything lies in the open gap ``(1, L)`` is
   unsolved. Pinning the left edge at ``M = 1`` keeps that gap visible as
   deliberate empty space — the **Lehmer phenomenon**.
3. **Histogram, not a plain sort.** Sorting shows order; it does not show
   *density*. A histogram in ``log M`` shows clustering. The lighter sorted
   reflow is provided too (:func:`sorted_reflow`) with a comparison in
   :func:`comparison_table`.

A precise note on family separation (sharpening the colloquial framing): the
robust, defensible signal is **the empty ``(1, L)`` band**, plus the fact that the
structured seeds take *discrete characteristic* Mahler values while the random
control scatters continuously. It is **not** true that every structured plate
sits in ``[φ, 2]`` — only the quadratic units (``φ``, ``τ``, ``√2``) do; ``E₈``,
the Fibonacci circulant, and the frustrated ring all have large measures and sit
far right alongside random plates. See the build spec's *Precision* note.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .plates import Plate
from .text import fmt_num, viridis

#: Smallest known Mahler measure > 1 (Lehmer 1933); re-exported from invariants.
from .invariants import LEHMER  # single source of truth
#: Cyclotomic floor (Kronecker): M = 1.
FLOOR = 1.0
#: log-M floor used for tiny galleries so the Lehmer marker stays on-axis.
_MIN_HI_LOGM = math.log(1.18)

_RANDOM_PROV = re.compile(r"^seeded mulberry32")


def family_of(prov: str) -> str:
    """``'random'`` if *prov* is the seeded-control family, else ``'structured'``.

    Keyed on the provenance prefix exactly as the tool's ``familyOf`` — only the
    seeded-random plate matches ``^seeded mulberry32``.
    """
    return "random" if _RANDOM_PROV.match(prov) else "structured"


def spectrum_bins(n: int) -> int:
    """Bin count: ``clamp(ceil(sqrt(n)), 3, 12)``.

    The ``√n`` rule sits between Sturges (``⌈log₂n⌉+1``) and the Rice rule
    (``⌈2n^{1/3}⌉``); the clamp keeps the grid legible. (Sturges 1926; Scott,
    *Biometrika* 1979.)
    """
    return max(3, min(12, math.ceil(math.sqrt(max(1, n)))))


@dataclass
class Bin:
    """One histogram column: a ``log M`` interval and the plates that fall in it."""

    index: int
    lo_logm: float
    hi_logm: float
    plates: List[Plate] = field(default_factory=list)

    @property
    def lo_m(self) -> float:
        return math.exp(self.lo_logm)

    @property
    def hi_m(self) -> float:
        return math.exp(self.hi_logm)

    @property
    def count(self) -> int:
        return len(self.plates)

    def family_counts(self) -> Dict[str, int]:
        out = {"structured": 0, "random": 0}
        for p in self.plates:
            out[p.family] += 1
        return out


@dataclass
class MahlerHistogram:
    """A binned spectrum of plates over ``log M`` with the floor pinned at M=1."""

    bins: List[Bin]
    plates: List[Plate]
    n_bins: int
    lo_logm: float          # always 0.0 (the M=1 floor)
    hi_logm: float
    span: float
    floor_m: float = FLOOR
    lehmer_m: float = LEHMER

    @property
    def m_max(self) -> float:
        return math.exp(self.hi_logm)

    def lehmer_fraction(self) -> float:
        """Position of the Lehmer marker as a fraction of the axis ``[0, 1]``."""
        return math.log(self.lehmer_m) / self.span if self.span else 0.0

    def lehmer_band_occupants(self) -> List[Plate]:
        """Plates landing in the open band ``(1, L)`` — expected to be empty."""
        return [p for p in self.plates if FLOOR < p.mahler < self.lehmer_m]

    def bin_of(self, plate: Plate) -> int:
        """The bin index a plate falls in (recomputed; matches :func:`build_histogram`)."""
        k = int(math.floor(plate.log_mahler / (self.span or 1.0) * self.n_bins))
        return max(0, min(self.n_bins - 1, k))


def build_histogram(plates: List[Plate],
                    max_log_m: Optional[float] = None) -> MahlerHistogram:
    """Bin *plates* in ``log M`` with the floor pinned at ``M = 1``.

    The bin assignment is exactly the spec's: ``k = floor(log M / span * B)``
    clamped to ``[0, B-1]``, where ``span = max(max_log_m, log 1.18)`` so the
    Lehmer marker stays on-axis for tiny galleries. Within each bin, plates are
    sorted by ``M`` for a clean gradient. ``O(n)`` bucketing + ``O(n log n)``
    worst case (all in one bin).
    """
    if not plates:
        return MahlerHistogram(bins=[], plates=[], n_bins=0, lo_logm=0.0,
                               hi_logm=_MIN_HI_LOGM, span=_MIN_HI_LOGM)
    if max_log_m is None:
        max_log_m = max(p.log_mahler for p in plates)
    hi = max(max_log_m, _MIN_HI_LOGM)
    span = hi if hi else 1.0
    B = spectrum_bins(len(plates))
    buckets: List[List[Plate]] = [[] for _ in range(B)]
    for p in plates:
        k = int(math.floor(p.log_mahler / span * B))
        if k >= B:
            k = B - 1
        if k < 0:
            k = 0
        buckets[k].append(p)
    bins: List[Bin] = []
    for i in range(B):
        buckets[i].sort(key=lambda p: (p.mahler, p.id))   # deterministic on near-equal M
        bins.append(Bin(index=i, lo_logm=i / B * span,
                        hi_logm=(i + 1) / B * span, plates=buckets[i]))
    return MahlerHistogram(bins=bins, plates=list(plates), n_bins=B,
                           lo_logm=0.0, hi_logm=hi, span=span)


def sorted_reflow(plates: List[Plate]) -> List[Plate]:
    """The lighter Goal-1 variant: plates in ascending ``M`` order, no bins.

    Shows monotone order with maximal plate width. Use when you only need a
    ranking, not the family-separation density a histogram reveals. ``O(n log n)``.
    """
    return sorted(plates, key=lambda p: p.mahler)


# --- renderers ------------------------------------------------------------------
def render_ascii(hist: MahlerHistogram, width: int = 32) -> str:
    """Render the histogram as a monospaced report (bins, ranges, family split)."""
    if not hist.bins:
        return "Mahler spectrum: (empty)"
    mx = max((b.count for b in hist.bins), default=1) or 1
    lines: List[str] = []
    lines.append("Mahler spectrum — log M binning, floor pinned at M = 1 (Kronecker)")
    lines.append(
        f"  {len(hist.plates)} plates · {hist.n_bins} bins · "
        f"M ∈ [{fmt_num(min(p.mahler for p in hist.plates))}, "
        f"{fmt_num(hist.m_max)}] · span(log M) = {hist.span:.3f}"
    )
    lines.append("")
    lines.append("  bin  M-range                       count  bar"
                 + " " * (width - 1) + "families")
    rule = "  " + "─" * (width + 56)
    lines.append(rule)
    for b in hist.bins:
        bar = "█" * max(0, round(b.count / mx * width))
        fam = b.family_counts()
        rng = f"[{fmt_num(b.lo_m):>8}, {fmt_num(b.hi_m):>9}{']' if b.index == hist.n_bins - 1 else ')'}"
        lines.append(
            f"  {b.index:>3}  {rng:<28}  {b.count:>4}   "
            f"{bar:<{width}} S:{fam['structured']} R:{fam['random']}"
        )
    lines.append(rule)
    # markers
    lehmer_pct = hist.lehmer_fraction() * 100
    band = hist.lehmer_band_occupants()
    lines.append(f"  floor   M=1     cyclotomic floor (Kronecker)         ← left edge")
    lines.append(f"  Lehmer  L≈{LEHMER:.5f}  smallest known measure > 1   at {lehmer_pct:.1f}% of axis")
    if band:
        names = ", ".join(p.name for p in band)
        lines.append(f"  ⚠ {len(band)} plate(s) inside the (1, L) band: {names}")
    else:
        lines.append("  (1, L) Lehmer band is EMPTY — the Lehmer phenomenon (expected)")
    return "\n".join(lines)


def render_svg(hist: MahlerHistogram,
               width: int = 760, height: int = 380) -> str:
    """Standalone SVG of the spectrum, in the tool's palette.

    Viridis bars (coloured by bin-centre ``log M`` fraction), a teal ``M = 1``
    floor tick, a gold ``Lehmer`` tick, and a right-edge ``M_max`` tick. The SVG
    is self-contained (no external CSS/JS) so it renders anywhere.
    """
    pad_l, pad_r, pad_t, pad_b = 48, 24, 36, 56
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base_y = pad_t + plot_h
    if not hist.bins:
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
                f'<rect width="{width}" height="{height}" fill="#0b0d18"/></svg>')
    mx = max((b.count for b in hist.bins), default=1) or 1
    bw = plot_w / hist.n_bins
    parts: List[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
                 f'font-family="ui-monospace,Menlo,monospace">')
    parts.append(f'<rect width="{width}" height="{height}" rx="14" fill="#0b0d18"/>')
    parts.append(f'<text x="{pad_l}" y="22" fill="#ececf4" font-size="14" '
                 f'font-family="Georgia,serif">Mahler spectrum · log M · floor at M=1</text>')
    # bars
    for b in hist.bins:
        h = (b.count / mx) * plot_h
        x = pad_l + b.index * bw
        center_frac = ((b.index + 0.5) / hist.n_bins)
        col = viridis(center_frac)
        fam = b.family_counts()
        parts.append(f'<rect x="{x + 2:.1f}" y="{base_y - h:.1f}" width="{bw - 4:.1f}" '
                     f'height="{h:.1f}" fill="{col}" opacity="0.92" rx="3"/>')
        if fam["random"]:
            # mark the random share with a dashed outline (control family)
            parts.append(f'<rect x="{x + 2:.1f}" y="{base_y - h:.1f}" width="{bw - 4:.1f}" '
                         f'height="{h:.1f}" fill="none" stroke="#3a4258" '
                         f'stroke-dasharray="4 3" rx="3"/>')
        if b.count:
            parts.append(f'<text x="{x + bw / 2:.1f}" y="{base_y - h - 6:.1f}" '
                         f'fill="#cfd3e6" font-size="11" text-anchor="middle">{b.count}</text>')
    # baseline
    parts.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l + plot_w}" y2="{base_y}" '
                 f'stroke="#23273d"/>')

    def fx(frac: float) -> float:
        return pad_l + max(0.0, min(1.0, frac)) * plot_w

    # Lehmer gap (1, L): conjecturally empty — shade it so the emptiness is explicit
    lf0 = hist.lehmer_fraction()
    parts.append(f'<rect x="{fx(0):.1f}" y="{pad_t}" width="{(fx(lf0) - fx(0)):.1f}" '
                 f'height="{plot_h:.1f}" fill="#e9c46a" opacity="0.07"/>')
    parts.append(f'<text x="{(fx(0) + fx(lf0)) / 2:.1f}" y="{pad_t + 12:.1f}" fill="#e9c46a" '
                 f'font-size="9" text-anchor="middle" opacity="0.85">Lehmer gap</text>')
    # floor tick (M=1) — teal, left edge
    parts.append(f'<line x1="{fx(0):.1f}" y1="{pad_t}" x2="{fx(0):.1f}" y2="{base_y + 6}" '
                 f'stroke="#5cc9c0" stroke-dasharray="4 4"/>')
    parts.append(f'<text x="{fx(0):.1f}" y="{base_y + 22}" fill="#5cc9c0" font-size="10" '
                 f'text-anchor="middle">M=1</text>')
    # Lehmer tick — gold
    lf = hist.lehmer_fraction()
    parts.append(f'<line x1="{fx(lf):.1f}" y1="{pad_t}" x2="{fx(lf):.1f}" y2="{base_y + 6}" '
                 f'stroke="#e9c46a" stroke-dasharray="4 4"/>')
    parts.append(f'<text x="{fx(lf):.1f}" y="{base_y + 36}" fill="#e9c46a" font-size="10" '
                 f'text-anchor="middle">Lehmer {LEHMER:.3f}</text>')
    # M_max tick — right edge
    parts.append(f'<text x="{fx(1):.1f}" y="{base_y + 22}" fill="#8e93ac" font-size="10" '
                 f'text-anchor="end">M_max {fmt_num(hist.m_max)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def comparison_table() -> str:
    """Markdown comparison of the histogram (primary) vs the sorted reflow."""
    return (
        "| Mode | Shows | Cost/add | Plate width | Use when |\n"
        "|---|---|---|---|---|\n"
        "| Histogram (primary) | clustering + family separation + M axis | O(n log n) "
        "| shared per bin | demonstrating the Lehmer spectrum |\n"
        "| Sorted reflow | monotone order only | O(n log n) | full grid width "
        "| you just want plates ranked by M |"
    )
