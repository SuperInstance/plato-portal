#!/usr/bin/env python3
"""Solution for Challenge 5: The Dial Cipher"""
import math

# Tradition landmarks
TRADITIONS = {
    "western": (2.72, 2.05, 1.80), "carnatic": (2.77, 3.63, 2.80),
    "jazz": (2.30, 2.50, 2.10), "gamelan": (1.40, 1.20, 2.90),
    "blues": (2.10, 2.80, 1.60), "arabic": (2.50, 3.10, 2.30),
    "japanese": (1.80, 1.50, 2.20), "throat_singing": (2.90, 0.80, 3.00),
}

TRADITION_KEYS = {
    "western": ord('W'), "carnatic": ord('C'), "jazz": ord('J'),
    "gamelan": ord('G'), "blues": ord('B'), "arabic": ord('A'),
    "japanese": ord('J'), "throat_singing": ord('T'),
}

def nearest_tradition(v, h, s):
    best_name = "unknown"
    best_dist = float('inf')
    for name, (tv, th, ts) in TRADITIONS.items():
        dist = math.sqrt((v - tv)**2 + (h - th)**2 + (s - ts)**2)
        if dist < best_dist:
            best_dist = dist
            best_name = name
    return best_name

# Encoded data from the cipher file
encoded = [
    (2.72, 2.05, 1.80, 29),
    (1.40, 1.20, 2.90, 39),
    (2.10, 2.80, 1.60, 35),
    (2.50, 3.10, 2.30, 33),
    (2.77, 3.63, 2.80, 28),
    (2.72, 2.05, 1.80, 46),
    (2.90, 0.80, 3.00, 39),
    (2.30, 2.50, 2.10, 17),
    (1.80, 1.50, 2.20, 36),
    (2.72, 2.05, 1.80, 46),
    (2.72, 2.05, 1.80, 32),
    (1.40, 1.20, 2.90, 44),
    (2.10, 2.80, 1.60, 38),
    (2.50, 3.10, 2.30, 49),
    (2.77, 3.63, 2.80, 28),
    (2.72, 2.05, 1.80, 45),
    (2.90, 0.80, 3.00, 40),
    (2.30, 2.50, 2.10, 34),
    (1.80, 1.50, 2.20, 36),
    (2.72, 2.05, 1.80, 46),
    (2.50, 3.10, 2.30, 38),
]

message = ""
for v, h, s, encoded_char in encoded:
    trad = nearest_tradition(v, h, s)
    key = TRADITION_KEYS[trad]
    decoded = encoded_char ^ key
    message += chr(decoded)

print(f"Decoded: {message}")
print(f"Flag: flag{{{message.lower().replace(' ', '_')}}}")
