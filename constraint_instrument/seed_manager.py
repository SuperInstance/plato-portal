"""
SeedManager — Deterministic reproducibility for the Constraint Instrument.

Same master seed + same parameters = identical output, every time.

This is critical for:
  - Education: repeatable exercises students can share
  - Testing: deterministic CI pipelines
  - Sharing: send seed+genre+params to reproduce exact output

Usage:
    from constraint_instrument.seed_manager import SeedManager

    sm = SeedManager(master_seed=42)

    # Get a deterministic RNG for a subsystem
    rng = sm.get_rng('melody')

    # Seed global random before a performance (for engines that use module-level random)
    sm.seed_global('perform')

    # Save/restore state
    state = sm.to_dict()
    sm2 = SeedManager.from_dict(state)

    # Fork a child
    child = sm.fork('tracks')
"""

import random
import json
from typing import Optional


class SeedManager:
    """Single master seed → deterministic random streams per subsystem.

    Guarantees: same master_seed always produces identical output.
    Each subsystem gets its own independent RNG stream, but all are
    derived from the single master seed.

    The global random module can be seeded deterministically for
    subsystems that use module-level random calls (which is most of
    the constraint_instrument engines).
    """

    def __init__(self, master_seed: int = 42):
        """Initialize with a master seed.

        Args:
            master_seed: The single source of determinism. Same seed = same output.
        """
        self._original_seed = master_seed
        self._master_rng = random.Random(master_seed)
        self._subsystems = {}  # name → random.Random instance
        self._subsystem_seeds = {}  # name → the seed that was assigned
        self._order = []  # track creation order for serialization
        self._global_seeds = {}  # purpose → seed value (for seeding global random)

    def get_rng(self, name: str) -> random.Random:
        """Get or create a deterministic RNG for subsystem 'name'.

        Same name always gets same stream for same master seed.
        Call order matters — first call for a name gets the next seed
        from the master RNG.

        Args:
            name: Subsystem identifier (e.g. 'perform', 'melody', '808')

        Returns:
            A random.Random instance with a deterministic seed
        """
        if name not in self._subsystems:
            seed = self._master_rng.randint(0, 2**32)
            self._subsystems[name] = random.Random(seed)
            self._subsystem_seeds[name] = seed
            self._order.append(name)
        return self._subsystems[name]

    def get(self, name: str) -> random.Random:
        """Alias for get_rng."""
        return self.get_rng(name)

    def seed_global(self, purpose: str) -> int:
        """Seed the global random module deterministically for a given purpose.

        Call this before any operation that uses module-level random calls.
        Same purpose + same master seed = same global random state.

        Args:
            purpose: What the global random is being used for
                     (e.g. 'perform', 'generate', 'loop')

        Returns:
            The seed value used
        """
        if purpose not in self._global_seeds:
            self._global_seeds[purpose] = self._master_rng.randint(0, 2**32)
        random.seed(self._global_seeds[purpose])
        return self._global_seeds[purpose]

    def reset(self, master_seed: Optional[int] = None):
        """Reset to initial state.

        Args:
            master_seed: New master seed, or None to reuse the original
        """
        if master_seed is not None:
            self._original_seed = master_seed
        self._master_rng = random.Random(self._original_seed)
        self._subsystems.clear()
        self._subsystem_seeds.clear()
        self._order.clear()
        self._global_seeds.clear()

    def to_dict(self) -> dict:
        """Serialize state for saving/loading sessions.

        Returns:
            Dict with all state needed to recreate this SeedManager
        """
        return {
            'master_seed': self._original_seed,
            'subsystem_seeds': dict(self._subsystem_seeds),
            'order': list(self._order),
            'global_seeds': dict(self._global_seeds),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SeedManager':
        """Restore from saved state.

        Args:
            data: Dict from to_dict()

        Returns:
            SeedManager in the exact same state
        """
        sm = cls(master_seed=data['master_seed'])

        # Replay the master RNG to the same position
        # by consuming the same number of random values
        n_subsystems = len(data.get('subsystem_seeds', {}))
        n_globals = len(data.get('global_seeds', {}))

        # Replay subsystem seeds
        for i in range(n_subsystems):
            sm._master_rng.randint(0, 2**32)

        # Replay global seeds
        for i in range(n_globals):
            sm._master_rng.randint(0, 2**32)

        # Restore subsystem state
        for name in data.get('order', []):
            seed = data['subsystem_seeds'][name]
            sm._subsystems[name] = random.Random(seed)
            sm._subsystem_seeds[name] = seed
            sm._order.append(name)

        sm._global_seeds = dict(data.get('global_seeds', {}))

        return sm

    def fork(self, name: str) -> 'SeedManager':
        """Create a child SeedManager seeded from this one.

        The child gets its own master seed derived from this manager,
        making it independent but deterministic.

        Args:
            name: Identifier for this fork

        Returns:
            A new SeedManager with a derived seed
        """
        child_seed = self._master_rng.randint(0, 2**32)
        return SeedManager(master_seed=child_seed)

    @property
    def master_seed(self) -> int:
        """The original master seed."""
        return self._original_seed

    def __repr__(self) -> str:
        return (f"SeedManager(master_seed={self._original_seed}, "
                f"subsystems={list(self._order)}, "
                f"globals={list(self._global_seeds.keys())})")

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'SeedManager':
        """Restore from JSON string."""
        return cls.from_dict(json.loads(json_str))
