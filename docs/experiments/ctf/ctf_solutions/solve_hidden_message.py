#!/usr/bin/env python3
"""Solution for Challenge 1: The Hidden Message"""
import math

# Tradition landmarks
TRADITIONS = {
    "western": (2.72, 2.05, 1.80), "carnatic": (2.77, 3.63, 2.80),
    "jazz": (2.30, 2.50, 2.10), "gamelan": (1.40, 1.20, 2.90),
    "blues": (2.10, 2.80, 1.60), "arabic": (2.50, 3.10, 2.30),
    "japanese": (1.80, 1.50, 2.20), "throat_singing": (2.90, 0.80, 3.00),
}

def consonance_score(v, h, s):
    min_dist = float('inf')
    for tv, th, ts in TRADITIONS.values():
        dist = math.sqrt((v - tv)**2 + (h - th)**2 + (s - ts)**2)
        min_dist = min(min_dist, dist)
    return max(0.0, 1.0 - (min_dist / 3.5))

# The positions from the challenge
positions = [
    (2.72, 2.05, 1.80), (2.30, 2.50, 2.10), (2.77, 3.63, 2.80),
    (2.77, 3.63, 2.80), (2.50, 3.10, 2.30), (1.40, 1.20, 2.90),
    (2.10, 2.80, 1.60), (2.72, 2.05, 1.80), (2.90, 0.80, 3.00),
    (2.50, 3.10, 2.30), (2.77, 3.63, 2.80), (1.80, 1.50, 2.20),
    (2.30, 2.50, 2.10), (2.90, 0.80, 3.00), (2.50, 3.10, 2.30),
]

# Compute consonance for each and map to ASCII
message = ""
for v, h, s in positions:
    score = consonance_score(v, h, s)
    char_code = round(score * 127)
    message += chr(char_code)

print(f"Decoded: {message}")
print(f"Flag: flag{{{message.lower().replace(' ', '_')}}}")
