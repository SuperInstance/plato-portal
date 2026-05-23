"""Deadband convergence funnel."""

import math


def step(
    current: float, target: float, epsilon: float, decay_rate: float
) -> tuple[float, float]:
    """One step of deadband convergence with exponential decay.

    The epsilon (deadband width) decays exponentially:
        new_eps = epsilon * exp(-decay_rate)
    NOT linearly as epsilon * (1 - decay_rate).

    Exponential decay ensures:
    - Strictly positive epsilon (never reaches zero)
    - Smooth, natural convergence characteristic
    - Consistent halving behavior independent of current epsilon

    Returns (new_value, new_epsilon).
    """
    diff = target - current
    new_eps = epsilon * math.exp(-decay_rate)

    if abs(diff) < epsilon:
        # Within deadband — snap toward target
        correction = diff * (1.0 - math.exp(-decay_rate))
        return (current + correction, new_eps)
    else:
        # Outside deadband — pull toward target
        step_size = math.copysign(epsilon, diff)
        return (current + step_size, new_eps)


def step_batch(
    currents: list[float],
    targets: list[float],
    epsilons: list[float],
    decay: float,
) -> tuple[list[float], list[float]]:
    """Batch funnel step for N agents."""
    results = [step(c, t, e, decay) for c, t, e in zip(currents, targets, epsilons)]
    new_values = [r[0] for r in results]
    new_eps = [r[1] for r in results]
    return (new_values, new_eps)
