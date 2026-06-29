#!/usr/bin/env python3
"""Worked example — the φ ⊕ φ similarity-class demonstration (Goal 2).

Run:  PYTHONPATH=../src python3 phi_plus_phi.py

Shows that ``φ ⊕ φ`` and ``companion(charpoly(φ ⊕ φ))`` have identical
characteristic polynomial / det / trace / Mahler measure, are both unimodular,
yet are **not similar** — their minimal polynomials differ in degree (2 vs 4).
The minimal polynomial is the invariant that separates the similarity classes.
"""

from matrix_plates import similarity_class_demo
from matrix_plates.text import poly_str


def fmt_matrix(M):
    w = max(len(str(x)) for row in M for x in row)
    return "\n".join("  [ " + "  ".join(str(x).rjust(w) for x in row) + " ]" for row in M)


def main() -> None:
    d = similarity_class_demo()
    p, c = d.parent, d.child

    print("φ ⊕ φ  (block-diagonal direct sum, derogatory)")
    print(fmt_matrix(p.M))
    print(f"  char-poly : {poly_str(p.coeffs)}")
    print(f"  min-poly  : {poly_str(p.minpoly)}   (degree {p.analysis.deg_min})")
    print(f"  det {p.det} · tr {p.tr} · M {round(p.mahler, 6)} · unimodular={p.unimodular}\n")

    print("companion(charpoly(φ ⊕ φ)) = companion of (x²−x−1)²  (non-derogatory)")
    print(fmt_matrix(c.M))
    print(f"  char-poly : {poly_str(c.coeffs)}")
    print(f"  min-poly  : {poly_str(c.minpoly)}   (degree {c.analysis.deg_min})")
    print(f"  det {c.det} · tr {c.tr} · M {round(c.mahler, 6)} · unimodular={c.unimodular}\n")

    print("comparison")
    print(f"  same char-poly / det / trace / Mahler : "
          f"{d.same_char_poly and d.same_det and d.same_trace and d.same_mahler}")
    print(f"  same minimal polynomial               : {d.same_min_poly}")
    print(f"  similar                               : {d.similar}")
    print("\nEqual characteristic polynomial does NOT imply similar; the minimal "
          "polynomial does.")


if __name__ == "__main__":
    main()
