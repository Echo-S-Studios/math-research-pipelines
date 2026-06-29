"""pytest bootstrap for the kira-language project (the disjoint language hub).

ONE-WAY BRIDGE TO loom
----------------------
KL_DTA's conformance test (`test_kl_dta_conformance.py`) cross-checks Cl(2,0)
against loom's exact integer companion-matrix route (the third route, anchored
on the phi void-law keystone x^2 = x + 1). `loom` lives in the L00M clone, NOT
here -- kira-language is DISJOINT. This shim makes `import loom` resolve to the
real L00M kernel so the bridge stays honest (no vendored copy that could drift).

Direction is strictly one-way, by construction:
  * kira-language reads loom            -> allowed (the bridge).
  * L00M imports kira-language / KL_DTA -> NEVER (L00M never sees this path).

Mechanism: APPEND the L00M root to sys.path (do not prepend). pytest already
prepends THIS directory, so the local KL_DTA.py is the module under test; only
`loom` -- which does not exist locally -- falls through to the appended L00M
root. So the copy under development always wins; only the bridge reaches out.

Override the L00M location with the env var KIRA_LANG_L00M_ROOT; otherwise it
defaults to the sibling clone ../L00M (both live under C:\\Users\\acead\\projects).
If neither resolves, the conformance test fails with its own clear ImportError
(the loom-free test_KL_DTA.py is unaffected and still runs).
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_L00M_ROOT = os.environ.get("KIRA_LANG_L00M_ROOT") or os.path.normpath(
    os.path.join(_HERE, os.pardir, "L00M")
)

if os.path.isdir(_L00M_ROOT) and _L00M_ROOT not in sys.path:
    sys.path.append(_L00M_ROOT)   # APPEND: local modules win; only `loom` falls through.
