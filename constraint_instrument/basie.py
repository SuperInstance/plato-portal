"""
Basie Mode — Real-Time Consensus.

Count Basie's band could swing with strangers. This mode simulates
real-time constraint negotiation between multiple players finding
consensus through iteration.

Key concepts:
- Jam session: multiple players with independent constraint models
- Consensus: the shared constraint model that emerges
- Groove: when all players lock onto the same feel
"""

import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .terrain import Terrain, TERRAINS


@dataclass
class PlayerModel:
    """Each player's independent constraint model."""
    name: str
    instrument: str
    tempo_perception: float       # what BPM they think it is
    key_perception: int           # what key they think it's in
    swing_amount: float           # how much swing they feel
    density: float                # how many notes per beat
    register: Tuple[int, int]     # their register range
    listening_weight: float = 0.5 # how much they adapt to others


@dataclass
class GrooveState:
    """The current state of group consensus."""
    tempo_consensus: float        # average perceived tempo
    key_consensus: int            # agreed key
    swing_consensus: float        # agreed swing feel
    pocket: float                 # 0=no groove, 1=locked
    description: str = ""


class JamSession:
    """A jam session with multiple players finding consensus."""

    def __init__(self, players: int, tempo: int, key: int, style: str,
                 terrain: Terrain):
        self.terrain = terrain
        self.target_tempo = tempo
        self.target_key = key
        self.style = style
        self.locked = False
        self.iteration = 0

        # Create players with slightly different perceptions
        instruments = ["piano", "sax", "trumpet", "bass", "drums",
                       "guitar", "trombone", "voice"]
        self.players: Dict[str, PlayerModel] = {}

        for i in range(players):
            inst = instruments[i % len(instruments)]
            # Each player starts with slightly different perceptions
            tempo_drift = random.gauss(0, tempo * 0.05)
            key_drift = random.choice([0, 0, 0, 0, 5, 7])  # usually right key
            swing = random.gauss(0.5, 0.15)

            self.players[inst] = PlayerModel(
                name=inst,
                instrument=inst,
                tempo_perception=tempo + tempo_drift,
                key_perception=key + key_drift,
                swing_amount=max(0.0, min(1.0, swing)),
                density=random.uniform(0.3, 0.7),
                register=self._default_register(inst),
                listening_weight=random.uniform(0.3, 0.8),
            )

    def _default_register(self, instrument: str) -> Tuple[int, int]:
        ranges = {
            "piano": (48, 84), "sax": (54, 79), "trumpet": (55, 79),
            "bass": (36, 60), "drums": (36, 50), "guitar": (40, 72),
            "trombone": (40, 67), "voice": (55, 74),
        }
        return ranges.get(instrument, (48, 84))

    def play(self, my_role: str = "piano", listen: bool = True,
             lead: bool = False, bars: int = 12) -> dict:
        """
        Play a round. Players adapt toward consensus if listening.
        """
        self.iteration += 1

        if listen and self.iteration > 1:
            self._adapt_players()

        # Generate notes for each player
        all_notes = {}
        for name, player in self.players.items():
            notes = self._generate_player_notes(player, bars)
            all_notes[name] = notes

        groove = self.consensus()
        return {
            "iteration": self.iteration,
            "notes": all_notes,
            "my_role": my_role,
            "groove": groove,
            "locked": self.locked,
        }

    def _adapt_players(self):
        """Players listen and adapt their models toward consensus."""
        avg_tempo = sum(p.tempo_perception for p in self.players.values()) / len(self.players)
        # Mode of key perceptions
        key_counts = {}
        for p in self.players.values():
            key_counts[p.key_perception] = key_counts.get(p.key_perception, 0) + 1
        consensus_key = max(key_counts, key=key_counts.get)
        avg_swing = sum(p.swing_amount for p in self.players.values()) / len(self.players)

        for player in self.players.values():
            w = player.listening_weight
            # Adapt toward group average
            player.tempo_perception += w * (avg_tempo - player.tempo_perception) * 0.3
            player.key_perception = int(player.key_perception + w * (consensus_key - player.key_perception) * 0.5)
            player.swing_amount += w * (avg_swing - player.swing_amount) * 0.2

    def consensus(self) -> GrooveState:
        """Measure the current group consensus."""
        tempos = [p.tempo_perception for p in self.players.values()]
        keys = [p.key_perception for p in self.players.values()]
        swings = [p.swing_amount for p in self.players.values()]

        avg_tempo = sum(tempos) / len(tempos)
        # Most common key
        key_counts = {}
        for k in keys:
            key_counts[k] = key_counts.get(k, 0) + 1
        consensus_key = max(key_counts, key=key_counts.get)
        avg_swing = sum(swings) / len(swings)

        # Pocket: how tight is the consensus (low variance = high pocket)
        tempo_var = sum((t - avg_tempo)**2 for t in tempos) / len(tempos)
        key_agreement = key_counts[consensus_key] / len(keys)
        swing_var = sum((s - avg_swing)**2 for s in swings) / len(swings)

        pocket = (1.0 - min(1.0, tempo_var / 100.0)) * key_agreement * (1.0 - min(1.0, swing_var / 0.1))
        pocket = max(0.0, min(1.0, pocket))

        if pocket > 0.9:
            desc = "Locked in! All players sharing the same feel."
        elif pocket > 0.7:
            desc = "Close — the groove is forming."
        elif pocket > 0.4:
            desc = "Finding it — players converging."
        else:
            desc = "Loose — still searching for consensus."

        self.locked = pocket > 0.85

        return GrooveState(
            tempo_consensus=round(avg_tempo, 1),
            key_consensus=consensus_key,
            swing_consensus=round(avg_swing, 3),
            pocket=round(pocket, 3),
            description=desc,
        )

    def lock(self) -> GrooveState:
        """Force consensus — lock all players to the same model."""
        groove = self.consensus()
        for player in self.players.values():
            player.tempo_perception = groove.tempo_consensus
            player.key_perception = groove.key_consensus
            player.swing_amount = groove.swing_consensus
        self.locked = True
        groove.pocket = 1.0
        groove.description = "Consensus achieved. All players sharing the same constraint model."
        return groove

    def _generate_player_notes(self, player: PlayerModel, bars: int) -> List[dict]:
        """Generate notes for one player based on their model."""
        bpm = player.tempo_perception
        beat_dur = 60.0 / bpm
        notes = []
        t = 0.0
        duration = bars * 4 * beat_dur

        degrees = [d.degree for d in self.terrain.scale_degrees]
        weights = [d.weight for d in self.terrain.scale_degrees]

        while t < duration:
            if random.random() > player.density:
                t += beat_dur * random.choice([0.5, 1.0])
                continue

            degree = random.choices(degrees, weights=weights)[0]
            pitch = player.key_perception + degree
            # Clamp to register
            pitch = max(player.register[0], min(player.register[1], pitch))

            # Swing timing
            swing_offset = player.swing_amount * beat_dur * 0.33
            if random.random() < 0.5:
                swing_offset = -swing_offset

            notes.append({
                "pitch": pitch,
                "velocity": random.randint(50, 100),
                "start": round(t + swing_offset, 3),
                "duration": round(beat_dur * random.choice([0.5, 1.0]), 3),
            })
            t += beat_dur * random.choice([0.5, 1.0, 1.0])

        return notes


class BasieEngine:
    """Real-time consensus engine."""

    def __init__(self, terrain: Terrain, key: int = 60):
        self.terrain = terrain
        self.key = key

    def join_jam(self, players: int = 4, tempo: int = 140,
                 key: Optional[int] = None, style: str = "swing") -> JamSession:
        """Create a new jam session."""
        return JamSession(
            players=players,
            tempo=tempo,
            key=key or self.key,
            style=style,
            terrain=self.terrain,
        )
