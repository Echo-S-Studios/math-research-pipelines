"""Regression tests for the Lehmer gap and the house vs Mahler distinction."""

import unittest

from matrix_plates import (Gallery, analyse, build, build_histogram,
                           render_svg, spectral_radius)
from matrix_plates.histogram import LEHMER
from _util import JS, close


class TestLehmerGap(unittest.TestCase):
    def setUp(self):
        self.g = Gallery.seed_batch()
        self.hist = build_histogram(self.g.plates, max_log_m=self.g.max_log_m)

    def test_lehmer_constant(self):
        self.assertAlmostEqual(LEHMER, 1.17628, places=5)

    def test_floor_pinned_not_autoscaled(self):
        self.assertEqual(self.hist.lo_logm, 0.0)
        self.assertGreater(min(p.log_mahler for p in self.g.plates), 0.0)

    def test_band_empty(self):
        self.assertEqual(self.hist.lehmer_band_occupants(), [])
        self.assertGreater(min(p.mahler for p in self.g.plates), LEHMER)

    def test_no_seed_plate_in_gap(self):
        for p in self.g.plates:
            self.assertFalse(p.analysis.in_lehmer_gap, f"{p.name} unexpectedly in gap")

    def test_cyclotomic_at_floor_not_in_gap(self):
        a = analyse([[0, -1], [1, 0]])     # companion of x^2+1
        self.assertTrue(a.at_floor)
        self.assertFalse(a.in_lehmer_gap)

    def test_svg_marks_gap(self):
        svg = render_svg(self.hist)
        self.assertIn("Lehmer gap", svg)
        self.assertIn("Lehmer", svg)


class TestHouseVsMahler(unittest.TestCase):
    """House (a max) and Mahler (a product) give complementary information."""

    def test_house_equals_spectral_radius(self):
        for name in ["companion_phi", "companion_gap", "cartanE8", "ring6"]:
            a = analyse(JS[name])
            self.assertTrue(close(a.house, spectral_radius(a.roots), rel=1e-9))

    def test_sqrt2_house_and_mahler_differ(self):
        # C(√2): eigenvalues ±√2, both outside -> house = √2 but Mahler = 2.
        a = analyse(JS["companion_sq2"])
        self.assertTrue(close(a.house, 2 ** 0.5, rel=1e-9))   # ~1.414
        self.assertTrue(close(a.mahler, 2.0, rel=1e-9))
        self.assertGreater(a.mahler, a.house)                 # distinct insights

    def test_phi_house_equals_mahler(self):
        # C(φ): only one eigenvalue outside, so house == Mahler == φ.
        a = analyse(JS["companion_phi"])
        self.assertTrue(close(a.house, a.mahler, rel=1e-9))

    def test_cyclotomic_house_one(self):
        a = analyse([[0, -1], [1, 0]])
        self.assertTrue(close(a.house, 1.0, rel=1e-9))
        self.assertTrue(close(a.mahler, 1.0, rel=1e-9))


if __name__ == "__main__":
    unittest.main()
