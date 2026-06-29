"""Exact linear algebra: products, big-integer powers, char-poly, det, rank."""

import unittest

from matrix_plates import char_poly, determinant, matmul, matpow, rank
from matrix_plates.linalg import (apply, identity, min_poly, poly_eq, poly_mul,
                                   trace, transpose)
from _util import JS, ORACLE


class TestPrimitives(unittest.TestCase):
    def test_matmul_identity(self):
        A = [[1, 2], [3, 4]]
        self.assertEqual(matmul(A, identity(2)), A)
        self.assertEqual(matmul(identity(2), A), A)

    def test_matmul_value(self):
        self.assertEqual(matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]]),
                         [[19, 22], [43, 50]])

    def test_transpose_trace(self):
        A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(transpose(A), [[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        self.assertEqual(trace(A), 15)

    def test_apply(self):
        self.assertEqual(apply([[0, 1], [1, 1]], [0, 1]), [1, 1])

    def test_matpow_fibonacci_bigint(self):
        # C(φ) powers list Fibonacci numbers; check a value far beyond 2**53.
        C = JS["companion_phi"]            # [[0,1],[1,1]]
        P = matpow(C, 200)
        F200 = 280571172992510140037611932413038677189525
        self.assertEqual(P[0][1], F200)    # exact big integer, no overflow
        self.assertEqual(matpow(C, 10)[0][1], 55)

    def test_matpow_zero(self):
        self.assertEqual(matpow([[2, 1], [1, 3]], 0), identity(2))


class TestCharPoly(unittest.TestCase):
    def test_matches_js_and_sympy(self):
        names = ["companion_phi", "companion_sq2", "companion_gap", "companion_K",
                 "phi_dsum_phi", "companion_of_phi2", "cartanE8", "fibcirc6",
                 "ring6", "ring5"]
        for name in names:
            with self.subTest(matrix=name):
                A = JS[name]
                coeffs, det = char_poly(A)
                self.assertEqual(coeffs, ORACLE[name]["charpoly"])
                self.assertEqual(det, ORACLE[name]["det"])

    def test_determinant_alias(self):
        self.assertEqual(determinant(JS["cartanE8"]), 1)
        self.assertEqual(determinant(JS["phi_dsum_phi"]), 1)

    def test_charpoly_rejects_non_integer(self):
        with self.assertRaises(ValueError):
            char_poly([[0.5, 1], [1, 0]])


class TestRank(unittest.TestCase):
    def test_full_and_deficient(self):
        self.assertEqual(rank([[1, 0], [0, 1]]), 2)
        self.assertEqual(rank([[1, 2], [2, 4]]), 1)        # rank-deficient
        self.assertEqual(rank([[0, 0], [0, 0]]), 0)

    def test_matches_oracle(self):
        for name in ["cartanE8", "ring6", "ring5", "phi_dsum_phi"]:
            with self.subTest(matrix=name):
                self.assertEqual(rank(JS[name]), ORACLE[name]["rank"])


class TestPolyHelpers(unittest.TestCase):
    def test_poly_mul(self):
        # (x^2 - x - 1)^2 = x^4 - 2x^3 - x^2 + 2x + 1
        self.assertEqual(poly_mul([1, -1, -1], [1, -1, -1]), [1, -2, -1, 2, 1])

    def test_poly_eq(self):
        self.assertTrue(poly_eq([1, 0, -2], [1, 0, -2]))
        self.assertFalse(poly_eq([1, 0, -2], [1, 0, -3]))


if __name__ == "__main__":
    unittest.main()
