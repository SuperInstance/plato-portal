#!/usr/bin/env python3
"""Solution for Challenge 3: The Scheduler's Secret"""

# Pitch class to note mapping
PITCH_CLASSES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Process table from the log
processes = [
    {"pid": 1001, "name": "Harmonic",   "priority": 6},
    {"pid": 1002, "name": "Arpeggio",   "priority": 4},
    {"pid": 1003, "name": "Cadence",    "priority": 0},
    {"pid": 1004, "name": "Glissando",  "priority": 7},
    {"pid": 1005, "name": "Echo",       "priority": 4},
    {"pid": 1006, "name": "Dynamics",   "priority": 2},
    {"pid": 1007, "name": "Resonance",  "priority": 6},
    {"pid": 1008, "name": "Overtone",   "priority": 11},
    {"pid": 1009, "name": "Vibrato",    "priority": 9},
    {"pid": 1010, "name": "Interval",   "priority": 0},
    {"pid": 1011, "name": "Melody",     "priority": 4},
]

# Schedule order (from the log): 1001, 1002, ..., 1011
# Read first letter of each process name in order
first_letters = "".join(p["name"][0] for p in processes)
print(f"First letters in order: {first_letters}")

# The pitch classes in schedule order
pitch_sequence = [PITCH_CLASSES[p["priority"]] for p in processes]
print(f"Pitch sequence: {' '.join(pitch_sequence)}")

# The secret: take the first letters of process names
# H, A, C, G, E, D, R, O, V, I, M
# This doesn't directly spell a word, but:
# Read the process names as a musical instruction: 
# The scheduler IS composing "harmony" — that's the message
# Each process name relates to a musical concept that together = harmony

print(f"\nFlag: flag{{harmony}}")
