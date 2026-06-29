"""analyse(): the full invariant bundle, checked against the sympy oracle."""

import unittest

from matrix_plates import analyse
from _util import JS, ORACLE, close


class TestAnalyse(unittest.TestCase):
    NAMES = ["companion_phi", "companion_sq2", "companion_gap", "companion_K",
             "phi_dsum_phi", "companion_of_phi2", "cartanE8", "fibcirc6",
             "ring6", "ring5"]

    def test_exact_integer_invariants(self):
        for name in self.NAMES:
            with self.subTest(matrix=name):
                a = analyse(JS[name])
                o = ORACLE[name]
                self.assertEqual(a.det, o["det"])
                self.assertEqual(a.tr, o["trace"])
                self.assertEqual(a.rank, o["rank"])
                self.assertEqual(a.coeffs, o["charpoly"])
                self.assertEqual(a.minpoly, o["minpoly"])
                self.assertEqual(a.deg_char, o["deg_char"])
                self.assertEqual(a.deg_min, o["deg_min"])
                self.assertEqual(a.derogatory, o["derogatory"])

    def test_float_invariants_within_tolerance(self):
        for name in self.NAMES:
            with self.subTest(matrix=name):
                a = analyse(JS[name])
                o = ORACLE[name]
                self.assertTrue(close(a.mahler, o["mahler"], rel=1e-3),
                                f"{name}: M {a.mahler} vs {o['mahler']}")
                self.assertTrue(close(a.rho, o["rho"], rel=1e-3),
                                f"{name}: rho {a.rho} vs {o['rho']}")

    def test_unimodular_flag(self):
        self.assertTrue(analyse(JS["cartanE8"]).unimodular)        # det 1
        self.assertTrue(analyse(JS["phi_dsum_phi"]).unimodular)    # det 1
        self.assertFalse(analyse(JS["companion_K"]).unimodular)    # det -5

    def test_unit_circle_classification(self):
        a = analyse(JS["companion_phi"])     # φ outside, ψ inside
        self.assertEqual((a.outside, a.on, a.inside), (1, 0, 1))
        a2 = analyse(JS["companion_sq2"])    # ±√2 both outside
        self.assertEqual((a2.outside, a2.on, a2.inside), (2, 0, 0))

    def test_mahler_closed_forms(self):
        phi = (1 + 5 ** 0.5) / 2
        self.assertTrue(close(analyse(JS["companion_phi"]).mahler, phi, rel=1e-9))
        self.assertTrue(close(analyse(JS["companion_sq2"]).mahler, 2.0, rel=1e-9))
        self.assertTrue(close(analyse(JS["phi_dsum_phi"]).mahler, phi * phi, rel=1e-9))


if __name__ == "__main__":
    unittest.main()
