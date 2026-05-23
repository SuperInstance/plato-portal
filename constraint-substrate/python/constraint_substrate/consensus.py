"""Metronome consensus rounds.

For angular/cyclic values (e.g. phase, clock position), arithmetic mean
fails near wrap-around boundaries (e.g. averaging 0.1 and 9.9 with modulus 10
should give 0.0, not 5.0). Use circular mean (atan2-based) instead.
"""

import math
from typing import List, Optional, Tuple


def _circular_mean(
    values: List[float], modulus: Optional[float] = None
) -> float:
    """Compute circular mean using atan2.

    If modulus is None, falls back to arithmetic mean (non-cyclic data).
    Otherwise, treats values as cyclic on [0, modulus) and computes the
    circular mean via the atan2 method.
    """
    if not values:
        return 0.0

    if modulus is None or modulus <= 0:
        return sum(values) / len(values)

    # Map values to angles on [0, 2π)
    two_pi = 2.0 * math.pi
    sin_sum = 0.0
    cos_sum = 0.0
    for v in values:
        angle = (v / modulus) * two_pi
        sin_sum += math.sin(angle)
        cos_sum += math.cos(angle)

    mean_angle = math.atan2(sin_sum / len(values), cos_sum / len(values))
    # atan2 returns [-π, π]; map back to [0, 2π)
    if mean_angle < 0:
        mean_angle += two_pi

    return (mean_angle / two_pi) * modulus


def round(
    values: List[float],
    epsilon: float,
    modulus: Optional[float] = None,
) -> Tuple[List[float], bool]:
    """One round of metronome consensus.

    If modulus is provided, uses circular mean (atan2-based) to correctly
    handle wrap-around for cyclic/phase values. Otherwise uses arithmetic mean.

    Returns (new_values, converged).
    """
    if not values:
        return ([], True)

    mean = _circular_mean(values, modulus)
    new_values = []
    all_converged = True

    for v in values:
        diff = mean - v
        # For cyclic values, take shortest path around the circle
        if modulus is not None and modulus > 0:
            diff = ((diff + modulus / 2.0) % modulus) - modulus / 2.0
        if abs(diff) > epsilon:
            all_converged = False
            new_values.append(v + math.copysign(epsilon * 0.5, diff))
        else:
            new_values.append(mean)

    return (new_values, all_converged)
