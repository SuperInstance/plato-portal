"""ConstraintOscilloscope — visualize the same constraint structure at 5 scales.

1. Sample level  — rendered audio waveform (lattice snap geometry)
2. Note level    — piano roll (pitch lattice & timing grid)
3. Phrase level  — holonomy trajectory (key drift, color-coded)
4. Piece level   — note density / structural arc
5. Lattice snap  — Eisenstein lattice snap visualization
"""

import json
import os
import sys
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


class ConstraintOscilloscope:
    """Multi-scale constraint visualizer."""

    def visualize_midi(
        self,
        midi_path: str,
        output_path: str = "constraint_scope.png",
        title: str | None = None,
        high_res: bool = False,
    ):
        """Full 5-panel visualization of a MIDI file.

        Args:
            midi_path: Path to the MIDI file.
            output_path: Where to save the PNG.
            title: Optional custom title.
            high_res: If True, output at 300 DPI instead of 150.
        """
        import mido

        mid = mido.MidiFile(midi_path)
        dpi = 300 if high_res else 150

        fig = plt.figure(figsize=(24, 16))
        base = os.path.basename(midi_path)
        fig.suptitle(
            title or f"Constraint Oscilloscope — {base}",
            fontsize=16,
            fontweight="bold",
        )
        gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.30)

        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_waveform(ax1, mid)

        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_piano_roll(ax2, mid)

        ax3 = fig.add_subplot(gs[1, 0])
        self._plot_holonomy(ax3, mid)

        ax4 = fig.add_subplot(gs[1, 1])
        self._plot_density(ax4, mid)

        # Panel 5: Eisenstein lattice snap
        ax5 = fig.add_subplot(gs[:, 2])
        self._plot_lattice_snap(ax5, mid)

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        return output_path

    # ------------------------------------------------------------------
    # Panel helpers
    # ------------------------------------------------------------------

    def _plot_waveform(self, ax, mid):
        """Panel 1: Rendered audio waveform showing lattice snap geometry."""
        # Lazy import so the module works even without constraint-synth installed
        try:
            cs_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "constraint-synth"
            )
            cs_path = os.path.abspath(cs_path)
            if cs_path not in sys.path:
                sys.path.insert(0, cs_path)
            from constraint_synth.synth import ConstraintSynth
            from constraint_synth.oscillator import LatticeOscillator

            synth = ConstraintSynth(oscillator=LatticeOscillator(lattice_shape="triangle"))
            notes = self._extract_notes(mid)[:4]
            if notes:
                segments = []
                for pitch, velocity, duration, _start in notes:
                    dur = max(duration, 0.01)
                    segments.append(synth.play_note(pitch, velocity, dur))
                signal = np.concatenate(segments)
                samples = min(4000, len(signal))
                t = np.arange(samples) / 44100 * 1000  # ms
                ax.plot(t, signal[:samples], linewidth=0.5, color="#2196F3")
                ax.set_title("Sample Level — Lattice Snap Geometry", fontsize=12)
                ax.set_xlabel("Time (ms)")
                ax.set_ylabel("Amplitude")
                ax.axhline(y=0, color="gray", linewidth=0.3)
                ax.set_ylim(-1.2, 1.2)
                return
        except Exception as exc:
            pass  # fall through to fallback

        # Fallback: synthetic waveform from note data
        notes = self._extract_notes(mid)[:8]
        if not notes:
            ax.text(0.5, 0.5, "No notes found", ha="center", va="center",
                    transform=ax.transAxes)
            ax.set_title("Sample Level — Lattice Snap Geometry", fontsize=12)
            return

        sr = 44100
        max_dur = sum(max(n[2], 0.01) for n in notes)
        total_samples = int(sr * max_dur)
        signal = np.zeros(total_samples)
        pos = 0
        for pitch, vel, dur, _ in notes:
            dur = max(dur, 0.01)
            freq = 440.0 * (2 ** ((pitch - 69) / 12.0))
            n = int(sr * dur)
            t = np.arange(n) / sr
            tone = np.sin(2 * np.pi * freq * t) * (vel / 127.0)
            end = min(pos + n, total_samples)
            signal[pos:end] += tone[: end - pos]
            pos = end

        samples = min(4000, len(signal))
        t_ms = np.arange(samples) / sr * 1000
        ax.plot(t_ms, signal[:samples], linewidth=0.5, color="#2196F3")
        ax.set_title("Sample Level — Waveform (synthetic fallback)", fontsize=12)
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Amplitude")
        ax.axhline(y=0, color="gray", linewidth=0.3)

    def _plot_piano_roll(self, ax, mid):
        """Panel 2: Piano roll showing note-level constraint (pitch quantization)."""
        notes = self._extract_notes(mid)
        if not notes:
            ax.text(0.5, 0.5, "No notes found", ha="center", va="center",
                    transform=ax.transAxes)
            ax.set_title("Note Level — Pitch Lattice & Timing Grid", fontsize=12)
            return

        for pitch, velocity, duration, start in notes:
            color = plt.cm.viridis(velocity / 127)
            ax.barh(
                pitch,
                duration * 1000,
                left=start * 1000,
                height=0.8,
                color=color,
                edgecolor="none",
                alpha=0.8,
            )

        ax.set_title("Note Level — Pitch Lattice & Timing Grid", fontsize=12)
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("MIDI Pitch")

        pitches = [n[0] for n in notes]
        ax.set_ylim(min(pitches) - 2, max(pitches) + 2)

        # C-major scale degree grid lines
        for note in range(min(pitches) - 2, max(pitches) + 3):
            pc = note % 12
            if pc in (0, 2, 4, 5, 7, 9, 11):
                ax.axhline(y=note, color="red", linewidth=0.3, alpha=0.4)

    def _plot_holonomy(self, ax, mid):
        """Panel 3: Holonomy trajectory showing phrase-level key drift."""
        notes = self._extract_notes(mid)
        if not notes:
            ax.text(0.5, 0.5, "No notes found", ha="center", va="center",
                    transform=ax.transAxes)
            ax.set_title("Phrase Level — Holonomy (Key Drift)", fontsize=12)
            return

        # Pitch-class distance from C (0) — cumulative drift
        key_center_pc = 0  # C
        drifts = [(n[0] % 12 - key_center_pc) for n in notes]
        cumulative = np.cumsum(drifts).astype(float)
        # Detrend so we see winding, not linear growth
        x = np.arange(len(cumulative))
        if len(x) > 1:
            slope = cumulative[-1] / (len(cumulative) - 1)
            cumulative -= x * slope

        times_ms = [n[3] * 1000 for n in notes]

        # Color-code by distance from tonic (key center)
        cmap = plt.cm.coolwarm
        abs_drift = np.abs(cumulative)
        max_drift = abs_drift.max() if abs_drift.max() > 0 else 1.0
        norm_drift = abs_drift / max_drift  # 0=tonic(blue), 1=far(red)

        # Plot as colored segments
        for i in range(len(times_ms) - 1):
            color = cmap(norm_drift[i])
            ax.plot(times_ms[i:i+2], cumulative[i:i+2], linewidth=1.5, color=color)

        # Add colorbar
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, max_drift))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label("|Drift| from tonic (semitones)")

        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.set_title("Phrase Level — Holonomy (Key Drift)", fontsize=12)
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Cumulative Drift (semitones)")

    def _plot_density(self, ax, mid):
        """Panel 4: Note density over time showing structural arc."""
        notes = self._extract_notes(mid)
        if not notes:
            ax.text(0.5, 0.5, "No notes found", ha="center", va="center",
                    transform=ax.transAxes)
            ax.set_title("Piece Level — Constraint Density (Structural Arc)", fontsize=12)
            return

        max_time = max(n[3] + n[2] for n in notes)
        n_bins = max(20, int(max_time / 0.2))  # ~200ms windows minimum
        n_bins = min(n_bins, 100)
        window = max_time / n_bins
        bins = np.linspace(0, max_time, n_bins + 1)

        note_counts = np.zeros(n_bins)
        velocities = np.zeros(n_bins)
        for pitch, vel, dur, start in notes:
            idx = min(int(start / window), n_bins - 1)
            note_counts[idx] += 1
            velocities[idx] += vel

        centers = (bins[:-1] + bins[1:]) / 2 * 1000  # ms
        ax.bar(centers, note_counts, width=window * 1000 * 0.8,
               color="#4CAF50", alpha=0.7, label="note count")

        # Overlay average velocity as line
        with np.errstate(invalid="ignore", divide="ignore"):
            avg_vel = np.where(note_counts > 0, velocities / note_counts, 0)
        ax2 = ax.twinx()
        ax2.plot(centers, avg_vel, color="#FF9800", linewidth=1.5, alpha=0.8,
                 label="avg velocity")
        ax2.set_ylabel("Avg Velocity", color="#FF9800")
        ax2.tick_params(axis="y", labelcolor="#FF9800")

        ax.set_title("Piece Level — Constraint Density (Structural Arc)", fontsize=12)
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Notes per window")

    def _plot_lattice_snap(self, ax, mid):
        """Panel 5: Eisenstein lattice snap — input points vs snapped lattice points."""
        notes = self._extract_notes(mid)
        if not notes:
            ax.text(0.5, 0.5, "No notes found", ha="center", va="center",
                    transform=ax.transAxes)
            ax.set_title("Lattice Snap — Eisenstein", fontsize=12)
            return

        # Eisenstein lattice: basis vectors 1 and e^(2πi/3)
        # Map (pitch, time) to 2D lattice coordinates
        omega = np.exp(2j * np.pi / 3)  # primitive 3rd root of unity
        e1 = np.array([1.0, 0.0])
        e2 = np.array([omega.real, omega.imag])

        # Normalize inputs to a reasonable range
        pitches = np.array([n[0] for n in notes], dtype=float)
        times = np.array([n[3] for n in notes], dtype=float)

        p_min, p_max = pitches.min(), pitches.max()
        t_min, t_max = times.min(), times.max()
        p_range = p_max - p_min if p_max > p_min else 1.0
        t_range = t_max - t_min if t_max > t_min else 1.0

        # Input points (normalized to [0,1] range)
        input_pts = np.column_stack([
            (pitches - p_min) / p_range,
            (times - t_min) / t_range
        ])

        # Snap to Eisenstein lattice: for each point, find nearest lattice point
        # Lattice generated by e1, e2 over integers
        snapped = np.zeros_like(input_pts)
        for i, (x, y) in enumerate(input_pts):
            # Express in lattice coords: (x, y) ≈ a*e1 + b*e2
            # Solve [e1 | e2] * [a, b]^T = [x, y]^T
            basis = np.column_stack([e1, e2])
            coords = np.linalg.solve(basis, np.array([x, y]))
            a_round, b_round = np.round(coords).astype(int)
            snapped[i] = a_round * e1 + b_round * e2

        # Plot input points (blue) and snapped points (red) with connecting lines
        ax.scatter(input_pts[:, 0], input_pts[:, 1], c="#2196F3", s=30,
                   alpha=0.8, label="Input", zorder=3)
        ax.scatter(snapped[:, 0], snapped[:, 1], c="#F44336", s=50,
                   alpha=0.8, marker="x", label="Lattice snap", zorder=3, linewidths=2)

        for i in range(len(input_pts)):
            ax.plot([input_pts[i, 0], snapped[i, 0]],
                    [input_pts[i, 1], snapped[i, 1]],
                    color="gray", linewidth=0.5, alpha=0.5)

        # Draw lattice grid in the background
        lat_range = np.linspace(-0.2, 1.2, 8)
        for a in range(-1, 3):
            for b in range(-1, 3):
                pt = a * e1 + b * e2
                if -0.3 <= pt[0] <= 1.3 and -0.3 <= pt[1] <= 1.3:
                    ax.plot(pt[0], pt[1], ".", color="lightgray", markersize=3)

        ax.set_title("Lattice Snap — Eisenstein", fontsize=12)
        ax.set_xlabel("Pitch (normalized)")
        ax.set_ylabel("Time (normalized)")
        ax.legend(loc="upper left", fontsize=9)
        ax.set_aspect("equal")

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_data(self, midi_path: str) -> str:
        """Export visualization data as JSON.

        Returns a JSON string containing all panel data extracted from the MIDI file.
        """
        import mido

        mid = mido.MidiFile(midi_path)
        notes = self._extract_notes(mid)

        data = {
            "source": os.path.basename(midi_path),
            "note_count": len(notes),
            "notes": [
                {
                    "pitch": int(p),
                    "velocity": int(v),
                    "duration_sec": round(d, 6),
                    "start_sec": round(s, 6),
                }
                for p, v, d, s in notes
            ],
            "holonomy": self._compute_holonomy_data(notes),
            "density": self._compute_density_data(notes),
            "lattice_snap": self._compute_lattice_data(notes),
        }
        return json.dumps(data, indent=2)

    def _compute_holonomy_data(self, notes):
        """Compute holonomy trajectory data for JSON export."""
        if not notes:
            return {"times_ms": [], "drift": [], "abs_drift": []}
        key_center_pc = 0
        drifts = [(n[0] % 12 - key_center_pc) for n in notes]
        cumulative = np.cumsum(drifts).astype(float)
        x = np.arange(len(cumulative))
        if len(x) > 1:
            slope = cumulative[-1] / (len(cumulative) - 1)
            cumulative -= x * slope
        return {
            "times_ms": [round(n[3] * 1000, 3) for n in notes],
            "drift": [round(float(c), 6) for c in cumulative],
            "abs_drift": [round(float(abs(c)), 6) for c in cumulative],
        }

    def _compute_density_data(self, notes):
        """Compute note density data for JSON export."""
        if not notes:
            return {"bins_ms": [], "counts": [], "avg_velocity": []}
        max_time = max(n[3] + n[2] for n in notes)
        n_bins = min(max(20, int(max_time / 0.2)), 100)
        window = max_time / n_bins
        bins = np.linspace(0, max_time, n_bins + 1)
        counts = np.zeros(n_bins)
        velocities = np.zeros(n_bins)
        for p, v, d, s in notes:
            idx = min(int(s / window), n_bins - 1)
            counts[idx] += 1
            velocities[idx] += v
        with np.errstate(invalid="ignore", divide="ignore"):
            avg_vel = np.where(counts > 0, velocities / counts, 0)
        return {
            "bins_ms": [round(float(b * 1000), 3) for b in (bins[:-1] + bins[1:]) / 2],
            "counts": [int(c) for c in counts],
            "avg_velocity": [round(float(v), 2) for v in avg_vel],
        }

    def _compute_lattice_data(self, notes):
        """Compute Eisenstein lattice snap data for JSON export."""
        if not notes:
            return {"input": [], "snapped": []}
        omega = np.exp(2j * np.pi / 3)
        e1 = np.array([1.0, 0.0])
        e2 = np.array([omega.real, omega.imag])
        basis = np.column_stack([e1, e2])

        pitches = np.array([n[0] for n in notes], dtype=float)
        times = np.array([n[3] for n in notes], dtype=float)
        p_min, p_max = pitches.min(), pitches.max()
        t_min, t_max = times.min(), times.max()
        p_range = p_max - p_min if p_max > p_min else 1.0
        t_range = t_max - t_min if t_max > t_min else 1.0

        input_pts = np.column_stack([(pitches - p_min) / p_range, (times - t_min) / t_range])
        snapped = []
        for x, y in input_pts:
            coords = np.linalg.solve(basis, np.array([x, y]))
            a_r, b_r = int(np.round(coords[0])), int(np.round(coords[1]))
            pt = a_r * e1 + b_r * e2
            snapped.append([round(float(pt[0]), 6), round(float(pt[1]), 6)])

        return {
            "input": [[round(float(x), 6), round(float(y), 6)] for x, y in input_pts],
            "snapped": snapped,
        }

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_notes(mid):
        """Extract (pitch, velocity, duration_sec, start_sec) from a MIDI file."""
        ticks_per_beat = mid.ticks_per_beat
        tempo = 500000  # default 120 BPM
        for track in mid.tracks:
            for msg in track:
                if msg.type == "set_tempo":
                    tempo = msg.tempo
                    break

        sec_per_tick = tempo / (ticks_per_beat * 1_000_000)
        notes = []

        for track in mid.tracks:
            abs_tick = 0
            note_ons = {}
            for msg in track:
                abs_tick += msg.time
                if msg.type == "note_on" and msg.velocity > 0:
                    note_ons[msg.note] = (abs_tick, msg.velocity)
                elif msg.type == "note_off" or (
                    msg.type == "note_on" and msg.velocity == 0
                ):
                    if msg.note in note_ons:
                        start_tick, vel = note_ons.pop(msg.note)
                        start_sec = start_tick * sec_per_tick
                        dur_sec = (abs_tick - start_tick) * sec_per_tick
                        notes.append((msg.note, vel, dur_sec, start_sec))

        return sorted(notes, key=lambda n: n[3])
