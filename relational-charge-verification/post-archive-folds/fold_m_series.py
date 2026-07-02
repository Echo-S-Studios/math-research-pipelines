#!/usr/bin/env python3
"""fold_m_series.py -- referee sync fold for the relational-charge deposit:
RC-l -> RC-m.

Edits (M-series; referee findings D1 + the two RC-l sync notes):
  M1  D1: the "--- the twenty-three cross-engine signatures." clause is
      reattached to the gp-decks bullet it describes (23 = A--I + P + Q +
      U + V, the pre-live set; run 3's count is 237) -- the K3 insertion
      had left it dangling after the live-replication bullet
  M2  Cor 7.16's corroboration list gains the "live instances" qualifier
      and the [-4,4]^5 (1063) entry, for parity with WP v1.3
  M3  ref [2]: digest rendered in full (kit archive-time rule) and the
      version note updated

All-or-nothing anchors; output .l.tex -> .m.tex.
Usage: python3 fold_m_series.py relational_charge_paper.l.tex
"""
import sys

E = []

E.append(("M1", r"""\item \texttt{gp -q cross\_check.gp}, \texttt{gp -q cross\_round6.gp}, and
\texttt{gp -q cross\_round8.gp}
\item live replication of ledger row~M (run~3): drivers and transcripts
SHA-pinned in the companion package
\texttt{pisot-residue-verification.zip} (SHA-256 \texttt{f803ce52dbfd_PLACEHOLDER})
--- the twenty-three cross-engine signatures.""",
r"""\item \texttt{gp -q cross\_check.gp}, \texttt{gp -q cross\_round6.gp}, and
\texttt{gp -q cross\_round8.gp}
--- the twenty-three cross-engine signatures.
\item live replication of ledger row~M (run~3, $237$ signatures): drivers
and transcripts SHA-pinned in the companion package
\texttt{pisot-residue-verification.zip} (SHA-256 \texttt{f803ce52dbfd_PLACEHOLDER})"""))

E.append(("M2", r"""live case is the quintic two-pair pattern; the executed scans of
\cite{pisotnote} find \emph{zero} mirrored cross-shell classes on every
live instance of the boxes $[-2,2]^5$ ($67$ two-pair), $[-3,3]^5$ ($313$),
$[-2,2]^6$ ($159$ two-pair with real spectator), and $[-2,2]^7$ ($414$:
$105$ two-pair, $309$ three-pair --- the first three-pair population).) \F""",
r"""live case is the quintic two-pair pattern; the executed scans of
\cite{pisotnote} find \emph{zero} mirrored cross-shell classes on every
live instance of the boxes $[-2,2]^5$ ($67$ two-pair), $[-3,3]^5$ ($313$),
$[-4,4]^5$ ($1063$), $[-2,2]^6$ ($159$ two-pair with real spectator), and
$[-2,2]^7$ ($414$: $105$ two-pair, $309$ three-pair --- the first
three-pair population); the counts are live instances, not census
totals.) \F"""))

E.append(("M3", r"""\bibitem{pisotnote} J.~Turner, \emph{The Pisot Cross-Shell Residue: A
Reduction Lemma, Sharpness Witnesses, and an Exhaustive Quintic Execution
of the $\nu$-Criterion}, session note (v1.1 with executed box extensions),
Echo-S Studios \texttt{math-research-pipelines}, July 2026; drivers and
transcripts SHA-pinned in the companion package
\texttt{pisot-residue-verification.zip} (SHA-256 \texttt{f803ce52\ldots})
and its N2--N4 successors.""",
r"""\bibitem{pisotnote} J.~Turner, \emph{The Pisot Cross-Shell Residue: A
Reduction Lemma, Sharpness Witnesses, and an Exhaustive Quintic Execution
of the $\nu$-Criterion}, session note (v1.4; box, degree, and P-series
extensions executed), Echo-S Studios \texttt{math-research-pipelines},
July 2026; drivers and transcripts SHA-pinned in the companion package
\texttt{pisot-residue-verification.zip} (SHA-256
\texttt{f803ce52dbfd_PLACEHOLDER}) and its N2--N4 successors.""" ))

FULL = (r"\texttt{f803ce52dbfd_PLACEHOLDER}",
        r"\texttt{f803ce52dbdfd070390df72749c3e77}\allowbreak"
        r"\texttt{829783e732a5f231e2d60e31be9160404}")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    digest_markup = (r"\texttt{f803ce52dbdfd070390df72749c3e77}\allowbreak"
                     r"\texttt{829783e732a5f231e2d60e31be9160404}")
    digest_chunked = (r"\texttt{f803ce52dbdfd070}\allowbreak"
                      r"\texttt{390df72749c3e778}\allowbreak"
                      r"\texttt{29783e732a5f231e}\allowbreak"
                      r"\texttt{2d60e31be9160404}")
    # normalize the anchors: the file carries the split full digest in the
    # K3 bullet; substitute the placeholder in our anchor strings
    edits = []
    for eid, old, new in E:
        old = old.replace(r"\texttt{f803ce52dbfd_PLACEHOLDER}", digest_markup)
        new = new.replace(r"\texttt{f803ce52dbfd_PLACEHOLDER}", digest_chunked)
        edits.append((eid, old, new))
    bad = [(eid, src.count(old)) for eid, old, _ in edits if src.count(old) != 1]
    if bad:
        for eid, n in bad:
            print(f"ANCHOR-FAIL {eid}: found {n} occurrences (need exactly 1).")
        sys.exit(1)
    out = src
    for eid, old, new in edits:
        out = out.replace(old, new, 1)
        print(f"{eid} applied.")
    dst = path.replace(".l.tex", ".m.tex")
    open(dst, "w", encoding="utf-8").write(out)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
