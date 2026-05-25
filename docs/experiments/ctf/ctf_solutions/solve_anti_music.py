#!/usr/bin/env python3
"""Solution for Challenge 4: The Anti-Music Detector"""
import math

# Tradition landmarks
TRADITIONS = {
    "western": (2.72, 2.05, 1.80), "carnatic": (2.77, 3.63, 2.80),
    "jazz": (2.30, 2.50, 2.10), "gamelan": (1.40, 1.20, 2.90),
    "blues": (2.10, 2.80, 1.60), "arabic": (2.50, 3.10, 2.30),
    "japanese": (1.80, 1.50, 2.20), "throat_singing": (2.90, 0.80, 3.00),
}

RANDOM_THRESHOLD = 0.15

def consonance_score(v, h, s):
    min_dist = float('inf')
    for tv, th, ts in TRADITIONS.values():
        dist = math.sqrt((v - tv)**2 + (h - th)**2 + (s - ts)**2)
        min_dist = min(min_dist, dist)
    return max(0.0, 1.0 - (min_dist / 3.5))

# The 10 audio samples are generated from these positions:
sample_positions = [
    (2.72, 2.05, 1.80),  # 1: western → music (score ~0.87)
    (0.50, 0.50, 0.50),  # 2: deep space → anti-music
    (2.30, 2.50, 2.10),  # 3: jazz → music
    (0.10, 0.10, 0.10),  # 4: void → anti-music
    (2.77, 3.63, 2.80),  # 5: carnatic → music
    (0.30, 0.30, 0.30),  # 6: near void → anti-music
    (2.10, 2.80, 1.60),  # 7: blues → music
    (0.20, 0.20, 0.20),  # 8: void → anti-music
    (2.50, 3.10, 2.30),  # 9: arabic → music
    (0.15, 0.15, 0.15),  # 10: edge → anti-music
]

classification = ""
for i, (v, h, s) in enumerate(sample_positions, 1):
    score = consonance_score(v, h, s)
    is_music = 0 if score < RANDOM_THRESHOLD else 1
    label = "MUSIC" if is_music else "ANTI-MUSIC"
    print(f"Sample {i:2d}: ({v:.2f}, {h:.2f}, {s:.2f}) → consonance={score:.4f} → {label}")
    classification += str(is_music)

print(f"\nClassification: {classification}")
print(f"Flag: flag{{{classification}}}")
