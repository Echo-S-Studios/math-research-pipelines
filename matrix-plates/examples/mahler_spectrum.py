#!/usr/bin/env python3
"""Worked example — the Mahler spectrum of the seed batch (Goal 1).

Run:  PYTHONPATH=../src python3 mahler_spectrum.py

Bins the nine seed-batch plates in ``log M`` with the floor pinned at ``M = 1``,
prints the ASCII spectrum, and writes ``spectrum.svg`` / ``spectrum.html``.

Note on family separation: the robust signal is the EMPTY ``(1, Lehmer)`` band,
plus the structured seeds taking *discrete* characteristic Mahler values while
the random control scatters. It is NOT the case that every structured plate sits
in ``[φ, 2]`` — E₈, the Fibonacci circulant, and the frustrated ring all have
large measures; the random plate often lands mid-pack, not at the right edge.
"""

from matrix_plates import (Gallery, build_histogram, render_ascii, render_svg,
                           sorted_reflow, spectrum_html)


def main() -> None:
    g = Gallery.seed_batch()
    hist = build_histogram(g.plates, max_log_m=g.max_log_m)

    print(render_ascii(hist))
    print("\nSorted reflow (ascending M) — the lighter Goal-1 variant:")
    for p in sorted_reflow(g.plates):
        print(f"  {round(p.mahler, 3):>11}   {p.name:<12} [{p.family}]")

    with open("spectrum.svg", "w", encoding="utf-8") as fh:
        fh.write(render_svg(hist))
    with open("spectrum.html", "w", encoding="utf-8") as fh:
        fh.write(spectrum_html(hist))
    print("\nwrote spectrum.svg and spectrum.html")


if __name__ == "__main__":
    main()
