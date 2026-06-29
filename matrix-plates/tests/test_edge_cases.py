"""Edge cases: derogatory, defective, repeated eigenvalues, cyclotomic, singular."""

import unittest

from matrix_plates import analyse
from _util import JS, close


class TestDerogatoryVsDefective(unittest.TestCase):
    """derogatory (min deg < n) and defective (non-diagonalizable) are independent."""

    def test_derogatory_not_defective(self):
        # φ ⊕ φ: repeated eigenvalues but diagonalizable -> derogatory, NOT defective
        a = analyse(JS["phi_dsum_phi"])
        self.assertTrue(a.derogatory)
        self.assertFalse(a.defective)
        self.assertEqual(a.num_invariant_factors, 2)

    def test_defective_not_derogatory(self):
        # single Jordan block at 1: non-diagonalizable -> defective, NOT derogatory
        a = analyse([[1, 1], [0, 1]])
        self.assertTrue(a.defective)
        self.assertFalse(a.derogatory)
        self.assertEqual(a.num_invariant_factors, 1)

    def test_both(self):
        # I2 ⊕ Jordan(1) style: companion of (x^2-x-1)^2 is defective (repeated roots),
        # non-derogatory (single invariant factor)
        a = analyse(JS["companion_of_phi2"])
        self.assertTrue(a.defective)         # (x^2-x-1)^2 not squarefree
        self.assertFalse(a.derogatory)

    def test_diagonalizable_distinct(self):
        a = analyse(JS["companion_phi"])     # distinct real eigenvalues
        self.assertFalse(a.defective)
        self.assertFalse(a.derogatory)


class TestRepeatedAndIdentity(unittest.TestCase):
    def test_identity_is_maximally_derogatory(self):
        a = analyse([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertTrue(a.derogatory)
        self.assertFalse(a.defective)        # diagonal -> diagonalizable
        self.assertEqual(a.num_invariant_factors, 3)   # (x-1),(x-1),(x-1)
        # Exact Kronecker floor: the only eigenvalue is 1 (min-poly x-1), so M = 1
        # exactly. The float Mahler carries Durand-Kerner fuzz on the triple root
        # (~1.00001), so assert the exact integer facts, not the float.
        self.assertEqual(a.minpoly, [1, -1])
        self.assertEqual((a.outside, a.on, a.inside), (0, 3, 0))

    def test_scalar_repeated(self):
        a = analyse([[2, 0], [0, 2]])        # 2I: invariant factors (x-2),(x-2)
        self.assertEqual(a.invariant_factors, [[1, -2], [1, -2]])
        self.assertTrue(a.derogatory)


class TestCyclotomicFloor(unittest.TestCase):
    def test_companion_x2_plus_1(self):
        a = analyse([[0, -1], [1, 0]])       # roots ±i
        self.assertTrue(close(a.mahler, 1.0))
        self.assertTrue(close(a.house, 1.0))
        self.assertTrue(a.at_floor)
        self.assertFalse(a.in_lehmer_gap)
        self.assertEqual((a.outside, a.on, a.inside), (0, 2, 0))


class TestSingularNilpotent(unittest.TestCase):
    def test_nilpotent(self):
        a = analyse([[0, 1], [0, 0]])        # nilpotent: x^2
        self.assertEqual(a.det, 0)
        self.assertEqual(a.coeffs, [1, 0, 0])
        self.assertEqual(a.minpoly, [1, 0, 0])  # x^2 (single Jordan block)
        self.assertTrue(a.defective)
        self.assertFalse(a.derogatory)
        self.assertTrue(close(a.house, 0.0))
        self.assertEqual(a.rank, 1)

    def test_zero_matrix(self):
        a = analyse([[0, 0], [0, 0]])
        self.assertEqual(a.rank, 0)
        self.assertEqual(a.minpoly, [1, 0])  # x  (diagonalizable: 0 matrix)
        self.assertTrue(a.derogatory)
        self.assertFalse(a.defective)


if __name__ == "__main__":
    unittest.main()
