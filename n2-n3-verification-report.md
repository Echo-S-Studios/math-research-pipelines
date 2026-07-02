# Verification Report — N2 + N3 Box Extensions (bundle rev 2, "filesfixed")

Independent re-verification of the N2 ([−3,3]⁵ quintic Pisot census + C2 scans)
and N3 ({−2..2}⁶ degree-12 Salem census) claims, executed 2026-07-02. Covers
`files.zip` (rev 1) and the superseding `filesfixed.zip` (rev 2), plus an
adversarial mathematical review of every `[FORCED]` certificate in the drivers
(15 agents: 5 referees + 10 skeptic verifiers).

## 1. Integrity

| artifact | SHA-256 | manifests |
|---|---|---|
| `files.zip` (rev 1) | `ff37134c…845d80b8a` | 3/3 manifests, 18/18 files OK |
| `filesfixed.zip` (rev 2) | `8432455c…362ed3a1` | 5/5 manifests OK (top-level pins component manifests + README + RUNBOOK) |

Rev-1 → rev-2 delta verified byte-for-byte: **all 17 shared authoring-session
files identical**; only `pisot83.jsonl` re-pinned (`7c5df8c5…` → `aeff3c3d…`),
and the new pin is **byte-identical to the regeneration this session produced
from the pinned generator before rev 2 arrived** — the re-pin is exactly right.
The rev-1 provenance seam (a `certs` field the pinned generator does not emit)
is fully explained: the old pin was the [−2,2]⁵ restriction of
`pisot_n2.jsonl`, row-for-row, all fields (verified).

## 2. Environment

Ubuntu 24.04.4 LTS · Python 3.11.15 · sympy 1.14.0 · PARI/GP 2.15.4.
(The bundle asks for Python 3.12; under 3.11.15 every artifact nevertheless
regenerated to its pin — no versioning signal observed.)

## 3. Execution results

`bash RUNBOOK.sh` → **`RUNBOOK: ALL GREEN`, exit 0** (~6 min). Every driver
also ran standalone from scratch in this session before rev 2 arrived, with
identical results. Regeneration determinism: `pisot83.jsonl`,
`pisot_n2.jsonl`, `empty_adjudication.jsonl` **byte-identical** to pins;
`n1_c2_scan.jsonl`, `n2_c2_scan.jsonl`, `n3_census.jsonl` identical minus the
`secs` timing field (including the per-instance `c2_sha` values).

| suite | result | evidence |
|---|---|---|
| N1 stage A | PASS | `PISOT 83 two-pair 67 mixed 16 … -> MATCH`, `dual_path_mismatch: 0` |
| N1 C2 scans | PASS | `clean {Phi1^20, det=2} verdicts this run: 67/67` |
| N1 symbolic H3 | PASS | deg-400 symbolic resultant vs Newton route: `IDENTICAL` (7.6 s) |
| GP spot deck | PASS | stdout byte-identical to pinned transcript; stderr = only the benign `parisize` line (H2) |
| N2 census | PASS | `431/313/118 reproduced; sub-box 83/67 MATCH` (hard assert), artifact byte-identical |
| N2 chain audit | PASS | `candidates (c0 != 0): 14406`, `empty chains: 2602`, **`0 cross-path disagreements`** |
| N2 adjudication | PASS | `{"total": 2602, "reducible": 2594, "interior_ne_4": 8, "pisot_found": 0}` → `ADJUDICATION CLEAN … the 431/313 census is complete [COMPUTED]` |
| N2 C2 scans | PASS | 313/313: m₁=20, m₂=0, higher=[], detector=2 (detector 6 count: 0); dual-path asserts held; 206.6 s scan time here |
| N3 census | PASS | `{"classes": 7875, "straddle_fail": 6548, "straddle_pass_reducible": 738, "salem": 589}`; `REGRESSION sub-box: 378/37/37 -> MATCH`; `inert verdicts {Phi1^12}: 589/589` (46 s here) |

Independent cross-checks performed by this session (not merely reruns):

- **Empty-chain audit by a second exact method.** Before rev 2 arrived I wrote
  an independent adjudicator (λ-sandwich: Schur-Cohn on P(λx) at rational
  λ = (2ᵏ∓1)/2ᵏ straddling 1, after a per-instance proof of no unimodular
  roots). Result: 2602 empty chains, 8 irreducible, **0 Pisot, 0 unresolved**
  — and the 8 interior counts (2,3,2,3,2,3,2,3) match rev 2's pinned
  `empty_adjudication.jsonl` (CRootOf rational enclosures) **instance-for-
  instance**. Two independent exact methods, identical verdicts.
- **N1-overlap**: the 67 sub-box rows of `n2_c2_scan.jsonl` match
  `n1_c2_scan.jsonl` row-for-row in order and in every scan field (verified —
  no shipped script enforces this; see finding F6).
- **Burnside pieces**: 125 twist-fixed vectors and 7875 classes re-derived
  independently; sub-box 378 = (729+27)/2.
- **Partition closure**: 862 (chain={4}) + 10 942 (cert≠4) + 2602 (empty)
  = 14 406 = all c₀≠0 candidates; 6548 + 738 + 589 = 7875.

## 4. Claim checklist (the N2/N3 results tables)

| claim | verdict |
|---|---|
| N2 census 16 807 → 431 / 313 / 118, exact | ✅ (hard-asserted, byte-identical artifact; soundness of accepted⇒Pisot referee-confirmed airtight) |
| Blaschke-shift resolution of 2602 empty-chain: 8 irreducible, 0 Pisot, 0 unresolved | ✅ substance, by two independent exact methods (rev 2 ships enclosures, not Blaschke shifts; rev 1 shipped nothing — gap now closed) |
| Regression [−2,2]⁵ = 83/67/16 | ✅ (also reproduced by a referee's fully SC/Routh-free independent census, entry-for-entry) |
| 313/313 → {Φ₁²⁰}, detector = 2 all, m₂ = 0, dual-paths held (154 s) | ✅ (206.6 s on this hardware) |
| N1-overlap 67/67 row-for-row | ✅ (verified here; not enforced by any shipped script) |
| No merged-shell two-pair quintic in [−3,3]⁵ | ✅ **conclusion true, cited evidence wrong** — see F3: "detector never returned 6" is vacuous (6 is unreachable); the correct certificate is det=2 ∧ m₂=0 ∧ higher=[] ∧ zero detector crashes |
| N3 15 625 → 125 → 7875 (Burnside) | ✅ (hard assert + independent re-derivation) |
| N3 cascade 6548 / 738 / 589 | ✅ reproduced exactly (print-only tallies; RUNBOOK now greps them) |
| N3 regression 378/37/37 | ✅ MATCH |
| N3 589/589 → {Φ₁¹²}, Φ₂ impossibility asserts held (33 s) | ✅ (46 s here; m₂=0 hard-asserted per instance, and the Φ₂⇒P-even⇒non-Salem argument referee-confirmed) |
| Thm 7.13 corroboration base 37 → 589, zero falsifiers | ✅ |
| Conj. 9.1 unfalsified across 313 two-pair quintics at [−3,3]⁵ | ✅ |

## 5. Adversarial review — confirmed findings

15-agent review of every `[FORCED]` claim in `stage_a_certify.py`,
`n2_stage_a.py`, `stage_bc.py`, `n3_census.py`. The exact-arithmetic core was
confirmed SOUND across the board (Schur-Cohn strict-Rouché exactness incl. the
a₀=0 sublevel case; Routh/Möbius mapping with both guards; the B1/B2 resultant
identity; the Newton route and p_k(Rat)=p_k(C2)²; the eval dual-path identity;
straddle⇔Salem incl. endpoint analysis; Burnside; the C6 sieve). Nine findings
survived dedicated skeptic verification (one was refuted). None falsifies a
numerical result; all are proof-structure / documentation defects:

- **F1 (GAP, stage A census completeness).** The [−2,2]⁵ chain silently drops
  622 both-degenerate candidates (conflated inside `sc_degenerate=1754`), and
  65/83 accepted Pisots (all |c₀|=1 units, where SC's δ₁=c₀²−1=0) rest solely
  on unproven Routh regularity; 4 of the 622 are irreducible with provably
  zero circle roots, so joint degeneracy carries no circle-root information.
  *Closed for this box*: the 622 are exactly the [−2,2]⁵ empties in
  `empty_adjudication.jsonl` (all non-Pisot), and an SC/Routh-free independent
  census reproduces `pisot83.jsonl` entry-for-entry.
- **F2 (UNSOUND, "4-path chain" independence).** SC(−P(−z)) ≡ SC(P) (identical
  δ-sequences) and RH(−P(−z)) ≡ RH(P) (mobius_q(neg) = rev(mobius_q(P));
  routh_lhp already tries both orders) — 0 exceptions across all 14 406
  candidates, exactly matching the audit's degeneracy tallies (SC 7748 = SCneg
  7748, RH 2604 = RHneg 2604). Chains have length 0/2/3, never 1; the
  `len(certs) >= 2` assert is vacuous; 263/431 rows (262 RH+RHneg, 1 SC+SCneg
  at c=(−2,1,1,−2,−3)) carry two labels but ONE independent method. Result
  unaffected (one exact path suffices; all 431 independently re-verified).
- **F3 (UNSOUND, shell-detector semantics).** The documented `{2,6}` dichotomy
  ("6 ⇔ merged") is false: sympy Sturm counts are distinct-root counts, and in
  a merged shell the 12 unimodular ratios provably collapse to ≤ 4 distinct
  t-values (2cos(φ₁±φ₂) are double roots of D) — 6 is unreachable dead code; a
  generic merged instance crashes the `{2,6}` assert LOUDLY (demonstrated),
  and a torsion-merged instance (ratios roots of unity) returns detector=2
  SILENTLY (demonstrated) — it is caught only by Φ_M content in the C6 scan.
  Corrected certificate used in §4 above: detector=2 ∧ m₂=0 ∧ higher=[] ∧ no
  crashes ⇒ distinct shells (collapse-to-2 requires ≥2 integer angle
  relations ⇒ torsion ⇒ cyclotomic content ⇒ caught). All 313 instances
  satisfy it; shells spot-checked genuinely distinct.
- **F4 (UNSOUND, N3 twist exclusivity).** "The two class members cannot both
  straddle" is false as stated: 160/7875 classes both-straddle via the
  closed-interval endpoint (T(±2)=0 ⇔ P(±1)=0). Provably the only escape, so
  all 160 are reducible and the Salem tally is unaffected; the true lemma is
  "both straddle ⇒ reducible".
- **F5 (GAP, rev 1 only).** The Blaschke audit `n2_chain_audit.py` was never
  shipped — 2602/14 406 candidates unadjudicated in rev 1. Closed in rev 2
  (`my_chain_audit.py` + `empty_adjudicate.py`, exit-code-coupled) and
  independently here (§3).
- **F6 (GAP).** N1-overlap 67/67 is asserted by no shipped script (verified
  true here).
- **F7 (GAP).** N3 cascade tallies and the sub-box MATCH line are print-only
  (the RUNBOOK's greps now gate them; a driver-level assert would be
  stronger).
- **F8 (GAP).** `totient_table` asserts 2φ(M)² ≥ M only up to 320 000;
  completeness of the torsion-candidate list beyond the table relies on the
  classical φ(n) ≥ √(n/2) — true, standard, but not verified in-run despite
  the docstring's "verified bound".
- **F9 (refuted finding, recorded for completeness).** "313/313 scan verdicts
  are never asserted by the N2 driver" was raised and then refuted as
  immaterial: the per-instance identities are hard-asserted inside
  `stage_bc`'s functions, and the recorded fields the claim cites were
  independently verified here.

## 6. Deviations

None at the execution level: every rerun matched its pin, every gate passed,
exit codes 0 throughout, no non-benign `***` GP stderr. The findings above are
wording/proof-structure corrections for the whitepaper's next revision, not
computational failures. **H4 (background-process reaping) did not reproduce in
this container**: five long-running harness-tracked background tasks (up to
15 min) all survived to completion; treat H4 as environment-specific rather
than binding for this container class.

## 7. Verdict

**All N2 and N3 numerical claims verified**, including full artifact-level
regeneration determinism, and the census-completeness gap of rev 1 is now
closed twice over (rev 2's enclosure adjudication + this session's independent
λ-sandwich audit, agreeing instance-for-instance). Both box extensions stand:
[−3,3]⁵ contains exactly 431 Pisot quintics (313 two-pair, 118 mixed), all 313
C2 scans are inert with distinct shells; {−2..2}⁶ contains exactly 589 Salem
twist-classes, all inert — Thm 7.13's corroboration base grows 37 → 589 with
zero falsifiers and Conj. 9.1 is unfalsified at the wider box. Two documented
`[FORCED]` statements (the detector's `{2,6}` dichotomy and N3 twist
exclusivity) are false as stated and should be reworded — with corrected
arguments supplied in F3/F4, their downstream conclusions survive unchanged.
