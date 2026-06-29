# NEXT SESSION — P2c: the non-disjoint compositum

Handoff so a **fresh session** can start P2c cleanly. P2c is the **next major build** (Ace's decision);
it begins in a new session, **not** the one that shipped A1/A2/A7. B1 (KIRA live-wire) is deferred to
its **own separate session** later. Read `README.md` + `A2_P2_DESIGN.md` first; this is the delta.

## WHAT — the non-disjoint compositum

A2.P2b grows `K → K(β)` only in the **disjoint** case (the new generator's minpoly stays irreducible
over `K`), where the trace-form Gram is the Kronecker product `G_W = G_K ⊗ G_L` (Prop 3.3). **P2c is
the non-disjoint case:** when the generator's minpoly **partially factors over `K`**, the tensor
shortcut is **INVALID** — `[K(β):K] < deg(m_β)`, so the true compositum is *smaller* than `G_K ⊗ G_L`.

The build must, exactly:
1. **Detect non-disjointness** = factor `m_β` over `K` (Trager / resultant, regime B): compute the
   minpoly of `β` **over `K`**, degree `e' = [K(β):K]`. Disjoint ⟺ `e' = deg(m_β)` (A2.P2b path);
   non-disjoint ⟺ `e' < deg(m_β)` (this path); `e' = 1` ⟺ `β ∈ K` (already-in-K, no growth).
2. **Build the TRUE compositum** `K(β)` of degree `[K:Q]·e'` — its actual basis and exact trace-form
   Gram (via a primitive element of `K(β)` and its minpoly, computed by resultant; *not* `G_K ⊗ G_L`).
3. **Re-derive** the projector exactly; the previously out-of-field element's residual → **0**.

## WHERE — the code

Extend **`compositum.py`**'s currently-REFUSED `non_disjoint` branch (in `CompositumLearner.propose`,
returns `FieldExtensionRefusal(kind="non_disjoint", ...)`) into **actual growth**. Likely shape: a
disjointness test up front (factor `m_β` over `K`); the disjoint case keeps the A2.P2b Kronecker path;
the non-disjoint case takes the new true-compositum path; `e'==1` stays the already-in-K refusal.

## CONCRETE TEST TARGET (the canonical non-disjoint witness)

`K = Q(√2)` (`G_K = diag(2,4)`), adjoin `β = √2+√3` (minpoly over Q is `x⁴−10x²+1`). Over `K=Q(√2)`
that minpoly **factors**:
```
x⁴ − 10x² + 1 = (x² + 2√2·x − 1)(x² − 2√2·x − 1)   over Q(√2)
```
so the minpoly of β **over K** is degree `e' = 2` (one quadratic factor), `β ∉ K`. True compositum
`K(β) = Q(√2,√3)`, degree `[K:Q]·e' = 2·2 = 4` — **NOT** the disjoint tensor degree `2·4 = 8`.
Test: detect non-disjoint → build the degree-4 compositum (correct basis/Gram, not `G_K ⊗ G_L`) →
β's residual → 0; witnessed. Plus the existing negatives (`e'==1` already-in-K still refused; over-cap).

## GUARDRAILS (unchanged)

Model-layer only (no `z`/KIRA/`_IC_*`/Plate-Matrices/numpy) · exact Fraction/int (G8) · monic-integer
generator (G10) · propose-for-confirm, `confirm()` the sole mutator (G2) · sha256 witness chain (G5,
record the non-disjoint extension: old→new degree, `e'`, generator minpoly, factorization) · bounded
by `HARD_DEGREE_CAP`. Additive; keep the prior 48 training tests green; gate = new P2c tests + all
training + full L00M suite + ZFP 74/74. Review leash: claim→build→result via the journal, HOLD the
commit for Ace.

## RELEVANT FILES

- `compositum.py` — the `non_disjoint` branch to extend; `CompositumLearner`, `Factor`, proposals.
- `field_extension.py` — `WorkingField` detection, `kron`, `tensor_gram`, `HARD_DEGREE_CAP`.
- `coords_to_minpoly.py` + `invariant_factors.py` — exact minpoly / SNF kernel; the basis for the
  factor-over-K computation (will likely need extension to factor over a number field, not just `Q`).
- `A2_P2_DESIGN.md` — the P2 math (Lemma 3.2 disjointness ⟺ `[KL:Q]=[K:Q][L:Q]`; Prop 3.3 Kronecker
  Gram for the **disjoint** case only; §5 hard-parts #3 names exactly this non-disjoint gap).
- `README.md`, `ROADMAP.md` — package index + the decision.
- **B1 (separate later session):** its spec is `WIRING_MAP.md` — untouched by P2c.

## PHASE → COMMIT LEDGER (state at handoff, all L00M `main`)

A1 `fea69c4` · A2.P0 `c1db881` · A2.P1 `5a80216` · A2.P2a `75524b3` · A2.P2b `c0b413f` ·
README `c90ff90` · ROADMAP `760125e` · A7 `6ad20eb` · capstone `3c61347`.

Package complete (A1+A2+A7+demo). P2c is the next build; B1 is its own later session; A3/P2d stays research.
