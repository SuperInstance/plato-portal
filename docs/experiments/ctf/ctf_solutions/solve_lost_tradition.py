#!/usr/bin/env python3
"""Solution for Challenge 2: The Lost Tradition"""

positions = [
    (2.50, 1.85, 2.73), (2.55, 1.92, 2.78), (2.48, 1.87, 2.71),
    (2.53, 1.90, 2.76), (2.51, 1.88, 2.74), (2.54, 1.91, 2.77),
    (2.49, 1.86, 2.72), (2.52, 1.89, 2.75),
]

avg_v = sum(p[0] for p in positions) / len(positions)
avg_h = sum(p[1] for p in positions) / len(positions)
avg_s = sum(p[2] for p in positions) / len(positions)

print(f"Lost tradition center: ({avg_v:.2f}, {avg_h:.2f}, {avg_s:.2f})")
print(f"Flag: flag{{{avg_v:.2f}_{avg_h:.2f}_{avg_s:.2f}}}")
