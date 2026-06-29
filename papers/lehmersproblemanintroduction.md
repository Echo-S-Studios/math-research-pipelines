# Lehmer's Problem: An Introduction

*A question first asked in 1933 that remains unresolved today — explained from the ground up, assuming no prior exposure.*

---

## The problem in one sentence

Lehmer's problem — named after the American number theorist **Derrick Henry Lehmer**, who raised it in 1933 — asks a deceptively simple question: among a natural notion of "size" attached to whole-number polynomials, is there a smallest size strictly greater than 1, or can that size be pushed arbitrarily close to 1 from above without ever equalling it? After more than ninety years, no one knows.

Stating it precisely needs exactly one definition.

---

## 1. The object: the Mahler measure

Take a polynomial with integer coefficients, written in terms of its complex roots $\alpha_1,\dots,\alpha_d$:

$$P(x) = a_d\,x^d + \cdots + a_0 = a_d \prod_{i=1}^{d}(x - \alpha_i), \qquad a_d \neq 0.$$

Its **Mahler measure** is

$$M(P) = |a_d| \prod_{i=1}^{d} \max\bigl(1, |\alpha_i|\bigr).$$

In words: take the leading coefficient, then multiply in the absolute value of every root that lies *outside* the unit circle. Roots on or inside the circle contribute a factor of 1 and drop out. There is an equivalent analytic formula (a consequence of Jensen's formula),

$$M(P) = \exp\!\left(\int_0^1 \log\bigl|P(e^{2\pi i\theta})\bigr|\,d\theta\right),$$

the exponential of the average of $\log|P|$ around the unit circle. The two definitions always agree.

A few concrete values make this tangible:

| Polynomial | Roots | Mahler measure |
|---|---|---|
| $x^2 + x + 1$ | $e^{\pm 2\pi i/3}$ — both *on* the unit circle | $M = 1$ |
| $x^2 - x - 1$ | $\varphi \approx 1.618$ and $-0.618$ | $M = \varphi \approx 1.618$ |
| $x^2 - 2$ | $\pm\sqrt2 \approx \pm 1.414$ — both outside | $M = 2$ |
| $x^{10}+x^9-x^7-x^6-x^5-x^4-x^3+x+1$ | one real root $\approx 1.17628$; the rest on/inside the circle | $M \approx 1.17628$ |

For $x^2 - x - 1$, only one root ($\varphi$) lies outside the circle, so $M = \varphi$. For $x^2 - 2$, both roots are outside, so $M = \sqrt2 \cdot \sqrt2 = 2$. For $x^2 + x + 1$, nothing is outside, so $M = 1$. The last row is the example everything turns on; we return to it.

---

## 2. Why 1 is a floor, and what sits exactly on it

For a monic integer polynomial (leading coefficient 1), $M(P)$ is a product of factors each $\geq 1$, so

$$M(P) \geq 1,$$

with equality exactly when *no* root lies outside the unit circle. A nineteenth-century theorem identifies that boundary case completely:

> **Kronecker's theorem (1857).** A monic integer polynomial whose roots all lie in the closed unit disk has every root equal to $0$ or to a root of unity. Hence $M(P) = 1$ if and only if $P$ is a product of cyclotomic polynomials and a power of $x$.

So the case $M = 1$ is fully understood: it is the "trivial" locus of roots of unity. All the difficulty lives just *above* 1.

---

## 3. The question Lehmer asked (1933)

Lehmer was building number sequences from polynomial roots (he was searching for large primes) and wanted to know how slowly such sequences could grow. That led him to the Mahler measure and to this question:

> **Is there a constant $c > 1$ such that every integer polynomial with $M(P) > 1$ satisfies $M(P) \geq c$?**

Equivalently: is $1$ an *isolated* point of the set of Mahler measures when approached from above — or do measures exist arbitrarily close to (but strictly greater than) 1?

Searching by hand, Lehmer found

$$L(x) = x^{10}+x^9-x^7-x^6-x^5-x^4-x^3+x+1,$$

with Mahler measure

$$M(L) = 1.176280818259917\ldots$$

This value, now called **Lehmer's number**, is the smallest Mahler measure greater than 1 that anyone has ever exhibited. It has held that record since 1933. No smaller example is known, and no proof exists that none can be smaller.

---

## 4. Two precise versions

The literature separates two statements of increasing strength:

- **Lehmer's problem (the weak, open form).** The infimum of Mahler measures greater than 1 is itself greater than 1 — i.e., *some* gap exists. Even this much is unproven.
- **Lehmer's conjecture (the strong form).** That infimum equals $M(L) \approx 1.17628$ and is attained by Lehmer's polynomial — i.e., $L$ is the true minimizer.

A proof of either would be a landmark. Both are open.

---

## 5. What is actually known

Progress is real but partial, and it splits along one decisive line: *reciprocal* versus *non-reciprocal* polynomials. A polynomial is **reciprocal** if its roots are closed under $\alpha \mapsto 1/\alpha$ (equivalently $x^{\deg P}P(1/x) = P(x)$); otherwise it is **non-reciprocal**.

| Result | Year | Scope | Statement |
|---|---|---|---|
| Kronecker | 1857 | all | $M = 1 \iff$ cyclotomic — the boundary case is settled |
| Smyth | 1971 | **non-reciprocal** $P$ | $M(P) \geq \theta_0 = 1.324717\ldots$, the *plastic number* (root of $x^3 - x - 1$, the smallest Pisot number) |
| Dobrowolski | 1979 | all non-cyclotomic, degree $d$ | $M(P) \geq 1 + c\left(\dfrac{\log\log d}{\log d}\right)^{3}$ |

Two things to read off this table:

- **Smyth's theorem completely solves Lehmer's problem for non-reciprocal polynomials.** There, the gap exists and its exact size is known: the plastic number $1.324717\ldots$. So the hard case is the reciprocal one — and note that Lehmer's own example $L$ is reciprocal.
- **Dobrowolski's bound applies to everything but decays to 1 as the degree grows.** For any fixed degree it gives a positive lower bound, but no *single* positive constant survives across all degrees at once. It comes tantalizingly close without closing the gap.

Beyond these, extensive computation has confirmed that no Mahler measure smaller than Lehmer's number exists among polynomials up to large degree — strong evidence for the conjecture, not a proof of it.

---

## 6. Why number theorists care: the height reformulation

The Mahler measure is a disguise for the **height** of an algebraic number. For an algebraic number $\alpha$ of degree $d$ with minimal polynomial $m_\alpha$, the absolute logarithmic Weil height satisfies

$$h(\alpha) = \frac{1}{d}\,\log M(m_\alpha).$$

Under this dictionary, Lehmer's conjecture becomes a statement about how *small* a height a non-trivial algebraic number can have:

> There is an absolute constant $c > 0$ such that every nonzero algebraic number $\alpha$ that is **not** a root of unity satisfies $h(\alpha) \geq c/\deg(\alpha)$.

Roots of unity have height $0$; the conjecture asserts that everything else is bounded away from $0$ at a controlled, degree-scaled rate. In this form the problem reaches into Diophantine geometry, the dynamics of toral automorphisms (where $\log M$ is a topological entropy), hyperbolic geometry (Salem numbers and short geodesics), and the arithmetic of special values of $L$-functions. That breadth is a large part of why it is considered important rather than merely curious.

---

## 7. Why it has resisted for over ninety years

Three concrete obstructions:

- **Uniformity in the degree.** One must control *all* polynomials of *every* degree with a single constant. The natural analytic estimates (Dobrowolski-type) inevitably weaken as the degree grows, so they cannot reach a uniform bound.
- **The hard case is structurally isolated.** Reciprocal polynomials — which contain all **Salem numbers** — are exactly where Smyth's clean argument does not apply. Lehmer's number is itself the smallest known Salem number, so the canonical example and the canonical obstruction are the same object.
- **Rigidity.** Perturbing a polynomial changes its measure discontinuously, as roots cross the unit circle and switch between contributing and not contributing. Smoothing and continuity techniques therefore gain no traction.

---

## 8. Where the live frontier sits

Stripped to its core, the open part of Lehmer's problem is one question about a single family of numbers:

> **Are Salem numbers bounded away from 1? Equivalently, is there a smallest Salem number — and is it Lehmer's $1.17628\ldots$?**

The non-reciprocal half is finished (Smyth: floor $= 1.324717\ldots$, the plastic number). The reciprocal/Salem half is the unsolved heart of the problem. This is precisely the boundary that any construction built on Mahler measures inherits: for non-reciprocal seeds a clean, unconditional cost floor is available off the shelf, whereas the reciprocal case can only be handled *structurally* — by closure or field-confinement arguments that prevent the problematic objects from arising — rather than by invoking a settled lower bound, because no such bound is known to exist.

---

## References (verify before citing)

I don't have live access to a citation database, so confirm bibliographic details before relying on them:

- D. H. Lehmer, *Factorization of certain cyclotomic functions*, **Annals of Mathematics** (2nd series) **34** (1933) — the original question and the degree-10 example.
- L. Kronecker, *Zwei Sätze über Gleichungen mit ganzzahligen Coefficienten*, **Crelle's Journal** (1857) — the $M = 1$ classification.
- C. J. Smyth, *On the product of the conjugates outside the unit circle of an algebraic integer*, **Bulletin of the London Mathematical Society** **3** (1971) — the non-reciprocal bound (plastic number).
- E. Dobrowolski, *On a question of Lehmer and the number of irreducible factors of a polynomial*, **Acta Arithmetica** **34** (1979) — the degree-dependent bound; explicit constants later by P. Voutier (1996).
- D. Lind, K. Schmidt, T. Ward, *Mahler measure and entropy for commuting automorphisms of compact groups*, **Inventiones Mathematicae** (1990) — the dynamical-entropy connection.
- C. J. Smyth, *The Mahler measure of algebraic numbers: a survey* (2008) — a readable modern overview.
