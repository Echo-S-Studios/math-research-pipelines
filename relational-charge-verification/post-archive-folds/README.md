# post-archive-folds — the relational-charge paper's K/L/M chain

Post-archive revisions of the parent deposit (`../relational_charge_paper.tex`,
which remains the **pinned v1.0.x archive** — see `../SHA256SUMS`; nothing in
this folder modifies it). Each step is an all-or-nothing anchored patcher.

## Chain

| build | produced by | adds | checks |
|---|---|---|---|
| `…k.tex/.pdf` | `fold_k_series.py` (ships inside `files-fixed.zip`'s `deposit-crossengine-fold/`, SHA-pinned there; **not in this repo**) | K1 harness rules H1/H2 beside the engine pins; K2 ledger row-M live clause (237/237, 474); K3 companion-package pointer with the full digest | 0 err / 0 undef |
| `…l.tex/.pdf` | `fold_l_series.py` | N6: the Z\* witness beside Ex 7.19, the real-pair ν-reduction beside Rem 7.6, Cor 7.16 sharpened — all as unnumbered blocks | 0 / 0; **compiled environment numbering verified unchanged** (7.6/7.13/7.16/7.19/7.20 preserved) |
| **`…m.tex/.pdf`** | `fold_m_series.py` | **HEAD** — referee sync: D1 (the "twenty-three signatures" clause reattached to the gp-decks bullet), Cor 7.16 + [−4,4]⁵ (1063) with the live-instances qualifier, ref [2] full digest | 0 / 0; numbering unchanged |

## Redundancy note

**m is the only current build.** k and l are superseded intermediates kept as
the auditable chain (each reproducible as previous + fold script; git history
preserves them). The intermediate PDFs are the safe prune if desired; tex and
patchers are the record.

Zenodo mapping per `FOLD-INSTRUCTIONS.md` (in the fold kit): the K fold is the
paper's v1.1.0; L and M continue under the same concept DOI (suggested
v1.2.0 = L+M together, changelog: session-note folds + referee sync).
