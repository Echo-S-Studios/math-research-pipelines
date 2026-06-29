"""mulberry32 PRNG + seeded matrices: bit-exact parity with the reference JS."""

import unittest

from matrix_plates import rand_int_matrix
from matrix_plates.prng import sample
from _util import JS, close


class TestPRNG(unittest.TestCase):
    def test_first_eight_seed_42(self):
        got = sample(42, 8)
        exp = JS["mulberry32_42_first8"]
        for i, (g, e) in enumerate(zip(got, exp)):
            with self.subTest(i=i):
                self.assertTrue(close(g, e, rel=0, abs_=1e-15), f"{g} vs {e}")

    def test_first_eight_seed_7(self):
        got = sample(7, 8)
        exp = JS["mulberry32_7_first8"]
        for i, (g, e) in enumerate(zip(got, exp)):
            with self.subTest(i=i):
                self.assertTrue(close(g, e, rel=0, abs_=1e-15), f"{g} vs {e}")

    def test_range(self):
        for v in sample(12345, 50):
            self.assertGreaterEqual(v, 0.0)
            self.assertLess(v, 1.0)

    def test_rand_int_matrix_matches_js(self):
        self.assertEqual(rand_int_matrix(4, 42), JS["randIntMat_4_42"])
        self.assertEqual(rand_int_matrix(4, 7), JS["randIntMat_4_7"])
        self.assertEqual(rand_int_matrix(3, 123), JS["randIntMat_3_123"])

    def test_rand_int_matrix_in_range(self):
        for row in rand_int_matrix(6, 999):
            for x in row:
                self.assertGreaterEqual(x, -3)
                self.assertLessEqual(x, 3)

    def test_reproducible(self):
        self.assertEqual(rand_int_matrix(5, 2024), rand_int_matrix(5, 2024))


if __name__ == "__main__":
    unittest.main()
