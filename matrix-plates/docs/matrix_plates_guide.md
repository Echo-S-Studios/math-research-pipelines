# Matrix Plates — Developer Guide

A field manual for turning the matrices produced by `matrix_plates.html` into generative content.
Each construction in the tool emits an **exact integer matrix** plus a set of invariants. This guide maps every
matrix family to a concrete computational use, gives runnable code, and names the single invariant that steers it.

The constructions themselves are classical; the point of this guide is the **pipeline** — read a plate, lift its
matrix and invariants, and run the matching recipe to produce output. No new mathematics is assumed.

---

## Workflow

1. **Generate** a plate in the tool (pick a construction, set seeds/params, *Press plate*; or *Seed batch*).
2. **Read** the invariant chips: `det`, `tr`, `ρ` (spectral radius), `‖·‖_F`, `M` (Mahler measure), `rank`,
   `integer`, `unimodular`, and the spectrum (eigenvalues relative to the unit circle).
3. **Lift** the matrix — copy the entries into a 2-D array (`Export .html` preserves them per plate).
4. **Run** the recipe for that family below. The invariant in each recipe's heading is the control dial.
5. **Record** `(construction, seeds, params)` for reproducibility — everything is deterministic except the
   seeded random family, which is reproducible from its integer seed.

---

## Core toolkit

Paste a plate's matrix as a JS array, e.g. `const M = [[0,1],[1,1]];`, then use these. All are dependency-free.

```js
function matmul(A, B) {                    // O(n^3)
  const n = A.length, m = B.length, p = B[0].length;
  const C = Array.from({ length: n }, () => new Array(p).fill(0));
  for (let i = 0; i < n; i++)
    for (let k = 0; k < m; k++)
      for (let j = 0; j < p; j++) C[i][j] += A[i][k] * B[k][j];
  return C;
}
const eye = n => Array.from({ length: n }, (_, i) =>
  Array.from({ length: n }, (_, j) => (i === j ? 1 : 0)));

function matpow(A, k) {                     // fast exponentiation, O(n^3 log k)
  let R = eye(A.length), P = A;
  while (k > 0) { if (k & 1) R = matmul(R, P); P = matmul(P, P); k >>= 1; }
  return R;
}
const apply = (A, v) => A.map(r => r.reduce((s, a, j) => s + a * v[j], 0));
```

Reference: Golub & Van Loan, *Matrix Computations* (matpow, stability); Strang, *Introduction to Linear Algebra*.

---

## Companion `C(p)` — sequence and growth-law generator

**Drive with: `ρ` (spectral radius = asymptotic growth rate).**

A companion matrix's powers run the linear recurrence whose roots are the seed's Galois conjugates. The φ plate
is the Fibonacci matrix; swap the seed polynomial to get a *different* growth law — a deterministic novel integer
sequence.

```js
const C  = [[0, 1], [1, 1]];               // companion of x^2 - x - 1  (φ)
const s0 = [0, 1];                          // seed state
const term = k => apply(matpow(C, k), s0)[0];   // k-th sequence term, O(d^3 log k)
// term(10) === 55. Swap C for the companion of x^2 - 7x + 1 (the "gap" plate) for a new law.
```

The `ρ` chip is `lim term(k+1)/term(k)` — use it directly as a tempo, zoom factor, or branching ratio.
For exact terms beyond ~2^53, run the same routine over `BigInt`:

```js
function matmulB(A, B) {                     // exact, arbitrary k
  const n = A.length, m = B.length, p = B[0].length;
  const C = Array.from({ length: n }, () => new Array(p).fill(0n));
  for (let i = 0; i < n; i++) for (let k = 0; k < m; k++)
    for (let j = 0; j < p; j++) C[i][j] += A[i][k] * B[k][j];
  return C;
}
```

Reference: Strang, *Linear Algebra*, companion-matrix recurrences; Perron–Frobenius for the growth rate.

---

## Kronecker `A ⊗ B` — self-similar texture generator

**Drive with: `M` (Mahler measure = multi-scale energy / detail density).**

Iterating the Kronecker product on a small 0/1 motif produces an exact fractal bitmap of size `n^L`. The
eigenvalue products (the ⊗ spectrum) set the energy across scales; the higher the gallery Mahler reading, the
busier the texture.

```js
function kron(A, B) {
  const n = A.length, m = B.length, C = [];
  for (let i = 0; i < n; i++) for (let k = 0; k < m; k++) {
    const row = [];
    for (let j = 0; j < n; j++) for (let l = 0; l < m; l++) row.push(A[i][j] * B[k][l]);
    C.push(row);
  }
  return C;
}
function fractal(seed, L) { let M = seed; for (let i = 1; i < L; i++) M = kron(M, seed); return M; }

const seed = [[1, 1, 1], [1, 0, 1], [1, 1, 1]];   // any motif
const tex  = fractal(seed, 3);                      // 27x27 -> draw nonzero cells as pixels
```

Reference: Hammack, Imrich & Klavžar, *Handbook of Product Graphs* (Kronecker/tensor products).

---

## Direct sum `A ⊕ B` — multi-voice / multi-channel generator

**Drive with: `rank` (number of independent active channels).**

A block-diagonal matrix runs several generators in parallel without interaction; the spectra coexist. Use one
companion per voice and read each block independently.

```js
function dsum(A, B) {
  const n = A.length, m = B.length, C = eye(n + m).map(r => r.fill(0));
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) C[i][j] = A[i][j];
  for (let i = 0; i < m; i++) for (let j = 0; j < m; j++) C[n + i][n + j] = B[i][j];
  return C;
}
// each diagonal block evolves on its own — e.g. two recurrences = two melodic voices.
```

---

## Commutator `[A,B] = AB − BA` — volume-preserving flow generator

**Drive with: `tr` (always 0 here ⇒ area/volume preservation).**

Because the trace is zero, `exp(tM)` has determinant 1 — the flow `x' = Mx` preserves area (Liouville). Use the
commutator as a swirling, non-dissipative field to advect particles or motes.

```js
function step(M, x, dt) { const Mx = apply(M, x); return x.map((v, i) => v + dt * Mx[i]); }
// advect a particle set with `step` for area-preserving motion (no sources or sinks).
```

Edge case: this is Euler integration; for long runs use RK4 or a symplectic integrator to keep the area exactly.
Reference: any dynamical-systems text on Liouville's theorem; `det(e^{tM}) = e^{t·tr M}`.

---

## Cartan `Aₙ / Dₙ / E₈` — optimal-lattice sampling, quantization, and modal synthesis

**Drive with: `det` and `unimodular` (E₈'s det = 1 marks the optimal 8-D lattice).**

Two distinct uses.

**(a) E₈ vector quantization / parameter snapping.** E₈ is the proven-optimal sphere packing and a near-optimal
quantizer in 8 dimensions; snap any 8-vector (eight control params, or two RGB+α blocks) to it for
minimal-distortion output.

```js
const dist2 = (p, q) => p.reduce((s, v, i) => s + (v - q[i]) ** 2, 0);
const rnd   = x => Math.round(x);

function nearestD8(x) {                      // round; fix parity if sum is odd
  let y = x.map(rnd), s = y.reduce((a, b) => a + b, 0);
  if (s % 2 !== 0) {
    let bi = 0, bd = -1;
    for (let i = 0; i < 8; i++) { const d = Math.abs(x[i] - y[i]); if (d > bd) { bd = d; bi = i; } }
    y[bi] += (x[bi] > y[bi] ? 1 : -1);
  }
  return y;
}
function nearestE8(x) {                       // E8 = D8 ∪ (D8 + ½); Conway–Sloane decoder (sketch)
  const a = nearestD8(x);
  const b = nearestD8(x.map(v => v - 0.5)).map(v => v + 0.5);
  return dist2(x, b) < dist2(x, a) ? b : a;
}
```

**(b) Aₙ modal synthesis.** The Aₙ Cartan matrix is the 1-D graph Laplacian; its eigenvalues are
`λ_k = 2 − 2cos(kπ/(n+1))` — the modes of a string. Use them as additive partials for a struck-string timbre.

```js
const modeFreq = (k, n, f0) => f0 * Math.sqrt(2 - 2 * Math.cos(k * Math.PI / (n + 1)));
// sum sin(2π · modeFreq(k,n,f0) · t) over k = 1..n  ->  physical-sounding partials
```

Reference: Conway & Sloane, *SPLAG* (E₈, decoder, quantization); Viazovska, *Annals of Math.* 2017 (optimality);
Spielman, *Spectral and Algebraic Graph Theory* (Laplacian spectra).

---

## Fibonacci / Lucas circulant `↻` — spectral synthesis and circular filtering

**Drive with: the spectrum (eigenvalues = DFT of the first row).**

A circulant is diagonalized by the DFT, so its first row *is* a frequency-domain object. Use the row as a circular
filter, or its DFT magnitude as additive partials whose envelope follows the golden growth.

```js
function dftMag(row) {                        // |eigenvalues| of circ(row)
  const n = row.length, out = [];
  for (let k = 0; k < n; k++) {
    let re = 0, im = 0;
    for (let j = 0; j < n; j++) { const a = -2 * Math.PI * k * j / n; re += row[j] * Math.cos(a); im += row[j] * Math.sin(a); }
    out.push(Math.hypot(re, im));
  }
  return out;
}
const partials = dftMag([1, 1, 2, 3, 5, 8]);   // fib row -> 6 partial amplitudes
// circular convolution of a signal with `row` = elementwise multiply in the DFT domain, O(n log n).
```

Reference: Davis, *Circulant Matrices*; Oppenheim & Schafer, *Discrete-Time Signal Processing* (circular convolution).

---

## Frustrated ring Laplacian `∿` — spectral layout and signed diffusion

**Drive with: `det` / `ρ` (det = 0 means balanced; det > 0 means frustrated).**

The signed Laplacian is positive semidefinite. When the sign pattern is *balanceable* (depends on `n mod 4`) the
smallest eigenvalue is 0 and `det = 0`; when *frustrated*, the lowest eigenvalue is strictly positive — so even the
smoothest mode decays, which produces twisting, non-flat patterns under diffusion.

```js
function diffuse(L, u, dt, steps) {           // u' = -L u  (graph heat flow)
  for (let s = 0; s < steps; s++) { const Lu = apply(L, u); u = u.map((v, i) => v - dt * Lu[i]); }
  return u;
}
// For layout: use the eigenvector of the second-smallest eigenvalue (Fiedler vector) as 1-D node coordinates.
```

Edge case: keep `dt < 2/ρ` or the explicit step diverges (use the `ρ` chip). Reference: Spielman, *Spectral and
Algebraic Graph Theory*; Harary, *On the notion of balance of a signed graph* (1953).

---

## Random (seeded) `⚄` — reproducible control / noise

**Drive with: `M` vs the structured families.**

The seeded random plate is the baseline. Generate it with the same seed to compare its Mahler measure against the
structured constructions — the structured families cluster at characteristic M values, random ones scatter. Use it
as reproducible procedural noise, or as the null model in a generative experiment.

```js
function mulberry32(seed) {                    // reproducible PRNG (same as the tool)
  let a = seed >>> 0;
  return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
const rnd = mulberry32(42);
const M = Array.from({ length: 4 }, () => Array.from({ length: 4 }, () => Math.floor(rnd() * 7) - 3));
```

---

## Invariant → control dial

| Invariant (chip) | What it reads | Drive in generation |
|---|---|---|
| `M` (Mahler) | spectral entropy / dynamical entropy | complexity, detail density, zoom rate, tempo |
| `ρ` (spectral radius) | dominant eigenvalue magnitude | iteration stability: `<1` decay, `=1` oscillate, `>1` grow; normalize by `ρ` to bound |
| `det` | volume scaling per step | `|det|=1` reversible/measure-preserving; `0` singular = projection / dimensionality reduction |
| `tr` (trace) | sum of eigenvalues | `tr=0` ⇒ volume-preserving flow (commutators) |
| `rank` | effective dimension | number of independent output channels |
| spectrum vs unit circle | inside / on / outside | decaying / pure-oscillation / growing modes |
| `integer`, `unimodular` | exactness, invertibility | exact pipelines, lattice bases, reversible transforms |

---

## What to produce → which plate → driven by

| Want to produce | Construction | Driven by |
|---|---|---|
| custom integer sequence / growth law | companion `C(p)` | `ρ` |
| deterministic fractal texture | Kronecker `A ⊗ B` | `M` |
| multi-voice sequence / multi-channel signal | direct sum `A ⊕ B` | `rank` |
| swirling, non-dissipative particle flow | commutator `[A,B]` | `tr = 0` |
| minimal-distortion 8-D quantizer / palette | Cartan `E₈` | `det = 1` |
| physical-sounding modal timbre | Cartan `Aₙ` | spectrum `λ_k` |
| frequency-domain synthesis / circular filter | circulant `↻` | DFT spectrum |
| spectral graph layout / signed diffusion | frustrated ring `∿` | `det` / `ρ` |
| reproducible noise / null model | random `⚄` | seed + `M` |

---

## Gotchas

- **Unbounded iteration.** If `ρ > 1`, `matpow(M,k)` and the flow `x ← Mx` blow up. Normalize `M ← M/ρ` to keep
  orbits bounded, or work in `BigInt` if you want the exact growth.
- **Kronecker size explosion.** `A ⊗ B` is `n·m × n·m`; iterating to level `L` gives `n^L`. Cap `L` for display.
- **Diffusion step size.** Explicit `diffuse` requires `dt < 2/ρ(L)`; otherwise it diverges.
- **Circulant length.** The first row length must equal the matrix order — the tool enforces this; preserve it on export.
- **Signed-ring balance.** Whether the frustrated ring is singular (`det = 0`) or frustrated (`det > 0`) depends on
  `n mod 4`. Read the `det` chip rather than assuming.
- **Root accuracy.** The spectrum uses Durand–Kerner; near-multiple eigenvalues converge slowly. Treat the plotted
  positions as visual, and use `det`/`tr` (exact, integer) for anything quantitative.
- **Non-integer seeds.** Non-monic ZFP values are not algebraic integers and are excluded from `companion` on
  purpose; do not reintroduce them if you want integer matrices downstream.

---

## Reproducibility

Every output is reproducible from `(construction, seed A, seed B, type, word, n, RNG seed)`. Log that tuple with
any artifact. The only stochastic source is the seeded PRNG, which is deterministic given its integer seed — so a
recorded tuple regenerates the exact matrix, hence the exact content.
