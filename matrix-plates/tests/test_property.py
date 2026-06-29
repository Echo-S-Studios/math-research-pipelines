"""Property-based tests over random integer matrices.

Skipped wholesale if ``hypothesis`` is not installed (it is an optional dev
dependency), so the core suite stays stdlib-only.
"""

import unittest

try:
    from hypothesis import HealthCheck, given, settings
    from hypothesis import strategies as st
    HAVE_HYPOTHESIS = True
except ImportError:  # pragma: no cover
    HAVE_HYPOTHESIS = False


if HAVE_HYPOTHESIS:
    from matrix_plates import analyse, char_poly, min_poly
    from matrix_plates.canonical import (invariant_factors, is_similar,
                                         rational_canonical_form)
    from matrix_plates.operators import companion
    from matrix_plates.polynomial import Poly
    from matrix_plates.roots import spectral_radius

    def _square(n_min=1, n_max=4, lo=-3, hi=3):
        return st.integers(min_value=n_min, max_value=n_max).flatmap(
            lambda n: st.lists(
                st.lists(st.integers(lo, hi), min_size=n, max_size=n),
                min_size=n, max_size=n))

    _SETTINGS = settings(max_examples=120, deadline=None,
                         suppress_health_check=[HealthCheck.too_slow])

    class TestProperties(unittest.TestCase):

        @_SETTINGS
        @given(_square())
        def test_charpoly_is_monic_integer_degree_n(self, A):
            coeffs, _ = char_poly(A)
            self.assertEqual(coeffs[0], 1)
            self.assertEqual(len(coeffs) - 1, len(A))
            self.assertTrue(all(isinstance(c, int) for c in coeffs))

        @_SETTINGS
        @given(_square())
        def test_minpoly_divides_charpoly(self, A):
            cp = Poly.from_high_low(char_poly(A)[0])
            mp = Poly.from_high_low(min_poly(A))
            self.assertTrue((cp % mp).is_zero)

        @_SETTINGS
        @given(_square())
        def test_phi_preserves_charpoly(self, A):
            cp = char_poly(A)[0]
            self.assertEqual(char_poly(companion(cp))[0], cp)

        @_SETTINGS
        @given(_square())
        def test_companion_is_nonderogatory(self, A):
            cp = char_poly(A)[0]
            self.assertEqual(min_poly(companion(cp)), cp)

        @_SETTINGS
        @given(_square())
        def test_invariant_factors_product_and_chain(self, A):
            facs = invariant_factors(A)
            prod = Poly.one()
            for f in facs:
                prod = prod * Poly.from_high_low(f)
            self.assertEqual(prod.to_high_low(), char_poly(A)[0])
            for i in range(len(facs) - 1):
                self.assertTrue((Poly.from_high_low(facs[i + 1])
                                 % Poly.from_high_low(facs[i])).is_zero)
            if facs:
                self.assertEqual(facs[-1], min_poly(A))

        @_SETTINGS
        @given(_square())
        def test_similar_to_own_rcf(self, A):
            self.assertTrue(is_similar(A, rational_canonical_form(A)))

        @_SETTINGS
        @given(_square())
        def test_house_matches_spectral_radius(self, A):
            a = analyse(A)
            self.assertLessEqual(abs(a.house - spectral_radius(a.roots)),
                                 1e-6 * max(1.0, a.house))

else:  # pragma: no cover

    class TestProperties(unittest.TestCase):
        @unittest.skip("hypothesis not installed (optional dev dependency)")
        def test_property_based(self):
            pass


if __name__ == "__main__":
    unittest.main()
