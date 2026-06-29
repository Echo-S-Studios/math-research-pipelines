"""The build-spec 'Verify' checklists, encoded as assertions.

Mirrors the spec's Goal-1 and Goal-2 verification steps and their named numeric
anchors (C(φ) → 1.618, C(√2) → 2, C(φ⁻⁴) → 6.854, E₈ unimodular, balanced vs
frustrated rings).
"""

import unittest

from matrix_plates import (Gallery, analyse, build, determinant,
                           frustrated_ring)
from matrix_plates.cli import _checks
from _util import close


class TestSpecChecklist(unittest.TestCase):
    def test_all_cli_checks_pass(self):
        results = _checks()
        failures = [name for name, ok, _ in results if not ok]
        self.assertEqual(failures, [], f"failing checks: {failures}")
        self.assertGreaterEqual(len(results), 8)


class TestNumericAnchors(unittest.TestCase):
    def test_named_mahler_values(self):
        m = {p.name: p.mahler for p in Gallery.seed_batch()}
        self.assertTrue(close(m["C(φ)"], 1.618033988749895, rel=1e-6))
        self.assertTrue(close(m["C(φ⁻⁴)"], 6.854101966249685, rel=1e-6))
        # C(√2) is not in the batch; build it directly.
        self.assertTrue(close(analyse(build("companion", a="sq2").M).mahler, 2.0, rel=1e-9))

    def test_e8_unimodular_det_one(self):
        a = analyse(build("cartan", ctype="E8").M)
        self.assertEqual(a.det, 1)
        self.assertTrue(a.unimodular)

    def test_ring_balance_cases(self):
        # n ≡ 0 (mod 4): balanced (det 0); n ≡ 2 (mod 4): frustrated (det > 0).
        self.assertEqual(determinant(frustrated_ring(4)), 0)
        self.assertEqual(determinant(frustrated_ring(8)), 0)
        self.assertGreater(determinant(frustrated_ring(6)), 0)

    def test_cartan_determinants(self):
        from matrix_plates import cartan_a, cartan_d, cartan_e8
        self.assertEqual(determinant(cartan_a(5)), 6)    # n+1
        self.assertEqual(determinant(cartan_d(4)), 4)
        self.assertEqual(determinant(cartan_e8()), 1)


if __name__ == "__main__":
    unittest.main()
