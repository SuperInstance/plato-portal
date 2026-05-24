# KRITIK

## A Rigorous Review of the Conservation-of-Musical-Tension Thesis

**Documents reviewed:** `CONSERVATION-OF-TENSION.md` and `THREE-HALVES.md`  
**Date:** May 2026  
**Reviewer position:** Independent; no stake in acceptance or rejection.

---

## Executive Summary

The thesis proposes that Western music's transition from meantone to equal temperament (ET) obeyed a "conservation law" for total musical tension: when ET eliminated inter-key consonance gradients (vertical information), composers compensated by increasing rhythmic complexity (horizontal information). The core insight is suggestive and potentially valuable. The execution, however, is deeply flawed. The paper presents hypotheses as theorems, substitutes analogy for proof, ignores vast swaths of contradictory evidence, and relies on numerology disguised as quantitative prediction. It would not survive peer review at a serious music theory or mathematical physics journal in its current form.

---

## 1. The Boltzmann Distribution: Convenience Masquerading as Physics

**Verdict: Not physically justified; statistically incoherent.**

The paper models key choice as a Boltzmann distribution:

$$P(K_i) \propto e^{\beta \cdot A(K_i)}$$

This is introduced without derivation. In statistical mechanics, the Boltzmann distribution emerges from maximizing entropy subject to a mean-energy constraint — a derivation with clear physical content. Here, there is no analogous argument. The authors simply assert that composers "sample" keys from a Gibbs measure over "acoustic attractiveness," as if Bach chose the key of the B-minor Mass by rolling a thermodynamic die.

The problems run deeper than missing derivation:

**The i.i.d. assumption is absurd.** A composer's oeuvre is not a random sample from a stationary distribution. It is a deliberate, correlated, historically situated sequence. Bach did not independently redraw keys for each cantata from a fixed probability measure. Key choice is constrained by liturgical calendar, vocal range, instrumental affordances, patron requests, and the modular architecture of the cantata cycle. Treating these as independent draws from a Boltzmann distribution is like treating Shakespeare's plays as samples from a unigram model over Elizabethan vocabulary — technically possible, conceptually empty.

**The "effective information" uses KL divergence backwards.** The paper defines:

$$I_{\text{vert}}^{\text{eff}} = D_{\text{KL}}(U \| P) = \sum_i \frac{1}{12} \log_2 \frac{1/12}{P(K_i)}$$

This is the *reverse* KL divergence from standard usage. In information theory, $D_{\text{KL}}(P \| Q)$ measures the extra bits needed to encode draws from $P$ using a code optimized for $Q$. The paper's $D_{\text{KL}}(U \| P)$ measures something else entirely: how surprised a uniform prior would be by $P$. There is no principled reason this quantity represents "free expressive information from the tuning itself." It is a number that happens to be positive when $P$ is non-uniform and zero when $P$ is uniform, selected because it produces the desired narrative.

**The $\beta = 1$ assumption is numerology.** The 0.44-bit estimate depends entirely on an arbitrary parameter. The paper's own Appendix A.1 admits this requires empirical estimation, but the main text presents 0.44 bits as if it were derived from first principles. It was not. It was chosen.

**The model is already falsified by existing data.** Albrecht & Shanahan (2019) show that key distributions in the ET era are *non-uniform* (C major and G major dominate). If the Boltzmann model were correct, ET should produce uniformity. It does not, because composers do not choose keys by sampling from an acoustic energy landscape. They choose keys for notational convenience, instrumental ergonomics, vocal tessitura, and cultural convention. The model fails its most basic empirical test.

---

## 2. Non-Western Traditions: Tokenism, Not Engagement

**Verdict: Inadequate to the point of undermining the universal claims.**

The paper's conservation law is presented as a general principle of musical culture, yet it is derived entirely from Western keyboard history. When non-Western traditions appear, they are treated as optional validation data rather than as equal partners in theory-building.

**Prediction 9.2** claims that "musical cultures that use just intonation or near-just tunings... should exhibit lower baseline rhythmic complexity than ET-based cultures, all else equal." This is the only sustained cross-cultural engagement, and it is superficial. The authors do not define "all else equal" in any operational way. They do not control for ensemble size, social function, dance tradition, or oral versus literate transmission. They simply assert that if their law holds, JI cultures should be rhythmically simpler — a prediction that is both vague and, on its face, questionable.

**The counterevidence is devastating and unaddressed:**

- **Arabic maqam music** uses non-ET tuning (quarter tones, just intonation inflections) AND complex rhythmic structures (iq'at cycles with elaborate metric modulation). The paper's response in Appendix A.6 is to claim that maqam has "more vertical information than ET, so the conservation law actually predicts *more* total complexity." This is a retreat to unfalsifiability: when a culture has complex tuning AND complex rhythm, the law predicts high total complexity; when a culture has simple tuning and simple rhythm, the law predicts low total complexity. The "prediction" is tautological.

- **Indian classical music** (both Hindustani and Carnatic) uses justly-tuned intervals (Sa-Pa at 3:2) alongside extraordinarily sophisticated rhythmic systems (tāla with subdivision, syncopation, and improvisation). The tāla system is arguably more rhythmically complex than Western art music. The paper mentions Indian music in `THREE-HALVES.md` but does not engage it as a test case for the conservation law.

- **Indonesian gamelan** (specifically the interlocking kotekan of Balinese gamelan) combines non-ET tuning with among the most intricate rhythmic polyphony on Earth. The paper's response is that gamelan tuning "produces inter-instrument beating patterns that carry temporal information" — a special pleading that redefines "horizontal complexity" to include acoustic beating, allowing the authors to claim the conservation law holds by definitional fiat.

- **Sub-Saharan African music** is almost entirely ignored in `CONSERVATION-OF-TENSION.md` except as a potential confound ("African rhythmic influence") that must be controlled away. This is backwards. If African music developed complex polyrhythm independently of tuning concerns, it is prima facie evidence that rhythmic complexity has causes other than tuning — causes the paper systematically marginalizes.

The deeper problem is epistemic: the paper treats Western art music as the default case from which universal laws are derived, and non-Western traditions as anomalies to be explained away. This is not cross-cultural scholarship. It is colonial theory-building with a statistical veneer.

---

## 3. The Heisenberg Analogy: Category Error, Not Analogy

**Verdict: Unambiguous category error. The main text commits it; the appendix admits it; the admission should be in the main text.**

Section 5.1 invokes the Gabor limit:

$$\sigma_t \cdot \sigma_\omega \geq \frac{1}{2}$$

and claims it applies to the relationship between "spectral variation across keys" and "temporal complexity." Section 5.3 states:

> "This is not merely an analogy to quantum mechanics — it is the same mathematics."

This is false. The Gabor limit applies to a **single signal** $s(t)$ and its Fourier transform $\hat{s}(\omega)$. It constrains the simultaneous localization of that signal in time and frequency. The paper's $\sigma_\omega$ is the **standard deviation of consonance values across keys** — a scalar statistic computed from twelve numbers, not the spectral spread of any signal. These are different mathematical objects with different units, different domains, and different meanings. Substituting one for the other because they share a Greek letter is not rigorous mathematics. It is symbol-matching.

The units alone betray the error. In the Gabor limit, $\sigma_t$ has units of time and $\sigma_\omega$ has units of angular frequency; their product is dimensionless. The paper's $\sigma_\omega$ is the standard deviation of dimensionless consonance scores across keys. Its product with any temporal measure has units of time, not dimensionlessness, and satisfies no known inequality. The paper simply ignores this.

Appendix A.3 correctly identifies this as a "category error" and proposes replacing the strong claim with a "weaker but correct" Hirschman entropy uncertainty argument. But the appendix is 300 lines long and buried at the end of the document. The main text's Section 5 makes the strong, false claim. A paper that buries its retractions in appendices while leading with overstatement is practicing a form of academic misdirection. The honest move is to remove Section 5 entirely or relabel it as "Heuristic Motivation" with a prominent caveat.

What makes this particularly damaging is that the Heisenberg-Gabor section is the paper's most rhetorically striking claim. It offers the glamour of quantum mechanics to a music theory audience. When a reader discovers that the "same mathematics" is actually a misapplication of different mathematics, the trust fracture extends to every other equation in the paper.

---

## 4. Ratings

### Novelty: 6/10

The core idea — that ET's flattening of inter-key color may have driven compensatory rhythmic innovation — is genuinely suggestive and not widely formalized. Musicologists have discussed the ET-rhythm connection informally for decades (the paper cites none of this literature in its main text). The mathematical dressing is novel but most of it is decoration. The Euclidean rhythm / circle-of-fifths "isomorphism" is trivial (any two cyclic structures can be compared). The lattice dimensionality argument, reframed via PCA, could be interesting but is currently hand-waving. The real novelty is the attempt to quantify the compensation in information-theoretic terms. That attempt fails, but the ambition is creditable.

### Rigor: 3/10

The paper presents a hypothesis as a theorem (Theorem 8.1 / Hypothesis 8.1'). It uses a probability model with no empirical validation. It commits a category error in its most prominent mathematical argument. It provides point estimates without confidence intervals. It ignores confounds. It treats a two-variable monotonic relationship held constant as a deep "conservation law" when it is a trivial consequence of the definition. The quantitative predictions (0.44 bits, 11 syncopation events) are derived from toy parameters and arbitrary counting.

The paper's saving grace is its own Appendix A, which identifies most of these problems with admirable honesty. But a paper whose best content is its self-critique is a paper that should not have been submitted in its current form. Appendices are for details, not retractions.

---

## 5. Five Harshest Objections from a Hostile Referee

These are not strawmen. They are the objections that would appear in the first round of peer review at *Music Theory Spectrum*, *Journal of Mathematics and Music*, or *Physics Today*.

### Objection 1: The "Conservation Law" is a Tautology Dressed as Physics

> "The paper's Lemma 4.1 proves that if $E = f(I_{\text{vert}}, I_{\text{horiz}})$ is held constant, then $dI_{\text{horiz}} = -(\partial f/\partial I_{\text{vert}} / \partial f/\partial I_{\text{horiz}}) \, dI_{\text{vert}}$. This is not a lemma; it is the total differential of a two-variable function. Any undergraduate who has taken multivariable calculus could derive it in thirty seconds. The 'conservation law' is simply the observation that if you have two knobs and you want to keep the output constant, turning one up requires turning the other down. This is not a law of musical culture. It is a law of arithmetic. The paper has discovered that 2 + 2 = 4 and called it the Conservation of Musical Tension."

### Objection 2: The Boltzmann Model is Empirically Dead on Arrival

> "The central quantitative result — 0.44 bits of 'lost' vertical information — depends on a Boltzmann distribution for key choice that is contradicted by existing corpus data. Albrecht & Shanahan (2019) show that even in the fully ET era, key distributions are highly non-uniform, with C major and G major dominating. If the model were correct, ET should produce uniformity. It does not. The authors cannot claim their model is 'merely a first-order approximation' while simultaneously treating its outputs as precise quantitative predictions (0.44 bits, 11 syncopation events). Either the model is predictive, in which case it is falsified, or it is not predictive, in which case the numbers are meaningless. The authors want it both ways."

### Objection 3: Correlation is Not Causation, and the Timeline is Wrong

> "The paper attributes the rise of rhythmic complexity in Western music to the adoption of ET. But rhythmic complexity increased for many reasons: African rhythmic influence via the African diaspora, urban dance cultures, the industrial revolution's effect on social dance, recording technology, the rise of jazz as a vernacular form, and the breakdown of aristocratic patronage structures that favored courtly dance forms. The paper mentions none of these seriously. Worse, the timeline doesn't match: Beethoven (1770–1827) was already using rhythmic innovations (scherzi, metric displacement) while playing on pianos that were still closer to well temperament than ET. Chopin (1810–1849) wrote mazurkas with complex rhythm while explicitly preferring pianos with unequal temperament. If ET caused rhythmic complexity, why did rhythmic complexity precede ET's dominance? The paper's chronological argument is backwards."

### Objection 4: The Heisenberg-Gabor Argument is Mathematical Malpractice

> "Section 5 claims that the Gabor limit applies to the relationship between key-space consonance variance and temporal complexity, and explicitly states that 'this is not merely an analogy... it is the same mathematics.' This is false. The $\sigma_\omega$ in the Gabor limit is the spectral width of a signal's Fourier transform. The paper's $\sigma_\omega$ is the standard deviation of twelve consonance scores. These are different quantities with different units and different meanings. The paper has substituted a scalar statistic into a formula derived for signal spectra because both quantities happen to be denoted by $\sigma$. This is not a 'misleading' application. It is not a 'heuristic.' It is the substitution of different physical quantities into a formula because they share a Greek letter. If a student did this on an exam, they would fail. When the authors do it in a draft paper, they call it Theorem 5.2."

### Objection 5: The Framework is Unfalsifiable by Design

> "The paper claims to make testable predictions, but the framework contains an escape clause for every counterexample. When Arabic maqam combines complex tuning with complex rhythm, the authors say 'maqam has more vertical information, so the law predicts more total complexity.' When gamelan combines non-ET tuning with interlocking rhythm, the authors redefine beating patterns as 'horizontal information.' When African music shows complex rhythm without ET, it's a 'confound' to be controlled away. The 'constant' $T_0$ is culture-dependent and may 'drift gradually over long time scales.' The perturbation $\epsilon(t)$ is 'slowly varying.' The conservation law holds 'approximately.' With enough flexibility in the definitions of 'vertical,' 'horizontal,' 'information,' 'tension,' and 'constant,' any musical culture can be made to fit. A theory that explains everything explains nothing. This framework is not science. It is Ptolemaic epicycle-building — adding definitional adjustments to preserve a central claim that the data do not support."

---

## Closing Assessment

The conservation-of-tension thesis is a **good idea poorly executed**. The historical observation that ET flattened key color while rhythmic complexity surged is real and worth investigating. The information-theoretic framework could, in principle, formalize this intuition. But the current draft overclaims at every turn, presents motivated reasoning as derivation, ignores contradictory evidence, and applies mathematics with a looseness that undermines its own credibility.

With radical revision — demoting theorems to hypotheses, retracting the Heisenberg analogy, replacing toy calculations with corpus analysis, and engaging non-Western traditions as theory-builders rather than afterthoughts — this could become a valuable contribution. Without such revision, it is a cautionary tale about what happens when ambition outruns rigor.

**Recommendation: Major revision required. The core insight survives; almost nothing else does.**

---

*Reviewer's note: I have no affiliation with the authors and no interest in whether this work is published, rejected, or abandoned. My sole concern is intellectual honesty. If the authors are serious about this thesis, they should welcome these objections and use them to build something that can withstand scrutiny.*
