# Jazz Saxophonist User Report

*I don't read docs. I play. This is what I found.*

---

## What Worked 🟢

### Core flow is solid

```python
from constraint_instrument import Instrument
inst = Instrument(mode='parker', terrain='bebop', key='Bb', bpm=120, bars=8)
notes = inst.perform()
```

This just works. No friction. I got note dicts with pitch, velocity, start_time, duration. Felt natural.

### Setting keys works beautifully

`key='Bb'`, `key='F#'`, `key='Eb'` — all just work. No fumbling with MIDI numbers. The aliases are sensible. Even `key='Db'` works. A musician doesn't think in numbers.

### Tempo control is intuitive

BPM 60 (lazy ballad), 120 (swingin'), 240 (burnin'), 400 (insane). All work. Each produces note counts that make musical sense — slower = more notes per bar, faster = fewer. This is correct.

### diagnose() is genuinely useful

I ran 50+ tests and the diagnostic was never wrong about what I needed to practice:
- Star ratings (★★★★☆) feel like a real teacher
- Order breakdown (POSITION, DIRECTION, CURVATURE, STRUCTURE) matches how I think about my playing
- Prescriptions with specific exercises are actually good advice:
  - "Practice resolving the 7th to the root"
  - "Play a 3-chorus solo where chorus 1 = simple, chorus 2 = develop, chorus 3 = peak"
- The recommendation paragraph reads like a real teacher's feedback, not a stats dump

### `render()` to WAV works

```python
inst.render('solo.wav')
```
Instant. No questions asked. WAV comes out at the right sample rate, right duration.

### `to_midi()` works

Out comes a proper MIDI file — format 1, 1 track, 480 ticks/beat. Can load into any DAW.

### Multiple terrains produce genuinely different music

I tried bebop, blues, delta_blues, modal, free_jazz, afro_cuban, indian_raga, bluegrass, gospel, hip_hop_trap, free_improvisation, bebop_rich, electronic_techno, chinese_silk_bamboo — all 17 terrains. Each one gives different pitch sets, different feel. The constraint model is real. This isn't random note generation.

### Modes have distinct personalities

| Mode | Personality |
|------|------------|
| parker | Technical, vocabulary-driven, great for practice |
| ella | Fluid, flowy, feels like singing |
| miles | Exploratory, angular intervals |
| armstrong | Liberated, joyful |
| ellington | Architectural, structured |
| goodman | Diagnostic — knows what's wrong with itself |
| basie | ...silent (see below) |

### 17 terrains across wildly different traditions

Blues, Indian raga, Chinese silk-and-bamboo, Afro-Cuban, bluegrass, gospel, trap, techno... this isn't a "jazz toy." It's a world music constraint engine. Surprising depth.

### Deterministic with seeding

```python
import random; random.seed(42)
```
Same seed = same performance. This matters for practice — you can replay and analyze.

---

## What Didn't Work 🔴

### Basie mode produces 0 notes

Every terrain, every key, every BPM. Basie just sits there. Zero notes. Every time. Is this a bug or is Basie's "real-time consensus" model actually producing silence? If it's intentional as a feature (empty ensemble waiting for input), there's no documentation telling me what to do. If it's broken... well, it's broken.

### `key='anything'` throws a TypeError, not a ValueError

```python
# Key 'something' crashes with:
TypeError: sequence item 0: expected str instance, int found
```
The error message itself is broken — it has an `int` in a string join. Not good. Should say "Unknown key 'something'. Valid keys: C, C#, Db, D..."

### No typo tolerance on terrain names

`'bluz'`, `'beboop'`, `'moadl'` all fail. I get that you can't guess every typo, but at least a fuzzy match or a "Did you mean 'bebop'?" would save me. The error message lists 27 available terrains including aliases — that's too much information and not enough help.

### `bars=0` produces hundreds of notes (probably defaults to something)

```python
inst = Instrument(mode='parker', terrain='bebop', key='C', bpm=120, bars=0)
# Returns 359 notes instead of 0 or raising an error
```
This is either a bug (bars parameter silently ignored) or a safety fallback that goes wrong. Either way, `bars=0` should mean zero bars.

---

## What Was Confusing 🤔

### The 4-tier diagnostic structure isn't documented at the surface

POSITION, DIRECTION, CURVATURE, STRUCTURE — these make sense to a musician, but it took me 20 tests to realize they map to "orders" (0, 1, 2, 3). I kept thinking they were separate modes or something. They're actually a hierarchy of musical awareness. That needs to be surfaced because it's the tool's best feature.

### Can't pass chord progressions

I tried `Instrument(..., chords=['Bb7', 'Eb7', 'Bb7'])` and got a TypeError. A jazz musician's most basic request is "play over these changes." Without chord progressions, the instrument is just noodling. This is a fundamental gap.

### `play()` blocks for the entire duration

It blocks for 9 seconds to play 4 bars. No async, no callback, no way to interrupt. If I'm trying to call-and-response or loop, I can't. It just locks up.

### Can't switch instrument/voice

`Instrument(..., instrument='tenor_sax')` → TypeError. The output is always piano/synth. If I'm a sax player, I want to hear a sax. Even just a simple synth voice selection would help.

### No set_notes() or external input

I can't feed a human-played phrase into the diagnostic engine. I can't analyze my own playing. I can only analyze what the tool generates. Goodman mode seems like it should be able to diagnose anything, but it can only diagnose itself.

### `bars=0` vs `bars=-4` inconsistency

`bars=0` → 359 notes. `bars=-4` → 0 notes. That's inconsistent. Both should either error or produce zero notes.

### Sparse constructor parameters

`Instrument.__init__` only accepts: `mode`, `terrain`, `key`, `bpm`, `bars`. That's 5 parameters. For a tool with 7 modes and 17 terrains, that's minimal. I kept wanting to pass `instrument`, `chords`, `time_signature`, `swing_amount`, `register`.

---

## What Was Missing 🧩

### No chord progression support
Biggest gap for a jazz musician. Without chords, I can't practice changes, ii-V-I, turnarounds, or anything harmonic.

### No way to input my own notes
I can't play a phrase on my real sax, transcribe it to MIDI, and analyze it with the diagnostic engine.

### No swing control
Bebop at 120 BPM should swing. Does it? The output doesn't tell me. The `rhythmic_skeletons` have a `swing` parameter (0.4-0.6), but I can't adjust it.

### No time signature
Everything is 4/4 as far as I can tell. What about 3/4, 5/4, 7/8?

### No progress tracking across sessions
If I practice daily, I want to see my diagnose scores going up over time. Nothing persists.

### No audible difference between modes
Parker and Ella sound the same when played back. The mode differences are in the *process* of generation, not the *sound*. That's philosophically interesting but practically confusing.

### MIDI export gives no track/part names
One track, unnamed. Fine for import, but no instrument assignment, no meta events.

---

## What Surprised Me 😲

### Good: diagnose() is genuinely useful

Honestly, the diagnostic engine is the best part of this tool. I started out wanting to just generate solos. I ended up wanting to improve my real playing. The prescriptions are specific and good. The star ratings make me want to get 5 stars on STRUCTURE.

### Good: The terrain taxonomy is amazing

17 terrains from delta blues to Indian raga to Chinese silk-bamboo to trap. This isn't a jazz player's pet project — someone really thought about world music constraint spaces. The delta_blues terrain correctly uses a pentatonic minor shell with blue notes.

### Bad: 0 bars = 359 notes

This smells like a lazy default somewhere. `bars` might not actually control the note count in the way I expect.

### Bad: Basie is still a mystery

Basie mode = "real-time consensus" with a JamSession model. But it produces 0 notes and I have no idea why. Is it waiting for multiple instruments? Is it web-socketed to something? Does it need a band? No clue.

### Confusing: "mode" vs "terrain" is musically backwards

To a jazz musician: "mode" is about scales (Dorian, Mixolydian). "Terrain" feels like "style or feel." But here, "mode" is the performance engine (Parker/Ella/etc.) and "terrain" is the constraint space. The naming is swapped from what I'd expect. I kept wanting to call `mode='dorian'` and `terrain='parker'`.

### Good: 17 terrains * 7 modes = 119 combos

Most combos produce different-sounding solos. That's a lot of variety from one API.

---

## Top 5 Requests 🏆

### 1. Chord progression support
I need to practice over changes. Without this, I'm just noodling. Give me a `chords` parameter or a progression API. 12-bar blues, rhythm changes, ii-V-Is. This is the difference between a toy and a practice tool.

### 2. Human input analysis
Let me pass my own note data to `diagnose()`. I'll play on my sax, write it down, and you tell me what I need to practice. The diagnostic engine is wasted if it can only analyze itself.

### 3. Instrument/Voice selection + better audio
Let me choose `instrument='tenor_sax'` or `instrument='trumpet'`. Even a basic MIDI synth voice matters. I need to hear what I'm playing through a saxophone timbre, not a default piano.

### 4. Swing/Feel parameters
BPM alone isn't enough. Give me a `swing` slider (0.0-1.0), an `articulation` setting (legato/staccato), and feel controls. Jazz is in the feel, not just the notes.

### 5. Time signature support
3/4, 5/4, 7/8, 5/8, 12/8. Rhythm changes are in 4/4 but ballads can be 3/4. Without time signature, there's a whole dimension of music I can't access.

---

## If This Tool Did One Thing...

If this tool let me input a MIDI file of my own playing and run `diagnose()` on it — giving me star ratings, identifying my weakest "order," and prescribing exercises — I would use it every single day as my practice companion.

The generated solos are fun. The constraints are fascinating. But the feedback loop between "what I played" and "what I should practice" is where the real value lives.

Right now it's a clever musical autocomplete. If I could use it as a coach that listens to *me*, it'd be transformative.

---

*Signed: A jazz saxophonist who just wants to play*
