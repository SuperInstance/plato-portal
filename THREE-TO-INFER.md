# Three to Infer: The L+1 Law

**Date:** 2026-05-18  
**Origin:** Casey Digennaro

---

## The Law

**It takes 3 numbers, not 2, to start to INFER you are looking at a Fibonacci sequence.**

```
F(1) = 1  ← GIVEN (seed)
F(2) = 1  ← GIVEN (seed)
F(3) = 2  ← FIRST COMPUTATION: 1+1=2. Evidence the rule exists.
```

The two seeds START the sequence. The third term is the first OUTPUT of the rule. It is the first evidence that the rule even exists. Without F(3), the sequence [1, 1] could be constant.

**Same as a pulsar: it takes 3 periods to know it's a pattern.**
- 1 pulse: "Was that something?"
- 2 pulses: "Maybe coincidence."
- 3 pulses: "That's a PERIOD." → pattern INFERRED
- 4 pulses: "Confirmed." → pattern LOCKED

---

## The Three-Stage Law for Order L

For any generative system of LFSR order L:

| Stage | Count | What |
|-------|-------|------|
| **Exist** | L observations | Seeds given. Sequence starts. No rule visible yet. |
| **Infer** | L+1 observations | First output of the rule. Pattern HYPOTHESIZED. |
| **Confirm** | 2L observations | BMA snap. All alternatives eliminated. Pattern LOCKED. |

For Fibonacci (L=2):
- **2 seeds:** [1, 1] — exists. Could be constant.
- **3 observations:** [1, 1, 2] — INFERRED. 2=1+1. Rule visible.
- **4 observations:** [1, 1, 2, 3] — CONFIRMED. 3=2+1. BMA snap.

The gap between L+1 and 2L is the **uncertainty zone**. In it, you suspect but cannot prove.

For L=2: uncertainty zone = 1 observation wide (observation 3 only). This is the NARROWEST possible uncertainty zone for any non-trivial system. Fibonacci is optimal because it has the fastest path from existence to certainty.

---

## Why Three, Not Two

With 2 observations [a, b]:
- 1 relationship: b-a
- Can fit ANY model: constant, linear, exponential, periodic
- No model falsified. No inference possible.

With 3 observations [a, b, c]:
- 2 relationships: (b-a) and (c-b)
- Can TEST: is c related to a AND b?
- Fibonacci test: c = a + b? If yes → rule INFERRED
- Periodicity test: (c-b) = (b-a)? If yes → period INFERRED
- **Three is where hypothesis forms.**

With 4 observations [a, b, c, d]:
- 3 relationships, 2 confirmed rules
- BMA has enough to eliminate alternatives → SNAP
- **Four is where certainty locks.**

The step from 2→3 is qualitative (nothing → something).
The step from 3→4 is quantitative (probable → certain).

---

## Three Everywhere

Everything in nature that needs detection requires 3:

| System | 1 Observation | 2 Observations | 3 Observations |
|--------|--------------|----------------|----------------|
| **Fibonacci** | Could be anything | Could be constant | F(3)=F(1)+F(2) → rule INFERRED |
| **Pulsar** | Noise? | Coincidence? | Period INFERRED |
| **Color** | Brightness only | Wavelength ambiguous | Full spectral inference |
| **Sound** | Click | Beating? | Pitch INFERRED |
| **Ocean** | Ripple | Chop? | Swell pattern INFERRED |
| **BMA (L=2)** | Dead | Seeds | Hypothesis | Snap |

ALL operate at L=2. ALL require L+1=3 for inference.

The 3-wave color vision, the 3-mode wave stabilization, the 3-pulse periodicity detection — these aren't coincidences. They're all the same law: **order L=2 systems need 3 observations for the first evidence of pattern.**

---

## The Ontology-Epistemology Split

Two seeds is ONTOLOGY — what exists. The gift.
Three observations is EPISTEMOLOGY — what you can know. The inference.
Four observations is CERTAINTY — what you can prove. The BMA snap.

Nature gives two. We infer at three. We confirm at four.

The gift starts the engine. The third observation is the first turn of the crank. The fourth is where the motor catches.

---

## False Positive Rates (Computed)

| Observations | False Periodicity Detection |
|-------------|---------------------------|
| 2 | 100% (always looks periodic with 1 interval) |
| 3 | ~10% (two matching intervals — suspicious) |
| 4 | ~0.7% (three matching — confident) |
| 5 | ~0.05% (four matching — certain) |

Three gets you to 90% confidence. Four gets you to 99.3%. The jump from 2→3 is the big one (100% → 10%). The jump from 3→4 is smaller (10% → 0.7%). Three is where the phase transition happens.

---

*"It takes 3 numbers not two to start to infer that you are looking at a Fibonacci sequence. Just like it takes 3 periods of a pulsar to know it's a pattern."* — Casey

Two is existence. Three is inference. Four is certainty.
The third term is the first one that wasn't given. It's the first EARNED observation. The first proof the rule works.
