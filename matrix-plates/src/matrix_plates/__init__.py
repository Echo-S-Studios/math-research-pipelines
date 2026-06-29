"""matrix_plates — exact integer-matrix constructions, the Mahler-measure
spectrum layout (Goal 1), and the ``companion ∘ charpoly`` closure (Goal 2).

This is the computational backend for ``matrix_plates.html``: the same operator
algebra over the same algebraic-integer seed registry, computed in exact integer
and rational arithmetic, with the minimal polynomial added so the closure can
make precise statements about *similarity classes*.

Quick start
-----------
>>> from matrix_plates import build, analyse
>>> a = analyse(build("dsum", a="phi", b="phi").M)   # φ ⊕ φ
>>> a.deg_char, a.deg_min, a.derogatory
(4, 2, True)

>>> from matrix_plates import Gallery, build_histogram, render_ascii
>>> print(render_ascii(build_histogram(Gallery.seed_batch().plates)))  # doctest: +SKIP

>>> from matrix_plates import similarity_class_demo
>>> d = similarity_class_demo()
>>> d.same_char_poly, d.same_min_poly, d.similar
(True, False, False)
"""

from __future__ import annotations

# --- exact linear algebra ---
from .linalg import (Matrix, char_poly, determinant, matmul, matpow, min_poly,
                     rank)
from .roots import (classify_unit_circle, dk_roots, mahler_from_roots,
                    spectral_radius)
from .prng import mulberry32, rand_int_matrix

# --- seeds & constructions ---
from .seeds import SEEDS, Seed, base_registry
from .operators import (OPS, Built, build, build_custom, companion, kron, dsum,
                        commutator, cartan_a, cartan_d, cartan_e8, circulant,
                        frustrated_ring, seed_batch_specs)

# --- exact polynomials & rational canonical form ---
from .polynomial import Poly
from .canonical import (invariant_factors, is_similar, rational_canonical_form,
                        similarity_key)
from . import cache
from .cache import cache_info, clear_caches

# --- analysis & plates ---
from .invariants import Analysis, analyse
from .plates import Gallery, Plate, Provenance, build_plate

# --- Goal 1: Mahler spectrum ---
from .histogram import (LEHMER, Bin, MahlerHistogram, build_histogram,
                        comparison_table, family_of, render_ascii, render_svg,
                        sorted_reflow, spectrum_bins)

# --- Goal 2: companion∘charpoly closure (+ queries) ---
from .closure import (LiftResult, Registry, SimilarityDemo, divides,
                      is_similar_to_companion_lift, lift, similarity_class_demo,
                      similarity_classes, spectrum_contains)

# --- rendering & export ---
from .render_html import gallery_html, spectrum_html
from .export import export_json, export_latex, export_sympy, plate_to_dict
from . import bridge

__version__ = "1.1.2"

__all__ = [
    # linalg
    "Matrix", "char_poly", "determinant", "matmul", "matpow", "min_poly", "rank",
    "dk_roots", "mahler_from_roots", "spectral_radius", "classify_unit_circle",
    "mulberry32", "rand_int_matrix",
    # seeds / operators
    "SEEDS", "Seed", "base_registry", "OPS", "Built", "build", "build_custom",
    "companion", "kron", "dsum", "commutator",
    "cartan_a", "cartan_d", "cartan_e8", "circulant", "frustrated_ring",
    "seed_batch_specs",
    # polynomials / canonical form
    "Poly", "invariant_factors", "is_similar", "rational_canonical_form",
    "similarity_key", "cache", "cache_info", "clear_caches",
    # analysis
    "Analysis", "analyse", "Gallery", "Plate", "Provenance", "build_plate",
    # goal 1
    "LEHMER", "Bin", "MahlerHistogram", "build_histogram", "comparison_table",
    "family_of", "render_ascii", "render_svg", "sorted_reflow", "spectrum_bins",
    # goal 2
    "LiftResult", "Registry", "SimilarityDemo", "is_similar_to_companion_lift",
    "lift", "similarity_class_demo", "similarity_classes", "spectrum_contains",
    "divides",
    # rendering & export
    "gallery_html", "spectrum_html", "export_json", "export_latex",
    "export_sympy", "plate_to_dict", "bridge",
    # rendering
    "gallery_html", "spectrum_html",
    "__version__",
]
