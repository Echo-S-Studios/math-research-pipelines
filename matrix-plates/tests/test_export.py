"""Export to JSON / LaTeX / SymPy."""

import json
import unittest

from matrix_plates import (Gallery, build, build_plate, export_json,
                           export_latex, export_sympy, plate_to_dict)
from matrix_plates.operators import build_custom


def _plate(op="dsum", **kw):
    return build_plate(build(op, **kw), 1)


class TestJSON(unittest.TestCase):
    def test_dict_keys_and_roundtrip(self):
        p = _plate("dsum", a="phi", b="phi")
        d = plate_to_dict(p)
        for k in ("matrix", "char_poly", "min_poly", "invariant_factors",
                  "det", "house", "derogatory", "defective"):
            self.assertIn(k, d)
        self.assertEqual(d["matrix"], [list(r) for r in p.M])
        self.assertEqual(d["invariant_factors"], [[1, -1, -1], [1, -1, -1]])

    def test_export_json_parses(self):
        g = Gallery.seed_batch()
        data = json.loads(export_json(g.plates))
        self.assertEqual(len(data), len(g))

    def test_single_plate_is_object(self):
        obj = json.loads(export_json(_plate("companion", a="phi")))
        self.assertIsInstance(obj, dict)


class TestLatex(unittest.TestCase):
    def test_contains_matrix_and_polys(self):
        tex = export_latex(_plate("companion", a="phi"))
        self.assertIn("\\begin{bmatrix}", tex)
        self.assertIn("x^{2} - x - 1", tex)   # char-poly of C(φ)


class TestSympy(unittest.TestCase):
    def test_compiles_and_has_assert(self):
        code = export_sympy(_plate("companion", a="gap"))
        compile(code, "<sympy-export>", "exec")     # valid Python
        self.assertIn("Matrix([", code)
        self.assertIn("charpoly", code)

    def test_custom_name_sanitized(self):
        code = export_sympy(build_plate(build_custom([[7]], "weird name!"), 1))
        compile(code, "<x>", "exec")
        self.assertIn("Matrix([", code)


if __name__ == "__main__":
    unittest.main()
