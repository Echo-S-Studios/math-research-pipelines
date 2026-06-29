"""Goal 2 — companion∘charpoly closure, similarity classes, and composition."""

import unittest

from matrix_plates import (Gallery, build, build_histogram,
                           is_similar_to_companion_lift, lift,
                           similarity_class_demo)
from matrix_plates.closure import Registry
from matrix_plates.operators import build_companion, build_kron
from matrix_plates.plates import build_plate


def _plate(op, **kw):
    return build_plate(build(op, **kw), 1)


class TestFixedPoint(unittest.TestCase):
    def test_companion_phi_is_fixed_point(self):
        p = _plate("companion", a="phi")
        r = lift(p, Registry())
        self.assertTrue(r.idempotent)
        self.assertEqual(r.child.M, [[0, 1], [1, 1]])
        self.assertTrue(r.spectrum_preserved)
        self.assertTrue(r.similar)            # companion is non-derogatory

    def test_degree_one_fixed_point(self):
        p = build_plate(type("B", (), {"M": [[5]], "name": "[[5]]",
                                       "prov": "ad hoc", "note": ""})(), 1)
        r = lift(p, Registry())
        self.assertEqual(r.child.M, [[5]])
        self.assertTrue(r.idempotent)


class TestDerogatorySimilarity(unittest.TestCase):
    def test_phi_plus_phi_not_similar(self):
        d = similarity_class_demo()
        # same spectrum / det / tr / Mahler ...
        self.assertTrue(d.same_char_poly)
        self.assertTrue(d.same_det)
        self.assertTrue(d.same_trace)
        self.assertTrue(d.same_mahler)
        # ... but different minimal polynomial => not similar
        self.assertFalse(d.same_min_poly)
        self.assertFalse(d.similar)
        self.assertEqual(d.parent.analysis.deg_min, 2)
        self.assertEqual(d.child.analysis.deg_min, 4)

    def test_lift_reports_not_similar_for_derogatory(self):
        parent = _plate("dsum", a="phi", b="phi")
        r = lift(parent, Registry())
        self.assertFalse(r.similar)
        self.assertFalse(r.idempotent)
        self.assertIn("NOT similar", r.note)

    def test_is_similar_predicate(self):
        self.assertTrue(is_similar_to_companion_lift(_plate("companion", a="gap")))
        self.assertFalse(is_similar_to_companion_lift(_plate("dsum", a="phi", b="phi")))


class TestRegistry(unittest.TestCase):
    def test_dedupe_on_second_lift(self):
        reg = Registry()
        g = Gallery()
        # φ ⊕ φ has a NOVEL char-poly (x²−x−1)², not a built-in seed signature,
        # so the first lift mints a new p̂ seed; the second lift hits the fixed
        # point and reuses it. (Lifting a built-in companion like C(gap) would
        # reuse its own seed immediately — that is the degenerate case.)
        base = g.add(build("dsum", a="phi", b="phi"))
        first = lift(base, reg, gallery=g)
        self.assertFalse(first.reused)            # minted a new seed
        second = lift(first.child, reg, gallery=g)
        self.assertTrue(second.reused)            # fixed point reuses it
        self.assertEqual(first.seed.id, second.seed.id)

    def test_generated_seed_feeds_binary_operator(self):
        reg = Registry()
        parent = _plate("dsum", a="phi", b="phi")
        r = lift(parent, reg)
        # the generated p̂ seed must be usable by ⊗ / ⊕ / [A,B]
        kbuilt = build_kron(r.seed.id, "sq2", reg.by_id)
        self.assertEqual(len(kbuilt.M), 4 * 2)    # deg-4 seed ⊗ deg-2 seed = 8x8

    def test_lift_rejects_non_monic(self):
        # A fabricated non-monic "char-poly" must be refused.
        bad = build_plate(type("B", (), {"M": [[0, 1], [1, 1]], "name": "x",
                                         "prov": "p", "note": ""})(), 1)
        object.__setattr__(bad.analysis, "coeffs", [2, -1, -1])  # leading 2 => non-monic
        with self.assertRaises(ValueError):
            lift(bad, Registry())


class TestComposition(unittest.TestCase):
    def test_lifted_companion_shares_parent_bin(self):
        # Φ preserves M, so parent and child land in the same Mahler-spectrum bin.
        g = Gallery()
        parent = g.add(build("dsum", a="phi", b="phi"))
        r = lift(parent, Registry(), gallery=g)
        hist = build_histogram(g.plates, max_log_m=g.max_log_m)
        self.assertEqual(hist.bin_of(parent), hist.bin_of(r.child))
        self.assertAlmostEqual(parent.mahler, r.child.mahler)


if __name__ == "__main__":
    unittest.main()
