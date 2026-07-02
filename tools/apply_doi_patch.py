#!/usr/bin/env python3
"""Close review finding F1 once the companion note has a DOI.

Usage:  python3 apply_doi_patch.py 10.5281/zenodo.XXXXXXX
Then recompile:  pdflatex relational_charge_paper.tex  (twice)

Patches three anchors in relational_charge_paper.tex:
bibitem [1], the access-path sentence in section 1.3, and the
artifact-deposit sentence in section 9. Each anchor is asserted to occur
exactly once; on any mismatch the file is left untouched.
"""
import sys

doi = sys.argv[1]
tex = "relational_charge_paper.tex"
src = open(tex).read()

PAIRS = [
    ("""Distributed with the
present note; intended for the project's papers drop-zone at
\\texttt{https://echo-s-studios.github.io/math-research-pipelines/}.
Appendix~\\ref{app:inherited} lists every statement imported from it.""",
     f"""Archived at DOI \\texttt{{{doi}}}; also served at
\\texttt{{https://echo-s-studios.github.io/math-research-pipelines/}}.
Appendix~\\ref{{app:inherited}} lists every statement imported from it."""),

    ("""requires~\\cite{CMC}, which is distributed with
this manuscript --- a DOI-archived deposit of the project repository is the
intended permanent access path.""",
     f"""requires~\\cite{{CMC}}, archived at DOI \\texttt{{{doi}}}."""),

    ("""a DOI-archived deposit of
these artifacts alongside the manuscript is the intended distribution
channel, enabling verification by a distinct operator.""",
     f"""the artifacts are deposited at DOI \\texttt{{{doi}}}, enabling
verification by a distinct operator."""),
]

for old, new in PAIRS:
    assert src.count(old) == 1, f"anchor drifted (count={src.count(old)}):\n{old[:60]}..."
for old, new in PAIRS:
    src = src.replace(old, new)
open(tex, "w").write(src)
print(f"patched 3 anchors with DOI {doi}; recompile twice.")
