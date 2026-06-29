"""Memoization layer (cache)."""

import unittest

from matrix_plates import cache
from matrix_plates.linalg import char_poly as raw_char_poly
from matrix_plates.linalg import min_poly as raw_min_poly
from _util import JS


class TestCache(unittest.TestCase):
    def setUp(self):
        cache.clear_caches()

    def test_matches_raw(self):
        for name in ["companion_phi", "phi_dsum_phi", "cartanE8"]:
            A = JS[name]
            self.assertEqual(cache.char_poly(A), raw_char_poly(A))
            self.assertEqual(cache.min_poly(A), list(raw_min_poly(A)))

    def test_hits_accumulate(self):
        A = JS["fibcirc6"]
        cache.char_poly(A)            # miss
        cache.char_poly(A)            # hit
        cache.char_poly(A)            # hit
        info = cache._char_poly_key.cache_info()
        self.assertGreaterEqual(info.hits, 2)

    def test_mutation_safety(self):
        A = JS["companion_phi"]
        first = cache.char_poly(A)[0]
        first.append(999)             # mutate the returned list
        second = cache.char_poly(A)[0]
        self.assertNotIn(999, second)  # cache returns a fresh copy each call

    def test_clear(self):
        cache.char_poly(JS["companion_sq2"])
        cache.clear_caches()
        self.assertEqual(cache._char_poly_key.cache_info().currsize, 0)

    def test_invariant_factors_cached(self):
        from matrix_plates.canonical import invariant_factors
        A = JS["phi_dsum_phi"]
        self.assertEqual(cache.invariant_factors(A), invariant_factors(A))


if __name__ == "__main__":
    unittest.main()
