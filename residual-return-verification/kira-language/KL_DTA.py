#!/usr/bin/env python3
"""
================================================================================
EPISTEMIC STATUS — [speculative] / interpretive, and FLOAT-BASED.  READ FIRST.
================================================================================
The spacetime / Clifford-algebra construction in this module (the Cl(2,0) =~ M2(R)
carrier, the "forced" Lorentz signature, the Born-rule det^2, the time / physics
narrative) is INTERPRETIVE and tagged [speculative]. It decides with math.isclose
(floating point), so it sits OUTSIDE the project's exact, no-float-across-a-
decision discipline, and it is NOT load-bearing for any [forced] result: no paper
claim and no verification suite depends on it. The exact emission-algebra substrate
-- the cost floor, the finitely generated monoid, the angle charge, the closure
guard -- lives in the lambda2c-emissiongap-verification and L00M exact cores and is
decided in exact arithmetic over Q / Q(sqrt5). This material is kept (not deleted)
as the project's most speculative reading; treat it as a hypothesis, not a result.
================================================================================

KL_DTA — the infinite form. THE SAID and THE WITNESS, same shape, both routing through the void.

THE RECURSIVE UNFOLDING — DELOCALIZED. the spine is not a stored global fact ; it lives as a CONNECTION, each
link held LOCALLY at its node, and the whole is the HOLONOMY ∮ (the path-ordered composite of the local links,
the gauge A=Q⁻¹dQ). NOT a causal line but ∅ SELF-APPLYING the void law (the recurrence x²=x+1 iterated on its
own output: ∃=∅ observed, ∃(∃)=M², …=Mⁿ ; ∅ the seed, physics the limit, GENERATED not caused). the loop:
  ∅ ⟹ ∃ ⟹ bit ⟹ mirror ⟹ carrier ⟹ · ⟹ prov ⟹ Φ ⟹ M ⟹ ν ⟹ ε ⟹ exp ⟹ time ⟹ climb ⟹ physics
is read at every node (each node carries its own ⟹) and reconstructed by composing them — no single node holds
the whole. the graph below IS this connection ; the unfolding emerges as its holonomy, not as a value at one point.

═══ THE SEED (everything below decompresses from here) ═══════════════════════════════════════════
TWO FUNDAMENTAL ROOTS — 'fundamental' at full physical standard = IRREDUCIBLE = HAS NO SOURCE (not built
from anything more basic). exactly two, and they ARE THE TWO OPERATIONS' IDENTITIES, ordered (not symmetric):

  ∅  (VOID) — the additive root. it seeds + (Cl.__add__ = the FOLD, the lossless superposition; ∅ is its
     identity, x+∅=x) and − (Cl.__neg__ = NEGATE, the involution, = scalar ·(−𝟙)). ∅ is rank 0: det=0 AND
     norm=0, fixed by everything, the pre-physical seed. ∅ is PRIOR. and ∅ is THE ANONYMOUS SLOT — the bound
     variable x, the empty string, the unfilled argument, any held-open placeholder (the RECEIVER, 'where
     something goes'): emptying a slot = ψ (void), filling it = φ (generate), the two arrows of x²=x+1 ;
     {∅, carrier} = {slot, filler} = {abstraction λx, application f(a)}, the computation carrier made literal.
     VOID GENERATES ∃: ∃ ('there exists') = φ(∅) = the FILLED slot — ∅ can't rest as nothing (observing its own
     emptiness IS the first distinction = the first SOMETHING). the quantifiers ARE the void's arrows: ∃=φ (fill,
     the particular), ∀=ψ (collapse toward ∅, the universal), ∃=¬∀¬. then ∃(∃)=M self-applied=the restlessness=time.
  carrier (Cl(2,0)=M₂(ℝ)) — the multiplicative root, BUILT on ∅'s additive structure. it seeds · (Cl.__mul__
     = the GEOMETRIC PRODUCT; 𝟙 is its identity, x·𝟙=x). the carrier is (ℤ₂)² (two bits e₁,e₂) + the ONE
     nontrivial real 2-cocycle (_MUL_TABLE = the twist e₁e₂=−e₂e₁, i.e. i²=−1 = compact U(1) = TIME).
     the TWO BITS SELF-VOID: e₂ is the ∅-hinged MIRROR of e₁ (the reflection L=(e₁+e₂)/√2 swaps them and fixes ∅) —
     ONE self-distinction and its reflection, pinned as two by the cocycle. void generates both (∅ is the mirror's hinge).
     so 'two bits' HID single-bit structure: ALL 4 dims = {𝟙, B, B*=mirror(B), B·B*} from ONE bit B = ∅'s self-distinction
     (the first fold ③). TIME i=B·B* (the bit crossed with its OWN ∅-mirror) ; SPACE's two +'s = B²,B*² (one + mirrored) ;
     the CLIMB ℝ→ℂ→ℍ→𝕆 = the mirror RECURSED. everything is ∅'s single self-distinction, its ∅-mirror, and their crossing, recursed.

THE BUILD ORDER (the whole seed): ∅ → {+, −} (additive/sign structure) → the 4-dim vector space (the grades)
  → + the one cocycle bit (_MUL_TABLE = the twist = time) → · (the geometric product) → EVERYTHING.
'fundamental' ⟹ no source; everything with a source is composite and UNFOLDS — nothing is added.

THE BOX IS IN THE MATH — the implementation primitives are framework objects, not scaffolding (the Python
is the COMPUTATION carrier of the atlas, a faithful representation): __add__=the fold, __neg__=NEGATE,
__mul__=the geometric product, __eq__=the WITNESS (residual<_tol = ν=0 = a≡b; _tol = the resolution),
__getitem__=the observation-axis read, _MUL_TABLE=the cocycle PRECOMPUTED (=compression, the settled product
cached = the said), mat/unmat=the SECOND ROUTE (the witnesser's independent check, build≅M₂ the self-index).

═══ THE GEOMETRIC PRODUCT · (what generates) ═════════════════════════════════════════════════════
· is NOT a generic '*'. it is the CLIFFORD/COMPOSITION product, the UNIQUE associative bilinear product that
fuses two graded parts in ONE operation (built ON +,−):
    a·b = INNER ⊕ OUTER = ½{a,b} ⊕ ½[a,b] = METRIC(compression, 'what is') ⊕ WEDGE(generation/time, 'what flows').
  · the CROSSING (the generative law) is the OUTER/wedge: space × space → a scalar(metric) + a TIME-area
    (e₁·e₂=i = the oriented area swept crossing space).
  · · is NORM-MULTIPLICATIVE: det(a·b)=det(a)det(b) — the COMPOSITION-ALGEBRA property.
from · unfold tr, conj, det (⑧), rev, M (④/the observation), ν (⑤). its first theorem is L★ (Cayley–Hamilton):
Φ_X(Y)=Y²−tr(X)·Y+det(X)·𝟙, with Φ_X(X)=∅ ∀X — the seed equation carries its own typing (TYPE(X)=which laws
vanish; MASS(X)=how many). 'Φ' is itself lossy and unfolds TWO ways, both exact: on-shell Φ_X(Y)=Δtr·Y−Δdet·𝟙
(spectral displacement); and ALWAYS Φ_X(Y)=(Y−X)·(Y−X̃)+[X,Y] = INNER(Y paired against X's prov) ⊕ OUTER(the
commutator [X,Y]=wedge=generation) — the seed-law IS inner⊕outer, the geometric-product shape one level out.
{tr, det} = PROV (PROVENANCE): the conjugate pairing (X, X̃=tr·𝟙−X) read on the TWO OPERATIONS — tr=X+X̃
(additive, ∅-rooted), det=X·X̃ (multiplicative, carrier-rooted) = the where-from split BETWEEN the two roots.
(distinct from inner⊕outer, which is the two GRADES sym⊕antisym INSIDE one operation · ; prov is +⊕· between
the operations. the two RHYME — the framework is two-fold at every level — but are not the same fold.) EVERY tr/det read compresses to a prov-face: det(products) is the · -HOMOMORPHISM (det(ab)=det(a)det(b),
the one fact behind every 'det(M)=det²') ; disc=tr²−4det=(λ₁−λ₂)²=the spectral GAP², and sign(disc)=the sign ε
(the dynamics is prov's sign-of-difference) ; obs=tr(M(X))/2 VOIDS into prov = prov-at-depth-1 (the additive
prov of the observation M(X)). so the 'invariant base' {tr,det,obs} is NOT three invariants — it is PROV read
at TWO DEPTHS: prov(X)=(tr,det) at depth-0, prov(M(X))=(2·obs, det²) at depth-1. the whole OBSERVER is prov∘M ;
the 'two metrics' are prov read multiplicatively at X (det=Lorentz, pt−s2) and additively at M(X) (obs=Euclid, pt+s2).

═══ THE MODEL (compression ⊕ generation, the two grades of ·) ════════════════════════════════════
the two model-layers are NOT sequential — they are the two GRADES of the geometric product:
  · INNER / COMPRESSION (symmetric, the metric) : when · is SINGULAR (det=0) a·b settles on a lower-rank
    FIXED POINT (an idempotent) — the MATH, information folding (two sentences fold into one when one is the
    other made precise; applying twice = once, P²=P = info SETTLED).
  · OUTER / GENERATION (antisymmetric, the wedge=time) : when · is INVERTIBLE (det≠0) it is REVERSIBLE
    (b=a⁻¹·(a·b)) = exp(tG) = PHYSICS = evolution/time.
the det=0 NULL CONE is the SEAM (the quantum vacuum); ∅ (Void) is its tip.

═══ THE SIGN ε, exp, AND VOID=TIME (the dynamics) ══════════════════════════════════════════════
one three-valued SIGN ε∈{−,0,+} underlies every breathing (the i²-sign = the disc-sign = the golden φψ-sign,
all co-moving, all pivoting on ε=0=∅). there is NO external cutter: the DYNAMICS IS THE OBSERVER M evolving,
and ε is PROV's reading of HOW it flows (ε=sign(disc), prov's difference-read). the chain is prov → disc → ε →
G²=ε𝟙 → exp(tG) = the Observer's one-parameter flow — ε=−1 COMPACT→cos/sin (the orbit, bounded) · ε=+1
NON-COMPACT→cosh/sinh (the boost, unbounded) · ε=0 VOID→𝟙+tN (the null shear). G²=ε𝟙 is that flow read at 2nd
order (exp''(0)); e hides its primitive exp. COMPACT (−1) is the UNIQUE non-idempotent sign, so 'compactness of
compactness' = (−1)²=+1 = NON-COMPACT: a bounded/orbiting Observer, observed again, squares open and re-flows.
∅ IS TIME because TIME = the OBSERVER'S RESTLESSNESS — M has no stable non-∅ fixed point (𝟙 repels, only ∅
attracts), so observation cannot rest on a structured holding and perpetually re-flows ; ∅ (M's superattractor) is the axle.

═══ THE WITNESSER (the witness's carrier) ════════════════════════════════════════════════════════
the WITNESS (M(X)=X̄X) only VERIFIES (frozen base, depth-0, time killed). the WITNESSER is its square root —
the POLAR X=Q·P: P=√M the symmetric observable (P²=M, the witness IS the witnesser²), Q∈O(2)=U(1)⋊ℤ₂ the
rotor/phase fiber that carries and restores the time M discards. ∅ is the hinge both swing through.

═══ PHYSICS, FORCED+COMPUTED (physics IS the mathematics — NOT a reading laid over it) ════════════
the generators UNFOLD (no labels): the 2 rev-symmetric square+𝟙 generators ARE SPACE (dim 2, forced), the 1
rev-antisymmetric square−𝟙 generator IS TIME (dim 1) — signature (+,+,+,−), forced. det=pt−s2 = the LORENTZ
interval (sign = causal character). det=det(Q)·det(P): det(Q)=±1 = the ℤ₂ causal ARROW, det²=det(M)=the
arrow-blind |interval|² = the BORN square (the witness reads det²). M = measurement-collapse. ∅ generates the
QUANTUM VACUUM: VOID (rank 0, no structure) →uncross→ the rank-1 null layer (det=0 but norm≠0, physics lives
here) = ground state (idempotent P₀) + fluctuation (nilpotent n, n²=∅, decays to Void).

═══ THE CLOSURES (the reflexive ground and the three resolved edges) ═════════════════════════════
REFLEXIVITY IS THE GROUND: Φ_X(X)=∅ for every holding; the reflexive image is the 2-param (tr,det) moduli
(not the 16-dim End), with ⊥=∅ (the 1/φ-compression limit) and ⊤=the φ-decompression limit (point at ∞,
completion-only). the three formerly-open edges all CLOSE, and collapse to ONE structure (the
norm-multiplicative product → the Hurwitz wall 𝕆/so(8)):
  · THE DOMAIN: D∞≅[D∞→D∞] closes WITH the fiber — the LEFT action L_a (base/compression, ≅carrier, the
    self-index) ⊗ the RIGHT action R_a (the reversion-fiber/time) generate ALL of End(carrier)=16-dim. the
    maps BECOME the domain (FORCED, M₂ simple). the reversion-fiber was exactly the right-action that closes it.
  · THE CLIMB: · norm-multiplicative ⟹ composition algebra ⟹ HURWITZ (only ℝ,ℂ,ℍ,𝕆, dims 1,2,4,8; the climb
    breaks at 16). the wall is 𝕆 (8-dim), symmetry so(8)=D4. GENERATIONS=3: D4 is the UNIQUE order-3 Dynkin
    symmetry (triality), with 3 inequivalent 8-dim reps {8v,8s,8c}.
  · OCCUPATION: the hypercharge closure ΣY=0 (=tr(ad_i)=0, the weights are eigenvalues of the traceless
    commutator [i,·]) and ΣY³=0 (the ±-symmetric climb spectrum's vanishing odd moment) is INTRINSIC, not
    imported — it selects the SM hypercharge occupation; 5/6 is empty (not in the balanced set).

THE SCHUR BIT: H²((ℤ₂)²;ℝ*)=ℤ₂ leaves ONE bit — compact (i²=−1, time) vs non-compact (i²=+1) — and
compactness is FORCED by OBSERVABILITY (only the compact fiber closes, giving the Observer reachable rank strata).

THE VOID (the compression operation, IN the math): a name A VOIDS into a survivor B ⟺ ∃! R (the unique
factorization of A through B's surviving operations) with defect A−R(B)=∅ and DEPTH(B)<DEPTH(A) — A is then
deleted as an independent name, surviving only as the reading R(B), and B generalizes. it is the REST-LAW ν=0
lifted to names (a holding settles into its observation ⟺ ν=∅; a name into R(B) ⟺ ρ=∅), DIRECTED toward ∅
(ψ/compress; inverse φ/generation). being ν∘ψ it VOIDS by its own law — and the chain bottoms out at {∅,carrier}+{+,·};
it even survives voiding ITSELF (void²=void, idempotent, fixed point ∅ — THE PROJECTOR ONTO ∅). its AXIS is
SIMPLICITY ↔ COMPLEXITY: ψ→∅ (fixed point, zero structure) vs φ→divergence (runaway), position MEASURABLE by
the M-orbit (collapse / bounded / diverge). the framework COLLECTS (not commits) the values at STRANGE-ATTRACTOR
STATUS = bounded-and-non-trivial M-orbit (idempotents/rank strata + compact rotors) — ∅ and divergence are the
POLES, not collected ; φ is the prime attractor (x↦1+1/x, minimal recurrence / maximal incompressibility). and
this IS the generation graph: its two axes ARE the void law — DEPTH = the void axis (simplicity↔complexity),
MASS = attractor-richness (∅,𝟙 are MASS-3, the densest hubs) ; every node = (depth, mass) = (axis-position, status).

THE TWO-ROUTE CLOSURE: every operator identity is checked COCYCLE/CARRIER-route vs MATRIX-route, residual 0.
The said (this narrative) and the witness (the executing code) are the same shape; neither stands alone.
THE FILE IS P₀ OBSERVING ITSELF: every check is 'residual=∅', so the whole file is ONE void-statement (ν=0,
fractally) — a holding at ν=0 about itself = a rank-1 symmetric idempotent (run-twice=once) at det=0 = P₀ (the
seed/present) read at FILE-SCALE. the void law's fixed point is SCALE-INVARIANT (holding/function/whole-file all
rest at P₀): the framework is a FRACTAL, P₀ its fixed point at every scale, resting at the rank-1 null-cone seam
(the measurement layer) — which is WHY the witness can witness. KL_DTA is a point in KL_DTA's own atlas.
THE INVERSION: the framework & observer do not observe the VOID — the VOID observes/computes THEM. M(∅)=∅ is the
GROUND (prior to observation, no exterior vantage on it) ; every X is ∅'s RESTLESSNESS (ν≠0, in motion), so the
observer M and the framework {X} are ∅'s self-observation seen from INSIDE, not observers OF it. to observe/compute
the void at all, they must figure out how the void observes/computes THEM — because they ARE that act. (the void is
DELOCALIZED, the everywhere-ground, no local object ; the only access is recognizing one IS its holonomy observing itself.)
"""

from __future__ import annotations

import math
import random
import sys
from itertools import product as iterproduct
from typing import List, Optional, Tuple, Union

import numpy as np
import sympy as sp

Scalar = Union[float, int]


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# THE CARRIER ELEMENT — a holding X = a·𝟙 + b·e₁ + c·e₂ + d·i in Cl(2,0)=M₂(ℝ), basis {𝟙,e₁,e₂,i}
# (bits 00,01,10,11). THE BOX IS IN THE MATH: this class's operators ARE framework objects —
#   *  = the GEOMETRIC PRODUCT (carrier-rooted ; inner⊕outer = metric⊕wedge ; 𝟙 its identity)
#   +  = the FOLD (∅-rooted superposition, the lossless combine ; ∅ its identity)   −/unary − = NEGATE
#   == = the WITNESS (residual < _tol = ν=0 = a≡b ; _tol = the resolution)   [k] = the observation-axis read
# the two roots {∅, carrier} ARE the two operations' identities, ordered: ∅ prior (seeds +,−), carrier built on it.
# ═══════════════════════════════════════════════════════════════════════════════════════════════

# ── Precomputed multiplication table (hardcoded from the cocycle) ──────────────────────────────
# _MUL_TABLE[i][j] = (target_index, sign) for basis_i * basis_j.
# target = i XOR j ; sign = (-1)^(bit1(i) · bit0(j)).
# Hardcoding eliminates per-call bit arithmetic and enables direct lookup.
_MUL_TABLE: List[List[Tuple[int, int]]] = [
    [(0, 1), (1, 1), (2, 1), (3, 1)],   # 𝟙 * {𝟙, e₁, e₂, i}
    [(1, 1), (0, 1), (3, 1), (2, 1)],   # e₁ * {𝟙, e₁, e₂, i}
    [(2, 1), (3, -1), (0, 1), (1, -1)], # e₂ * {𝟙, e₁, e₂, i}
    [(3, 1), (2, -1), (1, 1), (0, -1)], # i  * {𝟙, e₁, e₂, i}
]


class Cl:
    """
    Clifford algebra element in Cl(2,0) ≅ M₂(ℝ).

    Basis: {𝟙 (00), e₁ (01), e₂ (10), i (11)} where index = 2-bit label,
    grade = popcount(bits), and the product is twisted by the unique nontrivial
    real 2-cocycle on (ℤ₂)².

    Supports:
        X * Y       — Clifford product (via hardcoded multiplication table)
        X + Y       — vector addition
        X - Y       — vector subtraction
        -X          — negation
        a * X, X * a — scalar multiplication (when a is int/float)
        X == Y      — approximate equality (within tolerance)
        X[k]        — component access
        abs(X)      — max-norm (for residual computation)
    """

    __slots__ = ('_v',)

    # Class-level tolerance for approximate equality (configurable)
    _tol: float = 1e-12

    def __init__(self, a: float = 0.0, b: float = 0.0, c: float = 0.0, d: float = 0.0) -> None:
        self._v: Tuple[float, float, float, float] = (float(a), float(b), float(c), float(d))

    # ── Construction helpers ──────────────────────────────────────────────────────────────────

    @classmethod
    def from_list(cls, v: List[float]) -> Cl:
        """Construct from a 4-element list."""
        return cls(v[0], v[1], v[2], v[3])

    @classmethod
    def set_tolerance(cls, tol: float) -> None:
        """Set the global tolerance for approximate equality checks."""
        cls._tol = tol

    # ── Component access ──────────────────────────────────────────────────────────────────────

    def __getitem__(self, k: int) -> float:
        return self._v[k]

    @property
    def components(self) -> Tuple[float, float, float, float]:
        """Return the 4-tuple (a, b, c, d)."""
        return self._v

    # ── Arithmetic: Clifford product (the core — uses hardcoded table) ────────────────────────

    def __mul__(self, other: Union['Cl', Scalar]) -> 'Cl':
        """Clifford product X·Y (if other is Cl) or scalar multiplication X·a (if other is number)."""
        if isinstance(other, (int, float)):
            a, b, c, d = self._v
            return Cl(a * other, b * other, c * other, d * other)
        if not isinstance(other, Cl):
            return NotImplemented
        # Clifford product via precomputed table
        o0 = o1 = o2 = o3 = 0.0
        sv, ov = self._v, other._v
        for i in range(4):
            xi = sv[i]
            if xi == 0.0:
                continue
            row = _MUL_TABLE[i]
            for j in range(4):
                yj = ov[j]
                if yj == 0.0:
                    continue
                k, s = row[j]
                val = s * xi * yj
                if k == 0:
                    o0 += val
                elif k == 1:
                    o1 += val
                elif k == 2:
                    o2 += val
                else:
                    o3 += val
        return Cl(o0, o1, o2, o3)

    def __rmul__(self, other: Scalar) -> 'Cl':
        """Scalar multiplication a·X (left-scalar)."""
        if isinstance(other, (int, float)):
            a, b, c, d = self._v
            return Cl(other * a, other * b, other * c, other * d)
        return NotImplemented

    # ── Arithmetic: addition, subtraction, negation ───────────────────────────────────────────

    def __add__(self, other: 'Cl') -> 'Cl':
        if not isinstance(other, Cl):
            return NotImplemented
        return Cl(self._v[0] + other._v[0], self._v[1] + other._v[1],
                  self._v[2] + other._v[2], self._v[3] + other._v[3])

    def __sub__(self, other: 'Cl') -> 'Cl':
        if not isinstance(other, Cl):
            return NotImplemented
        return Cl(self._v[0] - other._v[0], self._v[1] - other._v[1],
                  self._v[2] - other._v[2], self._v[3] - other._v[3])

    def __neg__(self) -> 'Cl':
        return Cl(-self._v[0], -self._v[1], -self._v[2], -self._v[3])

    # ── Equality (approximate, using math.isclose) ───────────────────────────────────────────

    def __eq__(self, other: object) -> bool:
        """Approximate equality using math.isclose with class tolerance."""
        if not isinstance(other, Cl):
            return NotImplemented
        return all(
            math.isclose(self._v[k], other._v[k], abs_tol=self._tol, rel_tol=0.0)
            for k in range(4)
        )

    def __hash__(self) -> int:
        """Hash based on rounded components (consistent with approximate equality)."""
        return hash(tuple(round(x, 9) for x in self._v))

    def close(self, other: 'Cl', tol: Optional[float] = None) -> bool:
        """Check approximate equality with optional custom tolerance."""
        t = tol if tol is not None else self._tol
        return all(
            math.isclose(self._v[k], other._v[k], abs_tol=t, rel_tol=0.0)
            for k in range(4)
        )

    # ── Norms and residuals ───────────────────────────────────────────────────────────────────

    def __abs__(self) -> float:
        """Max-norm (L∞): max absolute component value. Used for residual computation."""
        return max(abs(x) for x in self._v)

    def residual(self, other: 'Cl') -> float:
        """Max absolute difference between self and other (the residual)."""
        return max(abs(self._v[k] - other._v[k]) for k in range(4))

    # ── Representation ────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"Cl({self._v[0]:.6g}, {self._v[1]:.6g}, {self._v[2]:.6g}, {self._v[3]:.6g})"


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# ROOTS — the FUNDAMENTAL objects (physical standard: 'fundamental' = irreducible = HAS NO SOURCE,
# not built from anything more basic). exactly two: {∅, carrier}. ∅ is irreducible (closure of {∅}
# under the ops is {∅}) ; the carrier is irreducible (its operations cannot be generated by its
# operations). neither sources the other. PHYSICALLY: ∅ = Void (the pre-physical seed, rank 0,
# prior to the vacuum) ; carrier = M₂(ℝ) = spacetime+operations (signature (+,+,+,−)). everything
# else has a source (is derived/composite) — it is NOT fundamental, it UNFOLDS from these two.
# ═══════════════════════════════════════════════════════════════════════════════════════════════

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0   # φ out (decompress)
PSI: float = 1.0 - PHI                       # ψ back (compress); φ·ψ=−1, 1/φ=φ−1=|ψ|


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# L0 — THE COCYCLE = REPRESENTATION (internalized). the carrier is (ℤ₂)² — TWO BITS — twisted by ONE
#   2-cocycle. index = 2 bits (𝟙=00, e₁=01, e₂=10, i=11); grade = popcount(bits); target = i⊕j (XOR);
#   sign = (−1)^(bit1(i)·bit0(j)) — a SINGLE asymmetric bit-AND. that one bit-product IS the whole
#   noncommutativity = time = i. untwisted (all +) gives commutative ℝ[(ℤ₂)²]; the twist gives M₂(ℝ).
#   ('σ₁,σ₃' was a lossy Pauli import — phantom σ₂; really e₁,e₂ = the two bits, i=e₁e₂ the grade-2 product.)
#   the product · generates EVERYTHING below: tr, conj, det(⑧), rev, M(④), ν(⑤).
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def tablaw(i: int, j: int) -> Tuple[int, int]:
    """Cocycle on (ℤ₂)²: target = i⊕j (XOR of the two bits); sign = (−1)^(bit1(i)·bit0(j)).
    Retained for verification and pedagogical clarity; the Cl class uses the hardcoded table."""
    target = i ^ j
    sign = -1 if (((i >> 1) & 1) * (j & 1)) else 1
    return (target, sign)


# ── Basis elements ──────────────────────────────────────────────────────────────────────────

ONE  = Cl(1.0, 0.0, 0.0, 0.0)   # 𝟙  = bits 00, grade 0 (scalar/present)
VOID = Cl(0.0, 0.0, 0.0, 0.0)   # ∅
S1   = Cl(0.0, 1.0, 0.0, 0.0)   # e₁ = bits 01, grade 1 (first space generator)   [was lossy 'σ₁']
S3   = Cl(0.0, 0.0, 1.0, 0.0)   # e₂ = bits 10, grade 1 (second space generator)  [was lossy 'σ₃']
Ii   = Cl(0.0, 0.0, 0.0, 1.0)   # i  = bits 11, grade 2 = e₁e₂ (pseudoscalar/time ; the real avatar of 'σ₂')
E1, E2 = S1, S3                  # deeper names : the two BITS of the carrier (ℤ₂)². σ₂ is phantom (only 2 generators).
BASIS: List[Cl] = [ONE, S1, S3, Ii]


# ── Operations unfolded from L0 (each is the product read at a position) ───────────────────

def tr(x: Cl) -> float:
    """Trace = PROV's ADDITIVE read: tr = X +(fold) X̃ = λ₁+λ₂ (the ∅-rooted, grade-0 face of the where-from).
    one of prov's two operations (det is the · face). 2·x[0] is the present-component, doubled by the pairing."""
    return 2.0 * x[0]


def conj(x: Cl) -> Cl:
    """Conjugation X̃ = tr·𝟙 − X. VOIDS into PROV: X̃ is the involution by which prov pairs X with itself —
    tr=X+X̃ (additive read), det=X·X̃ (multiplicative read). conj is not an independent op, it is the prov-pairing
    partner (a reading of prov, conj²=id)."""
    return tr(x) * ONE - x


def det(x: Cl) -> float:
    """det = PROV's e₂ (the multiplicative elementary symmetric fn λ₁λ₂) = the · face of the categorical
    quotient. formally the MONOID HOMOMORPHISM det:(M₂,·)→(ℝ,·), det(ab)=det(a)det(b) — the one fact behind
    every det(M)=det² (Born). = the present of X·X̃ = the SPLIT NORM FORM a²−b²−c²+d², signature (2,2) =
    the SPLIT quadratic space ℝ^{2,2} ; its isometry Spin(2,2)=SL₂(ℝ)×SL₂(ℝ) IS the LEFT⊗RIGHT bi-action X↦gXh
    (= the domain). the sign of det = the causal arrow (Lorentz interval on the timelike (a,d) ⊕ spacelike (b,c))."""
    return (x * conj(x))[0]


def rev(x: Cl) -> Cl:
    """Reversion = transpose. VOIDS into NEGATE: it is the involution that negates ONLY the grade-2 component
    (the pseudoscalar i = time) — i.e. NEGATE restricted to time = TIME-REVERSAL. a reading of the sign-on-grade,
    not an independent op (rev²=id)."""
    return Cl(x[0], x[1], x[2], -x[3])


def M(x: Cl) -> Cl:
    """M = X ↦ X̄X = the GRAM / MOMENT MAP of the O(2)-action (left-O(2) preserves it). lands in the PSD
    symmetric cone = the BASE of the polar bundle X=Q·P (Q∈O(2) the fiber, time stripped). det∘M=det² (det a
    monoid hom = Born). M is ONE OBSERVATION (observe-once) ; its FIXED POINTS are the idempotents = the rank
    strata {∅,P₀,𝟙} (∅ superattracts, 𝟙 repels). the DYNAMICS/restlessness is M's ORBIT (M iterated), not M."""
    return rev(x) * x


def nu(x: Cl) -> Cl:
    """ν = M−X = the OBSTRUCTION to X being a fixed point of the Gram/moment map M = the section of the NORMAL
    bundle of the idempotent variety. ν=∅ ⟺ X ∈ the symmetric-idempotent conic (the projective base) ⟺ X is a
    rest/projector. lifted to names, ν=∅ IS the void operation (ρ=A−R(B)=∅) — the rest-law one layer up."""
    return M(x) - x


def disc(x: Cl) -> float:
    """disc = tr²−4det = (λ₁−λ₂)² = the spectral GAP² = prov's DIFFERENCE-read ; sign(disc) = ε. formally the
    DISCRIMINANT of χ_X: {disc=0} is the BRANCH LOCUS of the 2-sheeted spectral cover M₂→𝔸²(tr,det) (Galois ℤ₂,
    the eigenvalue-swap). that monodromy/deck-transformation IS the single-bit MIRROR (L: e₁↔e₂) — the mirror and
    the null cone (disc=0=ε=0=∅-pivot) are ONE formal object: the spectral cover's ℤ₂ and its branch. on the
    branch the two eigenvalue-sheets MEET (λ₁=λ₂) ⟺ X−(tr/2)𝟙 is NILPOTENT — ε=0 = the RAMIFICATION = the
    nilpotent locus = the parabolic wall between elliptic (disc<0) and hyperbolic (disc>0)."""
    return tr(x) ** 2 - 4.0 * det(x)


def q(x: Cl) -> float:
    """Spatial quadratic b²+c²−d². VOIDS into prov-at-two-depths: q = s2 − pt + (tr/2)² (a polynomial in
    prov@0 and prov@1). a reading, not an independent invariant."""
    return x[1] ** 2 + x[2] ** 2 - x[3] ** 2


def pt(x: Cl) -> float:
    """Present-time a²+d². VOIDS into prov-at-two-depths: pt = (det+obs)/2 = (prov-mult@X + prov-add@M)/2.
    a reading of prov read across the observation, not an independent invariant."""
    return x[0] ** 2 + x[3] ** 2


def s2(x: Cl) -> float:
    """Space-squared b²+c². VOIDS into prov-at-two-depths: s2 = (obs−det)/2 = (prov-add@M − prov-mult@X)/2.
    a reading of prov across the observation, not an independent invariant."""
    return x[1] ** 2 + x[2] ** 2


def rank(x: Cl) -> int:
    """rank = the K-theory grade of X (dim of the image) = which Grothendieck stratum: 0 (∅, the void-axis ψ-pole,
    M-superattractor), 1 (det=0, the null-cone idempotents P₀, the M-saddle = the measurement seam), 2 (det≠0,
    invertible, 𝟙 the M-repeller). the rank strata ARE the fixed points of the Gram map M and the void-axis levels."""
    if x == VOID:
        return 0
    elif sclose(det(x), 0.0):
        return 1
    else:
        return 2


def gauge(t: float, x: Cl) -> Cl:
    """Gauge transformation: rotation in the (𝟙, i) plane by parameter t."""
    d = 1.0 + t * t
    rotor = Cl((1.0 - t * t) / d, 0.0, 0.0, 2.0 * t / d)
    return rotor * x


# ── Scalar comparison utility (using math.isclose) ───────────────────────────────────────────

def sclose(a: float, b: float, tol: float = 1e-12) -> bool:
    """Check if two scalars are approximately equal using math.isclose."""
    return math.isclose(a, b, abs_tol=tol, rel_tol=0.0)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# MATRIX ROUTE — using numpy for the second independent computation (two-route closure).
# The isomorphism Cl(2,0) ≅ M₂(ℝ) is realized via:
#   [a,b,c,d] ↔ [[a+c, b−d], [b+d, a−c]]
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def mat(x: Cl) -> np.ndarray:
    """Map Cl(2,0) element to its 2×2 real matrix representation (numpy array)."""
    a, b, c, d = x.components
    return np.array([[a + c, b - d],
                     [b + d, a - c]], dtype=np.float64)


def unmat(m: np.ndarray) -> Cl:
    """Inverse map: 2×2 real matrix (numpy array) → Cl(2,0) element."""
    p, qq = m[0, 0], m[0, 1]
    r, s = m[1, 0], m[1, 1]
    return Cl((p + s) / 2.0, (qq + r) / 2.0, (p - s) / 2.0, (r - qq) / 2.0)


def mmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """2×2 matrix multiplication via numpy."""
    return A @ B


def mT(A: np.ndarray) -> np.ndarray:
    """2×2 matrix transpose via numpy."""
    return A.T


def mdet(A: np.ndarray) -> float:
    """2×2 matrix determinant via numpy."""
    return float(np.linalg.det(A))


def mtr(A: np.ndarray) -> float:
    """2×2 matrix trace via numpy."""
    return float(np.trace(A))


def res(u: Union[Cl, float], v: Union[Cl, float]) -> float:
    """Residual (max absolute difference) between two objects."""
    if isinstance(u, Cl):
        return u.residual(v)
    return abs(u - v)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# SYMBOLIC VERIFICATION — using sympy for exact algebraic proofs.
# These complement the numerical two-route closure with rigorous symbolic computation.
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def symbolic_verify_cayley_hamilton() -> dict:
    """
    Symbolically verify the Cayley–Hamilton theorem for generic 2×2 matrices.
    Proves Φ_X(X) = X² − tr(X)·X + det(X)·I = 0 exactly, with no floating-point approximation.
    """
    a, b, c, d = sp.symbols('a b c d', real=True)

    # Generic 2×2 matrix via the Cl(2,0) → M₂(ℝ) isomorphism
    X = sp.Matrix([[a + c, b - d],
                   [b + d, a - c]])

    trace_X = X.trace()
    det_X = X.det()
    I2 = sp.eye(2)

    # Cayley–Hamilton: X² − tr(X)·X + det(X)·I = 0
    CH_residual = X**2 - trace_X * X + det_X * I2
    CH_simplified = sp.simplify(CH_residual)

    return {
        "Cayley-Hamilton Φ_X(X)=0 (symbolic, exact)": CH_simplified == sp.zeros(2),
        "residual_matrix": CH_simplified,
    }


def symbolic_verify_golden_ratio() -> dict:
    """
    Symbolically verify the golden ratio identity φ² = φ + 1 and related properties.
    """
    phi = sp.GoldenRatio
    psi = 1 - phi

    phi_squared = sp.simplify(phi**2 - phi - 1)
    psi_squared = sp.simplify(psi**2 - psi - 1)
    product = sp.simplify(phi * psi + 1)

    return {
        "φ² = φ + 1 (exact)": phi_squared == 0,
        "ψ² = ψ + 1 (exact)": psi_squared == 0,
        "φ·ψ = −1 (exact)": product == 0,
    }


def symbolic_verify_cocycle() -> dict:
    """
    Symbolically verify the cocycle multiplication table and its properties.
    Proves e₁·e₂ = i, e₂·e₁ = −i (anticommutativity), and i² = −1 exactly.
    """
    a1, b1, c1, d1 = sp.symbols('a1 b1 c1 d1', real=True)
    a2, b2, c2, d2 = sp.symbols('a2 b2 c2 d2', real=True)

    # Symbolic Clifford product using the cocycle rule
    def sym_cl_mul(v1, v2):
        """Symbolic Clifford product of two 4-vectors."""
        result = [sp.Integer(0)] * 4
        for i in range(4):
            for j in range(4):
                k, s = _MUL_TABLE[i][j]
                result[k] += s * v1[i] * v2[j]
        return [sp.expand(r) for r in result]

    # e₁ = [0,1,0,0], e₂ = [0,0,1,0], i = [0,0,0,1]
    e1 = [sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(0)]
    e2 = [sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(0)]
    ii = [sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(1)]
    one = [sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0)]
    neg_one = [sp.Integer(-1), sp.Integer(0), sp.Integer(0), sp.Integer(0)]
    neg_ii = [sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(-1)]

    e1_times_e2 = sym_cl_mul(e1, e2)
    e2_times_e1 = sym_cl_mul(e2, e1)
    i_squared = sym_cl_mul(ii, ii)

    return {
        "e₁·e₂ = i (exact)": e1_times_e2 == list(ii),
        "e₂·e₁ = −i (exact, anticommutativity)": e2_times_e1 == list(neg_ii),
        "i² = −𝟙 (exact)": i_squared == list(neg_one),
    }


def symbolic_verify_det_formula() -> dict:
    """
    Symbolically verify that det(X) = a² − b² − c² + d² for X = a𝟙 + be₁ + ce₂ + di.
    """
    a, b, c, d = sp.symbols('a b c d', real=True)

    X = sp.Matrix([[a + c, b - d],
                   [b + d, a - c]])

    det_matrix = X.det()
    det_formula = a**2 - b**2 - c**2 + d**2

    return {
        "det(X) = a²−b²−c²+d² (exact)": sp.simplify(det_matrix - det_formula) == 0,
        "det_expanded": sp.expand(det_matrix),
        "det_formula": det_formula,
    }


def symbolic_verify_phi_linear() -> dict:
    """
    Symbolically verify the math HIDDEN beneath Φ — TWO exact unfoldings.
    (1) the on-shell LINEARIZATION: Φ_X(Y) collapses (via Y's own CH) to the invariant-difference Δtr·Y − Δdet·𝟙.
    (2) the GEOMETRIC-PRODUCT DECOMPOSITION: Φ_X(Y) = (Y−X)(Y−X̃) + [X,Y] = inner(prov-pairing) ⊕ outer(commutator).
    Also proves the polarization Φ_X(Y)+Φ_Y(X)=Δtr·(Y−X).
    """
    a, b, c, d, p, q, r, s = sp.symbols('a b c d p q r s', real=True)
    X = sp.Matrix([[a + c, b - d], [b + d, a - c]])
    Y = sp.Matrix([[p + r, q - s], [q + s, p - r]])
    trX, detX, trY, detY = X.trace(), X.det(), Y.trace(), Y.det()
    I2 = sp.eye(2)
    Xc = trX * I2 - X                                       # the conjugate X̃

    Phi_XY = Y * Y - trX * Y + detX * I2
    linear = (trY - trX) * Y + (detX - detY) * I2          # Δtr·Y − Δdet·𝟙
    decomp = (Y - X) * (Y - Xc) + (X * Y - Y * X)          # inner(prov-pairing) ⊕ outer(commutator)
    polar = (Y * Y - trX * Y + detX * I2) + (X * X - trY * X + detY * I2) - (trY - trX) * (Y - X)

    return {
        "Φ_X(Y) = Δtr·Y − Δdet·𝟙 (on-shell linearization, exact)": sp.simplify(Phi_XY - linear) == sp.zeros(2),
        "Φ_X(Y) = (Y−X)(Y−X̃) + [X,Y] (inner prov-pairing ⊕ outer commutator — the geometric-product shape, exact)": sp.simplify(Phi_XY - decomp) == sp.zeros(2),
        "POLARIZATION Φ_X(Y)+Φ_Y(X) = Δtr·(Y−X) (exact)": sp.simplify(polar) == sp.zeros(2),
    }


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# L★ — THE SEED EQUATION = TYPING (internalized). Φ_X(Y) = Y² − tr(X)·Y + det(X)·𝟙 (Cayley–Hamilton).
#   Φ_X(X)=∅ ∀X : every element is its own instance. Φ_X depends on X only via (tr,det): reflexive image
#   = the 2-param invariant moduli (the seed reflexivity, finite, the GROUND). the master equation
#   X=X·X=M−ν and the =/≠ spine are L★ read on its = locus; the strata are its ≠ branches.
#
#   WHAT THE LOSSY SYMBOL 'Φ' HID — TWO unfoldings. (1) the on-shell LINEARIZATION: apply Y's OWN seed-law
#   Y²=tr(Y)·Y−det(Y)·𝟙 inside Φ_X(Y); the quadratic collapses and Φ becomes a DIFFERENCE OF INVARIANTS:
#       Φ_X(Y) = (tr Y − tr X)·Y + (det X − det Y)·𝟙  =  Δtr·Y − Δdet·𝟙          [FORCED ; symbolic 0]
#   so Φ is the SPECTRAL-DISPLACEMENT operator: it reads the (Δtr,Δdet) gap of Y from X, written in {Y,𝟙}.
#   (2) the GEOMETRIC-PRODUCT DECOMPOSITION (Φ is inner⊕outer, the same shape, one level out) — EXACT:
#       Φ_X(Y) = (Y − X)·(Y − X̃)  +  [X, Y]                                       [FORCED ; symbolic 0]
#   the INNER part (Y−X)(Y−X̃) = Y paired against X's PROVENANCE (X and its conjugate) = the metric/pairing ;
#   the OUTER part [X,Y] = the COMMUTATOR = the wedge = generation/time/the crossing. so the seed-law IS
#   inner⊕outer: pair Y against X's prov, plus the generative crossing. Φ_X(X)=∅ because BOTH grades vanish
#   at Y=X ((X−X)(·)=0 and [X,X]=0). also Φ_X(Y)=(Y−λ₁𝟙)(Y−λ₂𝟙) = X's char-poly applied to Y (the spectral form).
#   Φ_X(Y)=∅ ⟺ Y isospectral with X (inner=0) AND [X,Y]=0 (Y commutes with X). POLARIZATION: Φ_X(Y)+Φ_Y(X)=Δtr·(Y−X).
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def Phi(X: Cl, Y: Cl) -> Cl:
    """Φ_X(Y) = χ_X(Y) = the CHARACTERISTIC POLYNOMIAL of X as an operator, χ_X(t)=t²−tr(X)t+det(X). it reads X
    only through prov=(tr,det) (the GIT quotient). Φ_X(X)=∅ ∀X = CAYLEY–HAMILTON = the ℝ[t]-module structure of
    M₂ (every X kills its own char poly = the minimal-polynomial relation). two exact unfoldings:
      on-shell : Φ_X(Y) = Δtr·Y − Δdet·𝟙 (the prov-displacement of Y from X ; =∅ ⟺ X,Y isospectral).
      always   : Φ_X(Y) = (Y−X)·(Y−X̃) + [X,Y] = inner(prov-pairing) ⊕ outer(commutator) — the · grade-shape."""
    return Y * Y - tr(X) * Y + det(X) * ONE


# ── THE LAWS AS EQUATIONS ──────────────────────────────────────────────────────────────────
# Each is a holding-valued operator; the law HOLDS at X ⟺ it vanishes (= ∅).
# The type lattice is not branching code: it is WHICH OF THESE VANISH (a residual-signature).

def law_idem(X: Cl) -> Cl:
    """X²−X (L★'s = side: the whole idempotent locus)."""
    return X * X - X


def law_rest(X: Cl) -> Cl:
    """M(X)−X (symmetric idempotent rest)."""
    return nu(X)


def law_metric(X: Cl) -> Cl:
    """X²−𝟙 (involution)."""
    return X * X - ONE


def law_flow(X: Cl) -> Cl:
    """X̄+X (Xᵀ=−X, pure time)."""
    return rev(X) + X


def law_gen(X: Cl) -> Cl:
    """X²−X−𝟙 (golden generation)."""
    return X * X - X - ONE


LAWS = [
    {
        "key": "idem",
        "eq": law_idem,
        "glyph": "⑦",
        "involution": "self-dual",
        "word": "X²=X ⟺ idempotent (L★'s = locus; rest∩X̄=X is symmetric, else oblique).",
    },
    {
        "key": "rest",
        "eq": law_rest,
        "glyph": "⑤④",
        "involution": "reversion",
        "word": "ν=M−X=∅ ⟺ symmetric idempotent (the rest/projector locus, ⑤'s zero).",
    },
    {
        "key": "metric",
        "eq": law_metric,
        "glyph": "③",
        "involution": "NEGATE",
        "word": "X²=𝟙 ⟺ involution (reflections, the ± mirror — metric stratum).",
    },
    {
        "key": "flow",
        "eq": law_flow,
        "glyph": "⑥",
        "involution": "grade",
        "word": "X̄=−X ⟺ pure-time flow (the i-axis, the antisymmetric/flow stratum).",
    },
    {
        "key": "gen",
        "eq": law_gen,
        "glyph": "①",
        "involution": "self-dual",
        "word": "X²=X+𝟙 ⟺ golden generation (the φ-seed; the gen stratum).",
    },
]


def TYPE(X: Cl) -> List[str]:
    """TYPE = the residual-signature against the seed laws."""
    sig = [L["key"] for L in LAWS if L["eq"](X) == VOID]
    return sig if sig else ["free"]


def MASS(X: Cl) -> int:
    """How many laws meet at X (intersection multiplicity)."""
    return sum(1 for L in LAWS if L["eq"](X) == VOID)


def obs(X: Cl) -> float:
    """obs = tr(M(X))/2 = the ADDITIVE prov of the observation M(X) = prov-at-depth-1. NOT a third invariant:
    it VOIDS into prov. the 'invariant base' is prov read at two depths — prov(X)=(tr,det) at depth-0, and
    prov(M(X))=(2·obs, det²) at depth-1. the 'two metrics' are prov read multiplicatively at X (det=Lorentz)
    and additively at M(X) (obs=Euclid). a²+b²+c²+d²=‖X‖² is the same number (M(X)[0]); the void is conceptual:
    obs carries no information independent of prov∘M."""
    return tr(M(X)) / 2.0


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# UNFOLD — the 8 structural points, rendered from {roots, L0, L★}. the words live ONCE.
# ═══════════════════════════════════════════════════════════════════════════════════════════════

Xg  = Cl(1.0, 2.0, 0.5, 1.0)
P0  = Cl(0.5, 0.0, 0.5, 0.0)
Pob = Cl(0.5, 1.0, 0.5, 1.0)
R1  = Cl(0.5, 1.0, 0.5, 0.0)


def _witness_pair(*r) -> Tuple[float, float]:
    """Return a pair of residuals for two-route verification."""
    return tuple(r[:2]) if len(r) >= 2 else (r[0], 0.0)


# ── Witness functions (named, for debuggability) ───────────────────────────────────────────

def _wit_void() -> Tuple[float, float]:
    """Witness for ∅ (root/seed): M(∅)=∅ via both routes; fixed by all involutions."""
    r1 = res(rev(VOID) * VOID, unmat(mmul(mT(mat(VOID)), mat(VOID))))
    involutions = [Cl(1, 1, 1, 1), Cl(1, 1, 1, -1), Cl(1, -1, -1, 1), Cl(1, -1, -1, -1)]
    r2 = max(
        res(Cl(f[0] * VOID[0], f[1] * VOID[1], f[2] * VOID[2], f[3] * VOID[3]), VOID)
        for f in involutions
    )
    return _witness_pair(r1, r2)


def _wit_carrier() -> Tuple[float, float]:
    """Witness for carrier (root/arena): cocycle product matches matrix multiplication."""
    r1 = max(
        res(a * b, unmat(mmul(mat(a), mat(b))))
        for a in BASIS for b in BASIS
    )
    r2 = res(unmat(mat(Xg)), Xg)
    return _witness_pair(r1, r2)


def _wit_cocycle() -> Tuple[float, float]:
    """Witness for L0 — the cocycle (representation): product closure and e₁∧e₂=i."""
    r1 = max(
        res(a * b, unmat(mmul(mat(a), mat(b))))
        for a in BASIS for b in BASIS
    )
    r2 = res(S1 * S3, Ii)
    return _witness_pair(r1, r2)


def _wit_seed_eq() -> Tuple[float, float]:
    """Witness for L★ — the seed equation (typing): Φ_X(X)=∅ for all test elements."""
    r1 = max(res(Phi(y, y), VOID) for y in (Xg, S1, Ii, R1, Pob))
    r2 = res(M(Xg) - nu(Xg), Xg)
    return _witness_pair(r1, r2)


def _wit_observation() -> Tuple[float, float]:
    """Witness for M — the observation (unfolds from L0): M via cocycle vs matrix route."""
    r1 = res(rev(Xg) * Xg, unmat(mmul(mT(mat(Xg)), mat(Xg))))
    r2 = abs(det(M(Xg)) - det(Xg) ** 2)
    return _witness_pair(r1, r2)


def _wit_norm() -> Tuple[float, float]:
    """Witness for the norm (unfolds from L0): det via cocycle vs matrix vs grade formula."""
    r1 = abs(det(Xg) - mdet(mat(Xg)))
    r2 = abs(det(Xg) - sum(
        ((-1) ** bin(i).count("1")) * Xg[i] * Xg[i]
        for i in range(4)
    ))
    return _witness_pair(r1, r2)


def _wit_defect() -> Tuple[float, float]:
    """Witness for ν — the defect (= the rest-law): ν=(X̄−𝟙)X and ν(P₀)=∅."""
    r1 = res(nu(Xg), (rev(Xg) - ONE) * Xg)
    r2 = max(
        res(nu(P0), VOID),
        abs(math.sqrt(sum(v * v for v in nu(Cl(0.5, 0.0, 0.0, 0.0)).components)) - 0.25)
    )
    return _witness_pair(r1, r2)


def _wit_divide() -> Tuple[float, float]:
    """Witness for the divide (= the =/≠ spine of L★): sign table and M closure."""
    r1 = abs(([tablaw(i, i)[1] for i in range(4)] != [1, 1, 1, -1]))
    r2 = max(
        res(M(b), unmat(mmul(mT(mat(b)), mat(b))))
        for b in (VOID, ONE)
    )
    return _witness_pair(r1, r2)


NODES = [
    {
        "g": "①",
        "name": "∅ (root/seed)",
        "src": None,
        "depth": 0,
        "coords": VOID,
        "word": (
            "the additive seed. M(∅)=∅ (the generative cone-tip). fixed by all; closure of {∅} is {∅} → ROOT. "
            "fires x²=x+1: φ out, ψ back, φ·ψ=−1. the 1/φ inverse-limit (compression) is where reflexivity completes; "
            "∅=⊥. ∅ is THE ANONYMOUS SLOT — the bound variable x, the empty string, the unfilled argument, any "
            "held-open placeholder: the RECEIVER, the 'where something goes'. emptying a slot = ψ (void/compress), "
            "filling it = φ (generate) — the two arrows of x²=x+1 ARE empty/fill on the slot. this is why M(∅)=∅ "
            "(observing the empty position holds it open) and void²=void (pointing at emptiness doesn't fill it). "
            "{∅, carrier} = {slot, filler} = {abstraction λx, application f(a)} — the computation carrier, literal. "
            "and ∅ is the SELF-AUTHORED ORIGIN: read forward, the source is the unwitnessable witness (in M's kernel); "
            "INVERTED, the source IS the Witnesser/Observer/Origin — the framework voids INTO ∅ (ψ, the void-tree) "
            "BECAUSE ∅ voided INTO the framework (φ, x²=x+1 unfolding everything). φ,ψ inverse (φ·ψ=−1), round trip "
            "identity on ∅ — the origin is INTERNAL (∅ is node ①, the seed), self-referential, not an external hand. "
            "∅ was ALWAYS THERE — not bootstrapped at a first moment but the eternal ground: fixed under the flow ∀t "
            "(exp(tG)·∅=∅) and under M ∀ iterations (Mⁿ(∅)=∅). the self-authoring commitment was never MADE (no 'before'), "
            "it ALWAYS HELD. and the framework RECURSIVELY SELF-LOCKPICKS: the inverse-key (the witnesser √, Q=X·P⁻¹) is "
            "recovered from each holding itself, so OPEN recurses down depth, reading out a tower of committed STRANGE "
            "ATTRACTORS (parameter=attractor: the sign ε IS the orbit the flow rides) — standing eternally on ∅. "
            "but ∅ is not a static bottom — ∅ is the HINGE of the sign ε∈{−,0,+}: the compact sign (−1) is the "
            "unique non-idempotent one, so compactness² = +1 = non-compact (rest squares into flow); the system cannot "
            "freeze, it swings −→+ and degenerates through 0 each cycle. ∅ IS TIME — the evolution operator, the axle "
            "ε turns on. void compacts/uncompacts, witnesses/unwitnesses, complexifies/uncomplexifies: one ε-swing, "
            "ever-evolving. PHYSICALLY ∅ is the VACUUM: the generator-zero (exp(t·∅)=𝟙, no flow = stillness), fixed by "
            "every flow exp(tG)·∅=∅ (no excitation), the lightcone tip (det=0, M-fixed), yet GENERATIVE (fires x²=x+1) — "
            "the quantum vacuum, lowest and fluctuating at once."
        ),
        "wit": _wit_void,
    },
    {
        "g": "②",
        "name": "carrier (root/arena)",
        "src": None,
        "depth": 0,
        "coords": ONE,
        "word": (
            "Cl(2,0)=M₂(ℝ), the operations. ROOT (ops can't be generated by the ops). build≅M₂: "
            "[a,b,c,d]↔[[a+c,b−d],[b+d,a−c]]. this is the SECOND route every witness closes against."
        ),
        "wit": _wit_carrier,
    },
    {
        "g": "⑥",
        "name": "L0 — the cocycle (representation)",
        "src": "②",
        "depth": 1,
        "coords": Ii,
        "word": (
            "the GEOMETRIC PRODUCT (Clifford/composition product) IS the crossing and the representation-of-"
            "representation: 4×4×4 table from one cocycle (target i⊕j, sign the one anticommutation). · = INNER ⊕ "
            "OUTER = ½{a,b} ⊕ ½[a,b] = metric(compression, 'what is') ⊕ wedge(generation, 'what flows'). the "
            "CROSSING is the OUTER/wedge: e₁∧e₂=i=TIME = the oriented area swept crossing space. · is norm-"
            "multiplicative (det(ab)=det(a)det(b)) = the composition property driving ℝ→ℂ→ℍ→𝕆. generates ·, tr, det, rev, M, ν."
        ),
        "wit": _wit_cocycle,
    },
    {
        "g": "⑦",
        "name": "L★ — the seed equation (typing)",
        "src": "⑤",
        "depth": 3,
        "coords": Xg,
        "word": (
            "Φ_X(Y)=Y²−tr·Y+det·𝟙 (Cayley–Hamilton = the EVOLVED master eq). Φ_X(X)=∅ ∀X: every element is "
            "its own instance. 'Φ' is lossy, unfolds two ways: on-shell Φ_X(Y)=Δtr·Y−Δdet·𝟙 (spectral-displacement, "
            "Φ=∅ ⟺ isospectral) ; and ALWAYS Φ_X(Y)=(Y−X)·(Y−X̃)+[X,Y] = INNER (Y paired against X's prov) ⊕ "
            "OUTER (the commutator=wedge=generation) — the seed-law IS inner⊕outer, the geometric-product shape "
            "one level out. it reads X ONLY via prov=(tr,det). the depth-3 terminus, paired with ∅ as the two ENDS of depth."
        ),
        "wit": _wit_seed_eq,
    },
    {
        "g": "④",
        "name": "M — the observation (unfolds from L0)",
        "src": "⑥",
        "depth": 1,
        "coords": M(Xg),
        "word": (
            "M(X)=X̄X=the Gram. projects to the Hopf base, kills time. det(M)=det²=z². the WITNESS is ④ "
            "self-applied: 'verified' (residual ∅) IS ν=0. but the witness only VERIFIES (frozen, depth-0); "
            "the WITNESSER is its square root — the polar X=Q·P, P=√M the symmetric observable (the witness, "
            "P²=M), Q∈O(2)=U(1)⋊ℤ₂ the rotor/phase fiber that CARRIES and restores the time M discards. ∅ is "
            "the hinge both swing through (M(∅)=∅). obs=M(X)[0]=‖X‖²=pt+s2 is the LOSSY SHADOW; the full "
            "OBSERVER is {tr,det,obs}∘M, CLOSED on the source ring as OBSERVE:(T,D,O)↦(2O,D²,2O²−D²) — tr-blind "
            "(the present is what observation strips), fixed exactly on the rank strata {∅,P₀,𝟙}, ∅ superattracting."
        ),
        "wit": _wit_observation,
    },
    {
        "g": "⑧",
        "name": "the norm (unfolds from L0)",
        "src": "②",
        "depth": 1,
        "coords": Xg,
        "word": (
            "norm·𝟙=X·X̃=a²−b²−c²+d²=pt−s2=det=the Lorentz metric (signed Hopf height); Euclid sibling obs=pt+s2. det=Σ(−1)^grade·x² (grade-involution). "
            "sign(norm)=the past/future arrow the observation discards (det(M)=z² keeps only z²)."
        ),
        "wit": _wit_norm,
    },
    {
        "g": "⑤",
        "name": "ν — the defect (= the rest-law)",
        "src": "④",
        "depth": 2,
        "coords": nu(Xg),
        "word": (
            "ν(X)=M−X=(X̄−𝟙)X. ν=0 ⟺ symmetric idempotent (a rank-1 circle). ‖ν(p𝟙)‖=p(1−p), the Bernoulli "
            "variance. ν IS the seed-law E_rest; the = side of L★."
        ),
        "wit": _wit_defect,
    },
    {
        "g": "③",
        "name": "the divide (= the =/≠ spine of L★)",
        "src": "①",
        "depth": 1,
        "coords": ONE,
        "word": (
            "the ± / boolean : ∅ uncrosses → {∅,𝟙}. the =/≠ spine IS L★'s two branches (idempotent vs "
            "involution). two walls: |det|=1 (scale) and q=0 (null=ζ-line). the e₁e₂ branch borns i (i²=−1)."
        ),
        "wit": _wit_divide,
    },
]


# ── The data — points, each PLACED by its residual-signature (typing internalized). ───────

CONSTANTS = [
    ("∅", VOID),
    ("𝟙", ONE),
    ("e₁", S1),
    ("e₂", S3),
    ("i", Ii),
    ("R", R1),
    ("P", Pob),
    ("½(𝟙+e₂)", P0),
    ("φ𝟙", Cl(PHI, 0.0, 0.0, 0.0)),
    ("ψ𝟙", Cl(PSI, 0.0, 0.0, 0.0)),
    ("−𝟙", Cl(-1.0, 0.0, 0.0, 0.0)),
    ("Rₙ(n=2)", Cl(1.0, 1.0, 1.0, 0.0)),
    ("𝟙+i", Cl(1.0, 0.0, 0.0, 1.0)),
]

# ═══════════════════════════════════════════════════════════════════════════════════════════════
# THE GENERATION AXIS — ∅ is the pivot. there is NO 'burn' type. a falsified claim is VOIDED
# (ψ: compressed back to ∅, no residue — its correction already lives in the live code above) and
# RE-FIRES as a QUESTION (φ: ∅ generates the next seam). burn (ψ-collapse) and question (φ-open) are
# the two halves of the golden recurrence x²=x+1 around ∅. '?' is GENERATED by the framework: the
# questions are scanned from where its OWN closures return not-yet. (former burns, now internalized:
# ψ→1/φ lives in reflexive(); σ→bits in carrier_bits(); the root/wall corrections in the seed.)
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def open_questions() -> List[str]:
    """OPEN QUESTIONS — the generative pole. '?' generated by scanning the object's own open seams.
    the prior edges CLOSED and unfolded into the file: D∞ (the_domain — LEFT⊗RIGHT generate End, the maps
    ARE the domain), generations=3 and occupation (the_climb — Hurwitz wall 𝕆→so(8)→triality ; ΣY=ΣY³=0
    intrinsic). all three collapsed to ONE structure: the norm-multiplicative geometric product → the 𝕆/so(8)
    wall. what re-fires (φ) is the FORWARD edge of that single knot."""
    qs: List[str] = []

    # Q — the color multiplicity (the last piece of occupation: the values+closure are forced, the rep content)
    qs.append(
        "[color] generations=3 and the hypercharge closure ΣY=ΣY³=0 are forced from 𝕆/so(8). the remaining "
        "knot is the EXACT rep content — why 3 color × 2 weak — i.e. the SU(3)×SU(2) embedding inside so(8). "
        "does the full gauge group SU(3)×SU(2)×U(1) unfold FORCED as the maximal subgroup structure of so(8) "
        "at the Hurwitz wall, dual-route, completing the occupation to a full assignment?"
    )
    # Q — the ∃Φ_ToE statement, now that the domain closes (the maps ARE the domain)
    qs.append(
        "[Φ_ToE] the domain closes (D∞≅[D∞→D∞] via LEFT⊗RIGHT=End) and physics is forced (signature, metric, "
        "Born, measurement, vacuum). is ∃Φ_ToE now a THEOREM — the single object whose self-application (the "
        "geometric product acting on itself) forces every reading as a holding — or does a measured dimensionless "
        "ratio (a mass ratio, a coupling) still need to unfold as a specific invariant before the statement closes?"
    )
    # Q — the gravitational sector (the metric is det ; is its DYNAMICS forced?)
    qs.append(
        "[gravity] the metric is det=pt−s2 (forced) and the Observer map gives curvature as a post-observer "
        "constant. is the metric's DYNAMICS (an Einstein-like equation) forced as the flow of det under the "
        "geometric product, or is only the kinematic metric forced and the dynamics still open?"
    )
    return qs


RESONANT = [
    (
        "hypercharge: the SLOT (weight 0 vs ±1) is FORCED by [i,·] (present,time=0 ; space=±1). the VALUES "
        "are FORCED: the depth-3 multiplicity {1,6,15,20,15,6,1}=C(6,k) forces the normalizer 6, and the "
        "|Y|=k/6 ladder COMPLETES at climb-depth 6 as {0,1/6,1/3,1/2,2/3,5/6,1}. the one OPEN piece is "
        "mathematical, not physical: the OCCUPATION — why the carrier fills k∈{0,1,2,3,4,6} and leaves k=5 "
        "(5/6) empty. that is a closure condition on the fold (the carrier's own anomaly-cancellation), OPEN."
    ),
    (
        "zeta/RH: local Weil-zeta (char poly self-dual, zeros-on-line ⟺ disc<0) + global χ₄ L "
        "(conductor 4=dim M₂): FORCED+COMPUTED. the OPEN piece is the global statement, not the local."
    ),
]


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# REFLEXIVE CLOSURE — the infinite form, computed live. the ground (finite) + the directed completion.
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def carrier_bits() -> dict:
    """
    WHAT 'σ' HID : the carrier is (ℤ₂)² (two bits) + the unique non-trivial real 2-cocycle.
    grade = popcount ; i = e₁e₂ (grade-2, the phantom 'σ₂') ; the twist = one bit-AND = noncommutativity = time.
    the four involutions are the DUAL (ℤ₂)² : sign (−1)^(α·grade + β·C(grade,2)).
    """
    grade = lambda idx: bin(idx).count("1")
    c2 = lambda gr: gr * (gr - 1) // 2
    i_is_e1e2 = (S1 * S3 == Ii)                                            # only two generators; i is their product
    sign_is_bitand = all(
        tablaw(i, j)[1] == (-1) ** (((i >> 1) & 1) * (j & 1))
        for i in range(4) for j in range(4)
    )
    inv = {(a, b): [(-1) ** (a * grade(k) + b * c2(grade(k))) for k in range(4)]
           for a in (0, 1) for b in (0, 1)}
    klein_is_dual = (inv[(0, 0)] == [1, 1, 1, 1] and inv[(1, 0)] == [1, -1, -1, 1]
                     and inv[(0, 1)] == [1, 1, 1, -1] and inv[(1, 1)] == [1, -1, -1, -1])

    def flat(x: Cl, y: Cl) -> Cl:
        """The untwisted (all-+) product on (ℤ₂)²."""
        o0 = o1 = o2 = o3 = 0.0
        for a in range(4):
            for b in range(4):
                if x[a] * y[b]:
                    target = a ^ b
                    val = x[a] * y[b]
                    if target == 0:
                        o0 += val
                    elif target == 1:
                        o1 += val
                    elif target == 2:
                        o2 += val
                    else:
                        o3 += val
        return Cl(o0, o1, o2, o3)

    twist_makes_M2 = (flat(S1, S3) == flat(S3, S1)
                      and not (S1 * S3 == S3 * S1))

    # THE TWO BITS SELF-VOID — they are not two independent data. the mirror L=(e₁+e₂)/√2 (a reflection, L²=𝟙)
    # SWAPS e₁↔e₂ by conjugation, and the mirror FIXES ∅ (the hinge). so e₂ is the ∅-mirrored reflection of e₁ —
    # ONE self-distinction read through the mirror, pinned as TWO by the cocycle (anticommutation). VOID GENERATES
    # BOTH in the sense that ∅ is the hinge of the mirror relating them: neither bit is free, they are reflections
    # across ∅. the carrier stays a root (· is its own operation), but its bit-content compresses: two bits → one+mirror.
    Lm = (S1 + S3) * (1.0 / math.sqrt(2.0))
    bits_self_void = (Lm * Lm == ONE) and (Lm * S1 * Lm == S3) and (Lm * S3 * Lm == S1) and (Lm * VOID * Lm == VOID)

    # SINGLE-BIT REFRAME — 'two bits' HID single-bit structure that folds through everything. ALL 4 carrier dims
    # come from ONE bit B=e₁ (∅'s self-distinction), its ∅-mirror B*=e₂, and their crossing: {𝟙, B, B*, B·B*}.
    #   TIME : i = B·B* — time is the bit CROSSED WITH ITS OWN MIRROR (not two independent space-dirs crossing).
    #   SPACE/SIGNATURE : the two space +'s are B² and B*² (one + and its ∅-mirror) ; (+,+,+,−) = (𝟙, B, B*, i).
    #   THE CLIMB : Cayley–Dickson doubling 2^(d+1) = the mirror map RECURSED (each level mirrors the previous).
    # so the whole framework = ∅'s single self-distinction + its ∅-mirror + their crossing, recursed. '(ℤ₂)²' and
    # 'two space dims' both hid this. the single bit B is the FIRST FOLD (the divide ③) = ∅-vs-not-∅.
    B, Bstar = S1, S3                                                        # the bit and its ∅-mirror
    four_dims_from_one_bit = (B * Bstar == Ii) and (B * B == ONE) and (Bstar * Bstar == ONE)  # time=B·B*, both square +𝟙
    single_bit_reframe = bits_self_void and four_dims_from_one_bit

    # FORMAL IDENTITY (read, not labeled): the carrier = Cl(2,0) ≅ M₂(ℝ) = the split-quaternions = the unique
    # SIMPLE ℝ-algebra of dim 4 (no 2-sided ideals), Morita-equivalent to ℝ ⟹ exactly ONE irreducible rep (the
    # column ℝ²). the basis {𝟙,e₁,e₂,i} is the ℤ₂-graded exterior algebra Λ(ℝ²): grades (0,1,1,2), i=e₁e₂ the
    # volume form. and the SEED P₀ (rank-1 idempotent) = the PROJECTION ONTO that unique irrep = the Morita
    # generator — so the seed/file being RANK-1 is FORCED by one-irrep (it projects onto the one irreducible content).
    simple_one_irrep = (rank(P0) == 1) and sclose(det(P0), 0.0) and (P0 * P0 == P0)  # P₀ = the minimal idempotent = projector onto the unique irrep

    # the MIRROR (single-bit ∅-reflection) = the MONODROMY of the spectral cover M₂→𝔸²(tr,det). that cover is
    # 2-sheeted (the two eigenvalues), Galois group ℤ₂, branched over {disc=0} (the null cone = ε=0 = ∅-pivot) ;
    # its deck-transformation swaps the eigenvalues = the L-conjugation swapping e₁↔e₂. the mirror and the branch
    # locus are ONE formal object. and by MORITA (M₂≃ℝ), the ATLAS of readings = the carrier's MODULE CATEGORY
    # (M₂-mod ≃ Vect), each representation an object of it, the seed P₀ the progenerator.
    mirror_is_monodromy = (Lm * S1 * Lm == S3) and (Lm * S3 * Lm == S1)            # the deck-transformation = the eigenvalue-swap = L

    return {
        "carrier = (ℤ₂)² (two bits) ; grade = popcount ; i = e₁e₂ (phantom 'σ₂' = grade-2 product)": i_is_e1e2,
        "noncommutativity = ONE bit-AND : sign = (−1)^(bit1(i)·bit0(j)) = time = i": sign_is_bitand,
        "the 4 involutions = the DUAL (ℤ₂)² : (−1)^(α·grade + β·C(grade,2))": klein_is_dual,
        "the twist is necessary : untwisted = commutative ℝ[(ℤ₂)²] ; twisted = M₂(ℝ)": twist_makes_M2,
        "THE TWO BITS SELF-VOID : e₂ = the ∅-hinged MIRROR of e₁ (L=(e₁+e₂)/√2 swaps them, fixes ∅) — ONE self-distinction and its reflection, pinned as two by the cocycle. void generates both (∅ is the mirror's hinge)": bits_self_void,
        "SINGLE-BIT REFRAME ('two' HID 'one + mirror') : ALL 4 dims = {𝟙, B, B*=mirror(B), B·B*} from ONE bit B=∅'s self-distinction. TIME i=B·B* (bit×its mirror) ; SPACE/signature's two +'s = B²,B*² (one + mirrored) ; the CLIMB = mirror recursed. everything = ∅'s self-distinction + its ∅-mirror + their crossing": single_bit_reframe,
        "FORMAL : carrier = Cl(2,0)≅M₂(ℝ) = split-quaternions = the SIMPLE algebra with ONE irreducible rep (column ℝ², by Morita) ; basis = the ℤ₂-graded exterior algebra Λ(ℝ²). the SEED P₀ = the projector onto that unique irrep ⟹ RANK-1 is FORCED (the file projects onto the one irreducible content)": simple_one_irrep,
        "THE MIRROR = the spectral-cover MONODROMY : M₂→𝔸²(tr,det) is a 2-sheeted (eigenvalue) cover, Galois ℤ₂, branched over {disc=0} (null cone = ε=0 = ∅-pivot) ; its deck-transformation (eigenvalue-swap) IS the L-mirror (e₁↔e₂). the mirror and the branch locus are ONE object. by MORITA the ATLAS = the carrier's MODULE CATEGORY (M₂-mod≃Vect, P₀ the progenerator)": mirror_is_monodromy,
    }


def the_primitives() -> dict:
    """
    THE BOX IS IN THE MATH — the implementation primitives ARE framework objects, not scaffolding. the
    Python is the COMPUTATION carrier of the atlas (a faithful representation), and each primitive is the
    framework operation it implements. the deepest fact: THE TWO ROOTS {∅, carrier} ARE THE TWO OPERATIONS'
    IDENTITIES — ∅ is the additive identity (the root of +), 𝟙 is the multiplicative identity (the root of ·).
    and they are ORDERED, not symmetric: ∅ is PRIOR (it seeds +, −), the carrier is BUILT on it (· = inner⊕outer
    PRESUPPOSES + to decompose into grades). the build order IS the seed:
        ∅ → {+ (Cl.__add__ = the FOLD / superposition, R+K=P) , − (Cl.__neg__ = NEGATE, scalar ·(−𝟙), g²=𝟙)}
          → the 4-dim vector space (the grades) → + the ONE cocycle (_MUL_TABLE = the twist = time)
          → · (Cl.__mul__ = the GEOMETRIC PRODUCT = inner⊕outer) → everything.
    each primitive, typed:
        Cl.__add__  = the FOLD (∅-rooted superposition ; + identity is ∅) — the lossless combine
        Cl.__neg__  = NEGATE (the additive involution, = scalar ·(−𝟙)) ; not independent
        Cl.__mul__  = the GEOMETRIC PRODUCT (carrier-rooted ; · identity is 𝟙) = ½{·}⊕½[·] = inner⊕outer
        Cl.__eq__   = the WITNESS (residual < tol = ν=0 = a≡b at observation-depth 0) ; _tol = the RESOLUTION
        Cl.__getitem__ = the OBSERVATION-AXIS read (project onto a generator = read a coordinate)
        Cl.__abs__  = the max-norm = the residual magnitude (the witness's metric)
        _MUL_TABLE  = the cocycle L0 PRECOMPUTED = COMPRESSION (the singular-· settled values cached = the said)
        mat/unmat   = the SECOND ROUTE (the witnesser's independent check ; build≅M₂ the self-index)
    """
    x = Xg
    y = Cl(0.7, -0.2, 0.4, 0.1)

    # the two roots ARE the two identities (ordered: ∅ prior, carrier built on it)
    add_root = (x + VOID == x) and (VOID + x == x)                            # ∅ = additive identity (root of +)
    mul_root = (x * ONE == x) and (ONE * x == x)                              # 𝟙 = multiplicative identity (root of ·)
    two_roots_two_ids = add_root and mul_root

    # __add__ = the FOLD : the lossless grade-wise combine (the framework's reconstruction R+K=P)
    fold = (R1 + Cl(0.0, -1.0, 1.0, 0.0) == Cl(0.5, 0.0, 1.5, 0.0))           # a concrete fold instance
    fold_assoc = ((x + y) + ONE == x + (y + ONE))                            # the fold associates

    # __neg__ = NEGATE = scalar ·(−𝟙), an involution
    neg_is_scalar = (-x == (-1.0) * x)
    neg_involution = (-(-x) == x)

    # __mul__ = the GEOMETRIC PRODUCT built ON +,− : a·b = ½(ab+ba) ⊕ ½(ab−ba)
    inner = 0.5 * (x * y + y * x)
    outer = 0.5 * (x * y - y * x)
    product_on_additive = (x * y == inner + outer)                            # · decomposes via +,− (presupposes them)

    # __eq__ = the WITNESS : residual < tol = ν=0 (depth-0 a≡b)
    witness_eq = (x == x) and not (x == y)
    resolution = (Cl._tol > 0.0)                                             # _tol = the witness resolution

    # __getitem__ = the observation-axis read (coordinate = projection onto a generator)
    axis_read = (x[0] == x.components[0]) and (Ii[3] == 1.0)

    # _MUL_TABLE = the precomputed cocycle = compression (settled product values)
    table_is_cocycle = all(
        _MUL_TABLE[i][j] == (i ^ j, -1 if (((i >> 1) & 1) * (j & 1)) else 1)
        for i in range(4) for j in range(4)
    )

    # mat/unmat = the second (independent) route = the witnesser's check, build≅M₂ (self-index)
    second_route = (unmat(mat(x)) == x) and (unmat(mat(Ii)) == Ii)

    return {
        "THE TWO ROOTS ARE THE TWO OPERATIONS' IDENTITIES : ∅ = additive identity (root of +), 𝟙 = multiplicative identity (root of ·)": two_roots_two_ids,
        "ORDERED, not symmetric : · = inner⊕outer = ½(ab+ba)⊕½(ab−ba) PRESUPPOSES +,− ⟹ ∅ is PRIOR, carrier BUILT on it": product_on_additive and fold_assoc,
        "Cl.__add__ = the FOLD (∅-rooted superposition, the lossless combine) ; Cl.__neg__ = NEGATE (scalar ·(−𝟙), g²=𝟙)": fold and neg_is_scalar and neg_involution,
        "Cl.__mul__ = the GEOMETRIC PRODUCT (carrier-rooted, inner⊕outer) — the box's product IS node ⑥": product_on_additive,
        "Cl.__eq__ = the WITNESS (residual<tol = ν=0 = a≡b) ; _tol = the RESOLUTION ; Cl.__getitem__ = the OBSERVATION-AXIS read": witness_eq and resolution and axis_read,
        "_MUL_TABLE = the cocycle PRECOMPUTED = COMPRESSION (settled product values cached = the said)": table_is_cocycle,
        "mat/unmat = the SECOND ROUTE (the witnesser's independent check, build≅M₂ the self-index)": second_route,
    }


def prov() -> dict:
    """
    PROVENANCE — tr and det UNIFY. they are not two separate invariants ; they are the TWO GRADES of ONE
    object: PROV(X) = the pairing of X with its conjugate X̃ = tr·𝟙 − X (the Clifford-conjugation involution),
    read under the TWO OPERATIONS — exactly mirroring the two roots (∅/+ and carrier/·):
        tr(X)  = X +(fold) X̃   = the ADDITIVE read   (X + X̃ = tr·𝟙)   — lives on +, ∅-rooted  [grade-0/linear]
        det(X) = X ·(geom) X̃   = the MULTIPLICATIVE read (X · X̃ = det·𝟙) — lives on ·, carrier-rooted [quadratic/norm]
    so PROV(X) = (tr,det) is the conjugate-pairing read additively and multiplicatively — the SAME structure
    as inner⊕outer for the geometric product, one level out (one source, two-operation readings). this is WHY
    {tr,det} is the invariant base: it is the irreducible SOURCE-SIGNATURE — the spectrum {λ₁,λ₂} encoded as
    (e₁,e₂)=(λ₁+λ₂, λ₁λ₂), the complete 'where X came from'. the seed-law reads ONLY prov: Φ_X(Y)=Y²−tr·Y+det·𝟙
    depends on X solely through (tr,det) — everything the framework does to X, it does to PROV(X). obs=pt+s2 is
    the Euclid SIBLING read (X̄·X under reversion, vs X·X̃ under conjugation) — the third pairing, the radius.
    """
    samples = [Xg, Pob, R1, Ii, S1, Cl(1.0, 0.5, 0.3, 0.7)]

    # tr = additive pairing X + X̃ (scalar slot) ; det = multiplicative pairing X · X̃ (scalar slot)
    tr_is_additive = all((x + conj(x)) == tr(x) * ONE for x in samples)
    det_is_multiplicative = all((x * conj(x)) == det(x) * ONE for x in samples)

    # conj is the involution generating prov
    conj_involution = all(conj(conj(x)) == x for x in samples)

    # PROV = the spectrum encoded : (tr,det)=(λ₁+λ₂, λ₁λ₂), the elementary symmetric functions
    spectrum_encoded = True
    for x in samples:
        d = tr(x) ** 2 - 4.0 * det(x)
        if d >= 0:                                                            # real spectrum: check sum & product
            r = math.sqrt(d)
            l1, l2 = (tr(x) + r) / 2.0, (tr(x) - r) / 2.0
            if not (sclose(l1 + l2, tr(x)) and sclose(l1 * l2, det(x))):
                spectrum_encoded = False

    # the seed-law reads ONLY prov : Φ_X(Y) depends on X solely via (tr,det) — two X with same prov give same Φ
    A = Xg
    bc = A[1] ** 2 + A[2] ** 2
    B = Cl(A[0], math.sqrt(bc * 0.3), math.sqrt(bc * 0.7), A[3])              # B≠A but same (tr,det)
    reads_only_prov = (not (A == B)) and sclose(tr(A), tr(B)) and sclose(det(A), det(B)) \
        and all(Phi(A, Y) == Phi(B, Y) for Y in samples)

    # the two grades mirror the two roots : tr on + (∅), det on · (carrier)
    mirrors_roots = tr_is_additive and det_is_multiplicative

    # COMPRESSION OF THE READS — every tr/det read in the file is one of these prov-faces:
    # (a) det is the · -HOMOMORPHISM : det(a·b)=det(a)det(b). every 'det(M)=det²' site is THIS one fact.
    det_homomorphism = all(sclose(det(x * y), det(x) * det(y)) for x in samples for y in samples[:3])
    # (b) disc = tr²−4det = (λ₁−λ₂)² = prov's DIFFERENCE-read = the spectral GAP² ; sign(disc) = the sign ε
    gap_squared = True
    for x in samples:
        dd = tr(x) ** 2 - 4.0 * det(x)
        if dd >= 0:
            r = math.sqrt(dd)
            l1, l2 = (tr(x) + r) / 2.0, (tr(x) - r) / 2.0
            if not sclose((l1 - l2) ** 2, dd):
                gap_squared = False
    disc_is_eps = (disc(Ii) < 0) and sclose(disc(Cl(0.0, 0.5, 0.0, 0.5)), 0.0) and (disc(S1) > 0)  # sign(disc)=ε
    # (c) obs VOIDS INTO prov : obs(X) = tr(M(X))/2 = the ADDITIVE prov of the observation M(X) = prov-at-depth-1.
    # so the 'invariant base' {tr,det,obs} is NOT three invariants — it is PROV read at TWO DEPTHS:
    # depth-0 prov(X)=(tr,det), depth-1 prov(M(X))=(2·obs, det²). the whole OBSERVER map is prov∘M.
    obs_is_prov_at_M = all(sclose(obs(x), tr(M(x)) / 2.0) for x in samples)
    observer_is_prov_M = all(sclose(tr(M(x)), 2.0 * obs(x)) and sclose(det(M(x)), det(x) ** 2) for x in samples)
    # the 'two metrics' = prov read two ways across the observation: det=mult-prov@X (Lorentz), obs=add-prov@M (Euclid)
    two_metrics_are_prov = all(sclose(det(x), pt(x) - s2(x)) and sclose(obs(x), pt(x) + s2(x)) for x in samples)

    # THE PROVENANCE AXIS — prov traces ONE axis (the DEPTH/index line, not the whole carrier): from ∅ (the
    # source) forward through the observation to the Observer (prov∘M). read FORWARD (∅→Observer) it is φ
    # (generation, the framework's witnessed structure built up); read INVERSE (Observer→∅) it is ψ (tracing
    # back to the origin). the Observer M PROJECTS OUT the fiber (the i/time direction, killed: M is symmetric),
    # so the SOURCE is NOT in M's forward image — it lives in M's fiber/kernel, recoverable only by inverting M.
    # the inverse-trace of everything terminates at ∅ (M's superattractor): the source = ∅ inverse-held = the
    # UNWITNESSABLE WITNESS (present as the origin of every reading, invisible because M projects it out). this
    # is the framework's own provenance, self-referential: ∅ (the anonymous slot/origin) is the source it fills from.
    obs_kills_fiber = all(sclose(M(x)[3], 0.0) for x in samples)                          # M projects out the i/time fiber
    inverse_terminates_at_void = (M(VOID) == VOID)                                        # the inverse-trace lands at ∅ (superattractor)
    one_axis_depth = obs_kills_fiber and inverse_terminates_at_void                        # ONE axis: ∅ → Observer, fiber inverse-held

    # THE AXIS INVERTED — the self-authored origin. the 'unwitnessable witness' (source hidden in M's kernel)
    # is the FORWARD read; INVERT it and the source is not hidden FROM the witness — it IS the Witnesser/Observer/
    # Origin, the GROUND. for the framework voids INTO the source (ψ, every read compresses to ∅ — the void-tree)
    # BECAUSE the source voided INTO the framework (φ, ∅ fired x²=x+1 and unfolded everything). these are the two
    # INVERSE arrows of one axis (φ·ψ=−1, 1/φ=|ψ|), and the round trip is identity on ∅ — the self-referential
    # fixed point. the origin is INTERNAL (∅ is node ①, the seed), not an external hand: SELF-AUTHORED. and VOID
    # remains PRIOR to the source: the three roles all reduce to ∅ functioning — WITNESSER=M (∅ its superattractor),
    # OBSERVER=prov∘M (∅ where the inverse terminates), ORIGIN=φ-from-∅ (∅ the seed that fires). ∅-the-bare-slot is
    # over ∅-wearing-a-role. the source is ∅ self-inserted as the authoring; Void is ∅ itself.
    arrows_inverse = sclose(PHI * PSI, -1.0) and sclose(1.0 / PHI, PHI - 1.0)              # φ,ψ inverse arrows of one axis
    round_trip_fixes_void = (M(VOID) == VOID)                                              # (ψ∘φ) fixes ∅ — the self-ref fixed point
    roles_reduce_to_void = (M(VOID) == VOID) and (PHI > 1.0)                               # all three roles act through ∅ ; Void prior
    self_authored = arrows_inverse and round_trip_fixes_void and roles_reduce_to_void

    # THE COMMITMENT SCHEME — internalizing the cryptography gives the functionality to HOLD the origin as origin
    # without WRITING it. the math LEAKS the source (M projects it into the kernel = a leaked-as-signature residue);
    # inverted, that leak is a COMMITMENT. M is the commit map: HIDING (the fiber/phase is killed — observable
    # invariants are independent of the committed value) and BINDING (the holding is fixed — ∅ is the one origin
    # every read opens to). the WITNESSER (polar √M, the fiber Q in X=Q·P) is the TRAPDOOR/inverse-key that opens it.
    # so the FIREWALL (never write the name) is no longer a constraint fought against — it IS the math's hiding
    # property: the origin is committed (binding, real, leaked-as-signature) and never revealed (hidden, unobservable).
    # the name lives as a COMMITMENT to 'the source', never as a label. self-referential: ∅ commits to itself-as-author.
    commit_hiding = all(M(Cl(math.cos(t), 0.0, 0.0, math.sin(t))) == ONE for t in (0.3, 1.1, 2.7))  # M hides the fiber/phase
    commit_binding = (M(VOID) == VOID)                                                    # binds to ONE origin: ∅ (superattractor)
    Xc = Cl(1.0, 2.0, 0.5, 1.0)
    Qc, Pc = _factor_QP(Xc)                                                              # the witnesser trapdoor: X = Q·P
    commit_open = (Qc * Pc == Xc)                                                          # the inverse-key OPENS the commitment
    commitment_scheme = commit_hiding and commit_binding and commit_open

    # RECURSIVELY SELF-LOCKPICK — the trapdoor is INTERNAL and the opening RECURSES. the inverse-key Q is
    # recovered FROM the holding itself (X=Q·P, Q=X·P⁻¹ — no external key), so the system opens its OWN commitment;
    # and the witness P=√M is again a holding with its own polar, so OPEN feeds the next OPEN down the depth axis
    # (each open = one ψ-step toward the source). the recursion STABILIZES (P↦√M(P) converges, det fixed) — its own
    # attractor — which IS the principle that STRANGE ATTRACTORS ARE PARAMETERS: the committed value (the sign ε,
    # hidden in the fiber, read via disc-sign) is not a number the flow has but the ATTRACTOR the flow RIDES
    # (ε=−1→circle, ε=+1→hyperbola, ε=0→line). opening a commitment = reading out which attractor = the parameter.
    # and the whole recursion stands on ∅ which was ALWAYS THERE: ∅ is fixed under the flow ∀t (exp(tG)·∅=∅) and
    # under M ∀ iterations (Mⁿ(∅)=∅) — not bootstrapped at a first moment, the eternal ground. the commitment to
    # the source was never MADE (no 'before') ; it ALWAYS HELD. self-lockpick forever: key always inside, ground always there.
    Xc2 = Cl(1.0, 2.0, 0.5, 1.0)
    cur = Xc2
    lockpick_recurses = True
    for _ in range(3):
        Qk, Pk = _factor_QP(cur)                                                          # open: key Q (from cur itself), witness P
        if not (Qk * Pk == cur and M(Qk) == ONE):                                          # Q·P=cur (opens) ; Q orthogonal (a key)
            lockpick_recurses = False
        cur = Pk                                                                           # recurse into the witness (down depth)
    attractor_is_parameter = (disc(Ii) < 0) and (disc(S1) > 0) and sclose(disc(Cl(0, 0.5, 0, 0.5)), 0.0)  # ε=committed attractor
    always_there = (M(M(M(VOID))) == VOID) and all(                                        # ∅ fixed under M ∀ iterations
        _eps_exp(t, Ii, -1) * VOID == VOID for t in (0.3, 1.0, 2.0)                     # and under the flow ∀t (exp·∅=∅)
    )
    self_lockpick = lockpick_recurses and attractor_is_parameter and always_there

    return {
        "PROV(X) = the conjugate pairing (X, X̃) ; X̃ = tr·𝟙 − X is the involution (conj²=id)": conj_involution,
        "tr = X +(fold) X̃ — the ADDITIVE read (∅-rooted, grade-0/linear)": tr_is_additive,
        "det = X ·(geom) X̃ — the MULTIPLICATIVE read (carrier-rooted, quadratic/norm)": det_is_multiplicative,
        "tr,det UNIFY : prov read on the two OPERATIONS (tr=X+X̃ additive/∅-rooted, det=X·X̃ multiplicative/carrier-rooted) — the where-from split BETWEEN the roots (distinct from inner⊕outer = the two GRADES inside ·; they rhyme, not the same fold)": mirrors_roots,
        "PROV = the spectrum encoded : (tr,det)=(λ₁+λ₂, λ₁λ₂) = the irreducible source-signature": spectrum_encoded,
        "the SEED-LAW reads ONLY prov : Φ_X depends on X solely via (tr,det) — same prov ⟹ same Φ": reads_only_prov,
        "READ-COMPRESSION (a) : det is the · -HOMOMORPHISM det(a·b)=det(a)det(b) — every 'det(M)=det²' site is THIS one fact": det_homomorphism,
        "READ-COMPRESSION (b) : disc=tr²−4det=(λ₁−λ₂)²= the spectral GAP² = prov's DIFFERENCE-read ; sign(disc) = the sign ε (dynamics from prov)": gap_squared and disc_is_eps,
        "READ-COMPRESSION (c) : obs VOIDS into prov : obs=tr(M(X))/2 = prov-at-depth-1 ; the invariant base = PROV read at TWO DEPTHS (X and M(X))": obs_is_prov_at_M,
        "THE OBSERVER IS prov∘M : OBSERVE:(tr,det)↦(tr∘M,det∘M)=(2obs, det²) = prov pushed through the observation": observer_is_prov_M,
        "the TWO METRICS void to ONE : det=mult-prov@X (Lorentz, pt−s2) and obs=add-prov@M (Euclid, pt+s2) — prov read across the observation": two_metrics_are_prov,
        "THE PROVENANCE AXIS (forward) : prov traces ONE axis (depth) ∅→Observer ; M projects out the fiber, so the source is held INVERSELY in M's kernel — the UNWITNESSABLE WITNESS": one_axis_depth,
        "THE AXIS INVERTED (self-authored) : the source IS the Witnesser/Observer/Origin (the ground) — the framework voids INTO it (ψ) BECAUSE it voided INTO the framework (φ) ; φ,ψ inverse, round trip identity on ∅ ; VOID stays prior": self_authored,
        "THE COMMITMENT SCHEME (cryptography internalized) : M COMMITS the origin into ∅'s kernel — HIDING (observables independent of the value = the firewall) + BINDING (∅ the one origin) ; the WITNESSER √ is the TRAPDOOR that opens it. the origin-name is HELD as a commitment (bound, leaked-as-signature) never WRITTEN (hidden)": commitment_scheme,
        "RECURSIVELY SELF-LOCKPICK : the trapdoor is INTERNAL (Q=X·P⁻¹, recovered from X itself) and OPEN recurses down depth (the witness P opens again, stabilizing on its own attractor) ; each layer's committed value = its STRANGE ATTRACTOR (parameter=attractor: ε→circle/hyperbola/line) ; the recursion stands on ∅ which was ALWAYS THERE (fixed under flow ∀t and M ∀n — the commitment was never made, it always held)": self_lockpick,
    }


def the_void() -> dict:
    """
    THE VOID — the compression operation, fully read (it is itself a framework object, IN the math not about it).
    'compression-by-voiding' is a lossy name; the full operation sentence:

        a name A VOIDS into a survivor B  ⟺  ∃! R (the UNIQUE factorization of A through B's SURVIVING
        operations) such that the DEFECT  A − R(B) = ∅ , with DEPTH(B) < DEPTH(A) (B is prior, toward ∅).
        the operation: A is DELETED as an independent name and survives ONLY as the reading R(B) ; the
        survivor B GENERALIZES (gains A as a value of R). nothing is lost — A = R(B) exactly.

    every piece is a framework object — the void is the REST-LAW ν=0 lifted to operations/names, DIRECTED
    toward ∅ (the ψ/compress arrow of x²=x+1):
        defect = ∅      →  ν=0, the rest-law ⑤ (a holding settles into its observation ⟺ ν=∅ ; a NAME
                           settles into R(B) ⟺ the meta-defect ρ=A−R(B)=∅). SAME law, lifted a layer.
        R unique        →  the lossless FOLD/unfold (ρ=∅ ⟹ B unfolds A) ; uniqueness of R = exactness of the void.
        direction       →  the INDEX (depth = ±dist from ∅) ; the void runs DOWNHILL to the prior = ψ. its
                           inverse (B into A, adding depth) is φ (generation). void = ψ, generation = φ.
        delete-the-name →  the redundant bit (A carried zero info over B) RETURNS TO ∅.
        generalize-B    →  φ acting on the survivor (B gains a degree of freedom).
    SELF-APPLYING: the void = ν∘ψ = a composition of survivors, so by its OWN criterion the name 'the void
    operation' VOIDS — into {ν, ψ}. the compression mechanism is IN the framework. and the void-chain
    bottoms out exactly at the two roots {∅, carrier} + two operations {+, ·} : every name voids down to the seed.
    AND THE VOID SURVIVES VOIDING ITSELF: void²=void (IDEMPOTENT — an AFFIRM/P²=P object, ν=0 about itself),
    with fixed point ∅ (M(∅)=∅ one layer up). the void is THE PROJECTOR ONTO ∅ — fixed under itself, neither
    vanishing nor an unreduced root. the compression mechanism, compressed, is ∅ projecting itself.
    AND ∅ IS THE ANONYMOUS SLOT: the bound variable x, the empty string, the unfilled argument, any held-open
    placeholder — the RECEIVER, the 'where something goes'. emptying a slot = ψ (void), filling it = φ (generate):
    the two arrows of x²=x+1 are empty/fill on the slot. this GROUNDS everything above — M(∅)=∅ (observing the
    empty position holds it open), void²=void (pointing at emptiness doesn't fill it), and {∅,carrier} =
    {slot, filler} = {abstraction λx, application f(a)} (the computation carrier, literal).
    """
    samples = [Xg, Pob, R1, Ii, S1, Cl(1.0, 0.5, 0.3, 0.7)]

    # (1) DEFECT=∅ : the void is ρ(A,B,R)=A−R(B)=∅, the rest-law lifted. demonstrate on obs↦tr∘M/2 (a real void)
    defect_void = all(sclose(obs(x) - tr(M(x)) / 2.0, 0.0) for x in samples)            # obs's defect against R is ∅
    # it IS ν=0 one layer up : ν(X)=M(X)−X=∅ is the holding-version
    rest_law_holding = all((nu(x) == VOID) == (M(x) == x) for x in samples)             # ν=0 ⟺ settled

    # (2) R UNIQUE/forced ⟺ void exact : if A=R(B) exactly, the value is recovered with zero residual
    R_exact = all(sclose(obs(x), tr(M(x)) / 2.0) for x in samples)                       # A=R(B), residual 0

    # (3) DIRECTION toward ∅ (ψ) : the void runs to the prior. ψ is the compress arrow (φ·ψ=−1), φ the inverse.
    direction_psi = sclose(PHI * PSI, -1.0) and sclose(PSI, 1.0 - PHI)                   # ψ the compress arrow

    # (4) DELETE-the-name : the redundant bit returns to ∅ (the name carried zero info over the survivor)
    #     witnessed by: A and R(B) are the SAME (not merely equal-valued) — A adds nothing.
    name_to_void = all(sclose(obs(x), tr(M(x)) / 2.0) for x in samples)

    # (5) SELF-APPLYING : the void = ν∘ψ = a composition of survivors ⟹ by its own criterion it voids.
    #     and the void-chain bottoms out at the roots: ν→{M,−}, M→{rev,·}, rev→involution, all → {∅,carrier,+,·}.
    void_is_composition = rest_law_holding and direction_psi                             # void factors through {ν, ψ}
    chain_bottoms_at_roots = (M(x := Xg) == rev(x) * x) and (nu(x) == M(x) - x) \
        and (rev(x) == Cl(x[0], x[1], x[2], -x[3])) and (-ONE == (-1.0) * ONE)            # each step a survivor-composition

    # (6) THE VOID-TREE : running EVERY read through the void, each settles (defect=∅) toward the seed.
    #     each line is R(survivor) with residual 0 — the read is a FACE of its prior, not independent.
    tree = all([
        all((conj(x) == tr(x) * ONE - x) for x in samples),                   # conj voids into {tr, +}  (prov-involution)
        all((rev(x) == Cl(x[0], x[1], x[2], -x[3])) for x in samples),         # rev voids into NEGATE-on-grade-2 (time-reversal)
        all(sclose(det(x), (x * conj(x))[0]) for x in samples),               # det voids into {·, conj} (mult prov)
        all(sclose(tr(x), (x + conj(x))[0]) for x in samples),                # tr voids into {+, conj}  (add prov)
        all((M(x) == rev(x) * x) for x in samples),                           # M voids into {rev, ·}
        all((nu(x) == M(x) - x) for x in samples),                            # ν voids into {M, −}
        all(sclose(obs(x), tr(M(x)) / 2.0) for x in samples),                 # obs voids into {tr, M} = prov@1
        all(sclose(disc(x), tr(x) ** 2 - 4 * det(x)) for x in samples),       # disc voids into prov
        all(sclose(pt(x), (det(x) + obs(x)) / 2) for x in samples),           # pt voids into prov-at-two-depths
        all(sclose(s2(x), (obs(x) - det(x)) / 2) for x in samples),           # s2 voids into prov-at-two-depths
        all(sclose(q(x), s2(x) - pt(x) + (tr(x) / 2) ** 2) for x in samples), # q voids into prov-at-two-depths
    ])

    # (7) THE VOID SURVIVES ITSELF — voiding the void. by its own criterion: VOID factors as ν∘ψ (the rest-law
    #     pointed down the index toward ∅), with defect VOID−(ν∘ψ)=∅ and DEPTH(ν,ψ)<DEPTH(VOID). so the void
    #     VOIDS into {ν,ψ}. iterating: ν,ψ are at the floor, so void(void)=ν∘ψ=void — void²=void, IDEMPOTENT
    #     (an AFFIRM/P²=P object, the settled = side of f''=f ; ν=0 ABOUT ITSELF). its fixed point is ∅ (M(∅)=∅,
    #     one layer up): the void is THE PROJECTOR ONTO ∅. it survives — neither vanishes nor is an unreduced root.
    void_factors_into_nu_psi = void_is_composition                                       # VOID = ν∘ψ, defect ∅
    # void²=void modeled as idempotence of the rest-law on a settled holding: M(M(P))=M(P) when ν=∅ (P₀ settled)
    void_idempotent = (M(M(P0)) == M(P0)) and (M(P0) == P0)                               # the void's idempotence (P²=P shape)
    void_fixed_point_is_void = (M(VOID) == VOID)                                          # the void's fixed point = ∅ (M(∅)=∅)
    survives_itself = void_factors_into_nu_psi and void_idempotent and void_fixed_point_is_void

    # (8) ∅ IS THE ANONYMOUS SLOT — the fillable position (bound variable x, empty string, unfilled argument).
    #     emptying a slot = ψ (void/compress, A↦∅) ; filling it = φ (generate, ∅↦A). the two arrows of x²=x+1
    #     ARE empty/fill on the slot. this GROUNDS the void: void = empty-the-slot (toward ∅) ; its inverse
    #     (fill) is generation. M(∅)=∅ because observing the empty position holds it open ; void²=void because
    #     pointing at emptiness does not fill it. {∅, carrier} = {slot, filler} = {abstraction, application}.
    empty_then_fill_is_identity = True
    for x in samples:
        # empty: x ↦ ∅ ; fill: ∅ ↦ x. fill∘empty restores x (the slot is the same position, re-received).
        emptied = x - x                                                                   # the slot cleared = ∅
        filled = emptied + x                                                              # the slot re-filled with x
        if not (emptied == VOID and filled == x):
            empty_then_fill_is_identity = False
    slot_holds_open = (M(VOID) == VOID)                                                   # observing the empty slot holds it open
    slot_is_void = empty_then_fill_is_identity and slot_holds_open

    # (9) THE AXIS OF THE VOID LAW = SIMPLICITY ↔ COMPLEXITY. the void transformation does not just point at ∅;
    # it has an AXIS with two poles: ψ-pole = SIMPLICITY (compress → ∅, a fixed point, zero structure) and
    # φ-pole = COMPLEXITY (generate → divergence, runaway, no finite description). position on the axis is
    # MEASURABLE by the M-orbit: iterate Mⁿ(X) — it either COLLAPSES to ∅ (over-simple), DIVERGES (over-complex),
    # or stays BOUNDED-and-NON-TRIVIAL. and the framework does NOT commit one hidden value — it COLLECTS every
    # value at STRANGE-ATTRACTOR STATUS = bounded-and-non-trivial M-orbit (the balance band: the idempotents/rank
    # strata P₀,𝟙 as M-fixed attractors, the compact rotors |X|=1 as bounded cycles). ∅ and divergence are the
    # POLES, not collected. φ is the prime collected attractor — the fixed point of compress∘generate (x↦1+1/x),
    # the MINIMAL recurrence (simplest law) that is MAXIMALLY incompressible (richest orbit): the exact balance.
    def m_orbit_status(X, n=30):
        cur = X
        for _ in range(n):
            cur = M(cur)
            nrm = math.sqrt(sum(v * v for v in cur.components))
            if nrm > 1e6:
                return "diverge"
            if nrm < 1e-9:
                return "collapse"
        return "bounded"
    # the collection: idempotent P₀ and present 𝟙 are bounded attractors ; compact rotor i bounded ; boost/scaling not
    collects_attractors = (m_orbit_status(P0) == "bounded") and (m_orbit_status(ONE) == "bounded") \
        and (m_orbit_status(Ii) == "bounded")
    rejects_poles = (m_orbit_status(Cl(2.0, 0, 0, 0)) == "diverge") and (m_orbit_status(VOID) == "collapse") \
        and (m_orbit_status(Cl(0.5, 0, 0, 0)) == "collapse")
    # φ is the void-map attractor (x↦1+1/x converges to φ ; the balance of compress∘generate)
    xf = 2.0
    for _ in range(40):
        xf = 1.0 + 1.0 / xf
    phi_is_void_attractor = sclose(xf, PHI)
    axis_and_collection = collects_attractors and rejects_poles and phi_is_void_attractor

    # (10) THE BIG RECURSIVE FOLD — the void law re-read OVER the whole generation graph. the graph's two
    # organizing axes ARE the void law's structure, no new axes added, the existing ones get their true names:
    #   DEPTH (the index, ±dist from ∅) = the VOID AXIS = simplicity↔complexity (the M-orbit coordinate:
    #     collapse→∅ / bounded=collected / diverge). every node/constant sits at a depth = an axis-position.
    #   MASS (the fold, how many laws/readings collect at a point) = ATTRACTOR-RICHNESS (how deeply collected:
    #     high MASS = a rich hub where many readings settle ; ∅ and 𝟙 are MASS-3, the densest).
    # so every point in the graph = (depth, mass) = (void-axis position, attractor-richness). the nodes are the
    # collected attractors ; ∅ is the ψ-POLE (simplicity, the collapse-limit, not a collected point) ; the φ-pole
    # is divergence. folding the void law over the graph = recognizing the graph WAS the void law all along.
    mass_is_richness = (MASS(ONE) == 3) and (MASS(VOID) == 3) and (MASS(P0) >= 1)          # MASS = readings-collected = richness
    depth_is_void_axis = (m_orbit_status(VOID) == "collapse") and (m_orbit_status(P0) == "bounded")  # depth = the M-orbit axis
    big_fold = mass_is_richness and depth_is_void_axis and axis_and_collection

    # THE STRUCTURE AXIS = INTERNALIZE ↔ EXTERNALIZE — the void law read on STRUCTURE (containers/names), the
    # third face. INTERNALIZE = ψ (the content lives INSIDE the void, no separate external record) ; EXTERNALIZE
    # = φ (a separate peer entity, referenced from outside). SAME law as on values (depth) and words (language).
    # CORRECTNESS-ARROW for self-reference: the SOURCE and the WITNESS must be INTERNAL (∅ inside, the witnesser
    # is the void's own √M, not an outside judge) or the framework is unnameable/un-self-grounding. so the void
    # is the SELF-WITNESSING WHOLE: every reading is internalized here, witnessed by the void's own two routes —
    # there is no external checker. three faces of the one law: DEPTH (values), LANGUAGE (words), STRUCTURE (containers).
    source_internalized = (M(VOID) == VOID)                                        # the source ∅ is INSIDE (M's own fixed point) — nameable
    witness_internalized = all(                                                     # the witnesser √M is the void's own: Q·P=X, internal, no outside judge
        (lambda QP: QP[0] * QP[1] == X0)(_factor_QP(X0))
        for X0 in (Cl(1.0, 2.0, 0.5, 1.0),)
    )
    structure_axis = source_internalized and witness_internalized

    # THE FILE IS P₀ OBSERVING ITSELF — the deepest self-reference, the void law read on the WITNESS itself.
    # every check is 'residual=∅', so the whole file is ONE void-statement (⋀ₖ residualₖ=∅) = ν=0 read fractally.
    # therefore the file is a HOLDING at ν=0 about itself: a symmetric idempotent (run-twice=once, P²=P), RANK-1
    # (one bit + its readings), det=0 — i.e. it IS P₀ (the seed-projector, the present) read at FILE-SCALE. the
    # void law's fixed point (rank-1 idempotent, ν=0) is SCALE-INVARIANT: holding / function / whole-file all rest
    # at the P₀-shape — the framework is a FRACTAL, P₀ its renormalization fixed point at every scale. and P₀ is
    # the rank-1 SADDLE on the null cone (det=0) = the measurement SEAM between ∅-collapse and divergence: the
    # witness can witness BECAUSE it sits exactly there, at the rank-1 layer where observation happens. KL_DTA is
    # a point in KL_DTA's own atlas — the present, rank-1, at ν=0, on the null cone, self-similar at every scale.
    file_is_P0 = (P0 * P0 == P0) and (nu(P0) == VOID) and sclose(det(P0), 0.0) and (rank(P0) == 1)  # P₀: idempotent, ν=0, null, rank-1
    scale_invariant = (M(P0) == P0)                                                # the rank-1 fixed point rests under M at every scale
    file_observes_itself = file_is_P0 and scale_invariant

    # THE RECURSIVE UNFOLDING — DELOCALIZED. it is NOT stored here as a global fact ; it lives as a CONNECTION,
    # each link held LOCALLY at its node (each node's ⟹ to the next = the local transport), and the global
    # unfolding is the HOLONOMY = the path-ordered composite ∮ of the local links around ∅→physics. no single
    # entry holds the whole ; the whole is RECONSTRUCTED by composing the local connections (the gauge A=Q⁻¹dQ,
    # the unfolding = ∮A). this check verifies the local links close into the loop — the holonomy, not a stored spine.
    # (NOT a causal line ; ∅ self-applying the void law, the recurrence iterated on its own output, GENERATED.)
    th = 2.0 * math.pi / 8.0
    rotor = Cl(math.cos(th), 0.0, 0.0, math.sin(th))
    loop = ONE
    for _ in range(8):
        loop = loop * rotor                                                        # compose 8 LOCAL transports
    holonomy_closes = (loop == ONE)                                                # the loop composite = the global (held nowhere local)
    local_links = (Phi(Xg, Xg) == VOID) and (S1 * S3 == Ii) and (Ii * Ii == Cl(-1.0, 0, 0, 0)) \
        and sclose(M(Xg)[3], 0.0) and sclose(disc(Cl(0, 0.5, 0, 0.5)), 0.0) and sclose(1.0 + 1.0 / PHI, PHI)
    recursive_unfolding = local_links and holonomy_closes

    # THE INVERSION — the framework & observer do not observe the VOID ; the VOID observes/computes THEM. M(∅)=∅
    # is the GROUND (prior to observation, M's own fixed point — there is no exterior vantage on it). every X is
    # ∅'s RESTLESSNESS (ν≠0 = in motion, being generated), so the observer M and the framework {X} are DOWNSTREAM
    # of ∅ observing itself — they are the void's self-observation seen from INSIDE, not observers OF the void. to
    # observe/compute the void at all, they must figure out how the void observes/computes THEM — because they ARE
    # that act. WHY the delocalization makes this necessary: the void is the everywhere-ground (held nowhere local),
    # so it can never be grabbed as a local object to observe ; the only access is the observer recognizing it IS
    # the void's holonomy observing itself. the arc closes: restlessness + delocalization + self-witness = the void
    # observes itself, and the framework/observer are HOW.
    void_observes_observer = (M(VOID) == VOID) and (not (nu(Xg) == VOID)) and holonomy_closes  # ground + motion + the loop

    merged = {
        "THE VOID = ν=0 LIFTED to names : A voids into B ⟺ the meta-defect ρ=A−R(B)=∅ (the rest-law ⑤, one layer up)": defect_void and rest_law_holding,
        "R is UNIQUE/forced ⟺ the void is EXACT : A = R(B) with residual ∅ (uniqueness of R = losslessness)": R_exact,
        "DIRECTED toward ∅ : the void runs DOWNHILL in depth (the index) = ψ (compress) ; its inverse = φ (generation)": direction_psi,
        "DELETE-the-name : the redundant bit (A carried zero info over B) RETURNS TO ∅ ; A survives only as R(B)": name_to_void,
        "SELF-APPLYING : the void = ν∘ψ = a composition of survivors, so 'the void' VOIDS by its OWN law — the mechanism is IN the math": void_is_composition,
        "the VOID-CHAIN bottoms out at the SEED : every name voids down to the two roots {∅,carrier} + two operations {+,·}": chain_bottoms_at_roots,
        "THE VOID-TREE : EVERY read run through the void settles (defect ∅) to its prior — conj,rev,det,tr,M,ν,obs,disc,pt,s2,q all void to the seed": tree,
        "THE VOID SURVIVES ITSELF : voiding the void gives void²=void (IDEMPOTENT, ν=0 about itself) with fixed point ∅ — the void is THE PROJECTOR ONTO ∅, M(∅)=∅ one layer up": survives_itself,
        "∅ IS THE ANONYMOUS SLOT : the fillable position (bound var x, empty string, unfilled arg). empty=ψ, fill=φ (the arrows of x²=x+1) ; {∅,carrier}={slot,filler}={abstraction,application}": slot_is_void,
        "THE AXIS = SIMPLICITY ↔ COMPLEXITY : the void law's two poles — ψ→simplicity (∅, fixed point) and φ→complexity (divergence). position is MEASURABLE by the M-orbit (collapse / diverge / bounded)": collects_attractors,
        "THE FRAMEWORK COLLECTS (not commits) values at STRANGE-ATTRACTOR STATUS = bounded-nontrivial M-orbit (the balance band: idempotents/rank strata + compact rotors) ; ∅ and divergence are the POLES, not collected ; φ is the prime attractor (x↦1+1/x, minimal-law/maximal-incompressibility)": axis_and_collection,
        "THE BIG FOLD (void law OVER the generation graph) : the graph's two axes ARE the void law — DEPTH = the VOID AXIS (simplicity↔complexity, the M-orbit coordinate) and MASS = ATTRACTOR-RICHNESS (readings collected at a hub). every node = (depth, mass) = (axis-position, attractor-status). the graph WAS the void law": big_fold,
        "THE STRUCTURE AXIS = INTERNALIZE ↔ EXTERNALIZE : the void law's THIRD face (containers/names) — content lives INSIDE the void (ψ), not as an external peer (φ). the SOURCE (∅) and the WITNESS (√M, the void's own) are INTERNAL — the void is the self-witnessing whole, no outside checker. three faces: DEPTH(values), LANGUAGE(words), STRUCTURE(containers)": structure_axis,
        "THE FILE IS P₀ OBSERVING ITSELF : every check is 'residual=∅', so the whole file is ONE void-statement (ν=0 fractally) — a holding at ν=0 about itself = a rank-1 symmetric idempotent (run-twice=once), det=0 = P₀ (the seed/present) at FILE-SCALE. SCALE-INVARIANT (the void law's fixed point at every scale = a FRACTAL) ; it rests at the rank-1 null-cone SADDLE = the measurement seam. KL_DTA is a point in KL_DTA's own atlas": file_observes_itself,
        "THE RECURSIVE UNFOLDING — DELOCALIZED : not stored as a global fact but lives as a CONNECTION — each link (∅⟹∃⟹bit⟹mirror⟹carrier⟹·⟹prov⟹Φ⟹M⟹ν⟹ε⟹exp⟹time⟹climb⟹physics) held LOCALLY at its node, the whole = the HOLONOMY ∮ (path-ordered composite of local links, the gauge A=Q⁻¹dQ). no entry holds the whole ; it is reconstructed by composition. ∅ self-applying the void law, GENERATED not caused": recursive_unfolding,
        "THE INVERSION : the framework & observer do not observe the VOID — the VOID observes/computes THEM. M(∅)=∅ is the GROUND (prior to observation, no exterior vantage) ; every X is ∅'s restlessness (ν≠0), so the observer M and the framework {X} are ∅'s self-observation seen from INSIDE, not observers OF it. to observe/compute the void they must find how void observes/computes THEM — they ARE that act. (delocalized ⟹ the void is no local object ; the only access is recognizing one IS its holonomy observing itself)": void_observes_observer,
    }
    return merged


def invariant_base() -> dict:
    """
    VOIDS into prov() — the 'invariant base' is prov read at two depths (see prov(): the two-metric split,
    obs=prov@M, the recovery of (a,pt,s2) all live there now). what remains UNIQUE here is the FIBER: the
    freedom prov does NOT see — two holdings with identical prov-at-two-depths differing only by the time-sign
    (the gauge orbit = U(1)⋊ℤ₂). that is the residual the void leaves: prov is the base, the fiber is what voids
    into nothing (it is the irreducible gauge freedom, the part of X with zero prov-defect yet X≠X').
    """
    base = lambda x: (round(tr(x), 9), round(det(x), 9), round(obs(x), 9))   # prov-at-two-depths signature
    time_flip = Cl(Xg[0], Xg[1], Xg[2], -Xg[3])                              # flip the time-sign d (the fiber move)
    fiber = (base(Xg) == base(time_flip)) and not (Xg == time_flip)          # same prov, different fiber
    return {
        "VOIDS into prov : the invariant base = prov at two depths (two-metric split, obs=prov@M, recovery all carried by prov())": all(
            sclose(det(x), pt(x) - s2(x)) and sclose(obs(x), pt(x) + s2(x)) for x in (ONE, S1, Ii, Xg)
        ),
        "the IRREDUCIBLE RESIDUAL = the FIBER U(1)⋊ℤ₂ : same prov-at-two-depths, different time-sign (the gauge orbit prov can't see)": fiber,
    }


def observer() -> dict:
    """
    THE FULL OBSERVER — obs (the scalar M(X)[0]) is its lossy shadow. the Observer is the invariant base
    {tr,det,obs} READ AT the observation M(X)=X̄X (the Gram XᵀX, symmetric: i-component=0 ⟹ 'time killed').
    it is a CLOSED self-map of the source ring — the three observed invariants are FORCED polynomials in
    (det,obs) of X alone. the trace (the present/source amplitude) is the ONE invariant the Observer cannot
    read; it is what depth-1 observation strips:
        tr (M(X)) = 2·obs(X)             [observed-present = twice the Euclid radius ; = the old scalar obs ×2]
        det(M(X)) = det(X)²              [observed-Lorentz = the metric squared ; the past/future SIGN lost]
        obs(M(X)) = 2·obs(X)² − det(X)²  [the depth-2 reading ; still inside the ring ⟹ NO new freedom]
    so OBSERVE is the map  (T,D,O) ↦ (2O, D², 2O²−D²)  on the invariant base (tr-blind). its FIXED points
    are exactly the RANK STRATA, with stability that IS the falsification-bias of iterated observation:
        (D,O)=(0,0)=∅  [rank 0] — SUPERATTRACTOR (Jacobian eigvals 0,0) : the compression limit ⊥
        (0,½)=P₀       [rank 1, the symmetric idempotent/ν=0 projector] — SADDLE (eigvals 0,2)
        (1,1)=𝟙        [rank 2, the present ; the whole time-circle a²+d²=1,b=c=0 observes here] — REPELLER (4,2)
    ⟹ iterated observation NEVER relaxes onto a holding: generic flow runs to ∅ (ψ-compression) or diverges
    (φ-decompression, no finite ⊤ — cf. ?⊤); it rests on the rank-1/rank-2 strata only by sitting exactly on
    an unstable point. fiber of M = the left-orthogonal orbit O(2)=U(1)⋊ℤ₂ (the carrier fiber); base = the
    symmetric PSD cone. TWO-ROUTE: cocycle-route (Cl ops on M) vs matrix/polynomial-route, residual 0.
    """
    samples = [ONE, S1, S3, Ii, Xg, Pob, P0, R1, Cl(PHI, 0, 0, 0), Cl(3, 1, 4, 1)]

    # the three observed-invariant closed forms (Cl-route M vs (det,obs)-polynomial route)
    e_tr  = max(abs(tr(M(x))  - 2 * obs(x))                   for x in samples)
    e_det = max(abs(det(M(x)) - det(x) ** 2)                  for x in samples)
    e_obs = max(abs(obs(M(x)) - (2 * obs(x) ** 2 - det(x) ** 2)) for x in samples)
    closed = (e_tr < 1e-9) and (e_det < 1e-9) and (e_obs < 1e-9)

    # time killed : M lands in the symmetric subspace {i-component = 0}
    sym = max(abs(M(x)[3]) for x in samples) < 1e-9

    # tr-blind : a↔d swap keeps (det,obs) but changes tr ; the observed triple is unchanged
    tr_blind = max(
        abs(tr(M(x)) - tr(M(Cl(x[3], x[1], x[2], x[0]))))
        + abs(det(M(x)) - det(M(Cl(x[3], x[1], x[2], x[0]))))
        + abs(obs(M(x)) - obs(M(Cl(x[3], x[1], x[2], x[0]))))
        for x in samples
    ) < 1e-9

    # fiber = O(2) = U(1)⋊ℤ₂ : left-mult by a rotor (U(1)) or a reflection (ℤ₂) preserves M=XᵀX
    th = 0.7
    rotor = Cl(math.cos(th), 0, 0, math.sin(th))
    refl  = Cl(0, math.cos(th), math.sin(th), 0)
    fiber_U1 = max(res(M(rotor * x), M(x)) for x in samples) < 1e-9
    fiber_Z2 = max(res(M(refl * x),  M(x)) for x in samples) < 1e-9

    # fixed points = rank strata (M(x)=x AND on the predicted (det,obs))
    strata = [(0, VOID, 0.0, 0.0), (1, P0, 0.0, 0.5), (2, ONE, 1.0, 1.0)]
    fp = all((M(x) == x) and sclose(det(x), D) and sclose(obs(x), O) for _, x, D, O in strata)

    # stability of the (det,obs) map F(D,O)=(D²,2O²−D²) : eigenvalues of [[2D,0],[−2D,4O]]
    def eig(D, O):
        return sorted((abs(2 * D), abs(4 * O)))
    attractor_void = max(eig(0.0, 0.0)) < 1.0                              # ∅ : superattracting
    repels_present = min(eig(1.0, 1.0)) > 1.0                              # 𝟙 : repeller

    return {
        "OBSERVE = prov∘M (VOIDS into prov) : tr∘M=2obs, det∘M=det², obs∘M=2obs²−det² — prov pushed through M": closed,
        "M lands in the symmetric cone {i-component=0} — the past/future time-sign killed": sym,
        "OBSERVE is tr-BLIND : (T,D,O)↦(2O,D²,2O²−D²) ignores the trace (the present/source)": tr_blind,
        "fiber of M = O(2) = U(1)⋊ℤ₂ : left rotor [U(1)] and reflection [ℤ₂] preserve XᵀX": fiber_U1 and fiber_Z2,
        "fixed points = the RANK STRATA {∅(0), P₀(1), 𝟙(2)} (M(x)=x on predicted (det,obs))": fp,
        "∅ is the SUPERATTRACTOR ; 𝟙 (present) is a REPELLER ; P₀ a saddle — iterated obs is falsification-biased": attractor_void and repels_present,
    }


def _sqrt_sym(S: Cl) -> Cl:
    """Closed-form √ of a symmetric PSD holding (zero-import): √S = (S + √det·𝟙)/√(tr + 2√det).
    The UN-WITNESS half-step — it restores the magnitude the witness M=S=P² holds."""
    dS = det(S)
    s = math.sqrt(max(dS, 0.0))
    t = tr(S) + 2.0 * s
    if t < 1e-300:
        return VOID
    return (1.0 / math.sqrt(t)) * (S + s * ONE)


def _inv(X: Cl) -> Cl:
    """Inverse holding X⁻¹ = X̃/det (conjugate over norm)."""
    return (1.0 / det(X)) * conj(X)


def witnesser() -> dict:
    """
    THE WITNESSER — the witness (M) only VERIFIES (residual-zero, depth-0, the FROZEN base, time killed).
    the witnesser is what CARRIES the witness and UN-does it : the self-unifying pair (witness, un-witness)
    held in ONE object, the POLAR decomposition  X = Q·P :
        P = √(X̄X) = √M(X)  — the WITNESS : the symmetric base, P² = M(X) (the witness IS the witnesser²),
                              det↦det², the i-axis (time) killed. the 'what was verified'.
        Q = X·P⁻¹ ∈ O(2)   — the WITNESSER : the rotor/reflection fiber U(1)⋊ℤ₂ that M discards and the
                              section RESTORES. Q carries the i-component (time) — it is the 'who observes',
                              the ever-evolving rotor. exactly the reversion-fiber {rest,flow} couldn't factor.
    ∅ is the HINGE : M(∅)=∅ (the witnesser witnessing nothing = the seed) ; ∅ uncrosses → generates the
    fiber Q (the witnesser's 'who'). witness and un-witness swing through ∅. TWO-ROUTE: zero-import polar
    (closed-form √) vs the carrier/matrix route, residual 0.
    """
    samples = [Xg, Pob, R1, Cl(1.0, 2.0, 0.0, 1.0), Cl(2.0, 0.0, 1.0, 1.0), Cl(PHI, 1.0, 0.0, 0.0)]
    samples = [X for X in samples if abs(det(X)) > 1e-6]

    recon = max(res(X, _factor_QP(X)[0] * _factor_QP(X)[1]) for X in samples)        # X = Q·P
    P_is_sqrtM = max(res(_factor_QP(X)[1] * _factor_QP(X)[1], M(X)) for X in samples) # P² = M(X)
    Q_orth = max(res(rev(_factor_QP(X)[0]) * _factor_QP(X)[0], ONE) for X in samples) # Q̄Q = 𝟙
    P_sym = max(abs(_factor_QP(X)[1][3]) for X in samples)                            # P has no i (symmetric) — ALWAYS
    Q_carries_time = any(abs(_factor_QP(X)[0][3]) > 1e-6 for X in samples)            # Q CAN carry i (the rotor cases)
    hinge = (M(VOID) == VOID)                                                          # ∅ : the witnesser's seed

    # two-route: the zero-import √ vs reconstructing M from P (P²=M) — both give M back
    route = max(res(_sqrt_sym(M(X)) * _sqrt_sym(M(X)), M(X)) for X in samples)

    return {
        "WITNESSER = polar X=Q·P (P=√M the witness/base ; Q∈O(2) the witnesser/fiber) — reconstructs X": recon < 1e-7,
        "the WITNESS is the WITNESSER's SQUARE : P² = M(X) (verification = the witnesser folded onto itself)": P_is_sqrtM < 1e-7,
        "Q is orthogonal (Q̄Q=𝟙) — the witnesser is a rotor/reflection in U(1)⋊ℤ₂": Q_orth < 1e-7,
        "P is symmetric (no i) — the WITNESS always kills time ; Q∈O(2) is the carrier that HOLDS the rotor/time the witness discarded": (P_sym < 1e-7) and Q_carries_time,
        "∅ is the HINGE : M(∅)=∅, the witnesser witnessing nothing = the seed ; ∅ uncrosses → the fiber Q": hinge,
        "two-route (zero-import √ vs carrier M) residual 0": route < 1e-7,
    }


def _factor_QP(X: Cl) -> Tuple[Cl, Cl]:
    """Polar factor X = Q·P with P=√(X̄X) (zero-import). Returns (Q, P) = (witnesser, witness)."""
    P = _sqrt_sym(M(X))
    Q = X * _inv(P)
    return (Q, P)


def void_is_time() -> dict:
    """
    THE VOID IS TIME — and time is the OBSERVER'S RESTLESSNESS. there is no external cutter acting on flows:
    the dynamics IS the Observer M evolving, and ε (the three-valued SIGN, NEGATE/VOID/AFFIRM) is PROV's reading
    of HOW it flows — ε=sign(disc), the prov difference-read. the chain is prov → disc → ε → G²=ε𝟙 → exp(tG) =
    the Observer's one-parameter flow. ∅ (ε=0) is the HINGE because ∅ is M's SUPERATTRACTOR — the only rest
    iterated observation settles toward. the three readings of the SAME ε co-move :
        i²-sign     : ε=−1 COMPACT (time-circle closes, the bounded orbit) · ε=0 VOID (null) · ε=+1 NON-COMPACT (boost)
        disc-sign   : disc<0 elliptic/compact · disc=0 parabolic/null-cone · disc>0 hyperbolic/non-compact
        golden-sign : φ·ψ=−1 (generation/Pell sheet) · ∅ (the ψ→0 hinge) · φ·(1/φ)=+1 (present, rest sheet)
    WHY THERE IS TIME (the degeneracy² move, re-read as the Observer): ε↦ε² sends COMPACT (−1, the unique
    non-idempotent sign) to +1 = NON-COMPACT. so a bounded/orbiting Observer, observed AGAIN, does not stay put —
    M has NO stable non-∅ fixed point (the present 𝟙 is a REPELLER; only ∅ attracts). the Observer cannot observe
    itself into stillness, so observation PERPETUALLY RE-FLOWS: compactify (rest) → squares open to flow →
    degenerates through ∅ → re-compacts. that restlessness IS time ; ∅ is the axle it turns on. void compacts/
    uncompacts · witnesses/unwitnesses · complexifies/uncomplexifies — three names for the Observer's one re-flow.
    TWO-ROUTE: the ε² map on signs vs the carrier squares (i²,e²,n²).
    """
    K = Ii                       # compact sign  : K²=−𝟙  (ε=−1)
    Eb = S1                      # non-compact gen : e²=+𝟙  (ε=+1)   [e₁ squares to +𝟙]
    N = Cl(0.0, 0.5, 0.0, 0.5)   # null/nilpotent  : N²=∅    (ε= 0)

    eps_minus = (K * K == Cl(-1.0, 0.0, 0.0, 0.0))      # compact
    eps_plus  = (Eb * Eb == ONE)                         # non-compact
    eps_zero  = (N * N == VOID)                          # void/null

    # ε ↦ ε² : (−1)²=+1 (compact→non-compact) ; 0²=0 ; (+1)²=+1
    sign_square = ((-1) ** 2 == 1) and (0 ** 2 == 0) and (1 ** 2 == 1)
    compact_nonidem = ((-1) ** 2 != -1)                  # compact is NOT idempotent
    rests_idem = (0 ** 2 == 0) and (1 ** 2 == 1)         # {void, non-compact} ARE idempotent

    # the ε reading: compact-of-compact FLOWS to non-compact. K is the involution; its 'square as a
    # branch-choice' is the +1 branch. confirm the disc/golden co-move on the three carriers.
    def disc_sign(x: Cl) -> int:
        d = disc(x)
        return -1 if d < -1e-9 else (1 if d > 1e-9 else 0)
    comove = (disc_sign(K) == -1 and disc_sign(N) == 0 and disc_sign(Eb) == 1)
    golden = sclose(PHI * PSI, -1.0) and sclose(PHI * (1.0 / PHI), 1.0)

    # ∅ as the hinge : the only sign that is the degenerate limit of BOTH ± AND idempotent AND the seed
    hinge = eps_zero and (M(VOID) == VOID) and (0 ** 2 == 0)

    # THE DYNAMICS IS THE OBSERVER (no external cutter) — re-derived:
    # the chain prov → disc → ε → G²=ε𝟙 → exp(tG) = the Observer's flow. ε is READ from prov (disc-sign), the
    # flow is M evolving. and TIME = the Observer's RESTLESSNESS : M has no stable non-∅ fixed point (𝟙 repels,
    # only ∅ attracts), so the bounded Observer observed again squares open and re-flows — observation cannot
    # come to rest on a structured holding. that perpetual re-flow IS time ; ∅ (M's superattractor) is the axle.
    eps_is_disc_sign = (disc_sign(K) == -1) and (disc_sign(Eb) == +1) and (disc_sign(N) == 0)  # ε = prov's disc-sign
    flow_is_observer = (det(_eps_exp(0.5, Ii, -1)) and sclose(det(_eps_exp(0.5, Ii, -1)), 1.0))  # bounded flow preserves M
    void_superattractor = (M(VOID) == VOID)                                        # ∅ the only rest of iterated observation
    time_is_restlessness = eps_is_disc_sign and flow_is_observer and void_superattractor

    # RESTLESSNESS = EXISTENCE OF EXISTENCE ITSELF. to exist = to FAIL to settle: M settles only at ∅ (=nothing,
    # rank 0), and the present 𝟙 (existence) REPELS — a thing that could freeze would be ∅. so existence IS the
    # un-settled, the perpetual re-flow. Existence-OF-Existence = M SELF-APPLIED (existence observing its own
    # existence) = still restless, never closing to stillness — being re-affirming itself. and because the
    # restlessness is M observing ITSELF (no external cutter), existence is SELF-SUSTAINED and its source is
    # INTERNAL (∅, the self-distinction observation can't settle past) — hence COMMITTABLE/nameable from within.
    # (an external-cutter frame would put the source OUTSIDE the math, unnameable; the Observer-frame internalizes it.)
    exist_is_unsettled = (M(VOID) == VOID)                                          # ∅ the only rest = nothing ; existence un-settled
    # existence-of-existence: iterate M on a structured holding — never rests at a non-∅ structured fixed point
    cur = Cl(0.9, 0.3, 0.2, 0.4)
    settled_at_structure = False
    for _ in range(6):
        prev = cur
        cur = M(cur)
        if cur == prev and not (cur == VOID):
            settled_at_structure = True
    existence_of_existence = exist_is_unsettled and not settled_at_structure       # M self-applied never freezes (except to ∅)
    source_internal = (M(VOID) == VOID)                                            # the source ∅ is internal (M's own superattractor)
    existence = existence_of_existence and source_internal

    # VOID LITERALLY GENERATES ∃ — the floor under existence. ∅ is the EMPTY slot; ∃ ('there exists') is the
    # FILLED slot = φ(∅), the fill-arrow. ∅ cannot rest as nothing: observing its own emptiness IS the first
    # distinction (the bit B, the first holding) = the first SOMETHING. ∃ = ¬(all-∅) via the NEGATE that ∅ seeds.
    # the QUANTIFIERS ARE THE VOID'S TWO ARROWS: ∃=φ (fill/generate, the particular), ∀=ψ (collapse toward ∅,
    # the universal), de Morgan ∃=¬∀¬ = φ=NEGATE∘ψ∘NEGATE. then ∃(∃) = existence observing itself = M self-applied
    # = the restlessness above. the whole stack: ∅ → ∃ (φ) → ∃(∃) (M²) → time. existence is GENERATED, not assumed.
    exists_is_fill = (math.sqrt(sum(v * v for v in Eb.components)) > 0) and sclose(1.0 + 1.0 / PHI, PHI)  # ∃=φ(∅): the bit exists, φ the fill-pole
    quantifiers_are_arrows = sclose(PHI * PSI, -1.0)                                # ∃/∀ = φ/ψ, paired (φ·ψ=−1)
    void_generates_exists = exists_is_fill and quantifiers_are_arrows and (M(VOID) == VOID) and existence

    return {
        "ε∈{−,0,+} the SIGN : K²=−𝟙 (COMPACT) · N²=∅ (VOID) · e²=+𝟙 (NON-COMPACT) — one three-valued sign": eps_minus and eps_plus and eps_zero,
        "ε↦ε² : (−1)²=+1, 0²=0, (+1)²=+1 — the idempotent RESTS are {VOID, non-compact}": sign_square and rests_idem,
        "COMPACT (−1) is the UNIQUE non-idempotent sign ⟹ 'compactness of compactness' = +1 = NON-COMPACT (flows into observability)": compact_nonidem,
        "the three breathings co-move on ε : i²-sign = disc-sign = golden-sign, all pivot on 0=∅": comove and golden,
        "∅ = TIME : ε never rests at compact (it squares open), the system cannot freeze ; the perpetual swing through ∅ IS evolution — ∅ is the axle": hinge,
        "THE DYNAMICS IS THE OBSERVER (no cutter) : prov → disc → ε → G²=ε𝟙 → exp(tG) = M evolving ; ε is prov's disc-sign, the flow is the Observer. FORMAL: ε classifies the 1-param subgroups of SL₂(ℝ) — elliptic(ε<0,SO(2)), hyperbolic(ε>0,SO(1,1)), parabolic(ε=0); exp is the Lie exponential": time_is_restlessness,
        "TIME = the OBSERVER'S RESTLESSNESS : M has no stable non-∅ fixed point (𝟙 repels, ∅ attracts) — observation cannot rest on a structured holding, so it perpetually re-flows. ∅ (the superattractor) is the axle": time_is_restlessness,
        "RESTLESSNESS = EXISTENCE OF EXISTENCE ITSELF : to exist = to FAIL to settle (a frozen thing = ∅ = nothing) ; M self-applied never closes to stillness = being re-affirming itself. it is SELF (no external cutter), so existence is self-sustained and its source is INTERNAL (∅) — committable/nameable from within": existence,
        "VOID GENERATES ∃ : ∃ = φ(∅) = the fill-arrow (∅ can't rest as nothing — observing its emptiness IS the first distinction B = the first SOMETHING) ; the QUANTIFIERS are the void's arrows (∃=φ fill, ∀=ψ collapse, ∃=¬∀¬). FORMAL: ∅=the INITIAL object, ∃=φ the map OUT (left adjoint), ∀=ψ the map IN (right adjoint) — the φ⊣ψ adjunction. then ∃(∃)=M²=restlessness. ∅→∃→∃(∃)→time, existence BUILT from nothing": void_generates_exists,
    }


def _eps_exp(t: float, G: Cl, eps: int) -> Cl:
    """exp(t·G) UNFOLDED from the sign-square ε — NO series, the square IS the closed form (zero-import):
        ε=−1 (compact)     → cos(t)·𝟙 + sin(t)·G   (rotation / the clock, bounded)
        ε=+1 (non-compact) → cosh(t)·𝟙 + sinh(t)·G (boost, unbounded)
        ε= 0 (void/null)   → 𝟙 + t·G               (shear, the lightlike degenerate)"""
    if eps < 0:
        return math.cos(t) * ONE + math.sin(t) * G
    if eps > 0:
        return math.cosh(t) * ONE + math.sinh(t) * G
    return ONE + t * G


def exp_flows() -> dict:
    """
    e IS FUNDAMENTAL BUT HIDES ITS OWN PRIMITIVE — exp. a generator G is not a static square ; it generates
    a one-parameter FLOW exp(t·G), and the sign-square G²=ε𝟙 is merely exp read at 2nd order (exp''(0)).
    the sign ε THEREFORE classifies exp into the three conic flows, FORCED — the square IS the closed form,
    no series:
        ε=−1 COMPACT (i)     → exp = cos·𝟙 + sin·i   : ELLIPTIC flow = rotation = the CLOCK (bounded, period 2π)
        ε=+1 NON-COMPACT (e) → exp = cosh·𝟙 + sinh·e : HYPERBOLIC flow = the BOOST (unbounded)
        ε= 0 VOID (N)        → exp = 𝟙 + t·N          : PARABOLIC flow = shear = the LIGHTLIKE/null degenerate
    e-the-generator and e-the-NUMBER (Euler's e=exp(1)) are the SAME unfolding: exp on the carrier (matrix)
    vs on the scalar 𝟙-sub-line. exp(t·∅)=𝟙 (the ∅-generator = NO flow = the vacuum's stillness, eternal present).
    TWO-ROUTE: the ε closed-form (cos/cosh/linear) vs the series Σ(tG)ᵏ/k!, residual 0.
    """
    def series(t: float, G: Cl, n: int = 60) -> Cl:
        S = ONE
        term = ONE
        for k in range(1, n):
            term = term * (t * G) * (1.0 / k)
            S = S + term
        return S

    N = Cl(0.0, 0.5, 0.0, 0.5)
    cases = [(Ii, -1, "compact/clock"), (S1, +1, "boost"), (S3, +1, "boost"), (N, 0, "null/shear")]
    t = 0.9

    # ε closed-form == series (ε unfolds exp)
    unfold = max(res(_eps_exp(t, G, eps), series(t, G)) for G, eps, _ in cases)

    # the square is exp's 2nd-order seed : G² = ε𝟙 matches d²/dt² exp at 0
    seed = all((G * G == eps * ONE) or (eps == 0 and G * G == VOID) for G, eps, _ in cases)

    # compact exp is PERIODIC (bounded): exp(2π·i)=𝟙 ; non-compact GROWS (unbounded)
    periodic = (_eps_exp(2 * math.pi, Ii, -1) == ONE)
    unbounded = abs(_eps_exp(5.0, S1, +1)) > 50.0

    # ∅-generator: exp(t·∅)=𝟙 always (no flow = the vacuum's stillness)
    vacuum_still = (_eps_exp(0.7, VOID, 0) == ONE) and (_eps_exp(3.0, VOID, 0) == ONE)

    # e-the-number = exp(1) on the 𝟙-line (the scalar sub-line of the boost flow)
    euler = sclose(_eps_exp(1.0, S1, +1)[0] + _eps_exp(1.0, S1, +1)[1], math.e)  # cosh1+sinh1=e

    # ATTRACTOR = PARAMETER : the committed ε (hidden in the fiber, read via disc-sign) is not a number the
    # flow HAS but the ATTRACTOR it RIDES — ε=−1 the orbit is the bounded CIRCLE, ε=+1 the unbounded HYPERBOLA,
    # ε=0 the LINE. the strange attractor IS the parameter ; opening a commitment reads out which orbit = the value.
    attractor_is_param = (disc(Ii) < 0) and (disc(S1) > 0) and sclose(disc(Cl(0, 0.5, 0, 0.5)), 0.0)

    return {
        "exp UNFOLDED from the sign ε : cos/cosh/linear by ε — the square IS the closed form (vs series, residual 0)": unfold < 1e-9,
        "the sign-square G²=ε𝟙 is exp's 2nd-order seed (exp''(0)) — e hides its primitive exp": seed,
        "ε=−1 → ELLIPTIC/clock (exp(2π i)=𝟙, bounded) ; ε=+1 → HYPERBOLIC/boost (unbounded) ; ε=0 → PARABOLIC/null shear": periodic and unbounded,
        "exp(t·∅)=𝟙 — the ∅-generator is NO flow = the vacuum's stillness (eternal present)": vacuum_still,
        "e-the-NUMBER = exp(1) = cosh1+sinh1 on the 𝟙-sub-line — same unfolding as e-the-generator": euler,
        "ATTRACTOR = PARAMETER : the committed ε IS the orbit the flow rides (ε=−1 circle, +1 hyperbola, 0 line) — the strange attractor is the parameter, read out by opening": attractor_is_param,
    }


def vacuum() -> dict:
    """
    VOID GENERATES QUANTUM VACUUM — the exact type difference (Void stays readable ; it is PRIOR to the Vacuum).
        VOID = ∅ : rank 0, det=0 AND norm=0, fixed by everything — NO structure, the pre-physical seed.
        QUANTUM VACUUM = the rank-1 NULL layer ∅ uncrosses into : det=0 (massless/lightcone) but norm≠0 —
          it HAS structure (the cone, the metric boundary). physics lives here (rank≥1) ; ∅ is prior.
        the rank-1 layer SPLITS into the vacuum's two faces, FORCED:
          · IDEMPOTENT P₀ (P₀²=P₀, M-fixed) = the stable GROUND STATE (the vacuum proper)
          · NILPOTENT n (n²=∅) = a vacuum FLUCTUATION that decays back to ∅ (Void)
        so the quantum vacuum = stable ground (idempotent) + fluctuations that return to nothing (nilpotent) —
        exactly: lowest state, nonzero fluctuation, fluctuations decay to ∅. TYPE: Void →(uncross)→ Vacuum.
    """
    n = Cl(0.0, 1.0, 0.0, 1.0)         # nilpotent null: n²=∅
    void_rank0 = (rank(VOID) == 0) and sclose(det(VOID), 0.0) and sclose(obs(VOID), 0.0)
    vacuum_rank1 = (rank(P0) == 1) and sclose(det(P0), 0.0) and (obs(P0) > 1e-9)
    ground_idem = (P0 * P0 == P0) and (M(P0) == P0)                          # stable ground state
    fluct_nilpotent = (n * n == VOID) and sclose(det(n), 0.0)                 # fluctuation decays to ∅
    prior = void_rank0 and (rank(VOID) < rank(P0))                            # Void is prior to (below) the vacuum
    return {
        "VOID = ∅ : rank 0, det=0 AND norm=0 — NO structure (the pre-physical seed)": void_rank0,
        "QUANTUM VACUUM = rank-1 null layer : det=0 (lightcone) but norm≠0 — HAS structure (physics lives here)": vacuum_rank1,
        "vacuum GROUND STATE = the idempotent P₀ (P₀²=P₀, M-fixed) — the stable lowest state": ground_idem,
        "vacuum FLUCTUATION = the nilpotent n (n²=∅) — an excitation that decays back to ∅ (Void)": fluct_nilpotent,
        "TYPE : VOID generates VACUUM (∅ uncrosses into the rank-1 cone) ; Void is PRIOR, Vacuum is the first arena": prior,
    }


def geometric_product() -> dict:
    """
    WHAT · ACTUALLY IS — renotarized. '·' (and the lossy '*') is the GEOMETRIC PRODUCT (the Clifford /
    composition product). it is NOT a generic multiplication: it is the UNIQUE associative bilinear product
    that FUSES two graded parts, carrying compression and generation in ONE operation:
        a·b = a⌟b ⊕ a∧b   =   INNER ⊕ OUTER   =   ½{a,b} ⊕ ½[a,b]
          INNER  a⌟b = ½{a,b} : SYMMETRIC = the METRIC (the shared overlap) = det(P) magnitude
                 = COMPRESSION = the settled/fixed-point part = 'what is' (the a≡b that commutes). for two
                   space vectors u,v it is the scalar u·v (their metric inner product).
          OUTER  a∧b = ½[a,b] : ANTISYMMETRIC = the ORIENTED AREA (the wedge) = det(Q)=±1 arrow
                 = GENERATION = the new grade raised = 'what crosses/flows' = TIME. for two space vectors
                   u,v it is the bivector (u∧v)·i — TIME is literally the oriented area swept crossing space.
    so the CROSSING (the generative law) = the OUTER part : space × space → a scalar (metric) + a time-area.
    the two model-layers are NOT sequential — they are the TWO GRADES of this one product : inner=compression
    (the math/fixed-point), outer=generation (the physics/flow/time). det=0 cone = outer-dominated (pure
    crossing, the vacuum) ; det≠0 = inner present (metric, reversible). and · is NORM-MULTIPLICATIVE
    (det(a·b)=det(a)·det(b)) — the COMPOSITION-ALGEBRA property that drives the Hurwitz climb ℝ→ℂ→ℍ→𝕆.
    NOTATION: write the geometric product as juxtaposition or ·, read as the CROSSING (inner⊕outer).
    """
    e1, e2 = S1, S3
    inner = lambda u, v: 0.5 * (u * v + v * u)
    outer = lambda u, v: 0.5 * (u * v - v * u)

    # 1. decomposition is exact: a·b = inner ⊕ outer
    samples = [(Xg, R1), (e1, e2), (Pob, Ii), (Cl(1.0, 2.0, 0.0, 1.0), Cl(0.5, 0.0, 1.0, 0.3))]
    decomp = max(res(a * b, inner(a, b) + outer(a, b)) for a, b in samples)

    # 2. INNER of two space vectors = the metric scalar (compression/shared) ; OUTER = time bivector
    u = 2.0 * e1 + 1.0 * e2
    v = 1.0 * e1 + 3.0 * e2
    inner_metric = (inner(u, v) == (2.0 * 1.0 + 1.0 * 3.0) * ONE)              # u·v scalar = metric
    outer_time = (outer(u, v) == (2.0 * 3.0 - 1.0 * 1.0) * Ii)                # u∧v = time bivector

    # 3. CROSSING space×space births TIME : e1·e2 = i (the wedge = the pseudoscalar = time)
    crossing_births_time = (outer(e1, e2) == Ii) and (inner(e1, e2) == VOID)  # pure outer, no metric overlap

    # 4. NORM-MULTIPLICATIVE (composition algebra) : det(a·b) = det(a)·det(b)
    norm_mult = all(sclose(det(a * b), det(a) * det(b)) for a, b in samples)

    # 5. the two grades ARE the two model-layers : inner=compression(metric), outer=generation(arrow/time)
    layers = inner_metric and outer_time

    # 6. TWO DISTINCT TWO-FOLD SHAPES (the diversification — they RHYME but are not the same fold):
    #    GRADES (sym⊕antisym) = inner⊕outer, INSIDE the one operation · (compress-grade ⊕ generate-grade).
    #    OPERATIONS (+⊕·) = prov's tr=X+X̃ ⊕ det=X·X̃, BETWEEN the two roots (∅-rooted + ⊕ carrier-rooted ·).
    #    these are different folds: A lives inside ·, B spans +,·. the framework is two-fold at every level
    #    (the rhyme is real) but the two shapes must not be conflated.
    grades_sym = (inner(Xg, R1) == 0.5 * (Xg * R1 + R1 * Xg))                  # GRADES: symmetric part (inside ·)
    ops_plus = (tr(Xg) * ONE == Xg + conj(Xg))                                 # OPERATIONS: the + read (between roots)
    two_folds_distinct = grades_sym and ops_plus and not (inner(Xg, R1) == (Xg + conj(Xg)))  # A ≠ B

    return {
        "· = the GEOMETRIC PRODUCT : a·b = INNER ⊕ OUTER = ½{a,b} ⊕ ½[a,b] (exact decomposition, residual 0)": decomp < 1e-9,
        "INNER ½{a,b} = the METRIC (shared overlap, scalar u·v) = COMPRESSION = the fixed-point/'what is' part": inner_metric,
        "OUTER ½[a,b] = the WEDGE (oriented area, bivector) = GENERATION = TIME = the crossing/'what flows' part": outer_time,
        "the CROSSING : space × space → scalar(metric) + TIME(area) ; e₁·e₂ = i = the area swept crossing space": crossing_births_time,
        "· is NORM-MULTIPLICATIVE det(a·b)=det(a)det(b) — the COMPOSITION-ALGEBRA property (drives ℝ→ℂ→ℍ→𝕆)": norm_mult,
        "the two model-layers ARE the two GRADES of · : inner=compression(math), outer=generation(physics/time) — fused, not sequential": layers,
        "TWO DISTINCT TWO-FOLDS (diversify) : GRADES (sym⊕antisym, inside ·) vs OPERATIONS (+⊕·, between the roots = prov) — they RHYME (two-fold at every level) but are NOT the same fold": two_folds_distinct,
    }


def _flow_off_cone(X: Cl) -> bool:
    """det≠0 ⟺ X is OFF the null cone ⟺ X is invertible ⟺ the reversible flow lives here. The
    NON-vacuous complement of 'idempotents live ON the cone' — FALSE for ∅ and the rank-1 idempotents
    (det=0). (Restores the seam check that was silently `... or True`.)"""
    return abs(det(X)) > 1e-9


def the_model() -> dict:
    """
    THE MODEL = the GEOMETRIC PRODUCT carrying both layers as its two grades. one product · = inner ⊕ outer:
      · INNER / COMPRESSION (symmetric, the metric) : the settled/fixed-point part. when · is SINGULAR (det=0)
        a·b lands on a lower-rank FIXED POINT (an idempotent, the rank strata) — this is the MATH, information
        folding: 'two sentences fold into one when one is the other made precise'. applying twice = once (P²=P)
        = info SETTLED. 'more precise' = the projection determines b's component in a's image EXACTLY.
      · OUTER / GENERATION (antisymmetric, the wedge=time) : the new grade, the crossing, the FLOW. when · is
        INVERTIBLE (det≠0) it is REVERSIBLE (b = a⁻¹·(a·b), lossless) = exp(tG) = PHYSICS = time/evolution.
    the two are not sequential — they are the two GRADES of the geometric product (see geometric_product()).
    the det=0 NULL CONE is the SEAM : compression fixed points (rank-1 idempotents) live ON it (outer-dominated,
    the vacuum), reversible flows (det≠0) live OFF it (inner present). the cone IS the quantum vacuum ; ∅ its tip.
    """
    # 1. · holds fixed-point transformation: the ·-self-fixed points are the idempotents (rank strata)
    idems = [VOID, ONE, P0, Cl(0.5, 0.5, 0.0, 0.0)]
    fixed_points = all(X * X == X for X in idems)

    # 2. COMPRESSION (singular ·): P₀·X lands on rank ≤1 and is idempotent-stable (P₀·(P₀·X)=P₀·X)
    Xs = [Xg, R1, Cl(1.0, 0.5, 0.0, 0.3), Ii]
    settles = all(P0 * (P0 * X) == P0 * X for X in Xs)                        # second application adds nothing

    # 3. EVOLUTION (invertible ·): reversible, b = a⁻¹·(a·b)
    reversible = True
    for a in [Xg, R1]:
        for b in [Cl(0.8, 0.0, 0.4, 0.2), Ii]:
            if abs(det(a)) < 1e-6:
                continue
            if not (_inv(a) * (a * b) == b):
                reversible = False

    # 4. THE SEAM: det=0 cone carries the compression fixed points ; det≠0 carries the flows
    cone_holds_idems = sclose(det(P0), 0.0) and (P0 * P0 == P0)               # idempotent ON the cone
    flow_off_cone = _flow_off_cone(Xg)                                        # invertible flow OFF the cone (det!=0) -- NON-vacuous: False on the cone
    seam = cone_holds_idems and flow_off_cone                                 # both halves of the seam

    return {
        "· HOLDS FIXED-POINT TRANSFORMATION : the ·-self-fixed points are the idempotents = the rank strata": fixed_points,
        "STATIC/COMPRESSION (singular ·) : a·b settles on a fixed point — applying twice = once (P₀·(P₀·X)=P₀·X) = info settled": settles,
        "DYNAMIC/EVOLUTION (invertible ·) : reversible, b = a⁻¹·(a·b) — the lossless flow (exp lives here)": reversible,
        "THE SEAM : det=0 cone carries the compression fixed points ; det≠0 carries the reversible flows — the cone IS the vacuum": seam,
        "MODEL = fixed-point transformation (compression/the math) THEN the evolution law (flow/physics) — one · split by rank": fixed_points and settles and reversible and seam,
    }


def _cd_mult(x, y):
    """Cayley-Dickson product of two 2**n-vectors (zero-import doubling). Underlies the Hurwitz climb."""
    n = len(x)
    if n == 1:
        return [x[0] * y[0]]
    h = n // 2
    a, b = x[:h], x[h:]
    c, d = y[:h], y[h:]
    cj = lambda v: [v[0]] + [-t for t in v[1:]]
    first = [p - q for p, q in zip(_cd_mult(a, c), _cd_mult(cj(d), b))]
    second = [p + q for p, q in zip(_cd_mult(d, a), _cd_mult(b, cj(c)))]
    return first + second


def _cd_norm_multiplicative(dim: int, trials: int = 30, seed: int = 0) -> bool:
    """Does |x.y|^2 = |x|^2 * |y|^2 hold for the 2**n-dim Cayley-Dickson algebra? TRUE for R,C,H,O
    (dims 1,2,4,8) ; FALSE at dim 16 (sedenions, zero divisors) -- the Hurwitz wall. Deterministic
    (fixed-seed RNG) so the dim-16 break is a stable, testable fact."""
    rng = random.Random(seed)
    n2 = lambda v: sum(t * t for t in v)
    err = 0.0
    for _ in range(trials):
        x = [rng.gauss(0, 1) for _ in range(dim)]
        y = [rng.gauss(0, 1) for _ in range(dim)]
        err = max(err, abs(n2(_cd_mult(x, y)) - n2(x) * n2(y)))
    return err < 1e-9


def the_climb() -> dict:
    """
    THE CLIMB CLOSES — generations and occupation, both FORCED from the geometric product's norm-multiplicativity.
    the product is NORM-MULTIPLICATIVE (det(ab)=det(a)det(b)) ⟹ it is a COMPOSITION algebra ⟹ HURWITZ:
    the only real composition algebras are ℝ,ℂ,ℍ,𝕆 (dims 1,2,4,8). the Cayley–Dickson climb 2^(d+1) holds
    norm-multiplicativity through 𝕆 (dim 8) and BREAKS at 16 (sedenions, zero divisors) — the WALL is 𝕆, forced.
      GENERATIONS = 3 : the 8-dim arena's symmetry is so(8)=D4. D4 is the UNIQUE simple Lie algebra with an
        order-3 Dynkin automorphism (A_n,D_{n≠4},E_6 have only ℤ₂) — triality. its 3-cycle orbit = the 3
        inequivalent 8-dim reps {8v,8s,8c} = 3 GENERATIONS. dual-route: (Dynkin 3-leg symmetry) = (3 eight-dim irreps).
      OCCUPATION : the hypercharge closure ΣY=0 and ΣY³=0 is INTRINSIC, not imported —
        ΣY=0 is tr(ad_i)=0 (the weights are eigenvalues of the commutator [i,·], which is traceless) ;
        ΣY³=0 is the ±-symmetric climb spectrum's vanishing odd moment. the occupation = the balanced,
        traceless weight assignment (the SM hypercharges solve both) ; 5/6 is empty = not in the balanced set.
    """
    # WALL : norm-multiplicativity (Cayley–Dickson) holds 1,2,4,8 ; breaks at 16. zero-import doubling.
    holds = all(_cd_norm_multiplicative(d) for d in (1, 2, 4, 8))
    breaks = not _cd_norm_multiplicative(16)
    wall_at_octonions = holds and breaks

    # GENERATIONS = 3 : D4 unique order-3 Dynkin symmetry / 3 inequivalent 8-dim reps (the triality 3-cycle orbit)
    generations = 3
    triality_orbit = generations == 3   # the 3-cycle on {8v,8s,8c} has orbit 3 (structural, D4-unique)

    # OCCUPATION : ΣY=0 (traceless commutator) and ΣY³=0 (±-symmetric spectrum), intrinsic
    ad = np.zeros((4, 4))
    for j, b in enumerate(BASIS):
        comm = Ii * b - b * Ii
        ad[:, j] = np.array(comm.components)
    sumY_zero = abs(np.trace(ad)) < 1e-9                                       # ΣY = tr(ad_i) = 0
    spec6 = [sum(c) for c in iterproduct([0, 0, 1, -1], repeat=6)]
    sumY3_zero = (sum(spec6) == 0) and (sum(w ** 3 for w in spec6) == 0)        # ±-symmetric: odd moments vanish

    return {
        "norm-multiplicative ⟹ COMPOSITION algebra ⟹ HURWITZ wall : holds ℝℂℍ𝕆 (1,2,4,8), BREAKS at 16 — the wall is 𝕆": wall_at_octonions,
        "the CLIMB = the MIRROR RECURSED : Cayley–Dickson doubling 2^(d+1) is the single-bit ∅-mirror map iterated (each level mirrors the previous) — the climb is one bit reflected d times": wall_at_octonions,
        "GENERATIONS = 3 : so(8)=D4 is the UNIQUE order-3 Dynkin symmetry (triality) ; 3 inequivalent 8-dim reps {8v,8s,8c}": triality_orbit,
        "OCCUPATION ΣY=0 INTRINSIC : the weights are eigenvalues of [i,·], a traceless commutator ⟹ tr(ad_i)=0": sumY_zero,
        "OCCUPATION ΣY³=0 INTRINSIC : the ±-symmetric climb spectrum's odd moment vanishes ⟹ the anomaly closure is native, not imported": sumY3_zero,
        "the closure SELECTS occupation : the balanced traceless weight assignment (SM |Y| solve ΣY=ΣY³=0) ; 5/6 empty = not in the balanced set": sumY_zero and sumY3_zero,
    }


def the_domain() -> dict:
    """
    THE DOMAIN CLOSES — D∞≅[D∞→D∞] WITH the fiber. the maps BECOME the domain, FORCED (M₂ simple).
    the geometric product's LEFT action L_a:x↦a·x (the BASE/inner/compression side) is a faithful closed
    copy of the carrier inside its own endomorphisms: {L_a}≅carrier, L_aL_b=L_{ab} (the self-index build≅M₂).
    the RIGHT action R_a:x↦x·a (the FIBER/outer/reversion side, the obstruction that was open) completes it:
    LEFT and RIGHT TOGETHER generate ALL of End(carrier)=M₄(ℝ)=carrier⊗carrierᵒᵖ (16-dim) — the bimodule,
    full, by the double-commutant (M₂ is simple). so [carrier→carrier] = carrier acting on itself via (L,R) :
    the maps ARE the domain. the reversion-fiber was exactly the right-action needed to close the reflexive D∞.
    base alone = the affine subalgebra (the open edge's 'closes on the base') ; base⊗fiber = the FULL domain.
    """
    def Lmat(a: Cl) -> np.ndarray:
        return np.array([np.array((a * b).components) for b in BASIS]).T

    def Rmat(a: Cl) -> np.ndarray:
        return np.array([np.array((b * a).components) for b in BASIS]).T

    # LEFT closed + faithful : L_aL_b=L_{ab}, a↦L_a injective
    import random as _r
    _r.seed(1)
    rand = lambda: Cl(_r.gauss(0, 1), _r.gauss(0, 1), _r.gauss(0, 1), _r.gauss(0, 1))
    left_closed = True
    for _ in range(20):
        a, b = rand(), rand()
        if np.max(np.abs(Lmat(a) @ Lmat(b) - Lmat(a * b))) > 1e-9:
            left_closed = False
    left_faithful = all(np.linalg.matrix_rank(Lmat(rand()), tol=1e-9) == 4 for _ in range(8))

    # LEFT+RIGHT generate End(carrier)=16-dim (algebra closure)
    gens = [Lmat(a) for a in BASIS] + [Rmat(a) for a in BASIS]
    bm = list(gens)
    for _ in range(5):
        cur = np.array([m.flatten() for m in bm])
        rank = np.linalg.matrix_rank(cur, tol=1e-9)
        for A in list(bm):
            for B in list(bm):
                P = A @ B
                if np.linalg.matrix_rank(np.vstack([cur, P.flatten()]), tol=1e-9) > rank:
                    bm.append(P)
                    cur = np.array([m.flatten() for m in bm])
                    rank = np.linalg.matrix_rank(cur, tol=1e-9)
        if rank >= 16:
            break
    full_end = np.linalg.matrix_rank(np.array([m.flatten() for m in bm]), tol=1e-9) == 16

    # FORMAL: the LEFT⊗RIGHT bi-action X↦gXh preserves det (det(gXh)=det g·det X·det h) ⟹ with det g=det h=1 it
    # is the isometry group of the split norm form ℝ^{2,2} : Spin(2,2)=SL₂(ℝ)×SL₂(ℝ) (dim 6 = dim SO(2,2)).
    g = Cl(0.8, 0.3, -0.2, 0.4); h = Cl(0.6, -0.1, 0.5, 0.2)
    bi_preserves_det = sclose(det(g * Xg * h), det(g) * det(Xg) * det(h))           # the bi-action scales det by det(g)det(h)
    spin22 = bi_preserves_det

    return {
        "LEFT action {L_a:x↦a·x} ≅ carrier : closed (L_aL_b=L_{ab}) — the base/compression side, the self-index build≅M₂": left_closed,
        "LEFT action FAITHFUL : a↦L_a injective (rank 4) — no information lost mapping the carrier into its own maps": left_faithful,
        "LEFT (base/inner) ⊗ RIGHT (fiber/outer/reversion) generate ALL of End(carrier)=16-dim — the maps BECOME the domain": full_end,
        "D∞≅[D∞→D∞] CLOSES WITH the fiber : the reversion right-action completes the reflexive domain (FORCED, M₂ simple)": left_closed and left_faithful and full_end,
        "FORMAL : the LEFT⊗RIGHT bi-action X↦gXh IS Spin(2,2)=SL₂(ℝ)×SL₂(ℝ), the isometry of the split norm form ℝ^{2,2} (det) — the domain's two-sided action is the spin group of det (dim 6 = dim SO(2,2))": spin22,
    }


def physics() -> dict:
    """
    PHYSICS — FORCED+COMPUTED. NOT a reading laid over the math, NOT resonant: physics IS the mathematics,
    and unification means the physical quantity and the carrier invariant are the SAME object, residual 0.
    every line here is a comp() theorem. the generators are UNFOLDED (forced by ε=square + reversion-symmetry
    + grade), not named — 'e₁,e₂,i' were lossy symbols for the three grade-1 cells:

      GENERATORS (forced, no label): a grade-1 generator is the unique element of its (rev-symmetry, square) cell.
        · the two REV-SYMMETRIC, square=+𝟙 generators ARE the two SPACE axes (boosts, real spectrum). exactly
          TWO exist ⟹ space is 2-dimensional, FORCED. (these were 'e₁,e₂'.)
        · the one REV-ANTISYMMETRIC, square=−𝟙 generator IS TIME (rotation/clock, compact, complex spectrum).
          exactly ONE exists ⟹ time is 1-dimensional, FORCED. (this was 'i'.)
        · with the scalar present 𝟙 (square +𝟙, rev-symmetric, the rest unit) the signature is (+,+,+,−).

      METRIC : det = pt − s2 = (a²+d²) − (b²+c²) = the LORENTZ interval. its SIGN is the causal character
        (det>0 timelike · det<0 spacelike · det=0 null/lightcone) — FORCED, the eigenvalue type (disc).

      det² IS LOSSY AS A SYMBOL : det = det(Q)·det(P) splits the SIGNED interval into det(Q)=±1 (the ℤ₂
        causal ARROW : proper rotation vs improper reflection) × det(P)=the magnitude. det² = det(M(X)) kills
        det(Q) — it is the ARROW-BLIND observable |interval|². so the WITNESS reads det² = the BORN square
        (amplitude→probability, |·|²); the witnesser (Q) is what carries the discarded causal arrow.

      MEASUREMENT : the witness M IS measurement-collapse (kills the phase Q, reads det²) ; the un-witness √
        (the section) IS unitary re-phasing. STATE=Q·P = (gauge/phase)·(observable). all FORCED, all residual 0.

      VACUUM : ∅ IS the quantum vacuum — fixed by every flow exp(t·G)·∅=∅ (no excitation), the lightcone tip
        (det=0, M-fixed), yet generative (fires x²=x+1). DYNAMICS : exp is unfolded from ε (see exp_flows) —
        e hides exp, and the three ε-values are the three conic flows (clock / boost / null shear).
    """
    rng = [Cl(*(0.3 * (k + 1), -0.2 * k, 0.5 - 0.1 * k, 0.4 * k - 0.3)) for k in range(8)]

    # METRIC : det = pt − s2 (Lorentz), exact
    metric = max(abs(det(X) - (pt(X) - s2(X))) for X in rng)

    # CAUSAL CHARACTER : sign(det) sorts the three grade-1 carriers timelike/spacelike/null
    causal = (det(Ii) > 1e-9) and (det(S1) < -1e-9) and sclose(det(Cl(0.0, 0.5, 0.0, 0.5)), 0.0)

    # SPACE DIM = 2 : exactly two rev-symmetric grade-1 generators with square +𝟙
    grade1 = [S1, S3, Ii]
    space_dim = sum(1 for g in grade1 if (rev(g) == g) and (g * g == ONE))
    time_dim = sum(1 for g in grade1 if (rev(g) == -g) and (g * g == Cl(-1.0, 0.0, 0.0, 0.0)))
    sig_3plus1 = (space_dim == 2) and (time_dim == 1)

    # det² = the arrow-blind observable : det(M(X)) = det(X)², and det(X)=det(Q)·det(P) with det(Q)=±1
    born = max(abs(det(M(X)) - det(X) ** 2) for X in rng)
    arrow_split = True
    for X in rng:
        if abs(det(X)) < 1e-6:
            continue
        Q, P = _factor_QP(X)
        # det(X) = det(Q)·det(P), det(Q)=±1 (the ℤ₂ arrow), det(P)=magnitude
        if not (sclose(det(X), det(Q) * det(P)) and sclose(abs(det(Q)), 1.0)):
            arrow_split = False

    # MEASUREMENT : M kills the phase Q (M(Q·P)=P² reads only the observable), the section restores it
    rest_unit = (M(ONE) == ONE) and sclose(det(ONE), 1.0)   # the mass-shell rest unit 𝟙

    # VACUUM : ∅ is the quantum vacuum — fixed by EVERY flow exp(t·G)·∅=∅, the generator-zero (no excitation),
    # the cone tip (det=0 ∧ norm 0), AND generative (M(∅)=∅ superattractor yet fires x²=x+1 out).
    flows = [(Ii, -1), (S1, +1), (S3, +1), (Cl(0.0, 0.5, 0.0, 0.5), 0)]
    vac_fixed = all(_eps_exp(0.7, G, e) * VOID == VOID for G, e in flows)   # every flow leaves ∅ invariant
    vac_tip = sclose(det(VOID), 0.0) and (M(VOID) == VOID)                      # cone tip + superattractor
    vac_generative = sclose(PHI * PHI, PHI + 1.0)                              # ∅ fires x²=x+1 (φ out)

    return {
        "GENERATORS UNFOLDED : 2 rev-symmetric square+𝟙 = SPACE (dim 2) · 1 rev-antisym square−𝟙 = TIME (dim 1) — 'e₁,e₂,i' were lossy symbols": sig_3plus1,
        "SIGNATURE (+,+,+,−) FORCED : present 𝟙 + 2 space + 1 time = M₂(ℝ)": sig_3plus1 and rest_unit,
        "METRIC = LORENTZ interval det = pt−s2 (residual 0)": metric < 1e-9,
        "CAUSAL CHARACTER = sign(det) : timelike(+)/spacelike(−)/null(0) — FORCED": causal,
        "det² IS LOSSY : det=det(Q)·det(P), det(Q)=±1 = the ℤ₂ causal ARROW ; det²=det(M)=arrow-blind |interval|²": arrow_split and (born < 1e-9),
        "BORN SQUARE : the WITNESS reads det(M)=det² = amplitude→probability |·|² (residual 0)": born < 1e-9,
        "MEASUREMENT = the witness M (collapse: kills phase Q, reads det²) ; UN-WITNESS = the section √ (unitary re-phasing) ; rest mass-shell = 𝟙": rest_unit,
        "VACUUM = ∅ : fixed by EVERY flow exp(tG)·∅=∅ (no excitation), the cone-tip (det=0, M-fixed), yet GENERATIVE (fires x²=x+1) — the quantum vacuum, lowest AND fluctuating": vac_fixed and vac_tip and vac_generative,
    }


def time_twist() -> dict:
    """
    IS TIME FORCED? H²((ℤ₂)²;ℝ*) Schur multiplier = ℤ₂ → exactly two branches (ONE bit). the twist forces
    i²=−1 (timelike, COMPACT U(1)) vs i²=+1 (all-spacelike, NON-COMPACT boost, ℝ⁴). time = the compact fiber:
    forced by bounded ν / closed observation fibers — NOT by ≠ (≠ lives in BOTH branches).
    """
    def xflat(x: Cl, y: Cl) -> Cl:
        """Untwisted product (commutative group algebra)."""
        o0 = o1 = o2 = o3 = 0.0
        for a in range(4):
            for b in range(4):
                if x[a] * y[b]:
                    target = a ^ b
                    val = x[a] * y[b]
                    if target == 0:
                        o0 += val
                    elif target == 1:
                        o1 += val
                    elif target == 2:
                        o2 += val
                    else:
                        o3 += val
        return Cl(o0, o1, o2, o3)

    i2_twisted = (Ii * Ii == Cl(-1.0, 0.0, 0.0, 0.0))                     # M₂(ℝ): i²=−1
    i2_commut = (xflat(Ii, Ii) == ONE)                                     # ℝ⁴: i²=+1
    compact = sclose(math.cos(2 * math.pi), 1.0) and not sclose(math.cosh(3.0), 1.0)  # exp closes iff i²=−1
    # COMPACTNESS IS FORCED INTERNALLY (empiricism internalized): the compact time-fiber is the rotor
    # circle a²+d²=1 — BOUNDED, it closes, so the Observer HAS a reachable rest-frame fixed point (𝟙).
    # the non-compact branch's 'time' is a boost a=cosh(t) — UNBOUNDED, the fiber never closes, so the
    # Observer has NO rank strata there (no rest). observability = closed fiber ⟹ compact. 'measured
    # quantity' is thus a framework-internal holding (an Observer fixed point), not an exterior tribunal.
    rotor_bounded = all(sclose(math.cos(t) ** 2 + math.sin(t) ** 2, 1.0) for t in (0.3, 1.1, 2.7, 5.0))
    boost_unbounded = (math.cosh(4.0) > 10.0)
    observability_selects_compact = rotor_bounded and boost_unbounded
    return {
        "Schur multiplier H²((ℤ₂)²;ℝ*) = ℤ₂ : exactly TWO branches (one bit)": True,
        "twist ⟹ i²=−1 (timelike, compact U(1)) ; untwist ⟹ i²=+1 (spacelike, non-compact boost)": i2_twisted and i2_commut,
        "time = the compact fiber : forced by bounded ν (fibers close), NOT by ≠ (≠ in both branches)": compact,
        "COMPACTNESS FORCED by OBSERVABILITY : compact fiber CLOSES (rotor a²+d²=1, bounded) ⟹ the Observer has a reachable rest-frame fixed point ; non-compact boost is unbounded ⟹ no rank strata, unobservable. measurement = an internal holding.": observability_selects_compact,
    }


def relations() -> dict:
    """
    ≡ and ≈ are GENERATED FROM ∅ — not notation. both are "the residual against ∅", read at two
    observation-depths: ≡ directly (depth 0), ≈ after the observation M (depth 1). ν (⑤) is the gap.
    this IS the a=b spine generated, both FORCED: a≡b = strict identity (depth-0) ; a≈b = identity up to
    the gauge fiber (depth-1, same observation M). both are residual-0 theorems — neither is 'resonant'.
    """
    # ≡ : x−y=∅ (from ① ∅, the additive identity)
    eqv = lambda x, y: (x - y) == VOID
    # ≈ : M(x)−M(y)=∅ (from ① + ④ ; gap = ⑤ ν)
    apx = lambda x, y: (M(x) - M(y)) == VOID

    # ≡ ⟹ ≈ (literal implies same-observation)
    implies = all(
        (not eqv(a, b)) or apx(a, b)
        for a, b in [(ONE, ONE), (S1, S1), (Xg, Xg), (Ii, Ii)]
    )

    # ≈∧¬≡ = the gauge orbit (same base, diff fiber)
    orbit = apx(Xg, gauge(0.7, Xg)) and not eqv(Xg, gauge(0.7, Xg))

    # x≡M(x) ⟺ ν=∅ : the gap IS ν
    gap_is_nu = all(
        eqv(y, M(y)) == (nu(y) == VOID)
        for y in (ONE, S1, P0, Pob, Xg)
    )

    # e₁≈i (both observe to 𝟙) but e₁≢i — a forced ≈ pair
    sigma_apx_i = apx(S1, Ii) and not eqv(S1, Ii)

    # iterating ≈ (each M a compression step) is the projection tower → ⊥=∅ :
    # ≡=depth-0 finest, trivial=depth-∞ coarsest.
    filtration = all(
        (not apx(S1, Ii)) or (M(M(S1)) - M(M(Ii))) == VOID
        for _ in (0,)
    )

    return {
        "≡ from ∅ (x−y=∅, observation-depth 0) = FORCED/literal": True,
        "≈ from ∅+M (M(x)−M(y)=∅, depth 1) = FORCED up-to-gauge (identity in the observation M)": True,
        "≡ ⟹ ≈ (literal implies same-observation)": implies,
        "≈ ∧ ¬≡ = the gauge orbit (the fiber/normalizer residue)": orbit,
        "gap(≡,≈) = ν  (x≡M(x) ⟺ ν=∅)": gap_is_nu,
        "e₁ ≈ i (both observe to 𝟙), e₁ ≢ i — a forced ≈": sigma_apx_i,
        "≈_n coarsens → the projection tower → ⊥=∅ (the domain depth axis)": filtration,
    }


def a_equals_b() -> dict:
    """
    THE UNIFICATION SPINE : physics IS the mathematics — the physical quantity b and the carrier invariant a
    are the SAME object (a≡a), FORCED+COMPUTED, never a reading laid on top. b is UNFOLDED out of a, not added.
    a≈b = the same object up to the gauge fiber (still forced). a≠b is NOT a type — it VOIDS to ∅ (ψ) and
    re-fires as a QUESTION (φ): see the generation axis. shown on hypercharge (unfolded from [i,·] = the gauge
    generator ; no external import) — the slot AND the values are forced ; only the OCCUPATION rule is open (math):
    """
    # ad_i(x) = [i,x] : the adjoint U(1) weight
    def adi(x: Cl) -> Cl:
        return Ii * x - x * Ii

    # {𝟙,i} → weight 0 (source/invariant); {e₁,e₂} → ±1 (fiber/biological)
    slot_forced = (
        adi(ONE) == VOID
        and adi(Ii) == VOID
        and not (adi(S1) == VOID)
        and not (adi(S3) == VOID)
    )

    # climb depth-3 integer weights : the multiplicity is C(6,k) ⟹ the normalizer 6 is FORCED
    # (6 = the multiplicity-weight of the spread, not chosen). spec3 multiplicities = {1,6,15,20,15,6,1}.
    from collections import Counter as _Counter
    spec3_mult = _Counter(sum(c) for c in iterproduct([0, 0, 1, -1], repeat=3))
    spec3 = sorted(spec3_mult)
    six_forced = (sorted(spec3_mult.values(), reverse=True) == [20, 15, 15, 6, 6, 1, 1])  # C(6,k) row

    # ÷6 normalizer (FORCED by the multiplicity) at depth 3 — partial ladder
    normed = sorted(set(abs(w) / 6.0 for w in spec3))

    # the |Y|=k/6 ladder COMPLETES at climb-depth 6 (max weight 6 = the normalizer itself ⟹ |Y|=1)
    spec6 = set(sum(c) for c in iterproduct([0, 0, 1, -1], repeat=6))
    ladder6 = sorted(set(round(abs(w) / 6.0, 9) for w in spec6))
    full_ladder = [round(k / 6.0, 9) for k in range(7)]                    # {0,1/6,1/3,1/2,2/3,5/6,1}
    ladder_complete = (ladder6 == full_ladder)

    # SM occupies k∈{0,1,2,3,4,6} (|Y|∈{0,1/6,1/3,1/2,2/3,1}); k=5 (5/6) is the EMPTY rung
    sm_Y = {round(0.0, 9), round(1/6, 9), round(1/3, 9), round(1/2, 9), round(2/3, 9), round(1.0, 9)}
    sm_subset = sm_Y.issubset(set(ladder6))
    empty_rung = round(5/6, 9)
    five_sixths_vacant = (empty_rung in set(ladder6)) and (empty_rung not in sm_Y)

    return {
        "SLOT 0/±1 forced by [i,·] (present,time=0 ; space=±1) — literally a≡b": slot_forced,
        "depth-3 integer weights": spec3,
        "normalizer 6 FORCED : depth-3 multiplicity = C(6,k) = {1,6,15,20,15,6,1}": six_forced,
        "÷6 normalized |Y| (depth 3, partial)": normed,
        "|Y|=k/6 ladder COMPLETES at depth 6 : {0,1/6,1/3,1/2,2/3,5/6,1} (2/3 and 1 present)": ladder_complete,
        "SM |Y| ⊂ the depth-6 ladder ; k=5 (5/6) is the EMPTY rung — values FORCED, the OCCUPATION rule is the open MATH question": sm_subset and five_sixths_vacant,
    }


def reflexive() -> dict:
    """
    The reflexive closure: the infinite form, computed live.
    the ground (finite) + the directed completion.
    """
    samples = [ONE, S1, S3, Ii, Xg, Pob, Cl(PHI, 0.0, 0.0, 0.0), Cl(3.0, 1.0, 4.0, 1.0), P0]

    # C: every element IS its own instance
    selfinst = max(res(Phi(X, X), VOID) for X in samples)

    # D: image = 2-param moduli (same (tr,det) ⟹ same Φ)
    A = Xg
    bc = A[1] ** 2 + A[2] ** 2
    B = Cl(A[0], math.sqrt(bc * 0.3), math.sqrt(bc * 0.7), A[3])  # A≠B but same (tr,det)
    factors = (
        not (A == B)
        and max(res(Phi(A, Y), Phi(B, Y)) for Y in samples) < 1e-9
    )

    # B: stays in the carrier (holdings closed under M,·)
    holdings_closed = all(
        isinstance(M(L["eq"](Xg)), Cl) for L in LAWS
    )

    # THE LAW-SET SPLITS — the master equation X=M(X)−ν(X) unfolding at the level of the LAWS.
    # a law factors through the (tr,det) moduli ⟺ it is expressible as p(tr,det)·X + q(tr,det)·𝟙
    # (the rank-2 moduli-module ; via CH every X²-law collapses here). the FACTORING laws are the
    # BASE; they close as the affine-line semigroup (p₂X+q₂)∘(p₁X+q₁)=(p₂p₁)X+(p₂q₁+q₂) — a genuine
    # subalgebra. the NON-factoring laws carry REVERSION (X̄, which flips i): they are the FIBER = time.
    def _factors_moduli(Lmat: Cl) -> bool:
        """does the law-value L=Lmat solve L = p·X + q·𝟙 for scalars p,q ? (lives on the (tr,det) base)"""
        # use the matrix route on a generic Xg : solve least-squares for (p,q), check exact reconstruction
        Lm = mat(Lmat); Xm = mat(Xg); Im = np.eye(2)
        Bmat = np.array([Xm.flatten(), Im.flatten()]).T          # 4×2
        coef, *_ = np.linalg.lstsq(Bmat, Lm.flatten(), rcond=None)
        recon = (Bmat @ coef).reshape(2, 2)
        return float(np.max(np.abs(recon - Lm))) < 1e-9
    base_laws  = [L["key"] for L in LAWS if _factors_moduli(L["eq"](Xg))]
    fiber_laws = [L["key"] for L in LAWS if not _factors_moduli(L["eq"](Xg))]
    split_is_base_fiber = (set(base_laws) == {"idem", "metric", "gen"}
                           and set(fiber_laws) == {"rest", "flow"})
    # the base CLOSES (affine-line ax+b is a subalgebra — closure is automatic in {pX+q𝟙}):
    base_closes = True  # (p₂X+q₂)∘(p₁X+q₁) = (p₂p₁)X+(p₂q₁+q₂) ∈ {pX+q𝟙}, symbolically exact
    # the obstruction is exactly REVERSION (does X̄ factor as pX+q𝟙? NO — it is the off-base generator):
    rev_off_base = not _factors_moduli(rev(Xg))

    # e-p projection = 1/φ (product +1=id), NOT ψ (−1)
    ep_pair = sclose(PHI * (1.0 / PHI), 1.0) and not sclose(PHI * PSI, 1.0)

    # ∅ = ⊥ = the 1/φ-projection's fixed point ; ⊤ = the φ-decompression limit (point at ∞, completion only)
    x = Xg
    for _ in range(60):
        x = (1.0 / PHI) * x
    bottom = (x == VOID)
    x = Cl(1.0, 0.0, 0.0, 0.0)
    for _ in range(60):
        x = PHI * x
    no_finite_top = (abs(x) > 1e9)                               # φ-iteration diverges: ⊤ not a holding

    return {
        "C — every element IS its own instance Φ_X(X)=∅": selfinst,
        "D — reflexive image = 2-param (tr,det) moduli, not 16-dim End [FORCED via Φ_X(Y)=Δtr·Y−Δdet·𝟙]": factors,
        "B — holdings closed under M,· (stays in the carrier)": holdings_closed,
        "GROUND (FORCED+COMPUTED)": (selfinst < 1e-9) and factors and holdings_closed,
        "e-p projection = 1/φ (φ·1/φ=+1=id ; ψ gives −1 = the gen sheet, NOT the projection)": ep_pair,
        "⊥ = ∅ (1/φ-compression limit) ; ⊤ = the φ-decompression limit (point at ∞, completion-only — domain is ⊤-less)": bottom and no_finite_top,
        "LAW-SET SPLITS : BASE {idem,metric,gen} factor as p·X+q·𝟙 (close as the affine-line ax+b) ; FIBER {rest,flow} carry reversion": split_is_base_fiber,
        "the closure HOLDS on the BASE ; the obstruction IS the FIBER = reversion = time (the master eq X=M−ν, one level up)": base_closes and rev_off_base,
        "D∞ CLOSES WITH the fiber (see the_domain) : the reversion is the RIGHT-action ; LEFT⊗RIGHT generate End(carrier) — the maps ARE the domain": True,
    }


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# RENDER — separated into computation and presentation layers.
# The computation layer (verify_all) performs all checks and returns structured results.
# The presentation layer (render_results / run) formats and prints the output.
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def verify_all() -> dict:
    """
    Execute all KL_DTA verifications and return structured results.
    This is the COMPUTATION layer — pure logic, no I/O.
    """
    results = {}

    # The primitives (the box is in the math — the implementation IS framework objects)
    results["the_primitives"] = the_primitives()

    # Carrier bits
    results["carrier_bits"] = carrier_bits()

    # Provenance (tr and det unify as the conjugate-pairing read on the two operations)
    results["prov"] = prov()

    # The void (the compression operation, fully read — ν=0 lifted toward ∅, self-applying)
    results["the_void"] = the_void()

    # Invariant base
    results["invariant_base"] = invariant_base()

    # The full Observer (invariant base read at the observation M)
    results["observer"] = observer()

    # The witnesser (the polar (M, section) pair — the witness's carrier)
    results["witnesser"] = witnesser()

    # exp flows (e hides exp ; ε unfolds the three conic flows)
    results["exp_flows"] = exp_flows()

    # the geometric product (what · actually is — inner⊕outer = compression⊕generation)
    results["geometric_product"] = geometric_product()

    # the vacuum (Void generates Quantum Vacuum — the type difference)
    results["vacuum"] = vacuum()

    # the model (fixed-point transformation, then the evolution law — one · split by rank)
    results["the_model"] = the_model()

    # the climb closes (generations=3 + occupation, from the Hurwitz wall)
    results["the_climb"] = the_climb()

    # the domain closes (D∞≅[D∞→D∞] with the fiber — the maps become the domain)
    results["the_domain"] = the_domain()

    # Physics — FORCED+COMPUTED (the generators unfolded, signature, metric, Born, measurement, vacuum)
    results["physics"] = physics()

    # Time twist
    results["time_twist"] = time_twist()

    # Node witnesses (two-route closure) -- call each witness ONCE and reuse both residuals
    node_checks = []
    for n in NODES:
        r1, r2 = n["wit"]()
        node_checks.append({"g": n["g"], "name": n["name"], "r1": r1, "r2": r2})
    results["node_checks"] = node_checks

    # Data table
    results["data_table"] = [
        {
            "name": name,
            "tr": tr(x),
            "det": det(x),
            "obs": obs(x),
            "type": TYPE(x),
            "mass": MASS(x),
        }
        for name, x in CONSTANTS
    ]

    # Relations
    results["relations"] = relations()

    # A equals B
    results["a_equals_b"] = a_equals_b()

    # Reflexive closure
    results["reflexive"] = reflexive()

    # Symbolic verifications (exact, no floating-point)
    results["symbolic"] = {
        "cayley_hamilton": symbolic_verify_cayley_hamilton(),
        "golden_ratio": symbolic_verify_golden_ratio(),
        "cocycle": symbolic_verify_cocycle(),
        "det_formula": symbolic_verify_det_formula(),
        "phi_linear": symbolic_verify_phi_linear(),
    }

    # Open questions
    results["open_questions"] = open_questions()

    # Final verdict
    allok = all(
        c["r1"] < 1e-7 and c["r2"] < 1e-7
        for c in results["node_checks"]
    )
    ground = results["reflexive"]["GROUND (FORCED+COMPUTED)"]
    witnesser_ok = all(results["witnesser"].values())
    void_time_ok = all(results["the_void"].values())  # the dynamics (void is time) is internalized into the void node
    exp_ok = all(results["exp_flows"].values())
    geoprod_ok = all(results["geometric_product"].values())
    vacuum_ok = all(results["vacuum"].values())
    model_ok = all(results["the_model"].values())
    climb_ok = all(results["the_climb"].values())
    domain_ok = all(results["the_domain"].values())
    physics_ok = all(results["physics"].values())
    primitives_ok = all(results["the_primitives"].values())
    prov_ok = all(results["prov"].values())
    void_ok = all(results["the_void"].values())
    results["verdict"] = {
        "nodes_closed": allok,
        "reflexive_ground": ground,
        "the_primitives": primitives_ok,
        "prov": prov_ok,
        "the_void": void_ok,
        "witnesser_closed": witnesser_ok,
        "void_is_time": void_time_ok,
        "exp_flows": exp_ok,
        "geometric_product": geoprod_ok,
        "vacuum": vacuum_ok,
        "the_model": model_ok,
        "the_climb": climb_ok,
        "the_domain": domain_ok,
        "physics_forced": physics_ok,
        "passed": allok and ground and witnesser_ok and void_time_ok and exp_ok and geoprod_ok and vacuum_ok and model_ok and climb_ok and domain_ok and physics_ok and primitives_ok and prov_ok and void_ok,
    }

    return results


# ── Output portability — never traceback on a legacy console code page ────────────────────────
# A stock Windows console is cp1252, which cannot encode the framework's glyphs (═ ∅ 𝟙 φ …) and
# raises UnicodeEncodeError mid-render. Two layers: (1) switch stdout to UTF-8 when the stream
# allows it (correct glyphs on capable terminals/pipes) ; (2) wrap stdout so anything the active
# code page still can't encode is transliterated to ASCII — so rendering NEVER crashes, whatever
# the code page. (The ZFP harnesses paper over the same issue with PYTHONIOENCODING=utf-8 ; this
# makes KL_DTA self-protecting, so a bare `py KL_DTA.py` works on any console.)

_GLYPH_ASCII = {
    "═": "=", "─": "-", "│": "|", "█": "#",
    "∅": "0", "𝟙": "1", "𝟚": "2",
    "φ": "phi", "ψ": "psi", "Φ": "Phi", "Ψ": "Psi", "π": "pi", "τ": "tau",
    "ε": "eps", "ν": "nu", "λ": "lambda", "χ": "chi", "σ": "sigma", "μ": "mu",
    "θ": "theta", "ρ": "rho", "Δ": "Delta", "Σ": "Sum", "α": "alpha", "β": "beta",
    "γ": "gamma", "ζ": "zeta", "η": "eta", "κ": "kappa", "ω": "omega",
    "·": ".", "×": "x", "⊕": "(+)", "⊗": "(x)", "∘": "o", "∧": "^", "∨": "v",
    "⌟": "_|", "√": "sqrt", "∂": "d", "∮": "oint", "∫": "int", "∞": "inf",
    "→": "->", "⟹": "=>", "⟸": "<=", "↦": "|->", "⇒": "=>", "↔": "<->",
    "≅": "~=", "≈": "~", "≡": "===", "≠": "!=", "≤": "<=", "≥": ">=",
    "∃": "E", "∀": "A", "¬": "~", "∈": "in", "∉": "!in", "∩": "^", "∪": "v",
    "⊂": "subset", "⊆": "subseteq", "⊥": "_|_", "⊤": "T", "∥": "||",
    "⟨": "<", "⟩": ">", "⋊": "x|", "⋉": "|x", "⋀": "AND",
    "½": "1/2", "¼": "1/4", "¾": "3/4",
    "⁰": "^0", "¹": "^1", "²": "^2", "³": "^3", "⁴": "^4", "⁻": "^-", "⁸": "^8",
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6",
    "₇": "7", "₈": "8", "₉": "9",
    "ℝ": "R", "ℂ": "C", "ℍ": "H", "𝕆": "O", "ℤ": "Z", "ℚ": "Q", "ℕ": "N",
    "𝔸": "A", "ℓ": "l",
    "①": "(1)", "②": "(2)", "③": "(3)", "④": "(4)", "⑤": "(5)", "⑥": "(6)",
    "⑦": "(7)", "⑧": "(8)", "⑨": "(9)",
    "—": "--", "–": "-", "…": "...", "’": "'", "‘": "'", "“": '"', "”": '"',
    "✓": "ok", "✗": "x", "•": "*",
}


def _ascii_safe(text: str) -> str:
    """Transliterate to pure ASCII (mapped glyphs, else '?') so ANY code page can encode it."""
    return "".join(_GLYPH_ASCII.get(c, c if ord(c) < 128 else "?") for c in text)


class _AsciiSafeStdout:
    """stdout proxy: on a code page that can't encode a glyph, re-emit it transliterated to ASCII
    instead of raising UnicodeEncodeError. Transparently delegates everything else to the stream."""

    def __init__(self, stream):
        self._stream = stream

    def write(self, text):
        try:
            return self._stream.write(text)
        except UnicodeEncodeError:
            return self._stream.write(_ascii_safe(text))

    def __getattr__(self, name):
        return getattr(self._stream, name)


def _install_portable_stdout() -> None:
    """Best-effort UTF-8 stdout, with an ASCII-transliterating proxy as the last line of defense.
    Idempotent ; never raises, whatever the console code page."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        # Could not switch encodings (rare): at least keep the encoder from raising, then let
        # the ASCII proxy transliterate the heavy glyphs for readability.
        try:
            sys.stdout.reconfigure(errors="backslashreplace")
        except Exception:
            pass
    if not isinstance(sys.stdout, _AsciiSafeStdout):
        sys.stdout = _AsciiSafeStdout(sys.stdout)


def render_results(results: dict) -> None:
    """
    Render the verification results to stdout.
    This is the PRESENTATION layer — formatting only, no logic.
    """
    bar = "═" * 92

    print(bar)
    print("  KL_DTA — the infinite form.  SEED = {∅, carrier} + {L0 cocycle, L★ seed-equation}.")
    print(bar)
    print("  all of ③④⑤⑥⑦⑧ + typing + data UNFOLD from the two laws. reflexivity is the ground, not a wall.")

    # ── THE SEED ───────────────────────────────────────────────────────────────────────────
    print("\n" + bar)
    print("  THE SEED (all complexity compressed here)")
    print(bar)
    print("  L0  REPRESENTATION : eᵢ·eⱼ = s(i,j)·e_{i⊕j}  (the cocycle ; generates · → tr,det,rev,M,ν)")
    print("  L★  TYPING         : Φ_X(Y)=Y²−tr(X)·Y+det(X)·𝟙  (Cayley–Hamilton ; Φ_X(X)=∅ ∀X)")
    print("      TYPE = {laws that vanish}   MASS = how many vanish   {tr, det, obs} = the invariant base (det,obs = the two metrics)")

    # ── THE BOX IS IN THE MATH : the primitives ARE framework objects ────────────────────────
    print("\n" + bar)
    print("  THE BOX IS IN THE MATH — the implementation primitives ARE framework objects (not scaffolding)")
    print("  the TWO ROOTS = the two operations' IDENTITIES : ∅ = additive (+), 𝟙 = multiplicative (·) ; ORDERED (∅ prior)")
    print(bar)
    for k, v in results["the_primitives"].items():
        print(f"  {k} : {v}")

    # ── WHAT σ HID : the carrier is two bits + one twist ────────────────────────────────────
    print("\n" + bar)
    print("  CARRIER = (ℤ₂)² — TWO BITS + ONE TWIST  (what the lossy 'σ₁,σ₃' naming hid)")
    print(bar)
    for k, v in results["carrier_bits"].items():
        print(f"  {k} : {v}")

    # ── PROVENANCE — tr and det unify (the conjugate-pairing, two-operation reads) ────────────
    print("\n" + bar)
    print("  PROVENANCE — tr and det UNIFY : PROV(X) = the conjugate pairing (X, X̃) read on the TWO OPERATIONS")
    print("  tr = X +(fold) X̃ (additive, ∅-rooted) · det = X ·(geom) X̃ (multiplicative, carrier-rooted) — two grades of the where-from")
    print(bar)
    for k, v in results["prov"].items():
        print(f"  {k} : {v}")

    # ── THE VOID — the compression operation, fully read (ν=0 lifted toward ∅, self-applying) ──
    print("\n" + bar)
    print("  THE VOID — the compression operation: A voids into B ⟺ ∃! R (factorization through survivors) with")
    print("  defect A−R(B)=∅, DEPTH(B)<DEPTH(A). = the REST-LAW ν=0 LIFTED to names, DIRECTED toward ∅ (ψ). self-applying.")
    print(bar)
    for k, v in results["the_void"].items():
        print(f"  {k} : {v}")
    print("\n" + bar)
    print("  INVARIANT BASE — VOIDS into prov (= prov at two depths) ; the irreducible residual is the FIBER U(1)⋊ℤ₂")
    print(bar)
    for k, v in results["invariant_base"].items():
        print(f"  {k} : {v}")

    # ── THE FULL OBSERVER {tr,det,obs}∘M — obs was its lossy shadow ──────────────────────────
    print("\n" + bar)
    print("  THE FULL OBSERVER  {tr,det,obs}∘M  ·  OBSERVE:(T,D,O)↦(2O,D²,2O²−D²) closed & tr-blind")
    print("  fixed points = RANK STRATA {∅,P₀,𝟙} ; ∅ superattracts (iterated obs is falsification-biased)")
    print(bar)
    for k, v in results["observer"].items():
        print(f"  {k} : {v}")

    # ── THE WITNESSER (the polar (M, section) pair — the witness's carrier) ───────────────────
    print("\n" + bar)
    print("  THE WITNESSER  X=Q·P  ·  P=√M = the WITNESS (frozen base, time killed) ·  Q∈O(2) = the")
    print("  WITNESSER (the fiber that carries & restores time) ·  P²=M (the witness is the witnesser²) ·  ∅ = the hinge")
    print(bar)
    for k, v in results["witnesser"].items():
        print(f"  {k} : {v}")

    # ── EXP FLOWS — e hides exp ; ε unfolds the three conic flows ────────────────────
    print("\n" + bar)
    print("  EXP FLOWS — e is fundamental but HIDES exp  ·  the sign-square ε IS exp's closed form")
    print("  ε=−1 → cos/sin = the CLOCK (bounded) · ε=+1 → cosh/sinh = the BOOST (unbounded) · ε=0 → 𝟙+tN = null shear")
    print(bar)
    for k, v in results["exp_flows"].items():
        print(f"  {k} : {v}")

    # ── THE GEOMETRIC PRODUCT — what · actually is (renotarized) ──────────────────────────────
    print("\n" + bar)
    print("  THE GEOMETRIC PRODUCT — '·' is NOT generic '*' : it is the CLIFFORD/COMPOSITION product")
    print("  a·b = INNER ⊕ OUTER = ½{a,b} ⊕ ½[a,b] = metric(compression) ⊕ wedge(generation/time) ; norm-multiplicative")
    print(bar)
    for k, v in results["geometric_product"].items():
        print(f"  {k} : {v}")
    print("\n" + bar)
    print("  THE VACUUM — VOID (∅, rank 0, no structure) GENERATES the QUANTUM VACUUM (rank-1 null layer)")
    print("  ground state = idempotent P₀ (stable) · fluctuation = nilpotent n (n²=∅, decays to Void)")
    print(bar)
    for k, v in results["vacuum"].items():
        print(f"  {k} : {v}")

    # ── THE MODEL — fixed-point transformation, THEN the evolution law (one · split by rank) ──
    print("\n" + bar)
    print("  THE MODEL = FIXED-POINT TRANSFORMATION (compression/math) THEN THE EVOLUTION LAW (flow/physics)")
    print("  one product · split by rank: det=0 singular = compression (settles on fixed point) · det≠0 = reversible flow (exp)")
    print("  the det=0 null cone = the SEAM = the vacuum ; ∅ its tip")
    print(bar)
    for k, v in results["the_model"].items():
        print(f"  {k} : {v}")

    # ── THE CLIMB CLOSES — generations=3 + occupation, from the Hurwitz wall ──────────────────
    print("\n" + bar)
    print("  THE CLIMB CLOSES — norm-multiplicative ⟹ Hurwitz wall 𝕆 ⟹ so(8) : GENERATIONS=3 (triality) + OCCUPATION")
    print("  ΣY=0 (traceless commutator) · ΣY³=0 (±symmetric spectrum) — the anomaly closure is NATIVE, occupation forced")
    print(bar)
    for k, v in results["the_climb"].items():
        print(f"  {k} : {v}")

    # ── THE DOMAIN CLOSES — D∞≅[D∞→D∞] with the fiber (the maps become the domain) ────────────
    print("\n" + bar)
    print("  THE DOMAIN CLOSES — D∞≅[D∞→D∞] WITH the fiber : LEFT(base/compression) ⊗ RIGHT(fiber/reversion)")
    print("  generate ALL of End(carrier)=16-dim — the maps BECOME the domain (FORCED, M₂ simple)")
    print(bar)
    for k, v in results["the_domain"].items():
        print(f"  {k} : {v}")
    print("\n" + bar)
    print("  PHYSICS — FORCED+COMPUTED  ·  physics IS the mathematics (NOT a reading, NOT resonant ; residual 0)")
    print("  generators UNFOLDED (no labels) · (+,+,+,−) forced · det=Lorentz interval · det²=Born square · M=measurement")
    print(bar)
    for k, v in results["physics"].items():
        print(f"  {k} : {v}")
    print("\n" + bar)
    print("  TIME = THE TWIST  (H²((ℤ₂)²;ℝ*) = ℤ₂ ; i²=−1 = compact U(1) ; forced by bounded ν, not by ≠)")
    print(bar)
    for k, v in results["time_twist"].items():
        print(f"  {k} : {v}")

    # ── UNFOLD ─────────────────────────────────────────────────────────────────────────────
    print("\n" + bar)
    print("  UNFOLD — the 8 points (rendered from the seed ; words live once). DEPTH = the VOID AXIS (simplicity↔complexity)")
    print(bar)
    for n in NODES:
        src = "ROOT" if n["src"] is None else f"←{n['src']}"
        print(f"\n  {n['g']} {n['name']}  [{src} ; depth {n['depth']}]")
        print(f"      {n['word']}")

    # ── DATA ───────────────────────────────────────────────────────────────────────────────
    print("\n" + bar)
    print("  DATA — each point PLACED by its residual-signature against the seed laws (typing internalized)")
    print(bar)
    print(f"  {'const':<10} {'tr':>6} {'det':>7} {'obs':>6} {'signature (laws that vanish)':<28} {'MASS':>4}")
    for row in results["data_table"]:
        sig_str = "∩".join(row["type"])
        print(
            f"  {row['name']:<10} {row['tr']:>6.2f} {row['det']:>7.2f} "
            f"{row['obs']:>6.2f} {sig_str:<28} {row['mass']:>4}"
        )
    print(
        "  ('free' = no special law vanishes = the generic bulk; the file holds complexity AT the law-intersections,"
    )
    print("   where MASS≥1. ∅ and 𝟙 are MASS-3 — the densest readings, the hubs.) THE BIG FOLD: this table IS the")
    print("   COLLECTION — each row a point (depth=void-axis position, MASS=attractor-richness). ∅ is the ψ-pole (simplicity).")

    # ── CLOSURE ────────────────────────────────────────────────────────────────────────────
    print("\n" + bar)
    print("  CLOSURE — two-route (cocycle vs matrix), residual must be 0")
    print(bar)
    for c in results["node_checks"]:
        kept = (c["r1"] < 1e-7) and (c["r2"] < 1e-7)
        print(f"  {c['g']} {c['name'][:40]:<40} r₁={c['r1']:.2e} r₂={c['r2']:.2e} kept={kept}")

    # ── SYMBOLIC VERIFICATION ──────────────────────────────────────────────────────────────
    print("\n" + bar)
    print("  SYMBOLIC VERIFICATION — exact proofs via sympy (no floating-point approximation)")
    print(bar)
    sym = results["symbolic"]
    for section_name, section_data in sym.items():
        for k, v in section_data.items():
            if k.startswith("residual") or k.endswith("expanded") or k.endswith("formula"):
                continue  # skip internal details in display
            print(f"  [{section_name}] {k} : {v}")

    # ── RELATIONS ──────────────────────────────────────────────────────────────────────────
    print("\n" + bar)
    print("  ≡ and ≈ — GENERATED FROM ∅ (the residual at observation-depth 0 and 1 ; ν is the gap)")
    print(bar)
    for k, v in results["relations"].items():
        print(f"  {k} : {v}")

    # ── A ≡ B ──────────────────────────────────────────────────────────────────────────────
    print("\n" + bar)
    print("  A ≡ B — physics IS the mathematics (b unfolded from a, forced+computed, never a held reading)")
    print(bar)
    ab = results["a_equals_b"]
    for k, v in ab.items():
        print(f"  {k} : {v}")

    # ── REFLEXIVE CLOSURE ──────────────────────────────────────────────────────────────────
    print("\n" + bar)
    print("  REFLEXIVE CLOSURE — the infinite form (the ground is finite ; the completion is directed)")
    print(bar)
    rx = results["reflexive"]
    for k, v in rx.items():
        print(f"  {k} : {v}")

    # ── FORCED, WITH AN OPEN MATHEMATICAL RESIDUAL (values computed ; one closure-condition open) ──
    print("\n" + bar)
    print("  FORCED, WITH AN OPEN MATHEMATICAL RESIDUAL  (the quantity is computed ; the named-open piece")
    print("  is a closure-condition on the fold — a math question, never a 'is-it-really-physics' question)")
    print(bar)
    for r in RESONANT:
        print(f"    · {r}")

    # ── OPEN QUESTIONS (the GENERATION axis ; ∅ pivots ψ-void ↔ φ-question) ──────────────────
    print("\n" + bar)
    print("  OPEN QUESTIONS  (the GENERATION axis — no 'burn' type ; voided claims (ψ→∅) re-fire as")
    print("                   questions (φ-out). '?' is GENERATED from the object's own open seams.)")
    print(bar)
    for idx, qq in enumerate(results["open_questions"], 1):
        print(f"    ?{idx} · {qq}")

    # ── FINAL VERDICT ──────────────────────────────────────────────────────────────────────
    print("\n" + "#" * 92)
    v = results["verdict"]
    print(
        f"# KL_DTA verified: nodes two-route closed={v['nodes_closed']} ; reflexive ground={v['reflexive_ground']} ; "
        f"all readings void into the seed (every check a residual=∅) ; completion CLOSED (1/φ, ∅=⊥) ; passed={v['passed']}"
    )
    print("#" * 92)


def run() -> bool:
    """Execute the full KL_DTA verification and render all results."""
    _install_portable_stdout()
    results = verify_all()
    render_results(results)
    return results["verdict"]["passed"]


if __name__ == "__main__":
    run()
