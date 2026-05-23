"""
Constraint Instrument — A constraint-music toolset inspired by jazz masters.

Seven modes, seven ways of relating to constraint space:
  Parker   — practice & internalize the lattice
  Miles    — explore the frontier, always new
  Ellington — architect for emergence
  Basie    — real-time consensus
  Goodman  — diagnostic, find what's missing
  Armstrong — liberation through constraint removal
  Ella     — pure flow, the tool disappears
"""

from .instrument import Instrument
from .terrain import Terrain, TERRAINS

__version__ = "0.1.0"
__all__ = ["Instrument", "Terrain", "TERRAINS"]
