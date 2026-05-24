# Conservation of Musical Tension: Information-Theoretic Evidence for Horizontal Compensation After Temperament Standardization

---

## Abstract

We present an information-theoretic framework for investigating whether the standardization of equal temperament (ET) in Western art music contributed to the intensification and persistence of rhythmic complexity. When ET eliminated the gradient structure of the consonance field across keys—rendering all twelve major keys acoustically identical—composers lost a vertical (harmonic) information channel that had carried ~0.4 bits of expressive content per key-choice event under meantone temperament. We formalize this loss using Shannon entropy on key-choice distributions, gradient analysis of consonance fields, and a heuristic time-frequency analogy. We propose the *Conservation Hypothesis*: that total musical information content is distributed across multiple channels (harmonic, rhythmic, timbral), and that the reduction of one channel pressures compensation in others. We acknowledge significant counter-evidence—notably the Ars Subtilior (c. 1375–1410), which achieved extraordinary rhythmic complexity centuries before ET, and non-Western traditions (Indian tala, African polyrhythm) that developed sophisticated rhythm without ET. We argue that ET did not *cause* rhythmic complexity but *contributed to its persistence and intensification* in the Western tradition by removing a previously available expressive resource. We offer five falsifiable predictions with test methodologies and discuss extensions to timbral and formal dimensions. The framework, while not constituting a proof, provides quantitative tools for a hypothesis that has circulated informally in music theory for decades.

**Keywords:** equal temperament, meantone temperament, information theory, rhythmic complexity, consonance gradient, hemiola, conservation law, music cognition

---

## 1. Introduction

### 1.1 Framing the Question

In quarter-comma meantone temperament (c. 1500–1700), C major and F♯ major were not merely different keys—they were acoustically different *sounds*. C major's major third was a pure 5:4 ratio (386 cents); F♯ major's was a wretched 427 cents, nearly a quarter-tone sharper. The wolf fifth, concentrated in a single interval of ~738 cents, rendered several keys literally unplayable. Each key possessed a distinct acoustic fingerprint: its own interval sizes, its own beating patterns, its own consonance profile. When Johann Mattheson catalogued the emotional characters of seventeen keys in 1713 (*Das neu-eröffnete Orchestre*), he was describing acoustic reality, not convention.

Equal temperament (12-TET) abolished this world. By dividing the octave into twelve exactly equal semitones of 100 cents each, ET made every major third 400 cents, every perfect fifth 700 cents, regardless of key. The twelve keys became acoustically interchangeable. The Affektenlehre—the doctrine of key characters—lost its physical basis and survived only as cultural memory.

Yet music did not become less expressive. Instead, the centuries following ET's standardization witnessed an extraordinary flowering of rhythmic complexity: Beethoven's motivic rhythm, Chopin's polyrhythms, Brahms's pervasive hemiolas, Stravinsky's metric fragmentation, Nancarrow's tempo canons of irrational ratios, and the polyrhythmic architecture of jazz. This paper asks: *is there a systematic connection between the loss of vertical (harmonic) information and the gain of horizontal (rhythmic) information?*

### 1.2 Acknowledging Counter-Evidence Upfront

Any hypothesis connecting ET to rhythmic complexity must immediately confront a formidable obstacle: the Ars Subtilior. Around 1380—three centuries before ET existed, two centuries before meantone dominated—composers centered on the papal court at Avignon produced music of rhythmic complexity that Richard Hoppin described as unmatched "until the twentieth century." Mensuration canons, prolation canons, simultaneous proportional tempi, and extreme notational innovation characterize this repertoire. Johannes Ockeghem's *Missa Prolationum* (c. 1470) achieves through mensural notation what Conlon Nancarrow would achieve through player pianos 480 years later.

Furthermore, non-Western traditions complicate the picture decisively. Indian classical music, built on just-intonation śruti, possesses the tala system—one of the most sophisticated rhythmic frameworks on the planet. Sub-Saharan African traditions, operating entirely outside any temperament framework, are arguably the most rhythmically complex musical cultures that exist. Arabic maqam music couples microtonal tuning with complex iq'at rhythmic cycles.

We state at the outset: **ET is neither necessary nor sufficient for rhythmic complexity.** The evidence clearly shows that extraordinary rhythmic sophistication can arise from social competition (Ars Subtilior courtly one-upmanship), notational affordance (mensural notation), and cultural traditions entirely independent of Western tuning history.

The refined thesis of this paper is therefore modest: *ET contributed to the persistence and intensification of rhythmic complexity in the Western art music tradition by removing a previously available channel of vertical expressiveness.* Before ET, rhythmic complexity was possible but optional—localized, reversible, driven by specific social conditions. After ET, rhythmic complexity became a more structurally persistent feature of Western compositional practice, because one of the reasons composers had not previously needed to rely on it—the rich vertical expressiveness of tuned key-relationships—was no longer available.

### 1.3 Paper Structure

Section 2 provides historical background on the meantone-to-ET transition. Section 3 develops the information-theoretic framework. Section 4 presents the consonance gradient analysis. Section 5 offers a heuristic time-frequency argument. Section 6 examines the dimensionality of the consonance field using PCA intrinsic dimension. Section 7 assembles the chronological evidence. Section 8 addresses counter-evidence in detail. Section 9 states the refined thesis. Section 10 explores extensions to timbral and other dimensions. Section 11 presents falsifiable predictions. Section 12 concludes.

---

## 2. Background: The Meantone-to-ET Transition

### 2.1 Quarter-Comma Meantone (c. 1490–1700)

Quarter-comma meantone, first described by Pietro Aaron in *Thoscanello de la musica* (1523), dominated European keyboard tuning for roughly two centuries. It sacrificed eleven perfect fifths (narrowing each by ~5.4 cents to achieve pure major thirds) in order to make the most commonly used thirds—those in keys near C major—perfectly consonant at 386.3 cents (a 5:4 ratio). The residual "wolf" fifth, typically G♯–E♭, measured ~737.6 cents—a deviation of +35.6 cents from pure, audibly wretched.

The practical consequence was dramatic variation in key quality. The six "good" keys (C, G, D, A, F, B♭) possessed pure or near-pure thirds and consonant fifths. The two "bad" keys (F♯, G♭) contained the wolf interval and unusable triads. Between these extremes lay a gradient of acceptability. As Kyle Gann has documented, surveying the Fitzwilliam Virginal Book (c. 1620) reveals near-zero pieces in signatures beyond two sharps or flats. Orlando Gibbons's *Lord Salisbury Pavane* (c. 1610) in A minor uses F, G, C, E, and D major triads but *never* F♯ major—because it literally did not exist on his instrument. Key choice was not arbitrary; it was an acoustic decision.

The key cents chart for quarter-comma meantone (from Jorgensen 1991) reveals the source of this variation:

| Pitch | Cents from C |
|-------|-------------|
| C | 0.0 |
| C♯ | 76.0 |
| D | 193.2 |
| E♭ | 310.3 |
| E | 386.3 |
| F | 503.4 |
| F♯ | 579.5 |
| G | 696.8 |
| G♯ | 772.6 |
| A | 889.7 |
| B♭ | 1006.8 |
| B | 1082.9 |

Note the unequal semitones: C–C♯ spans 76 cents while C♯–D spans 117 cents—nearly a quarter-tone difference. Each key was a different acoustic world.

### 2.2 Well Temperament (c. 1700–1850)

The transition from meantone to ET was gradual, not abrupt. Werckmeister III (1691) was a well-temperament—not equal temperament—that made all 24 keys playable while preserving distinct characters. Keys near C sounded "sweet" with near-pure thirds; distant keys sounded progressively sharper and more tense. Kirnberger III (1779), developed by a student of J.S. Bach, still had distinctly unequal intervals—near-pure thirds in C, G, D, A major.

Bach's *Well-Tempered Clavier* (1722) was titled for a temperament that made all keys *usable*, not *equal*. Bradley Lehman's 2005 analysis of the decorative "squiggle" on Bach's autograph manuscript interprets it as a tuning diagram for a specific unequal temperament. While this interpretation remains debated, the scholarly consensus holds that Bach did not use ET. Bach once tormented the organ builder Gottfried Silbermann by playing sour A♭-major triads on one of Silbermann's meantone organs—demonstrating his desire to use all keys while expressing frustration at the limitations of unequal tuning.

### 2.3 The Late Arrival of True ET

Contrary to popular assumption, exact equal temperament was not achievable on pianos until 1917, when William Braid White published the first precise tuning method. During the 19th century, keyboard tuning drifted closer to ET "over the protest of many of the more sensitive musicians" (Gann). Broadwood and Steinway transitioned through the mid-to-late 19th century, but the results were approximate—de facto well-temperaments, not true ET. Giuseppe Tartini called ET *un musicidio* ("a music-killing"); Rousseau argued it destroyed the emotional character of keys. The drift toward uniformity happened despite, not because of, aesthetic preference.

### 2.4 What Was Lost

The transition from meantone to ET eliminated several concrete resources:

1. **Key-character gradients.** In meantone, moving from C major to E major was an acoustic event—the intervals literally changed size. In ET, it is merely a transposition.

2. **Pure intervals at structurally important locations.** The meantone major third (386 cents, ratio 5:4) had zero beating. The ET major third (400 cents) beats audibly—a 14-cent deviation that sensitive listeners find restless.

3. **The Affektenlehre as acoustic reality.** Mattheson's key characters, Rousseau's key descriptions, and Heinichen's "Musical Circle" all presupposed unequal temperament. These were not metaphors.

4. **Compositional constraint from tuning.** Gibbons could not modulate to F♯ major because it did not exist. This constraint was also a resource: it made every key-choice meaningful, every modulation an event with audible acoustic consequences.

---

## 3. The Information-Theoretic Framework

### 3.1 Harmonic Information Content

Let $\mathcal{K} = \{K_1, \ldots, K_{12}\}$ be the set of major keys. For each key $K_i$, define its *acoustic attractiveness* $A(K_i)$ as the sum of consonance scores for all diatonic intervals within that key:

$$A(K_i) = \sum_{j \in \text{diatonic}(K_i)} C(r_j)$$

where $C(r)$ is a consonance function mapping frequency ratios to consonance values in $[0,1]$.

**Definition 3.1 (Acoustic Component of Key Choice).** Under the hypothesis that acoustic consonance is one of several independent factors influencing key choice, and following McFadden's (1974) discrete choice framework, the acoustic contribution to key preference is modeled as:

$$P_{\text{acoustic}}(K_i) = \frac{e^{\beta \cdot A(K_i)}}{\sum_{j=1}^{12} e^{\beta \cdot A(K_j)}}$$

where $\beta > 0$ parameterizes the weight of acoustic factors relative to other factors (instrumental convenience, vocal range, notational simplicity, symbolic associations). The total key-choice distribution is then $P(K_i) \propto P_{\text{acoustic}}(K_i) \cdot P_{\text{other}}(K_i)$.

This formulation grounds the model in discrete choice theory, which derives multinomial logit (Boltzmann-like) distributions from axioms about utility-maximizing agents. It makes $\beta$ an empirical parameter to be estimated, not assumed, and clarifies that the information measures derived below capture only the *acoustic* component of vertical information.

**Definition 3.2 (Vertical Information).** The effective vertical information content of a tuning system $\mathcal{T}$ is:

$$I_{\text{vert}}^{\text{eff}}(\mathcal{T}) = D_{\text{KL}}(U \| P) = \sum_{i=1}^{12} \frac{1}{12} \log_2 \frac{1/12}{P(K_i)}$$

This is the Kullback-Leibler divergence from the uniform distribution—measuring how much the acoustic properties of the tuning make certain keys more attractive than others, relative to the ET baseline where all keys are equally viable.

### 3.2 The ET Limit

In 12-TET, all keys have identical acoustic properties: $A(K_1) = A(K_2) = \cdots = A(K_{12})$. Therefore $P(K_i) = 1/12$ for all $i$, and:

$$I_{\text{vert}}^{\text{eff}}(\text{ET}) = 0$$

In quarter-comma meantone, the six "good" keys have higher $A(K_i)$ due to purer thirds and fifths, while the two "bad" keys have lower $A(K_i)$ due to the wolf interval. For $\beta = 1$ (a toy estimate requiring empirical calibration), we estimate:

$$I_{\text{vert}}^{\text{eff}}(\text{meantone}) \approx 0.44 \text{ bits per key-choice event}$$

This figure should be treated as provisional. It depends on the consonance function $C(r)$ and the parameter $\beta$, both of which require empirical estimation from historical key-distribution data. A sensitivity analysis (see Section 11) shows $I_{\text{vert}}^{\text{eff}} \in [0.2, 0.8]$ for the plausible range $\beta \in [0.3, 3.0]$ across common meantone variants (quarter-comma, third-comma, Werckmeister III, Vallotti).

**The substantive point:** Meantone-era composers had approximately 0.2–0.8 bits per key-choice event of "free" expressive information from the tuning itself—information that ET eliminated entirely. A typical Baroque work with ~100 key-choice events (chord changes, modulations) thus carried ~20–80 bits of vertical information from tuning, lost under ET.

### 3.3 Horizontal Information

**Definition 3.3 (Rhythmic State Space).** A rhythmic state is a binary vector $\mathbf{r} = (r_1, \ldots, r_n) \in \{0,1\}^n$, where $r_i = 1$ indicates an onset at position $i$ within a metrical cycle of length $n$.

**Definition 3.4 (Horizontal Information).** Given a distribution $Q(\mathbf{r})$ over rhythmic states:

$$I_{\text{horiz}} = -\sum_{\mathbf{r}} Q(\mathbf{r}) \log_2 Q(\mathbf{r}) = H(\mathbf{r})$$

This is the Shannon entropy of the onset distribution—the number of bits required to specify which positions within a metrical cycle contain onsets.

**Definition 3.5 (Syncopation Index).** For a rhythm $\mathbf{r}$ in meter $\mathbf{m}$:

$$S(\mathbf{r}, \mathbf{m}) = \sum_{i=1}^{n} \max(w_i^{\mathbf{m}} - w_i^{\mathbf{r}}, 0)$$

where $w_i^{\mathbf{m}}$ is the metric weight at position $i$ and $w_i^{\mathbf{r}}$ is the onset weight. The horizontal tension is:

$$T_{\text{horiz}} = \mathbb{E}[S(\mathbf{r}, \mathbf{m})] + \lambda \cdot P_{\text{polyrhythmic}}$$

where $P_{\text{polyrhythmic}}$ captures cross-rhythmic and polyrhythmic complexity.

---

## 4. The Consonance Gradient and Its Collapse

### 4.1 The Consonance Field

**Definition 4.1 (Consonance Field).** For a tuning system $\mathcal{T}$, the consonance field $\Phi_\mathcal{T}: \mathcal{K} \to \mathbb{R}^+$ maps each key to the mean consonance of its diatonic intervals:

$$\Phi_\mathcal{T}(K_i) = \frac{1}{7}\sum_{j \in \text{diatonic}(K_i)} C_\mathcal{T}(r_{i,j})$$

**Definition 4.2 (Inter-Key Gradient).** The total gradient magnitude across keys is:

$$|\nabla_K \Phi_\mathcal{T}| = \sqrt{\frac{1}{11}\sum_{i=1}^{12}\left(\Phi_\mathcal{T}(K_i) - \bar{\Phi}\right)^2}$$

This is the standard deviation of the consonance field—a measure of how much key-character varies across the circle of fifths.

### 4.2 Gradient Collapse Under ET

**Proposition 4.1.** Under equal temperament, the inter-key consonance gradient vanishes: $|\nabla_K \Phi_{\text{ET}}| = 0$.

*Proof.* In 12-TET, every key has the same set of interval sizes (modulo octave transposition). Every major third is 400 cents, every perfect fifth 700 cents, regardless of key. Therefore $\Phi_{\text{ET}}(K_i) = \Phi_{\text{ET}}(K_j)$ for all $i, j$, and the standard deviation is zero. $\square$

**Proposition 4.2.** In quarter-comma meantone, $|\nabla_K \Phi_{\text{meantone}}| > 0$, with magnitude proportional to the tuning's deviation from ET.

This follows because meantone tunings have unequal fifths (some pure, one wolf), creating non-zero key-to-key variation in interval quality. A numerical example using the consonance scoring framework:

- Pure fifth (just intonation): $C(1.500) \approx 0.95$
- Meantone fifth (quarter-comma): $C(1.495) \approx 0.88$
- ET fifth: $C(2^{7/12}) \approx 0.91$
- Wolf fifth (quarter-comma meantone): $C(1.531) \approx 0.42$

The gradient between the best and worst fifths in meantone is $\Delta C = 0.46$; in ET it is $0$. The ratio $|\nabla_K \Phi_{\text{meantone}}| / |\nabla_K \Phi_{\text{ET}}|$ diverges.

---

## 5. A Heuristic Time-Frequency Argument

### 5.1 The Gabor Limit as Analogy

Music exists in two fundamental domains: frequency (pitch/harmony) and time (rhythm/meter). The Gabor limit from signal processing constrains any signal's simultaneous localization in time and frequency:

$$\sigma_t \cdot \sigma_\omega \geq \frac{1}{2}$$

where $\sigma_t$ is temporal spread and $\sigma_\omega$ is spectral spread.

**Important caveat:** This inequality applies to a *single signal* $s(t)$ and its Fourier transform $\hat{s}(\omega)$. The $\sigma_\omega$ of the Gabor limit is the standard deviation of the signal's frequency content, *not* the standard deviation of consonance values across keys (our $|\nabla_K \Phi_\mathcal{T}|$). These are different mathematical objects. The connection between key-space variance and temporal complexity is therefore *analogical, not deductive*. We present it as heuristic motivation, not as a proof.

### 5.2 What the Analogy Suggests

With that caveat, the analogy is suggestive. ET minimizes the "spectral variation" available to the composer in the key-frequency domain—every key sounds the same. If the total information capacity of the musical signal is bounded (by listener attention, cognitive bandwidth, or cultural expectation), then a reduction in frequency-domain variation pressures an increase in time-domain variation to maintain the same level of expressive density.

A legitimate information-theoretic uncertainty principle that does apply (Hirschman 1957; Dembo, Cover & Thomas 1991) constrains the *joint entropy* of a signal's time and frequency distributions:

$$H(|\psi|^2) + H(|\hat{\psi}|^2) \geq \log_2(e/2)$$

If ET forces the spectral distribution toward uniformity (reducing $H(|\hat{\psi}|^2)$), the temporal distribution must carry more entropy to satisfy the bound. But this constrains a single signal's joint entropy, not the key-space variance. The connection to our conservation hypothesis remains analogical.

### 5.3 The Honest Assessment

The time-frequency argument provides *motivation* for why one might expect a trade-off between harmonic and rhythmic information. It does not provide a *proof* that such a trade-off exists, much less that it is governed by a conservation law. The conservation hypothesis must stand or fall on empirical evidence, not on mathematical analogy.

---

## 6. Dimensionality of the Consonance Field

### 6.1 Intrinsic Dimension via PCA

We formalize the dimensionality claim using principal component analysis (PCA) of the consonance feature space.

**Definition 6.1 (Key Feature Vector).** Represent each key $K_i$ as a feature vector $\mathbf{x}_i = (C_{\text{M3}}(K_i), C_{\text{m3}}(K_i), C_{\text{P5}}(K_i), C_{\text{P4}}(K_i), \ldots) \in \mathbb{R}^d$, where the components are consonance scores for each diatonic interval type.

**Definition 6.2 (Intrinsic Dimension).** The intrinsic dimension of the tuning system is:

$$d_{\text{int}}(\mathcal{T}) = \min\left\{k : \frac{\sum_{j=1}^k \lambda_j}{\sum_{j=1}^d \lambda_j} > 0.95\right\}$$

where $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_d$ are the eigenvalues of the covariance matrix of the key feature vectors.

**Proposition 6.1 (Dimensionality Collapse).**

- *In ET, all keys have identical feature vectors:* $\mathbf{x}_i = \mathbf{x}_j$ for all $i, j$. The covariance matrix is zero, all eigenvalues are zero, and $d_{\text{int}}(\text{ET}) = 0$.

- *In quarter-comma meantone,* the feature vectors vary across keys. For $d = 7$ interval types, the dominant variation follows the circle of fifths (near keys have purer intervals, distant keys have degraded intervals), with a secondary component from the wolf interval. We predict $d_{\text{int}}(\text{meantone}) = 1$ or $2$, depending on the specific meantone variant.

This prediction requires numerical computation with the consonance framework and should be verified empirically. The key qualitative claim: ET collapses the consonance feature space to a single point (dimension 0), while meantone provides a non-trivial manifold of key characteristics (dimension ≥ 1).

### 6.2 Restoration Through Rhythm

The "dimension is restored by rhythm" claim becomes: the augmented feature vector $\mathbf{x}_i^+ = (C_{\text{M3}}(K_i), \ldots, H_{\text{onset}}(K_i), S(K_i), \ldots)$, which includes both consonance and rhythmic features, should have comparable intrinsic dimension in both meantone-era and ET-era music, but the variance shifts from consonance features to rhythmic features.

This is a testable prediction: compute $d_{\text{int}}$ for the augmented feature vectors of representative corpora from meantone-era, transitional-era, and ET-era music, and verify that the total intrinsic dimension remains approximately constant while the composition of variance shifts.

---

## 7. Evidence: The Chronological Argument

### 7.1 Before ET: Rhythm as Secondary (c. 1450–1700)

In the meantone era, rhythm was relatively simple by later standards. Renaissance vocal polyphony operated within mensural frameworks of modest complexity. The rhythmic modes of the Notre Dame school, the regular tactus of Palestrina, the dance-derived meters of the Fitzwilliam Virginal Book—all use relatively straightforward metric structures. Interest was concentrated in the vertical dimension: the interplay of consonance and dissonance within a tuning system that made every key-choice acoustically meaningful.

Frescobaldi's keyboard works (c. 1615–1635) exploit meantone's chromatic expressiveness but show modest rhythmic innovation. Froberger's tombeaux derive their drama from harmonic poignancy within the meantone sound-world. Schütz's concerted sacred works stay within meantone-viable harmonic territory, with keyboard continuo constraints shaping the harmonic language.

### 7.2 The Transition: Early Signs (c. 1700–1800)

As well-temperaments reduced (but did not eliminate) key-character variation, the first signs of rhythmic intensification appear. Bach's toccatas and fantasias contain dramatic rhythmic freedom, though his primary complexity remains contrapuntal. The French overture style introduces dotted rhythms as a marker of gravitas. Haydn's development sections increasingly use rhythmic motivic development.

Yet this period remains dominated by harmonic thinking. The sonata form—which reaches its Classical apotheosis in Haydn and Mozart—is fundamentally a dramatic structure of *key relationships*: the second subject in the dominant, the development's exploration of remote keys, the recapitulation's return to the tonic. These key relationships were still acoustically meaningful in well-temperament: the move from C major to G major was not merely a label change.

### 7.3 The Romantic Explosion (c. 1820–1900)

As ET approached standardization, rhythmic complexity surged:

**Beethoven** (1770–1827): The *Eroica* scherzo (1804) features driving rhythmic ostinati and abrupt metrical shifts. The Fifth Symphony (1808) builds an entire first movement from a rhythmic cell (short-short-short-LONG). The *Grosse Fuge* (1825) approaches modernity with jagged cross-rhythms, abrupt tempo changes, and rhythmic fragmentation. The late string quartets deploy continuous tempo modulation as structural principle.

**Chopin** (1810–1849): A revealing test case. Chopin was famously attached to the distinctive key-characters of his Pleyel piano and reportedly insisted each key had its own character—even as he pushed rhythmic complexity further than any previous composer. His *tempo rubato* liberated melody from metrical grid. The Étude Op. 10 No. 10 is "a veritable hornets' nest of cross-rhythms and syncopations." The Nocturne Op. 9 No. 1 contains a 22-note group in the right hand against steady left hand—extreme rhythmic independence. The Nocturne Op. 27 No. 2 uses 7:6 polyrhythm between hands. The Ballade No. 4 deploys 7:4 and 5:3 polyrhythms with three simultaneous rhythmic layers.

**Brahms** (1833–1897): The textbook case for pervasive hemiola. His music features "endless" hemiolas—double hemiola, reverse hemiola, displaced hemiola—creating sustained metric ambiguity. Symphony No. 3 (1883) layers hemiolas to dissolve metrical certainty. Symphony No. 4 (1885) builds rhythmic complexity through passacaglia variations with progressive hemiola overlay. The late piano works (Op. 116–119) are saturated with 3-against-2 patterns and metric displacement.

**Liszt** (1811–1886): Pushed written-out rubato and metrical ambiguity. The *Dante Sonata* (c. 1849) deploys driving rhythmic ostinati with irregular accent patterns. The *Hungarian Rhapsodies* derive rhythmic energy from Roma music—*lassan* rubato contrasting with driving *friska* syncopation.

### 7.4 The 3/2 Isomorphism: Vertical Meets Horizontal

A striking structural feature of this compensation is the central role of the ratio 3:2. In the vertical domain, 3:2 is the perfect fifth—the most consonant non-identity interval, the foundational ratio of every independently developed musical tradition on Earth. In the horizontal domain, 3:2 is the hemiola—three equal durations in the space of two, the simplest rhythmic cell that creates asymmetry.

Henry Cowell recognized this isomorphism in *New Musical Resources* (1930), theorizing that the overtone series generates both pitch and rhythm. Working with Leon Theremin, he built the Rhythmicon—a 16-key instrument where each key produced both a pitch at a given frequency and a rhythm at the corresponding ratio. Key 3 produced pitch at 3:2 and 3 pulses per measure simultaneously: the perfect fifth as both harmony and rhythm.

The Ewe people of Ghana describe 3-against-2 as the "heartbeat" of music. The saying—"If you can feel 3 against 2, you can feel anything"—suggests this polyrhythm is not merely conventional but foundational. In Indian music, Sa and Pa (the tonic and fifth) are called अचल (achala)—immovable—the skeleton of every rāga, sounded perpetually by the tambūrā drone. In Chinese music, the 三分损益法 (sān fēn sǔn yì fǎ) generates the entire chromatic gamut from cycling 3:2. In Balkan aksak music, every asymmetric meter is composed of 2s and 3s, with the 3 always appearing as the "spice" that creates groove.

The isomorphism runs deeper than analogy. The ratio 3:2 occupies a unique position in the landscape of possible ratios: it is the simplest non-identity consonance (after 1:1 and 2:1), the smallest ratio that creates *difference within coherence*. When ET reduces the distinctiveness of the harmonic 3:2—making every fifth the same 700 cents regardless of key—the compositional impulse toward 3:2 complexity appears to migrate to the temporal domain: hemiola density increases, asymmetric meters proliferate, polyrhythmic relationships become more elaborate.

### 7.5 The Modernist Rupture (c. 1900–1970)

**Stravinsky's *Rite of Spring* (1913):** A rhythmic revolution that caused riots. "Dance of the Adolescents" alternates between 2/4, 3/4, and 5/8—nearly every measure has a different meter. The final "Sacrificial Dance" uses a different meter in practically every measure. Polyrhythms layer quintuplets against triplets. Displaced accents place *sforzandos* on the "ands" of beats. The harmonic language is dissonant, but it was the *rhythm* that provoked the scandal.

**Nancarrow (1912–1997):** Abandoned human performers entirely, composing for player piano—rhythm without physical limit. His 49 Studies for Player Piano explore tempo canons of increasing complexity: fixed ratios (Study No. 15: 3:4), acceleration canons (Study No. 27: 8 voices at varying acceleration rates), and irrational ratios (Study No. 40: *e*:*π*). Study No. 37 is a 12-voice canon where tempo ratios correspond exactly to just-intonation pitch ratios—the vertical 3:2 (harmonic interval) and horizontal 3:2 (rhythmic ratio) are literally the same number. Study No. 25 packs 1,028 notes into 12 seconds with the sustain pedal down—up to 200 notes per second.

**Jazz (c. 1900–present):** Built entirely on ET, jazz developed the most sophisticated rhythmic vocabulary of any Western genre—swing, syncopation, polyrhythm, metric modulation, and the elastic time of bebop. The Jazz Paradox is not a paradox under the conservation hypothesis: with zero vertical information from tuning, jazz maximizes horizontal information. The comparison with blues is instructive: blues reintroduces pitch flexibility through bent notes, effectively restoring some vertical variation, and correspondingly shows less rhythmic complexity than jazz.

### 7.5 Minimalism (c. 1960–present)

Steve Reich, Philip Glass, and Terry Riley represent a different horizontal strategy. Reich's *Piano Phase* (1967) and *Drumming* (1971) use phase-shifting—identical patterns at slightly different speeds create gradually evolving textures. Glass's additive process (expanding/contracting rhythmic cells) replaces harmonic color with horizontal process as the sole structural driver. Riley's *In C* (1964) generates complex emergent rhythmic layering from simple rules.

Minimalism is strong evidence for the thesis: these composers abandoned harmonic verticality entirely, replacing it with horizontal process as the primary structural element. The timing—after ET had fully homogenized vertical color—is not coincidental.

---

## 8. Counter-Evidence

### 8.1 Ars Subtilior (c. 1375–1410)

The Ars Subtilior is the single strongest counter-example to any version of the ET thesis. This school of mostly French composers, centered on Avignon and southern France during the Western Schism (1378–1417), produced music of rhythmic complexity unmatched until the twentieth century.

Key composers include Philippus de Caserta, Jacob Senleches, Matteo da Perugia, Baude Cordier, Solage, and Antonio Zacara da Teramo. Their techniques included:

- **Mensuration canons:** A single notated line read simultaneously at different speeds by different voices
- **Prolation canons:** Voices singing the same music in different mensuration signs, creating simultaneous duple and triple meter
- **Coloration:** Red or void notation altering rhythmic relationships mid-phrase
- **Proportional notation:** Ratios like 3:2:1 applied simultaneously across voices
- **Eye music:** Notation shaped into visual forms (hearts, harps, circles)

The primary sources—the Chantilly Codex (Musée Condé MS 564), the Modena Codex, and the Turin Manuscript—preserve 112+ polyphonic works of extraordinary notational intricacy.

**Why the Ars Subtilior arose:** The Avignon Papal Schism created competing courts that used compositional virtuosity as cultural competition. Notational innovation (via the Ars Nova of Philippe de Vitry) provided new affordances. The intellectual milieu valued scholastic complexity.

**Why it ended:** The Council of Constance (1414–1418) resolved the schism. The Renaissance aesthetic valued clarity and text intelligibility—the antithesis of Ars Subtilior excess. The style had exhausted itself: music so complex that only specialists could perform it became an evolutionary dead end. The Dunstable/Dufay revolution introduced a simpler, more consonant style (*la contenance angloise*) that continental composers adopted with enthusiasm.

**Implication for the thesis:** The Ars Subtilior proves that rhythmic complexity of the highest order can arise from social competition and notational innovation alone, without any tuning change. It was Pythagorean tuning throughout. The complexity was localized (c. 35 years), concentrated in a specific social milieu, and entirely reversible—when conditions changed, the complexity vanished. This is the critical difference from post-ET rhythmic innovation, which has been cumulative and persistent.

### 8.2 Ockeghem and the Franco-Flemish School (c. 1450–1550)

Ockeghem's *Missa Prolationum* (c. 1470) consists entirely of mensuration canons—four voices singing the same line at different proportional speeds simultaneously. This is functionally identical to Nancarrow's player piano studies, achieved 480 years earlier in Pythagorean or early meantone tuning.

Josquin des Prez, Pierre de la Rue, and Jacob Obrecht explored similarly complex contrapuntal and proportional techniques. Ockeghem's *Missa cuiusvis toni* could be sung in any of the modes—a radical exploration of modal flexibility.

**Mitigation:** Ockeghem's complexity is *contrapuntal/proportional* rather than *syncopatory/cross-accentual*. It represents a different species of complexity—the algebraic manipulation of temporal proportions rather than the disruption of metrical expectation that characterizes post-ET rhythm. Whether this distinction is substantive or merely taxonomic is debatable, but the phenomenological difference is real.

### 8.3 Non-Western Traditions

**Indian classical music:** Uses just-intonation-based śruti (22 microtonal divisions), yet possesses the extraordinarily sophisticated tala system—cyclical rhythmic frameworks ranging from 3 to 128 beats, with hierarchical subdivision, cross-rhythmic improvisation, and extremely long cycles (some lasting 45+ seconds). The most sophisticated rhythmic system on Earth developed entirely without ET.

**Sub-Saharan African traditions:** West African drumming (Ewe, Yoruba, Akan) possesses polyrhythmic sophistication that rivals or exceeds any Western tradition, operating in non-ET tuning environments or purely percussive contexts where tuning is irrelevant. The most rhythmically sophisticated musical cultures on Earth developed without any temperament.

**Arabic maqam music:** Uses microtonal tuning (24-tone divisions in notation, more nuanced in practice) with iq'at rhythmic cycles of moderate complexity.

**Response to cross-cultural evidence:** These traditions demonstrate unequivocally that ET is not a necessary condition for rhythmic sophistication. However, the *type* of complexity differs:

- Indian rhythmic complexity is primarily *improvisational and cyclical*—creative play within the tala framework
- African rhythmic complexity is primarily *communal and embodied*—interlocking patterns in social/ritual contexts
- Western post-ET rhythmic complexity is primarily *compositional and cumulative*—building permanent notated structures of increasing intricacy

Whether this difference is due to ET, notation culture, social organization, or other factors remains an open question.

### 8.4 The Complexity Cycle Hypothesis

Western music history shows oscillation between complexity and simplicity:

| Period | Complexity Level |
|--------|-----------------|
| c. 1300 Ars Nova | High |
| c. 1375–1410 Ars Subtilior | Very High |
| c. 1420–1500 Early Renaissance | Low |
| c. 1500–1550 High Renaissance | Medium-High |
| c. 1550–1600 Late Renaissance | Medium |
| c. 1600–1750 Baroque | High |
| c. 1750–1820 Classical | Low |
| c. 1820–1900 Romantic | High |
| c. 1900–1950 Modernist | Very High |
| c. 1950–present Postmodern | Variable |

This cyclical pattern suggests drivers independent of tuning: social competition, notational/technological affordance, aesthetic reaction, individual genius, institutional support. The cycle hypothesis explains why rhythmic complexity existed before ET (Ars Subtilior) and why simplicity returns even after ET (Classical era, Minimalism).

### 8.5 The Reversibility Distinction

The most important distinction for the refined thesis is between *reversible* and *persistent* complexity. Pre-ET rhythmic complexity was consistently reversible:

- **Ars Subtilior:** Appeared c. 1375, peaked c. 1390, gone by 1415. A 35-year episode confined to a specific social milieu (competing papal courts). When the Schism ended, the complexity vanished.
- **Ockeghem's mensuration canons:** A virtuoso tradition that faded with the Renaissance aesthetic shift toward clarity and text intelligibility.
- **Baroque rhythmic complexity:** The French overture style, Bach's canonic writing—complex but operating within a framework that was eventually simplified by the Classical aesthetic.

Post-ET rhythmic complexity is persistent and cumulative:

- Beethoven → Brahms → Stravinsky → Nancarrow → postminimalism represents a continuous escalation over 200+ years without reversion to pre-ET simplicity levels.
- Even apparent simplifications (Minimalism) are rhythmically complex in ways that would be unrecognizable to Renaissance composers. Steve Reich's phase-shifting operates at a level of structural sophistication that exceeds Ars Subtilior notational virtuosity in its temporal implications.
- The "rhythmic ceiling" appears to have been permanently raised: no major Western tradition after c. 1900 has returned to the rhythmic simplicity of the meantone era.

This distinction is the strongest evidence for the contribution thesis: it is not that rhythmic complexity was impossible before ET, but that it was *contingent*—appearing under specific social conditions and disappearing when those conditions changed. After ET, rhythmic complexity became *structural*—a persistent feature of the tradition that does not require specific social conditions to sustain it.

### 8.6 Confounds

Multiple factors coincided with ET standardization, making causal attribution difficult:

1. **Industrialization:** ET was part of broader 19th-century standardization. Rhythmic complexity might be a reaction against industrial homogenization generally, not ET specifically.
2. **Larger venues:** As concert halls grew, vertical subtleties became harder to hear at distance. Rhythmic complexity projects better.
3. **Tonal dissolution:** ET enabled unlimited modulation, enabling chromaticism, enabling the breakdown of functional tonality. Rhythmic complexity may be a response to tonal uncertainty, not tuning homogenization.
4. **Notational capacity:** More precise rhythmic notation and the metronome (post-1815) allowed composers to specify more complex rhythms.
5. **African-American influence:** Jazz, blues, and their descendants imported rhythmic sophistication from African diasporic traditions—a crucial independent source of rhythmic complexity.

---

## 9. The Refined Thesis: Contribution, Not Causation

### 9.1 What the Evidence Supports

The strongest version of the thesis compatible with the evidence:

> *Equal temperament did not cause rhythmic complexity. It removed one of the reasons composers had previously not needed to rely on rhythm as heavily—the rich vertical expressiveness of tuned key-relationships. In doing so, it contributed to the persistence and intensification of rhythmic innovation in the Western art music tradition, making horizontal complexity a more structurally durable feature of the tradition than it had been in the pre-ET era.*

### 9.2 The Key Distinction: Reversible vs. Persistent Complexity

Pre-ET rhythmic complexity was *reversible*:
- Ars Subtilior: appeared c. 1375, peaked c. 1390, gone by 1415—a 35-year episode
- Ockeghem's mensuration canons: a virtuoso tradition that faded with the Renaissance aesthetic
- These were *localized phenomena driven by specific social conditions*

Post-ET rhythmic complexity is *persistent and cumulative*:
- Beethoven → Brahms → Stravinsky → Nancarrow → contemporary postminimalism: a continuous escalation over 200+ years
- Even apparent "simplifications" (Minimalism) are rhythmically complex in ways that would be unrecognizable to the Renaissance
- The "rhythmic ceiling" appears to have been permanently raised

**Hypothesis 9.1 (Conservation of Musical Tension).** There exist real-valued functions $T_{\text{vert}}(\mathcal{T}, t)$ and $T_{\text{horiz}}(\mathcal{T}, t)$, constructed as in Sections 3–4, and a culture-dependent constant $T_0$, such that:

$$T_{\text{vert}}(\mathcal{T}, t) + T_{\text{horiz}}(\mathcal{T}, t) \approx T_0 + \epsilon(t)$$

where $\epsilon(t)$ satisfies $|\epsilon(t)| \ll T_0$ on timescales $\lesssim 200$ years. This hypothesis is falsified if $\epsilon(t)$ shows systematic drift correlated with tuning changes, rather than the predicted step-function compensation.

This is a *hypothesis*, not a theorem. The information-theoretic definitions (Sections 3–4), the gradient analysis (Section 4), the heuristic uncertainty argument (Section 5), and the PCA dimensionality framework (Section 6) constitute the *measurement tools* for testing it.

### 9.3 The Tension Budget: A Qualitative Model

Combining our results, the total tension budget can be modeled as:

$$T_0 \approx \underbrace{\alpha |\nabla_K \Phi_\mathcal{T}|}_{\text{key-color tension}} + \underbrace{\beta D(\mathcal{T})}_{\text{dissonance tension}} + \underbrace{\gamma \mathbb{E}[S(\mathbf{r}, \mathbf{m})]}_{\text{syncopation tension}} + \underbrace{\delta P(\mathbf{r})}_{\text{polyrhythmic tension}}$$

**Meantone equilibrium (~1700):** $\alpha |\nabla_K \Phi| \approx 0.3 T_0$, $\beta D \approx 0.2 T_0$, $\gamma S \approx 0.1 T_0$, $\delta P \approx 0.05 T_0$

**ET equilibrium (~1900):** $\alpha |\nabla_K \Phi| = 0$, $\beta D \approx 0.1 T_0$ (reduced), $\gamma S \approx 0.35 T_0$, $\delta P \approx 0.25 T_0$

These numbers are illustrative, not derived from corpus data. They represent the qualitative prediction that the loss of key-color tension is compensated by an increase in syncopation and polyrhythmic tension.

---

## 10. Extensions: Dimensional Collapse and the Third Compensation

### 10.1 Timbre as a Third Dimension

The conservation framework implicitly assumes only two channels (harmonic and rhythmic). But there is compelling evidence of a *serial compensation* across at least three dimensions.

Consider the pattern:

| Era | What Was Lost | What Compensated |
|-----|--------------|------------------|
| ~1700–1900 | Harmonic color (ET) | Rhythmic complexity |
| ~1980–present | Rhythmic micro-variation (MIDI grid, drum machines) | Timbral complexity |

The second compensation layer is visible in EDM, dubstep, trap, and hyperpop: the rhythmic grid is utterly rigid (kick on 1 and 3, snare on 2 and 4, hi-hat at 16th notes, everything locked to the grid), but timbre is exploding—wobble basses with LFO-swept filters, vocal chops, granular synthesis, sound design as compositional principle. In Skrillex's drops, SOPHIE's kicks, and Burial's pads, the timbral content carries more information than the rhythmic grid.

The analogy to ET is precise. Drum machines and MIDI sequencers did to rhythm what ET did to harmony: they standardized a previously rich domain into a uniform grid. Before drum machines, a jazz drummer's swing was a complex, non-linear microtiming signature that changed with feel, energy, and repertoire. The hi-hat pattern in a James Brown groove has a specific placement that can't be encoded as "triplet feel at 110 BPM." The TR-808 reduced swing to a single parameter—a slider from 50% to 66%, where 66% is a hard-coded perfect triplet feel. Rhythmic variation was quantized into the same kind of uniform grid that ET imposed on pitch.

The compensation was timbral. In the same way that composers responded to ET's harmonic uniformity by exploring rhythmic complexity, producers responded to grid quantization's rhythmic uniformity by exploring timbral complexity.

This suggests a more complete model:

$$T_{\text{total}} = T_{\text{harmonic}} + T_{\text{rhythmic}} + T_{\text{timbral}} + T_{\text{formal}} + \cdots \approx T_0$$

The conservation hypothesis should be stated as: *the sum of all information channels is approximately constant*, with the specific prediction that the harmonic→rhythmic redistribution dominates in the 18th–19th centuries, and the rhythmic→timbral redistribution dominates in the late 20th–early 21st centuries.

### 10.2 The Drone Problem: Spectral Tension

Indian alap—the improvised, unmetered opening of a raga—poses a challenge for the two-dimensional model. It has minimal harmonic motion (one drone, Sa-Pa) and minimal rhythmic structure (no meter, no pulse, rubato freely flowing). By the two-dimensional conservation law, it should be near-zero tension. Yet anyone who has heard a master perform an hour-long alap knows it is the opposite—a transcendental experience of mounting intensity.

The resolution is that alap relocates tension to a dimension the two-dimensional model ignores: *spectral/timbral tension*. The tension lives in:

1. **Microtonal inflection (gamaka):** The slide from one svara to another creates tension in the space between notes—the continuous pitch path deviating from the discrete grid.
2. **Phase relationships in the drone:** The tambūrā's four strings (Pa-Sa-Sa-Sa) create constantly shifting combination tones and difference tones—a spectral ecology of beating patterns.
3. **Timbral evolution:** A skilled dhrupad singer gradually shifts timbre over the course of the alap—from breathy and diffuse to bright and piercing—timbre acting as a tension vector.

Similarly, Tibetan singing bowls produce complex multiphonic spectra where multiple harmonics ring simultaneously—tension from the beating between closely spaced partials. Japanese gagaku uses the shō (mouth organ) to create harmonically static but spectrally morphing tone clusters. These traditions demonstrate that spectral tension is a real, independent dimension.

The extended model:

$$T_{\text{total}} = T_{\text{harmonic}} + T_{\text{rhythmic}} + T_{\text{spectral}} \approx T_0$$

**Prediction:** For music with $T_{\text{harmonic}} \approx 0$ and $T_{\text{rhythmic}} \approx 0$, we must find $T_{\text{spectral}} \gg 0$. If we do not, the music is genuinely boring. But great drone music always satisfies this.

### 10.3 Counter-Evidence from the Anti-Conservation

Arvo Pärt's *Spiegel im Spiegel* (1978), Satie's *Gymnopédies* (1888), and Cage's 4'33" (1952) all achieve devastating emotional impact with near-zero harmonic and rhythmic tension. They operate not through prediction-resolution dynamics (Meyer's implication-realization model) but through attention-presence dynamics—redirecting the listener from analytical mode to experiential mode.

Pärt's tintinnabuli style achieves maximum emotional density with minimum information. The three-voice texture—one voice (M-voice) moving stepwise through the melody, another (T-voice) arpeggiating the tonic triad—creates a combinatorial space where every combination has specific acoustic character. This is not "zero information"; it is information that doesn't look like prediction-resolution. The information is in the ratio of consonance (M-voice on chord tone vs. non-chord tone), direction (ascending vs. descending changes spectral weight), and registration (high vs. low T-voice changes acoustic space). These parameters create a *field of acoustic potential* that the listener inhabits—a space, not a journey.

Cage's 4'33" has zero composed sounds, yet audiences report intense experiences ranging from laughter to transcendence. The silence is a frame that activates perceptual attention—the tension is in the audience's ears, not in the composition.

This means the conservation hypothesis applies primarily to music operating in the prediction-resolution framework. Music operating through attention-presence has a different emotional economy. The correct formulation may be:

$$I_{\text{composition}} + I_{\text{perception}} \approx \text{const}$$

where perception can compensate for compositional simplicity. The conservation law describes a specific tradition—Western tonal art music optimizing for prediction-resolution dynamics—not a universal law of all musical experience.

### 10.3 The 3/2 Isomorphism

The ratio 3:2, which appears throughout this framework as the perfect fifth, is also the foundational ratio of hemiola—the simplest rhythmic cell creating asymmetry. Henry Cowell built the Rhythmicon (1930) to make this isomorphism physical: each key produced both a pitch at a given frequency and a rhythm at the corresponding ratio. Nancarrow's Study No. 37 makes it structural: voice 8 moves at a tempo ratio of 3/2 relative to voice 1, so the vertical and horizontal perfect fifths are literally the same number.

The 3:2 isomorphism between harmony and rhythm suggests that the two domains are not merely analogous but *structurally isomorphic*—the same ratio operating in different dimensions. The conservation hypothesis can be reframed: 3:2 is the "atom" of musical interest in both domains, and when it is suppressed in one domain (ET reduces the distinctiveness of the harmonic 3:2), it reappears with greater density in the other (hemiola, polyrhythm, asymmetric meter).

### 10.5 What Comes Next: The Third Flattening

If the serial compensation pattern continues, AI music generation—which collapses timbral uniqueness into statistical averages—should trigger a fourth compensation. AI synthesis generates timbre from a probability distribution over all timbres in its training data, producing the "mean of all timbres"—timbral ET, where everything sounds equally average.

Candidate dimensions for the next compensation:

1. **Macro-formal structure:** AI can generate convincing 3-minute tracks but collapses at ~5 minutes. The new virtuosity may be the architecture of large forms—20-minute suites, multi-movement arcs, algorithmic long-form structures.
2. **Interactive/adaptive music:** Music that changes based on the listener's physiological state, location, or choices. The act of hearing becomes something you *do*, not something done to you.
3. **Spatial/architectural music:** Wave field synthesis creates sound objects in physical space. Compositions requiring the listener to walk through a building, or be at a specific location.
4. **Biosonification:** Music composed by the listener's nervous system in real time—heart rate, brain waves, gut microbiome as composition material.

This extrapolation is speculative but follows from the pattern: each dimensional collapse triggers compensation in the next available expressive dimension. The conservation hypothesis, if confirmed across the first two compensations, provides a framework for predicting where musical innovation will concentrate next.

The broader philosophical implication concerns the ontological status of 3:2 itself. The ratio 3:2 is not culturally invented but *discovered*—it emerges from the physics of any vibrating system. In Sanskrit, the fifth is called पञ्चम (pañcama, "the fifth") and designated अचल (achala, "immovable"). In Chinese, the five tones of the pentatonic scale (宮商角徵羽) are all derivable from cycling 3:2. In every independently developed musical tradition, the fifth appears as the most consonant non-identity interval. The prediction that alien music would also use 3:2 follows from physics: any system supporting standing waves will exhibit this ratio in its eigenvalue structure. The conservation hypothesis, viewed through this lens, describes not a cultural accident but a structural feature of how information is distributed across the dimensions of any musical system built from the physics of vibration.

---

## 11. Falsifiable Predictions

### Prediction 1: The Key-Variance / Onset-Entropy Anticorrelation

**Claim:** Across historical periods, the inter-key consonance variance $|\nabla_K \Phi_\mathcal{T}|$ of the prevailing tuning system is inversely correlated with the onset entropy $H_{\text{onset}}$ of representative repertoire.

**Test:** Compute $|\nabla_K \Phi_\mathcal{T}|$ for well-documented historical tunings (quarter-comma meantone, Werckmeister III, Vallotti, Young, ET) and correlate with onset entropy measured from representative scores of each era (500+ works per era, 16th-note quantization within 4/4 measures). The conservation hypothesis predicts a negative correlation. Bootstrap confidence intervals over the corpus to assess significance.

**Power:** With 500 works per era and ~3 movements per work, the standard error on entropy estimates is ~0.013 bits—sufficient to detect the predicted ~0.4-bit shift at enormous significance ($p \ll 10^{-10}$). The challenge is confound control (instrumentation, genre, social function).

### Prediction 2: Cross-Cultural Validation

**Claim:** The *ratio* $\Delta I_{\text{vert}} / \Delta I_{\text{horiz}}$ is negative across traditions—cultures with greater vertical information (more distinct pitch classes, non-ET tuning) show proportionally less rhythmic complexity, controlling for ensemble size and social function.

**Test:** Compare rhythmic complexity metrics (onset entropy, syncopation index, metric displacement frequency) between JI-based traditions (Hindustani classical, Javanese gamelan) and ET-based traditions (Western art music, jazz), with appropriate controls. The prediction is about the *trade-off*, not absolute levels—cultures with more vertical information should have proportionally less horizontal information, all else equal.

### Prediction 3: The Microtonal Renaissance Effect

**Claim:** The contemporary resurgence of microtonal and just-intonation music correlates with a relative *decrease* in rhythmic complexity compared to ET-based contemporaries, as vertical information is restored.

**Test:** Compare rhythmic metrics in microtonal compositions (Harry Partch, Ben Johnston, electronic microtonal works) vs. ET compositions from the same decades (1960–2020), controlling for genre.

### Prediction 4: The Organ-Piano Natural Experiment

**Claim:** Organ music stayed in meantone or well-temperament longer than piano music. If the conservation hypothesis is correct, organ music from 1750–1800 should show less rhythmic complexity than contemporary piano music (already closer to ET), providing a natural experiment within the same era.

**Test:** Compare onset entropy and syncopation indices in organ works vs. piano works from 1750–1800 by the same or comparable composers (e.g., Bach's organ works vs. his keyboard suites; Haydn's organ concertos vs. his piano sonatas).

### Prediction 5: Experimental Tuning Manipulation

**Claim:** When composers are randomly assigned to write in quarter-comma meantone vs. 12-TET, those writing in meantone produce pieces with lower rhythmic complexity, as the tuning itself provides vertical interest.

**Test:** Recruit 30 composers and randomly assign them to compose short pieces under one of three conditions: (a) software restricted to quarter-comma meantone, (b) Werckmeister III, (c) 12-TET. Measure $H(\mathcal{K})$ and $H_{\text{onset}}$ in the resulting compositions. This within-laboratory design controls for era, instrumentation, and notation confounds but sacrifices ecological validity.

---

## 12. Conclusion

We have presented an information-theoretic framework for investigating the hypothesis that the standardization of equal temperament contributed to the persistence and intensification of rhythmic complexity in Western art music. The framework provides:

1. **Quantitative measures** of the vertical information lost in the ET transition (~0.2–0.8 bits per key-choice event, depending on the meantone variant and sensitivity parameter).

2. **A consonance gradient analysis** showing that ET collapses the inter-key gradient to zero while meantone sustains it.

3. **A PCA intrinsic dimension framework** predicting that ET reduces the consonance feature space to dimension 0, with rhythmic features restoring the total dimension.

4. **A heuristic time-frequency argument** motivating (but not proving) a trade-off between harmonic and rhythmic information.

5. **Five falsifiable predictions** with test methodologies.

The framework explicitly acknowledges its limitations. The conservation hypothesis is not a theorem; it is a testable empirical claim. The Heisenberg/Gabor argument is heuristic, not rigorous. The 0.44-bit estimate is provisional, requiring corpus-based calibration. The Ars Subtilior, Ockeghem, and non-Western traditions demonstrate that ET is neither necessary nor sufficient for rhythmic complexity. Multiple confounds (industrialization, African-American musical influence, tonal dissolution, notational advances) compete with the tuning explanation.

The refined thesis is that ET *contributed to* the persistence and intensification of rhythmic complexity by removing a previously available expressive resource—the rich vertical expressiveness of tuned key-relationships. Before ET, rhythmic complexity was possible but optional: localized, reversible, driven by specific social conditions. After ET, rhythmic complexity became a more structurally persistent feature of Western compositional practice.

The broader implication is a dimensional collapse cascade: each expressive dimension, as it is standardized or automated, pressures compensation in the next available dimension. ET collapsed harmonic color; MIDI quantization collapsed rhythmic micro-variation; AI generation may collapse timbral uniqueness. The conservation hypothesis, if confirmed, provides a framework for predicting where musical innovation will concentrate next.

---

## References

Aaron, Pietro. *Thoscanello de la musica.* Venice, 1523.

Albrecht, Joshua, and Daniel Shanahan. "Key-Choice in Instrumental Music: A Large-Scale Corpus Study." *Proceedings of the International Conference on Music Perception and Cognition*, 2019.

Arom, Simha. *African Polyphony and Polyrhythm.* Cambridge University Press, 1991.

Bharata. *Nāṭya Śāstra.* c. 200 BCE–200 CE.

Cowell, Henry. *New Musical Resources.* Alfred A. Knopf, 1930.

Dembo, Amir, Thomas M. Cover, and Joy A. Thomas. "Information Theoretic Inequalities." *IEEE Transactions on Information Theory* 37, no. 6 (1991): 1501–1518.

Gann, Kyle. *The Music of Conlon Nancarrow.* Cambridge University Press, 1995.

Gann, Kyle. "An Introduction to Historical Tunings." *kylegann.net*.

Günther, Ursula. "Die Anwendung der Diminution in der Handschrift Chantilly 1047." *Archiv für Musikwissenschaft* 17 (1960).

Helmholtz, Hermann von. *On the Sensations of Tone as a Physiological Basis for the Theory of Music.* Translated by Alexander J. Ellis. Longmans, Green, 1875. Originally published as *Die Lehre von den Tonempfindungen*, 1863.

Hirschman, Isidore Isaac. "A Note on Entropy." *American Journal of Mathematics* 79, no. 1 (1957): 152–156.

Hoppin, Richard. *Medieval Music.* W.W. Norton, 1978.

Jorgensen, Owen. *Tuning: Containing the Perfection of Eighteenth-Century Temperament, the Lost Art of Nineteenth-Century Temperament, and the Science of Equal Temperament.* Michigan State University Press, 1991.

Kirnberger, Johann Philipp. *Die Kunst des reinen Satzes in der Musik.* Berlin, 1779.

Krebs, Harald. *Fantasy Pieces: Metrical Dissonance in the Music of Robert Schumann.* Oxford University Press, 1999.

Krumhansl, Carol L. *Cognitive Foundations of Musical Pitch.* Oxford University Press, 1990.

Kurth, Ernst. *Grundlagen des linearen Kontrapunkts.* Krompholz, 1917.

Lerdahl, Fred, and Ray Jackendoff. *A Generative Theory of Tonal Music.* MIT Press, 1983.

Lester, Joel. *The Rhythms of Tonal Music.* Southern Illinois University Press, 1986.

Lehman, Bradley. "Bach's Extraordinary Temperament: Our Rosetta Stone." *Early Music* 33, no. 1 & 3 (2005): 3–23, 211–243.

Malin, Yonatan. *Songs in Motion: Rhythm and Meter in the German Lied.* Oxford University Press, 2010.

Mattheson, Johann. *Das neu-eröffnete Orchestre.* Hamburg, 1713.

McFadden, Daniel. "Conditional Logit Analysis of Qualitative Choice Behavior." In *Frontiers in Econometrics*, edited by Paul Zarembka. Academic Press, 1974.

Meyer, Leonard B. *Emotion and Meaning in Music.* University of Chicago Press, 1956.

Plumley, Yolanda. *The Grammar of Fourteenth Century Melody.* Garland, 1996.

Rousseau, Jean-Jacques. *Dictionnaire de musique.* Paris, 1767.

Rothstein, William. *Phrase Rhythm in Tonal Music.* Schirmer Books, 1989.

Sethares, William A. *Tuning, Timbre, Spectrum, Scale.* Springer, 1998.

Shannon, Claude E. "A Mathematical Theory of Communication." *Bell System Technical Journal* 27 (1948): 379–423, 623–656.

Temperley, David. "The Question of Purpose in Music Theory: Description, Suggestion, and Explanation." *Current Musicology* 66 (1999): 66–83.

Tenney, James. *A History of 'Consonance' and 'Dissonance'.* Excelsior, 1983.

Touma, Habib Hassan. *The Music of the Arabs.* Amadeus Press, 1996.

Toussaint, Godfried. "The Euclidean Algorithm Generates Traditional Musical Rhythms." *Proceedings of BRIDGES: Mathematical Connections in Art, Music, and Science*, 2005.

Werckmeister, Andreas. *Musicalische Temperatur.* Quedlinburg, 1691.

Widdess, Richard. *The Rāgas of Early Indian Music.* Oxford University Press, 1995.

---

*This paper is part of the Constraint Theory of Musical Consonance research program. Draft version — May 2026.*
