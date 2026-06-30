# `Zipped-Tarred-Pipelines/` — offline-distribution archives

Packaged, single-file copies of the three pipelines, for handing someone the whole verification
package offline (e.g. to onboard an LLM or a reviewer with no repo access).

| Archive | Mirrors | Notes |
|---|---|---|
| `lambda2c-emissiongap-verification.zip` | [`../lambda2c-emissiongap-verification/`](../lambda2c-emissiongap-verification/) | the λ = 2c & Emission-Gap suite |
| `matrix-plates-1.1.2.tar` | [`../matrix-plates/`](../matrix-plates/) | the Mahler-measure plates package (v1.1.2) |
| `residual-return-verification-v2.tar` | [`../residual-return-verification/`](../residual-return-verification/) | the exact-learning substrate (v2; ~1.4 MB — includes the committed PDFs) |

> **These are duplicates, not the source of truth.** Develop, test, and contribute in the three
> canonical top-level directories. The archives are point-in-time snapshots and are **not refreshed
> automatically**, so they can drift behind the live trees; their version tags (none / `1.1.2` /
> `v2`) are inconsistent for the same reason.

To extract:

```bash
unzip lambda2c-emissiongap-verification.zip
tar -xf matrix-plates-1.1.2.tar
tar -xf residual-return-verification-v2.tar
```

A future cleanup option (noted in the repo scoping) is to move these to **GitHub Releases** as
downloadable assets rather than keeping ~1.6 MB of duplicated content in the git history.
