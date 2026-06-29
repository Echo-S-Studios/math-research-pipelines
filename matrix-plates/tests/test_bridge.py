"""Optional NumPy/SymPy bridge — checks skip gracefully when a lib is absent."""

import unittest

from matrix_plates import analyse, bridge
from _util import JS, close


class TestBridge(unittest.TestCase):
    def test_capability_flags_are_bool(self):
        self.assertIsInstance(bridge.have_numpy(), bool)
        self.assertIsInstance(bridge.have_sympy(), bool)

    @unittest.skipUnless(bridge.have_sympy(), "sympy not installed")
    def test_sympy_exact_agreement(self):
        for name in ["companion_phi", "phi_dsum_phi", "ring6", "cartanE8"]:
            A = JS[name]
            a = analyse(A)
            self.assertEqual(bridge.sympy_char_poly(A), a.coeffs)
            self.assertEqual(bridge.sympy_min_poly(A), a.minpoly)
            self.assertTrue(close(bridge.sympy_mahler(A), a.mahler, rel=1e-6))

    @unittest.skipUnless(bridge.have_numpy(), "numpy not installed")
    def test_numpy_mahler_close(self):
        A = JS["companion_gap"]
        self.assertTrue(close(bridge.numpy_mahler(A), analyse(A).mahler, rel=1e-3))

    def test_verify_report_structure(self):
        rep = bridge.verify(JS["companion_phi"])
        self.assertIn("char_poly", rep)
        if bridge.have_sympy():
            self.assertTrue(rep["sympy"]["char_poly_match"])
            self.assertTrue(rep["sympy"]["min_poly_match"])

    def test_missing_package_message(self):
        # _require raises a helpful ImportError naming the package
        with self.assertRaises(ImportError):
            bridge._require("definitely_not_a_real_package_xyz")


if __name__ == "__main__":
    unittest.main()
