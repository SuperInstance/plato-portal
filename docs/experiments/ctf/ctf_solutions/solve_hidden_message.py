#!/usr/bin/env python3
"""Solution for Challenge 1: The Hidden Message"""
import math

# The WAV file contains 18 notes. Each note was synthesized at a position
# whose consonance score (multiplied by 95 and offset by 32) maps to an ASCII character.
# 
# The challenge file includes the actual consonance scores measured from the audio.
# Players must extract these from the audio and convert them.

# Pre-computed consonance scores (players derive these by analyzing the WAV)
scores = [
    0.863, 0.947, 0.863, 0.905, 0.337, 0.863, 0.905, 0.337,
    0.947, 0.863, 0.863, 0.905, 0.337, 0.905, 0.863, 0.905,
    0.947, 0.947
]

# Mapping: char = round(score * 95) + 32
message = ""
for s in scores:
    char_code = round(s * 95) + 32
    message += chr(char_code)

print(f"Decoded: {message}")
print(f"Flag: flag{{{message.lower().replace(' ', '_')}}}")
