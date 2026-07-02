# Execution Report — N4 (degrees 6–7) + N6 (parent-paper fold)

Comprehensive execution of the two remaining N-series items, 2026-07-02.
Exact arithmetic throughout; every claim below is machine-asserted in the
committed artifacts.

## N4 — degree 6–7 Pisot censuses and cross-shell scans (`n4-degree67/`)

**Census discipline (upgraded).** The four-path certificate chain
{Schur–Cohn, Möbius–Routh} × {P(x), −P(−x)} is computed *unconditionally*, and
the degenerate-chain population is adjudicated exactly *in the same run*
(reciprocal ⇒ not Pisot; reducible ⇒ rejected; otherwise non-reciprocity
forces gcd(P, rev P) = 1, hence no unimodular roots, and a scaled Schur–Cohn
sandwich at rational radii straddling 1 pins the interior count). Zero
candidates left unadjudicated, by construction — the F1-class gap of the N2
review is closed structurally, not post hoc.

**Regression gate.** Degree 5 reproduces the archived census (83/67/16,
instance-set identical to `pisot83.jsonl`) and all 67 scans agree
field-for-field with the archived `n1_c2_scan.jsonl` (detector, m₁, m₂,
higher). New machinery validated against old before any new claim.

**Degree 6, [-2,2]⁶ (15 625).** 160 Pisot sextics: 159 two-pair with real
spectator, 1 one-pair, 0 totally real. Degenerate chains 2 950
(150 reciprocal / 2 794 reducible / 6 irreducible non-Pisot / 0 Pisot).
Scans: 160/160 Rat = {Φ₁⁶}; 159/159 live: Rat° squarefree, detector = 2
everywhere, composed-square scans exactly {Φ₁^{deg S*}}, Φ₂-multiplicity 0,
no higher content.

**Degree 7, [-2,2]⁷ (78 125).** 414 Pisot septics: **309 three-pair (the
first three-pair population)** + 105 two-pair with two real spectators.
Degenerate chains 13 598 (250 / 13 316 / 31 / **1**). The 1 is the headline
census finding: a genuine Pisot,

    x⁷ − 2x⁶ + 2x⁵ + 2x⁴ − 2x³ − x² + 1,   c = (1, −1, −2, 2, 2, −2, −2),

is invisible to all four certificate paths (c₀ = 1 degenerates Schur–Cohn at
δ₁ = c₀²−1 = 0 and both Routh tables) and was caught only by the exact
adjudication. **At degree 7 the empty-chain gap is no longer hypothetical**;
the N2-style lazy-chain semantics would have silently undercounted the
census. Scans: 414/414 Rat = {Φ₁⁷}; 414/414 live: detector = number of pairs
on every instance (309 × 3, 105 × 2 — no merged shells), all Rat°
irreducible of degree 42, composed squares of degree 1 764 scanned
completely: **{Φ₁⁴²} on all 414 — zero mirrored cross-shell classes through
degree 7**, including every pairwise ν of the three-pair pattern (each is a
product of two u's, covered by the single composed square, exactly as N4
predicted).

**P7 resolved affirmatively.** 3 sextic instances have reducible Rat°
(factor shapes 12+18, 12+18, 6+24); the qualifying product S* shrinks to
degrees 12/12/24; scans still inert. First observed non-generic-Galois
instances.

**Cross-engine.** GP deck (`n4_spot.gp`: polresultant + full factor +
poliscyclo — an independent decision path): 4/4 signatures identical to the
sympy Newton/trial-division route, including the adjudicated instance
(ratsig [[1,7]], deg S* 42, detector 2, c2sig [[1,42]]).

Runtimes: censuses 42 s; scans 415 s (deg 6) + 1 794 s wall (deg 7, four
checkpointed shards). All artifacts SHA-pinned in
`n4-degree67/MANIFEST.sha256` (13 files).

## N6 — L-series fold into the parent paper (`relational_charge_paper.l.tex`)

Applied by `fold_l_series.py` (all-or-nothing anchored patcher, J/K idiom) on
top of the K-series build:

- **L1**: the real-pair ν-reduction folded directly after the ν-criterion
  remark (compiled Rem 7.6) — real×non-real coherence decided by the Rat_p
  scan alone, no 2-part loss; inertness below two non-real shells; residue
  localized at the quintic two-pair pattern.
- **L2**: the hypothesis-necessity witness Z\* = x⁴−3x²+1 = (x²−x−1)(x²+x−1)
  folded directly after the sharpness example (compiled Ex 7.19) — isolates
  irreducibility and the disjoint-modulus clause of Thm 7.13's mixed form;
  together with x⁴−2 every hypothesis of the theorem is isolated.
- **L3**: Cor 7.16's parenthetical sharpened in place — residue location plus
  executed zero-falsifier evidence: 67 ([-2,2]⁵), 313 ([-3,3]⁵),
  159 ([-2,2]⁶), 414 ([-2,2]⁷, incl. the 309 three-pair instances).
- **L4**: bibliography entry for the session note (`\cite{pisotnote}`).

**Numbering discipline verified:** L1/L2 are unnumbered blocks (K1 precedent)
and L3 edits inside an existing environment, so the compiled numbering of
every environment is unchanged (`.aux` label diff: only page positions moved;
7.6 / 7.10 / 7.13 / 7.16 / 7.19 / 7.20 all preserved) — the session note's
citations into the parent remain valid. Build check at the archive bar:
pdflatex twice, **0 errors, 0 undefined references**, overfull count
unchanged (7), 26 pages.

## Whitepaper v1.2 (`pisot_residue_whitepaper.v12.tex`)

`fold_w_series.py` (9 anchored W-series edits): N4 subsection added to the
extensions section, N4 marked executed, P1's evidence base extended to all
573 + 380 live instances, **P7 promoted to resolved**, P8's empty range
extended, appendix runtimes added. Build: 0 errors, 0 undefined refs,
overfull unchanged (1 pre-existing), 11 pages.

## Verdict

Both remaining N-series items are executed and verified. The evidence base
for the general Pisot-inertness conjecture (P1) now spans degrees 5–7:
67 + 313 + 159 + 414 = 953 live instances (including the first 309
three-pair executions), zero falsifiers, nothing promoted. The lasting
methodological yields: unconditional adjudication is now mandatory census
discipline (a real degree-7 Pisot lives in the degenerate-chain population),
and P7's reducible-Rat° instances exist and remain inert.
