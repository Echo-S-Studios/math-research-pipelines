# Relational-charge verification bundle — 2026-07-02

Companion artifacts for *Relational Charge on the Spectral Semiring*
(`relational_charge_paper.tex` / `.pdf`). Repository deposit context:
DOI 10.5281/zenodo.21121863 (v1.0.0); this bundle ships in the repository
deposit from v1.0.1 onward (paper, section 9).

## Integrity

    sha256sum -c SHA256SUMS        # 11 artifacts, all must report OK

## Replication (paper section 9; expected outputs = Appendix A signatures)

    python3 relational_charge_probe.py    # entries A-H, ~1 s  ({1:10} for Lehmer)
    python3 supplement_round3.py          # entries O-S
    python3 supplement_round6.py          # entries U-V
    python3 supplement_round7.py          # entry W + census rejection tally (378) + nu-criterion
    python3 census_deg12.py               # Theorem 7.10 census, ~2 min (37/37 inert)
    gp -q cross_check.gp  < /dev/null     # cross-engine rows A-I, P, Q
    gp -q cross_round6.gp < /dev/null     # cross-engine rows U, V

Any deviation from Appendix A is a finding.

## Engines

Python 3.12.3, sympy 1.14.0; PARI/GP 2.15.4. All arithmetic is exact:
no floating-point number crosses a decision boundary.

## Notes

- `supplement_for_paper.py`: round-1/2 ledger checks (imports the probe).
- `apply_doi_patch.py`: retired with an APPLIED banner; kept for provenance.
- This `README.md` is documentation and is not covered by `SHA256SUMS`.
