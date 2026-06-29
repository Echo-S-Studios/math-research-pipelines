"""Plates, provenance, and galleries.

A :class:`Plate` is a built matrix together with its analysis, presentation
metadata, and a :class:`Provenance` record. A :class:`Gallery` holds plates in
insertion order, indexes them by id, tracks the running ``log M`` ceiling used by
the Mahler-spectrum layout (Goal 1), and can walk lineage / find descendants —
so you can trace how a matrix was generated through successive companion lifts.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .invariants import Analysis, analyse
from .operators import Built, seed_batch_specs


@dataclass
class Provenance:
    """How a plate came to exist.

    ``kind`` is ``'construct'`` (a catalogue construction), ``'lift'`` (a
    ``companion ∘ charpoly`` lift of ``parents[0]``), or ``'custom'`` (a
    user-supplied matrix). ``parents`` are plate ids (lifts have exactly one;
    constructions have none — their inputs are seeds, not plates).
    """

    kind: str
    label: str
    params: Dict[str, object] = field(default_factory=dict)
    parents: List[int] = field(default_factory=list)
    seed: str = ""

    @classmethod
    def construct(cls, built: "Built") -> "Provenance":
        return cls(kind="construct", label=built.prov)

    @classmethod
    def custom(cls, label: str = "user matrix") -> "Provenance":
        return cls(kind="custom", label=label)


@dataclass
class Plate:
    """A built matrix, analysed, with a stable id, metadata, and provenance."""

    id: int
    name: str
    prov: str
    note: str
    analysis: Analysis
    provenance: Optional[Provenance] = None

    # --- convenience pass-throughs to the analysis ---
    @property
    def M(self):
        return self.analysis.M

    @property
    def n(self) -> int:
        return self.analysis.n

    @property
    def mahler(self) -> float:
        return self.analysis.mahler

    @property
    def log_mahler(self) -> float:
        return math.log(self.analysis.mahler)

    @property
    def det(self) -> int:
        return self.analysis.det

    @property
    def tr(self) -> int:
        return self.analysis.tr

    @property
    def rho(self) -> float:
        return self.analysis.rho

    @property
    def house(self) -> float:
        return self.analysis.house

    @property
    def coeffs(self) -> List[int]:
        return self.analysis.coeffs

    @property
    def minpoly(self) -> List[int]:
        return self.analysis.minpoly

    @property
    def invariant_factors(self) -> List[List[int]]:
        return self.analysis.invariant_factors

    @property
    def similarity_key(self) -> Tuple[Tuple[int, ...], ...]:
        return self.analysis.similarity_key

    @property
    def derogatory(self) -> bool:
        return self.analysis.derogatory

    @property
    def defective(self) -> bool:
        return self.analysis.defective

    @property
    def unimodular(self) -> bool:
        return self.analysis.unimodular

    @property
    def family(self) -> str:
        """``'random'`` for the seeded-control family, else ``'structured'``."""
        from .histogram import family_of
        return family_of(self.prov)


def build_plate(built: Built, uid: int,
                provenance: Optional[Provenance] = None) -> Plate:
    """Analyse a :class:`~matrix_plates.operators.Built` into a :class:`Plate`."""
    return Plate(id=uid, name=built.name, prov=built.prov, note=built.note,
                 analysis=analyse(built.M),
                 provenance=provenance or Provenance.construct(built))


class Gallery:
    """An ordered collection of plates with id-indexing and lineage tracking."""

    def __init__(self) -> None:
        self.plates: List[Plate] = []
        self.by_id: Dict[int, Plate] = {}
        self._uid = 0
        self.max_log_m = math.log(1.6)

    def __iter__(self):
        return iter(self.plates)

    def __len__(self) -> int:
        return len(self.plates)

    def _register(self, plate: Plate) -> Plate:
        self.plates.append(plate)
        self.by_id[plate.id] = plate
        if plate.log_mahler > self.max_log_m:
            self.max_log_m = plate.log_mahler
        return plate

    def add(self, built: Built, provenance: Optional[Provenance] = None) -> Plate:
        """Analyse and append a built matrix; update the ``log M`` ceiling."""
        self._uid += 1
        return self._register(build_plate(built, self._uid, provenance))

    def add_plate(self, plate: Plate) -> Plate:
        """Append an already-built plate (used by the closure for lifted plates)."""
        return self._register(plate)

    def next_uid(self) -> int:
        self._uid += 1
        return self._uid

    def clear(self) -> None:
        self.plates.clear()
        self.by_id.clear()
        self._uid = 0
        self.max_log_m = math.log(1.6)

    # --- lineage / provenance queries ---
    def lineage(self, plate: Plate) -> List[Plate]:
        """The ancestry chain (oldest → *plate*) following lift parents."""
        chain = [plate]
        cur = plate
        seen = {plate.id}
        while cur.provenance and cur.provenance.parents:
            par = self.by_id.get(cur.provenance.parents[0])
            if par is None or par.id in seen:
                break
            chain.append(par)
            seen.add(par.id)
            cur = par
        return list(reversed(chain))

    def descendants(self, plate_id: int) -> List[Plate]:
        """All plates whose lineage passes through *plate_id*."""
        return [p for p in self.plates
                if any(a.id == plate_id for a in self.lineage(p)) and p.id != plate_id]

    @classmethod
    def seed_batch(cls) -> "Gallery":
        """A gallery preloaded with the tool's *Seed batch* (nine plates)."""
        g = cls()
        for spec in seed_batch_specs():
            g.add(spec)
        return g
