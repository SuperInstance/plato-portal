#!/usr/bin/env python3
"""Solution for Challenge 1: The Hidden Message"""
import math

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

# Positions from the challenge file
positions = [
    (2.392, 2.941, 0.050),
    (0.179, 1.205, 1.557),
    (0.259, 2.346, 1.791),
    (1.090, 0.219, 0.447),
    (2.959, 0.906, 0.329),
    (1.750, 0.100, 0.787),
    (1.944, 1.096, 0.675),
    (1.134, 2.773, 2.825),
]

# Formula: ASCII_code = round(score * 95) + 32
message = ""
for v, h, s in positions:
    score = consonance_score(v, h, s)
    char_code = round(score * 95) + 32
    message += chr(char_code)

print(f"Decoded: {message}")
print(f"Flag: flag{{{message.lower()}}}")
