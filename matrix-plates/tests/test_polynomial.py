"""Exact polynomial arithmetic (Poly)."""

import unittest
from fractions import Fraction

from matrix_plates.polynomial import Poly


class TestPoly(unittest.TestCase):
    def test_roundtrip_high_low(self):
        p = Poly.from_high_low([1, -2, -1, 2, 1])
        self.assertEqual(p.to_high_low(), [1, -2, -1, 2, 1])
        self.assertEqual(p.degree, 4)

    def test_arithmetic(self):
        a = Poly.from_high_low([1, -1, -1])      # x^2 - x - 1
        self.assertEqual((a + a).to_high_low(), [2, -2, -2])
        self.assertEqual((a - a).to_high_low(), [0])
        self.assertEqual((a * a).to_high_low(), [1, -2, -1, 2, 1])
        self.assertEqual((a * 3).to_high_low(), [3, -3, -3])

    def test_divmod_exact(self):
        big = Poly.from_high_low([1, -2, -1, 2, 1])   # (x^2-x-1)^2
        d = Poly.from_high_low([1, -1, -1])           # x^2-x-1
        q, r = big.divmod(d)
        self.assertEqual(q.to_high_low(), [1, -1, -1])
        self.assertTrue(r.is_zero)

    def test_divmod_remainder(self):
        q, r = Poly.from_high_low([1, 0, 0]).divmod(Poly.from_high_low([1, -1]))  # x^2 / (x-1)
        self.assertEqual(q.to_high_low(), [1, 1])     # x + 1
        self.assertEqual(r.to_high_low(), [1])        # remainder 1

    def test_gcd_monic(self):
        big = Poly.from_high_low([1, -2, -1, 2, 1])
        d = Poly.from_high_low([1, -1, -1])
        g = big.gcd(d)
        self.assertTrue(g.is_monic())
        self.assertEqual(g.to_high_low(), [1, -1, -1])

    def test_squarefree(self):
        self.assertTrue(Poly.from_high_low([1, -1, -1]).is_squarefree())   # x^2-x-1
        self.assertFalse(Poly.from_high_low([1, -2, 1]).is_squarefree())   # (x-1)^2
        self.assertFalse(Poly.from_high_low([1, -2, -1, 2, 1]).is_squarefree())  # (x^2-x-1)^2

    def test_deriv_and_eval(self):
        p = Poly.from_high_low([1, 0, -1])            # x^2 - 1
        self.assertEqual(p.deriv().to_high_low(), [2, 0])   # 2x
        self.assertEqual(p.eval(2), Fraction(3))

    def test_latex(self):
        self.assertEqual(Poly.from_high_low([1, -1, -1]).latex(), "x^{2} - x - 1")
        self.assertEqual(Poly.from_high_low([1, 0, 1]).latex(), "x^{2} + 1")


if __name__ == "__main__":
    unittest.main()
