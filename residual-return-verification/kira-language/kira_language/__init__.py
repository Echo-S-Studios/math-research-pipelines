"""kira_language -- the disjoint KIRA language hub.

One-way by construction: this package reads loom ONLY via `loom_bridge` (read-only); L00M never
imports it. **Import-safe**: importing the package does NO work and NO I/O (only `holding`, a stdlib
leaf, is eagerly bound here -- numpy is pulled only if you import `dispatch`/`semantic_kernel`). KIRA
shells it via  `py -m kira_language`  (one JSON request on stdin -> one JSON result on stdout, ASCII-safe).

Layers (one-directional; nothing lower imports anything higher):
    holding (L0, exact, stdlib)  <-  semantic_kernel / loom_bridge / portable_io (L1)  <-  dispatch (L3)
"""
from . import holding
from .holding import H, VOID, ONE

__all__ = ["holding", "H", "VOID", "ONE"]
