# Design notes — what the metaphors mean

This is the conceptual companion to the technical
[`matrix_plates_build_spec.md`](matrix_plates_build_spec.md). It explains the two
core metaphors — **plates** and the **companion closure** — in mathematical
terms, then shows a handful of examples where the system reveals something
genuinely interesting rather than merely running code.

---

## 1. What a "plate" is

A **plate** is an *exact integer matrix treated as a finished, reusable artifact,
graded by the entropy of its spectrum.* The metaphor is the printing/commemorative
plate: you *press* a construction (a companion, a Kronecker product, a Cartan
matrix) and out comes a fixed object whose markings — its invariants — are
engraved exactly, never approximated.

Three commitments follow from taking "plate" seriously:

* **Exactness is the point.** A plate's engraved data — characteristic
  polynomial, minimal polynomial, invariant factors, determinant, trace, rank —
  are computed in exact integer / rational arithmetic. They are facts about the
  plate, not floating-point estimates. (Only the *positions* of eigenvalues and
  the Mahler measure / house, which are transcendental in general, are floating
  point — and the engraving is explicit about which is which.)

* **The grading is entropy.** Plates are arranged by `log M`, where `M` is the
  Mahler measure of the characteristic polynomial. For a monic integer
  polynomial, `log M` is exactly the topological entropy of the associated
  toral automorphism (Lind–Schmidt–Ward). So the gallery axis is not arbitrary;
  it is the natural information-theoretic coordinate, and it is additive because
  Mahler measures multiply.

* **Two numbers, two readings.** Each plate carries both a **Mahler measure** (a
  *product*, `∏_{|λ|>1}|λ|` — total spectral entropy) and a **house** `⌈A⌉` (a
  *max*, `max|λ|` — the dominant growth rate). They answer different questions,
  and they come apart (see §3.2).

The floor of the gallery is pinned at `M = 1` — the **Kronecker floor**, attained
exactly by products of cyclotomics — so the empty space below Lehmer's number
stays visible. The emptiness is the content (§3.3).

---

## 2. What the companion closure is trying to achieve

Write `Φ = companion ∘ charpoly`: take a matrix, read its characteristic
polynomial, and build that polynomial's **companion matrix**. Three goals, each
mathematical:

### 2.1 A canonical spectral representative
`Φ(A)` is the companion (rational-canonical) form of `A`'s characteristic
polynomial — *the* matrix that has exactly `A`'s spectrum and nothing else
remembered. It strips `A` down to its char-poly and rebuilds the simplest matrix
with that char-poly. So `Φ` is a normalization: every plate has a canonical
spectral twin.

### 2.2 A retraction (idempotence)
A companion matrix's characteristic polynomial is its own defining polynomial, so
`Φ(Φ(A)) = Φ(A)`: one step reaches a fixed point. `Φ` is a **retraction** of the
space of integer matrices onto the subspace of companion matrices. "Closure" is
literal — applying the operation again changes nothing.

### 2.3 A self-extending algebra of algebraic integers
Because companion polynomials are monic, `Φ(A)` is always integral; its char-poly
defines a new algebraic integer. Feeding that polynomial back into the **seed
registry** makes the registry *closed under `Φ`*: every plate's spectrum becomes a
reusable seed for the binary operators (`⊗`, `⊕`, `[·,·]`). The system generates
its own building blocks. Deduplication by polynomial signature keeps the fixed
points from multiplying.

And the sharp lesson `Φ` exists to teach: **the characteristic polynomial is a
complete similarity invariant only for non-derogatory matrices.** For a
derogatory input, `Φ` preserves the spectrum but changes the *minimal* polynomial
and the *invariant factors*, so the output is **not similar** to the input. Equal
spectrum ⇏ same matrix up to change of basis. The minimal polynomial / invariant
factors are what decide it.

---

## 3. Examples where it gets interesting

### 3.1 Same spectrum, different matrix — `φ ⊕ φ`
`φ ⊕ φ` (two golden-ratio companion blocks) and `Φ(φ ⊕ φ) = companion((x²−x−1)²)`
share **everything spectral**: char-poly `(x²−x−1)²`, `det 1`, `tr 2`, house `φ`,
Mahler `φ²`, both unimodular. Yet they are **not similar**:

```
invariant factors(φ ⊕ φ)      = [ x²−x−1 ,  x²−x−1 ]     (two blocks)
invariant factors(companion)  = [ (x²−x−1)² ]            (one block)
minimal polynomial:  x²−x−1   (degree 2)   vs   (x²−x−1)²   (degree 4)
```

`φ ⊕ φ` is **derogatory** (the eigenvalue orbit repeats with two eigenvectors);
its companion is not. This is the whole "similarity classes" point in one pair,
and the `⊕` operator hands you the witness for free. In the Mahler-spectrum
layout they even land in the **same bin** (identical `M`) — same height on the
entropy axis, different matrix.

### 3.2 House and Mahler come apart — `√2`
The companion of `x² − 2` has eigenvalues `±√2`, **both outside** the unit circle:

```
house ⌈A⌉ = max|λ| = √2 ≈ 1.414        (one dominant mode)
Mahler  M = |√2|·|−√2| = 2             (total entropy)
```

So `M > ⌈A⌉`: the *product* sees both expanding directions, the *max* sees one.
Contrast `φ` (companion of `x²−x−1`), where only one root is outside, so house
`= Mahler = φ`. Reporting both is not redundancy; `√2` is the counterexample.

### 3.3 The Lehmer gap is empty on purpose
Pin the floor at `M = 1` and the band `(1, 1.17628)` — up to **Lehmer's number** —
is conspicuously empty for every seed family. No integer matrix's char-poly is
known to land there; whether any *can* is Lehmer's unsolved problem. The smallest
structured measure is `φ ≈ 1.618`, well clear of the gap. The visualization shades
the gap so the absence is something you *see*.

### 3.4 Derogatory ≠ defective
Two independent ways a matrix can be "degenerate," often conflated:

| Matrix | derogatory? (min-poly degree < n) | defective? (not diagonalizable) |
|---|:---:|:---:|
| `φ ⊕ φ` | **yes** (repeated invariant factor) | no (diagonalizable) |
| Jordan block `[[1,1],[0,1]]` | no (single invariant factor) | **yes** (one eigenvector) |
| `companion((x²−x−1)²)` | no | **yes** (repeated roots) |
| `2·I` | **yes** | no |

`defective` is decided exactly by whether the minimal polynomial is *squarefree*;
`derogatory` by whether it has degree `< n`. The plate engraves both.

### 3.5 Structure does not mean small — `E₈`
The `E₈` Cartan matrix is **unimodular** (`det 1`), the gram matrix of the densest
8-dimensional lattice — maximally structured. Its Mahler measure is `≈ 177.67`.
"Structured" and "small spectral entropy" are unrelated; the colloquial picture of
algebraic plates hugging `[φ, 2]` while random ones fly off is wrong (a random
`[−3,3]` plate often lands *left* of `E₈`). The robust signals are the empty
Lehmer gap and the *discreteness* of structured Mahler values — not their size.

---

## 4. Where to look in the code

| Idea | Module |
|---|---|
| plate + its engraving | `invariants.analyse`, `plates.Plate` |
| entropy grading / Lehmer floor | `histogram` |
| the closure `Φ`, self-extension, queries | `closure` |
| canonical representative / similarity | `canonical` (Smith form over `ℚ[x]`) |
| house vs Mahler | `roots`, `invariants.Analysis.house` |
| provenance / lineage of lifts | `plates.Provenance`, `Gallery.lineage` |

See `examples/phi_plus_phi.py` (§3.1) and `examples/mahler_spectrum.py` (§3.3) to
run the two flagship examples, or `matrix-plates demo` / `matrix-plates compare`.
