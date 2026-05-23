"""constraint-substrate — The 5 irreducible primitives."""

from .lattice import snap, snap_batch, COVERING_RADIUS
from .funnel import step as funnel_step, step_batch as funnel_batch
from .holonomy import winding as holonomy_winding
from .rigidity import is_laman
from .consensus import round as consensus_round

__version__ = "0.2.0"
__all__ = [
    "snap",
    "snap_batch",
    "COVERING_RADIUS",
    "funnel_step",
    "funnel_batch",
    "holonomy_winding",
    "is_laman",
    "consensus_round",
]
