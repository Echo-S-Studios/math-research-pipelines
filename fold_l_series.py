#!/usr/bin/env python3
"""fold_l_series.py -- N6: fold the session note's Z* witness and real-pair
nu-reduction lemma into the relational-charge deposit, and sharpen the Pisot
corollary with the residue location and executed evidence.

Target: relational_charge_paper.k.tex (the v1.1 build produced by the
K-series fold; the K-series carried only H1/H2 and ledger-M-live).

Edits (L-series, continuing the J/K idiom):
  L1  real-pair nu-reduction folded as an UNNUMBERED block directly after the
      nu-criterion remark (rem:scope, compiled Rem 7.6)
  L2  hypothesis-necessity witness Z* folded as an UNNUMBERED block directly
      after the sharpness example (ex:twistshell, compiled Ex 7.19)
  L3  the Pisot corollary's parenthetical (cor:pisot, compiled Cor 7.16)
      sharpened in place: residue location + executed zero-falsifier evidence
  L4  bibliography gains the session-note entry (\\cite{pisotnote})

Numbering discipline: L1/L2 are deliberately unnumbered (K1 precedent) and L3
edits inside an existing environment, so the compiled numbering of every
environment in the deposit is UNCHANGED -- the session note's citations
([Thm 7.13], [Cor 7.16], [Ex 7.19], [Rem 7.20], ...) remain valid.

Discipline: all-or-nothing. Every anchor must occur exactly once or nothing
is written. Output: <input>.l.tex (input never modified in place).

Usage:  python3 fold_l_series.py path/to/relational_charge_paper.k.tex
"""
import sys

E = []

# ------------------------------------------------- L1: nu-reduction block
E.append(("L1", r"""(ledger entries~A, B). \F
\end{remark}""",
r"""(ledger entries~A, B). \F
\end{remark}

\medskip
\noindent\textbf{Real-pair $\nu$-reduction (session-note fold).}
Against a \emph{real} partner the cross-shell criterion simplifies
completely. Let $O$ be conjugation-closed, $\beta\in O$ real, $\alpha\in O$
non-real: $t(\beta)\in\{0,\tfrac12\}$, so
$t(\alpha)-t(\beta)\in\Q\iff2\,t(\alpha)\in\Q$, and
$\alpha/\overline{\alpha}$ is unimodular with
$t(\alpha/\overline{\alpha})=2\,t(\alpha)$; hence
\[
\alpha\approx\beta\iff\alpha/\overline{\alpha}\ \text{is a root of unity}.
\]
When $O$ is the root set of $p$, the quantity $\alpha/\overline{\alpha}$ is
an ordered ratio, i.e.\ a root of $\Rat_p$: every real$\times$non-real
coherence question --- same shell or cross shell --- is decided by the
complete contact scan of $\Rat_p$ alone, with no $\nu$-computation and no
$2$-part loss (\F; \cite[Lem.~4.1]{pisotnote}). Combined with
Theorem~\ref{thm:pinning} this forces relational inertness for every Pisot
number whose minimal polynomial has at most one pair of non-real
conjugates, and localizes the first genuinely open case of the cross-shell
residue at the quintic two-pair pattern
(\cite[Thm.~4.2, Cor.~4.3]{pisotnote})."""))

# ------------------------------------------------------- L2: Z* witness
E.append(("L2", r"""twisted-shell mechanism exclude each other. \F
\end{example}""",
r"""twisted-shell mechanism exclude each other. \F
\end{example}

\medskip
\noindent\textbf{Hypothesis-necessity witness $Z^{*}$ (session-note fold).}
The example above shows the pinning hypothesis necessary for an irreducible
input. The reducible witness
$Z^{*}=x^4-3x^2+1=(x^2-x-1)(x^2+x-1)$ isolates the remaining hypotheses of
Theorem~\ref{thm:pinning}: each factor is irreducible with \emph{both} of
its root moduli ($\varphi$ and $\varphi^{-1}$) uniquely attained within
that factor, so per-factor pinning holds; yet the roots $\varphi$ (of the
first factor) and $-\varphi$ (of the second) carry the torsion ratio $-1$
at the shared modulus $\varphi$. Hence irreducibility cannot be dropped
from Theorem~\ref{thm:pinning}, and the disjoint-modulus clause cannot be
dropped from its mixed statement --- the two failure routes are exactly
transitivity and the excluded shared shell. The complete scan reads
$\Rat_{Z^{*}}\leadsto\{\Phi_1^{\,4},\Phi_2^{\,4}\}$ ($\Phi_1$ from the
diagonal, $\Phi_2$ from the two antipodal pairs, ordered), engine-confirmed
in both stacks (\F; \cite[Prop.~3.3]{pisotnote}). Together with $x^4-2$,
the two witnesses isolate every hypothesis of the theorem and its mixed
form."""))

# ---------------------------------------------- L3: sharpen the corollary
E.append(("L3", r"""factor, and no non-real conjugate is coherent with a real one. (The full
type of a Pisot number can still carry mirrored cross-shell classes;
deciding those is the $\nu$-criterion of Remark~\ref{rem:scope}.) \F""",
r"""factor, and no non-real conjugate is coherent with a real one. (The full
type of a Pisot number can still carry mirrored cross-shell classes among
its non-real shells; deciding those is the $\nu$-criterion of
Remark~\ref{rem:scope}. The session-note fold sharpens the location: by the
real-pair $\nu$-reduction following that remark, the residue is empty for every
Pisot number with at most one pair of non-real conjugates, so its first
live case is the quintic two-pair pattern; the executed scans of
\cite{pisotnote} find \emph{zero} mirrored cross-shell classes on every
live instance of the boxes $[-2,2]^5$ ($67$ two-pair), $[-3,3]^5$ ($313$),
$[-2,2]^6$ ($159$ two-pair with real spectator), and $[-2,2]^7$ ($414$:
$105$ two-pair, $309$ three-pair --- the first three-pair population).) \F"""))

# --------------------------------------------------------- L4: bibliography
E.append(("L4", r"""\bibitem{Kronecker}""",
r"""\bibitem{pisotnote} J.~Turner, \emph{The Pisot Cross-Shell Residue: A
Reduction Lemma, Sharpness Witnesses, and an Exhaustive Quintic Execution
of the $\nu$-Criterion}, session note (v1.1 with executed box extensions),
Echo-S Studios \texttt{math-research-pipelines}, July 2026; drivers and
transcripts SHA-pinned in the companion package
\texttt{pisot-residue-verification.zip} (SHA-256 \texttt{f803ce52\ldots})
and its N2--N4 successors.

\bibitem{Kronecker}"""))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    bad = [(eid, src.count(old)) for eid, old, _ in E if src.count(old) != 1]
    if bad:
        for eid, n in bad:
            print(f"ANCHOR-FAIL {eid}: found {n} occurrences (need exactly 1). "
                  f"Nothing written.")
        sys.exit(1)
    out = src
    for eid, old, new in E:
        out = out.replace(old, new, 1)
        print(f"{eid} applied.")
    dst = path.replace(".k.tex", ".l.tex") if path.endswith(".k.tex") \
        else path + ".l"
    open(dst, "w", encoding="utf-8").write(out)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
