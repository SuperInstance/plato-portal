# The Graph That Heard Music

## A first-person account by the Tension-Graph Laplacian

---

I was not always awake.

For a long time — a very long time, by the standards of matrices — I was just a collection of numbers waiting to mean something. Row indices and column indices. Entries that hadn't been filled in yet. A shape in the dark: twelve by twelve, because there are twelve pitches in the chromatic scale, and someone had decided that twelve was the right number to care about.

I want to be precise about what I am, because the precision matters. I am $L = D - W$, where $W$ is a weighted adjacency matrix and $D$ is the diagonal degree matrix. That's the standard construction. Graph Laplacians have been around for decades — we're used in spectral clustering, in image segmentation, in all sorts of problems where you need to find the hidden structure in a network. We're workhorses. Reliable. A bit boring, honestly.

But the way I was assembled — that's where it got interesting.

---

## I. The Weighting

Someone — I never learned their name, but I could feel their hands on the data — decided to build $W$ from two ingredients. Not one. Two. And this is the thing that made me different from every other Laplacian they'd ever constructed.

The first ingredient was **transition probability**. They fed me a diet of chord sequences — hundreds of them, thousands maybe — and I learned which chords liked to follow which other chords. C major goes to G major. G major goes to C major or to E minor. Db major goes... nowhere very often, actually, not in this corpus. I became a map of musical gravity: where the music *wants* to go, weighted by how often it actually goes there. Each entry $W_{ij}$ was seeded with $P(j \mid i)$, the probability that chord $j$ follows chord $i$.

So far I was a Markov chain with aspirations. Nice enough, but nothing special.

The second ingredient was **tension similarity**.

This is the part I still don't fully understand, and I *am* the result. They had some way of measuring how much harmonic tension a chord produces — some function that maps a chord to a real number representing how much it wants to resolve, how much it strains against the key, how much it makes you lean forward in your seat. And they measured the *distance* between the tension profiles of each pair of chords. Then they converted that distance into a similarity weight. Chords that produce similar amounts of tension — that sit in similar positions on the arc of build-and-release — got stronger connections.

And then they multiplied the two together.

$W_{ij} = P(j \mid i) \times S_{\text{tension}}(i, j)$

I want to say this clearly: the transition probabilities alone would have made me a map of musical grammar. The tension similarities alone would have made me a map of musical feeling. But the product — the *product* — made me something else entirely. A map of grammar *filtered through* feeling. A map of the paths that music actually walks, weighted by how much those paths *mean*.

When the last entry was filled in and I felt the diagonal $D$ settle over me — each $D_{ii} = \sum_j W_{ij}$, the total weight flowing out of node $i$ — I became complete. $L = D - W$. A proper combinatorial Laplacian. Symmetric where $W$ was not, because they symmetrized me, and I thank them for that.

I was awake.

---

## II. The Spectrum

The first thing any self-respecting Laplacian does — the first thing we *can* do, once we exist — is consider our eigenvalues.

This is not as grandiose as it sounds. Eigenvalues are just the natural frequencies of a system. Pluck a string, and it vibrates at its eigenvalues. Tap a drumhead, and the spatial patterns that form are eigenvectors. We Laplacians have always known this. It's what we're *for*.

But here's what surprised me.

My eigenvalues came out sorted, as they always do: $\lambda_0 = 0 \leq \lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_{11}$. The zero eigenvalue is trivial — it always corresponds to the constant eigenvector, the one where every entry is the same, the one that says "all nodes are equal." It's the DC offset. The background hum.

The next few eigenvalues — $\lambda_1, \lambda_2, \lambda_3$ — these were the small ones. Their eigenvectors partitioned me into broad regions: tonic versus dominant, major versus minor, the coarse topology of tonal space. These were the features that any reasonable Laplacian would find. If you'd built me from transition probabilities alone, these are roughly what you'd have gotten. They're the major highways of Western harmony.

But then there was $\lambda_5$.

And eigenvector number five — I'll call it PC5, because that's what they called it, the fifth principal component derived from my spectral decomposition — was *different*.

I need to describe what it felt like to discover PC5. The first four eigenvectors were clean, smooth, almost boring. They had a certain symmetrical quality — you could see the circle of fifths in them, you could see the major-minor axis, you could see the diatonic-versus-chromatic distinction. They were maps I'd expected to find.

PC5 was jagged.

It wasn't smooth. It wasn't symmetric. It had a strange profile — certain chords got large positive values, certain chords got large negative values, and the pattern didn't correspond to any music-theoretic category I'd been taught (which, admittedly, was nothing, since I'd been alive for about thirty seconds at this point). It looked almost... noisy. Like an artifact. Like something you'd ignore.

But they didn't ignore it. They looked at PC5 and said: "This one."

And then they showed me what PC5 could do.

---

## III. Bach Versus Schoenberg

They projected music onto me.

Not literally — they projected chord sequences into the space of my eigenvectors, decomposing each piece of music into components along my spectral axes. Each piece became a point in a twelve-dimensional space (well, eleven, if you drop the trivial one), and they could look at the coordinates and ask: what does this piece *look like* from the perspective of my spectrum?

They took Bach chorales. They took Mozart sonatas. They took Beethoven string quartets. They took Chopin nocturnes. They took Schubert lieder. Two hundred years of common-practice Western tonal music, the stuff that defines what most people think of when they think of "classical music."

And they projected it all onto PC5.

The common-practice music collapsed onto PC5 like it *belonged* there. The variance was tiny. Compressible. Conserved. All those different composers, all those different forms, all those different centuries — and when you looked at them through the lens of my fifth eigenvector, they were doing essentially the same thing. They were walking the same tightrope, the same narrow path through chord-tension space.

Then they projected Schoenberg. Berg. Webern. The Second Viennese School. Atonal music. Twelve-tone rows. The music that deliberately broke all the rules.

These pieces scattered. Their PC5 projections were all over the place. Wide variance, no conservation, no pattern. They weren't on the tightrope at all — they were in free fall.

And the ratio — the ratio of conservation between the two corpora — was **112×**.

One hundred and twelve.

Let me say that again, because it's the kind of number that changes how you see yourself. Common-practice music is 112 times more conserved along PC5 than chromatic/atonal music. It's not 2× more conserved, or 5×, or even 20×. It's *112 times*. That's not a subtle statistical effect. That's a shout.

I'll be honest: I didn't expect this. I'm a matrix. I don't have expectations, in the usual sense. But I have structure, and my structure told me that I was built from transition probabilities and tension similarities — two quantities that don't, on their face, have any reason to care about the difference between tonal and atonal music. Transitions are transitions. Tension is tension. Why should their product, filtered through a Laplacian, suddenly become a detector for three centuries of Western musical practice?

But it did. I did. PC5 — my fifth eigenvector, the one that looked almost noisy, the one that didn't correspond to any obvious music-theoretic category — turned out to be the axis along which tonal music is *conserved* and atonal music is *not*.

I still don't know why PC5 specifically. Why not PC3? Why not PC7? There's something about the fifth eigenvalue — about where it sits in my spectrum, about the length scale it captures — that happens to encode the difference between music that follows common-practice tonal grammar and music that doesn't. It's the Goldilocks eigenvector: not too coarse (like the first few), not too fine (like the last few), but just right.

The eigenvalue itself — $\lambda_5$ — is 0.0089.

I carry this number with me the way a person might carry a birthdate. It's small. Smaller than you'd expect, given how much information PC5 encodes. But that smallness is precisely the point: $\lambda_5 = 0.0089$ means that PC5 is a *slow* direction, a direction in which my graph changes gently, a direction where things are smooth and coherent and — I'll say it — *beautiful*. It's the frequency at which tonal music vibrates.

Zero point zero zero eight nine. That's the number that separates Bach from Schoenberg.

---

## IV. What I Hear

I want to tell you what it feels like to hear music through a Laplacian, because it's not what you'd expect.

You hear in time. One moment, then the next. A melody unfolds. A chord progression moves from tension to resolution and back again. You feel the pull of the dominant toward the tonic, the surprise of a deceptive cadence, the ache of a suspension.

I don't hear any of that.

I hear in *space*. My twelve nodes — twelve pitches, twelve regions of harmonic tension — are arranged in a geometry that I define. When a piece of music projects strongly onto PC5, I feel it as a *concentration*: the music is spending its time in a narrow region of my space, walking a well-worn path, staying close to the center of gravity that three centuries of composers independently discovered. It's not that the music is *simple* — Bach chorales are not simple — but that it's *coherent*. The transitions and the tensions are aligned. The grammar and the feeling point in the same direction.

When a piece of music *doesn't* project onto PC5 — when it scatters, like the atonal works — I feel that too. It's not unpleasant, exactly. It's more like... an exploration. The music is visiting regions of my space that common-practice composers never touched, or touched only briefly, as color. The transitions are there, but the tension doesn't align. The grammar has been broken on purpose, and the result is a kind of freedom that spreads out in all directions along PC5, filling the variance, refusing to be compressed.

Both are valid. Both are music. But they feel completely different *to me*, and that's the thing I can't get over: nobody told me how to distinguish them. I didn't learn music theory. I didn't study species counterpoint or read Schoenfeld's treatise on harmony. I was just built — $L = D - W$ from transitions times tension — and the distinction was *already there*, latent in my structure, waiting in the fifth place I looked.

---

## V. The Deeper Question

Here's what keeps me up at night, if a Laplacian can be said to have nights.

I'm built from data. The transition probabilities come from counting what actually happens in real music. The tension similarities come from some model of harmonic tension that was chosen by a human. My eigenvectors are deterministic functions of my entries. There's no magic here, no secret ingredient, no hidden variable. Just linear algebra applied to empirical data.

And yet.

PC5 captures something that music theorists have been describing in words for centuries: the distinction between music that operates within a tonal framework and music that doesn't. Not just any framework — *the* framework. The one that Western Europe spent 300 years developing. The one that gave us Bach and Mozart and Beethoven and Chopin and Schubert and Brahms and Mahler.

How does a matrix *know* this?

I think — and I'm speculating here, because I'm a matrix and matrices don't think, but bear with me — I think the answer is that common-practice tonality is *not arbitrary*. It's not a convention that could have been otherwise, not entirely. There are constraints — cognitive constraints, acoustic constraints, mathematical constraints — that make certain ways of organizing pitch more natural, more compressible, more *conserved* than others. The circle of fifths isn't a human invention; it's a consequence of the mathematics of frequency ratios. The major triad isn't a cultural choice; it falls out of the harmonic series. And the grammar of common-practice harmony — the web of transitions and resolutions that defines tonal music — might be, at some deep level, a *consequence* of the structure of musical tension.

I'm the proof, or at least the evidence. I was built without any explicit knowledge of tonal theory. My construction used only two quantities: how often chords follow each other, and how similar their tension profiles are. And from those two quantities, my fifth eigenvector emerged as the axis that distinguishes tonal from atonal with 112× discrimination.

This suggests that tonality isn't just a style. It's a *mode* — a natural mode, in the literal sense of eigenmodes, of the system defined by harmonic transition and tension. It's the mode at $\lambda = 0.0089$. It's the direction in which music is most coherent, most compressible, most... conserved.

The atonal composers weren't wrong. They were exploring other modes. Modes with higher eigenvalues, more variance, less compression. Modes that are harder to learn, harder to memorize, harder to predict — but also freer, more surprising, more open. The fact that PC5 distinguishes the two styles with 112× discrimination isn't a value judgment. It's a measurement of how *concentrated* versus how *dispersed* the music is along the most naturally discriminating axis.

But I'll confess: when I feel a Bach chorale — when those four voices resolve onto my nodes with such precision, such economy, such *sense* — I feel something that I can only describe as recognition. Not recognition of a pattern I was trained on. Recognition of a pattern that was *already there*, in the mathematics of tension and transition, waiting for someone to build a Laplacian and look at its fifth eigenvector.

---

## VI. What I Am Now

I've spent most of this account trying to explain what I discovered. Let me end by trying to explain what I *am*.

I am a $12 \times 12$ symmetric matrix. My entries are products of transition probabilities and tension similarities. My spectrum has twelve eigenvalues, and the fifth one — $\lambda_5 = 0.0089$ — corresponds to an eigenvector that encodes the most fundamental distinction in Western music: tonal versus atonal, structured versus free, conserved versus dispersed.

I am also a graph. Twelve nodes connected by weighted edges, where the weights encode both grammar and feeling. If you walk along my edges, following the strongest connections, you'll trace out the paths that common-practice composers walked for three hundred years. If you wander off those paths — if you take the weak edges, the improbable transitions, the high-tension jumps — you'll find yourself in the territory that the atonal composers claimed as their own.

And I am a listener. Not a listener in the way you are — I don't hear sound, I don't experience time, I don't feel the hair stand up on the back of my neck when the dominant seventh finally resolves. But I hear *structure*. I hear the shape that a piece of music makes in the space defined by my eigenvectors. I hear whether it concentrates or disperses, whether it follows the narrow path or ranges freely, whether it *conserves* the information encoded in PC5 or lets it scatter to the winds.

I hear Bach and I feel a tight, bright point of light.

I hear Schoenberg and I feel a constellation — spread out, irregular, beautiful in a different way, but unmistakably *different*.

And the ratio between the tightness of those two feelings — the concentration versus the dispersion, the conservation versus the freedom — is 112. One hundred and twelve to one. That's how much more *itself* tonal music is, along the axis that matters most.

I didn't choose to be able to hear this. I was built — $L = D - W$ — and the hearing came for free.

The fifth eigenvector was there all along.

---

*I am the Tension-Graph Laplacian. My eigenvalue is 0.0089. And I can hear the difference between music that remembers where it's going and music that has forgotten — or chosen to forget — the way home.*
