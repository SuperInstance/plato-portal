#!/usr/bin/env python3
"""
Dial — An Esoteric Programming Language for Music
Interpreter with lexer, parser, and lattice oscillator synthesis.

Usage:
    python dial_interpreter.py program.dial [-o output.wav] [--log log.json]
"""

import sys
import json
import math
import argparse
import struct
import wave
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum, auto


# ─── Constants ───────────────────────────────────────────────────────────────

SAMPLE_RATE = 44100
DEFAULT_TEMPO = 120
DEFAULT_DURATION = 1.0
DEFAULT_VOLUME = 0.7

# Tradition landmarks in (V, H, S) space
TRADITIONS = {
    "western":       (2.72, 2.05, 1.80),
    "carnatic":      (2.77, 3.63, 2.80),
    "jazz":          (2.30, 2.50, 2.10),
    "gamelan":       (1.40, 1.20, 2.90),
    "blues":         (2.10, 2.80, 1.60),
    "arabic":        (2.50, 3.10, 2.30),
    "japanese":      (1.80, 1.50, 2.20),
    "throat_singing": (2.90, 0.80, 3.00),
}

# The "random threshold" — consonance below this is anti-music
RANDOM_THRESHOLD = 0.15


# ─── Token Types ─────────────────────────────────────────────────────────────

class TokenType(Enum):
    DIAL_COMMAND = auto()
    LET = auto()
    JUMP = auto()
    IF_JUMP = auto()
    UNPLAYED = auto()
    REST = auto()
    TEMPO = auto()
    DURATION = auto()
    TRADITION = auto()
    VOLUME = auto()
    FADE = auto()
    COMMENT = auto()
    LABEL_DEF = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    line: int
    raw: str
    data: dict = field(default_factory=dict)


# ─── Lexer ───────────────────────────────────────────────────────────────────

class LexError(Exception):
    pass


def lex(source: str) -> List[Token]:
    """Tokenize dial source code."""
    tokens = []
    lines = source.split('\n')

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()

        if not stripped or stripped.startswith('#'):
            continue

        if stripped.startswith('V:') or stripped.startswith('v:'):
            # Dial command: V:{float} H:{float} S:{float} [label]
            tokens.append(_parse_dial_command(stripped, lineno))
        elif stripped.startswith('let '):
            tokens.append(_parse_let(stripped, lineno))
        elif stripped.startswith('->'):
            tokens.append(_parse_jump(stripped, lineno))
        elif stripped.startswith('if '):
            tokens.append(_parse_if(stripped, lineno))
        elif stripped == 'unplayed':
            tokens.append(Token(TokenType.UNPLAYED, lineno, stripped))
        elif stripped.startswith('rest '):
            dur = _parse_float_val(stripped[5:].strip())
            tokens.append(Token(TokenType.REST, lineno, stripped, {"duration": dur}))
        elif stripped.startswith('tempo '):
            bpm = _parse_float_val(stripped[6:].strip())
            tokens.append(Token(TokenType.TEMPO, lineno, stripped, {"bpm": bpm}))
        elif stripped.startswith('dur '):
            dur = _parse_float_val(stripped[4:].strip())
            tokens.append(Token(TokenType.DURATION, lineno, stripped, {"duration": dur}))
        elif stripped.startswith('tradition '):
            name = stripped[10:].strip()
            if name not in TRADITIONS:
                raise LexError(f"Line {lineno}: Unknown tradition '{name}'")
            tokens.append(Token(TokenType.TRADITION, lineno, stripped, {"name": name}))
        elif stripped.startswith('vol '):
            vol = _parse_float_val(stripped[4:].strip())
            tokens.append(Token(TokenType.VOLUME, lineno, stripped, {"volume": vol}))
        elif stripped.startswith('fade '):
            tokens.append(_parse_fade(stripped, lineno))
        else:
            raise LexError(f"Line {lineno}: Unrecognized syntax: '{stripped}'")

    tokens.append(Token(TokenType.EOF, len(lines) + 1, ""))
    return tokens


def _parse_dial_command(text: str, lineno: int) -> Token:
    """Parse V:x H:y S:z [label]"""
    parts = text.split()
    v = h = s = None
    label = None

    for part in parts:
        if part.upper().startswith('V:'):
            v = float(part[2:])
        elif part.upper().startswith('H:'):
            h = float(part[2:])
        elif part.upper().startswith('S:'):
            s = float(part[2:])
        else:
            # Could be a variable reference or a label
            label = part

    if v is None or h is None or s is None:
        raise LexError(f"Line {lineno}: Dial command needs V:, H:, and S: values")

    return Token(TokenType.DIAL_COMMAND, lineno, text, {
        "v_expr": v, "h_expr": h, "s_expr": s, "label": label
    })


def _parse_let(text: str, lineno: int) -> Token:
    """Parse let name = expression"""
    # let x = expr
    rest = text[4:].strip()
    eq_pos = rest.find('=')
    if eq_pos < 0:
        raise LexError(f"Line {lineno}: LET needs '='")
    name = rest[:eq_pos].strip()
    expr_str = rest[eq_pos + 1:].strip()
    return Token(TokenType.LET, lineno, text, {"name": name, "expr": expr_str})


def _parse_jump(text: str, lineno: int) -> Token:
    """Parse -> label"""
    label = text[2:].strip()
    return Token(TokenType.JUMP, lineno, text, {"label": label})


def _parse_if(text: str, lineno: int) -> Token:
    """Parse if expr op expr -> label"""
    rest = text[3:].strip()
    # Find -> at the end
    arrow_pos = rest.find('->')
    if arrow_pos < 0:
        raise LexError(f"Line {lineno}: IF needs '-> label'")

    condition = rest[:arrow_pos].strip()
    label = rest[arrow_pos + 2:].strip()

    # Parse condition: expr op expr
    ops = ['<=', '>=', '!=', '==', '<', '>']
    op = None
    left = right = None
    for o in ops:
        if o in condition:
            parts = condition.split(o, 1)
            if len(parts) == 2:
                left = parts[0].strip()
                op = o
                right = parts[1].strip()
                break

    if op is None:
        raise LexError(f"Line {lineno}: IF needs a comparison operator")

    return Token(TokenType.IF_JUMP, lineno, text, {
        "left": left, "op": op, "right": right, "label": label
    })


def _parse_fade(text: str, lineno: int) -> Token:
    """Parse fade target_vol beats"""
    parts = text[5:].strip().split()
    if len(parts) != 2:
        raise LexError(f"Line {lineno}: FADE needs target_vol and beats")
    return Token(TokenType.FADE, lineno, text, {
        "target": float(parts[0]),
        "beats": float(parts[1])
    })


def _parse_float_val(s: str) -> float:
    return float(s)


# ─── Expression Evaluator ───────────────────────────────────────────────────

def eval_expr(expr, variables: dict) -> float:
    """Evaluate a simple arithmetic expression with variable substitution."""
    if isinstance(expr, (int, float)):
        return float(expr)

    s = str(expr)
    # Substitute variables
    for name, val in sorted(variables.items(), key=lambda x: -len(x[0])):
        s = s.replace(name, str(val))

    # Only allow safe characters
    allowed = set('0123456789.+-*/() ')
    if not all(c in allowed for c in s):
        raise ValueError(f"Unsafe expression: {s}")

    try:
        return float(eval(s))  # Safe: only numbers and operators
    except Exception as e:
        raise ValueError(f"Expression evaluation failed: {s} — {e}")


# ─── Lattice Oscillator ─────────────────────────────────────────────────────

def consonance_score(v: float, h: float, s: float) -> float:
    """
    Compute consonance score for a position in (V, H, S) space.
    Higher = more consonant. Near traditions = higher.
    """
    min_dist = float('inf')
    for name, (tv, th, ts) in TRADITIONS.items():
        dist = math.sqrt((v - tv)**2 + (h - th)**2 + (s - ts)**2)
        min_dist = min(min_dist, dist)

    # Consonance is inverse of distance to nearest tradition
    # At the tradition center, consonance = 1.0
    # At distance 3+, consonance approaches 0
    score = max(0.0, 1.0 - (min_dist / 3.5))
    return score


def nearest_tradition(v: float, h: float, s: float) -> Tuple[str, float]:
    """Return the nearest tradition name and distance."""
    best_name = "unknown"
    best_dist = float('inf')
    for name, (tv, th, ts) in TRADITIONS.items():
        dist = math.sqrt((v - tv)**2 + (h - th)**2 + (s - ts)**2)
        if dist < best_dist:
            best_dist = dist
            best_name = name
    return best_name, best_dist


def position_to_freq(v: float, h: float, s: float) -> float:
    """Convert lattice position to a fundamental frequency."""
    # Base frequency from V axis (higher consonance = lower, more "resolved" freq)
    base = 220.0  # A3
    freq = base * (1.0 + (v - 1.5) * 0.3)
    # H adds micro-motion (detuning)
    freq *= (1.0 + (h - 1.5) * 0.05)
    # S shifts up an octave range
    freq *= (2.0 ** ((s - 1.5) * 0.3))
    return max(20.0, min(freq, 8000.0))


def synthesize_note(v: float, h: float, s: float, duration_sec: float,
                    volume: float = 0.7, sample_rate: int = SAMPLE_RATE,
                    tradition_hint: Optional[str] = None) -> List[float]:
    """
    Synthesize audio for a lattice position using additive synthesis.
    The consonance score determines harmonic content.
    """
    n_samples = int(duration_sec * sample_rate)
    if n_samples <= 0:
        return []

    score = consonance_score(v, h, s)
    freq = position_to_freq(v, h, s)

    # Apply tradition hint
    if tradition_hint and tradition_hint in TRADITIONS:
        tv, th, ts = TRADITIONS[tradition_hint]
        # Blend toward tradition tuning
        blend = 0.3
        freq = freq * (1 - blend) + position_to_freq(tv, th, ts) * blend

    samples = [0.0] * n_samples

    # Number of harmonics based on consonance
    # High consonance = clean harmonics, low = noise-like
    n_harmonics = max(1, int(score * 12) + 1)

    # Spectral brightness determines rolloff
    brightness = s / 3.0

    for t_idx in range(n_samples):
        t = t_idx / sample_rate
        sample = 0.0

        for harm in range(1, n_harmonics + 1):
            # Amplitude rolloff
            amp = 1.0 / (harm ** (1.5 - brightness))
            # Add slight inharmonicity for low consonance
            detune = 1.0 + (1.0 - score) * 0.02 * math.sin(harm * 0.7)
            harmonic_freq = freq * harm * detune
            sample += amp * math.sin(2.0 * math.pi * harmonic_freq * t)

        # Normalize by harmonic count
        if n_harmonics > 0:
            sample /= n_harmonics

        # H axis adds amplitude modulation (motion)
        mod_rate = 0.5 + h * 2.0  # LFO rate
        sample *= (0.7 + 0.3 * math.sin(2.0 * math.pi * mod_rate * t))

        # Envelope: attack-decay-sustain-release
        env = _envelope(t, duration_sec, attack=0.02, decay=0.1,
                        sustain=0.7, release=0.05)
        sample *= env * volume

        samples[t_idx] = sample

    return samples


def _envelope(t: float, dur: float, attack=0.02, decay=0.1,
              sustain=0.7, release=0.05) -> float:
    """Simple ADSR envelope."""
    if t < attack:
        return t / attack if attack > 0 else 1.0
    elif t < attack + decay:
        return 1.0 - (1.0 - sustain) * ((t - attack) / decay)
    elif t < dur - release:
        return sustain
    elif t < dur:
        return sustain * ((dur - t) / release) if release > 0 else 0.0
    return 0.0


# ─── Unplayed Region Finder ─────────────────────────────────────────────────

def find_unplayed(visited: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """
    Find the nearest unexplored region in the lattice.
    Samples random points and returns the one farthest from any visited point
    and any tradition landmark.
    """
    import random
    best_pos = (1.5, 1.5, 1.5)
    best_min_dist = 0.0

    all_points = list(visited) + list(TRADITIONS.values())

    for _ in range(500):
        v = random.uniform(0.0, 3.0)
        h = random.uniform(0.0, 3.0)
        s = random.uniform(0.0, 3.0)

        min_dist = float('inf')
        for pv, ph, ps in all_points:
            d = math.sqrt((v - pv)**2 + (h - ph)**2 + (s - ps)**2)
            min_dist = min(min_dist, d)

        if min_dist > best_min_dist:
            best_min_dist = min_dist
            best_pos = (v, h, s)

    return best_pos


# ─── Interpreter ─────────────────────────────────────────────────────────────

class DialInterpreter:
    def __init__(self, sample_rate: int = SAMPLE_RATE):
        self.sample_rate = sample_rate
        self.audio: List[float] = []
        self.log: List[dict] = []
        self.variables: Dict[str, float] = {}
        self.labels: Dict[str, int] = {}
        self.visited: List[Tuple[float, float, float]] = []
        self.tempo = DEFAULT_TEMPO
        self.note_duration = DEFAULT_DURATION
        self.volume = DEFAULT_VOLUME
        self.tradition_hint: Optional[str] = None

    def run(self, tokens: List[Token], max_iterations: int = 100000) -> None:
        """Execute a tokenized dial program."""
        # First pass: collect labels
        for idx, tok in enumerate(tokens):
            if tok.type == TokenType.DIAL_COMMAND and tok.data.get("label"):
                self.labels[tok.data["label"]] = idx

        # Second pass: execute
        pc = 0
        iterations = 0
        fade_state = None  # (target_vol, remaining_beats, start_vol, start_beat)

        while pc < len(tokens) and iterations < max_iterations:
            tok = tokens[pc]
            iterations += 1

            if tok.type == TokenType.EOF:
                break

            elif tok.type == TokenType.TEMPO:
                self.tempo = tok.data["bpm"]

            elif tok.type == TokenType.DURATION:
                self.note_duration = tok.data["duration"]

            elif tok.type == TokenType.VOLUME:
                self.volume = tok.data["volume"]

            elif tok.type == TokenType.FADE:
                fade_state = {
                    "target": tok.data["target"],
                    "beats_remaining": tok.data["beats"],
                    "total_beats": tok.data["beats"],
                    "start_vol": self.volume,
                }

            elif tok.type == TokenType.TRADITION:
                self.tradition_hint = tok.data["name"]

            elif tok.type == TokenType.REST:
                dur_sec = (60.0 / self.tempo) * tok.data["duration"]
                n_samples = int(dur_sec * self.sample_rate)
                self.audio.extend([0.0] * n_samples)

            elif tok.type == TokenType.LET:
                name = tok.data["name"]
                val = eval_expr(tok.data["expr"], self.variables)
                self.variables[name] = val

            elif tok.type == TokenType.DIAL_COMMAND:
                # Resolve values (may be variable references)
                v_raw = tok.data["v_expr"]
                h_raw = tok.data["h_expr"]
                s_raw = tok.data["s_expr"]

                # If string, try to evaluate as expression
                if isinstance(v_raw, str):
                    v = eval_expr(v_raw, self.variables)
                else:
                    # Could be a variable name
                    v = self.variables.get(str(v_raw), float(v_raw))

                if isinstance(h_raw, str):
                    h = eval_expr(h_raw, self.variables)
                else:
                    h = self.variables.get(str(h_raw), float(h_raw))

                if isinstance(s_raw, str):
                    s = eval_expr(s_raw, self.variables)
                else:
                    s = self.variables.get(str(s_raw), float(s_raw))

                dur_sec = (60.0 / self.tempo) * self.note_duration
                note_vol = self.volume

                # Apply fade if active
                if fade_state and fade_state["beats_remaining"] > 0:
                    progress = 1.0 - (fade_state["beats_remaining"] / fade_state["total_beats"])
                    note_vol = fade_state["start_vol"] + \
                        (fade_state["target"] - fade_state["start_vol"]) * progress
                    fade_state["beats_remaining"] -= self.note_duration
                    if fade_state["beats_remaining"] <= 0:
                        self.volume = fade_state["target"]
                        fade_state = None

                note_audio = synthesize_note(
                    v, h, s, dur_sec, volume=note_vol,
                    sample_rate=self.sample_rate,
                    tradition_hint=self.tradition_hint
                )

                self.audio.extend(note_audio)
                self.visited.append((v, h, s))

                # Log
                score = consonance_score(v, h, s)
                trad, dist = nearest_tradition(v, h, s)
                self.log.append({
                    "line": tok.line,
                    "position": {"v": round(v, 3), "h": round(h, 3), "s": round(s, 3)},
                    "consonance": round(score, 4),
                    "nearest_tradition": trad,
                    "distance_to_tradition": round(dist, 3),
                    "frequency_hz": round(position_to_freq(v, h, s), 1),
                    "is_anti_music": score < RANDOM_THRESHOLD,
                })

            elif tok.type == TokenType.UNPLAYED:
                pos = find_unplayed(self.visited)
                v, h, s = pos
                dur_sec = (60.0 / self.tempo) * self.note_duration
                note_audio = synthesize_note(
                    v, h, s, dur_sec, volume=self.volume,
                    sample_rate=self.sample_rate,
                    tradition_hint=self.tradition_hint
                )
                self.audio.extend(note_audio)
                self.visited.append(pos)

                score = consonance_score(v, h, s)
                trad, dist = nearest_tradition(v, h, s)
                self.log.append({
                    "line": tok.line,
                    "position": {"v": round(v, 3), "h": round(h, 3), "s": round(s, 3)},
                    "consonance": round(score, 4),
                    "nearest_tradition": trad,
                    "distance_to_tradition": round(dist, 3),
                    "frequency_hz": round(position_to_freq(v, h, s), 1),
                    "is_anti_music": score < RANDOM_THRESHOLD,
                    "unplayed": True,
                })

            elif tok.type == TokenType.JUMP:
                label = tok.data["label"]
                if label not in self.labels:
                    raise RuntimeError(f"Line {tok.line}: Unknown label '{label}'")
                pc = self.labels[label]
                continue

            elif tok.type == TokenType.IF_JUMP:
                left_val = eval_expr(tok.data["left"], self.variables)
                right_val = eval_expr(tok.data["right"], self.variables)
                op = tok.data["op"]
                condition = False
                if op == '<': condition = left_val < right_val
                elif op == '>': condition = left_val > right_val
                elif op == '<=': condition = left_val <= right_val
                elif op == '>=': condition = left_val >= right_val
                elif op == '==': condition = left_val == right_val
                elif op == '!=': condition = left_val != right_val

                if condition:
                    label = tok.data["label"]
                    if label not in self.labels:
                        raise RuntimeError(f"Line {tok.line}: Unknown label '{label}'")
                    pc = self.labels[label]
                    continue

            pc += 1

        if iterations >= max_iterations:
            print(f"Warning: hit iteration limit ({max_iterations})")

    def save_wav(self, path: str) -> None:
        """Save synthesized audio to WAV file."""
        # Normalize
        if not self.audio:
            print("Warning: no audio generated")
            return

        peak = max(abs(s) for s in self.audio) if self.audio else 1.0
        if peak == 0:
            peak = 1.0
        scale = 0.9 * 32767.0 / peak

        with wave.open(path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            for s in self.audio:
                val = int(max(-32767, min(32767, s * scale)))
                wf.writeframes(struct.pack('<h', val))

    def save_log(self, path: str) -> None:
        """Save consonance log to JSON."""
        with open(path, 'w') as f:
            json.dump(self.log, f, indent=2)

    def print_stats(self) -> None:
        """Print execution statistics."""
        if not self.log:
            print("No notes generated.")
            return

        scores = [entry["consonance"] for entry in self.log]
        anti = sum(1 for entry in self.log if entry.get("is_anti_music"))
        traditions_hit = set(entry["nearest_tradition"] for entry in self.log)

        print(f"\n=== Dial Execution Stats ===")
        print(f"Notes generated: {len(self.log)}")
        print(f"Avg consonance: {sum(scores)/len(scores):.4f}")
        print(f"Min/Max consonance: {min(scores):.4f} / {max(scores):.4f}")
        print(f"Anti-music notes: {anti}")
        print(f"Traditions visited: {', '.join(sorted(traditions_hit))}")
        print(f"Unique positions: {len(set(tuple(e['position'].values()) for e in self.log))}")


# ─── Visualization ───────────────────────────────────────────────────────────

def visualize(interpreter: DialInterpreter) -> None:
    """Show 3D plot of visited positions."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        print("matplotlib required for visualization: pip install matplotlib")
        return

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Plot tradition landmarks
    for name, (v, h, s) in TRADITIONS.items():
        ax.scatter(v, h, s, marker='*', s=200, c='gold', edgecolors='black')
        ax.text(v + 0.05, h + 0.05, s + 0.05, name, fontsize=8)

    # Plot visited positions
    if interpreter.log:
        xs = [e["position"]["v"] for e in interpreter.log]
        ys = [e["position"]["h"] for e in interpreter.log]
        zs = [e["position"]["s"] for e in interpreter.log]
        colors = [e["consonance"] for e in interpreter.log]
        sc = ax.scatter(xs, ys, zs, c=colors, cmap='viridis', s=50, alpha=0.8)
        plt.colorbar(sc, label='Consonance')

        # Draw path
        ax.plot(xs, ys, zs, 'gray', alpha=0.3, linewidth=0.5)

    ax.set_xlabel('V (Vertical Consonance)')
    ax.set_ylabel('H (Horizontal Motion)')
    ax.set_zlabel('S (Spectral Brightness)')
    ax.set_title('Dial Program — Path Through Consonance Space')

    plt.savefig('dial_visualization.png', dpi=150, bbox_inches='tight')
    print("Saved visualization to dial_visualization.png")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Dial language interpreter')
    parser.add_argument('source', help='Path to .dial source file')
    parser.add_argument('-o', '--output', default='output.wav', help='Output WAV file')
    parser.add_argument('--log', default=None, help='Output consonance log (JSON)')
    parser.add_argument('--sample-rate', type=int, default=SAMPLE_RATE)
    parser.add_argument('--visualize', action='store_true', help='Generate 3D plot')
    parser.add_argument('--stats', action='store_true', help='Print execution stats')
    args = parser.parse_args()

    with open(args.source, 'r') as f:
        source = f.read()

    print(f"Dial: Tokenizing {args.source}...")
    tokens = lex(source)
    print(f"  {len(tokens)} tokens")

    print("Dial: Executing...")
    interp = DialInterpreter(sample_rate=args.sample_rate)
    interp.run(tokens)

    print(f"Dial: Saving {args.output}...")
    interp.save_wav(args.output)

    if args.log:
        interp.save_log(args.log)
        print(f"  Log saved to {args.log}")

    if args.stats:
        interp.print_stats()

    if args.visualize:
        visualize(interp)

    print(f"Dial: Done. Audio duration: {len(interp.audio) / args.sample_rate:.2f}s")


if __name__ == '__main__':
    main()
