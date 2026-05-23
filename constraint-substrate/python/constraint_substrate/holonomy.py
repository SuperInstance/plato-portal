"""Holonomy / winding number computation."""


def winding(values: list[float], modulus: float) -> float:
    """Compute holonomy (winding number) of a sequence of values modulo `modulus`."""
    if not values:
        return 0.0

    total = 0.0
    for i in range(1, len(values)):
        diff = values[i] - values[i - 1]
        wrapped = diff - modulus * round(diff / modulus)
        total += wrapped

    return total / modulus
