"""Provenance and lineage tracking."""

import unittest

from matrix_plates import Gallery, build
from matrix_plates.closure import Registry, lift
from matrix_plates.operators import build_companion


class TestProvenance(unittest.TestCase):
    def test_construction_provenance(self):
        g = Gallery()
        p = g.add(build("companion", a="phi"))
        self.assertEqual(p.provenance.kind, "construct")
        self.assertEqual(p.provenance.parents, [])

    def test_lift_provenance(self):
        g = Gallery()
        parent = g.add(build("dsum", a="phi", b="phi"))
        res = lift(parent, Registry(), gallery=g)
        self.assertEqual(res.child.provenance.kind, "lift")
        self.assertEqual(res.child.provenance.parents, [parent.id])
        self.assertEqual(res.child.provenance.seed, res.seed.glyph)

    def test_lineage_chain(self):
        g = Gallery()
        reg = Registry()
        p0 = g.add(build("dsum", a="phi", b="phi"))
        r1 = lift(p0, reg, gallery=g)        # mints p̂₁
        chain = g.lineage(r1.child)
        self.assertEqual([p.id for p in chain], [p0.id, r1.child.id])
        self.assertEqual(chain[0].id, p0.id)  # oldest first

    def test_descendants(self):
        g = Gallery()
        reg = Registry()
        root = g.add(build("dsum", a="phi", b="phi"))
        child = lift(root, reg, gallery=g).child
        self.assertIn(child.id, [d.id for d in g.descendants(root.id)])
        self.assertEqual(g.descendants(child.id), [])  # leaf

    def test_lineage_of_construction_is_singleton(self):
        g = Gallery()
        p = g.add(build_companion("gap"))
        self.assertEqual(g.lineage(p), [p])


if __name__ == "__main__":
    unittest.main()
