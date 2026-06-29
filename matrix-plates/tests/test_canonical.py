"""Rational canonical form: invariant factors, similarity, RCF — vs sympy oracle."""

import json
import pathlib
import unittest

from matrix_plates import char_poly, min_poly
from matrix_plates.canonical import (invariant_factors, is_similar,
                                     rational_canonical_form, similarity_key)
from matrix_plates.polynomial import Poly
from _util import JS

_INV = json.loads((pathlib.Path(__file__).resolve().parent
                   / "fixtures" / "invariant_factors_oracle.json").read_text())


class TestInvariantFactors(unittest.TestCase):
    def test_matches_oracle(self):
        for name, rec in _INV.items():
            A = rec.get("matrix") or JS[name]
            with self.subTest(matrix=name):
                self.assertEqual(invariant_factors(A), rec["invariant_factors"])

    def test_product_is_charpoly(self):
        for name, rec in _INV.items():
            A = rec.get("matrix") or JS[name]
            with self.subTest(matrix=name):
                prod = Poly.one()
                for f in invariant_factors(A):
                    prod = prod * Poly.from_high_low(f)
                self.assertEqual(prod.to_high_low(), char_poly(A)[0])

    def test_last_factor_is_minpoly(self):
        for name, rec in _INV.items():
            A = rec.get("matrix") or JS[name]
            facs = invariant_factors(A)
            with self.subTest(matrix=name):
                self.assertEqual(facs[-1], min_poly(A))

    def test_divisibility_chain(self):
        # each invariant factor divides the next
        facs = invariant_factors(JS["ring5"])   # two distinct factors
        for i in range(len(facs) - 1):
            q, r = Poly.from_high_low(facs[i + 1]).divmod(Poly.from_high_low(facs[i]))
            self.assertTrue(r.is_zero, f"f{i} must divide f{i+1}")


class TestSimilarity(unittest.TestCase):
    def test_phi_plus_phi_not_similar_to_companion(self):
        self.assertFalse(is_similar(JS["phi_dsum_phi"], JS["companion_of_phi2"]))

    def test_reflexive(self):
        self.assertTrue(is_similar(JS["cartanE8"], JS["cartanE8"]))

    def test_different_sizes_not_similar(self):
        self.assertFalse(is_similar(JS["companion_phi"], JS["cartanE8"]))

    def test_similarity_key_distinguishes(self):
        self.assertNotEqual(similarity_key(JS["phi_dsum_phi"]),
                            similarity_key(JS["companion_of_phi2"]))

    def test_permutation_similar(self):
        # A and P A P^{-1} are similar; swap basis vectors 0 and 1 of C(gap)
        A = JS["companion_gap"]
        B = [[A[1][1], A[1][0]], [A[0][1], A[0][0]]]  # conjugation by the swap
        self.assertTrue(is_similar(A, B))


class TestRationalCanonicalForm(unittest.TestCase):
    def test_companion_is_its_own_rcf(self):
        self.assertEqual(rational_canonical_form(JS["companion_phi"]), JS["companion_phi"])

    def test_rcf_idempotent(self):
        rcf = rational_canonical_form(JS["phi_dsum_phi"])
        self.assertEqual(rational_canonical_form(rcf), rcf)

    def test_rcf_preserves_charpoly(self):
        rcf = rational_canonical_form(JS["ring5"])
        self.assertEqual(char_poly(rcf)[0], char_poly(JS["ring5"])[0])
        self.assertTrue(is_similar(rcf, JS["ring5"]))


if __name__ == "__main__":
    unittest.main()
