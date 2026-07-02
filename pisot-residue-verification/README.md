# pisot-residue-verification — session reports and transcripts

Home of every verification and execution **report** of the 2026-07-02 Pisot
cross-shell residue program, in campaign order. The runnable artifact
packages the reports describe live in sibling directories (map below).

## Reports (chronological)

| file | covers | verdict |
|---|---|---|
| `pisot-residue-verification-report.md` | zero-shot verification of the original 12-stage `pisot-residue-verification.zip` bundle (S0–S11) | all claims verified, exit 0 |
| `pisot-residue-verification-run-output.txt` | full pipeline stdout of that run | evidence transcript |
| `n2-n3-verification-report.md` | N2 ([−3,3]⁵) + N3 ({−2..2}⁶) box extensions, bundle rev 2, incl. the 15-agent adversarial review (findings F1–F9) | all numerical claims verified; RUNBOOK ALL GREEN |
| `n2-n3-runbook-output.txt` | full rev-2 RUNBOOK stdout | evidence transcript |
| `n2-n3-independent-empty-chain-audit.py` | this session's independent λ-sandwich adjudicator (the second exact method behind the 2602/8/0 completeness result) | 0 Pisots among the skipped set |
| `n4-n6-execution-report.md` | N4 (degree 6–7 censuses + scans) and N6 (parent-paper L-series fold); erratum E2 applied | executed and verified |
| `p-series-execution-report.md` | the P-series falsifier table run in full (P1–P8), incl. the [−4,4]⁵ box; erratum E1 applied | executed; nothing promoted |

## Program map

| location | contents |
|---|---|
| `../n4-degree67/` | N4 artifact package (drivers, pinned censuses/scans, GP deck, RUNBOOK, ERRATA) |
| `../p-series/` | P-series artifact package (drivers, pinned data, RUNBOOK, ERRATA, deps) |
| `../pisot-residue-whitepaper/` | the session-note whitepaper version chain v1.1→v1.4 + fold patchers |
| `../relational-charge-verification/post-archive-folds/` | the parent paper's post-archive K/L/M fold chain |

The original verification bundles (`pisot-residue-verification.zip`,
SHA-256 `f803ce52…9404`; `files-fixed.zip`, SHA-256 `8432455c…d3a1`) are
session uploads pinned by digest in the reports and in whitepaper
Appendix A; they are not duplicated into the repository.
