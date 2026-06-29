"""Constructions: parity with the reference JS builders + operator algebra laws."""

import unittest

from matrix_plates import (cartan_a, cartan_d, cartan_e8, circulant, commutator,
                           companion, dsum, frustrated_ring, kron)
from matrix_plates.linalg import trace
from matrix_plates.operators import (build, build_companion, fib_word,
                                     lucas_word, seed_batch_specs)
from matrix_plates.seeds import SEED_BY_ID
from _util import JS


class TestConstructionsMatchJS(unittest.TestCase):
    def test_companions(self):
        self.assertEqual(companion(SEED_BY_ID["phi"].poly), JS["companion_phi"])
        self.assertEqual(companion(SEED_BY_ID["sq2"].poly), JS["companion_sq2"])
        self.assertEqual(companion(SEED_BY_ID["gap"].poly), JS["companion_gap"])
        self.assertEqual(companion(SEED_BY_ID["K"].poly), JS["companion_K"])
        self.assertEqual(companion(SEED_BY_ID["cons"].poly), JS["companion_cons"])
        self.assertEqual(companion(SEED_BY_ID["res"].poly), JS["companion_res"])

    def test_companion_of_phi_squared(self):
        # companion of (x²−x−1)² built from its coefficients
        self.assertEqual(companion([1, -2, -1, 2, 1]), JS["companion_of_phi2"])

    def test_dsum(self):
        cphi = companion(SEED_BY_ID["phi"].poly)
        self.assertEqual(dsum(cphi, cphi), JS["phi_dsum_phi"])

    def test_kron(self):
        a = companion(SEED_BY_ID["phi"].poly)
        b = companion(SEED_BY_ID["sq3"].poly)
        self.assertEqual(kron(a, b), JS["kron_phi_sq3"])

    def test_cartan(self):
        self.assertEqual(cartan_e8(), JS["cartanE8"])
        self.assertEqual(cartan_a(5), JS["cartanA5"])
        self.assertEqual(cartan_d(4), JS["cartanD4"])

    def test_circulant_words(self):
        self.assertEqual(fib_word(6), [1, 1, 2, 3, 5, 8])
        self.assertEqual(lucas_word(6), [2, 1, 3, 4, 7, 11])
        self.assertEqual(circulant(fib_word(6)), JS["fibcirc6"])

    def test_frustrated_ring(self):
        self.assertEqual(frustrated_ring(6), JS["ring6"])
        self.assertEqual(frustrated_ring(5), JS["ring5"])


class TestOperatorLaws(unittest.TestCase):
    def test_commutator_is_traceless(self):
        a = companion(SEED_BY_ID["phi"].poly)
        b = companion(SEED_BY_ID["sq2"].poly)
        self.assertEqual(trace(commutator(a, b)), 0)

    def test_commutator_size_guard(self):
        a = companion(SEED_BY_ID["phi"].poly)      # 2x2
        b = companion(SEED_BY_ID["K"].poly)        # 4x4
        with self.assertRaises(ValueError):
            commutator(a, b)

    def test_ring_balance_by_n_mod_4(self):
        from matrix_plates import determinant
        # Genuine cycles (n >= 4): n ≡ 0 (mod 4) balanced, n ≡ 2 (mod 4) frustrated.
        self.assertEqual(determinant(frustrated_ring(4)), 0)    # balanced
        self.assertEqual(determinant(frustrated_ring(8)), 0)    # balanced
        self.assertGreater(determinant(frustrated_ring(6)), 0)  # frustrated
        self.assertGreater(determinant(frustrated_ring(10)), 0)  # frustrated

    def test_ring_digon_degenerates_to_zero(self):
        # n = 2 is a digon: the two antiparallel ±1 edges cancel -> zero matrix.
        self.assertEqual(frustrated_ring(2), [[0, 0], [0, 0]])


class TestDispatcher(unittest.TestCase):
    def test_build_dispatch(self):
        self.assertEqual(build("companion", a="phi").M, JS["companion_phi"])
        self.assertEqual(build("dsum", a="phi", b="phi").M, JS["phi_dsum_phi"])
        self.assertEqual(build("cartan", ctype="E8").M, JS["cartanE8"])
        self.assertEqual(build("rand", n=4, seed=42).M, JS["randIntMat_4_42"])

    def test_unknown_op(self):
        with self.assertRaises(ValueError):
            build("nope")

    def test_commutator_dispatch_error(self):
        with self.assertRaises(ValueError):
            build("comm", a="phi", b="K")    # unequal sizes

    def test_seed_batch_shape(self):
        specs = seed_batch_specs()
        self.assertEqual(len(specs), 9)
        names = [s.name for s in specs]
        self.assertEqual(names[0], "C(φ)")
        self.assertEqual(names[3], "E₈")
        self.assertTrue(names[-1].startswith("rand"))


if __name__ == "__main__":
    unittest.main()
