# constraint-synth CTF Challenges

> *"The music hides secrets. The lattice reveals them."*

A set of Capture The Flag challenges that teach consonance theory, dial positions, and the constraint-synth ecosystem through puzzle-solving.

## Challenges

### 1. The Hidden Message (Easy)
**File:** `ctf_challenges/hidden_message.wav`

A WAV file contains a melody where each note's consonance score maps to an ASCII character. Decode the message.

**Flag format:** `flag{message_here}`

### 2. The Lost Tradition (Medium)
**File:** `ctf_challenges/lost_tradition.dial`

Given a set of dial positions from a "lost tradition," find the center of the cluster. The flag is the coordinate.

**Flag format:** `flag{V.H_S.H_S.H}` (rounded to 2 decimal places)

### 3. The Scheduler's Secret (Medium)
**File:** `ctf_challenges/scheduler_log.txt`

A kernel log from a C-SCHED system shows process schedules. Each process's priority maps to a pitch class. Decode the word.

**Flag format:** `flag{word}`

### 4. The Anti-Music Detector (Hard)
**Files:** `ctf_challenges/audio_samples/sample_01.wav` through `sample_10.wav`

10 WAV files — some are music, some are anti-music (consonance below random threshold). Classify each. The flag is the concatenated indices of music files.

**Flag format:** `flag{XXXXXXXXXX}` (1=music, 0=anti-music)

### 5. The Dial Cipher (Expert)
**File:** `ctf_challenges/dial_cipher.txt`

An encrypted message where each character is encoded as a dial position `(V, H, S)`. The key is the nearest tradition to each position, used as a one-time pad. Decode the message.

**Flag format:** `flag{decoded_message}`

## Setup

```bash
pip install numpy scipy
python dial_interpreter.py  # From the dial_lang experiment
```

## Difficulty Guide

| Challenge | Difficulty | Concepts Tested |
|-----------|-----------|-----------------|
| Hidden Message | ⭐ Easy | Consonance scoring, ASCII mapping |
| Lost Tradition | ⭐⭐ Medium | Cluster analysis, tradition mapping |
| Scheduler's Secret | ⭐⭐ Medium | Pitch classes, kernel logs |
| Anti-Music Detector | ⭐⭐⭐ Hard | Threshold detection, batch analysis |
| Dial Cipher | ⭐⭐⭐⭐ Expert | Tradition XOR cipher, dial positions |

## Rules

1. All challenges can be solved using only the tools in this repository
2. No brute-forcing — each challenge has a logical path
3. Progressive hints are available in `HINTS.md`
4. The goal is learning, not just solving

---

*Built for the constraint-synth research project. Each challenge teaches a core concept.*
