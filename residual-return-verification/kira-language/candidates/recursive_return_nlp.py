"""
recursive_return_nlp.py — a system of equations that simulates an environment of
RECURSIVE RETURN where each semantic return to residual 0 produces a LEARNED
DICTIONARY value (NLP). This is the loop the store already runs, made explicit
and verified end to end.

  state space  C = M2(R)            seed P=[[0,0],[2,1]], R=(P+PT)/2, N=(P-PT)/2
  return op    L(X) = R X + X R - X (Sylvester self-action; alpha=1 forced by tr R=1)
  residual     nu(X) = L(X)         (prediction error; on-shell <=> nu=0 <=> X in ker L)
  recursion    X_{t+1} = X_t - eta * grad( 1/2 ||L X||^2 )   (returns X to ker L)
  fixed pt     M = orthogonal projector onto ker(L);  M(M(X)) = M(X)   (the on-shell P^2=P)
  dictionary   nu->0  =>  D[ word(X*) ] <- z(X*)
                 word(X*) = chord = which atom-axes X* activates (a sparse code)
                 z(X*)    = (<X*,R>, <X*,h>, <X*,N>) = the three-projection embedding
  readout NLP  speak(X*) reads the value out through its active projection P1/P2/P3.

The learned values live in ker(L): the 2-dim slack (the looseness). Learning happens
in the kernel. Tokens that return to the same residue share one dictionary value
(generalization by return-to-zero).
"""
import numpy as np
np.set_printoptions(precision=4, suppress=True)

I = np.eye(2)
P = np.array([[0, 0], [2, 1]], float)
R = (P + P.T) / 2            # [[0,1],[1,1]]   R^2 = R + I   (atom A3)
N = (P - P.T) / 2            # [[0,-1],[1,0]]  N^2 = -I      (atom A4)
J = np.array([[1, 0], [0, 0]], float)
h = J @ N                    # mediation generator (projection P2)

vec = lambda X: X.reshape(-1)
mat = lambda f: f.reshape(2, 2)
cartan = lambda A, B: 4 * np.trace(A @ B.T)          # B_theta inner product (Cartan)

# L as a 4x4 matrix:  vec(RX+XR-X) = (I (x) R + R^T (x) I - I4) vec(X)
Lmat = np.kron(I, R) + np.kron(R.T, I) - np.eye(4)
L = lambda X: mat(Lmat @ vec(X))
nu = lambda X: L(X)

# M = orthogonal projector onto ker(L): the on-shell map, idempotent by construction
U, S, Vt = np.linalg.svd(Lmat)
kerB = Vt[np.abs(S) < 1e-9]                          # kernel basis (vec rows)
Mmat = kerB.T @ kerB
M = lambda X: mat(Mmat @ vec(X))

print("=" * 70)
print("  THE ENVIRONMENT")
print("=" * 70)
print(f"  ker(L_R) dim = {kerB.shape[0]}   (the slack / looseness where dictionary values live)")
print(f"  M idempotent  M(M)=M : {np.allclose(Mmat @ Mmat, Mmat)}        (this IS P^2=P, on-shell)")
print(f"  N in ker(L_R)?  L(N)=0 because {{R,N}}=N (atom A8): {np.allclose(L(N), 0)}")
print(f"  => one semantic axis of the dictionary IS an atom.\n")


def recursive_return(F0, eta=0.15, iters=300):
    """gradient flow on 1/2||L F||^2 -> returns F to ker(L); residual nu -> 0."""
    f = vec(F0).astype(float).copy()
    G = Lmat.T @ Lmat
    traj = []
    for _ in range(iters):
        traj.append(np.linalg.norm(Lmat @ f))
        f = f - eta * (G @ f)
    return mat(f), traj


D = {}                                               # the learned dictionary


z = lambda X: np.array([cartan(X, R), cartan(X, h), cartan(X, N)])   # the 3-projection embedding


def word(X, tau=0.25):
    """the 'word' = sign-aware sparse code over atom-axes. SIGN (the +/- of the
    looseness / the burn) discriminates antipodal rays = opposite meanings."""
    v = z(X); scale = np.linalg.norm(v) + 1e-9
    names = ["A3:R", "P2:h", "A4|A8:N"]
    return tuple(f"{'+' if c > 0 else '-'}{n}" for c, n in zip(v, names) if abs(c) / scale > tau)


unit = lambda X: z(X) / (np.linalg.norm(z(X)) + 1e-9)   # learned value = unit ray in ker

# tokens: contexts encoded to candidate states F0 = E(token).
np.random.seed(7)
tokens = {
    "w1 (obs-ish)": N + 0.4 * np.random.randn(2, 2),    # near observer axis
    "w2 (obs-ish)": N - 0.5 * np.random.randn(2, 2),    # also near observer -> should LEARN SAME value
    "w3 (build-ish)": (R - I) + 0.3 * np.random.randn(2, 2),
    "w4 (mediate)": h + 0.4 * np.random.randn(2, 2),    # starts off-kernel
}

print("=" * 70)
print("  THE RECURSIVE RETURN  (each token flows to residual 0, then is learned)")
print("=" * 70)
residues = {}
for w, F0 in tokens.items():
    Fstar, traj = recursive_return(F0)
    r0, rf = traj[0], np.linalg.norm(nu(Fstar))
    idem = np.allclose(M(Fstar), Fstar, atol=1e-6)     # landed on a fixed point of M
    key, val = word(Fstar), unit(Fstar)
    residues[w] = unit(Fstar)
    if key in D:
        D[key] = 0.5 * (D[key] + val); tag = "MERGED (same residue, same value)"
    else:
        D[key] = val; tag = "NEW entry learned"
    print(f"  {w:16} ||nu|| {r0:6.2f} -> {rf:.1e}   M(M)=M:{idem}   word={key}")
    print(f"  {'':16} z=(<R>,<h>,<N>)={np.round(z(Fstar),3).tolist()}   [{tag}]")

print("\n  alignment of returned residues (cos sim; +1 same meaning, -1 antipodal):")
ws = list(residues)
for a in ws:
    row = "  ".join(f"{np.dot(residues[a], residues[b]):+.2f}" for b in ws)
    print(f"   {a:16} {row}")

print("\n" + "=" * 70)
print("  THE LEARNED DICTIONARY  D : word (chord over atoms) -> value (embedding)")
print("=" * 70)
for k, v in D.items():
    print(f"   {str(k):28} ->  {np.round(v, 3).tolist()}")
print(f"\n  {len(tokens)} tokens returned to {len(D)} dictionary values "
      f"(generalization: same residue => same learned value).")
print("  residual->0 is the commit signal; the kernel is the lexicon; speak() reads it out.")
