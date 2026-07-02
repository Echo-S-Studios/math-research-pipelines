#!/usr/bin/env python3
"""fold_y_series.py -- fold the 2026-07-02 referee errata into the pisot
whitepaper: v1.3 -> v1.4.

Edits (Y-series; referee findings E1-E3, F1-F3, plus the adopted free
irreducibility remark):
  Y1  date line: v1.4 marker
  Y2  abstract: errata changelog sentence
  Y3  E2: the degree-7 display corrected to the c-vector expansion
  Y4  E1: degree condition attached to the "reciprocal => not Pisot" rule
  Y5  E3: both-straddle count restated as 163 (3 twist-fixed + 160)
  Y6  F1: "byte-identical" qualified by the per-row timing field
  Y7  free theorem: the 862 concordant candidates are automatically
      irreducible; twist involution fixed-point-free (431+431)
  Y8  E1 numbers in the P-series subsection (7/37/103; 13 totally-real;
      twelve strict; new instance named) + F2 composition note (2662)
  Y9  P-table rows P3 and P4 updated (2662; 13/13)
  Y10 F3: files-fixed.zip naming

All-or-nothing anchors; output .v13.tex -> .v14.tex.
Usage: python3 fold_y_series.py pisot_residue_whitepaper.v13.tex
"""
import sys

E = []

E.append(("Y1", r"""\date{July 2, 2026; v1.1 (box extensions), v1.2 (degree extensions N4), and v1.3 (P-series executed in full) addenda folded same day \\ \small Session note; all computations exact, artifact manifest in Appendix~A.}""",
r"""\date{July 2, 2026; v1.1 (box extensions), v1.2 (degree extensions N4), v1.3 (P-series executed in full), and v1.4 (referee errata E1--E3) addenda folded same day \\ \small Session note; all computations exact, artifact manifest in Appendix~A.}"""))

E.append(("Y2", r"""($3$ reducible-$\Rat^{\circ}$ instances, $S^{*}$ shrinking to degrees
$12/12/24$, still inert).
\end{abstract}""",
r"""($3$ reducible-$\Rat^{\circ}$ instances, $S^{*}$ shrinking to degrees
$12/12/24$, still inert). \emph{v1.4 addendum:} the independent referee
pass's errata are folded --- E1: the degree-$2$ census is $7$, not $6$
($x^2-3x+1=\mathrm{minpoly}(\varphi^2)$ is reciprocal \emph{and} Pisot; the
``reciprocal $\Rightarrow$ not Pisot'' rule is \F\ only for degree
$\ge3$; P4 grows to $13$ instances, twelve strict $+$ the golden equality,
unfalsified); E2: the degree-$7$ display corrected to its $c$-vector; E3:
the both-straddle count is $163$ under the delivered predicate ($3$
twist-fixed $+$ $160$ two-member, all reducible). No theorem touched.
\end{abstract}"""))

E.append(("Y3", r"""\[
x^7-2x^6+2x^5+2x^4-2x^3-x^2+1\qquad c=(1,-1,-2,2,2,-2,-2),
\]""",
r"""\[
x^7-2x^6-2x^5+2x^4+2x^3-2x^2-x+1\qquad c=(1,-1,-2,2,2,-2,-2),
\]"""))

E.append(("Y4", r"""\textbf{Census, with in-run adjudication.} The four-path chain is now
computed \emph{unconditionally} and the degenerate-chain population is
adjudicated exactly in the same run (reciprocal $\Rightarrow$ not Pisot;
reducible $\Rightarrow$ rejected; otherwise $P\neq\pm\mathrm{rev}(P)$ with""",
r"""\textbf{Census, with in-run adjudication.} The four-path chain is now
computed \emph{unconditionally} and the degenerate-chain population is
adjudicated exactly in the same run (reciprocal $\Rightarrow$ not Pisot
\emph{for degree $\ge3$} --- at degree $2$ the reciprocals $x^2-kx+1$,
$k\ge3$, are Pisot, erratum E1; reducible $\Rightarrow$ rejected;
otherwise $P\neq\pm\mathrm{rev}(P)$ with"""))

E.append(("Y5", r"""over the box. Correction, pinned: the twist-exclusivity shortcut (``the two
class members cannot both straddle'') fails at Sturm endpoints --- $160$
classes both straddle, each provably with $P(\pm1)=0$, hence reducible ---
so exclusivity holds in the weaker, sufficient form ``both straddle
$\Rightarrow$ both reducible.'' \F""",
r"""over the box. Correction, pinned (count refined by the referee pass, E3):
the twist-exclusivity shortcut (``the two class members cannot both
straddle'') fails at Sturm endpoints --- $163$ classes have all their
members straddling under the delivered predicate ($3$ twist-fixed
single-member classes and $160$ two-member classes), every one provably
with $P(\pm1)=0$, hence reducible --- so exclusivity holds in the weaker,
sufficient form ``both straddle $\Rightarrow$ both reducible.'' \F"""))

E.append(("Y6", r"""Both box extensions of \S\ref{sec:next} (N2, N3) were executed post-archive
and independently re-verified end-to-end (zero-shot verification session,
2026-07-02: manifest integrity, full regeneration of every pinned artifact ---
byte-identical, also under Python~3.11.15 --- and an adversarial referee pass
over every \F-tagged certificate).""",
r"""Both box extensions of \S\ref{sec:next} (N2, N3) were executed post-archive
and independently re-verified end-to-end (zero-shot verification session,
2026-07-02: manifest integrity, full regeneration of every pinned artifact ---
byte-identical up to the per-row timing field, also under Python~3.11.15 ---
and an adversarial referee pass over every \F-tagged certificate)."""))

E.append(("Y7", r"""$\{p(x),-p(-x)\}$ collapses to \emph{two} independent methods (both
transforms commute with $x\mapsto-x$; verified with $0$ exceptions and $0$
cross-path disagreements over all $14406$ candidates), so per-instance
certificates carry at most two independent computations. \F""",
r"""$\{p(x),-p(-x)\}$ collapses to \emph{two} independent methods (both
transforms commute with $x\mapsto-x$; verified with $0$ exceptions and $0$
cross-path disagreements over all $14406$ candidates), so per-instance
certificates carry at most two independent computations. \F\ Referee
addendum, adopted: the $862$ interior-$4$-concordant candidates are
\emph{automatically irreducible} --- a proper monic factor with all roots
strictly inside the unit disk would have integer constant term of modulus
in $(0,1)$ --- and the twist involution $P\mapsto-P(-x)$ is fixed-point-free
on them ($431$ Pisot $+$ $431$ anti-Pisot), so the census cut below the
concordance is purely the Sturm gate; the irreducibility gate provably
never fires (verified $862/862$). \F"""))

E.append(("Y8", r"""execution):} the totally-real populations of the boxes $[-3,3]^{2,3,4}$
($6/5/1$ instances of $6/37/103$ Pisots; the degree-$4$ census re-derived
under the v1.2 discipline matches the archived sweep, $103=103$) and the
degree-$5$--$7$ boxes ($0$ totally real, including $[-4,4]^5$) give $12$
totally-real Pisot instances; for each, $P(\varphi)$ is evaluated exactly
in $\Z[\varphi]$ ($\varphi^2=\varphi+1$ reduction; the sign of $a+b\varphi$
decided by integer squares against $\sqrt5$), and since $\theta$ is the
unique root above $1$: $\theta>\varphi\iff P(\varphi)<0$,
$\theta=\varphi\iff P=x^2-x-1$. Result: eleven strict certificates, one
equality (exactly the golden minimal polynomial), zero falsifiers. \F\ per
instance; \C\ over the populations.""",
r"""execution):} the totally-real populations of the boxes $[-3,3]^{2,3,4}$
($7/5/1$ instances of $7/37/103$ Pisots --- the degree-$2$ count corrected
by erratum E1, whose instance $x^2-3x+1=\mathrm{minpoly}(\varphi^2)$ is
reciprocal \emph{and} Pisot; the degree-$4$ census re-derived under the
v1.2 discipline matches the archived sweep, $103=103$) and the
degree-$5$--$7$ boxes ($0$ totally real, including $[-4,4]^5$) give $13$
totally-real Pisot instances; for each, $P(\varphi)$ is evaluated exactly
in $\Z[\varphi]$ ($\varphi^2=\varphi+1$ reduction; the sign of $a+b\varphi$
decided by integer squares against $\sqrt5$), and since $\theta$ is the
unique root above $1$: $\theta>\varphi\iff P(\varphi)<0$,
$\theta=\varphi\iff P=x^2-x-1$. Result: twelve strict certificates
(including $P(\varphi)=1-\sqrt5<0$ for $\theta=\varphi^2$), one equality
(exactly the golden minimal polynomial), zero falsifiers. \F\ per
instance; \C\ over the populations."""))

E.append(("Y8b", r"""degree $20$) --- P7 witnesses now exist at degree $5$. Aggregates: P3
observed on $2661/2661$ certified Pisots across degrees $2$--$7$ and five
boxes; P1's zero-falsifier base is now $2016$ live instances. \F\ per
instance; \C\ over the ranges; nothing promoted.""",
r"""degree $20$) --- P7 witnesses now exist at degree $5$. Aggregates: P3
observed on $2662/2662$ scan executions on record (composition: $147$ at
degrees $2$--$4$ in $[-3,3]^n$; $83$ and $313$-live and $1545$ across the
three nested quintic boxes, counted per run; $160$ and $414$ at degrees
$6$--$7$); P1's zero-falsifier base is now $2016$ live instances. \F\ per
instance; \C\ over the ranges; nothing promoted."""))

E.append(("Y9a", r"""in any box extension. & \F\ (Thm.~\ref{thm:pin}; observed $2661/2661$,
degrees $2$--$7$, \S\ref{sec:pseries}) & --- (a deviation would
falsify the pinning theorem)\\""",
r"""in any box extension. & \F\ (Thm.~\ref{thm:pin}; observed $2662/2662$
scan executions, degrees $2$--$7$, \S\ref{sec:pseries}) & --- (a deviation
would falsify the pinning theorem)\\"""))

E.append(("Y9b", r"""\Op\ ($12/12$ certified exactly, equality once, \S\ref{sec:pseries}) & a
totally-real Pisot with $\theta<\varphi$ (would falsify the gap on
admissible objects)\\""",
r"""\Op\ ($13/13$ certified exactly, equality once, \S\ref{sec:pseries}) & a
totally-real Pisot with $\theta<\varphi$ (would falsify the gap on
admissible objects)\\"""))

E.append(("Y10", r"""filesfixed.zip (box-extension bundle) & 8432455c20b07e9b6c2be5987484e8b720ceb27cefdaf7add6b34a28362ed3a1\\""",
r"""files-fixed.zip (box-extension bundle) & 8432455c20b07e9b6c2be5987484e8b720ceb27cefdaf7add6b34a28362ed3a1\\"""))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    bad = [(eid, src.count(old)) for eid, old, _ in E if src.count(old) != 1]
    if bad:
        for eid, n in bad:
            print(f"ANCHOR-FAIL {eid}: found {n} occurrences (need exactly 1).")
        sys.exit(1)
    out = src
    for eid, old, new in E:
        out = out.replace(old, new, 1)
        print(f"{eid} applied.")
    dst = path.replace(".v13.tex", ".v14.tex")
    open(dst, "w", encoding="utf-8").write(out)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
