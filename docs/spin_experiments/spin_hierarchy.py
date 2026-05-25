#!/usr/bin/env python3
"""Experiment 3: Spin hierarchy — music as nested spins at multiple timescales."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json

OUT = os.path.dirname(__file__)

SR = 44100
DUR = 10.0  # 10 seconds
t = np.linspace(0, DUR, int(SR*DUR), endpoint=False)

# --- Generate a simple Bach-style chorale: 4 voices, chord progression ---
def note_freq(name):
    """Convert note name to frequency."""
    notes = {'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11}
    base = name[:-1]
    octave = int(name[-1])
    midi = (octave+1)*12 + notes[base]
    return 440.0 * 2**((midi-69)/12)

# Simple chorale progression (one chord per ~1.25s)
chords = [
    [('C4',0.4), ('E4',0.3), ('G4',0.3), ('C5',0.2)],   # C major
    [('A3',0.35), ('C4',0.3), ('E4',0.3), ('A4',0.2)],   # A minor
    [('F3',0.35), ('A3',0.3), ('C4',0.3), ('F4',0.2)],   # F major
    [('G3',0.35), ('B3',0.3), ('D4',0.3), ('G4',0.2)],   # G major
    [('C4',0.4), ('E4',0.3), ('G4',0.3), ('C5',0.2)],   # C major
    [('D4',0.35), ('F4',0.3), ('A4',0.3), ('D5',0.15)],  # D minor
    [('G3',0.35), ('B3',0.3), ('D4',0.3), ('G4',0.2)],   # G major
    [('C4',0.4), ('E4',0.3), ('G4',0.3), ('C5',0.2)],   # C major
]

# Generate signal
signal = np.zeros_like(t)
chord_dur = DUR / len(chords)

for i, chord in enumerate(chords):
    start = i * chord_dur
    end = (i+1) * chord_dur
    mask = (t >= start) & (t < end)
    t_chord = t[mask] - start
    
    for note_name, amp in chord:
        freq = note_freq(note_name)
        # Add harmonics for richer sound
        for h in range(1, 6):
            harmonic_amp = amp / h
            phase = 2 * np.pi * freq * h
            # Envelope: gentle attack/release
            env = np.minimum(t_chord / 0.02, 1.0) * np.minimum((chord_dur - t_chord) / 0.02, 1.0)
            env = np.clip(env, 0, 1)
            signal[mask] += harmonic_amp * env * np.sin(phase * t_chord + np.random.uniform(0, 2*np.pi))

# Normalize
signal = signal / np.max(np.abs(signal)) * 0.8

# --- FFT at multiple timescales ---
windows = {
    'Tone (20ms)': 0.020,
    'Note (200ms)': 0.200,
    'Phrase (2s)': 2.0,
    'Section (10s)': 10.0,
}

# Pick analysis point at 3s (middle of piece)
analysis_time = 3.0
fig, axes = plt.subplots(2, 2, figsize=(14, 10), tight_layout=True)
hierarchy_data = {}

for ax, (label, win_dur) in zip(axes.flat, windows.items()):
    win_samples = int(win_dur * SR)
    center = int(analysis_time * SR)
    start = max(0, center - win_samples // 2)
    end = min(len(signal), start + win_samples)
    chunk = signal[start:end]
    
    # Apply Hann window
    window = np.hanning(len(chunk))
    chunk_windowed = chunk * window
    
    # FFT
    fft = np.fft.rfft(chunk_windowed)
    freqs = np.fft.rfftfreq(len(chunk_windowed), 1/SR)
    magnitudes = np.abs(fft)
    
    # Limit display range
    if win_dur <= 0.02:
        freq_mask = (freqs > 50) & (freqs < 5000)
        xlabel = 'Frequency (Hz)'
    elif win_dur <= 0.2:
        freq_mask = (freqs > 20) & (freqs < 2000)
        xlabel = 'Frequency (Hz)'
    else:
        freq_mask = (freqs > 1) & (freqs < 500)
        xlabel = 'Frequency (Hz)'
    
    ax.plot(freqs[freq_mask], magnitudes[freq_mask], color='steelblue', lw=0.8)
    ax.set_title(f'{label} — Window = {win_dur*1000:.0f}ms')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('|FFT|')
    
    # Find dominant frequencies
    top_k = 5
    valid_mags = magnitudes[freq_mask]
    valid_freqs = freqs[freq_mask]
    top_indices = np.argsort(valid_mags)[-top_k:][::-1]
    dominant = [(float(valid_freqs[i]), float(valid_mags[i])) for i in top_indices if valid_mags[i] > 0.01]
    
    for f, m in dominant[:3]:
        ax.axvline(f, color='red', alpha=0.3, lw=0.8)
    
    hierarchy_data[label] = {
        "window_ms": win_dur * 1000,
        "dominant_freqs_hz": dominant,
        "n_fft_bins": len(fft),
        "freq_resolution_hz": float(SR / len(chunk_windowed))
    }

plt.suptitle('Spin Hierarchy: Same Mathematics at Every Timescale', fontsize=14, y=1.02)
plt.savefig(os.path.join(OUT, 'spin_hierarchy.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ spin_hierarchy.png")

# --- Multi-timescale spectrogram ---
fig, ax = plt.subplots(figsize=(14, 6))
# Use a moderate window for overview
from scipy.signal import spectrogram
f_sg, t_sg, Sxx = spectrogram(signal, SR, nperseg=2048, noverlap=1536)
freq_mask = (f_sg > 50) & (f_sg < 2000)
ax.pcolormesh(t_sg, f_sg[freq_mask], 10*np.log10(Sxx[freq_mask] + 1e-10), shading='gouraud', cmap='magma')
ax.set_ylabel('Frequency (Hz) — Spin Rate')
ax.set_xlabel('Time (s)')
ax.set_title('Spectrogram: Spins at All Rates Visible Simultaneously')
plt.colorbar(ax.collections[0], label='Power (dB)')
plt.savefig(os.path.join(OUT, 'spin_spectrogram.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ spin_spectrogram.png")

# --- Save data ---
with open(os.path.join(OUT, 'spin_hierarchy.json'), 'w') as f:
    json.dump(hierarchy_data, f, indent=2)

print("\n✅ Experiment 3 complete: spin_hierarchy")
