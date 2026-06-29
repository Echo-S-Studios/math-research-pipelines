"""Goal 1 — Mahler-spectrum histogram behaviour."""

import math
import unittest

from matrix_plates import (Gallery, build, build_histogram, family_of,
                           render_ascii, render_svg, sorted_reflow,
                           spectrum_bins)
from matrix_plates.histogram import LEHMER
from matrix_plates.plates import build_plate


def _phi_plus_phi_plate():
    return build_plate(build("dsum", a="phi", b="phi"), 1)


class TestBinning(unittest.TestCase):
    def setUp(self):
        self.g = Gallery.seed_batch()
        self.hist = build_histogram(self.g.plates, max_log_m=self.g.max_log_m)

    def test_floor_pinned_at_M1(self):
        # The left edge is log(1) = 0, NOT the data minimum (log φ ≈ 0.48).
        self.assertEqual(self.hist.lo_logm, 0.0)
        self.assertEqual(self.hist.bins[0].lo_logm, 0.0)
        self.assertAlmostEqual(self.hist.bins[0].lo_m, 1.0)

    def test_not_autoscaled_to_minimum(self):
        min_log = min(p.log_mahler for p in self.g.plates)
        self.assertGreater(min_log, 0.0)          # smallest plate is φ, log φ > 0
        self.assertLess(self.hist.lo_logm, min_log)  # floor still sits below it

    def test_lehmer_band_empty(self):
        # No stock seed lands in (1, L): the Lehmer phenomenon.
        self.assertEqual(self.hist.lehmer_band_occupants(), [])
        self.assertGreater(min(p.mahler for p in self.g.plates), LEHMER)

    def test_bin_assignment_consistent(self):
        for b in self.hist.bins:
            for p in b.plates:
                self.assertEqual(self.hist.bin_of(p), b.index)

    def test_within_bin_sorted(self):
        for b in self.hist.bins:
            ms = [p.mahler for p in b.plates]
            self.assertEqual(ms, sorted(ms))

    def test_all_plates_binned_once(self):
        total = sum(b.count for b in self.hist.bins)
        self.assertEqual(total, len(self.g.plates))


class TestBinHeuristic(unittest.TestCase):
    def test_sqrt_rule_clamped(self):
        self.assertEqual(spectrum_bins(1), 3)      # clamped up
        self.assertEqual(spectrum_bins(9), 3)      # ceil(sqrt 9) = 3
        self.assertEqual(spectrum_bins(10), 4)     # ceil(sqrt 10) = 4
        self.assertEqual(spectrum_bins(200), 12)   # clamped down (ceil sqrt = 15)


class TestReflowAndFamily(unittest.TestCase):
    def test_sorted_reflow_monotone(self):
        g = Gallery.seed_batch()
        ms = [p.mahler for p in sorted_reflow(g.plates)]
        self.assertEqual(ms, sorted(ms))

    def test_family_of(self):
        self.assertEqual(family_of("seeded mulberry32 · n=4"), "random")
        self.assertEqual(family_of("companion · ℚ(√5)"), "structured")
        self.assertEqual(family_of("cartan · rank 8 · unimodular"), "structured")


class TestEdgeCases(unittest.TestCase):
    def test_empty_gallery(self):
        h = build_histogram([])
        self.assertEqual(h.bins, [])
        self.assertEqual(h.n_bins, 0)

    def test_single_plate_no_div_by_zero(self):
        p = build_plate(build("companion", a="phi"), 1)
        h = build_histogram([p])               # span floored at log(1.18)
        self.assertGreater(h.span, 0.0)
        self.assertEqual(sum(b.count for b in h.bins), 1)


class TestRenderers(unittest.TestCase):
    def test_ascii_mentions_floor_and_lehmer(self):
        g = Gallery.seed_batch()
        txt = render_ascii(build_histogram(g.plates, max_log_m=g.max_log_m))
        self.assertIn("M = 1", txt)
        self.assertIn("Lehmer", txt)
        self.assertIn("EMPTY", txt)

    def test_svg_is_wellformed_svg(self):
        g = Gallery.seed_batch()
        svg = render_svg(build_histogram(g.plates, max_log_m=g.max_log_m))
        self.assertTrue(svg.lstrip().startswith("<svg"))
        self.assertTrue(svg.rstrip().endswith("</svg>"))
        self.assertIn("Lehmer", svg)


if __name__ == "__main__":
    unittest.main()
