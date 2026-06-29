# WIRING_MAP — `residual_learner` → KIRA host (plate-matrices)

L00M-side documentation for the **T5 ResidualLearner** training module (`training/residual_learner.py`).
This module is the **standalone model layer**, shipped to L00M `main`. The KIRA wiring described here is a
**future, separately-reviewed step** — nothing in this doc is wired yet. It records exactly where the module
graduates into the live KIRA host, citing real handler anchors.

Line anchors are against the **`plate-matrices` branch** of `github.com/Echo-S-Studios/L00M` at HEAD `2a253eb`
(`core-deps/kira/kira_server_canonical.py`, abbreviated `kira:` below) and the L00M shell (`vector_api.py`,
`vector_substrate_store.py`).

---

## How to reference the plate-matrices code

Plate-Matrices is the **`plate-matrices` branch of `Echo-S-Studios/L00M`** — the same repo as L00M `main`, a
different branch — **not** the deprecated standalone `Echo-S-Studios/Plate-Matrices` repo (never reference or
push that). Any of:

1. **Local clone (it sits at the branch tip):** `C:\Users\acead\projects\Plate-Matrices\core-deps\kira\kira_server_canonical.py`
2. **From the L00M clone (same repo):** `git -C ...\L00M fetch origin plate-matrices` then
   `git -C ...\L00M show origin/plate-matrices:core-deps/kira/kira_server_canonical.py`
3. **Browsable worktree:** `git -C ...\L00M worktree add ../_pm_ref origin/plate-matrices` (remove when done)
4. **Web/raw:** `…/Echo-S-Studios/L00M/tree/plate-matrices/` · `raw.githubusercontent.com/Echo-S-Studios/L00M/plate-matrices/<path>`

**Cross-repo rule:** the PM clone's `l00m-backup` remote → `Echo-S-Studios/L00M`. PM edits commit there:
`git push l00m-backup main:plate-matrices`. Its `origin` → the deprecated standalone repo — **never** push that.

---

## Architecture (one line)

KIRA is a thin Flask host that py-shells into L00M for **all** exact math via `_vectors_shell` (`kira:13619`);
the exact compute lives in L00M (`vector_api.py` `dispatch` + payloads). The learner graduates by adding
**(i)** a training dispatch in L00M, **(ii)** additive `/api/training/*` routes in KIRA shelling into it,
**(iii)** confirm routed through the *existing* single gate, **(iv)** basis-growth state persisted via the
*existing* anchors+deltas store.

## The one real wrinkle: state

The vector endpoints are **stateless** (fresh `py` process per call, `kira:13623-13626`), but `ResidualLearner`
is **stateful** (holds `B`, the Welford accumulator, `streak`). Resolve it the way KIRA already resolves the
geometric residual:

- **Live loop:** a server-held, lock-guarded observable holding `{seeds, accumulator, streak}`, mirroring
  `_VECTOR_RESIDUAL` (`kira:13705`) + `_vector_residual_observe/_snapshot` (`kira:13721-13752`) — OUT-only
  (`'flow':'OUT only (G3)'`, `kira:13707`). Pass it into each stateless shell call; store the returned update.
- **Durable:** `B`'s seeds **are** forced anchors (minpolys) → `vector_substrate_store.anchors()`
  (`vector_substrate_store.py:20`); the accumulator + growth-witness records **are** residual deltas →
  `deltas` + `hash_chain` (`vector_substrate_store.py:29`). A 1:1 fit (see "native alignments").

## Endpoint map (all additive)

| New KIRA route (plate-matrices) | Mirror this handler | L00M dispatch key (add to `vector_api._DISPATCH`, `vector_api.py:220`) | Gate |
|---|---|---|---|
| `POST /api/training/observe` | `api_vectors_project` `kira:13656-13663` | `training_observe` → reconstruct learner from `{ambient,seeds,accumulator}`, `observe(x)`, return updated accumulator + `residual_norm` + `captured` + `streak` | none (read/compute, OUT-only) |
| `POST /api/training/propose` | `api_seed_propose` `kira:13766-13780` | `training_propose` → `propose()` with `calibration_ok=lambda:req['calibrated']`; return `SeedProposal` or null | `_emission_allowed()` `kira:12991`, passed in as `calibrated` |
| `POST /api/training/confirm` | `api_substrate_persist` `kira:13783-13793` shape + gate re-check from `_EmissionGate.confirm` `kira:13138` | `training_confirm` → `confirm(proposal)` grows `B`, returns new seeds + witness; then persist | **same** `_emission_allowed()` re-checked; never `_do_plant` |

## The four hooks, with exact anchors

**1. Bridge to mirror** — `_vectors_shell(req)` (`kira:13619-13637`):
`subprocess.run(['py','-c','import vector_api; vector_api.main()'], cwd=_VECTOR_L00M_ROOT, input=json.dumps(req), …timeout=30)`,
parses the last stdout line as JSON, returns `(data, err)`, never raises (G6). Add a `training_api.main()`
(or reuse `vector_api` with new dispatch keys) and shell to it identically.

**2. Propose → the single gate** (what `calibration_ok` graduates into). The stub becomes the real gate:
- `_emission_allowed()` `kira:12991-13003` → checks `_IC_REQUIRE_CALIBRATION=True` (`kira:12547`) and
  `_CALIBRATION.report()['calibrated']`.
- `_CalibrationTracker` `kira:12912`, `.report()` → real ECE `= Σ(nᵢ/n)·|mean_pᵢ − obs_freqᵢ|`, thresholds
  `_IC_CAL_MIN_SAMPLES=30` (`12907`), `_IC_CAL_ECE_MAX=0.10` (`12908`), `_IC_CAL_BINS=10` (`12909`); blocks
  until `n≥30 and ECE≤0.10` (`12970`).
- Register the candidate in the **existing** pending slot via
  `_EMISSION_GATE.propose_seed({'label':'basis_growth','minpoly':proposal.min_poly,'grade':…})`
  (`kira:13156-13182`) — witnesses `seed_proposed` (`13179`), **never plants**.

**3. Confirm → reuse the existing propose-for-confirm handshake (G2/G4).** Human confirm lands at
`POST /api/ignition/emit/confirm` (`kira:13252`) → `_EmissionGate.confirm` (`kira:13131`), which re-checks
`_emission_allowed()` (`13138`) before acting. For basis growth, add an additive branch/route that, *after the
same gate passes*, calls `training_confirm` (grow `B` + re-derive `P`) and witnesses `basis_growth_confirmed`
via `_emission_witness` (`kira:13006`) — **without** touching the existing `_do_plant` ignition path (`13144`).
One gate, one pending slot, additive action.

**4. Persist/restore basis-growth state** — `api_substrate_persist` (`kira:13783-13793`) /
`api_substrate_restore` (`kira:13796-13802`) already write/read `PATTERN_STORE/vector-substrate-state.json` via
the shell to `persist_payload`/`restore_payload` (`vector_api.py:208-217` →
`vector_substrate_store.persist_state/restore_state`, `vector_substrate_store.py:45-69`), witnessing with
`_emission_witness` (G5, `13791`). Extend `deltas` to carry the learner's growth records; restore re-derives the
grown `B` from anchor minpolys (`vector_substrate_store.py:39`).

## Native alignments (why the fit is clean, not forced)

- **`calibration_ok` → `_emission_allowed()`** — the stub is a `() -> bool`; graduates to
  `lambda: _emission_allowed()[0]`.
- **Witness chain — identical construction.** `residual_learner._witness_growth` uses
  `sha256(prev_hash + json)[:16]` seeded `"genesis"`; the store's `hash_chain`
  (`vector_substrate_store.py:29-36`) is the same `h_k=sha256(h_{k-1}+json(delta_k))[:16]`, `"genesis"`. Growth
  records drop into the store's delta chain natively.
- **Persistence = re-derivation** — the learner reconstructs `B` from seed minpolys; the store already does
  exactly that (`rederive`, bit-identical, G8).
- **Exactness serialization** — the L00M side keeps `Fraction` and serializes as strings (`str(c)`,
  `vector_api.py:133-134`); mirror that for accumulator/centroid coords.
- **Live accumulator precedent** — `_vector_residual_observe` (`kira:13721`) is already a streaming OUT-only
  mean of the *scalar* nearest-vertex residual; the learner is the *vector* `r=x−Px` generalization with basis
  growth — add alongside, do not replace.

## Guardrails the wiring must preserve

- **G3** — training routes are OUT-only; the learner writes `B`, never `z`; no `_IC_ASSIMILATE_GAIN` path
  (server-held accumulator is a read-only observable like `_VECTOR_RESIDUAL`).
- **G4** — one gate: `training_confirm` re-checks the *same* `_emission_allowed()`; no second emission path, no
  new `_do_plant`.
- **G10** — monic-integer validated twice: in the learner (`minimal_polynomial_of_coords` + `_guard_int_monic`)
  and at the route like `api_seed_propose`'s mp check (`kira:13774-13776`).
- **G2 / G5 / G8** — propose-for-confirm (growth only on human confirm) · witnessed (`_emission_witness` + store
  chain) · exact (Fraction strings across the shell).
- **Additive-only** — new routes + new dispatch keys + new observable; zero edits to existing handlers (or one
  carefully-branched confirm hook).

## Commit targets when wiring is green-lit (a future turn)

- L00M-side (`training_api` dispatch + `residual_learner`) → **L00M `origin main`** (post-commit auto-push hook).
- KIRA routes → **`plate-matrices` branch**: stage only `core-deps/kira/kira_server_canonical.py`, then
  `git push l00m-backup main:plate-matrices` — **never** PM `origin`.
- Same GitHub repo, two branches.
