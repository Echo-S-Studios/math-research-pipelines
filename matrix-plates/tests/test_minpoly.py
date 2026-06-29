"""Exact minimal polynomial — the Goal-2 workhorse — vs the sympy oracle."""

import unittest

from matrix_plates import min_poly
from matrix_plates.operators import companion
from _util import JS, ORACLE


class TestMinPoly(unittest.TestCase):
    def test_matches_oracle(self):
        names = ["companion_phi", "companion_sq2", "companion_gap", "companion_K",
                 "phi_dsum_phi", "companion_of_phi2", "cartanE8", "fibcirc6",
                 "ring6", "ring5"]
        for name in names:
            with self.subTest(matrix=name):
                self.assertEqual(min_poly(JS[name]), ORACLE[name]["minpoly"])

    def test_derogatory_phi_plus_phi(self):
        # φ ⊕ φ : char-poly (x²−x−1)² but min-poly x²−x−1 (degree 2 < 4).
        mp = min_poly(JS["phi_dsum_phi"])
        self.assertEqual(mp, [1, -1, -1])
        self.assertEqual(len(mp) - 1, 2)

    def test_companion_is_nonderogatory(self):
        # A companion matrix is always non-derogatory: min-poly == char-poly.
        for sid_poly in ([1, -1, -1], [1, 0, -2], [1, -7, 1], [1, 0, 5, 0, -5]):
            with self.subTest(poly=sid_poly):
                C = companion(sid_poly)
                self.assertEqual(min_poly(C), sid_poly)

    def test_degree_one(self):
        self.assertEqual(min_poly([[7]]), [1, -7])
        self.assertEqual(min_poly([[-3]]), [1, 3])

    def test_identity_minpoly(self):
        # I_n has minimal polynomial (x - 1), degree 1, derogatory for n >= 2.
        self.assertEqual(min_poly([[1, 0], [0, 1]]), [1, -1])

    def test_rejects_non_integer(self):
        with self.assertRaises(ValueError):
            min_poly([[0.5, 1.0], [1.0, 0.0]])


if __name__ == "__main__":
    unittest.main()
