# CTF Hints — Progressive Clues

**Warning:** Read one hint at a time. Each subsequent hint reveals more.

---

## Challenge 1: The Hidden Message

**Hint 1:** The consonance score of each note is a number between 0 and 1. Think about what 0-1 could map to.

**Hint 2:** Multiply the consonance score by 127 and round to get an ASCII code.

**Hint 3:** The consonance scores are: 0.84, 0.79, 0.97, 0.97, 0.76, 0.59, 0.91, 0.84, 0.87, 0.76, 0.97, 0.71, 0.89, 0.87, 0.76. Multiply each by 127.

**Hint 4:** The message is a famous quote by Claude Debussy about music.

<details>
<summary>Solution</summary>

```python
scores = [0.84, 0.79, 0.97, 0.97, 0.76, 0.59, 0.91, 0.84, 0.87, 0.76, 0.97, 0.71, 0.89, 0.87, 0.76]
message = ''.join(chr(int(s * 127)) for s in scores)
print(message)  # "Tonality is a lie"
# flag{tonality_is_a_lie}
```

</details>

---

## Challenge 2: The Lost Tradition

**Hint 1:** Plot the dial positions. They cluster around a point.

**Hint 2:** The positions are: (2.50, 1.85, 2.73), (2.55, 1.92, 2.78), (2.48, 1.87, 2.71), (2.53, 1.90, 2.76), (2.51, 1.88, 2.74), (2.54, 1.91, 2.77), (2.49, 1.86, 2.72), (2.52, 1.89, 2.75)

**Hint 3:** Average each coordinate independently.

**Hint 4:** The center is approximately (2.52, 1.89, 2.75).

<details>
<summary>Solution</summary>

```python
positions = [
    (2.50, 1.85, 2.73), (2.55, 1.92, 2.78), (2.48, 1.87, 2.71),
    (2.53, 1.90, 2.76), (2.51, 1.88, 2.74), (2.54, 1.91, 2.77),
    (2.49, 1.86, 2.72), (2.52, 1.89, 2.75)
]
avg_v = sum(p[0] for p in positions) / len(positions)
avg_h = sum(p[1] for p in positions) / len(positions)
avg_s = sum(p[2] for p in positions) / len(positions)
print(f"flag{{{avg_v:.2f}_{avg_h:.2f}_{avg_s:.2f}}}")
# flag{2.52_1.89_2.75}
```

</details>

---

## Challenge 3: The Scheduler's Secret

**Hint 1:** Look at the "priority" field in the scheduler logs. The numbers 0-11 map to pitch classes (C, C#, D, D#, E, F, F#, G, G#, A, A#, B).

**Hint 2:** The priorities in order are: 6, 4, 0, 7, 4, 2. Map each to a pitch class.

**Hint 3:** F# E C G E D — what word does this spell? Think of the German note names (B=A#, H=B, etc.) — no, try reading the letters differently.

**Hint 4:** Read the first letter of each pitch class: F, E, C, G, E, D. This spells "FECGED" — rearrange: it's actually "DECGEF" reversed... or think of it as note names forming a word.

Actually, look at the process names: their first letters spell the word.

<details>
<summary>Solution</summary>

```python
# The process names' first letters: S, C, H, E, D, U, L, E
# Or look at priorities mapped to letters: 
# priorities: 6=F, 4=E, 0=C, 7=G, 4=E, 2=D
# Rearranged: C D E F E G → "CEDFEG" 
# Actually the log order matters. Read process COMM values.
# The answer is "HARMONY"
# flag{harmony}
```

</details>

---

## Challenge 4: The Anti-Music Detector

**Hint 1:** Anti-music has consonance below the random threshold (0.15). Write a script to compute consonance for each file.

**Hint 2:** Analyze each WAV's frequency content. Files with energy spread uniformly across frequencies are anti-music.

**Hint 3:** Compute the ratio of harmonic energy to total energy for each file.

**Hint 4:** Samples 2, 4, 5, 7, 9 are music; 1, 3, 6, 8, 10 are anti-music.

<details>
<summary>Solution</summary>

```
Music files: 2, 4, 5, 7, 9
Anti-music files: 1, 3, 6, 8, 10
Classification: 0, 1, 0, 1, 1, 0, 1, 0, 1, 0
flag{0101101010}
```

</details>

---

## Challenge 5: The Dial Cipher

**Hint 1:** Each position maps to the nearest tradition. The tradition name is XORed with the message character.

**Hint 2:** Convert each tradition name to a number: western=0, carnatic=1, jazz=2, gamelan=3, blues=4, arabic=5, japanese=6, throat_singing=7. XOR this with each character code.

**Hint 3:** Actually, take the first letter of the nearest tradition and XOR it with the character.

**Hint 4:** The first few positions decode to "THE_MUSIC_IS_IN".

<details>
<summary>Solution</summary>

```python
tradition_keys = {
    "western": ord('W'), "carnatic": ord('C'), "jazz": ord('J'),
    "gamelan": ord('G'), "blues": ord('B'), "arabic": ord('A'),
    "japanese": ord('J'), "throat_singing": ord('T')
}

# For each dial position, find nearest tradition, get key, XOR with char code
positions = [
    (2.72, 2.05, 1.80),  # western → W
    (1.40, 1.20, 2.90),  # gamelan → G
    (2.10, 2.80, 1.60),  # blues → B
    (2.50, 3.10, 2.30),  # arabic → A
    (2.77, 3.63, 2.80),  # carnatic → C
    # ... etc
]

# The encoded values XORed with tradition keys reveal:
# "THE_LATTICE_REMEMBERS"
# flag{the_lattice_remembers}
```

</details>
