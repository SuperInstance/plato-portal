"""C FFI bindings for constraint-substrate via ctypes.

Loads libconstraint_substrate.so (built from C) and wraps all 5 primitives
with proper type conversion. Falls back gracefully if .so not available.
"""

import ctypes
import os
import platform
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# ---------------------------------------------------------------------------
# Locate the shared library
# ---------------------------------------------------------------------------

def _find_lib() -> Optional[str]:
    """Search for libconstraint_substrate.so in likely locations."""
    candidates = []
    
    # 1. Next to this file's package (python/constraint_substrate/)
    pkg_dir = Path(__file__).parent
    candidates.append(pkg_dir / "libconstraint_substrate.so")
    
    # 2. In the c/ directory (c/libconstraint_substrate.so)
    # Walk up from python/constraint_substrate/ -> constraint-substrate/c/
    substrate_root = pkg_dir.parent.parent
    candidates.append(substrate_root / "c" / "libconstraint_substrate.so")
    
    # 3. System library paths
    candidates.append(Path("libconstraint_substrate.so"))
    
    for c in candidates:
        expanded = Path(c).expanduser().resolve()
        if expanded.exists():
            return str(expanded)
    
    return None


_lib = None
_available = False

_lib_path = _find_lib()
if _lib_path is not None:
    try:
        _lib = ctypes.CDLL(_lib_path)
        _available = True
    except OSError:
        _available = False


def is_available() -> bool:
    """Return True if the C shared library was loaded successfully."""
    return _available


def lib_path() -> Optional[str]:
    """Return the path to the loaded .so, or None."""
    return _lib_path


# ---------------------------------------------------------------------------
# C struct definitions
# ---------------------------------------------------------------------------

class _CsSnapResult(ctypes.Structure):
    _fields_ = [("a", ctypes.c_double), ("b", ctypes.c_double), ("error", ctypes.c_double)]


class _CsEdge(ctypes.Structure):
    _fields_ = [("a", ctypes.c_uint32), ("b", ctypes.c_uint32)]


class _CsConsensusResult(ctypes.Structure):
    _fields_ = [("values", ctypes.POINTER(ctypes.c_double)), ("converged", ctypes.c_int)]


# ---------------------------------------------------------------------------
# Wrapped primitives (only populated if _available)
# ---------------------------------------------------------------------------

def snap(x: float, y: float, group_order: int = 3) -> Tuple[float, float, float]:
    """Snap a 2D point to the nearest Eisenstein A₂ lattice point via C.
    
    Returns (snapped_x, snapped_y, error_magnitude).
    """
    if not _available:
        raise RuntimeError("C shared library not available")
    _lib.cs_snap.restype = _CsSnapResult
    _lib.cs_snap.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_uint32]
    result = _lib.cs_snap(x, y, group_order)
    return (result.a, result.b, result.error)


def funnel_step(current: float, target: float, epsilon: float, decay_rate: float) -> Tuple[float, float]:
    """One step of deadband convergence funnel via C.
    
    Returns (new_value, new_epsilon).
    """
    if not _available:
        raise RuntimeError("C shared library not available")
    _lib.cs_funnel_step.restype = _CsSnapResult  # same layout: double, double
    _lib.cs_funnel_step.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    # Actually CsFunnelResult has {double value; double epsilon;} same layout as first two fields
    result = _lib.cs_funnel_step(current, target, epsilon, decay_rate)
    return (result.a, result.b)


def holonomy_winding(values: List[float], modulus: float) -> float:
    """Compute holonomy (winding number) via C."""
    if not _available:
        raise RuntimeError("C shared library not available")
    _lib.cs_holonomy.restype = ctypes.c_double
    _lib.cs_holonomy.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_uint32, ctypes.c_double]
    n = len(values)
    arr = (ctypes.c_double * n)(*values)
    return _lib.cs_holonomy(arr, n, modulus)


def is_laman(n: int, edges: List[Tuple[int, int]]) -> bool:
    """Check Laman rigidity via C."""
    if not _available:
        raise RuntimeError("C shared library not available")
    _lib.cs_is_laman.restype = ctypes.c_int
    _lib.cs_is_laman.argtypes = [ctypes.c_uint32, ctypes.POINTER(_CsEdge), ctypes.c_uint32]
    edge_count = len(edges)
    c_edges = (_CsEdge * edge_count)(*( _CsEdge(a, b) for a, b in edges ))
    return bool(_lib.cs_is_laman(n, c_edges, edge_count))


def consensus_round(values: List[float], epsilon: float, modulus: Optional[float] = None) -> Tuple[List[float], bool]:
    """One round of metronome consensus via C.
    
    Returns (new_values, converged).
    """
    if not _available:
        raise RuntimeError("C shared library not available")
    n = len(values)
    arr = (ctypes.c_double * n)(*values)
    
    _lib.cs_consensus_mod.restype = _CsConsensusResult
    _lib.cs_consensus_mod.argtypes = [
        ctypes.POINTER(ctypes.c_double), ctypes.c_uint32,
        ctypes.c_double, ctypes.c_double
    ]
    
    mod_val = modulus if modulus is not None and modulus > 0 else -1.0
    result = _lib.cs_consensus_mod(arr, n, epsilon, mod_val)
    
    new_values = [result.values[i] for i in range(n)]
    converged = bool(result.converged)
    
    _lib.cs_consensus_free(result)
    
    return (new_values, converged)
