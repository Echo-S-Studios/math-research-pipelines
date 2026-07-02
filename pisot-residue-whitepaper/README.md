# pisot-residue-whitepaper — the session note's version chain

The whitepaper *"The Pisot Cross-Shell Residue: A Reduction Lemma, Sharpness
Witnesses, and an Exhaustive Quintic Execution of the ν-Criterion"* with its
same-day addenda folded in sequence. Every step is an all-or-nothing anchored
patcher (each anchor must occur exactly once or nothing is written), so the
whole chain is auditable and mechanically reproducible.

## Version chain

| version | produced by | adds | build check |
|---|---|---|---|
| v1.0 | authoring session (`paper/` inside `pisot-residue-verification.zip`, SHA-pinned there; **not in this repo**) | the original session note | 0 err / 0 undef |
| v1.1 | `fold_v11_whitepaper.py` (V-series, 15 edits) on v1.0 | N2/N3 box extensions, H4, pinned corrections (detector semantics, twist exclusivity, chain independence) | 0 / 0 |
| v1.2 | `fold_w_series.py` (W-series, 9 edits) | N4 executed (degrees 6–7, first three-pair population, degenerate-chain Pisot), P7 resolved | 0 / 0 |
| v1.3 | `fold_x_series.py` (X-series, 9 edits) | the P-series executed in full ([−4,4]⁵, P4 standalone, updated falsifier table) | 0 / 0 |
| **`…v14.tex/.pdf`** | `fold_y_series.py` (Y-series, 12 edits) | **HEAD** — referee errata E1–E3 + F1–F3 + the adopted free irreducibility remark | 0 / 0 |

## Redundancy note

**v14 is the only version kept in-tree** (pruned 2026-07-02; no Zenodo
deposit pending). The v1.1–v1.3 intermediates remain fully recoverable two
ways: (a) git history — last present at commit `81f4db0`
(`git show 81f4db0:pisot-residue-whitepaper/pisot_residue_whitepaper.v12.tex`);
(b) mechanically — each version is exactly (previous version + its fold
script), so the chain regenerates from the bundle-pinned v1.0 with the four
patchers kept here.

Naming: the first patcher is `fold_v11_whitepaper.py` (it predates the
letter-series convention adopted from W onward); it is the V-series.
