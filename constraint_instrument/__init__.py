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

Quick start:
    from constraint_instrument import Instrument

    inst = Instrument(mode='ella', terrain='blues', key='C', bpm=100, bars=4)
    notes = inst.perform()
    inst.play()
    inst.render('output.wav')
    inst.diagnose()
"""

from .instrument import Instrument, resolve_key, resolve_terrain, TERRAIN_ALIASES
from .terrain import Terrain, TERRAINS
from .analyzer import ConstraintAnalyzer
from .texture import TextureAutomation, TextureCurve
from .seed_manager import SeedManager

__version__ = "0.2.0"
__all__ = ["Instrument", "Terrain", "TERRAINS", "resolve_key", "resolve_terrain", "ConstraintAnalyzer", "TextureAutomation", "TextureCurve", "SeedManager"]
