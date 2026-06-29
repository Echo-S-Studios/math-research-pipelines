"""Goal 2 — ``charpoly ↦ companion`` as a closure, with a queryable registry.

``Φ = companion ∘ charpoly`` sends a matrix to the companion (rational-canonical
representative) of its characteristic polynomial. It powers a **self-extending**
seed registry and demonstrates, in one move, that equal characteristic polynomial
⇒ equal ``det``/``tr``/``ρ``/``M`` always, but ⇏ *similar* (the derogatory case;
the minimal polynomial / invariant factors separate the classes).

This module also makes the registry **queryable**:

* :meth:`Registry.query_extends` — "what plates extend this seed?" (a plate
  *extends* a seed when the seed's minimal polynomial divides the plate's
  characteristic polynomial, i.e. the seed's conjugate orbit is a sub-spectrum);
* :func:`similarity_classes` — group plates by rational canonical form;
* lineage / descendants live on :class:`~matrix_plates.plates.Gallery`.

Properties of ``Φ``: idempotent (a companion is its own lift — a retraction onto
companion matrices), dimension-preserving, and integral (companion polynomials
are monic). See the build spec, §3.

Reference: Horn & Johnson, *Matrix Analysis* 2e, §3.2–§3.3; Dummit & Foote,
§12.2 (rational canonical form).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .canonical import is_similar, similarity_key
from .linalg import poly_eq
from .operators import build_companion
from .plates import Gallery, Plate, Provenance, build_plate
from .polynomial import Poly
from .seeds import Seed, base_registry
from .text import sub


# --- similarity / spectrum-containment helpers ---------------------------------
def divides(a: List[int], b: List[int]) -> bool:
    """True if polynomial *a* divides *b* (both **high → low**), exactly over ℚ."""
    pa, pb = Poly.from_high_low(a), Poly.from_high_low(b)
    if pa.is_zero:
        return pb.is_zero
    return (pb % pa).is_zero


def spectrum_contains(plate: Plate, seed: Seed) -> bool:
    """True if *seed*'s conjugate orbit is a sub-spectrum of *plate*.

    Defined as: the seed's (monic, irreducible-or-not) polynomial divides the
    plate's characteristic polynomial. E.g. ``φ ⊕ φ`` extends ``φ``.
    """
    return divides(seed.poly, plate.coeffs)


def similarity_classes(plates: List[Plate]) -> Dict[Tuple[Tuple[int, ...], ...], List[Plate]]:
    """Group *plates* by similarity class (equal rational canonical form)."""
    classes: Dict[Tuple[Tuple[int, ...], ...], List[Plate]] = {}
    for p in plates:
        classes.setdefault(p.similarity_key, []).append(p)
    return classes


# --- the lift ------------------------------------------------------------------
@dataclass
class LiftResult:
    """The outcome of lifting one plate through ``Φ = companion ∘ charpoly``."""

    parent: Plate
    child: Plate
    seed: Seed
    reused: bool
    idempotent: bool
    spectrum_preserved: bool
    similar: bool
    note: str = ""


class Registry:
    """A self-extending seed registry: built-ins plus generated ``p̂ₖ`` seeds.

    Deduplicates by characteristic-polynomial signature, so lifting the same
    spectrum twice reuses one seed (the fixed point) rather than minting a copy.
    """

    def __init__(self) -> None:
        self.by_id: Dict[str, Seed] = base_registry()
        self.sig_to_id: Dict[str, str] = {s.signature(): sid
                                          for sid, s in self.by_id.items()}
        self.gen_count = 0

    def seed_for_poly(self, coeffs: List[int], parent_name: str = "") -> Tuple[Seed, bool]:
        """Return ``(seed, reused)`` for a monic integer char-poly."""
        key = ",".join(str(c) for c in coeffs)
        sid = self.sig_to_id.get(key)
        if sid is not None:
            return self.by_id[sid], True
        self.gen_count += 1
        sid = f"gen{self.gen_count}"
        seed = Seed(
            id=sid,
            glyph="p\u0302" + sub(self.gen_count),
            field="\u211A[x]/(p)",
            poly=list(coeffs),
            note=("char-poly lift of " + parent_name +
                  " — spectrum-preserving (same det, tr, M).") if parent_name
                 else "char-poly lift — spectrum-preserving.",
        )
        self.by_id[sid] = seed
        self.sig_to_id[key] = sid
        return seed, False

    def generated(self) -> List[Seed]:
        """Seeds minted by lifts, in creation order."""
        return [self.by_id[f"gen{i}"] for i in range(1, self.gen_count + 1)
                if f"gen{i}" in self.by_id]

    # --- queries ---
    def describe(self, seed_id: str) -> Dict[str, object]:
        """A summary dict for a seed id (built-in or generated)."""
        s = self.by_id[seed_id]
        return {"id": s.id, "glyph": s.glyph, "field": s.field, "degree": s.degree,
                "poly": list(s.poly), "generated": seed_id.startswith("gen"),
                "note": s.note}

    def query_extends(self, seed_id: str, plates: List[Plate]) -> List[Plate]:
        """Plates whose spectrum contains *seed_id* (the seed divides their char-poly)."""
        s = self.by_id[seed_id]
        return [p for p in plates if spectrum_contains(p, s)]


def _validate_monic_integer(coeffs: List[int]) -> None:
    if (not coeffs) or len(coeffs) < 2 or coeffs[0] != 1 \
            or any(not isinstance(c, int) for c in coeffs):
        raise ValueError(
            "char-poly is not a monic integer polynomial — cannot lift to an "
            "algebraic-integer seed. (Got leading coefficient "
            f"{coeffs[0] if coeffs else 'None'}.)")


def lift(plate: Plate,
         registry: Registry,
         gallery: Optional[Gallery] = None) -> LiftResult:
    """Lift *plate* through ``Φ``: build the companion of its char-poly.

    Validates the char-poly is monic integer, dedupes against the registry,
    builds ``companion(charpoly)``, analyses it, records provenance
    (``parents=[plate.id]``), and classifies the relationship (idempotent?
    similar?). The similarity verdict is exact: similar ⇔ *plate* is
    non-derogatory ⇔ ``companion(charpoly(plate))`` has the same invariant factors.
    """
    coeffs = plate.coeffs
    _validate_monic_integer(coeffs)
    seed, reused = registry.seed_for_poly(coeffs, plate.name)
    built = build_companion(seed.id, registry.by_id)
    prov = Provenance(kind="lift", label="companion ∘ charpoly",
                      params={"seed": seed.id}, parents=[plate.id], seed=seed.glyph)
    if gallery is not None:
        child = gallery.add(built, provenance=prov)
    else:
        child = build_plate(built, plate.id, provenance=prov)
    idempotent = (child.M == plate.M)
    spectrum_preserved = poly_eq(child.coeffs, plate.coeffs)
    similar = not plate.derogatory
    if idempotent:
        note = "fixed point: input was already a companion (Φ∘Φ = Φ)."
    elif not similar:
        note = ("derogatory input: same spectrum, different minimal polynomial "
                f"(deg {plate.analysis.deg_min} → {child.analysis.deg_min}) — NOT similar.")
    else:
        note = "non-derogatory input: companion is similar to the source (same invariant factors)."
    return LiftResult(parent=plate, child=child, seed=seed, reused=reused,
                      idempotent=idempotent, spectrum_preserved=spectrum_preserved,
                      similar=similar, note=note)


def is_similar_to_companion_lift(plate: Plate) -> bool:
    """True iff ``companion(charpoly(plate))`` is *similar* to *plate* (⇔ non-derogatory)."""
    return not plate.derogatory


@dataclass
class SimilarityDemo:
    """The worked ``φ ⊕ φ`` similarity-class demonstration."""

    parent: Plate
    child: Plate
    same_char_poly: bool
    same_det: bool
    same_trace: bool
    same_mahler: bool
    same_min_poly: bool
    same_invariant_factors: bool
    similar: bool


def similarity_class_demo(registry: Optional[Registry] = None) -> SimilarityDemo:
    """Build ``φ ⊕ φ`` and its companion lift; return the full comparison.

    Parent and child share char-poly / det / tr / ρ / M and both are unimodular,
    yet differ in minimal polynomial (deg 2 vs 4) and in invariant factors
    (``[x²−x−1, x²−x−1]`` vs ``[(x²−x−1)²]``) — so they are **not similar**.
    """
    registry = registry or Registry()
    g = Gallery()
    from .operators import build_dsum
    parent = g.add(build_dsum("phi", "phi"))
    res = lift(parent, registry, gallery=g)
    child = res.child
    return SimilarityDemo(
        parent=parent, child=child,
        same_char_poly=poly_eq(parent.coeffs, child.coeffs),
        same_det=(parent.det == child.det),
        same_trace=(parent.tr == child.tr),
        same_mahler=(abs(parent.mahler - child.mahler) < 1e-9),
        same_min_poly=poly_eq(parent.minpoly, child.minpoly),
        same_invariant_factors=is_similar(parent.M, child.M),
        similar=res.similar,
    )
